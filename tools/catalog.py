#!/usr/bin/env python3
"""Generate the README inventory from the single source of skill metadata."""
import argparse
from pathlib import Path
from validate import frontmatter

START = "<!-- catalog:start -->"
END = "<!-- catalog:end -->"


def render(root):
    lines = ["| Skill | 类型 | 用途 |", "| --- | --- | --- |"]
    kinds = {"knowledge": "知识", "method": "判断方法", "operation": "操作"}
    for path in sorted((root / "skills").glob("*/SKILL.md")):
        meta, _ = frontmatter(path)
        desc = meta["description"].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| [{meta['name']}]({path.relative_to(root).as_posix()}) | {kinds[meta['metadata']['kind']]} | {desc} |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    path = args.root / "README.md"
    original = path.read_text()
    before, rest = original.split(START, 1)
    _, after = rest.split(END, 1)
    desired = before + START + "\n" + render(args.root) + "\n" + END + after
    if args.write:
        path.write_text(desired)
    elif original != desired:
        print("FAIL: README catalog differs; run tools/catalog.py --write")
        return 1
    print("PASS: README catalog matches skill frontmatter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
