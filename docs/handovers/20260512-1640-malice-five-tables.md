# 20260512-1640 malice-five-tables

## Context

- 按“方方正正、便于编辑”的要求，将 `malice-everlasting` 关系总结落地为五张 Markdown 表。

## Inputs

- `../lucius_relationships/public/default-worlds/coc-eternal-malice.json`
- `knowledge-base/trpg/coc7e/modules/malice-everlasting/index/metadata.json`

## Actions

- 基于参考 JSON 生成五张结构化表：contacts / relationships / events / event-participants / tags
- 统一字段主键与关系方向
- 为每行补充 `evidence` 和 `confidence`
- 更新模块 README，增加五表入口与编辑规范
- 运行一致性自检：引用 ID、事件关联、证据和置信度字段完整性

## Outputs

- [knowledge-base/trpg/coc7e/modules/malice-everlasting/parsed/contacts.md](knowledge-base/trpg/coc7e/modules/malice-everlasting/parsed/contacts.md)
- [knowledge-base/trpg/coc7e/modules/malice-everlasting/parsed/relationships.md](knowledge-base/trpg/coc7e/modules/malice-everlasting/parsed/relationships.md)
- [knowledge-base/trpg/coc7e/modules/malice-everlasting/parsed/events.md](knowledge-base/trpg/coc7e/modules/malice-everlasting/parsed/events.md)
- [knowledge-base/trpg/coc7e/modules/malice-everlasting/parsed/event-participants.md](knowledge-base/trpg/coc7e/modules/malice-everlasting/parsed/event-participants.md)
- [knowledge-base/trpg/coc7e/modules/malice-everlasting/parsed/tags.md](knowledge-base/trpg/coc7e/modules/malice-everlasting/parsed/tags.md)
- [knowledge-base/trpg/coc7e/modules/malice-everlasting/README.md](knowledge-base/trpg/coc7e/modules/malice-everlasting/README.md)

## Next

- 基于五表继续补充 `notes/` 的章节级证据摘要（按页码与场景拆分）。
- 后续可直接将五表映射到可视化平台的数据导入层。

## SelfReview

- 风险：当前 `evidence` 主要指向结构化参考 JSON，尚未逐条挂载 PDF 页码证据。
- 验证：一致性检查通过（contacts=34, events=18, relationships=34, participants=50, tags=34）。
