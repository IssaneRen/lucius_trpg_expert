#!/usr/bin/env python3
"""知识导入 CLI。

当前实现：
- ingest:web   最小可运行链路（抓取网页文本 -> markdown -> catalog）
- ingest:pdf   PDF 文本提取 -> markdown -> catalog
- ingest:media 占位命令
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import re
import shutil
import subprocess
import urllib.request
from pathlib import Path
from typing import Iterable


logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOGGER = logging.getLogger("ingestion_cli")
ROOT = Path(__file__).resolve().parents[3]

# PDF 文本最大字符数，超出截断
PDF_MAX_CHARS = 50000


def _slugify(text: str) -> str:
    """将任意文本转换为可用于文件名的 slug。"""
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return normalized or "untitled"


def _strip_html(html: str) -> str:
    """以轻量方式剥离 HTML 标签，得到可读纯文本。

    说明：
    - 这是最小可运行实现，不追求复杂网页的高保真抽取。
    - 后续可替换为更稳定的正文抽取算法。
    """
    no_script = re.sub(r"<(script|style)[^>]*>.*?</\\1>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", no_script)
    text = re.sub(r"\\s+", " ", text).strip()
    return text


def _write_markdown(namespace: str, url: str, tags: Iterable[str], text: str) -> Path:
    """将抓取文本写入标准化 markdown 文档并返回路径。"""
    captured_at = dt.datetime.now(dt.timezone.utc)
    timestamp = captured_at.strftime("%Y%m%d_%H%M%S")
    slug = _slugify(url.split("/")[-1] or "web")
    target_dir = ROOT / "knowledge-base" / namespace / "sources" / "web"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{timestamp}_{slug}.md"
    body = text[:8000] if text else "(empty content)"
    target.write_text(
        (
            "---\n"
            f"source: {url}\n"
            f"captured_at: {captured_at.isoformat()}\n"
            f"namespace: {namespace}\n"
            f"tags: [{', '.join(tags)}]\n"
            "---\n\n"
            "# Web Ingestion Result\n\n"
            f"{body}\n"
        ),
        encoding="utf-8",
    )
    LOGGER.info("ingest_web: markdown_written path=%s", target.as_posix())
    return target


def _append_catalog(
    namespace: str,
    url: str,
    tags: Iterable[str],
    markdown_path: Path,
    source_tier: str,
    trust_note: str,
) -> None:
    """向全局 catalog 追加一条 JSONL 记录。

    参数说明：
    - source_tier: 来源级别（official/community/private/internal）
    - trust_note: 可信度备注，便于后续审查和过滤
    """
    record = {
        "id": markdown_path.stem,
        "namespace": namespace,
        "source": url,
        "tags": list(tags),
        "source_tier": source_tier,
        "trust_note": trust_note,
        "path": markdown_path.as_posix(),
        "ingested_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    catalog = ROOT / "knowledge-base" / "index" / "catalog.jsonl"
    catalog.parent.mkdir(parents=True, exist_ok=True)
    with catalog.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    LOGGER.info("ingest_web: catalog_appended id=%s", record["id"])


def ingest_web(
    url: str,
    namespace: str,
    tags: list[str],
    source_tier: str,
    trust_note: str,
) -> None:
    """执行 web 导入链路。

    该方法会将来源级别和可信度备注同时写入 catalog，便于后续自动筛选。
    """
    LOGGER.info(
        "ingest_web: start url=%s namespace=%s source_tier=%s",
        url,
        namespace,
        source_tier,
    )
    request = urllib.request.Request(url, headers={"User-Agent": "lucius-ingestion/0.1"})
    with urllib.request.urlopen(request, timeout=15) as response:
        html = response.read().decode("utf-8", errors="ignore")
    text = _strip_html(html)
    md_path = _write_markdown(namespace=namespace, url=url, tags=tags, text=text)
    _append_catalog(
        namespace=namespace,
        url=url,
        tags=tags,
        markdown_path=md_path,
        source_tier=source_tier,
        trust_note=trust_note,
    )
    LOGGER.info("ingest_web: done")


# ---------------------------------------------------------------------------
# PDF ingestion
# ---------------------------------------------------------------------------


def _extract_pdf_text_pymupdf(file_path: Path) -> list[str]:
    """使用 pymupdf (fitz) 逐页提取 PDF 文本。

    返回每页文本的列表。如果 pymupdf 不可用则抛出 ImportError。
    """
    import fitz  # type: ignore[import-untyped]  # pymupdf

    pages: list[str] = []
    with fitz.open(str(file_path)) as doc:
        for page in doc:
            pages.append(page.get_text())
    return pages


def _extract_pdf_text_pdftotext(file_path: Path) -> list[str]:
    """使用系统 pdftotext 命令逐页提取 PDF 文本。

    依赖 poppler（macOS: brew install poppler）。
    返回每页文本的列表。如果 pdftotext 不可用则抛出 FileNotFoundError。
    """
    pdftotext_bin = shutil.which("pdftotext")
    if not pdftotext_bin:
        raise FileNotFoundError("pdftotext not found in PATH")

    # pdftotext -layout 保持原始排版，输出到 stdout
    result = subprocess.run(
        [pdftotext_bin, "-layout", str(file_path), "-"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdftotext failed: {result.stderr.strip()}")

    # pdftotext 用 form-feed (\x0c) 分隔页面
    raw_pages = result.stdout.split("\x0c")
    # 最后一个元素通常是空字符串
    pages = [p for p in raw_pages if p.strip()]
    return pages


def _extract_pdf_text(file_path: Path) -> list[str]:
    """提取 PDF 文本，优先使用 pymupdf，fallback 到 pdftotext。

    如果两者都不可用，抛出 RuntimeError 附带安装提示。
    """
    # 尝试 pymupdf
    try:
        return _extract_pdf_text_pymupdf(file_path)
    except ImportError:
        LOGGER.info("ingest_pdf: pymupdf not available, trying pdftotext fallback")
    except Exception as e:
        LOGGER.warning("ingest_pdf: pymupdf extraction failed (%s), trying pdftotext", e)

    # 尝试 pdftotext
    try:
        return _extract_pdf_text_pdftotext(file_path)
    except FileNotFoundError:
        pass
    except Exception as e:
        raise RuntimeError(f"pdftotext extraction failed: {e}") from e

    # 两者都不可用
    raise RuntimeError(
        "PDF 文本提取失败：pymupdf 和 pdftotext 均不可用。\n"
        "请安装其中之一：\n"
        "  pip install pymupdf        # 推荐\n"
        "  brew install poppler       # macOS, 提供 pdftotext 命令"
    )


def _write_pdf_markdown(
    namespace: str,
    source: str,
    tags: Iterable[str],
    pages: list[str],
    slug: str,
    source_tier: str,
    trust_note: str,
) -> Path:
    """将 PDF 提取文本写入标准化 markdown 文档并返回路径。"""
    captured_at = dt.datetime.now(dt.timezone.utc)
    timestamp = captured_at.strftime("%Y%m%d_%H%M%S")
    target_dir = ROOT / "knowledge-base" / namespace / "sources" / "pdf"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{timestamp}_{slug}.md"

    # 构建正文：逐页用 ## Page N 分隔
    body_parts: list[str] = []
    total_chars = 0
    truncated = False
    for i, page_text in enumerate(pages, start=1):
        header = f"## Page {i}\n\n"
        content = page_text.strip() + "\n"
        if total_chars + len(header) + len(content) > PDF_MAX_CHARS:
            body_parts.append(header)
            remaining = PDF_MAX_CHARS - total_chars - len(header)
            if remaining > 0:
                body_parts.append(content[:remaining])
            body_parts.append("\n\n[truncated]\n")
            truncated = True
            break
        body_parts.append(header)
        body_parts.append(content)
        total_chars += len(header) + len(content)

    body = "".join(body_parts)

    frontmatter = (
        "---\n"
        f"source: {source}\n"
        f"captured_at: {captured_at.isoformat()}\n"
        f"namespace: {namespace}\n"
        f"tags: [{', '.join(tags)}]\n"
        f"source_tier: {source_tier}\n"
        f"trust_note: {trust_note}\n"
        f"total_pages: {len(pages)}\n"
        f"truncated: {str(truncated).lower()}\n"
        "---\n\n"
        "# PDF Ingestion Result\n\n"
    )

    target.write_text(frontmatter + body, encoding="utf-8")
    LOGGER.info("ingest_pdf: markdown_written path=%s", target.as_posix())
    return target


def ingest_pdf(
    file_path: str,
    namespace: str,
    tags: list[str],
    source_tier: str,
    trust_note: str,
) -> None:
    """执行 PDF 导入链路。

    流程：PDF 路径校验 -> 文本提取 -> markdown 生成 -> catalog 追加。
    """
    pdf_path = Path(file_path).resolve()

    # 路径校验
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    if not pdf_path.is_file():
        raise ValueError(f"Path is not a file: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        LOGGER.warning("ingest_pdf: file does not have .pdf extension: %s", pdf_path.name)

    LOGGER.info(
        "ingest_pdf: start file=%s namespace=%s source_tier=%s",
        pdf_path,
        namespace,
        source_tier,
    )

    # 从文件名派生 slug（去掉 .pdf 后缀，转 kebab-case）
    slug = _slugify(pdf_path.stem)

    # 提取文本
    pages = _extract_pdf_text(pdf_path)
    if not pages:
        LOGGER.warning("ingest_pdf: no text extracted from PDF")
        pages = ["(no extractable text)"]

    LOGGER.info("ingest_pdf: extracted %d pages", len(pages))

    # 写入 markdown
    source = f"file://{pdf_path}"
    md_path = _write_pdf_markdown(
        namespace=namespace,
        source=source,
        tags=tags,
        pages=pages,
        slug=slug,
        source_tier=source_tier,
        trust_note=trust_note,
    )

    # 追加 catalog
    _append_catalog(
        namespace=namespace,
        url=source,
        tags=tags,
        markdown_path=md_path,
        source_tier=source_tier,
        trust_note=trust_note,
    )
    LOGGER.info("ingest_pdf: done")


def ingest_media(_path: str, _namespace: str) -> None:
    """多媒体导入占位实现。"""
    LOGGER.info("ingest_media: TODO 预留接口，后续接入 ASR/OCR 等流程")


def build_parser() -> argparse.ArgumentParser:
    """构建 CLI 参数解析器。"""
    parser = argparse.ArgumentParser(description="knowledge ingestion cli")
    sub = parser.add_subparsers(dest="command", required=True)

    web = sub.add_parser("ingest:web", help="ingest from web url")
    web.add_argument("--url", required=True)
    web.add_argument("--namespace", default="general")
    web.add_argument("--tags", default="web")
    web.add_argument("--source-tier", default="official")
    web.add_argument("--trust-note", default="seed source")

    pdf = sub.add_parser("ingest:pdf", help="ingest text from PDF file")
    pdf.add_argument("--file", required=True, help="path to the PDF file")
    pdf.add_argument("--namespace", default="general", help="knowledge namespace")
    pdf.add_argument("--tags", default="pdf", help="comma-separated tags")
    pdf.add_argument("--source-tier", default="private-pdf", help="source tier level")
    pdf.add_argument("--trust-note", default="pdf import", help="trust/provenance note")

    media = sub.add_parser("ingest:media", help="placeholder for media ingestion")
    media.add_argument("--path", required=True)
    media.add_argument("--namespace", default="general")
    return parser


def main() -> None:
    """CLI 入口函数。"""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "ingest:web":
        tags = [x.strip() for x in args.tags.split(",") if x.strip()]
        ingest_web(
            url=args.url,
            namespace=args.namespace,
            tags=tags,
            source_tier=args.source_tier,
            trust_note=args.trust_note,
        )
    elif args.command == "ingest:pdf":
        tags = [x.strip() for x in args.tags.split(",") if x.strip()]
        ingest_pdf(
            file_path=args.file,
            namespace=args.namespace,
            tags=tags,
            source_tier=args.source_tier,
            trust_note=args.trust_note,
        )
    elif args.command == "ingest:media":
        ingest_media(_path=args.path, _namespace=args.namespace)


if __name__ == "__main__":
    main()
