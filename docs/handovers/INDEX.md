# Handover Index

极简交接索引。每个小 step 必须对应一条文档记录，保证任意 AI 或人工可无缝接手。

## 命名规范

- 文件名：`YYYYMMDD-HHMM-step-slug.md`
- 示例：`20260512-1615-seed-coc-sources.md`

## 最新步骤

| Step | Status | Doc | Owner |
|---|---|---|---|
| handover-doc-system | done | `docs/handovers/20260512-1610-handover-doc-system.md` | codex |
| seed-coc-kp-sources | done | `docs/handovers/20260512-1615-seed-coc-kp-sources.md` | codex |
| module-folder-bootstrap | done | `docs/handovers/20260512-1620-module-folder-bootstrap.md` | codex |
| catalog-schema-upgrade | done | `docs/handovers/20260512-1625-catalog-schema-upgrade.md` | codex |
| self-review-gate | done | `docs/handovers/20260512-1630-self-review-gate.md` | codex |
| phase-acceptance-check | done | `docs/handovers/20260512-1635-phase-acceptance-check.md` | codex |

## 审查要点

- 每条 step 文档必须包含：`Context` `Inputs` `Actions` `Outputs` `Next` `SelfReview`
- `Outputs` 中的文件路径必须可点击、可追踪
- `SelfReview` 不能空白，至少包含 1 条风险与 1 条验证结果
- 自审项必须覆盖 `docs/handovers/SELF_REVIEW_CHECKLIST.md`
