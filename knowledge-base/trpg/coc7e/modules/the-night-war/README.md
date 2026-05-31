# The Night War (夜战)

作者：Kevin A. Ross
收录于：Tales of the Miskatonic Valley（密斯卡托尼克流域新传）第6章

## 模组概述

一战西线战场，1918年。调查员们以美国远征军士兵的身份，在法国前线的战壕中经历一场超乎寻常的夜间战斗。本模组与《永恒恶意》(Malice Everlasting) 存在剧情关联。

## 核心特征

- **时代**：1918年一战 / 1928年阿卡姆（框架时间线）
- **风格**：高烈度军事战斗 + 克苏鲁恐怖
- **武器系统**：M1917步枪(.30-06)、.45手枪、手雷、刺刀、迫击炮/火炮
- **特殊技能需求**：炮术(Artillery)、军事科学、急救
- **玩家人数**：2-6人
- **预计时长**：1-2场

## 目录结构

- `raw/`: 原始 PDF
- `parsed/`: 解析后的结构化文本
- `notes/`: KP 运行手记
- `index/metadata.json`: 模组元数据

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

## 与《永恒恶意》的关联

本模组可作为《永恒恶意》的前置或后续体验。跑过《永恒恶意》的调查员可能会发现两个模组之间存在令人不安的联系。

## KP 注意事项

- 本模组战斗烈度极高，建议使用预设士兵角色卡或让玩家按军事背景建卡
- 模组提供了详细的随机事件表和NPC士兵数据表
- 炮击规则和毒气规则需要KP提前熟悉
