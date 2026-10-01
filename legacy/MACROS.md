# Macro Catalog

These placeholders replace instance-specific values found in the original local skill set.

| Macro | Meaning |
| --- | --- |
| `${LOCAL_HOME}` | Local home directory root |
| `${LOCAL_USER}` | Local workstation username |
| `${OBS_BASE_URL}` | OBS base URL |
| `${OBS_HOST}` | OBS hostname without scheme |
| `${OBS_USER}` | OBS home-project namespace user |
| `${VALIDATION_BRANCH}` | Validation branch or topic name |
| `${OBS_HOME_PROJECT}` | Fully qualified OBS home project name |
| `${OBS_RELEASE_REPO_X86_64}` | OBS release repository path for `x86_64` |
| `${OBS_RELEASE_REPO_RISCV64}` | OBS release repository path for `riscv64` |
| `${GIT_HOST}` | Git hosting domain |
| `${GIT_FORK_USER}` | Git fork namespace/user |
| `${DISTRO_REPO_NAME}` | Distribution repository name |
| `${GIT_REVISION}` | Exact Git revision used for validation |
| `${VALIDATION_PACKAGES}` | Example package set used in validation examples |
| `${DOWNSTREAM_PACKAGES}` | Example dependent package set used in rebuild examples |

## Suggested Safe Defaults

```env
OBS_BASE_URL=https://obs.example.invalid
OBS_HOST=obs.example.invalid
OBS_USER=example-user
VALIDATION_BRANCH=example-branch
OBS_HOME_PROJECT=home:example-user:example-branch
OBS_RELEASE_REPO_X86_64=target/x86_64
OBS_RELEASE_REPO_RISCV64=target/riscv64
GIT_HOST=github.com
GIT_FORK_USER=example-user
DISTRO_REPO_NAME=openRuyi
GIT_REVISION=<exact-commit-sha>
VALIDATION_PACKAGES="pkg-a pkg-b pkg-c"
DOWNSTREAM_PACKAGES="pkg-d pkg-e"
```

