#!/usr/bin/env python3
"""Checks every pull request must pass. Standard library only: python3 scripts/check.py"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_LINES = 150
errors = []


def check(ok, message):
    if not ok:
        errors.append(message)


def frontmatter(path):
    text = path.read_text()
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    check(match, f"{path.relative_to(ROOT)}: no frontmatter")
    return dict(line.split(":", 1) for line in match.group(1).splitlines() if ":" in line) if match else {}


def anchors(path):
    """GitHub's heading anchors for a markdown file."""
    found = set()
    for line in re.sub(r"```.*?```", "", path.read_text(), flags=re.S).splitlines():
        if line.startswith("#"):
            title = re.sub(r"[`*]", "", line.lstrip("#").strip()).lower()
            found.add(re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", title)))
    return found


# Manifests
plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
version = plugin.get("version", "")
check(re.fullmatch(r"\d+\.\d+\.\d+", version), "plugin.json: version is not x.y.z")
check(plugin.get("license") and (ROOT / "LICENSE").is_file(), "plugin.json `license` and a LICENSE file are both needed")
check(market["plugins"][0]["name"] == plugin["name"], "marketplace.json and plugin.json disagree on the name")
check(market["plugins"][0]["description"] == plugin["description"], "marketplace.json and plugin.json disagree on the description")
check(f"## {version}" in (ROOT / "CHANGELOG.md").read_text(), f"CHANGELOG.md has no entry for {version}")
json.loads((ROOT / "hooks/hooks.json").read_text())

# Skills: name matches the folder, short, and documented
commands = (ROOT / "docs/commands.md").read_text()
for skill in sorted((ROOT / "skills").iterdir()):
    path = skill / "SKILL.md"
    meta = frontmatter(path)
    check(meta.get("name", "").strip() == skill.name, f"{skill.name}: frontmatter name is not the folder name")
    check(meta.get("description", "").strip(), f"{skill.name}: no description")
    lines = len(path.read_text().splitlines())
    check(lines <= MAX_LINES, f"{skill.name}: {lines} lines, over {MAX_LINES}")
    check(f"\n## /anu:{skill.name}\n" in commands, f"docs/commands.md has no section for /anu:{skill.name}")

# Agents: name matches the file, model pinned, no field Claude Code ignores for plugin agents, documented
team = (ROOT / "docs/team.md").read_text()
for path in sorted((ROOT / "agents").glob("*.md")):
    meta = frontmatter(path)
    check(meta.get("name", "").strip() == path.stem, f"{path.name}: frontmatter name is not the file name")
    check(meta.get("model", "").strip(), f"{path.name}: no model")
    for field in ("hooks", "mcpServers", "permissionMode"):
        check(field not in meta, f"{path.name}: `{field}` is ignored in a plugin agent")
    check(f"anu:{path.stem}" in team, f"docs/team.md does not mention anu:{path.stem}")

# Relative links and anchors in the README and docs
for page in [ROOT / "README.md", ROOT / "CHANGELOG.md", *sorted((ROOT / "docs").glob("*.md"))]:
    text = re.sub(r"```.*?```", "", page.read_text(), flags=re.S)
    for target in re.findall(r"\]\(([^)\s]+)\)", text) + re.findall(r'(?:src|href)="([^"]+)"', text):
        if re.match(r"[a-z]+:", target):
            continue
        file, _, anchor = target.partition("#")
        dest = (page.parent / file).resolve() if file else page
        where = f"{page.relative_to(ROOT)}: {target}"
        check(dest.exists(), f"{where} does not exist")
        if anchor and dest.suffix == ".md" and dest.exists():
            check(anchor in anchors(dest), f"{where} has no such heading")

for message in errors:
    print("FAIL", message)
print(f"{len(errors)} problem(s)" if errors else "all checks passed")
sys.exit(1 if errors else 0)
