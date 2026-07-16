# 生命周期时期协议

本协议将 `pdca-skill-creator` 的工作分为四个隔离时期。目的不是增加文档，而是让每次需求只加载必要上下文、只修改允许范围内的内容，并让业务技能的运行反馈可控地回流到创建器。

通过 `pdca-skill-creator` 进入的业务需求，先执行“创建器包装层”：原始需求只作为目标业务能力描述，必须被改写为“创建/升级某个业务技能”的时期 1 任务。包装层完成前，不得进入搜索、真实抓取、运行脚本或输出最终业务结果。

## 时期定义

| 时期 | 名称 | 主体 | 允许写入 | 不允许写入 |
|---|---|---|---|---|
| `0` | 创建器更新迭代期 | 创建器源码与发布包 | `SKILL.md`、模板、门禁、回归用例、版本和发布包 | 业务技能的运行数据、未经脱敏的业务反馈 |
| `1` | 生成业务技能期 | 业务技能源码与设计契约 | `SKILL.md`、脚本、规则、部署契约、测试基线、时期 1 Plan 历史 | 伪造运行证据、未确认生产参数 |
| `2` | 业务技能使用与检查期 | 某一次业务运行 | 用户指定工作目录下的 `outputs/`、`logs/`、`evidence/` | 技能源码、`references/` 规则、基线、创建器源码 |
| `3` | 业务技能复盘期 | 时期 2 证据与用户反馈 | 复盘报告、改动提案、复测计划、反馈包 | 未确认的源码/规则修改、直接发布创建器 |

## 需求分流模板

每个需求先记录以下字段；复合需求拆成多条，不用一个时期覆盖全部。

| 字段 | 说明 |
|---|---|
| `request_id` | 本次需求或提案编号 |
| `active_period` | `0`、`1`、`2` 或 `3` |
| `subject` | 创建器、业务技能或一次运行 |
| `creator_wrapper` | 仅时期 1 必填；记录原始业务目标、包装后的技能创建目标、本轮禁止的直接执行动作 |
| `source_evidence` | 仅记录当前时期所需的文件路径、运行编号或用户确认 |
| `allowed_write_scope` | 本期允许修改的目录/文件 |
| `blocked_actions` | 本期禁止的动作 |
| `exit_condition` | 进入下一时期前需要满足的条件 |
| `next_period` | 计划进入的下一时期；没有则填 `none` |

## Subagent 双上下文合同

时期 1 可使用 subagent 做业务核心封装或最小业务探索，但它们都是受限设计/诊断角色，不是业务执行角色。主 agent 维护技能封装、用户确认与时期切换；业务封装 subagent 只定义 Do/Check 合同，探索 subagent 只确认未知字段、页面状态、选择器或外部限制。

使用业务封装 subagent 时，业务技能必须创建 `references/business-core-boundary.md`，至少包含：

```text
主任务时期：1
主任务目标：创建/升级业务 skill；不执行业务 Do
业务封装问题：
允许输入：用户需求、确认表、脱敏规则和最小必要历史片段
禁止输入：真实全量业务数据、完整页面样本、时期 2 日志和最终报表
禁止动作：真实 Do/Check、批量采集、最终报表、基线更新、外部同步、时期切换和发布
返回文件：business-core-summary.json
返回字段：do_core_actions、inputs、outputs、check_rules、exception_taxonomy、evidence_requirements、open_decisions、coverage_gaps、confidence
主 agent 转写目标：业务核心实现计划、Do 计划、脚本设计、Check 规则、输出 schema、AI 决策检查单
停止条件：合同完整、存在待确认业务决策或达到约定范围
```

`business-core-summary.json` 只是一份设计输入，不得包含真实业务结果、运行状态或最终报表行。主 agent 必须按确认表进行二次审查后才能把它写入技能契约。

使用 subagent 时，业务技能必须创建 `references/subagent-boundary.md`，至少包含：

```text
主任务时期：1
主任务目标：创建/升级业务 skill；不执行业务 Do
subagent 探索问题：
允许来源与样本上限：
隔离证据目录：{work_root}/work/probes/{probe_id}/
禁止写入：{work_root}/outputs/、baseline/、技能根目录、插件发布目录
禁止动作：批量采集、最终报表、基线更新、外部同步、时期 2 Do/Check
返回文件：probe-summary.json
返回字段：field_candidates、selector_candidates、source_fingerprints、evidence_paths、diagnostics、confidence、open_questions
停止条件：达到样本上限、出现登录/验证码/权限阻断、已覆盖字段映射问题
主 agent 消费规则：仅将摘要转化为设计契约、选择器、测试基线或待确认项
```

`probe-summary.json` 不得包含完整批量业务数据、最终报表内容或可直接当作业务结论的记录集。若探索需要保留原始片段，只能放在隔离证据目录，并以 URL 指纹和路径形式在摘要中引用。

## 生成业务技能必须创建的契约

在业务技能内创建 `references/lifecycle-contract.md`，至少包含下列内容：

```text
生命周期版本：1
当前默认时期：1（生成）
业务技能标识：
工作目录根路径：

创建器包装结果：
- 原始业务目标：
- 包装后的技能创建目标：
- 本轮禁止的直接执行业务动作：
- 允许的试抓/样例边界：

时期 1：需求确认、源码/契约生成和测试基线
时期 2：只写 {工作目录}/outputs、logs、evidence；禁止修改技能源码
时期 3：输出改动提案、影响范围、风险、用户确认点和复测计划
时期 0 反馈出口：{工作目录}/creator-feedback/{request_id}.json

时期切换记录：
- 来源时期：
- 目标时期：
- 原因：
- 证据路径：
- 允许修改范围：
- 回退或复测入口：
```

## 时期 2 运行约束

- 每次运行必须有唯一 `run_id`，推荐路径为 `{work_root}/outputs/{run_id}/`。
- 运行结果、日志、截图和 Check 诊断只写入该运行目录或用户指定等价目录。
- 业务数据、运行日志、检查结果和报表数值只能由已确认脚本或确定性工具写入；AI 只能引用这些产物解释、检查或提出提案，不得直接补写或伪造运行数据。
- 每次运行必须由 Do 脚本写入 `run-manifest.json` 或等价结构化清单，记录来源、处理步骤、结果摘要、脚本版本/哈希、证据路径和退出码；缺少清单的结果不得进入基线、同步或业务结论。
- 运行失败的修复建议只能写入诊断或时期 3 提案；不得在 Do/Check 过程中修改 `scripts/`、`references/` 或基线。
- 运行报告必须记录运行参数来源、使用的规则版本/哈希、退出码、证据路径和下一步时期建议。

## 时期 3 复盘与改动提案

复盘至少生成一个 `change-proposal.md` 或等价结构化文件，包含：

| 字段 | 要求 |
|---|---|
| 提案编号 | 可追溯到运行 `run_id` |
| 问题与证据 | 只引用时期 2 产物路径 |
| 根因类型 | 需求、实现、规则、环境、数据源或用户操作 |
| 目标时期 | `1`（业务技能）或 `0`（创建器） |
| 允许修改文件 | 精确文件列表；未知时不得实施 |
| 影响范围 | 业务功能、兼容性、成熟度、部署或成本 |
| 用户确认点 | 需要确认的业务选择或风险 |
| 复测计划 | 用例、成功标准、证据输出路径 |
| 回退方案 | 修改失败或结果退化时的恢复方法 |

业务技能提案回到时期 1 才能实施。创建器提案必须先去除业务敏感数据，并提交为反馈包。

## 创建器反馈包

时期 3 向时期 0 的反馈采用下列字段。它是候选改进输入，不是自动修改授权：

```json
{
  "feedback_id": "creator-feedback-YYYYMMDD-001",
  "source_skill": "example-skill",
  "source_period": 3,
  "target_period": 0,
  "anonymized": true,
  "reproducible_case": "简短、无敏感数据的复现描述",
  "evidence_paths": ["{work_root}/outputs/run-id/check-result.json"],
  "suggested_creator_scope": ["SKILL.md", "references/pdca-stage-template.md"],
  "expected_regression_test": "要补充或执行的创建器用例",
  "risk": "low|medium|high",
  "user_confirmation_required": true
}
```

时期 0 接收后必须：确认可泛化性、选择或新增回归用例、修改创建器规则/模板/脚本、运行回归、记录版本和发布同步。任何一步缺失，都不得声称创建器已吸收该反馈。

## 最小上下文原则

- 时期 0 读取创建器自身的相关规则、模板、测试与发布状态，不加载业务全量历史或截图。
- 时期 1 读取当前业务需求、确认表和相关 Plan 历史片段。
- 时期 1 使用业务封装 subagent 时，主 agent 只读取 `business-core-summary.json` 与所列开放决策；不将完整业务数据、运行日志或最终报表作为封装上下文。
- 时期 1 使用 subagent 时，主 agent 只读取 `probe-summary.json` 与最小必要证据索引；不加载完整页面文本、批量样本记录或截图，除非用户明确要求诊断且该内容与当前字段问题直接相关。
- 时期 2 默认只读取当前配置、最新规则和最新必要日志索引；不默认读完整 Plan 历史。
- 时期 3 读取指定运行的结构化结果、Check 结果和与提案有关的历史片段；不读取无关历史运行。
