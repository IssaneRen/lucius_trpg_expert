# 多平台统一使用与知识库管理优化

> 调研日期：2026-05-15
> 状态：✅ 已完成
> 负责人：Claude Code (团队调度)

---

## 背景

本项目是一个面向 TRPG 场景的多 AI 协作知识库，需要支持 Claude Code、Codex CLI、Cursor 三平台统一使用。经调研发现当前架构方向正确（SSOT + 同步分发），但存在适配缺口和索引不完整问题。

## 架构现状

```
源定义（唯一修改入口）              平台适配层（只读、自动生成）
┌─────────────┐
│ agents/     │──────────────→ .claude/agents/      (Claude Code) ✅
│ skills/     │──────────────→ .claude/skills/      (Claude Code) ✅
│ rules/      │──────────────→ .cursor/rules/       (Cursor) ⚠️ 缺 frontmatter
└─────────────┘
       ↕ scripts/sync_ai_configs.py
┌─────────────┐
│ codex/      │  ← 仅占位 README，未打通 ❌
└─────────────┘

共识入口文件：
  • AGENTS.md  → Claude Code ✓ / Codex CLI ✓ / Cursor ✓
  • CLAUDE.md  → Claude Code ✓ / Cursor ✓
```

## 知识库现状

| 指标 | 数值 |
|------|------|
| 内容 md 文件 | 9 个（排除 README） |
| 文本总量 | 564 行 / 43KB |
| 二进制资源 | 1 PDF(7.1MB) + 3 PNG(~8MB) |
| catalog 索引 | 2 条记录（覆盖率 22%） |
| 数据库 | 无（纯文件系统） |

## 核心结论

1. **三平台统一使用**：架构已就绪，Claude Code 完整可用，Cursor 基本可用，Codex 尚需补全
2. **文件系统管理知识库**：当前规模完全可靠且优于 SQL，但 catalog 索引严重不完整需修复

---

## 优化任务清单

### Task 1: 补全 catalog.jsonl 索引覆盖 [P0]

- **状态**: ✅ 已完成
- **目标**: 将 9 个内容 md 文件全部纳入 catalog.jsonl 索引
- **当前问题**: 仅 2/9 文件被索引（22% 覆盖率），AI 依赖 catalog 发现知识时会遗漏 78%
- **执行方案**:
  1. 为 parsed/ 下 5 个文件添加 frontmatter
  2. 为 kp-hooks-and-inspirations.md、sources-seed.md 补充 catalog 记录
  3. 确保所有记录字段一致（含 source_tier, trust_note）
- **验收标准**: catalog.jsonl 记录数 >= 9，字段格式统一

### Task 2: 增强同步脚本 — Cursor .mdc 适配 [P1]

- **状态**: ✅ 已完成
- **目标**: 同步时为 .cursor/rules/*.md 注入 .mdc frontmatter
- **当前问题**: Cursor 规则以纯 .md 同步，缺少 description/alwaysApply 元数据，无法使用条件触发
- **执行方案**:
  1. 在 rules/*.md 源定义中添加 YAML frontmatter（description + globs）
  2. 修改 sync 脚本，将 .md 复制为 .mdc 并保留 frontmatter
  3. 或：sync 脚本在复制时自动注入 `alwaysApply: true`
- **验收标准**: `.cursor/rules/` 下文件为 .mdc 格式，含有效 frontmatter

### Task 3: 增强同步脚本 — Codex .toml 生成 [P1]

- **状态**: ✅ 已完成
- **目标**: 将 agents/*.md 转换为 codex/ 下的可用配置
- **当前问题**: codex/ 仅有占位 README，三平台"统一使用"在 Codex 端未打通
- **执行方案**:
  1. 解析 agents/*.md 中的 `# Agent: name` + `## 职责` + 正文
  2. 生成 `codex/agents/*.toml` 格式：name/description/developer_instructions
  3. 同步 rules → codex/instructions.md（Codex 可读取的项目指令格式）
- **验收标准**: `codex/` 下有实际 agent 配置文件，Codex CLI 可发现并使用

### Task 4: 添加 pre-commit hook [P2]

- **状态**: ✅ 已完成
- **目标**: 提交时自动执行同步脚本，消除手动遗忘的漂移风险
- **当前问题**: 同步完全依赖手动运行 `python3 scripts/sync_ai_configs.py`，无任何自动化保障
- **执行方案**:
  1. 创建 `.git/hooks/pre-commit` 执行同步脚本
  2. 同步后 `git diff --exit-code` 检测是否有新变更
  3. 如有变更则自动 stage 并提示用户
  4. 或使用 `.husky/` 方式（如果未来引入 package.json）
- **验收标准**: 修改 agents/skills/rules 后提交时，适配层自动更新

### Task 5: 实现 ingest:pdf 基础功能 [P3]

- **状态**: ✅ 已完成
- **目标**: 让 PDF 模组能自动化入库（文本提取 → markdown → catalog 索引）
- **当前问题**: cli.py 中 ingest:pdf 仅为 TODO 占位，7.1MB 核心 PDF 内容无法自动化处理
- **执行方案**:
  1. 使用 pymupdf/pdfplumber 提取 PDF 文本
  2. 按页/章节切分为 markdown 文件
  3. 生成 frontmatter 并追加 catalog.jsonl
  4. 输出到 `{namespace}/sources/pdf/` 或 `modules/{name}/parsed/`
- **验收标准**: `python cli.py ingest:pdf --file xxx.pdf --namespace trpg/coc7e` 可正常执行

---

## 进度日志

| 日期 | 事件 | 备注 |
|------|------|------|
| 2026-05-15 | 调研完成，报告落地 | 经 2 轮专家评审修正 |
| 2026-05-15 | 5 项任务并行执行完成 | 子 agent 执行 + 主调度整合 |
| 2026-05-15 | 专家评审通过 | CC专家88分/Codex专家82分 |
| 2026-05-15 | 修复专家指出的缺陷 | TOML转义+AGENTS.md frontmatter剥离 |
| 2026-05-15 | 全部完成 | sync脚本验证通过，三平台产物正确 |

---

## 断点续传指引

如果后续需要继续推进：
1. 检查本文件中各 Task 的状态标记（⬜/🔄/✅/❌）
2. 未完成的任务可直接从「执行方案」步骤继续
3. 每个 Task 完成后更新状态和进度日志
4. 所有 Task 完成后将顶部状态改为 ✅ 已完成
