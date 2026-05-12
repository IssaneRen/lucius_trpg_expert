# CLAUDE / Cursor 执行说明

## 作用范围

本文件用于约束本仓库内 AI 助手运行行为，不参与应用部署。

## 运行约定

- 先读 `README.md` 与 `AGENTS.md` 再执行任务。
- 优先使用 `agents/`、`skills/`、`rules/` 中的源定义。
- 平台适配层（`.cursor/`、`.claude/`、`codex/`）由同步脚本维护。
- 知识导入统一使用 `packages/ingestion/src/cli.py`。

## 命名与落库

- 知识文档命名建议：`YYYYMMDD_HHMMSS_slug.md`
- catalog 统一维护在 `knowledge-base/index/catalog.jsonl`
- 文档 frontmatter 至少包含：`source`、`captured_at`、`namespace`、`tags`

## 质量门禁

- 新增规则/技能/agent 必须包含职责与回退策略。
- 合并前必须运行最小验证命令并确认成功。
