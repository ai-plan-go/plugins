# PDCA Skill Creator

[简体中文](README.zh-CN.md) | English

![PDCA Skill Creator banner](assets/readme-banner-en.png)

`pdca-skill-creator` is a Codex skill for creating self-checking, repeatable, and continuously improving skills based on the PDCA loop: Plan, Do, Check, Act.

It helps turn recurring business workflows, inspection tasks, monitoring jobs, reports, crawler workflows, and operational processes into Codex skills with clear execution steps, check rules, evidence, logs, health diagnosis, and review-driven evolution.

## What It Does

`pdca-skill-creator` is a meta-skill. It does not only write a workflow description; it helps transform a recurring process into a durable Codex skill that can execute, check, review, and evolve.

Generated skills are designed around four stages:

- **Plan**: Clarify requirements, define boundaries, design execution steps, and create check rules.
- **Do**: Execute tasks through scripts or deterministic tools, while preserving logs and evidence.
- **Check**: Validate results with explicit rules, diagnose issues, and recommend actions.
- **Act**: Review outcomes, absorb user feedback, and decide whether a new Plan cycle is needed.

## Core Capabilities

### Business-First Skill Design

- Converts fuzzy business goals into concrete inputs, outputs, rules, and operating boundaries.
- Identifies the business core first, then adds PDCA, reports, logs, baselines, and review structure around it.
- For crawler and page-inspection work, requires a real collection path: URL handling, Playwright access, DOM extraction, screenshots, structured results, and error classification.
- Uses selector configuration such as `references/selectors.yaml` when page selectors are unknown, and requires scripts to actually consume that configuration.

### PDCA Execution Scaffold

- Generates business-specific Plan, Do, Check, and Act stages with inputs, actions, outputs, exception handling, evidence, and confirmation points.
- Requires a step-by-step confirmation table before creating automation, crawler, inspection, report, or scheduled skills.
- Creates executable scaffolds for automation, monitoring, reporting, crawler, and recurring operations.
- Uses script-first execution with `init_project.py`, `run_task.py`, `check_outputs.py`, `smoke_test.py`, and scheduled entry points when needed.
- Requires `references/do-run-plan.md` for L3/L4 executable skills so the Do script flow is understandable without reading source code.
- Keeps screenshots, logs, and structured files as evidence rather than relying on repeated AI-only reasoning.

### Evidence-Based Maturity

- Separates target maturity from current maturity so scaffolds are not mistaken for production-ready systems.
- Produces capability and business-core implementation matrices that mark each capability as implemented, placeholder, or pending.
- Requires Check scripts to consume rule files and output schemas.
- Keeps rule files, schemas, Do outputs, Check fields, and deployment contracts aligned.

Generated skills use four maturity levels:

| Level | Meaning | Typical Evidence |
|---|---|---|
| L1 Specification | Workflow, rules, and open questions are documented, but the skill must not claim to be runnable. | PDCA stages, business rules, open questions |
| L2 Rules | Rules, deployment contracts, and output formats exist, but stable execution scripts are missing. | Check rules, output schema, deployment contract |
| L3 Executable | Do/Check scripts, structured outputs, logs, and a local manual entry point exist. | `run_task.py`, `check_outputs.py`, smoke test, runtime logs |
| L4 Deployable | L3 plus a real business execution path, scheduled entry point, failure handling, and deployment acceptance records. | Scheduler entry point, exit codes, log discovery, deployment parameters, acceptance record |

### Quality Gates And Scoring

- Keeps `scripts/run_creator_use_case_test.py` for creator regression testing with the default Amazon ASIN use case.
- Adds a ShowStart post-rock regression case for install verification, runtime selection, field quality, classification evidence, and network diagnostics.
- Adds a generic generated-skill quality gate through `scripts/run_generated_skill_quality_gate.py`.
- Requires newly generated skills to include `scripts/score_skill_quality.py` and `references/skill-quality-rubric.json` for business-neutral PDCA quality scoring.
- Requires newly generated skills to include `scripts/run_business_use_case_test.py` and `references/business-use-case-profile.json` for scenario-specific scoring.
- Uses a default passing line of 85/100 with no P0/P1 blockers.

### Self-Optimization And Retesting

- Separates self-optimization mechanism, executable self-optimization, and proven self-evolution.
- Requires Act outputs to name retest entries and evidence paths.
- Marks untested optimization claims as pending or not verified instead of implying success.
- Preserves requirement history and decisions in `references/plan-history.md`.

### Plugin Delivery And Clean Packaging

- Generates a Codex-installable plugin directory with `.codex-plugin/plugin.json` and `skills/` when plugin delivery is requested.
- Requires install, reinstall, installed-cache synchronization, structure checks, and one post-install dry run to be documented and verifiable.
- Requires Windows scheduler entry points to accept an explicit Python runtime instead of assuming bare `python`.
- Requires crawler and classifier smoke tests to validate expected sample fields and business classification results.
- Classifies collection failures such as network permission, timeout, HTTP, login or captcha, selector, and proxy errors with rerun guidance.
- Treats zip files as optional transport archives, not as a replacement for installable plugin structure.
- Excludes `__pycache__/`, `*.pyc`, `work_smoke/`, `tmp_smoke/`, business test reports, temporary logs, and local test outputs from final deliverables.
- Supports testing either plain skill folders or installable plugin roots.

## Version Summary

| Version | Main change |
|---|---|
| 0.2.18 | Added creator-wrapper gating so business requests passed to the creator are first converted into skill-creation goals before any runtime execution. |
| 0.2.17 | Added hard stage gates for creator period separation, mandatory progress reporting, and aligned published package versions for the release. |
| 0.2.16 | Required script-only business data generation and a source-processing-result run manifest for executable skills. |
| 0.2.15 | Made the whole requirements table a mandatory user-confirmed gate; added crawler scope, probe field mapping, and script-vs-AI automation analysis. |
| 0.2.14 | Updated the ShowStart regression to require multi-record homepage list collection, deduplication, bounded detail enrichment, and batch sync-plan checks. |
| 0.2.13 | Added four-period lifecycle isolation for creator evolution, skill generation, runtime checks, and evidence-based review proposals. |
| 0.2.12 | Added post-install verification, configurable Python runtime entrypoints, sample-based crawler classification tests, detailed network diagnostics, a ShowStart post-rock regression case, and stricter delivery cleanup. |
| 0.2.11 | Clarified that README files are human-facing promotion and usage guides, while SKILL.md is the AI-facing source for workflow control and templates. |
| 0.2.10 | Clarified README roles, repository structure, and version synchronization rules to prevent documentation drift. |
| 0.2.9 | Added required Do-script run plan docs so generated runtime scripts are not black boxes. |
| 0.2.8 | Added step-by-step confirmation table gates for parameters, status, risks, and handling actions. |
| 0.2.7 | Added automation preflight confirmation, Codex scheduling classification, installable-plugin gates, and source-safe smoke-test checks. |
| 0.2.6 | Split generic PDCA quality scoring from business-specific use-case scoring. |
| 0.2.5 | Added explicit self-optimization layers, retest evidence paths, plugin-aware testing, and clean release hygiene. |
| 0.2.4 | Added creator use-case testing loop, default Amazon ASIN regression case, and deterministic test reports. |
| 0.2.3 | Strengthened installable plugin delivery, contract consistency, selector consumption, smoke tests, and packaging cleanup. |
| 0.2.2 | Put the business core first and required real crawler/page-inspection scaffolds. |
| 0.2.1 | Added maturity grading, capability boundaries, rule-consuming checkers, and post-generation self-checks. |

## Use Cases

Use this skill when you want to create or upgrade a Codex skill for:

- Recurring business operations.
- Website, marketplace page, product page, or admin-page inspections.
- E-commerce listing, ASIN, price, inventory, image, or content quality checks.
- Daily, weekly, operational, or business analysis reports.
- Spreadsheet exports, business metrics, and anomaly checks.
- Web crawling, DOM extraction, screenshot archiving, and evidence workflows.
- Internal standard operating procedures that need to become reusable skills.
- Existing skills that need better review loops, check rules, or runtime-cost controls.

## Workflow

![PDCA workflow](assets/pdca-workflow-en.png)

## Who It Is For

- Operations, product, growth, and data teams that want to turn repeated work into Codex skills.
- Teams that want AI workflows to include logs, evidence, check rules, and review loops.
- Skill creators who want to avoid re-explaining requirements every time.
- Teams that need requirement history and decision records across multiple iterations.

## Repository Structure

```text
pdca-skill-creator/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    └── pdca-stage-template.md
```

- `SKILL.md`: Main skill entry point, trigger description, creation workflow, and mandatory rules.
- `agents/openai.yaml`: Codex UI metadata, including display name, short description, and default prompt.
- `references/pdca-stage-template.md`: Detailed PDCA stage template loaded when creating business skills.

## Installation

The simplest way is to add this repository as a Codex plugin marketplace.

## Publication Metadata

- Plugin name: `pdca-skill-creator`
- Marketplace: `ai-plan-go`
- Published repository: <https://github.com/ai-plan-go/plugins>
- Git URL: `https://github.com/ai-plan-go/plugins.git`
- Current version: `0.2.18`

Future sessions should use this section, `marketplace.json`, and `plugins/pdca-skill-creator/.codex-plugin/plugin.json` to quickly identify the published plugin.

### Install from Codex

1. Open Codex.
2. Go to **Plugins**.
3. Choose **Add plugin marketplace**.

![Codex add plugin marketplace button](assets/codex-plugins-button.png)

4. Enter this GitHub URL:

```text
https://github.com/ai-plan-go/plugins.git
```

5. Install **PDCA Skill Creator** from the marketplace.

### Manual Fallback

If marketplace installation is not available in your Codex build, copy the skill folder manually:

```bash
git clone https://github.com/ai-plan-go/plugins.git
mkdir -p ~/.codex/skills
cp -R plugins/pdca-skill-creator/skills/pdca-skill-creator ~/.codex/skills/
```

### Verify Installation

After restarting or refreshing Codex, try:

```text
Use $pdca-skill-creator to create a skill for a recurring workflow.
```

If the skill is loaded correctly, Codex should use the PDCA workflow and ask for the business goal, inputs, outputs, check rules, and review requirements.

## Usage

After installing or enabling the skill in Codex, use prompts like:

```text
Use $pdca-skill-creator to create a skill for daily Amazon listing checks.
```

The creator will help confirm:

- The business goal.
- Required input data.
- Data source, output format, trigger plan, runtime parameters, and delivery form.
- Who consumes the output.
- Success and failure criteria.
- Exceptions that must be diagnosed.
- Whether scripts, logs, screenshots, reports, or historical records are needed.
- How future Act-stage reviews should improve the skill.

## Generated Skill Guarantees

Skills created with `pdca-skill-creator` are designed to include:

- A clear PDCA operating model.
- Explicit inputs, actions, outputs, exception handling, and evidence requirements.
- Script-first execution for repeatable tasks.
- A step-by-step confirmation table for automation-style skills.
- A `references/do-run-plan.md` document for executable Do scripts.
- Structured logs and check results.
- Health diagnosis with P0/P1/P2 priority levels.
- Token-control rules for scripts, screenshots, and historical logs.
- A `references/plan-history.md` file for preserving historical requirements and decisions.
- Source metadata that records the creator name, repository, version, and generation date.

## Design Philosophy

The goal is not to make AI think harder every time. The goal is to make repeatable work more structured:

- Scripts execute the stable parts.
- Rules check the results.
- Logs and evidence make conclusions reviewable.
- Act-stage reviews preserve learning.
- Historical Plan records prevent requirement drift.

## Version

Current creator version: `0.2.18`

Source repository: <https://github.com/ai-plan-go/plugins.git>

