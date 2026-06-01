# 原初之境 Agent 调度记录

source: knowledge-base/trpg/coc7e/modules/the-primal-state/raw/the-primal-state-zh-TW.pdf
namespace: trpg/coc7e
tags: module, coc7e, the-primal-state, pdf, zh-TW
started_at: 2026-05-31

## 状态

- knowledge-ingest: `ingest:pdf` 已调用，当前项目实现为 TODO，占位日志确认未解析 PDF。
- PDF toolchain: PyMuPDF/pypdf/pdfplumber 不存在；pip 安装受 PyPI SSL 错误阻断；已改用本机 Git 自带 Poppler `pdftotext.exe`。
- PDF extraction: `pdftotext -layout -enc UTF-8` 已生成全文文本。
- page split: 已按 form-feed 分割为 142 个页文件。

## 产物

- raw text: `knowledge-base/trpg/coc7e/modules/the-primal-state/raw/full-layout.txt`
- raw PDF: `knowledge-base/trpg/coc7e/modules/the-primal-state/raw/the-primal-state-zh-TW.pdf`
- supporting PDF: `knowledge-base/trpg/coc7e/modules/the-primal-state/raw/down-the-rabbit-hole-zh-TW.pdf`
- pages: `knowledge-base/trpg/coc7e/modules/the-primal-state/parsed/pages/page-*.txt`

## Agent 分工

- toolchain-agent `019e7eac-13a4-72d1-8ada-a683ba4f2397`: 完成 PDF 工具链调研，建议 PyMuPDF 首选，当前用 Poppler 作为 fallback。
