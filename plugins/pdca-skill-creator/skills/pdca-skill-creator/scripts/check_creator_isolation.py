#!/usr/bin/env python3
"""Verify that the released creator contains the subagent-isolation guardrails."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "SKILL.md": ["探索 subagent", "业务封装 subagent", "probe-summary.json", "business-core-summary.json", "subagent 不是运行授权"],
    "references/lifecycle-protocol.md": ["Subagent 双上下文合同", "references/subagent-boundary.md", "references/business-core-boundary.md", "probe-summary.json", "business-core-summary.json"],
    "references/pdca-stage-template.md": ["Subagent 探索边界", "业务封装 Subagent 边界", "probe-summary.json", "business-core-summary.json", "时期 2"],
    "references/subagent-isolation-protocol.md": ["Role split", "Business Encapsulation Contract", "business-core-summary.json", "Main-Agent Consumption Rule"],
    "references/use-case-test-subagent-isolation.md": ["active_period=1", "references/subagent-boundary.md", "Failure Conditions"],
    "references/use-case-test-business-encapsulation-isolation.md": ["active_period=1", "business-core-summary.json", "references/business-core-boundary.md", "Failure Conditions"],
}


def main() -> int:
    missing: list[dict[str, str]] = []
    for relative, phrases in REQUIRED.items():
        path = ROOT / relative
        if not path.exists():
            missing.append({"file": relative, "requirement": "file exists"})
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                missing.append({"file": relative, "requirement": phrase})
    print(json.dumps({"passed": not missing, "missing": missing}, ensure_ascii=False, indent=2))
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
