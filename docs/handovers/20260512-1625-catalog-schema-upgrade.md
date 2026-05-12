# 20260512-1625 catalog-schema-upgrade

## Context

- 为 CoC/KP 来源分层落地扩展 catalog 字段，支持 `source_tier` 与 `trust_note`。

## Inputs

- `packages/ingestion/src/cli.py`
- `knowledge-base/index/catalog.jsonl`

## Actions

- 扩展 `_append_catalog` 入参与 record 字段
- 扩展 `ingest:web` 参数：`--source-tier`、`--trust-note`
- 更新 `ingest_web` 写入逻辑，确保字段随导入链路落库

## Outputs

- `packages/ingestion/src/cli.py`
- [docs/handovers/20260512-1625-catalog-schema-upgrade.md](docs/handovers/20260512-1625-catalog-schema-upgrade.md)

## Next

- 定义固定自审清单并将其纳入每条 step 交接流程。

## SelfReview

- 风险：历史 catalog 旧记录缺少新字段，需要后续补齐或兼容读取。
- 验证：CLI 参数与写库逻辑已同步更新，满足新字段落库要求。
