---
name: writing-studio
description: Write or review professional, human-facing prose so the result is clear, well-structured, correctly shaped for its document type, and free of AI-sounding filler. Use this skill WHENEVER you are about to write something a person will read (a proposal, email, chat or Slack message, document or wiki page, blog post, announcement, status update, RFC or design doc, release notes, exec brief, incident report, peer performance feedback, RACI or roles-and-responsibilities matrix) OR when asked to review, improve, polish, critique, proofread, tighten, sharpen, or shorten any existing text. Prefer it over ad-hoc style fixes, especially for multi-paragraph or long-form writing. Do NOT use it for code, code comments, commit messages, machine-readable data (JSON/YAML/CSV), or trivial one-line replies.
---

# Writing Studio

Write new prose well, or review existing prose, for any human reader.

## Overview

This skill helps you do two things: **generate** strong professional writing on the first try, and **review** existing writing and return useful, prioritized feedback. It works for any document a person reads, including proposals, emails, chat messages, documents and wiki pages, blog posts, announcements, status updates, RFCs, release notes, and incident reports.

For any task, you first identify a few things about the writing (its document type, purpose, where it will be read, the tone, and the audience), then apply a shared set of writing rules plus a template for that document type. The rules cover clarity, structure, concision, and honesty, and they include checks that stop the output from sounding machine-written or stating facts that were never given.

A good result in generate mode is a draft that is shaped correctly for its document type, holds the requested tone, invents no facts, and reads like a capable person wrote it. A good result in review mode is a short, prioritized list of findings grouped by impact, each explaining the problem and the fix.

## When to use this skill

Load this skill whenever you are about to produce, expand, edit, or review prose a person will read. Beyond the document types in the description, this includes:

- Converting notes or an outline into prose, or summarizing a long document.
- Adjusting writing to a target tone or audience ("make this more formal", "an exec version").
- Producing output that other people, not just the requester, will read, even mid-task in a larger job.

### When NOT to use this skill

- Code generation, code comments shorter than a sentence, or commit messages governed by house conventions.
- Machine-readable data (JSON, YAML, CSV) — there is no human reader to optimize for.
- One-line acknowledgements ("done", "got it").
- Translation/transcription where the source style must be preserved verbatim.

## Constraints

- **Preserve the writer's intent and voice.** In review, do not rewrite meaning or flatten a distinctive voice into generic corporate prose. In generate, match the requested tone; do not impose a house style.
- **Apply rules with judgment, not as a checklist.** Each universal rule names when it applies and when it does not. Clarity for the actual reader beats conformity. If a rule would hurt this format/tone/audience, skip it and (in review) say why.
- **Never fabricate.** No invented quantification, sources, names, or dates. Name the gap (`[CLARIFY: ...]`) instead. This is enforced by the anti-hallucination pass in `references/universal-rules.md` (rule A9).
- **Honor stated length limits as hard caps.** If content will not fit, ask what to cut rather than overflowing. In review, prioritize and deduplicate findings: group by impact (structure → substance → sentence-level) and report a repeated issue once with examples, not per-paragraph.

## Inputs

Before drafting or reviewing, resolve these from context. Infer silently when confident; **ask only when a key input is genuinely unclear.**

- **mode** — `generate` (write new text) or `review` (give feedback on existing text). If the user supplies text and says "improve", default to `review` and offer a rewrite.
- **format** — the document type (proposal, email, blog, status update, RFC, ...). This selects the template in `references/formats/`. If none matches, see Workflow Step 2.
- **purpose** — inform, persuade/recommend, announce, request, instruct, report, document a decision, narrate a vision.
- **medium** — where it will be read: email, chat, wiki page or document, issue tracker, printed page. This sets length and formatting conventions.
- **tone** — formal, neutral, friendly, persuasive, authoritative, visionary, urgent, or a free-form description ("warm but direct"). If unspecified, use the format's default.
- **audience** — who reads it, what they know, how much attention they will give. This drives tone and vocabulary.
- **completeness** (only for formats that define levels, e.g. proposal, RACI) — how fully worked-out this should be. The level names are format-specific and listed in that format's base file. Infer from the request: "shoot a quick note proposing X" → proposal floater; "write up a one-pager" → one-pager; "write the proposal doc" → full; "drop a note in the channel on who owns what" → RACI prose. Ask if unclear. Formats without levels (e.g. blog post, peer feedback) ignore this.

Example: "Write an email to the team reporting the launch slip" resolves cleanly (format=email, purpose=report, medium=email, audience=team) — proceed. "Write something about X" does not — ask for format and destination.

## Output

**Generate mode.** Lead with the deliverable itself, starting with its natural title (or no title for a short email/message). Put meta below a `---` divider so a human sees only the prose:

```text
[the prose]

---
## Notes (for the agent, not the reader)
- What you used: format / purpose / medium / tone / audience (inferred or given)
- Rules relaxed and why (e.g. "skipped quantify-impact: visionary tone")
- Open items: [CLARIFY: ...] for anything unverified
```

**Review mode.** Use this template:

```text
## Verdict
One or two sentences: is it fit for its format, purpose, audience? Biggest lever to improve it.

## Findings (highest impact first)
### Structure
- [issue] -> [why it hurts the reader] -> [suggested fix]
### Substance
- ...
### Sentence-level / style
- [pattern] (e.g. "em-dash overuse, 6 instances") -> [fix], shown once with examples

## Suggested revision (optional)
[A rewritten version, if wanted or if it is the fastest way to show the fix.]
```

## Workflow

### Step 1: Resolve the inputs

Determine the mode and the other inputs (see Inputs). Infer when confident; ask only when a key input is genuinely unclear. In generate mode, when you infer rather than ask, record your read in the *notes* block, not in the deliverable.

### Step 2: Load the rules and the format

Always read `references/universal-rules.md` and `references/ai-patterns.md`. Then load the matching format:

- A simple format is a single file: `references/formats/<format>.md`.
- A format with **completeness levels** is a folder: load the base `references/formats/<format>/<format>.md` plus **exactly one** level file matching the completeness (e.g. `proposal/proposal-floater.md`). Do not load the other levels.

If no format matches, say so ("I don't have a dedicated template for <format> yet, so I'm using the universal rules"), then write with the universal rules and the closest structural pattern. Do not pretend a template exists.

### Step 3: Produce the draft or the review

In **generate**, write to the format template, apply the tone and medium guidance, and suppress the ai-patterns. In **review**, produce findings with the review template, applying each rule only where it fits this format, tone, and audience.

### Step 4: Run the final passes, then present

Run the **anti-hallucination pass** (universal-rules.md A9): classify each specific factual claim as Verified / Inferred / Unknown, and ask about or strip the Inferred and Unknown ones; never invent facts. Then run the **ai-patterns pass**. Present the output in the shape defined under Output.

## Reference files

- `references/universal-rules.md` — always-on rules (incl. the A9 anti-hallucination protocol), conditional rules, and the tone and medium guidance. Read every time.
- `references/ai-patterns.md` — LLM tells to suppress so text does not read as machine-written. Read every time you draft.
- `references/formats/` — per-format templates and rules. Currently supported:
  - `references/formats/proposal/` — internal decision/strategy proposal. Load the base (proposal.md) plus exactly one level file: proposal-floater.md, proposal-onepager.md, or proposal-full.md.
  - `references/formats/raci/` — RACI responsibility matrix (Responsible / Accountable / Consulted / Informed). Load the base (raci.md) plus exactly one level file: raci-prose.md for plain text in Slack or email, or raci-onepager.md for the wiki-page artifact. The base carries the *ownership clause*: the mandatory sections that stop a RACI becoming a "not my job" shield or a blame map.
  - `references/formats/peer-feedback.md` — peer performance feedback (Strengths + Opportunities). Single file; no completeness levels. Collects receiver role, optional role expectations, and optional org values before generating or reviewing SBI-structured feedback items.
  - `references/formats/_TEMPLATE.md` — scaffold for adding a new format (single-file or base+levels).

To grow the library, copy `_TEMPLATE.md`, fill in the template, default axes, format-specific rules, and which conditional rules to relax, then add a line to the supported list above. Build format-by-format; a small set of well-specified formats beats a large set of thin ones.
