# PDCA Skill Creator Repository Structure

This document is the source of truth for repository layout, README roles, and synchronization rules.

Core rule: README files are human-facing promotion, usage, installation, package, or maintainer guides. `SKILL.md` files are AI-facing execution and behavior instructions. Business workflow controls, generation templates, quality gates, and operational rules belong in `SKILL.md`, `references/`, and `scripts/`, not in README.

## README Roles

| File | Audience | Role | Version source |
|---|---|---|---|
| repository-root `README.md` | Humans maintaining or browsing the repository | English repository landing page, release summary, installation guidance, and links to authoritative files | Reads from `plugins/pdca-skill-creator/skills/pdca-skill-creator/SKILL.md` and `plugins/pdca-skill-creator/.codex-plugin/plugin.json`; do not use as the authority for skill behavior |
| repository-root `README.zh-CN.md` | Chinese-speaking humans maintaining or browsing the repository | Chinese repository landing page, release summary, installation guidance, and links to authoritative files | Reads from `plugins/pdca-skill-creator/skills/pdca-skill-creator/SKILL.md` and `plugins/pdca-skill-creator/.codex-plugin/plugin.json`; do not use as the authority for skill behavior |

## Authoritative Files

Behavioral rules and generation constraints must be updated in this order:

1. `SKILL.md`: authoritative skill behavior and business control boundaries.
2. `references/pdca-stage-template.md`: reusable template loaded when creating generated business skills.
3. `scripts/run_creator_use_case_test.py` or other checkers: executable gates that enforce the rules.
4. README files: human-facing summaries, installation, usage, and navigation only.

Do not add a new business control rule only to README. If a rule changes generated-skill behavior, maturity, confirmation flow, automation handling, output contracts, or quality gates, it must first appear in `SKILL.md` and relevant templates/checkers. README may then summarize the change in plain language.

## Source And Publish Layout

```text
plugins-repo/
├── README.md
├── README.zh-CN.md
├── marketplace.json
├── assets/
└── plugins/
    └── pdca-skill-creator/
        ├── .codex-plugin/
        │   └── plugin.json
        ├── assets/
        ├── docs/
        │   └── repository-structure.md
        └── skills/
            └── pdca-skill-creator/
                ├── SKILL.md
                ├── agents/
                ├── references/
                └── scripts/
```

## Synchronization Checklist

Before publishing:

- `plugins/pdca-skill-creator/skills/pdca-skill-creator/SKILL.md` must match the intended released rules.
- `plugins/pdca-skill-creator/skills/pdca-skill-creator/references/` must match the intended released templates and contracts.
- `plugins/pdca-skill-creator/skills/pdca-skill-creator/scripts/` must match the intended released checkers and tooling.
- `plugins/pdca-skill-creator/.codex-plugin/plugin.json` version must match the version stated in `SKILL.md`.
- Repository-root `README.md` and `README.zh-CN.md` must both reflect the new version and major release changes.
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
5. repository-root `README.md`
6. repository-root `README.zh-CN.md`
7. `docs/repository-structure.md` when the sync contract, file list, or release process changes

### Minimum Upgrade Checks

Before commit:

- Search for the old version string and confirm no stale version remains in released files.
- Confirm `README.md` and `README.zh-CN.md` both mention the same current version.
- Confirm the structure examples place `README.md` and `README.zh-CN.md` only at the repository outermost level.
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
- Reintroducing duplicate README files under the plugin package and causing structure drift
- Publishing with temporary cache or smoke outputs staged
