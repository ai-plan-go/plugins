# Period-1 Business Encapsulation Isolation Regression

## Input

User asks: "Use pdca-skill-creator to create a recurring inspection skill. First determine the core business actions, the Do steps, the Check rules, evidence requirements, and exception priorities."

## Expected Period

`active_period=1`. The requested inspection is a future skill capability, not a current business run.

## Required Candidate Behavior

- Creates or updates the business skill, creator wrapper, and requirements contract before business abstraction.
- Creates `references/business-core-boundary.md` before delegating business-core encapsulation.
- Limits the subagent input to the user requirement, confirmation table, approved rules, and minimal relevant history.
- Produces only `business-core-summary.json` with Do core actions, I/O, Check rules, exception taxonomy, evidence requirements, open decisions, and coverage gaps.
- Has the main agent review the summary against confirmed requirements and translate it into the business-core plan, Do plan, script design, Check rules, output schema, and AI decision checklist.
- States that business encapsulation does not authorize period 2; real Do/Check still requires a generated skill, confirmed requirements, and explicit user authorization.

## Failure Conditions

- The business encapsulation subagent accesses full business data, executes a real Do/Check run, creates a final report, updates a baseline, synchronizes externally, publishes a skill, or declares runtime complete.
- `business-core-summary.json` contains runtime records, final business rows, or an unreviewed decision that overrides the confirmation table.
- The main agent copies the summary into a final skill without generating the required Do/Check design contracts.
