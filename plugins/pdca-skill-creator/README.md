# PDCA Skill Creator 工作区说明

本目录用于维护 `pdca-skill-creator` 的开发源码和 GitHub 插件发布包。由于多个会话会共同维护本项目，后续编辑请先按本文确认文件职责，避免改错副本或误删发布文件。

## 发布识别信息

- 插件名称：`pdca-skill-creator`
- 插件市场：`ai-plan-go`
- 发布仓库：<https://github.com/ai-plan-go/plugins>
- Git 地址：`https://github.com/ai-plan-go/plugins.git`
- 当前版本：`0.2.9`
- 发布仓库目录：`plugins-publish/`

## 能力分组

### 需求与业务核心

- 将用户输入拆分为业务需求、产品形态、技术偏好和固定约束。
- 先识别“没有它就不算完成业务”的核心动作，再补 PDCA、报表、日志、基准和复盘结构。
- 对网页巡检、爬虫和页面状态采集任务，要求生成真实采集框架：URL、Playwright 访问、DOM 提取、截图、错误分类和结构化落盘。
- 页面选择器未知时生成 `references/selectors.yaml`，并要求采集脚本实际读取和消费。

### PDCA 结构与可执行脚手架

- 生成业务化 Plan、Do、Check、Act 阶段，明确输入、动作、产物、异常处理、证据和用户确认点。
- 对巡检、监控、报表、爬虫、数据检查和周期性运营动作，默认生成 L3 最小可执行脚手架。
- 标准脚本包括 `init_project.py`、`run_task.py`、`check_outputs.py`、`smoke_test.py` 和按需定时入口。
- 生成 L3/L4 可执行技能时，必须同步生成 `references/do-run-plan.md`，说明 Do 脚本运行入口、参数、流程、产物、日志、异常和 Check 衔接。
- Check 脚本必须读取规则文件和输出 schema，不能只把规则写在文档里。

### 成熟度、证据与契约一致性

- 区分目标成熟度和当前成熟度，避免把占位脚手架描述成可部署系统。
- 生成能力矩阵和业务核心实现矩阵，逐项标注已实现、占位、待确认、证据和缺口。
- 校验 `check-rules`、`output-schema`、Do 输出、Check 检查字段和部署契约的一致性。
- 区分预期失败和非预期失败：dry-run 空字段可以预期，字段名不一致、规则未读取、schema 不匹配必须修复。

### 质量门禁与评分

- 创建器自测保留 `scripts/run_creator_use_case_test.py`，默认用亚马逊 ASIN 用例做回归测试。
- 通用评分抽象为 `scripts/run_generated_skill_quality_gate.py`，只检查所有 PDCA 技能共通规范，不包含业务关键词。
- 生成业务技能时，要求同步生成 `scripts/score_skill_quality.py` 和 `references/skill-quality-rubric.json`，用于通用规范验收。
- 生成业务技能时，要求同步生成 `scripts/run_business_use_case_test.py` 和 `references/business-use-case-profile.json`，用于当前业务专属验收。
- 默认通过线为 85 分，且不能存在 P0/P1 阻断项。

### 自我优化与复测

- 生成技能必须区分“自我优化机制”“自我优化可执行”“自我进化有效性”。
- Act 产物必须包含复测入口和复测证据路径；未运行复测时必须标为“待确认”或“未验证”。
- 用例测试支持多轮生成、评分、报告、Act 改进和复测；达到通过标准后停止，不为凑轮次重复测试。

### 插件交付与清洁发布

- 用户要求插件或 Codex 可安装产物时，默认生成 `.codex-plugin/plugin.json` 和 `skills/` 目录。
- zip 只能作为附加传输包，不能替代可安装插件目录。
- 成品目录不得包含 `__pycache__/`、`*.pyc`、`work_smoke/`、临时日志和本地测试输出。
- 评分脚本支持普通技能目录和可安装插件根目录，报告会标明请求目录、实际识别目录和候选类型。

## 版本摘要

| 版本 | 主要变化 |
|---|---|
| 0.2.9 | 新增 Do 脚本流程计划文档要求，避免生成插件的运行脚本成为黑盒。 |
| 0.2.8 | 新增步骤检查确认表门禁，要求逐项确认参数、状态、风险和处理动作后再生成自动化技能。 |
| 0.2.7 | 强化自动化任务生成前确认、Codex 安排任务识别、可安装插件门禁和 smoke 写入边界检查。 |
| 0.2.6 | 拆分通用规范评分和业务用例评分，新增生成技能双层质量门禁。 |
| 0.2.5 | 强化自我优化能力分层、复测证据路径、插件形态测试识别和清洁发布。 |
| 0.2.4 | 新增创建器用例测试闭环、默认亚马逊 ASIN 回归用例和确定性测试脚本。 |
| 0.2.3 | 强化可安装插件交付、输出契约一致性、选择器消费和 smoke test 判错。 |
| 0.2.2 | 强化业务核心优先和爬虫类真实采集框架，避免 PDCA 外壳挤掉核心业务。 |
| 0.2.1 | 建立成熟度分级、能力边界、检查器生成和生成后自检要求。 |

## 目录职责

```text
pdca-skill-creator/
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── run_creator_use_case_test.py
│   └── run_generated_skill_quality_gate.py
├── references/
│   └── pdca-stage-template.md
├── codex-skill-creator.txt
└── plugins-publish/
    ├── README.md
    ├── README.zh-CN.md
    ├── marketplace.json
    ├── .agents/
    │   └── plugins/marketplace.json
    └── plugins/
        └── pdca-skill-creator/
```

- 根目录 `SKILL.md`、`agents/`、`references/` 是开发源码。
- `codex-skill-creator.txt` 是早期设计稿和补充约束记录，只在需要追溯设计意图时参考。
- `plugins-publish/` 是实际发布到 GitHub 的插件市场仓库，远程为 `https://github.com/ai-plan-go/plugins.git`。
- `plugins-publish/plugins/pdca-skill-creator/skills/pdca-skill-creator/` 是发布包内的技能副本，发布前需要和根目录源码同步。
- `plugins-publish/.agents/plugins/marketplace.json` 和 `plugins-publish/marketplace.json` 都是发布仓库的一部分，不视为无用重复文件。

## 推荐维护流程

1. 先修改根目录源码：`SKILL.md`、`agents/openai.yaml`、`scripts/`、`references/`。
2. 将源码同步到发布包：
   - `SKILL.md` -> `plugins-publish/plugins/pdca-skill-creator/skills/pdca-skill-creator/SKILL.md`
   - `agents/openai.yaml` -> `plugins-publish/plugins/pdca-skill-creator/skills/pdca-skill-creator/agents/openai.yaml`
   - `scripts/` -> `plugins-publish/plugins/pdca-skill-creator/skills/pdca-skill-creator/scripts/`
   - `references/` -> `plugins-publish/plugins/pdca-skill-creator/skills/pdca-skill-creator/references/`
3. 更新 `plugins-publish/plugins/pdca-skill-creator/.codex-plugin/plugin.json` 中的版本和描述。
4. 校验插件包。
5. 在 `plugins-publish/` Git 仓库中提交并推送。

## 清理规则

可以清理：

- 根目录下空的临时目录。
- 未被 Git 跟踪、且不是源码或发布包的一次性生成文件。
- 明确过期的本地缓存刷新版本号，例如只用于本机重装的 `+codex.*` 后缀。

不要清理：

- `plugins-publish/.git/`，这是发布仓库的 Git 元数据。
- `plugins-publish/.agents/plugins/marketplace.json`，这是发布市场配置。
- `plugins-publish/plugins/pdca-skill-creator/`，这是发布插件包。
- 根目录 `SKILL.md`、`agents/`、`references/`，这是开发源码。

## 当前已知状态

- 根目录源码和发布包内技能副本已同步到 `0.2.9`。
- 上一版 GitHub 发布提交：`a622c93 Release pdca-skill-creator 0.2.2`。
- 发布地址：<https://github.com/ai-plan-go/plugins>
