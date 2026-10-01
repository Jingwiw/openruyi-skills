#!/usr/bin/env python3
"""Run one Docker experiment; persist output and verify exact-container cleanup."""
import argparse
import json
import re
import subprocess
import time
import uuid
from pathlib import Path


def execute(image, platform, inputs, output, command, network="none", timeout=600):
    inputs, output = Path(inputs).resolve(), Path(output).resolve()
    if not inputs.is_dir() or not re.fullmatch(r".+@sha256:[0-9a-f]{64}", image):
        raise ValueError("existing input directory and digest-pinned image required")
    if not command or timeout <= 0 or output == inputs or ',' in str(inputs) or ',' in str(output):
        raise ValueError("command, positive timeout and distinct mount-safe paths required")
    output.mkdir(parents=True, exist_ok=False)
    result = dict(image=image, platform=platform, inputs=str(inputs), command=command,
                  events=[], experiment_exit=None, cleanup_verified=False)
    name = "skill-experiment-" + uuid.uuid4().hex
    cid = None

    def call(args, limit=30):
        p = subprocess.run(["docker", *args], capture_output=True, timeout=limit)
        event = dict(command=["docker", *args], stdout=p.stdout.decode(errors="replace"),
                     stderr=p.stderr.decode(errors="replace"), exit_status=p.returncode)
        result["events"].append(event)
        return p

    try:
        created = call(["create", "--name", name, "--pull=never", "--platform", platform,
                        "--network", network, "--mount", f"type=bind,src={inputs},dst=/input,readonly",
                        "--mount", f"type=bind,src={output},dst=/output", image, *command])
        if created.returncode:
            raise RuntimeError("docker create failed; see events")
        cid = created.stdout.decode().strip()
        if not re.fullmatch(r"[0-9a-f]{64}", cid):
            raise RuntimeError("docker create returned no valid container ID")
        result["container_id"] = cid
        try:
            p = call(["start", "--attach", cid], limit=timeout)
            (output / "stdout.bin").write_bytes(p.stdout)
            (output / "stderr.bin").write_bytes(p.stderr)
        except subprocess.TimeoutExpired as exc:
            (output / "stdout.bin").write_bytes(exc.stdout or b"")
            (output / "stderr.bin").write_bytes(exc.stderr or b"")
            result["runner_timeout"] = True
        state = call(["inspect", "--format", "{{json .State}}", cid])
        if state.returncode:
            raise RuntimeError("cannot observe container state")
        result["state"] = json.loads(state.stdout)
        if not result["state"]["Running"]:
            result["experiment_exit"] = result["state"]["ExitCode"]
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        result["runner_error"] = str(exc)
    except KeyboardInterrupt:
        result["runner_error"] = "interrupted"
    finally:
        # The unique name also covers a create response lost before its ID arrived.
        try:
            if cid is None:
                lookup = call(["ps", "-aq", "--no-trunc", "--filter", f"name=^/{name}$"])
                if lookup.returncode:
                    raise RuntimeError("cannot reconcile container creation")
                found = lookup.stdout.decode().split()
                if len(found) > 1 or any(not re.fullmatch(r"[0-9a-f]{64}", x) for x in found):
                    raise RuntimeError("ambiguous container identity")
                cid = found[0] if found else None
            if cid:
                removed = call(["rm", "--force", cid])
                absent = call(["ps", "-aq", "--no-trunc", "--filter", f"id={cid}"])
                result["cleanup_verified"] = removed.returncode == 0 and absent.returncode == 0 and not absent.stdout.strip()
            else:
                result["cleanup_verified"] = True
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
            result["cleanup_error"] = str(exc)
        result["finished_at"] = time.time()
        (output / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"result": str(output / "result.json"), "experiment_exit": result["experiment_exit"],
                      "cleanup_verified": result["cleanup_verified"]}))
    if result.get("runner_error") or result.get("runner_timeout") or not result["cleanup_verified"]:
        return 1
    return result["experiment_exit"] if result["experiment_exit"] is not None else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--network", default="none")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    return execute(args.image, args.platform, args.input, args.output, command, args.network, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
