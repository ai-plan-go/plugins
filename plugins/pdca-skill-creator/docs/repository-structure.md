# PDCA Skill Creator Repository Structure

This document is the source of truth for repository layout, README roles, and synchronization rules.

Core rule: README files are human-facing promotion, usage, installation, package, or maintainer guides. `SKILL.md` files are AI-facing execution and behavior instructions. Business workflow controls, generation templates, quality gates, and operational rules belong in `SKILL.md`, `references/`, and `scripts/`, not in README.

## README Roles

| File | Audience | Role | Version source |
|---|---|---|---|
| `README.md` | Humans maintaining or browsing the local workspace | Human-facing overview, usage, install/release pointers, and links to authoritative files | Reads from `SKILL.md` and `.codex-plugin/plugin.json`; do not use as the authority for skill behavior |
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
- `plugins-publish/README.md`, `plugins-publish/README.zh-CN.md`, and `plugins-publish/plugins/pdca-skill-creator/README.md` must not contain stale version numbers.
- Generated caches such as `__pycache__/`, `*.pyc`, `work_smoke/`, temporary logs, and local test outputs must not be staged.
