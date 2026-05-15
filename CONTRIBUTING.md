# Contributing

## 分支与提交

- 建议使用 Conventional Commits，例如：`feat: add web ingestion scaffold`
- 提交前执行最小验证命令并确保通过

## Git Hooks 安装

首次克隆仓库后，运行以下命令安装 pre-commit hook：

```bash
bash scripts/install-hooks.sh
```

安装后，当你提交 `agents/`、`skills/`、`rules/` 中的变更时，hook 会自动执行 AI 配置同步并 stage 产物，无需手动运行同步脚本。

## 基本流程

1. 在 `agents/skills/rules` 修改源定义
2. 提交代码（pre-commit hook 自动执行同步）
3. 执行 ingest 或索引相关验证命令
4. 更新文档并提交

> **备注**：若未安装 hook，也可手动执行 `python3 scripts/sync_ai_configs.py` 完成同步。
