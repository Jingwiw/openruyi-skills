#!/usr/bin/env python3
"""Create immutable description-only evaluation variants and task inputs."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


def prepare(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output.is_relative_to(root / "skills"):
        raise ValueError("evaluation output must be outside active skills")
    output.mkdir(parents=True, exist_ok=False)
    inputs = root / "tests/evals"
    descriptions = json.loads((inputs / "descriptions.json").read_text())
    shutil.copytree(inputs / "tasks", output / "tasks")
    for label, mapping in descriptions.items():
        target = output / "variants" / label / "skills"
        shutil.copytree(root / "skills", target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for path in target.glob("*/SKILL.md"):
            original = path.read_text()
            updated = re.sub(r"^description:.*$", lambda _: "description: " + json.dumps(mapping[path.parent.name], ensure_ascii=False), original, flags=re.M)
            path.write_text(updated)
            assert original.split("---", 2)[2] == updated.split("---", 2)[2]
    for path in inputs.glob("*.json"):
        if path.name != "descriptions.json":
            shutil.copy2(path, output / path.name)
    hashes = {str(p.relative_to(output)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(output.rglob("*")) if p.is_file()}
    (output / "sha256.json").write_text(json.dumps(hashes, indent=2) + "\n")
    return len(descriptions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(f"Prepared {prepare(args.root, args.output)} variants; no agents or remote actions launched")
