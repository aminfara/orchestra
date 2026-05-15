# Canonical SKILL.md Body Template (v0.5)

This is the locked v0.1 structural template that skill-linter enforces against the body of a SKILL.md. Headings must match exactly. Ordering is strict. Optional sections must be omitted entirely (not stubbed with "N/A") when they do not apply.

## The template

```markdown
# <Human-Readable Skill Title>

<One-sentence pitch — exactly one line, directly under the H1.>

## Overview

<Paragraph 1: WHAT this skill does.>

<Paragraph 2: WHY this skill exists.>

<Paragraph 3: HOW success looks — what a successful invocation produces.>

<!-- 3 paragraphs minimum, 5 maximum. 3 is encouraged. -->

## When to use this skill

<Concrete trigger contexts. "Use when…" guidance.>

<!-- Optional, encouraged sub-section -->
### When NOT to use this skill

<Counter-examples and near-miss cases where another skill/tool is better.>

## Constraints

- <Constraint 1: a hard rule the skill must obey, optionally with a brief "why".>
- <Constraint 2.>
- <…>

<!-- Required. Bullet list only. At least 1 bullet. Soft-warn at >4, error at >8.
     7+ bullets also feed into the polyglot signal. -->

## Inputs
<!-- OPTIONAL — omit entirely if the skill has no user-provided inputs. -->

<What to gather from the user before starting: parameters, files, questions to ask.>

## Output
<!-- OPTIONAL — omit entirely if the skill produces no structured output. -->

<Templates, schemas, or file formats the skill produces.>

## Workflow

### Step 1: <Title>

<Instructions.>

### Step 2: <Title>

<Instructions.>

<!-- Loops, when present, must have a clear exit condition. -->

## Reference files
<!-- OPTIONAL — omit entirely if the skill has no bundled scripts/references/assets.
     The plain heading `## References` is also accepted as a canonical alias (v0.7). -->

- `scripts/<file>.py` — <when and why to use it>
- `references/<file>.md` — <when to read it>
```

## Locked rules at a glance

- H1 title is required and must match the kebab `name` from frontmatter when title-cased (e.g., `skill-creator` → `Skill Creator`).
- The one-line pitch is required and must be a single line directly under the H1.
- `## Overview` is required and contains 3-5 plain paragraphs (what, why, how success looks). No sub-headings inside Overview.
- `## When to use this skill` is required. `### When NOT to use this skill` is an encouraged sub-section.
- `## Constraints` is required (v0.3). Bullet list only, at least 1 bullet. Soft-warn at >4, error at >8. 7+ bullets also feed into the polyglot signal.
- `## Inputs` and `## Output` are optional. When present, they must appear before `## Workflow` in this order.
- `## Workflow` is required and contains `### Step N: <Title>` sub-headings numbered sequentially starting at 1.
- `## Reference files` is optional (v0.4). When present, it must appear after `## Workflow` and use a bullet list of files with one-liner pointers.
- Section ordering is exact: H1 → pitch → Overview → When to use → Constraints → (Inputs?) → (Output?) → Workflow → (Reference files?).
- Heading names are exact — no synonyms like `## Process`, `## Steps`, `## How it works`.
- Optional sections that do not apply must be omitted entirely; the linter emits an `info` finding so skill-creator can revalidate the omission.
