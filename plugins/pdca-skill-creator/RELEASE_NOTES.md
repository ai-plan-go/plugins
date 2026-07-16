# pdca-skill-creator 0.2.29

发布日期：2026-07-16

## 本次优化

1. 新增业务 `SKILL.md` 与创建器审计信息的隔离规则：业务入口只写触发场景、输入、运行、输出、检查、边界和复盘入口。
2. 将创建器包装、完整需求确认表、生成来源、成熟度审计和自我优化分层默认迁移到 `references/plan-history.md` 或 `references/deployment-contract.md`。
3. 更新生成质量门禁：业务 `SKILL.md` 泄漏 `Step 1 - 需求检查确认`、`Step 2 - 创建器包装`、包装层字段或生成审计信息时标记为 P1。
4. 保留创建器对话中的确认门禁，但不再要求业务入口文档暴露创建器步骤。

## 同步修改范围

- `.codex-plugin/plugin.json`
- `skills/pdca-skill-creator/SKILL.md`
- `skills/pdca-skill-creator/references/pdca-stage-template.md`
- `skills/pdca-skill-creator/scripts/run_generated_skill_quality_gate.py`
- `skills/pdca-skill-creator/scripts/run_creator_use_case_test.py`

## 发布说明

- 当前目录即为可发布插件目录，插件版本为 `0.2.29`。
