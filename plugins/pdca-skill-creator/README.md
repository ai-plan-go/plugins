# PDCA Skill Creator Plugin Package

This directory is the installable package for the `pdca-skill-creator` Codex plugin.

## Package Role

This README is a human-facing package guide. It explains what this plugin package is, where the installable skill lives, and how to verify the version. It is different from:

- `../../README.md`: marketplace repository landing page.
- `../../../README.md` in the local development workspace: maintainer workflow and release notes.
- `skills/pdca-skill-creator/SKILL.md`: AI-facing authoritative skill behavior, workflow controls, templates, and generation rules.

If this README conflicts with `skills/pdca-skill-creator/SKILL.md`, the skill file wins.

## Version

- Current version: `0.2.14`
- Manifest: `.codex-plugin/plugin.json`
- Skill entry: `skills/pdca-skill-creator/SKILL.md`

## What This Plugin Provides

`pdca-skill-creator` creates or upgrades PDCA-based Codex skills for recurring workflows, inspections, monitors, reports, crawler tasks, and operational processes.

The current package requires generated executable skills to include:

- Four isolated lifecycle periods for creator evolution, business-skill generation, runtime checking, and evidence-based review. Runtime output is separated from skill source; reviews produce scoped proposals before implementation.
- List-page and batch crawler skills collect configurable multiple records, deduplicate them, preserve per-record evidence, and bound detail-page enrichment instead of relying on one fixed detail URL.

- A step-by-step confirmation table for automation-style tasks.
- A Do-script run plan document at `references/do-run-plan.md`.
- Install, reinstall, installed-cache synchronization, structure validation, and a post-install dry run for generated plugins.
- Configurable Python runtime parameters for Windows scheduler entry points.
- Sample-based crawler and classifier checks that validate real fields, evidence, and expected candidate results.
- Actionable network, timeout, HTTP, login or captcha, selector, and proxy diagnostics.
- Plan, Do, Check, and Act stages with inputs, actions, outputs, exceptions, evidence, and confirmation points.
- Executable scaffolds such as `init_project.py`, `run_task.py`, `check_outputs.py`, and `smoke_test.py` when L3/L4 maturity is targeted.
- Quality gates for generic PDCA structure and business-specific use cases.
- Conservative maturity labels and self-optimization evidence boundaries.

## Package Structure

```text
pdca-skill-creator/
├── README.md
├── .codex-plugin/
│   └── plugin.json
├── assets/
└── skills/
    └── pdca-skill-creator/
        ├── SKILL.md
        ├── agents/
        ├── references/
        └── scripts/
```

## Version Sync Rule

Before publishing, keep these files aligned:

- `.codex-plugin/plugin.json`
- `skills/pdca-skill-creator/SKILL.md`
- marketplace `README.md` and `README.zh-CN.md`
- this package README

Repository and README role details live in `docs/repository-structure.md`.
