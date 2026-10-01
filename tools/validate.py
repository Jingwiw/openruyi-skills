#!/usr/bin/env python3
"""Validate this repository's skill format/portability, not model behavior."""
import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
LINK = re.compile(r"!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)")
KINDS = {"knowledge", "method", "operation"}


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ValueError("non-string or duplicate YAML key")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter")
    meta = yaml.load(match[1], Loader=UniqueLoader)
    if not isinstance(meta, dict):
        raise ValueError("frontmatter must be a mapping")
    return meta, match[2]


def validate_skill(directory):
    directory = Path(directory)
    root = directory.resolve()
    errors = []
    try:
        meta, body = frontmatter(directory / "SKILL.md")
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        return [str(exc)]
    name = meta.get("name")
    if not isinstance(name, str) or not NAME.fullmatch(name) or len(name) > 64 or name != directory.name:
        errors.append("name must match directory and Agent Skills naming rules")
    description = meta.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append("description must be 1..1024 characters")
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    if set(meta) - allowed:
        errors.append("unknown frontmatter fields")
    metadata = meta.get("metadata", {})
    if not isinstance(metadata, dict) or any(not isinstance(v, str) for v in metadata.values()):
        errors.append("metadata must map strings to strings")
    elif metadata.get("kind") not in KINDS:
        errors.append("metadata.kind must be knowledge, method or operation (repository convention)")
    if not body.strip():
        errors.append("empty instructions")
    for optional in ("license", "allowed-tools", "compatibility"):
        if optional in meta and not isinstance(meta[optional], str):
            errors.append(f"{optional} must be a string")
    if isinstance(meta.get("compatibility"), str) and len(meta["compatibility"]) > 500:
        errors.append("compatibility exceeds 500 characters")
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            errors.append(f"symlink not portable as a standalone directory: {path.relative_to(directory)}")
            continue
        if not path.is_file() or path.suffix != ".md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(str(exc))
            continue
        if "[TODO:" in text:
            errors.append(f"unfinished scaffold: {path.name}")
        if re.search(r"/(?:Users|home)/[^\s/]+/", text):
            errors.append(f"hardcoded home directory: {path.name}")
        for target in LINK.findall(text):
            parts = urlsplit(target.strip("<>"))
            if parts.scheme or parts.netloc or not parts.path:
                continue
            resolved = (path.parent / unquote(parts.path)).resolve()
            if not resolved.is_relative_to(root):
                errors.append(f"reference escapes individual skill: {target}")
            elif not resolved.exists():
                errors.append(f"missing local reference: {target}")
    return errors


def validate_repo(root):
    root = Path(root)
    paths = sorted((root / "skills").glob("*/SKILL.md"))
    errors = []
    if not paths:
        errors.append("no active skills")
    for path in paths:
        errors.extend(f"{path.parent.name}: {e}" for e in validate_skill(path.parent))
    if list((root / "legacy").rglob("SKILL.md")):
        errors.append("legacy skill entrypoints must not be discoverable")
    return paths, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--skill", action="store_true", help="validate one independently copied skill")
    args = parser.parse_args()
    if args.skill:
        errors = validate_skill(args.root)
        count = 1
    else:
        paths, errors = validate_repo(args.root)
        count = len(paths)
    for error in errors:
        print(error, file=sys.stderr)
    print(f"{'FAIL' if errors else 'PASS'}: {count} skills; {len(errors)} structural errors; behavior not evaluated")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
