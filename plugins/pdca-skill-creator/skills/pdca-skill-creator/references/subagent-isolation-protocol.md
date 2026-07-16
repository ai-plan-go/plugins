# Subagent Isolation Protocol

## Purpose

This protocol prevents a period-1 business-skill creation task from drifting into period-2 business execution when a limited page probe or field-mapping experiment is needed.

## Role split

| Role | Allowed work | Forbidden work |
|---|---|---|
| Main agent | Create the skill, maintain period and confirmation gates, turn summaries into design artifacts | Treat probe data as a final business result |
| Exploration subagent | Inspect the bounded sample, save isolated evidence, emit a structured summary | Batch collection, final reports, baseline updates, external sync, period-2 Do/Check |
| Review subagent | Validate boundary contract and candidate skill artifacts | Access raw business samples unless a specific diagnosis requires it |

## Required Boundary Contract

Create `references/subagent-boundary.md` before exploration. The contract must set an explicit sample limit, an isolated evidence directory, a return schema, forbidden actions, and a stopping condition.

## Directory Boundary

```text
{work_root}/
├── work/probes/{probe_id}/
│   ├── evidence/
│   └── probe-summary.json
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
