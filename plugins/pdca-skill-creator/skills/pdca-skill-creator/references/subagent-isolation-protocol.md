# Subagent Isolation Protocol

## Purpose

This protocol prevents a period-1 business-skill creation task from drifting into period-2 business execution when business-core abstraction or a limited page probe is needed.

## Role split

| Role | Allowed work | Forbidden work |
|---|---|---|
| Main agent | Create the skill, maintain period and confirmation gates, turn summaries into design artifacts | Treat probe data as a final business result |
| Business encapsulation subagent | Define business-core Do actions, Check rules, I/O, exceptions, evidence, open decisions, and coverage gaps | Real Do/Check, full business data, final reports, runtime authorization, or publishing |
| Exploration subagent | Inspect the bounded sample, save isolated evidence, emit a structured summary | Batch collection, final reports, baseline updates, external sync, period-2 Do/Check |
| Review subagent | Validate boundary contract and candidate skill artifacts | Access raw business samples unless a specific diagnosis requires it |

## Business Encapsulation Contract

Create `references/business-core-boundary.md` before delegating business abstraction. The contract must name the business question, permitted requirement inputs, prohibited real data, return schema, forbidden actions, main-agent conversion targets, and a stopping condition.

The business encapsulation subagent may only return `business-core-summary.json`. It describes a proposed business contract and must not contain runtime records, final business rows, or a claim that the business action has run.

```json
{
  "encapsulation_id": "core-YYYYMMDD-001",
  "active_period": 1,
  "business_object": "",
  "do_core_actions": [],
  "inputs": [],
  "outputs": [],
  "check_rules": [],
  "exception_taxonomy": [],
  "evidence_requirements": [],
  "open_decisions": [],
  "coverage_gaps": [],
  "confidence": "low|medium|high",
  "stopped_by": "contract_complete|needs_confirmation|scope_limit"
}
```

The main agent must review this summary against the confirmation table, then translate it into the business-core implementation plan, `references/do-run-plan.md`, `references/script-design.md`, `references/check-rules.yaml`, `references/output-schema.json`, and `references/ai-decision-checklist.md`. The summary alone never authorizes period 2.

## Required Boundary Contract

Create `references/subagent-boundary.md` before exploration. The contract must set an explicit sample limit, an isolated evidence directory, a return schema, forbidden actions, and a stopping condition.

## Directory Boundary

```text
{work_root}/
├── work/probes/{probe_id}/
│   ├── evidence/
│   └── probe-summary.json
├── work/business-core/{encapsulation_id}/
│   └── business-core-summary.json
├── outputs/                 # period-2 only
├── baseline/                # period-2 only
└── skill-source/            # main agent writes design artifacts only
```

## Summary Schema

```json
{
  "probe_id": "probe-YYYYMMDD-001",
  "active_period": 1,
  "sample_limit": {"pages": 3, "elements": 10},
  "field_candidates": [],
  "selector_candidates": [],
  "source_fingerprints": [],
  "evidence_paths": [],
  "diagnostics": [],
  "confidence": "low|medium|high",
  "open_questions": [],
  "stopped_by": "limit_reached|blocked|mapping_complete"
}
```

The summary is an engineering input, not a business result. It must not include a batch data table, final report rows, or a conclusion that the business task has completed.

## Main-Agent Consumption Rule

The main agent may consume only the summary and evidence paths, then update selectors, field mappings, test fixtures, confirmation questions, or diagnostic rules. It must keep `active_period=1` until the period-transition gate is explicitly satisfied.
