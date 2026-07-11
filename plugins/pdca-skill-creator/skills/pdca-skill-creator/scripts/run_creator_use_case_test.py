#!/usr/bin/env python3
"""Run a pdca-skill-creator use case test against a generated skill."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


RUBRIC = [
    ("pdca", 10, ["Plan", "Do", "Check", "Act", "输入", "动作", "产物", "异常处理"]),
    ("business_core", 12, ["业务核心", "字段提取", "证据截图", "异常", "分级"]),
    ("crawler_framework", 12, ["playwright", "selectors.yaml", "screenshot", "captcha", "timeout", "DOM"]),
    ("amazon_rules", 12, ["ASIN", "List Price", "Typical Price", "Buy Box", "Coupon", "Prime", "差评", "跟卖", "A+", "排名"]),
    ("project_isolation", 8, ["input", "daily_reports", "summary", "baseline", "screenshots", "logs", "项目"]),
    ("reports_evidence", 8, ["双", "Sheet", "截图", "嵌入", "旧图片|旧图|图片重叠|清理旧", "异常汇总"]),
    ("contract_consistency", 10, ["check-rules", "output-schema", "required_outputs", "outputs", "deployment-contract"]),
    ("maturity", 8, ["目标成熟度", "当前成熟度", "L3", "L4", "占位", "待确认"]),
    ("executable_scaffold", 10, ["init_project.py", "run_task.py", "check_outputs.py", "smoke_test.py", "run_daily_check.ps1", "退出码"]),
    ("self_check_act", 10, ["smoke test", "自检", "Act", "plan-history", "复盘", "改进", "自我优化|自我进化|优化机制|self-optimization|self optimization|self-evolution|self evolution", "复测|re-run|retest|re-test"]),
]


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "scripts/init_project.py",
    "scripts/run_task.py",
    "scripts/check_outputs.py",
    "scripts/smoke_test.py",
    "scripts/run_daily_check.ps1",
    "references/deployment-contract.md",
    "references/do-run-plan.md",
    "references/plan-history.md",
]

REQUIRED_CONFIRMATION_KEYWORDS = [
    "步骤检查确认表",
    "步骤",
    "参数类别",
    "数据来源",
    "输出格式",
    "触发方案",
    "运行参数",
    "确认状态",
    "未确认风险",
    "处理动作",
]

CODEX_AUTOMATION_KEYWORDS = [
    "Codex 已安排任务",
    "Codex automation",
    "automation",
    "未安排",
    "已安排",
]

DO_RUN_PLAN_KEYWORDS = [
    "运行入口",
    "参数表",
    "前置检查",
    "执行流程",
    "产物清单",
    "可观测",
    "异常诊断",
    "Check",
    "用户确认",
]


OPTIONAL_CONTRACT_FILES = [
    "references/check-rules.yaml",
    "references/check-rules.md",
    "references/output-schema.json",
    "references/output-schema.md",
    "references/selectors.yaml",
    "references/selectors.yml",
]


FORBIDDEN_DELIVERABLE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    "work_smoke",
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return ""


def all_text(skill_dir: Path) -> str:
    parts: list[str] = []
    for path in skill_dir.rglob("*"):
        relative_parts = set(path.relative_to(skill_dir).parts)
        if "__pycache__" in relative_parts or "work_smoke" in relative_parts:
            continue
        if path.is_file() and path.suffix.lower() in {".md", ".py", ".ps1", ".yaml", ".yml", ".json", ".txt"}:
            parts.append(f"\n\n--- {path.relative_to(skill_dir)} ---\n")
            parts.append(read_text(path))
    return "\n".join(parts)


def contains_any_file(skill_dir: Path, names: list[str]) -> bool:
    return any((skill_dir / name).exists() for name in names)


def resolve_skill_dir(candidate_dir: Path) -> tuple[Path, str]:
    """Accept either a skill directory or an installable plugin root."""
    if (candidate_dir / "SKILL.md").exists():
        return candidate_dir, "skill"

    plugin_manifest = candidate_dir / ".codex-plugin" / "plugin.json"
    skills_root = candidate_dir / "skills"
    if plugin_manifest.exists() and skills_root.exists():
        skill_dirs = sorted(path.parent for path in skills_root.glob("*/SKILL.md"))
        if len(skill_dirs) == 1:
            return skill_dirs[0], "plugin"
        if len(skill_dirs) > 1:
            named_dir = skills_root / candidate_dir.name
            if (named_dir / "SKILL.md").exists():
                return named_dir, "plugin"
            return skill_dirs[0], "plugin"

    return candidate_dir, "unknown"


def keyword_score(text: str, keywords: list[str], points: int) -> tuple[int, list[str]]:
    lowered = text.lower()
    hits = []
    missing = []
    for kw in keywords:
        alternatives = [part.strip().lower() for part in kw.split("|")]
        if any(part in lowered for part in alternatives):
            hits.append(kw)
        else:
            missing.append(kw)
    score = round(points * len(hits) / len(keywords))
    return score, missing


def script_consumes_file(script_text: str, file_hint: str) -> bool:
    normalized = script_text.replace("\\", "/").lower()
    return file_hint.lower() in normalized


def forbidden_deliverable_files(skill_dir: Path) -> list[str]:
    forbidden: list[str] = []
    for path in skill_dir.rglob("*"):
        rel = path.relative_to(skill_dir)
        rel_text = rel.as_posix()
        if "__pycache__" in rel.parts or "work_smoke" in rel.parts or path.suffix == ".pyc":
            forbidden.append(rel_text)
    return sorted(forbidden)


def current_maturity_overclaims_l4(text: str) -> bool:
    current_lines = [
        line.strip()
        for line in text.splitlines()
        if re.search(r"当前成熟度|current maturity", line, re.I)
    ]
    overclaim_lines = [
        line
        for line in current_lines
        if "L4" in line
        and not re.search(r"不可标为\s*L4|不得标为\s*L4|不能标为\s*L4|not\s+be\s+marked\s+as\s+L4", line, re.I)
        and not re.search(r"目标成熟度|target maturity", line, re.I)
    ]
    if not overclaim_lines:
        return False
    return bool(re.search(r"stub|placeholder|not_configured|TODO|占位|dry-run only", text, re.I))


def has_self_optimization_mechanism(text: str) -> bool:
    return bool(
        re.search(r"Act", text, re.I)
        and re.search(r"plan-history|复盘|改进", text, re.I)
        and re.search(r"自我优化|自我进化|优化机制|self[- ]?optimization|self[- ]?evolution|复测|re-run|retest|re-test", text, re.I)
    )


def overclaims_self_evolution(text: str) -> bool:
    claims = re.search(r"已验证.{0,20}自我(?:优化|进化)|自我进化有效性.{0,20}已实现|self[- ]?(?:optimization|evolution).{0,30}verified", text, re.I)
    evidence = re.search(r"Do 退出码|Check 退出码|smoke\+Act|use-case-test|复测.{0,20}(?:通过|提升|减少|改善)", text, re.I)
    return bool(claims and not evidence)


def run_use_case_test(skill_dir: Path) -> dict:
    requested_dir = skill_dir
    skill_dir, candidate_type = resolve_skill_dir(skill_dir)
    text = all_text(skill_dir)
    issues: list[dict] = []
    dimension_scores: dict[str, dict] = {}
    total = 0

    missing_required = [name for name in REQUIRED_FILES if not (skill_dir / name).exists()]
    for name in missing_required:
        issues.append({"priority": "P0", "type": "missing_required_file", "detail": name})

    forbidden_files = forbidden_deliverable_files(skill_dir)
    if forbidden_files:
        preview = ", ".join(forbidden_files[:8])
        if len(forbidden_files) > 8:
            preview += f", ... (+{len(forbidden_files) - 8})"
        issues.append({"priority": "P1", "type": "unclean_deliverable", "detail": preview})

    if not contains_any_file(skill_dir, ["references/check-rules.yaml", "references/check-rules.md"]):
        issues.append({"priority": "P1", "type": "missing_check_rules", "detail": "references/check-rules.*"})
    if not contains_any_file(skill_dir, ["references/output-schema.json", "references/output-schema.md"]):
        issues.append({"priority": "P1", "type": "missing_output_schema", "detail": "references/output-schema.*"})
    if not contains_any_file(skill_dir, ["references/selectors.yaml", "references/selectors.yml"]):
        issues.append({"priority": "P1", "type": "missing_selectors", "detail": "references/selectors.yaml"})

    if candidate_type != "plugin":
        issues.append({
            "priority": "P1",
            "type": "not_installable_codex_plugin",
            "detail": "candidate is a bare skill directory; installable Codex deliverables need .codex-plugin/plugin.json and skills/{name}/SKILL.md",
        })

    for name, points, keywords in RUBRIC:
        score, missing = keyword_score(text, keywords, points)
        dimension_scores[name] = {
            "score": score,
            "max": points,
            "missing_keywords": missing,
        }
        total += score

    run_task = read_text(skill_dir / "scripts" / "run_task.py")
    check_outputs = read_text(skill_dir / "scripts" / "check_outputs.py")
    smoke_test = read_text(skill_dir / "scripts" / "smoke_test.py")
    deployment_contract = read_text(skill_dir / "references" / "deployment-contract.md")
    do_run_plan = read_text(skill_dir / "references" / "do-run-plan.md")
    skill_md = read_text(skill_dir / "SKILL.md")

    if run_task and not re.search(r"playwright|async_playwright|sync_playwright", run_task, re.I):
        issues.append({"priority": "P0", "type": "crawler_framework_missing", "detail": "run_task.py does not reference Playwright"})
    if run_task and contains_any_file(skill_dir, ["references/selectors.yaml", "references/selectors.yml"]):
        if not script_consumes_file(run_task, "selectors"):
            issues.append({"priority": "P1", "type": "selectors_not_consumed", "detail": "run_task.py does not read selectors config"})
    if check_outputs and contains_any_file(skill_dir, ["references/check-rules.yaml", "references/check-rules.md"]):
        if not script_consumes_file(check_outputs, "check-rules"):
            issues.append({"priority": "P1", "type": "check_rules_not_consumed", "detail": "check_outputs.py does not read check-rules"})
    if check_outputs and contains_any_file(skill_dir, ["references/output-schema.json", "references/output-schema.md"]):
        if not script_consumes_file(check_outputs, "output-schema"):
            issues.append({"priority": "P1", "type": "schema_not_consumed", "detail": "check_outputs.py does not read output-schema"})
    if smoke_test and not re.search(r"check_outputs|run_task|init_project", smoke_test, re.I):
        issues.append({"priority": "P1", "type": "weak_smoke_test", "detail": "smoke_test.py does not exercise init/run/check chain"})
    if smoke_test and re.search(r"parents\s*\[\s*1\s*\]|parent\.parent|references.+plan-history|plan-history.+open\s*\(", smoke_test, re.I):
        issues.append({
            "priority": "P1",
            "type": "smoke_writes_skill_source",
            "detail": "smoke_test.py appears to write references/plan-history.md under the skill source; runtime evidence should go to the work/output directory or fail gracefully on read-only installs",
        })
    if run_task:
        if not do_run_plan:
            issues.append({
                "priority": "P1",
                "type": "missing_do_run_plan",
                "detail": "references/do-run-plan.md is required to explain the Do script flow, parameters, outputs, logs, and failures",
            })
        else:
            missing_do_plan = [keyword for keyword in DO_RUN_PLAN_KEYWORDS if keyword.lower() not in do_run_plan.lower()]
            if missing_do_plan:
                issues.append({
                    "priority": "P1",
                    "type": "incomplete_do_run_plan",
                    "detail": "missing do-run-plan sections: " + ", ".join(missing_do_plan),
                })

    confirmation_missing = [
        keyword for keyword in REQUIRED_CONFIRMATION_KEYWORDS
        if keyword not in deployment_contract and keyword not in skill_md
    ]
    if confirmation_missing:
        issues.append({
            "priority": "P1",
            "type": "missing_preflight_confirmation_contract",
            "detail": "missing confirmation fields: " + ", ".join(confirmation_missing),
        })

    automation_context = re.search(r"每日|定时|自动|安排任务|监控|周期", text, re.I)
    if automation_context and not any(keyword.lower() in text.lower() for keyword in CODEX_AUTOMATION_KEYWORDS):
        issues.append({
            "priority": "P1",
            "type": "codex_automation_not_classified",
            "detail": "scheduled/automated use case does not distinguish Codex arranged task from local scheduler script",
        })

    if current_maturity_overclaims_l4(text):
        issues.append({"priority": "P1", "type": "possible_maturity_overclaim", "detail": "L4 appears together with placeholder markers"})
    if not has_self_optimization_mechanism(text):
        issues.append({"priority": "P1", "type": "missing_self_optimization_mechanism", "detail": "candidate does not clearly define Act-based self-optimization mechanism and re-test path"})
    if overclaims_self_evolution(text):
        issues.append({"priority": "P1", "type": "self_evolution_overclaim", "detail": "candidate claims verified self-evolution without Do/Check/Act or re-test evidence"})

    p0 = [item for item in issues if item["priority"] == "P0"]
    p1 = [item for item in issues if item["priority"] == "P1"]
    passed = total >= 85 and not p0 and not p1

    return {
        "tested_at": datetime.now().isoformat(timespec="seconds"),
        "requested_dir": str(requested_dir),
        "skill_dir": str(skill_dir),
        "candidate_type": candidate_type,
        "score": total,
        "max_score": 100,
        "passed": passed,
        "threshold": 85,
        "dimension_scores": dimension_scores,
        "issues": issues,
        "summary": {
            "p0": len(p0),
            "p1": len(p1),
            "p2": len([item for item in issues if item["priority"] == "P2"]),
            "missing_required_files": missing_required,
        },
    }


def write_report(result: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "use-case-test.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# PDCA Skill Creator Use Case Test Report",
        "",
        f"- Tested at: {result['tested_at']}",
        f"- Requested candidate: `{result.get('requested_dir', result['skill_dir'])}`",
        f"- Candidate: `{result['skill_dir']}`",
        f"- Candidate type: {result.get('candidate_type', 'unknown')}",
        f"- Score: {result['score']}/{result['max_score']}",
        f"- Passed: {result['passed']}",
        "",
        "## Dimension Scores",
        "",
        "| Dimension | Score | Missing Keywords |",
        "|---|---:|---|",
    ]
    for name, info in result["dimension_scores"].items():
        missing = ", ".join(info["missing_keywords"]) if info["missing_keywords"] else "-"
        lines.append(f"| {name} | {info['score']}/{info['max']} | {missing} |")

    lines.extend(["", "## Issues", ""])
    if result["issues"]:
        lines.extend(["| Priority | Type | Detail |", "|---|---|---|"])
        for issue in result["issues"]:
            lines.append(f"| {issue['priority']} | {issue['type']} | {issue['detail']} |")
    else:
        lines.append("No P0/P1/P2 issues detected by the static use case tester.")

    lines.extend([
        "",
        "## Act Improvements",
        "",
        "Prioritize P0, then P1, then P2. Re-run the use case tester after updating the creator rules or the candidate skill.",
    ])
    (out_dir / "use-case-test-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    act_lines = ["# Act Improvements", ""]
    if result["issues"]:
        for issue in result["issues"]:
            act_lines.append(f"- [{issue['priority']}] Fix `{issue['type']}`: {issue['detail']}")
    else:
        act_lines.append("- No blocking static issues. Continue with business review or stop if the score is above threshold.")
    (out_dir / "act-improvements.md").write_text("\n".join(act_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a pdca-skill-creator use case test against a generated candidate skill.")
    parser.add_argument("--skill-dir", required=True, help="Generated skill directory to test.")
    parser.add_argument("--out", required=True, help="Directory for use-case-test.json and reports.")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    out_dir = Path(args.out).resolve()
    if not skill_dir.exists():
        raise SystemExit(f"skill-dir not found: {skill_dir}")

    result = run_use_case_test(skill_dir)
    write_report(result, out_dir)
    print(json.dumps({"passed": result["passed"], "score": result["score"], "out": str(out_dir)}, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
