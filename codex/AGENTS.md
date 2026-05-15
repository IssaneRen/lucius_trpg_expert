# Project Rules (Auto-generated)

本文件由 `scripts/sync_ai_configs.py` 自动生成，汇总 `rules/` 目录中的项目规则。
请勿手动编辑，源文件位于 `rules/` 目录。


---

# Agent Collaboration Rule

## 协作流程

1. 先路由：判断请求属于 researcher/indexer/responder 哪类职责。
2. 再检索：优先知识库，必要时补充外部来源。
3. 再执行：严格按技能契约产出结构化结果。
4. 最后沉淀：可复用结论写入知识库或对话沉淀目录。

## 质量要求

- 结论必须可追踪到来源。
- 任务失败时需提供下一步可执行建议。
- 多 agent 输出冲突时，以规则与证据优先。


---

# Knowledge Ingestion Rule

## 必填元数据

- `source`
- `captured_at`
- `namespace`
- `tags`

## 导入约束

1. 新增知识必须进入 `knowledge-base/<namespace>/sources/`。
2. 每次导入都要向 `knowledge-base/index/catalog.jsonl` 写入记录。
3. 对解析失败的条目需输出可追踪日志并保留重试信息。
4. 外部资料导入时，必须保留原始链接以便审计。


---

# Repository Structure Rule

## 目标

保证仓库层次稳定、便于多端拆分和多 AI 协作。

## 规则

1. `apps/` 仅放可独立部署应用，不放共享逻辑。
2. `packages/` 仅放共享能力，禁止耦合具体应用配置。
3. `knowledge-base/` 中内容必须按命名空间归档。
4. `agents/`、`skills/`、`rules/` 是协作源定义，禁止在适配层直接改。
5. 平台目录（`.cursor/`、`.claude/`、`codex/`）由同步脚本维护。
