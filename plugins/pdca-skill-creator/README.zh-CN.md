# PDCA Skill Creator 插件包

本目录是 `pdca-skill-creator` Codex 插件的可安装包目录。

## 文档角色

本 README 面向中文读者，说明这个插件包是什么、可执行技能位于哪里、以及如何核对版本。它和以下文件分工不同：

- `README.md`：同一插件包的英文说明。
- `../../README.md`：插件仓库或市场入口说明。
- `skills/pdca-skill-creator/SKILL.md`：面向 AI 的权威技能规则、工作流控制、模板和质量门禁。

如果本文件与 `skills/pdca-skill-creator/SKILL.md` 冲突，以 `SKILL.md` 为准。

## 版本

- 当前版本：`0.2.21`
- 清单文件：`.codex-plugin/plugin.json`
- 技能入口：`skills/pdca-skill-creator/SKILL.md`

## 这个插件提供什么

`pdca-skill-creator` 用于创建或升级带有 PDCA 闭环的 Codex 技能，适用于重复性流程、巡检、监控、报表、爬虫和运营自动化场景。

当前插件包要求生成的可执行技能至少具备：

- 四个相互隔离的生命周期时期：创建器演进期、业务技能生成期、运行与检查期、证据驱动复盘期。
- 在用户完整确认一张整体需求确认表之前，不得把创建器会话误当作最终业务执行。
- 对网页爬虫和前台巡检类技能，默认采用 Playwright-first 的真实页面访问链路；纯 HTTP 客户端只允许用于辅助诊断或离线样本准备，不能作为主采集实现。
- 业务数据、运行日志、检查结果和报表值只能由脚本或确定性工具写出，不能由 AI 文本补造。
- L3/L4 运行保留来源、处理、结果三段式证据，包括脚本版本、记录数、证据路径和退出码。
- `references/do-run-plan.md`、`references/script-design.md`、`references/ai-decision-checklist.md` 三份必备说明。
- 适用于 Windows 的可配置 Python 运行入口、样例驱动自检、结构化诊断和保守成熟度标注。

## 目录结构

```text
pdca-skill-creator/
├── README.md
├── README.zh-CN.md
├── .codex-plugin/
│   └── plugin.json
├── assets/
└── skills/
    └── pdca-skill-creator/
        ├── SKILL.md
        ├── agents/
        ├── references/
        └── scripts/
```

## 升级同步规则

发布新版本前，至少同步检查这些文件：

- `.codex-plugin/plugin.json`
- `skills/pdca-skill-creator/SKILL.md`
- `README.md`
- `README.zh-CN.md`
- 市场或发布用 `README.md`、`README.zh-CN.md`
- 结构说明文件 `docs/repository-structure.md`

更完整的升级说明和防漏改清单见 `docs/repository-structure.md`。
