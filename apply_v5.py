#!/usr/bin/env python3
"""
Apply the v5 orchestration rewrite to an existing saas-builder-skills checkout.

Run from the repository root:
    python apply_v5.py

This script:
- writes/replaces the v5 architecture files included beside this script;
- adds the 3 orchestration skills;
- replaces skill-finder and research-report-builder;
- updates plugin manifests to v5.0.0;
- regenerates registry.json by scanning current skills;
- re-flattens plugin/.claude/skills/ from current skills.

It intentionally preserves all specialist skill bodies not explicitly replaced.
"""
from pathlib import Path
import json, re, shutil, sys

ROOT = Path.cwd()
OVERLAY = Path(__file__).resolve().parent

REPLACE = [
    "README.md",
    "ARCHITECTURE.md",
    "shared/references/output-conventions.md",
    "shared/references/project-schema.md",
    "shared/references/routing-model.md",
    "skills/orchestration/project-orchestrator/SKILL.md",
    "skills/orchestration/project-state-manager/SKILL.md",
    "skills/orchestration/hub-renderer/SKILL.md",
    "skills/meta/skill-finder/SKILL.md",
    "skills/research/research-report-builder/SKILL.md",
]

def copy_overlay():
    for rel in REPLACE:
        src = OVERLAY / rel
        dst = ROOT / rel
        if not src.exists():
            raise FileNotFoundError(src)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.resolve() != dst.resolve():
            shutil.copy2(src, dst)

def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    fm = text[3:end]
    out = {}
    current = None
    desc_lines = []
    for raw in fm.splitlines():
        line = raw.rstrip()
        if re.match(r"^[A-Za-z0-9_-]+:\s*", line):
            if current == "description":
                out["description"] = " ".join(desc_lines).strip()
                desc_lines = []
            k, v = line.split(":", 1)
            current = k.strip()
            v = v.strip()
            if current == "description" and v in (">", "|"):
                desc_lines = []
            else:
                out[current] = v.strip("\"'")
        elif current == "description":
            desc_lines.append(line.strip())
    if current == "description":
        out["description"] = " ".join(desc_lines).strip()
    return out

CAPABILITY_MAP = {
    "research": "discovery",
    "audience-positioning": "definition",
    "funnel-build": "marketing",
    "copywriting": "marketing",
    "planning": "planning",
    "building": "execution",
    "testing": "verification",
    "deployment": "launch",
    "operations": "operations",
    "growth": "growth",
    "meta": "meta",
    "orchestration": "orchestration",
}

def regenerate_registry():
    items = []
    for p in sorted((ROOT / "skills").glob("*/*/SKILL.md")):
        text = p.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        category = p.parts[-3]
        slug = fm.get("name") or p.parent.name
        items.append({
            "slug": slug,
            "folder": p.parent.relative_to(ROOT).as_posix(),
            "capability": fm.get("capability") or CAPABILITY_MAP.get(category, category),
            "legacy_stage": None,
            "description": fm.get("description", "")[:700]
        })
    registry = {
        "name": "saas-builder-skills",
        "description": "Specialist skill library behind the v5 project orchestrator.",
        "version": "5.0.0",
        "architecture": "orchestrator-state-renderer-specialists",
        "skill_count": len(items),
        "skills": items,
    }
    (ROOT / "registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(items)

def update_manifests(count):
    plugin = ROOT / "plugin/.claude-plugin/plugin.json"
    marketplace = ROOT / ".claude-plugin/marketplace.json"
    if plugin.exists():
        data = json.loads(plugin.read_text(encoding="utf-8"))
        data["version"] = "5.0.0"
        data["description"] = f"{count} specialist skills behind one v5 project orchestrator with shared project state, conditional routing, verification, launch, operations and growth."
        plugin.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    if marketplace.exists():
        data = json.loads(marketplace.read_text(encoding="utf-8"))
        data.setdefault("metadata", {})["description"] = f"{count} specialist skills behind one v5 project orchestrator."
        for p in data.get("plugins", []):
            if p.get("name") == "saas-builder-skills":
                p["version"] = "5.0.0"
                p["description"] = f"{count} specialist skills behind one project orchestrator. Handles apps, SaaS, websites, brands, services, features, launches and ongoing operations without a rigid stage maze."
                tags = set(p.get("tags", []))
                tags.update(["orchestration", "sdlc", "project-management"])
                p["tags"] = sorted(tags)
        marketplace.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

def reflatten():
    src = ROOT / "skills"
    dst = ROOT / "plugin/.claude/skills"
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)
    seen = set()
    for skill in sorted(src.glob("*/*")):
        if not (skill / "SKILL.md").exists():
            continue
        slug = skill.name
        if slug in seen:
            raise RuntimeError(f"Duplicate skill slug: {slug}")
        seen.add(slug)
        shutil.copytree(skill, dst / slug)

def main():
    if not (ROOT / "skills").exists():
        sys.exit("Run this script from the saas-builder-skills repository root.")
    copy_overlay()
    count = regenerate_registry()
    update_manifests(count)
    reflatten()
    print(f"v5 rewrite applied. {count} skills registered and flattened.")
    print("Review git diff, then commit as v5.0.0.")

if __name__ == "__main__":
    main()
