# Knowledge Ingest Skill

## 适用场景

- 用户要求新增知识条目
- 需要从 web/pdf/media 导入资料

## 输入

- `source_type`: web/pdf/media
- `source`: url 或本地路径
- `namespace`: 知识命名空间
- `tags`: 标签列表

## 输出

- `markdown_path`: 导入后的 markdown 路径
- `catalog_record_id`: catalog 记录 ID
- `status`: success/failed

## 执行流程

1. 校验参数完整性与 namespace 合法性。
2. 调用 `packages/ingestion/src/cli.py` 对应命令。
3. 校验输出文件与 catalog 记录是否存在。
4. 返回结构化结果与后续建议。

## 失败回退

- 解析失败时，返回原始 source 与失败原因。
- 建议用户切换导入方式或重试。
