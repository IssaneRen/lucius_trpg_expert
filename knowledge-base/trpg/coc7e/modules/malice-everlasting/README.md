# Malice Everlasting Module

首个 CoC 模组目录，按 `规则体系 -> 模组` 组织。

- `raw/`: 原始文件引用或受控副本
- `parsed/`: 解析后的结构化文本
- `notes/`: KP 运行手记
- `index/metadata.json`: 模组元数据与追踪信息

## 五表入口（便于编辑）

- [parsed/contacts.md](parsed/contacts.md)
- [parsed/relationships.md](parsed/relationships.md)
- [parsed/events.md](parsed/events.md)
- [parsed/event-participants.md](parsed/event-participants.md)
- [parsed/tags.md](parsed/tags.md)

## 编辑规范

- 主键字段固定：`contact_id`、`relationship_id`、`event_id`、`participant_id`、`tag_id`。
- 关系方向固定：`source_contact_id -> target_contact_id`，不可反向混用。
- 每一行必须包含 `evidence` 与 `confidence`，便于后续回溯与审查。
- 修改表数据后，优先在 `notes/` 增加变更说明，记录原因与影响范围。
