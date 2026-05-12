# TRPG Query Routing Skill

## 适用场景

- 用户提出 TRPG 规则问答
- 需要在多规则体系间路由查询

## 路由策略

1. 根据关键词识别规则域（dnd5e/coc7e/pf2e）。
2. 未命中时回退到 `general` 命名空间。
3. 命中多个规则时输出候选并请求澄清。

## 输出格式

- `target_namespace`
- `confidence`
- `reason`
- `next_action`

## 回退策略

- 无法判断时，默认 `general` 并显式说明不确定性。
