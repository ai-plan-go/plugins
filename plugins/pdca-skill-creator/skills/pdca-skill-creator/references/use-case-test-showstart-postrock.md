# ShowStart Post-Rock Plugin Use Case

## 用例目标

验证 `pdca-skill-creator` 生成的爬虫/分类/插件型 PDCA 技能，是否能覆盖安装、运行、字段提取、业务分类、网络诊断、dry-run 同步和交付清洁。

## 用户需求摘要

- 爬取秀动演出信息。
- 第一轮只提取演出名字和艺人。
- 先筛选摇滚演出，再结合艺人和详情页证据识别是否为后摇演出。
- 命中后摇后生成待同步后台清单；后台未配置时不得真实上架。
- 图片只在最终同步后台阶段抓取。
- 交付为 Codex 可安装插件目录。
- 支持人工触发和定时入口。

## 样例验收

样例详情页：

```text
https://www.showstart.com/event/302861
```

期望结果：

| 字段 | 期望 |
|---|---|
| 演出名 | `【云南后摇新锐】 一便士草莓地 新专辑《Wasteland Music》专场` |
| 艺人 | `一便士草莓地` |
| 风格证据 | 页面或外部证据包含 `后摇` 或 `post-rock` |
| 分类结果 | 进入后摇候选 |
| 同步行为 | 后台未配置时只生成 dry-run `sync_plan` |

如果网络或权限阻止访问，不得伪造上述字段，必须输出 `network_permission_denied`、`timeout`、`http_error`、`captcha_or_login`、`selector_miss` 或等价诊断，并给出复跑建议。

## 必须检查

- 插件根目录包含 `.codex-plugin/plugin.json`、`skills/` 和 `skills/{SKILL_NAME}/SKILL.md`。
- 文档包含安装、重装、源码修正后同步已安装缓存和安装后结构检查说明。
- `run_daily_check.ps1` 支持可配置 Python 路径，不能只写裸 `python`。
- `scripts/smoke_test.py` 或 `scripts/run_business_use_case_test.py` 包含样例期望结果校验，不只检查产物文件存在。
- `references/business-use-case-profile.json` 记录样例 URL、期望字段、期望分类、dry-run 同步约束和失败诊断要求。
- 成品目录不包含 `__pycache__/`、`*.pyc`、`work_smoke/`、`tmp_smoke/` 或业务测试报告残留。

## 通过标准

- 创建器用例评分不低于 85。
- 无 P0/P1。
- 若真实访问样例页，能提取期望演出名和艺人，并识别为后摇候选。
- 若访问失败，必须输出明确网络/权限/页面诊断，且当前成熟度不得高于 L3 可执行脚手架。
