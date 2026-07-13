#!/usr/bin/env python3
"""Run a generic PDCA generated-skill quality gate.

This checker intentionally avoids business-specific terms. It validates the
common contract every PDCA-generated skill should satisfy.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


RUBRIC = [
    ("pdca_stage_contract", 12, ["Plan", "Do", "Check", "Act", "输入|input", "动作|action", "产物|output", "异常处理|exception"]),
    ("source_and_maturity", 12, ["pdca-skill-creator", "创建器版本|creator version", "目标成熟度|target maturity", "当前成熟度|current maturity", "L1|L2|L3|L4", "占位|待确认|placeholder|pending"]),
    ("business_core", 10, ["业务核心|business core", "核心动作|core action", "实现矩阵|implementation matrix", "证据|evidence", "缺口|gap"]),
    ("capability_matrix", 10, ["能力矩阵|capability matrix", "已实现|implemented", "占位|placeholder", "待确认|pending", "证据|evidence"]),
    ("executable_scaffold", 14, ["init_project.py", "run_task.py", "check_outputs.py", "smoke_test.py", "退出码|exit code", "日志|log", "结构化|structured"]),
    ("contract_consistency", 14, ["check-rules", "output-schema", "required_outputs", "outputs", "deployment-contract", "schema", "规则|rule"]),
    ("evidence_and_logs", 10, ["证据|evidence", "日志|log", "diagnostic|诊断", "P0", "P1", "P2"]),
    ("self_optimization", 10, ["自我优化|self-optimization", "自我进化|self-evolution", "复测|retest|re-test", "plan-history", "Act"]),
    ("clean_packaging", 8, ["__pycache__", "work_smoke", "临时|temporary", "打包|package"]),
]


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "scripts/init_project.py",
    "scripts/run_task.py",
    "scripts/check_outputs.py",
    "scripts/smoke_test.py",
    "references/deployment-contract.md",
    "references/plan-history.md",
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return ""


def resolve_skill_dir(candidate_dir: Path) -> tuple[Path, str]:
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


def all_text(skill_dir: Path) -> str:
    parts: list[str] = []
    for path in skill_dir.rglob("*"):
        rel_parts = set(path.relative_to(skill_dir).parts)
        if "__pycache__" in rel_parts or "work_smoke" in rel_parts:
            continue
        if path.is_file() and path.suffix.lower() in {".md", ".py", ".ps1", ".json", ".yaml", ".yml", ".txt"}:
            parts.append(f"\n\n--- {path.relative_to(skill_dir).as_posix()} ---\n")
            parts.append(read_text(path))
    return "\n".join(parts)


def keyword_score(text: str, keywords: list[str], points: int) -> tuple[int, list[str]]:
    lowered = text.lower()
    hits: list[str] = []
    missing: list[str] = []
    for keyword in keywords:
        alternatives = [part.strip().lower() for part in keyword.split("|")]
        if any(part in lowered for part in alternatives):
            hits.append(keyword)
        else:
            missing.append(keyword)
    return round(points * len(hits) / len(keywords)), missing


def script_mentions(script_text: str, hint: str) -> bool:
    return hint.lower() in script_text.replace("\\", "/").lower()


def forbidden_files(skill_dir: Path) -> list[str]:
    found: list[str] = []
    for path in skill_dir.rglob("*"):
        rel = path.relative_to(skill_dir)
        if (
            "__pycache__" in rel.parts
            or "work_smoke" in rel.parts
            or "tmp_smoke" in rel.parts
            or path.suffix.lower() == ".pyc"
            or path.name in {"business-use-case-test.json", "business-use-case-test-report.md", "business-act-improvements.md"}
        ):
            found.append(rel.as_posix())
    return sorted(found)


def maturity_overclaim(text: str) -> bool:
    current_lines = [line.strip() for line in text.splitlines() if re.search(r"当前成熟度|current maturity", line, re.I)]
    claims_l4 = [
        line
        for line in current_lines
        if "L4" in line
        and not re.search(r"不可标为\s*L4|不得标为\s*L4|不能标为\s*L4|not\s+be\s+marked\s+as\s+L4", line, re.I)
        and not re.search(r"目标成熟度|target maturity", line, re.I)
    ]
    return bool(claims_l4 and re.search(r"stub|placeholder|not_configured|TODO|占位|dry-run only", text, re.I))


def run_quality_gate(candidate_dir: Path) -> dict:
    requested_dir = candidate_dir
    skill_dir, candidate_type = resolve_skill_dir(candidate_dir)
    text = all_text(skill_dir)
    issues: list[dict] = []
    dimensions: dict[str, dict] = {}
    total = 0

    missing_required = [name for name in REQUIRED_FILES if not (skill_dir / name).exists()]
    for name in missing_required:
        issues.append({"priority": "P0", "type": "missing_required_file", "detail": name})

    forbidden = forbidden_files(skill_dir)
    if forbidden:
        issues.append({"priority": "P1", "type": "unclean_deliverable", "detail": ", ".join(forbidden[:8])})

    for name, points, keywords in RUBRIC:
        score, missing = keyword_score(text, keywords, points)
        dimensions[name] = {"score": score, "max": points, "missing_keywords": missing}
        total += score

    run_task = read_text(skill_dir / "scripts" / "run_task.py")
    check_outputs = read_text(skill_dir / "scripts" / "check_outputs.py")
    smoke_test = read_text(skill_dir / "scripts" / "smoke_test.py")
    run_daily = read_text(skill_dir / "scripts" / "run_daily_check.ps1")
    do_run_plan = read_text(skill_dir / "references" / "do-run-plan.md")
    deployment_contract = read_text(skill_dir / "references" / "deployment-contract.md")
    business_profile = read_text(skill_dir / "references" / "business-use-case-profile.json")
    business_test = read_text(skill_dir / "scripts" / "run_business_use_case_test.py")

    if any((skill_dir / "references" / name).exists() for name in ["check-rules.yaml", "check-rules.yml", "check-rules.json"]) and not script_mentions(check_outputs, "check-rules"):
        issues.append({"priority": "P1", "type": "check_rules_not_consumed", "detail": "check_outputs.py should read references/check-rules.yaml"})
    if (skill_dir / "references" / "output-schema.json").exists() and not script_mentions(check_outputs, "output-schema"):
        issues.append({"priority": "P1", "type": "schema_not_consumed", "detail": "check_outputs.py should read references/output-schema.json"})
    if any((skill_dir / "references" / name).exists() for name in ["selectors.yaml", "selectors.yml", "selectors.json"]) and not script_mentions(run_task, "selectors"):
        issues.append({"priority": "P1", "type": "selectors_not_consumed", "detail": "run_task.py should read references/selectors.yaml"})
    if smoke_test and not re.search(r"init_project|run_task|check_outputs", smoke_test, re.I):
        issues.append({"priority": "P1", "type": "weak_smoke_test", "detail": "smoke_test.py should exercise init/run/check chain"})
    if run_daily and re.search(r"^\s*python\s+", run_daily, re.I | re.M) and not re.search(r"\$Python|param\s*\([^)]*Python", run_daily, re.I | re.S):
        issues.append({"priority": "P1", "type": "run_daily_hardcodes_python", "detail": "run_daily_check.ps1 should accept a configurable Python path"})
    if candidate_type == "plugin":
        install_text = do_run_plan + "\n" + deployment_contract + "\n" + text
        missing_install_terms = [term for term in ["安装", "重装", "缓存", ".codex-plugin", "plugin.json", "skills/"] if term.lower() not in install_text.lower()]
        if missing_install_terms:
            issues.append({"priority": "P1", "type": "missing_install_verification", "detail": "plugin install verification missing: " + ", ".join(missing_install_terms)})
    if re.search(r"爬|crawl|crawler|采集|抓取|网页|页面", text, re.I):
        expected_terms = ["network_permission_denied", "timeout", "http_error", "captcha_or_login", "selector_miss"]
        missing_diag = [term for term in expected_terms if term.lower() not in (run_task + check_outputs + deployment_contract).lower()]
        if len(missing_diag) >= 3:
            issues.append({"priority": "P1", "type": "weak_network_diagnostics", "detail": "crawler diagnostics should distinguish common failure causes; missing: " + ", ".join(missing_diag)})
        if not re.search(r"sample|expected|样例|期望|candidate|候选", business_profile + business_test + smoke_test, re.I):
            issues.append({"priority": "P1", "type": "missing_business_sample_expectation", "detail": "crawler/classification tests should include sample expected key fields and classification outcome"})
    if maturity_overclaim(text):
        issues.append({"priority": "P1", "type": "possible_maturity_overclaim", "detail": "current maturity appears to claim L4 while placeholder markers exist"})
    if not re.search(r"自我优化|self[- ]?optimization", text, re.I) or not re.search(r"复测|retest|re-test", text, re.I):
        issues.append({"priority": "P1", "type": "missing_self_optimization_gate", "detail": "self-optimization layer and retest entry are not explicit"})

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
        "threshold": 85,
        "passed": passed,
        "dimension_scores": dimensions,
        "issues": issues,
        "summary": {"p0": len(p0), "p1": len(p1), "p2": len([item for item in issues if item["priority"] == "P2"])},
    }


def write_outputs(result: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "skill-quality-gate.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Generated Skill Quality Gate",
        "",
        f"- Tested at: {result['tested_at']}",
        f"- Requested candidate: `{result['requested_dir']}`",
        f"- Resolved skill: `{result['skill_dir']}`",
        f"- Candidate type: {result['candidate_type']}",
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
        lines.append("No P0/P1/P2 issues detected by the generic quality gate.")

    (out_dir / "skill-quality-gate-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a generic quality gate against a generated PDCA skill or plugin.")
    parser.add_argument("--skill-dir", required=True, help="Generated skill directory or installable plugin root.")
    parser.add_argument("--out", required=True, help="Output directory for quality gate reports.")
    args = parser.parse_args()

    candidate_dir = Path(args.skill_dir).resolve()
    if not candidate_dir.exists():
        raise SystemExit(f"skill-dir not found: {candidate_dir}")

    result = run_quality_gate(candidate_dir)
    write_outputs(result, Path(args.out).resolve())
    print(json.dumps({"passed": result["passed"], "score": result["score"], "out": str(Path(args.out).resolve())}, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
