# lucius_trpg_expert

一个面向 TRPG 场景的多 AI 协作知识库仓库，支持 Cursor、Claude Code、Codex 与后续工具共同迭代。

## 仓库目标

- 统一管理多规则 TRPG 知识与通用知识索引。
- 提供可扩展的知识导入能力（web/pdf/media）。
- 让多 AI 工具共享一套 agents/skills/rules 源定义，避免配置漂移。
- 为未来 `apps/` 子项目（web/mobile/miniapp）提供隔离部署边界。

## 目录概览

- `knowledge-base/`: 知识内容、来源与索引
- `agents/`: 平台无关 agent 定义（SSOT）
- `skills/`: 平台无关 skill 定义（SSOT）
- `rules/`: 可执行协作规则（SSOT）
- `.cursor/`, `.claude/`, `codex/`: 各 AI 工具适配层
- `packages/`: 共享能力（ingestion/index/retrieval/tooling）
- `apps/`: 业务应用子项目（未来拆分部署）
- `scripts/`: 自动化脚本（配置同步、检查）
- `docs/`: 设计文档、架构与路线图

## 多 AI 协作流程

1. 在 `agents/`、`skills/`、`rules/` 更新源定义。
2. 执行 `scripts/sync_ai_configs.py` 同步到平台适配目录。
3. 在各 AI 工具中执行同一套规范与上下文。

## 快速开始

```bash
python3 packages/ingestion/src/cli.py ingest:web --url "https://example.com" --namespace general --tags demo,web
python3 scripts/sync_ai_configs.py
```

## 后续路线

- `ingest:pdf` 与 `ingest:media` 实现真实解析链路
- 引入向量索引与检索增强
- 对话质量评估与自我迭代机制
