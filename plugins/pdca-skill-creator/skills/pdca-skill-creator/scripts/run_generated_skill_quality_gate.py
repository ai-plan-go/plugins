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
    ("executable_scaffold", 12, ["init_project.py", "run_task.py", "check_outputs.py", "smoke_test.py", "退出码|exit code", "日志|log", "结构化|structured"]),
    ("contract_consistency", 12, ["check-rules", "output-schema", "required_outputs", "outputs", "deployment-contract", "schema", "规则|rule"]),
    ("evidence_and_logs", 10, ["证据|evidence", "日志|log", "diagnostic|诊断", "P0", "P1", "P2"]),
    ("lifecycle_isolation", 8, ["生命周期|lifecycle", "准备阶段|preparation phase", "运行阶段|runtime phase", "复盘阶段|review phase", "创建器反馈出口|creator feedback outlet", "lifecycle-contract", "run_id", "改动提案|change proposal"]),
    ("self_optimization", 8, ["自我优化|self-optimization", "自我进化|self-evolution", "复测|retest|re-test", "plan-history", "Act"]),
    ("clean_packaging", 6, ["__pycache__", "work_smoke", "临时|temporary", "打包|package"]),
]


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "scripts/init_project.py",
    "scripts/run_task.py",
    "scripts/check_outputs.py",
    "scripts/smoke_test.py",
    "references/do-run-plan.md",
    "references/script-design.md",
    "references/ai-decision-checklist.md",
    "references/deployment-contract.md",
    "references/data-provenance-contract.md",
    "references/lifecycle-contract.md",
    "references/plan-history.md",
]


CONFIRMATION_KEYWORDS = [
    "整体需求确认表",
    "整体确认",
    "业务自动化分析",
    "脚本固化",
    "AI 决策点",
]


SCRIPT_DESIGN_KEYWORDS = [
    "脚本与职责",
    "业务主流程",
    "输入",
    "输出",
    "异常",
    "证据",
    "已覆盖",
    "未覆盖",
]


AI_DECISION_KEYWORDS = [
    "AI 不得自行决定",
    "AI 允许自行完成",
    "脚本固化",
    "AI 决策点",
    "用户确认",
    "正式运行",
]


CRAWLER_CONFIRMATION_KEYWORDS = [
    "爬虫抓取范围",
    "筛选条件",
    "详情页",
    "分页",
    "试抓",
    "字段映射",
    "页面信息",
    "输出字段",
    "转换规则",
    "缺失处理",
]


DATA_PROVENANCE_KEYWORDS = [
    "AI 不得|AI must not|AI cannot",
    "脚本|script",
    "run-manifest|run_manifest|运行清单",
    "数据来源|data source",
    "处理流程|processing",
    "处理结果|result",
    "脚本版本|script version|脚本哈希|script hash",
    "文件哈希|file hash",
    "记录数|record count",
    "证据路径|evidence path",
    "退出码|exit code",
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


def script_uses_playwright(script_text: str) -> bool:
    return bool(re.search(r"playwright|async_playwright|sync_playwright", script_text, re.I))


def script_uses_http_client(script_text: str) -> bool:
    return bool(re.search(r"urlopen|requests\.|httpx|aiohttp|invoke-webrequest|invoke-restmethod|\biwr\b|\birm\b|curl", script_text, re.I))


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

    run_task = read_text(skill_dir / "scripts" / "run_task.py")
    check_outputs = read_text(skill_dir / "scripts" / "check_outputs.py")
    smoke_test = read_text(skill_dir / "scripts" / "smoke_test.py")
    run_daily = read_text(skill_dir / "scripts" / "run_daily_check.ps1")
    do_run_plan = read_text(skill_dir / "references" / "do-run-plan.md")
    script_design = read_text(skill_dir / "references" / "script-design.md")
    ai_decision_checklist = read_text(skill_dir / "references" / "ai-decision-checklist.md")
    deployment_contract = read_text(skill_dir / "references" / "deployment-contract.md")
    data_provenance_contract = read_text(skill_dir / "references" / "data-provenance-contract.md")
    business_profile = read_text(skill_dir / "references" / "business-use-case-profile.json")
    business_test = read_text(skill_dir / "scripts" / "run_business_use_case_test.py")
    lifecycle_contract = read_text(skill_dir / "references" / "lifecycle-contract.md")
    scoring_text = "\n".join([
        text,
        do_run_plan,
        script_design,
        ai_decision_checklist,
        deployment_contract,
        data_provenance_contract,
        lifecycle_contract,
        plan_history,
    ])

    for name, points, keywords in RUBRIC:
        score, missing = keyword_score(scoring_text, keywords, points)
        dimensions[name] = {"score": score, "max": points, "missing_keywords": missing}
        total += score

    if any((skill_dir / "references" / name).exists() for name in ["check-rules.yaml", "check-rules.yml", "check-rules.json"]) and not script_mentions(check_outputs, "check-rules"):
        issues.append({"priority": "P1", "type": "check_rules_not_consumed", "detail": "check_outputs.py should read references/check-rules.yaml"})
    if (skill_dir / "references" / "output-schema.json").exists() and not script_mentions(check_outputs, "output-schema"):
        issues.append({"priority": "P1", "type": "schema_not_consumed", "detail": "check_outputs.py should read references/output-schema.json"})
    if any((skill_dir / "references" / name).exists() for name in ["selectors.yaml", "selectors.yml", "selectors.json"]) and not script_mentions(run_task, "selectors"):
        issues.append({"priority": "P1", "type": "selectors_not_consumed", "detail": "run_task.py should read references/selectors.yaml"})
    if run_task and script_uses_http_client(run_task) and not script_uses_playwright(run_task):
        issues.append({"priority": "P1", "type": "crawler_framework_http_only", "detail": "run_task.py appears to use an HTTP client without a Playwright page-access path"})
    site_probe_text = run_task + "\n" + do_run_plan + "\n" + deployment_contract
    if re.search(r"站点摸底|字段映射|试抓|site probe|field mapping|probe", site_probe_text, re.I):
        if script_uses_http_client(site_probe_text) and not script_uses_playwright(site_probe_text):
            issues.append({"priority": "P1", "type": "period1_probe_http_only", "detail": "period-1 site probing or field mapping must be Playwright-first; HTTP clients may only be auxiliary diagnostics"})
    if smoke_test and not re.search(r"init_project|run_task|check_outputs", smoke_test, re.I):
        issues.append({"priority": "P1", "type": "weak_smoke_test", "detail": "smoke_test.py should exercise init/run/check chain"})
    missing_provenance = [keyword for keyword in DATA_PROVENANCE_KEYWORDS if not any(part.lower() in data_provenance_contract.lower() for part in keyword.split("|"))]
    if missing_provenance:
        issues.append({"priority": "P1", "type": "incomplete_data_provenance_contract", "detail": "data-provenance-contract.md missing: " + ", ".join(missing_provenance)})
    if run_task and not re.search(r"data-provenance|run[_-]manifest|运行清单", run_task, re.I):
        issues.append({"priority": "P1", "type": "run_manifest_not_generated", "detail": "run_task.py should write a data provenance run-manifest in the work/output directory"})
    if check_outputs and not re.search(r"data-provenance|run[_-]manifest|运行清单", check_outputs, re.I):
        issues.append({"priority": "P1", "type": "run_manifest_not_checked", "detail": "check_outputs.py should validate the data provenance run-manifest"})
    confirmation_blob = deployment_contract + "\n" + text
    missing_confirmation = [keyword for keyword in CONFIRMATION_KEYWORDS if keyword.lower() not in confirmation_blob.lower()]
    if missing_confirmation:
        issues.append({"priority": "P1", "type": "incomplete_preflight_confirmation", "detail": "missing overall confirmation fields: " + ", ".join(missing_confirmation)})
    lifecycle_required = ["准备阶段|preparation phase", "运行阶段|runtime phase", "复盘阶段|review phase", "创建器反馈出口|creator feedback outlet", "run_id", "outputs", "改动提案|change proposal", "创建器反馈|creator feedback"]
    lifecycle_missing = [item for item in lifecycle_required if not any(part.lower() in lifecycle_contract.lower() for part in item.split("|"))]
    if lifecycle_missing:
        issues.append({"priority": "P1", "type": "incomplete_lifecycle_contract", "detail": "lifecycle-contract.md missing: " + ", ".join(lifecycle_missing)})
    if re.search(r"active_period|当前请求时期|时期\s*`?[0-3]`?", text, re.I):
        issues.append({"priority": "P1", "type": "creator_internal_state_leaked", "detail": "business SKILL.md should not expose creator-only active_period or numbered creator periods"})
    creator_process_terms = [
        r"Step\s*1\s*-\s*需求检查确认",
        r"Step\s*2\s*-\s*创建器包装",
        r"Step\s*3\s*-\s*业务核心收敛",
        r"创建器包装",
        r"包装后的技能创建目标",
        r"本轮禁止",
        r"允许的试抓",
        r"生成来源",
        r"整体需求确认表",
        r"自我优化能力分层",
    ]
    leaked_terms = [pattern for pattern in creator_process_terms if re.search(pattern, text, re.I)]
    if leaked_terms:
        issues.append({"priority": "P1", "type": "creator_process_leaked_to_business_skill", "detail": "business SKILL.md leaks creator process terms: " + ", ".join(leaked_terms)})
    if not re.search(r"Step\s*1\s*-\s*需求检查确认|需求检查确认步骤", deployment_contract + "\n" + plan_history, re.I):
        issues.append({"priority": "P1", "type": "missing_named_requirement_confirmation_step", "detail": "references should record the named Step 1 requirement-confirmation step"})
    missing_script_design = [keyword for keyword in SCRIPT_DESIGN_KEYWORDS if keyword.lower() not in script_design.lower()]
    if missing_script_design:
        issues.append({"priority": "P1", "type": "incomplete_script_design_doc", "detail": "script-design.md missing: " + ", ".join(missing_script_design)})
    missing_ai_decision = [keyword for keyword in AI_DECISION_KEYWORDS if keyword.lower() not in ai_decision_checklist.lower()]
    if missing_ai_decision:
        issues.append({"priority": "P1", "type": "incomplete_ai_decision_checklist", "detail": "ai-decision-checklist.md missing: " + ", ".join(missing_ai_decision)})
    if run_task and re.search(r"(?:skill_dir|skill_root|__file__).{0,80}(?:write_text|open\s*\()", run_task, re.I | re.S):
        issues.append({"priority": "P1", "type": "runtime_writes_skill_source", "detail": "run_task.py appears to write runtime evidence under the skill source; use the configured work/output directory"})
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
        powershell_probe_text = run_daily + "\n" + do_run_plan + "\n" + deployment_contract
        if not re.search(r"PowerShell|\.ps1|\$Python|-Python", powershell_probe_text, re.I):
            issues.append({"priority": "P1", "type": "missing_windows_powershell_fallback", "detail": "crawler skills should document a Windows PowerShell host-run path for Playwright when Codex sandbox blocks browser startup"})
        if not re.search(r"sample|expected|样例|期望|candidate|候选", business_profile + business_test + smoke_test, re.I):
            issues.append({"priority": "P1", "type": "missing_business_sample_expectation", "detail": "crawler/classification tests should include sample expected key fields and classification outcome"})
        missing_crawler_confirmation = [keyword for keyword in CRAWLER_CONFIRMATION_KEYWORDS if keyword.lower() not in confirmation_blob.lower()]
        if missing_crawler_confirmation:
            issues.append({"priority": "P1", "type": "incomplete_crawler_confirmation_contract", "detail": "crawler confirmation is missing: " + ", ".join(missing_crawler_confirmation)})
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
