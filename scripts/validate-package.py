#!/usr/bin/env python3
"""
Validates the plugin structure before publishing/committing.

Checks:
- plugin.json and marketplace.json exist and are valid JSON
- required fields are present in each manifest
- the plugin "name" in plugin.json matches the "name" listed in
  marketplace.json
- each skill referenced in marketplace.json (via source) has a
  skills/<name>/SKILL.md folder
- each SKILL.md has YAML frontmatter with "name" and "description", and the
  "name" matches the folder name
- if plugin.json declares "license", a LICENSE file exists at the repo root

Usage:
    python scripts/validate-package.py

Dependency: PyYAML (pip install pyyaml)
"""

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: this script needs the PyYAML package. Install it with:")
    print("  pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []
WARNINGS: list[str] = []


def fail(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def load_json(path: Path) -> dict | None:
    if not path.exists():
        fail(f"File not found: {path.relative_to(ROOT)}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"{path.relative_to(ROOT)}: invalid JSON, {e}")
        return None


def parse_skill_frontmatter(skill_md: Path) -> dict | None:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        fail(f"{skill_md.relative_to(ROOT)}: no YAML frontmatter at the start of the file")
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        fail(f"{skill_md.relative_to(ROOT)}: malformed YAML frontmatter (missing closing '---')")
        return None
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        fail(f"{skill_md.relative_to(ROOT)}: error parsing frontmatter YAML, {e}")
        return None
    if not isinstance(data, dict):
        fail(f"{skill_md.relative_to(ROOT)}: empty or invalid frontmatter YAML")
        return None
    return data


def validate_plugin_json() -> dict | None:
    path = ROOT / ".claude-plugin" / "plugin.json"
    data = load_json(path)
    if data is None:
        return None

    required = ["name", "description", "version"]
    for field in required:
        if not data.get(field):
            fail(f"plugin.json: missing or empty required field: '{field}'")

    name = data.get("name", "")
    if name and (name != name.lower() or " " in name):
        fail(f"plugin.json: 'name' must be lowercase-kebab-case, found: '{name}'")

    if "FILL IN" in json.dumps(data):
        warn("plugin.json still has unfilled placeholder field(s) ('FILL IN...')")

    if data.get("license") and not (ROOT / "LICENSE").exists():
        fail("plugin.json declares a 'license' but no LICENSE file exists at the repo root")

    return data


def validate_marketplace_json(plugin_data: dict | None) -> dict | None:
    path = ROOT / ".claude-plugin" / "marketplace.json"
    data = load_json(path)
    if data is None:
        return None

    required = ["name", "owner", "version", "description", "plugins"]
    for field in required:
        if not data.get(field):
            fail(f"marketplace.json: missing or empty required field: '{field}'")

    if "FILL IN" in json.dumps(data):
        warn("marketplace.json still has unfilled placeholder field(s) ('FILL IN...')")

    plugins = data.get("plugins", [])
    if not isinstance(plugins, list) or not plugins:
        fail("marketplace.json: 'plugins' must be a list with at least one item")
        return data

    for entry in plugins:
        for field in ["name", "description", "source"]:
            if not entry.get(field):
                fail(f"marketplace.json: plugin entry missing required field '{field}': {entry}")

        source = entry.get("source", "")
        source_path = (ROOT / source).resolve() if source else None
        if source_path and not source_path.exists():
            fail(f"marketplace.json: 'source' points to a path that doesn't exist: '{source}'")

        if plugin_data and entry.get("name") != plugin_data.get("name"):
            fail(
                f"marketplace.json: plugin name ('{entry.get('name')}') doesn't match "
                f"'name' in plugin.json ('{plugin_data.get('name')}')"
            )

    return data


def validate_skills() -> None:
    skills_dir = ROOT / "skills"
    if not skills_dir.exists():
        warn("'skills/' folder not found, nothing to validate")
        return

    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
    if not skill_dirs:
        warn("'skills/' folder exists but is empty")
        return

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            fail(f"skills/{skill_dir.name}/: missing SKILL.md file")
            continue

        frontmatter = parse_skill_frontmatter(skill_md)
        if frontmatter is None:
            continue

        for field in ["name", "description"]:
            if not frontmatter.get(field):
                fail(f"skills/{skill_dir.name}/SKILL.md: frontmatter missing '{field}' field")

        fm_name = frontmatter.get("name", "")
        if fm_name and fm_name != skill_dir.name:
            fail(
                f"skills/{skill_dir.name}/SKILL.md: frontmatter 'name' ('{fm_name}') "
                f"doesn't match the folder name ('{skill_dir.name}')"
            )

        desc = frontmatter.get("description", "")
        if desc and len(desc) > 1024:
            warn(f"skills/{skill_dir.name}/SKILL.md: description is {len(desc)} characters, consider shortening it")


def main() -> int:
    plugin_data = validate_plugin_json()
    validate_marketplace_json(plugin_data)
    validate_skills()

    if WARNINGS:
        print("Warnings:")
        for w in WARNINGS:
            print(f"  ⚠ {w}")
        print()

    if ERRORS:
        print("Errors found:")
        for e in ERRORS:
            print(f"  ✗ {e}")
        print(f"\n{len(ERRORS)} error(s). Fix these before publishing.")
        return 1

    print("✓ All good, plugin.json, marketplace.json, and the skills passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
