# Rule Catalog (v0.5)

Each rule has a stable ID, a severity, a detection rule, and a syntactic suggestion. Suggestions describe the *shape* of the fix, never the *content* of the fix.

## Operating doctrine

- **Zero false positives.** Trust in the linter requires zero false positives. When a rule's detection logic is ambiguous, prefer to pass over to flag. Better to miss a real issue than to flag a non-issue. Every new rule must ship with at least one negative fixture proving it does NOT fire on a compliant skill.
- **Stable IDs.** `R001`-`R029` are stable for backward compatibility. New rules append; existing IDs never change meaning.
- **Single source of truth.** This file is canonical. The implementation in `scripts/lint.py` and the test suite in `tests/` must stay in sync with it.

## Severity model

- **error** — structural violations the skill cannot ship with. Skill-creator must fix.
- **warning** — quality concerns. Skill-creator should fix or briefly justify keeping as-is.
- **info** — informational only. Used for omitted optional sections so skill-creator can revalidate the omission.

`passed` in the JSON report is `true` only when the report contains zero errors.

## Rules

### R001 — `missing-h1-title`
- Severity: error
- Detection: The body has no `# <Title>` heading at the top.
- Suggestion: *"Add an `# <Human-Readable Skill Title>` H1 at the very top of the SKILL.md body."*

### R002 — `h1-name-mismatch`
- Severity: error
- Detection: Two-tier match (zero-false-positive doctrine — prefer to pass):
  - **Tier 1**: Case-insensitive exact match after mechanically title-casing the kebab name. This fixes the acronym false positive — `azure-ai` → `Azure Ai` (wrong casing) vs H1 `Azure AI` (correct). Since comparison is case-insensitive per-token, `AI` ≡ `Ai` and the match passes.
  - **Tier 2**: 50% word-overlap tolerance. If Tier 1 fails, check whether ≥50% of the kebab name's tokens appear (case-insensitively) in the H1 words. This allows deliberate author titles like `React Composition Patterns` for `vercel-composition-patterns` while still catching truly unrelated H1s. "Microsoft Foundry Skill" for `microsoft-foundry` passes (both tokens present); a completely unrelated H1 would fail.
- Suggestion: *"The H1 title has low word overlap with the kebab `name`. Ensure the H1 is a human-readable form of the skill name (at least half the name's words should appear in the H1)."*

### R003 — `missing-pitch-line`
- Severity: error
- Detection: No non-empty, non-heading line appears directly under the H1 before the next heading.
- Suggestion: *"Add a single-sentence pitch directly under the H1 title, before any other heading."*

### R004 — `pitch-not-one-line`
- Severity: error
- Detection: The pitch under the H1 spans more than one line (e.g., wraps into multiple paragraphs or contains a hard line break).
- Suggestion: *"Collapse the pitch into a single line directly under the H1."*

### R005 — `missing-section`
- Severity: error
- Detection: One of the required sections is absent: `## Overview`, `## When to use this skill`, `## Workflow`.
- Suggestion: *"Add the required section `<heading>` in its canonical position."*

### R006 — `non-canonical-heading`
- Severity: error
- Detection: A heading uses a synonym of a canonical heading name. Examples flagged: `## Process`, `## Steps`, `## How it works`, `## What it does`, `## Usage`, `## Procedure` when used in place of `## Workflow`; `## Summary`, `## Description`, `## Intro` when used in place of `## Overview`.
- Suggestion: *"Rename `<found>` to its canonical equivalent `<expected>`."*

### R007 — `section-out-of-order`
- Severity: error
- Detection: Required or optional sections appear in the wrong order. The locked order is: H1 → pitch → Overview → When to use → (Inputs?) → (Output?) → Workflow.
- Suggestion: *"Move `<found>` so that the canonical section ordering is preserved."*

### R008 — `overview-paragraph-count`
- Severity: error
- Detection: `## Overview` contains fewer than 3 or more than 5 plain paragraphs.
- Suggestion: *"Adjust `## Overview` to contain between 3 and 5 paragraphs (3 is encouraged)."*

### R009 — `overview-has-subheadings`
- Severity: error
- Detection: `## Overview` contains any `###` (or deeper) sub-headings.
- Suggestion: *"Remove all sub-headings from `## Overview`; keep it as plain paragraphs only."*

### R010 — `workflow-missing-steps`
- Severity: error
- Detection: `## Workflow` exists but contains no `### Step N: <Title>` sub-headings.
- Suggestion: *"Convert the workflow body into numbered `### Step N: <Title>` sub-headings."*

### R011 — `workflow-step-numbering`
- Severity: error
- Detection: `### Step N:` sub-headings are not sequential starting at 1 (e.g., gaps, duplicates, or starting at a number other than 1).
- Suggestion: *"Renumber the `### Step N:` headings so they are sequential starting at 1."*

### R012 — `empty-workflow-step`
- Severity: warning for a single empty step; **error** if 2 or more workflow steps are empty.
- Detection: A `### Step N:` sub-section has effectively no body content (only whitespace, comments, or fewer than ~10 substantive characters before the next heading).
- Suggestion (single): *"Add instructions to `### Step <N>`, remove it, or merge it with an adjacent step."*
- Suggestion (multiple): *"Multiple empty workflow steps detected. Either flesh out each step's instructions, remove the empty steps, or merge them into adjacent steps."*

### R013 — `loop-without-exit-condition`
- Severity: warning
- Detection: A workflow step body contains loop language (`repeat`, `loop`, `until`, `iterate`, `keep going`, `while`, `go back to step`, `return to step`) but no clear exit condition (`until the user says…`, `until <state>`, `when <condition>`, `once <condition>`, `if <state>, stop`, etc.).
- Suggestion: *"Add a clear exit condition to the loop in this step so it cannot run forever."*

### R014 — `polyglot-skill`
- Severity: warning
- Detection: One or more of these syntactic signals fire:
  - **Pitch (tightened in v0.2)**: the one-line pitch contains a strong second-workflow marker (`" and also "`, `" and additionally "`, `" and separately "`, `" and independently "`), OR the pitch contains 3+ verb-object clauses separated by `" and "` / `", "`. A single `" and "` joining two clauses about the same workflow is no longer flagged on its own.
  - `## Overview` lists multiple distinct primary use cases joined by `also`, `in addition`, `or alternatively`, or `as well as`.
  - `## Workflow` contains top-level branches like *"if the user wants X, follow these steps; if they want Y, follow these completely different steps."*
  - **Description (tightened in v0.6)**: the frontmatter `description` contains ≥4 *distinct workflow verbs* drawn from a curated allowlist (create, edit, lint, validate, deploy, search, summarize, etc.). The earlier "raw clause count" approach was retired because legitimate enumerations of formats, domains, or products inflated the clause count without implying multiple workflows. Counting verbs from a small allowlist yields a much cleaner signal.
- Suggestion: *"This skill appears polyglot. Consider splitting it into narrower skills, each with a single primary workflow. Skill-creator should decide how to split."*

### R015 — `optional-section-omitted`
- Severity: info
- Detection: `## Inputs` or `## Output` is absent.
- Suggestion: *"Optional section `<heading>` is omitted. If the skill takes user-provided inputs / produces structured output, consider adding it; otherwise leave omitted."*

### R016 — `skill-md-unreadable`
- Severity: error (terminal — no other rules run)
- Detection: `SKILL.md` does not exist, frontmatter cannot be parsed, or the body is empty.
- Suggestion: *"Ensure `SKILL.md` exists, has valid YAML frontmatter, and a non-empty body."*

### R018 — `missing-constraints-section`
- Severity: error
- Detection: `## Constraints` section is absent. (Implemented via R005 `missing-section` since `## Constraints` is in REQUIRED_SECTIONS.)
- Suggestion: *"Add the required section `## Constraints` between `## When to use this skill` and `## Inputs` (or `## Workflow` if Inputs is omitted). Use a bullet list with at least 1 constraint."*

### R019 — `constraints-out-of-order`
- Severity: error
- Detection: `## Constraints` appears outside its canonical slot (between `## When to use this skill` and `## Inputs`). (Implemented via R007 `section-out-of-order` since `## Constraints` is in CANONICAL_ORDER.)
- Suggestion: *"Move `## Constraints` to its canonical slot, immediately after `## When to use this skill`."*

### R020 — `constraints-empty`
- Severity: error
- Detection: `## Constraints` exists but contains no bullets.
- Suggestion: *"Add at least one constraint bullet. Every skill must declare its constraints explicitly (even if minimal)."*

### R021 — `constraints-not-bullets`
- Severity: error
- Detection: `## Constraints` body contains non-bullet content: paragraphs, sub-headings, code blocks, or other markdown elements.
- Suggestion: *"Reformat `## Constraints` as a bullet list. Remove paragraphs, sub-headings, and code blocks."*

### R022 — `constraints-too-many`
- Severity: warning if >4, **error** if >8.
- Detection: Counts top-level bullets inside `## Constraints`.
- Suggestion (warning): *"Consider whether all constraints are essential. Merge overlapping ones, or split the skill if it is doing too much."*
- Suggestion (error): *"More than 8 constraints suggests this skill is over-constrained or polyglot. Split it into narrower skills, or merge related constraints."*
- Bonus: 7+ bullets also feeds into R014 (`polyglot-skill`) as an additional syntactic signal.

### R017 — `non-canonical-section` (strict mode only)
- Severity: error
- Detection: Active only when `--strict` is passed. Any `##` heading that is not in the canonical set (`## Overview`, `## When to use this skill`, `## Constraints`, `## Inputs`, `## Output`, `## Workflow`, `## Reference files`) and is not already covered by R006's synonym list.
- Suggestion: *"Heading `<found>` is not in the canonical set. Either rename it to a canonical heading, fold its content into the appropriate canonical section, or remove it."*
- Rationale: Default mode flags only known synonyms (R006). Strict mode rejects domain-named h2s like `## Creating a skill`, `## Improving the skill`, `## Description Optimization`, etc., enforcing total uniformity. Use strict mode for new skills where applying the template is cheap; leave it off for legacy skills where retrofit cost is high.

### R023 — `reference-files-position` (v0.4)
- Severity: error
- Detection: `## Reference files` is present but appears before `## Workflow`. Implemented via R007 `section-out-of-order` since `## Reference files` is in CANONICAL_ORDER as the last allowed section.
- Suggestion: *"Move `## Reference files` so it appears after `## Workflow`."*

### Synonyms recognized for `## Reference files` (R006)
`## Reference Files` (different capitalization), `## Reference`, `## Resources`, `## Bundled resources`, `## Files`.

### Canonical aliases (v0.7) — accepted as equivalent, no rename required
- `## References` ≡ `## Reference files` — both spellings are accepted everywhere a canonical heading is expected (R005, R007, R017, R023, R029). The alias was added based on a real-world skill audit that found 3/5 skills used `## References` — recognizing both as canonical avoids forcing a low-value rename.

Aliases differ from synonyms in that they do NOT trigger R006 (`non-canonical-heading`); the linter treats both spellings as equally valid.

---

## v0.5 rules — adapted from `check-skill`

These rules were inspired by the `check-skill` peer linter. Only generic, project-agnostic checks were adopted (privacy, MARVIN-specific, and Rovo-specific rules were intentionally omitted).

### R024 — `name-matches-directory`
- Severity: error
- Detection: The skill's directory name does not match the frontmatter `name` field exactly.
- Suggestion: *"Rename either the skill directory or the frontmatter `name` so they match exactly."*
- Rationale: A name/directory mismatch is a common failure mode that breaks tooling that locates skills by directory name.

### R025 — `references-only-text`
- Severity: warning
- Detection: The `references/` directory contains files with extensions other than `.md` or `.txt` (hidden dotfiles ignored).
- Suggestion: *"Move non-text files out of `references/` (e.g., into `assets/` or `scripts/`), or convert them to `.md` / `.txt`."*
- Rationale: `references/` is for human/agent-readable text. Binary or executable files belong elsewhere.

### R026 — `body-not-empty`
- Severity: warning
- Detection: After stripping comments, code blocks, headings, and whitespace, the body has fewer than 50 substantive characters.
- Suggestion: *"Add substantive content to the SKILL.md body. A near-empty skill provides no instructions for the model."*
- Rationale: A skill with only headings and no content offers nothing to the model.

### R027 — `line-budget`
- Severity: info
- Detection: `SKILL.md` exceeds 500 lines total.
- Suggestion: *"Consider moving long templates, examples, or detailed steps into `references/` files."*
- Rationale: Progressive disclosure — long SKILL.md files load too much into context. Informational only; never blocks.

### R028 — `body-leanness`
- Severity: warning
- Detection: The SKILL.md body (after frontmatter) exceeds 300 lines.
- Suggestion: *"Trim the SKILL.md body. Move long templates, checklists, or examples to `references/` and keep the body focused."*
- Rationale: SkillsBench research suggests compact skills outperform long ones for agent effectiveness.

### R029 — `reference-files-pointers-resolve`
- Severity: warning
- Detection: Bullets in the `## Reference files` section reference paths (in inline code) that do not exist in the skill directory. Absolute paths, URLs, and obvious placeholders like `file.py` are exempt (zero-false-positive guard).
- Suggestion: *"Update each broken pointer in `## Reference files` to a real file, remove stale entries, or create the missing file."*
- Rationale: Stale pointers in the Reference files section are a silent rot pattern.

## Notes on suggestion style

- Suggestions describe the *shape* of the fix, not the content.
- Do not propose what a new section should *say*; only that it should *exist* and *where*.
- Do not propose what a polyglot skill should be *split into*; only that it should be split.
- Do not propose what a loop's exit condition *should be*; only that one is needed.

This separation keeps skill-linter syntactic and skill-creator authoritative on substance.
