# Self Review Checklist

每个 step 收尾必须执行以下自审，并把结论写入 step 文档的 `SelfReview`。

## 1) 结构审查

- 新增路径是否符合既定层级（规则域/模组域/通用域）
- 是否避免把临时文件放入长期目录

## 2) 数据审查

- catalog 是否新增可追踪记录
- 必填元数据是否齐全：`source` `captured_at` `namespace` `tags`
- 新字段是否一致：`source_tier` `trust_note`

## 3) 可接手审查

- 下一个执行者是否可以只看 `INDEX.md + 本 step 文档` 就继续
- `Next` 是否给出可执行动作而非抽象描述

## 4) 命令审查

- 本 step 涉及命令是否可复现
- 关键命令是否在文档中可复制使用

## 5) 风险审查

- 至少记录 1 条残余风险
- 至少记录 1 条已完成验证结果
