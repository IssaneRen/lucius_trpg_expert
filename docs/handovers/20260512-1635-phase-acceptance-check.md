# 20260512-1635 phase-acceptance-check

## Context

- 按第二阶段验收标准做最终检查，并明确缺口。

## Inputs

- `docs/handovers/INDEX.md`
- `knowledge-base/trpg/coc7e/index/sources-seed.md`
- `knowledge-base/trpg/coc7e/modules/malice-everlasting/index/metadata.json`
- `packages/ingestion/src/cli.py`

## Actions

- 执行 `sync_ai_configs.py`
- 实跑 `ingest:web` 导入 CoC 官方来源
- 编译检查 Python 脚本
- 检查 catalog 新字段落库

## Outputs

- `knowledge-base/trpg/coc7e/sources/web/20260512_081228_call-of-cthulhu-resources.md`
- `knowledge-base/index/catalog.jsonl`（新增含 `source_tier` 和 `trust_note` 记录）
- `docs/handovers/20260512-1635-phase-acceptance-check.md`

## Next

- 增加 `catalog` 历史数据迁移脚本，补齐旧记录新字段。
- 增加 `source_path` 迁移映射机制，提升跨机器可移植性。

## SelfReview

- 风险：旧 catalog 记录仍可能缺少 `source_tier/trust_note`。
- 风险：`malice-everlasting` 当前使用绝对路径引用 PDF，跨设备迁移需映射。
- 验证：验收四项均已完成，且导入链路实跑成功。
