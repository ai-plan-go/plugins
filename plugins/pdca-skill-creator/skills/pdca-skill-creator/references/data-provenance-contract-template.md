# 数据可追溯契约模板

生成的 L3/L4 业务技能将本模板业务化为 `references/data-provenance-contract.md`。业务数据、运行日志、检查结果和报表数值只能由已确认的脚本或确定性工具写入；AI 不得直接生成、补造、回填或改写这些运行产物。

## 数据生成边界

- 允许写入业务数据的生成者：`scripts/run_task.py`、`scripts/check_outputs.py` 或用户确认的等价确定性工具。
- AI 允许输出：代码、规则、解释、复盘提案和待确认说明；这些内容不得混入结构化业务数据、运行日志、基线或同步输入。
- 数据源不可访问、字段无法提取或规则无法判断时，写入结构化阻断诊断和未验证状态，不填充推测值。

## 运行清单

Do 脚本必须在 `{work_root}/outputs/{run_id}/run-manifest.json` 或等价路径写入以下内容：

```json
{
  "run_id": "task-YYYYMMDD-HHMMSS",
  "started_at": "ISO-8601",
  "finished_at": "ISO-8601",
  "mode": "dry-run|live|stub",
  "trigger_source": "manual|scheduler|codex_automation",
  "generator": {
    "type": "script",
    "path": "scripts/run_task.py",
    "version_or_hash": "..."
  },
  "sources": [
    {
      "type": "url|file|api|user_input",
      "locator": "...",
      "retrieved_at": "ISO-8601",
      "fingerprint": "file hash or response summary",
      "record_count": 0,
      "access_status": "ok|blocked|partial"
    }
  ],
  "processing": [
    {
      "step": 1,
      "rule_or_function": "...",
      "input_count": 0,
      "output_count": 0,
      "description": "filter/deduplicate/transform",
      "error_count": 0
    }
  ],
  "results": [
    {
      "path": "...",
      "file_hash": "...",
      "record_count": 0,
      "schema_version": "...",
      "quality_metrics": {},
      "evidence_paths": []
    }
  ],
  "diagnostics": [],
  "exit_code": 0,
  "eligible_for_baseline_or_sync": false
}
```

## Check 规则

`scripts/check_outputs.py` 必须读取运行清单，并至少校验：

- 运行清单、来源和输出路径存在且位于工作目录。
- `generator.type` 为 `script` 或用户确认的确定性工具，且脚本版本或哈希存在。
- 来源、处理和结果三段均有记录；记录数、文件哈希和 schema 可验证或明确标为未验证。
- 任何 `blocked`、`partial`、未验证字段或不一致记录会阻止基线更新和外部同步。
- 检查结论引用 `run_id`、来源/结果路径和证据路径，不凭 AI 叙述生成数据结论。
