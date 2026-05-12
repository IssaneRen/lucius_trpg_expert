# 20260512-1615 seed-coc-kp-sources

## Context

- 建立 CoC/KP 初步来源池，支撑后续批量导入与可信度分层。

## Inputs

- `knowledge-base/trpg/coc7e/index/`
- 官方站点与社区入口链接

## Actions

- 梳理并分层首批来源（official/community）
- 为每条来源补充 `Tier` 和 `TrustNote`
- 定义导入优先级

## Outputs

- [knowledge-base/trpg/coc7e/index/sources-seed.md](knowledge-base/trpg/coc7e/index/sources-seed.md)

## Next

- 创建 `coc7e/modules/malice-everlasting` 模组结构并补齐元数据。

## SelfReview

- 风险：社区来源稳定性与可持续性较弱，需后续回源校验。
- 验证：首批来源已按层级与可信度备注落地，可直接用于导入任务拆分。
