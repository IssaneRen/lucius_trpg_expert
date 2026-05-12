# Contributing

## 分支与提交

- 建议使用 Conventional Commits，例如：`feat: add web ingestion scaffold`
- 提交前执行最小验证命令并确保通过

## 基本流程

1. 在 `agents/skills/rules` 修改源定义
2. 执行 `python3 scripts/sync_ai_configs.py`
3. 执行 ingest 或索引相关验证命令
4. 更新文档并提交
