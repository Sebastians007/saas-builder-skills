# Migration to v5

This package is an overlay for the existing repository because the current GitHub connection was read-only.

## Apply

1. Download/extract this package.
2. Copy `apply_v5.py` and the overlay folders/files into your existing `saas-builder-skills` checkout, preserving paths.
3. From the repository root run:

```bash
python apply_v5.py
```

4. Review:

```bash
git diff
git status
```

5. Commit:

```bash
git add -A
git commit -m "v5.0.0: replace rigid stages with project orchestration"
git push
```

## What the script preserves

All existing specialist skills are preserved except:
- `skills/meta/skill-finder/SKILL.md`, rewritten to use the live registry;
- `skills/research/research-report-builder/SKILL.md`, rewritten as a scoped Discover specialist.

It adds:
- `project-orchestrator`
- `project-state-manager`
- `hub-renderer`
- architecture/state/routing references

It regenerates:
- `registry.json`
- `plugin/.claude/skills/`
- plugin version/description metadata

## Expected count

Starting from the current public repo with 87 skills, v5 adds three new orchestration skills, so the expected total is **90**.
