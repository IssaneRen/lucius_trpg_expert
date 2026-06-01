# 20260512-1620 module-folder-bootstrap

## Context

- 为 CoC7e 模组建立标准目录，并以 `Malice Everlasting` 作为首个接入样本。

## Inputs

- `knowledge-base/trpg/coc7e/modules/malice-everlasting/raw/malice-everlasting.pdf`
- `knowledge-base/trpg/coc7e/`

## Actions

- 创建 `modules/malice-everlasting` 目录骨架
- 建立 `raw/parsed/notes/index` 四层
- 写入 `index/metadata.json`；当前策略已调整为把私有 PDF 源文件复制到模块 `raw/`，避免 clone 后丢失源材料。

## Outputs

- [knowledge-base/trpg/coc7e/modules/malice-everlasting/README.md](knowledge-base/trpg/coc7e/modules/malice-everlasting/README.md)
- `knowledge-base/trpg/coc7e/modules/malice-everlasting/index/metadata.json`
- `knowledge-base/trpg/coc7e/modules/malice-everlasting/raw/.gitkeep`
- `knowledge-base/trpg/coc7e/modules/malice-everlasting/parsed/.gitkeep`
- `knowledge-base/trpg/coc7e/modules/malice-everlasting/notes/.gitkeep`

## Next

- 升级 catalog 字段，并同步 ingestion 写入逻辑。

## SelfReview

- 风险：使用绝对路径在跨机器迁移时可能失效，需要后续增加 path-mapping 机制。
- 验证：目录结构和 metadata 字段齐全，满足首个模组接入要求。
