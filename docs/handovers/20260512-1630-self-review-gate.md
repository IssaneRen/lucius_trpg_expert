# 20260512-1630 self-review-gate

## Context

- 把“每步固定自审”从口头约定升级为可执行文档门禁。

## Inputs

- `docs/handovers/INDEX.md`
- `docs/handovers/TEMPLATE.md`

## Actions

- 新增统一清单 `SELF_REVIEW_CHECKLIST.md`
- 在 `INDEX.md` 中显式要求 step 文档覆盖该清单
- 补充最近步骤记录，确保索引可直接审查

## Outputs

- `docs/handovers/SELF_REVIEW_CHECKLIST.md`
- `docs/handovers/INDEX.md`
- `docs/handovers/20260512-1630-self-review-gate.md`

## Next

- 按验收标准执行最终检查，并记录缺口与后续动作。

## SelfReview

- 风险：若后续执行者绕过 `INDEX.md` 直接改文件，流程约束可能弱化。
- 验证：固定自审清单已落地并在索引中绑定，具备最小门禁能力。
