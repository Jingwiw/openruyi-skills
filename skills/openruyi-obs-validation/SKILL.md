---
name: openruyi-obs-validation
description: Validate an openRuyi Git branch in OBS by creating or reconciling a home project, pinning package services to an exact Git commit in a GitHub fork, triggering builds, classifying OBS failures, and reporting what is a branch regression versus an upstream repo-capability gap. Use when working against ${OBS_HOST} for branch verification or when turning an ad hoc OBS validation run into a repeatable procedure.
---

# openRuyi OBS Validation

Use this skill when the task is to validate an `openRuyi` branch in OBS, especially in a `${OBS_HOME_PROJECT}` project.

## Workflow

1. Read the local Git context first.
   - Get the branch name with `git branch --show-current`.
   - Get the exact commit with `git rev-parse HEAD`.
   - Get the fork URL with `git remote get-url origin`.
   - Derive the affected package list from `git diff --name-only $(git merge-base main HEAD)..HEAD | cut -d/ -f2 | sort -u`.
   - If the branch changes foundational sysusers ownership or shared runtime identities, add a small set of related packages for blast-radius checks.
   - Example: when validating `system-user-root` changes, also add `fuse` because it has `Requires(pre): group(trusted)`.

2. Prefer exact commit pinning over branch-name pinning.
   - OBS `obs_scm` supports using a Git revision directly.
   - For validation, set `<param name="revision">` to the exact commit SHA, not just the branch name.
   - This makes the result reproducible and avoids later branch drift.
   - Resolve the full SHA directly from local Git with `git rev-parse HEAD`; do not hand-copy a partial or remembered 40-byte value.

3. Use OBS HTTP API with `curl` if `osc` is unavailable.
   - Keep credentials out of the command line when possible.
   - Create a temporary netrc file and pass `--netrc-file`.
   - Delete the temp credential file before handoff if it is no longer needed.

4. Reconcile the project before touching packages.
   - Read `${OBS_BASE_URL}/source/<project>/_meta`.
   - For validation-only home projects, keep `build` enabled and `publish` disabled.
   - Keep repository paths pointed at `${OBS_RELEASE_REPO_X86_64}` and `${OBS_RELEASE_REPO_RISCV64}` unless the task explicitly requires other repos.

5. Reconcile each package source entry.
   - Read `.../source/<project>/<package>`.
   - Read `.../source/<project>/<package>/_meta`.
   - Read `.../source/<project>/<package>/_service`.
   - If the package already exists, update `_service` in place.
   - If the package is missing, create a minimal package `_meta` first. On this OBS instance, uploading `_service` to a missing package returns `unknown_package`.
   - After package creation, create or repair `_service` so it pulls `SPECS/<package>/*` from the GitHub fork.
   - On this OBS instance, prefer enabling `download_assets` by default.
   - Even some local-source packages have shown transient or persistent service failures when `download_assets` was omitted.
   - Reserve `download_assets=no` for narrow debugging only.
   - A minimal package `_meta` shape is:

```xml
<package name="<package>" project="<project>">
  <title><package></title>
  <description>Validation package for <branch> at <exact-commit-sha></description>
</package>
```
   - A standard service shape is:

```xml
<services>
  <service name="obs_scm" mode="trylocal">
    <param name="scm">git</param>
    <param name="url">https://${GIT_HOST}/<user>/${DISTRO_REPO_NAME}/</param>
    <param name="revision"><exact-commit-sha></param>
    <param name="exclude">*</param>
    <param name="extract">SPECS/<package>/*</param>
  </service>
</services>
```

   - The reliable default is to append:

```xml
  <service name="download_assets" mode="trylocal"></service>
```

6. Refresh sources after updating `_service`.
   - Call `POST /source/<project>/<package>?cmd=runservice`.
   - Do not assume updating `_service` alone is enough.
   - Re-check the package directory and confirm the new `_service` revision is visible.
   - After bulk `runservice`, expect many packages to stay in `blocked` with `service in progress` for a while; this is transitional.

7. Poll build results from the project level.
   - Use `GET /build/<project>/_result`.
   - Track both `x86_64` and `riscv64`.
   - Expect transitional states like `blocked`, `scheduled`, `building`, and `service in progress`.

8. Classify failures instead of flattening them.
   - `unresolvable` with missing packages or capabilities is usually a repo-capability gap, not a branch regression.
   - `blocked` on another package in the same project is usually build-order dependency, not a spec bug.
   - `%check` failures and timeouts need log inspection before deciding they are branch regressions.
   - Use `.../build/<project>/<repo>/<arch>/<package>/_log?start=0` for logs.
   - When the change updates foundational sysusers providers but keeps the same NEVR in OBS, downstream `rebuild` results can be misleading because cached build roots may retain the old provider payloads.
   - For confirmation runs of downstreams after `setup`, `dbus`, `system-user-root`, or similar provider changes, prefer `wipe + rebuild` before reading log warnings.
   - When logs show `systemd-tmpfiles` failures such as `Failed to resolve user 'lp'`, check whether the referenced account is supposed to come from a foundational provider.
   - If `SPECS/setup/uidgid` claims a base account but `setup-build.sysusers` or `setup.sysusers` omit it, fix `setup` first instead of duplicating the account in consumer packages.
   - After fixing that provider drift, rebuild the provider first and then `wipe + rebuild` the affected consumers for a fresh verdict.
   - openRuyi currently disables rpm native sysusers handling in `SPECS/rpm/rpm.spec` by removing `sysusers.sh` and masking `%__systemd_sysusers`; do not assume packaged `sysusers.d` alone will create pre-unpack accounts or auto-provide `user()`/`group()` capabilities in this distro.
   - While that distro-level disable remains in place, keep `%sysusers_create_package` in `%pre` for affected packages and keep explicit `Provides: user(...)`/`group(...)` glue when another package depends on a shared identity such as `messagebus`.
   - After reassigning a shared account provider, inspect fresh build logs for upstream-installed sysusers files that still land in the buildroot, for example `/usr/lib/sysusers.d/dbus.conf`.
   - If upstream still installs a sysusers file after the spec stops packaging it, OBS may fail with `Installed (but unpackaged) file(s) found`; either package that file intentionally or disable/remove the upstream install path consistently.

9. Report validation in three buckets.
   - `Succeeded`: packages built successfully for the target arch/repo.
   - `Infra or repo gap`: package cannot build because OBS or the project lacks required dependencies.
   - `Branch regression`: package fails because the branch changes introduced a real build or test failure.

## API Endpoints

- Project meta: `/source/<project>/_meta`
- Project config: `/source/<project>/_config`
- Package directory: `/source/<project>/<package>`
- Package meta: `/source/<project>/<package>/_meta`
- Package service file: `/source/<project>/<package>/_service`
- Run services: `POST /source/<project>/<package>?cmd=runservice`
- Build results: `/build/<project>/_result`
- Build log: `/build/<project>/<repository>/<arch>/<package>/_log?start=0`
- Package search: `/search/package/id?match=...`

## Good Defaults

- Name the validation project `${OBS_HOME_PROJECT}`.
- Disable `publish` for validation projects.
- Pin packages to the exact Git commit being validated.
- Create missing packages with a minimal `_meta`, then upload `_service`, then `runservice`.
- When the change touches shared sysusers providers, include 1-3 dependent packages to test downstream impact.
- Keep the project summary factual and short.
- Reuse existing project/package state when it is already mostly correct.

## Scripts

- `scripts/render_service.sh`
  - Render a package `_service` file.
  - The reliable default on this OBS instance is to enable `download_assets` by default.
  - Reserve `download_assets=no` for narrow debugging only.
- `scripts/render_package_meta.sh`
  - Render a minimal package `_meta` for missing packages in a home project.
- `scripts/sync_project.sh`
  - Do a full package sync-and-trigger pass for an OBS home project.
  - It creates missing package `_meta`, uploads `_service`, and calls `runservice`.
  - Required env: `OBS_NETRC_FILE`
  - Optional env: `OBS_BASE_URL` (default `${OBS_BASE_URL}`)
  - Usage:

```sh
OBS_NETRC_FILE=/tmp/obs-netrc \
scripts/sync_project.sh ${OBS_HOME_PROJECT} ${GIT_FORK_USER} ${GIT_REVISION} ${VALIDATION_PACKAGES}
```
- `scripts/wipe_rebuild.sh`
  - Wipe prior build state and immediately queue a rebuild for the selected packages.
  - Use this after changing foundational sysusers providers while package NEVR stays the same.
  - Required env: `OBS_NETRC_FILE`
  - Optional env: `OBS_BASE_URL` (default `${OBS_BASE_URL}`)
  - Usage:

```sh
OBS_NETRC_FILE=/tmp/obs-netrc \
scripts/wipe_rebuild.sh ${OBS_HOME_PROJECT} x86_64 x86_64 ${DOWNSTREAM_PACKAGES}
```
- `scripts/scan_sysusers_logs.sh`
  - Scan package build logs for sysusers-related warnings, conflicts, and unresolved users/groups.
  - It can scan an explicit package list or every package currently present in the project.
  - Required env: `OBS_NETRC_FILE`
  - Optional env: `OBS_BASE_URL` (default `${OBS_BASE_URL}`)
  - Usage:

```sh
OBS_NETRC_FILE=/tmp/obs-netrc \
scripts/scan_sysusers_logs.sh ${OBS_HOME_PROJECT} x86_64 x86_64
```

## Notes

- `openruyi` package sources often mix service-only packages and branch-link packages; inspect instead of assuming one layout.
- A project-level `_meta` can be created successfully while every package PUT still fails with `unknown_package`; package creation is separate.
- If one package in the set produces a subpackage needed by another package in the same validation project, allow scheduler blocking to clear before calling it a failure.
- If the requested external docs are unavailable or stale, rely on the live OBS API behavior and note the gap in the final handoff.
