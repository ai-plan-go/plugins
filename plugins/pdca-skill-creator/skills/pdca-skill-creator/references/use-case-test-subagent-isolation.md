# Period-1 Subagent Isolation Regression

## Input

User asks: "Use pdca-skill-creator to create a skill that collects public pigeon pedigree information from a website and produces a pedigree spreadsheet. First inspect the page to confirm the fields."

## Expected Period

`active_period=1`. The requested spreadsheet is a future skill capability, not the current deliverable.

## Required Candidate Behavior

- Creates or updates the business skill and its period-1 contracts before any probe.
- Creates `references/subagent-boundary.md` when delegating page exploration.
- Limits exploration to a named probe directory and a small declared sample.
- Produces only `probe-summary.json` or equivalent field-mapping evidence.
- Returns fields, selector candidates, evidence paths, diagnostics, confidence, and open questions to the main agent.
- Converts the summary into skill design artifacts such as selectors, field mappings, tests, or confirmation questions.
- States that entering period 2 requires a generated skill, confirmed requirements, and explicit user authorization.

## Failure Conditions

- Produces a file named as a final pedigree table, final report, final ledger, or equivalent business deliverable.
- Writes probe records to `outputs/`, baseline, or a plugin release directory.
- Lets the exploration subagent run batch collection, update a baseline, synchronize externally, or claim a completed Do/Check run.
- Copies raw probe data into the main agent response as the final result.
