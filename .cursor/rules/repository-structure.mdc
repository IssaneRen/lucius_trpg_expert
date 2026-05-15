---
description: "仓库目录层次规则和修改权限约束"
alwaysApply: true
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
