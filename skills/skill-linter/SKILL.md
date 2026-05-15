---
name: skill-linter
description: Lint a SKILL.md against the canonical structural template and report findings (missing sections, wrong ordering, non-canonical headings, infinite-loop risks, polyglot skills) for skill-creator to fix. Use this skill whenever the user asks to lint a skill, whenever a skill has just been created or edited with skill-creator, or whenever the user mentions skill structure, skill template, or skill consistency.
---

# Skill Linter

A companion linter to skill-creator that enforces a canonical SKILL.md body structure and flags suspicious loops and polyglot skills.

## Overview

Skill-linter inspects the body of a SKILL.md after a skill has been created or edited and reports structural findings against a fixed, opinionated template. It checks heading names, section ordering, the presence of a one-line pitch, the shape of the Overview, the use of `### Step N:` sub-headings inside Workflow, and two semantic-but-syntactically-detectable risks: loops without a clear exit condition, and skills that appear to cover multiple unrelated workflows (polyglot skills).

This skill exists because skill-creator deliberately produces skills generatively, optimizing for the user's intent rather than a uniform shape. That flexibility is good, but a portfolio of skills written across different sessions and model versions tends to drift in section names, ordering, verbosity, and structure. A small, focused linter that runs after creation closes that gap without conflicting with skill-creator: skill-linter only reports findings and proposes the *shape* of a fix, never the content. Skill-creator decides how to apply the fix.

Success looks like this: after skill-creator finishes producing or editing a skill, skill-linter is invoked, produces a JSON report of findings (errors, warnings, info), and hands that report to skill-creator with a clear instruction to fix errors, decide on warnings, and revalidate omitted optional sections. The result is a skill whose SKILL.md follows the canonical template exactly — same heading names, same ordering, same minimum content shape — while preserving the substantive instructions skill-creator wrote.

## When to use this skill

Use skill-linter whenever:

- A skill has just been created or edited (especially via skill-creator) and you want to enforce the canonical SKILL.md structure before shipping.
- The user asks to "lint", "validate the structure of", "check the template of", or "audit" a skill.
- You suspect a skill might be polyglot — i.e., trying to do many different things — and want a syntactic signal to confirm.
- You want to catch loops in a Workflow that lack an explicit exit condition.
- You are reviewing a portfolio of skills and want a consistent structural baseline.

Skill-linter is intentionally narrow: it only inspects the SKILL.md body. It is complementary to (not a replacement for) `skill-creator/scripts/quick_validate.py`, which already enforces frontmatter validity, naming rules, and length limits.

### When NOT to use this skill

- Do not use skill-linter to judge the *substance* of a skill's instructions. It is a syntactic linter, not a semantic reviewer.
- Do not use it as a gating step for skills that are intentionally exploratory drafts the user has not yet asked to finalize.
- Do not use it to validate the YAML frontmatter — that is `quick_validate.py`'s job.
- Do not use it to evaluate skill performance — that is the eval/benchmark loop in skill-creator.

## Constraints

- **Read-only and explicitly invoked**: Skill-linter never edits the skill it lints, never watches files, never hooks into editors, and never auto-triggers on save. It only runs when explicitly invoked, and only ever produces a JSON report and a hand-off message; skill-creator decides and applies fixes.
- **Syntactic, not semantic**: All suggestions describe the *shape* of a fix, not the *content*. The linter never proposes what a section should *say*, what a polyglot skill should be *split into*, or what a loop's exit condition *should be*.
- **Body-only scope**: Inspects only the body of `SKILL.md`. Frontmatter validation is delegated to `skill-creator/scripts/quick_validate.py`; performance evaluation is delegated to skill-creator's eval/benchmark loop.
- **Zero false positives**: Trust in the linter requires zero false positives. When a check is ambiguous, pass. Better to miss a real issue than to flag a non-issue. Each new rule must ship with at least one negative fixture proving it does NOT fire on compliant skills.

## Inputs

To lint a skill, gather:

- **`skill_path`** (required): Absolute path to the skill directory containing `SKILL.md`.
- **`output_path`** (optional): Where to write the report file. **Defaults to no file** — output is printed to stdout only. Pass an explicit path (e.g., `/tmp/skill-lint-<name>.json`) only when you need a persistent artifact. Never write into the skill's own directory — it may be version-controlled and owned by someone else.
- **`hand_off_to_skill_creator`** (optional, default `true`): Whether to format the findings as a hand-off prompt for skill-creator after producing the JSON report.
- **`strict`** (optional, default `false`): Whether to run in strict mode. Strict mode adds rule R017 (`non-canonical-section`) which flags ANY `##` heading not in the canonical set — useful for new skills where applying the template is cheap. Leave off for legacy skills where retrofit cost is high.

If the user provides only a skill name and no path, search common locations (`~/.agents/skills/<name>/`, `./<name>/`, `./skills/<name>/`) and confirm with the user before proceeding.

## Output

Skill-linter produces two artifacts:

1. **A JSON (or markdown) report** printed to stdout. Optionally also written to `output_path` when `--output` is explicitly provided — never to the skill's own directory.

```json
{
  "skill_path": "path/to/skill",
  "skill_name": "skill-name",
  "passed": false,
  "summary": {"errors": 2, "warnings": 1, "info": 1},
  "findings": [
    {
      "rule": "missing-section",
      "severity": "error",
      "location": "SKILL.md body",
      "found": null,
      "expected": "## Overview",
      "suggestion": "Add a `## Overview` section with 3-5 paragraphs (what / why / how success looks)."
    }
  ]
}
```

`passed` is `true` only when there are zero errors. Warnings and info findings do not block.

2. **A hand-off message** for skill-creator (if `hand_off_to_skill_creator` is true), using this exact wording:

> The skill-linter found the following structural issues in the SKILL.md you just produced.
>
> For each `error` → fix the structural violation while preserving all existing content and intent.
> For each `warning` → fix or briefly justify keeping as-is.
> For each `info` → revalidate whether the omitted optional section is appropriate.
>
> Do not change the skill's substantive behavior — only its structure and clarity. Suggestions describe the shape of the fix, not the content; you decide the content.

Suggestions in findings are always *syntactic*: they describe the *shape* of the fix (e.g., "split into narrower skills", "add a `## Overview` section with 3 paragraphs"), never the *content* of the fix (e.g., they never say *what* the new skills should be or *what* the Overview paragraphs should contain). Skill-creator owns those decisions.

## Workflow

### Step 1: Locate and read the SKILL.md

Resolve `skill_path` to an absolute path. Read `<skill_path>/SKILL.md` in full. Parse the frontmatter (YAML) to extract `name` and `description`. Separate the body (everything after the closing `---`).

If the file does not exist or the frontmatter cannot be parsed, stop with a single error finding (`rule: "skill-md-unreadable"`) — there is nothing to lint without a body.

### Step 2: Run the structural rules

Run the rules defined in `references/rules.md`. The full catalog is documented there; the rule engine in `scripts/lint.py` implements them. Each rule produces zero or more findings with `rule`, `severity`, `location`, optional `found` and `expected`, and a `suggestion` describing the shape of the fix.

The structural rules check, in this order:

- The H1 title exists and matches the kebab `name` from frontmatter when title-cased.
- A single-line pitch exists directly under the H1.
- All required sections (`## Overview`, `## When to use this skill`, `## Workflow`) are present.
- Headings use canonical names exactly (no synonyms like `## Process`, `## Steps`, `## How it works`).
- Sections appear in the locked order: H1 → pitch → Overview → When to use → (optional Inputs) → (optional Output) → Workflow.
- `## Overview` contains 3 to 5 plain paragraphs and no sub-headings.
- `## Workflow` contains `### Step N:` sub-headings, numbered sequentially starting at 1.
- Empty workflow steps are flagged (single empty step → warning; ≥2 empty steps → error).

### Step 3: Run the loop-termination rule

Inside `## Workflow`, scan each step body for loop-language signals: `repeat`, `loop`, `until`, `iterate`, `keep going`, `while`, `go back to step`, `return to step`.

For each signal, look in the same step for a clear exit condition: phrases like `until the user says…`, `until <state>`, `when <condition>`, `once <condition>`, `if <state>, stop`. If no clear exit condition is found, emit a warning (`rule: "loop-without-exit-condition"`).

Iteration caps are not required — a clear exit condition suffices. If both are missing or the exit is suspiciously vague, raise the warning.

### Step 4: Run the polyglot-detection rule

Look for syntactic signals that the skill covers multiple unrelated workflows:

- The one-line pitch joins two distinct activity verbs with `" and "`.
- `## Overview` lists multiple distinct primary use cases joined by `also`, `in addition`, `or alternatively`, or `as well as`.
- `## Workflow` contains top-level branches like *"if the user wants X, follow these steps; if they want Y, follow these completely different steps"*.
- The frontmatter `description` lists ≥3 distinct domains/verbs joined by commas or `and`.

If any signal fires, emit a single warning (`rule: "polyglot-skill"`) with a syntactic suggestion: *"This skill appears polyglot. Consider splitting it into narrower skills, each with a single primary workflow. Skill-creator should decide how to split."*

Do not propose what the new skills should be — that is skill-creator's call.

### Step 5: Emit info findings for omitted optional sections

If `## Inputs` or `## Output` is absent, emit a single `info`-severity finding per missing optional section, with the suggestion: *"Optional section `## Inputs` is omitted. If the skill takes user-provided inputs, consider adding it; otherwise leave omitted."*

Info findings never block — they exist so skill-creator can revalidate the necessity of each optional section.

### Step 6: Aggregate, write the report, and hand off

Aggregate all findings into the JSON shape shown in `## Output`. Compute `summary.errors`, `summary.warnings`, `summary.info`. Set `passed = (summary.errors == 0)`.

Write the report to `output_path`. If `hand_off_to_skill_creator` is true, also print the hand-off message verbatim, followed by the report path.

Do not edit the skill yourself. Skill-linter only reports; skill-creator fixes.

## Reference files

- `references/template.md` — The canonical SKILL.md body template (locked v0.1). Read this when you need to remind yourself of the exact required structure, ordering, and naming.
- `references/rules.md` — The full rule catalog with rule IDs, severities, detection logic, and suggestion text. Read this when you need to understand exactly what a rule checks or why it fired.
- `scripts/lint.py` — Executable Python implementation of all rules. Run it with `python scripts/lint.py <skill_path> [--output <path>] [--no-handoff] [--strict] [--format json|md]` to produce a JSON or grouped-markdown report. Output goes to stdout by default; `--output` is opt-in and should never point inside the reviewed skill's directory.
