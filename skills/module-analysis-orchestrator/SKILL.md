---
name: module-analysis-orchestrator
description: Use when coordinating multi-agent TRPG module/PDF analysis where the main agent should only orchestrate extraction, dispatch parser agents, track progress, run expert reviews after each segment, handle continuation after context compaction, and produce a final concise module architecture.
---

# Module Analysis Orchestrator

Use this skill when the user asks for a TRPG module/PDF to be analyzed by multiple agents and explicitly wants the main agent to manage only coordination, context compression, progress records, retries, expert review, and final synthesis.

## Role Boundary

The main agent is the coordinator.

- Do not personally perform full segment analysis when subagents are available.
- Do maintain task state, source paths, segment ownership, review status, blockers, and final synthesis.
- Do inspect enough raw material to verify extraction quality and integrate results.
- If a subagent stalls or fails, dispatch a replacement with the same segment and the latest state.
- Do not ask the user mid-run unless the source file is inaccessible and no reasonable recovery path exists.

## Required Skills To Combine

- `knowledge-ingest`: source validation, namespace/tags, catalog entry, traceability.
- `trpg-document-reader`: PDF/text extraction, page preservation, OCR/tool fallback.
- `module-clue-analyst`: segment-level nodes, clues, revelations, dependencies, NPCs, locations, timeline.
- `team-leader-work`: multi-agent dispatch and expert review pattern.

## Workflow

### 1. Intake

Capture:

- `source_type`: normally `pdf`
- `source`: original local path or URL
- `namespace`: usually `trpg/coc7e`, `trpg/dnd5e`, `trpg/pf2e`, or `general`
- `tags`: module name, system, language, source type
- `captured_at`: current date/time

Create a dispatch log under:

```text
docs/reports/<module-slug>/agent-dispatch-log.md
```

The log must include source, namespace, tags, current phase, agents, segment IDs, review status, retry status, and output paths.

### 2. Ingest And Extraction

First call the project ingestion entrypoint if present.

```text
packages/ingestion/src/cli.py ingest:pdf --path <source> --namespace <namespace>
```

If it is TODO, missing, or insufficient:

- Record that failure in the dispatch log.
- Continue with local PDF extraction tooling.
- Preserve page boundaries.
- Write raw and page-level outputs under:

```text
knowledge-base/<namespace>/modules/<module-slug>/raw/
knowledge-base/<namespace>/modules/<module-slug>/parsed/pages/
```

Preferred fallback order:

1. PyMuPDF (`fitz`) for page text, TOC, blocks, images.
2. `pdftotext -layout -enc UTF-8` if available.
3. OCR only for pages with little/no text and many images.

On Windows, avoid hardcoding CJK paths through non-UTF-8 shell literals. Prefer discovering paths from the filesystem and passing them as `Path` objects. When writing JSON, use UTF-8 and `ensure_ascii=False`.

### 3. Segment Plan

Split by TOC or page ranges into chunks:

```text
knowledge-base/<namespace>/modules/<module-slug>/parsed/chunks/<segment-id>.md
```

Each chunk must include:

- segment title
- source page range
- original `PDF_PAGE_FILE` markers
- extracted text

Track every segment in the dispatch log:

```text
segment_id | pages | parser_agent | parser_status | reviewer_agent | review_score | review_status | final_file
```

### 4. Parser Agent Dispatch

Dispatch parser agents per segment. Each parser prompt must require:

- scope and page range
- scene/node list
- clue table
- revelation list where relevant
- NPCs, locations, items
- dependencies and next-node links
- failure/callback options
- page evidence

Parser agents collect facts only. They do not write final global conclusions.

Save each accepted parser result to:

```text
docs/reports/<module-slug>/segment-<id>-analysis.md
```

### 5. Expert Review After Each Segment

After each segment parser completes, dispatch an independent expert review agent.

Reviewer checks:

- factual accuracy against raw chunk
- missing nodes or clues
- wrong inference vs evidence
- page evidence quality
- hard blockers for running the module
- score 0-100

Decision:

- `>= 80`: pass; apply required small corrections.
- `70-79`: conditional; apply corrections and optionally re-review if core logic changed.
- `< 70`: fail; redispatch parser or reviewer after updating instructions.

The main agent applies review corrections to segment files and records the result.

### 6. Final Synthesis

After all segments pass or are corrected, write:

```text
knowledge-base/<namespace>/modules/<module-slug>/parsed/module-architecture.md
```

Keep the final user-facing architecture simple and explicit:

- one-sentence premise
- recommended play order
- main plot truth
- major adventure branches
- key NPCs
- locations
- clue flow
- climax and endings
- keeper prep checklist
- review status summary

Do not hide spoilers unless the user requests spoiler-free output.

### 7. Catalog Entry

Append or update:

```text
knowledge-base/index/catalog.jsonl
```

Required fields:

- `id`
- `namespace`
- `source`
- `source_type`
- `tags`
- `path`
- `raw_text_path`
- `captured_at`
- `ingested_at`
- `status`
- `note`

Use UTF-8 JSONL. On Windows, verify CJK paths after writing:

```python
Path("knowledge-base/index/catalog.jsonl").read_text(encoding="utf-8")
```

If `?` appears in a path, the string was already corrupted before JSON writing. Recover the real path by enumerating the filesystem, then rewrite the record.

## Completion Checklist

- Source accessible.
- Raw extraction exists.
- Page files exist and preserve page numbers.
- All chunks mapped to page ranges.
- Each chunk has parser output.
- Each chunk has expert review or documented merged review.
- Required review corrections applied.
- Final module architecture written.
- Catalog entry valid UTF-8 with non-corrupted source path.
- Dispatch log updated with final statuses.

