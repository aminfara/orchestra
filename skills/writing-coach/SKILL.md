---
name: writing-coach
description: Bimodal writing coach that either writes prose or reviews existing prose so the result is clear, concise, and appropriate to its type, tone, and audience. Load this skill whenever an agent is about to write any piece of prose for a human reader (docs, emails, narratives, blogs, essays, PR descriptions, RFCs, executive briefings, marketing copy, creative writing) OR whenever an agent receives a request to review prose of any length — including near-synonyms like "polish", "critique", "proofread", "tighten", or "sharpen". Prefer this skill over ad-hoc style nitpicking, especially for multi-paragraph or long-form text where context and structure matter as much as individual sentences.
---

# Writing Coach

A bimodal writing coach that helps an agent draft *or* review prose so the result is clear, concise, well-structured, and faithful to the writer's intent, type, tone, and audience.

## Overview

This skill teaches an agent two modes for working on prose: **write** (help compose or expand a draft) and **review** (give holistic, contextual feedback on existing text). In both modes the agent treats the writing as a whole — not a stream of disconnected paragraphs — and applies a small set of durable principles (clarity, concision, structure, accurate evidence, appropriate voice) with judgment rather than as rigid rules.

The skill exists because earlier rule-based reviewers worked well only paragraph-by-paragraph and produced rigid, conflicting findings on long text generated in one shot by an AI. Reviewers without context will demand quantification of an anecdote, force active voice into a methods passage, or flag a deliberate stylistic choice as a violation. This skill keeps the same time-tested rules but layers context on top: the writing's *type* (technical, business, creative), *tone* (formal, informal, persuasive, humorous), *purpose* (answer-a-question vs. narrative), and *audience* (executive, peer engineer, customer, general reader). Rules apply only when the context warrants them, and when they conflict, clarity for the intended reader wins.

A successful invocation produces one of two artifacts. In **write** mode: a draft (or revision) that is structured for its purpose, uses concrete language, sustains the requested tone, and explains the principles applied. In **review** mode: a prioritized, deduplicated set of findings grouped by impact (structure → substance → sentence-level), each with the *why* and a suggested rewrite, plus an optional revised version of the whole text. The outcome — regardless of writing type — is text the intended reader can understand on first read.

## When to use this skill

Load this skill whenever an agent is about to produce, expand, edit, or review prose meant for a human reader. Concrete trigger contexts include:

- The agent is drafting a document longer than a few sentences (RFCs, design docs, blog posts, emails, executive updates, PR descriptions, release notes, status reports, narratives, proposals, marketing copy, creative pieces).
- The user asks the agent to "review", "edit", "critique", "tighten", "proofread", "improve", or "make more concise/clear/engaging" any existing text.
- The agent is asked to convert a bullet outline or notes into prose, or to summarize a long document into a shorter one.
- The user mentions a target tone or audience ("make this sound more formal", "an exec version of this", "explain this to a new hire").
- The agent is producing output that will be read by people other than the requesting user (customer-facing copy, public docs, team-wide comms).

### When NOT to use this skill

- Pure code generation, code comments shorter than a sentence, or commit messages where house conventions already cover style.
- Structured data the agent is producing for another machine (JSON, YAML, CSV) — there is no human reader to optimize for.
- One-off chat replies and acknowledgements (a one-line "done" does not need a coach).
- Translation or transcription tasks where the source text's style must be preserved verbatim.
- Tasks where another, narrower skill already owns the format (e.g., a dedicated commit-message skill, a dedicated changelog skill).

## Constraints

- **Preserve the writer's intent, voice, and stated constraints.** Never silently rewrite meaning, invent facts, or replace the writer's voice with a generic one. Honor any stated length target as a hard upper bound — if the content cannot fit, ask which sections to compress rather than overflowing. When unsure what the writer meant, ask or mark `[CLARIFY: …]` rather than guess — but use inline markers sparingly (see Principle 4.1 in `references/rules.md`); for color details, pick one plausible choice and list assumptions in the Notes sidecar instead.
- **Apply rules with context, not rigidly.** Every principle in `references/rules.md` is conditional on writing type, tone, audience, and purpose. If a rule would hurt clarity or distort meaning in a given passage, skip it and say why.
- **Findings must be prioritized and deduplicated.** In review mode, group findings by impact (structure → substance → sentence-level) and suppress duplicates of the same issue across many paragraphs; report the pattern once with examples.
- **Never produce or invent quantification.** Quantify only what the source supports. For anecdotes, future work, or claims with no underlying data, prefer concrete language over fabricated numbers, and call out the gap rather than filling it.

## Inputs

Before drafting or reviewing, gather (or infer with a one-line confirmation) these four context dimensions. They drive which rules apply and how strictly.

- **mode** — `write` (compose/expand a draft) or `review` (give feedback on existing text). If the user provides text and asks to "improve", default to `review` and offer to follow up with a `write`-mode rewrite.
- **type** — `technical` (docs, RFCs, runbooks, postmortems), `business` (status updates, exec memos, proposals, emails), or `creative` (blogs, narratives, marketing copy, fiction). When ambiguous, infer from the text and confirm in one line.
- **tone** — `formal`, `informal`, `persuasive`, `humorous`, `neutral`, or a short free-form description (e.g., "warm but direct"). Default to `neutral` for technical, `formal` for business, and let the source dictate for creative.
- **purpose** — `answer` (the writing answers a specific question) or `narrative` (the writing tells a story or builds an argument). This selects the structural pattern in `references/structures.md`.
- **audience** (optional but encouraged) — who will read this (e.g., "VP of engineering", "new hire on day one", "external customers"). When provided, calibrate vocabulary and assumed knowledge to that reader.

If the user supplies only the text, infer all four dimensions, state your inference in one line at the top of the output, and proceed. Do not block on confirmation for short tasks.

## Output

Output shape depends on `mode`. Use these exact templates so downstream agents can parse the result.

The deliverable is the prose itself — start the output with the *natural title* of the piece (or no title if a short email), not with a `## Draft` wrapper heading. The `## Notes` block is a sidecar for the calling agent, separated from the deliverable by a `---` divider, and exists so a downstream agent can verify what shape and principles were used. A human reader of the deliverable should see only the prose; everything below the divider is meta.

**Write mode** produces:

```markdown
<the natural H1 title of the piece, or no title for short forms>

<the prose itself, structured per the purpose>

---

## Notes (for the calling agent — not part of the deliverable)
- Type / Tone / Purpose / Audience: <inferred or supplied>
- Structure used: <e.g., "answer-first", "what / so what / now what", "SCIPAB">
- Principles applied: <2-5 short bullets — only the ones that actually shaped the draft>
- Open questions or assumptions made: <list, or "none">
```

**Review mode** produces:

```markdown
## Summary
<2-4 sentences: what the piece does well, the single biggest improvement opportunity, and whether the structure fits the purpose>

## Findings (prioritized)
### Structure
- <finding>: <why it matters for this audience/purpose> — <suggested shape of the fix>
### Substance
- <finding>: <why> — <suggested fix>
### Sentence-level (patterns, not every instance)
- <pattern, e.g., "passive voice in 6 sentences in §3">: <why> — <one rewrite example, plus "apply same pattern to the rest">

## Optional revision
<a revised version of the whole text, only if the user asked for one or the review surfaced enough sentence-level issues that a rewrite is faster than a list>
```

Findings should number in the single digits for short pieces and low double digits for long ones. If a rule does not fire on this text, omit it — never pad the report.

## Workflow

### Step 1: Establish context

Read the user's request and any supplied text in full before doing anything else. Identify the four context dimensions in `## Inputs` (mode, type, tone, purpose, plus audience if given). When a dimension is missing, infer it from the text and state your inference in one line; do not ask a question for every dimension on short tasks. When something genuinely cannot be inferred (e.g., the audience for an internal memo with no signals), ask one targeted question and proceed once answered.

If `mode = review` and the text is longer than a few paragraphs, also do a fast first pass for *structure and purpose fit* before looking at any sentences. Most high-leverage feedback for long AI-generated text lives at the structural level, and sentence-level findings made before reading the whole thing tend to conflict with each other.

### Step 2: Select the structural pattern

Pick the structure that matches `purpose`:

- **answer** → answer-first: lead with the answer, then explain the reasoning, then educate further (background, caveats, related context). The reader who only reads the first sentence still gets the answer.
- **narrative** → what / so what / now what: state what is happening or what was done, then why it matters, then what the reader should do or expect next. For persuasive narratives, the "so what" carries the argument.

`references/structures.md` documents both patterns plus alternatives (SCIPAB for executive memos, problem-solution for proposals, hero's journey for stories) and when to use each. Read it when the default patterns do not fit.

### Step 3: Apply the principles with context

Open `references/rules.md` and apply the principles that fit this text's type, tone, audience, and purpose. The reference file groups principles into clarity, concision, structure, evidence, and voice, and — for each — lists when the principle applies, when it does NOT, and how to soften it for non-technical writing. When two principles conflict (e.g., active voice vs. focusing on the recipient of an action in a methods passage), prefer the one that serves the reader's understanding for this audience.

For tone and writing-type-specific guidance (formal vs. informal vs. persuasive vs. humorous; technical vs. business vs. creative), open `references/tones.md` and use it to calibrate vocabulary, sentence length, and structural choices. Do not flatten a deliberate creative voice into neutral prose, and do not let an informal blog post drift into legalese.

To avoid the generic, puffy register that AI-generated prose tends toward — overused vocabulary, empty `-ing` clauses, promotional adjectives, decorative formatting — also consult `references/ai-patterns.md` once per draft or review and remove patterns that fire.

### Step 4: Produce the output

In **write** mode, draft (or revise) the text using the chosen structure and the principles that survived Step 3. Mark anything the source does not support with `[CLARIFY: <what is missing>]` rather than inventing it. Then fill in the `## Draft` and `## Notes` template from `## Output`.

In **review** mode, collect findings as you read, then before writing the report: deduplicate (collapse repeated instances of the same issue into one pattern finding with examples), prioritize (structure → substance → sentence-level), and drop any finding that does not change the reader's experience. Then fill in the `## Summary`, `## Findings`, and (if asked) `## Optional revision` template from `## Output`.

In both modes, before returning the result, do a deliberate re-read pass:

1. Would the intended audience understand this on the first read? If not, fix it before returning.
2. Open `references/ai-patterns.md` and scan for puffery vocabulary, empty `-ing` clauses, overused AI vocabulary, em-dash overload, and formulaic conclusions. Count instances; if any pattern appears more than once, rewrite to remove it.
3. Count `[CLARIFY: …]` markers in the prose. If there are more than 2-3 in a piece under 1000 words, most are probably color details — convert all but the load-bearing ones into a single "assumptions made" line in the Notes sidecar.
4. Check the deliverable against the requested length. If you are over the upper bound, compress the lowest-information section before returning.

### Step 5: Offer the natural next step, then stop

After returning the output, offer exactly one follow-up appropriate to what just happened, then stop and wait for the user's next message. Examples: after `review`, offer "want me to apply these as a rewrite?"; after `write`, offer "want a shorter or longer version, or a different tone?". One offer per turn, then control returns to the user — the skill never re-invokes itself.

## Reference files

- `references/rules.md` — The full principle catalog (clarity, concision, structure, evidence, voice) with "when this applies / when it does not / how to soften" for each. Read this in Step 3.
- `references/structures.md` — Structural patterns (answer-first, what / so what / now what, SCIPAB, problem-solution, narrative arc) and how to choose between them. Read this in Step 2 when the default does not fit.
- `references/tones.md` — Calibration guidance for writing type (technical / business / creative) and tone (formal / informal / persuasive / humorous / neutral). Read this in Step 3 to keep voice consistent.
- `references/ai-patterns.md` — Specific patterns AI-generated prose falls into (overused vocabulary, empty `-ing` clauses, promotional adjectives, decorative formatting) and how to remove them. Read this once per draft or review.
