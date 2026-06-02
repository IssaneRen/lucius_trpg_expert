---
name: coc7e-recruitment-poster
description: |
  Write non-spoiler recruitment copy for a CoC 7e module/campaign and generate
  ready-to-paste poster prompts for ChatGPT web gpt-image-v2.
fallback: |
  If the module summary is incomplete or inconsistent, produce a safe, generic
  recruitment copy that only uses confirmed facts (time, place, theme, tone),
  and mark any assumptions explicitly.
---

# CoC 7e Recruitment + Poster Prompt Skill

## Goal

- Produce **attractive** recruitment copy that **strictly follows module key facts**.
- Produce **ready-to-paste** poster prompts for **ChatGPT web** running **gpt-image-v2**.
- Keep players intrigued while avoiding keeper-only spoilers.

## Inputs (required)

- `module_title`: string
- `system`: string (expect `"coc7e"`)
- `time_place`: string (e.g. `"1925–1930 Vermont, New England"`)
- `core_theme`: string (1 sentence)
- `structure`: bullet list (how many parts, optional side-quests)
- `hooks_safe`: 5–12 bullets (player-visible mysteries / imagery)
- `content_warnings`: bullets (themes that should be disclosed)
- `campaign_scope`: one of `campaign` | `two-shots` | `mini-arc`

## Guardrails (must follow)

- **No keeper-only truth**: do not reveal “who/what/why” if it is flagged as core truth, secret branching, or solution mechanics.
- **Use only safe hooks**: “phenomena / rumors / imagery / public reports” are OK.
- **Do not mention** “four truths / keeper chooses” lists; you may say “multiple possible explanations”.
- **Avoid trademarked characters and recognizable real people** in poster prompts.
- **Avoid overt Lovecraftian clichés** in visuals (no tentacle-face monster).

## Output A — Recruitment Copy (template)

Produce in this structure:

- Title (1 line)
- Elevator pitch (2–3 lines)
- Highlights (5–8 bullets)
- What you’ll do at the table (3–5 bullets)
- Tone & safety (bullets)
- Character fit (3–5 bullets)
- Logistics (session count range + onboarding)
- Signup questions (3 short questions)

## Output B — Poster Prompt (gpt-image-v2)

### Prompt format (single paste)

Write one block that includes:

- Task + poster purpose
- Layout constraints (2:3 vertical, letterpress broadside)
- Typography vibe (1920s letterpress, Chinese vintage print feel)
- Color palette (2–3 spot colors + aged paper)
- Era elements (New England rural, 1920s props)
- Subtle dread cues (fog, wrong shadows, geometric sky)
- Exact headline text (if needed)
- “Please avoid:” negative constraints list

### Period-safe objects (clarify)

- **Allowed**: 1920s automobiles (silhouette), telephone poles/wires, hand-painted shop signs, oil lanterns, early street lamps.
- **Avoid**: smartphones, modern computers, post-2010 car designs, modern LED billboards, modern neon aesthetics.

### Two variants

- Variant 1: **Folk-horror / rural**
- Variant 2: **Modern encroachment / industrial**

## Output C — Two deliverables mode

If asked for both:

1) Full campaign recruitment + poster prompt
2) First two short modules recruitment + poster prompt

Ensure both sets **reuse the same visual language** (consistent brand), but with different central imagery.

