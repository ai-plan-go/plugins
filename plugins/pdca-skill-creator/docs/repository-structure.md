# PDCA Skill Creator Repository Structure

This document is the source of truth for repository layout, README roles, and synchronization rules.

Core rule: README files are human-facing promotion, usage, installation, package, or maintainer guides. `SKILL.md` files are AI-facing execution and behavior instructions. Business workflow controls, generation templates, quality gates, and operational rules belong in `SKILL.md`, `references/`, and `scripts/`, not in README.

## README Roles

| File | Audience | Role | Version source |
|---|---|---|---|
| `README.md` | Humans maintaining or browsing the local workspace | Human-facing overview, usage, install/release pointers, and links to authoritative files | Reads from `SKILL.md` and `.codex-plugin/plugin.json`; do not use as the authority for skill behavior |
| `README.zh-CN.md` | Chinese-speaking humans maintaining or browsing the local workspace | Chinese human-facing package overview, usage, install/release pointers, and links to authoritative files | Reads from `SKILL.md` and `.codex-plugin/plugin.json`; do not use as the authority for skill behavior |
| `plugins-publish/README.md` | GitHub marketplace visitors | English promotional and usage landing page for the whole plugin marketplace repository | Must match `plugins/pdca-skill-creator/.codex-plugin/plugin.json` |
| `plugins-publish/README.zh-CN.md` | GitHub marketplace visitors | Chinese promotional and usage landing page for the whole plugin marketplace repository | Must match `plugins/pdca-skill-creator/.codex-plugin/plugin.json` |
| `plugins-publish/plugins/pdca-skill-creator/README.md` | Users browsing the plugin package directory | Human-facing single-plugin package guide: what this plugin is, where the executable skill lives, and how to verify the version | Must match `.codex-plugin/plugin.json` in the same directory |

## Authoritative Files

Behavioral rules and generation constraints must be updated in this order:

1. `SKILL.md`: authoritative skill behavior and business control boundaries.
2. `references/pdca-stage-template.md`: reusable template loaded when creating generated business skills.
3. `scripts/run_creator_use_case_test.py` or other checkers: executable gates that enforce the rules.
4. README files: human-facing summaries, installation, usage, and navigation only.

Do not add a new business control rule only to README. If a rule changes generated-skill behavior, maturity, confirmation flow, automation handling, output contracts, or quality gates, it must first appear in `SKILL.md` and relevant templates/checkers. README may then summarize the change in plain language.

## Source And Publish Layout

```text
pdca-skill-creator/
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── agents/
├── docs/
│   └── repository-structure.md
├── references/
├── scripts/
└── plugins-publish/
    ├── README.md
    ├── README.zh-CN.md
    ├── marketplace.json
    └── plugins/
        └── pdca-skill-creator/
            ├── README.md
            ├── .codex-plugin/
            │   └── plugin.json
            └── skills/
                └── pdca-skill-creator/
                    ├── SKILL.md
                    ├── agents/
                    ├── references/
                    └── scripts/
```

## Synchronization Checklist

Before publishing:

- Root `SKILL.md` and `plugins-publish/plugins/pdca-skill-creator/skills/pdca-skill-creator/SKILL.md` must match.
- Root `references/` and published skill `references/` must match for files that are part of the skill.
- Root `scripts/` and published skill `scripts/` must match for files that are part of the skill.
- `.codex-plugin/plugin.json` version must match the version stated in published `SKILL.md`.
- Local package `README.md` and `README.zh-CN.md` must both reflect the new version and major release changes.
- `plugins-publish/README.md`, `plugins-publish/README.zh-CN.md`, and `plugins-publish/plugins/pdca-skill-creator/README.md` must not contain stale version numbers.
- Generated caches such as `__pycache__/`, `*.pyc`, `work_smoke/`, temporary logs, and local test outputs must not be staged.

## Upgrade Release Guide

Use this section as the fixed release checklist whenever `pdca-skill-creator` is upgraded. The goal is to prevent partial version bumps and stale human-facing docs.

### Release Trigger

Run this checklist whenever any of the following changes:

- `SKILL.md` behavioral rules
- `references/pdca-stage-template.md`
- quality gates such as `scripts/run_creator_use_case_test.py`
- plugin metadata such as `.codex-plugin/plugin.json`
- human-facing package or marketplace positioning

### Required File Sync Order

Update files in this order:

1. `skills/pdca-skill-creator/SKILL.md`
2. `skills/pdca-skill-creator/references/pdca-stage-template.md`
3. `skills/pdca-skill-creator/scripts/run_creator_use_case_test.py` and related checkers
4. `.codex-plugin/plugin.json`
5. local package `README.md`
6. local package `README.zh-CN.md`
7. marketplace or publish-facing `README.md`
8. marketplace or publish-facing `README.zh-CN.md`
9. `docs/repository-structure.md` when the sync contract, file list, or release process changes

### Minimum Upgrade Checks

Before commit:

- Search for the old version string and confirm no stale version remains in released files.
- Confirm `README.md` and `README.zh-CN.md` both mention the same current version.
- Confirm the package structure examples list both README files if both are required.
- Confirm any newly introduced hard rule in `SKILL.md` is summarized in the human-facing READMEs.
- Confirm the release did not stage `__pycache__/`, `*.pyc`, temporary logs, `work_smoke/`, or local debug outputs.
- Run at least syntax or smoke validation for changed checker scripts.

### Release Notes Scope

Human-facing READMEs do not need to restate full AI rules, but they must summarize release-impacting changes such as:

- new required runtime dependencies
- new mandatory documents or checks
- changed maturity boundaries
- changed crawler framework defaults
- changed install or reinstall expectations

### Typical Failure Modes To Prevent

- Only bumping `.codex-plugin/plugin.json` but forgetting `SKILL.md`
- Updating English README but not `README.zh-CN.md`
- Updating `SKILL.md` without syncing `pdca-stage-template.md`
- Tightening a checker script without documenting the resulting release expectation
- Publishing with temporary cache or smoke outputs staged
