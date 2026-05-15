---
description: "知识导入必填元数据和格式约束"
alwaysApply: true
---

# Knowledge Ingestion Rule

## 必填元数据

- `source`
- `captured_at`
- `namespace`
- `tags`

## 导入约束

1. 新增知识必须进入 `knowledge-base/<namespace>/sources/`。
2. 每次导入都要向 `knowledge-base/index/catalog.jsonl` 写入记录。
3. 对解析失败的条目需输出可追踪日志并保留重试信息。
4. 外部资料导入时，必须保留原始链接以便审计。
