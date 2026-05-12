#!/usr/bin/env python3
"""知识导入 CLI。

当前实现：
- ingest:web   最小可运行链路（抓取网页文本 -> markdown -> catalog）
- ingest:pdf   占位命令
- ingest:media 占位命令
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import re
import urllib.request
from pathlib import Path
from typing import Iterable


logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOGGER = logging.getLogger("ingestion_cli")
ROOT = Path(__file__).resolve().parents[3]


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


def _append_catalog(namespace: str, url: str, tags: Iterable[str], markdown_path: Path) -> None:
    """向全局 catalog 追加一条 JSONL 记录。"""
    record = {
        "id": markdown_path.stem,
        "namespace": namespace,
        "source": url,
        "tags": list(tags),
        "path": markdown_path.as_posix(),
        "ingested_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    catalog = ROOT / "knowledge-base" / "index" / "catalog.jsonl"
    catalog.parent.mkdir(parents=True, exist_ok=True)
    with catalog.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    LOGGER.info("ingest_web: catalog_appended id=%s", record["id"])


def ingest_web(url: str, namespace: str, tags: list[str]) -> None:
    """执行 web 导入链路。"""
    LOGGER.info("ingest_web: start url=%s namespace=%s", url, namespace)
    request = urllib.request.Request(url, headers={"User-Agent": "lucius-ingestion/0.1"})
    with urllib.request.urlopen(request, timeout=15) as response:
        html = response.read().decode("utf-8", errors="ignore")
    text = _strip_html(html)
    md_path = _write_markdown(namespace=namespace, url=url, tags=tags, text=text)
    _append_catalog(namespace=namespace, url=url, tags=tags, markdown_path=md_path)
    LOGGER.info("ingest_web: done")


def ingest_pdf(_path: str, _namespace: str) -> None:
    """PDF 导入占位实现。"""
    LOGGER.info("ingest_pdf: TODO 预留接口，后续接入真实 PDF 解析流程")


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

    pdf = sub.add_parser("ingest:pdf", help="placeholder for pdf ingestion")
    pdf.add_argument("--path", required=True)
    pdf.add_argument("--namespace", default="general")

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
        ingest_web(url=args.url, namespace=args.namespace, tags=tags)
    elif args.command == "ingest:pdf":
        ingest_pdf(_path=args.path, _namespace=args.namespace)
    elif args.command == "ingest:media":
        ingest_media(_path=args.path, _namespace=args.namespace)


if __name__ == "__main__":
    main()
