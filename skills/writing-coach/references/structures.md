# Structural Patterns

The shape of a piece of writing matters more than any individual sentence. A misshapen long draft cannot be saved by sentence-level edits — the reader will lose the thread before any clever wording lands. Pick the shape first, then write or review against it.

This file lists the patterns the skill draws from, when each fits, and the minimum scaffolding for each. The skill's default selection logic is in `SKILL.md` Step 2; this file expands the choices and adds alternates for cases where the default does not fit.

## How to choose

Two questions narrow it down quickly:

1. **Is the writing answering a specific question, or telling a story / building an argument?** Answer → use an *answer-first* pattern. Narrative or argument → use a *what / so what / now what* pattern (or a relative).
2. **Who is the reader, and how much of their attention will you actually get?** Less attention (executives, busy peers, scanners) → tighter pyramid, stronger lead. More attention (deep-dive readers, technical reviewers, story readers) → more room to unfold.

If both questions still leave you unsure, default to *answer-first* for technical and business writing and *what / so what / now what* for narratives. These two cover the vast majority of cases.

---

## Pattern 1: Answer-first

**Use when:** the writing answers a question, makes a recommendation, reports a result, or resolves a decision.

**Shape:**

1. **Answer** (one sentence, sometimes two). The reader who stops here has the point.
2. **Reasoning** (1-3 paragraphs). Why this is the answer — the supporting evidence and logic.
3. **Educate further** (optional). Background, caveats, alternatives considered, related context. The reader who wants depth gets it; the reader who wanted the answer is already gone.

**Example shape (status update):**

> We're shifting the launch from Q2 to Q3. Two of the four blocking features slipped, and the customer pilot revealed a data-migration issue that needs another four weeks. The Q3 date assumes the migration fix lands by `2026-06-30`; if it slips again we'll re-evaluate. Background and the full risk list are in the linked doc.

**Failure modes to avoid:**
- Burying the answer under a paragraph of context.
- Hedging the answer ("we *might* shift to Q3") when you actually know.
- Repeating the answer in three different places.

---

## Pattern 2: What / so what / now what (narrative)

**Use when:** the writing tells a story, walks through what happened, or builds an argument over multiple paragraphs. Common for blog posts, retros, project narratives, postmortems, and most long-form internal writing.

**Shape:**

1. **What** — what happened, what was done, what is true. Concrete, specific, ideally with dates and actors.
2. **So what** — why it matters. The insight, consequence, or argument that the *what* supports.
3. **Now what** — what the reader should do, expect, or take away.

The *so what* is where most narratives live or die. A *what* without a *so what* reads as a log; a *so what* without a *what* reads as opinion.

**Example shape (blog post):**

> Last quarter, three teams independently built dashboards on top of the same metrics service (*what*). Each team spent 4-6 weeks on plumbing that was already built next door, and we ended up with three near-identical dashboards that drift out of sync (*so what*). Going forward, new dashboards go through the platform team's intake, and we're documenting the existing service so the next team finds it before they build it again (*now what*).

**Failure modes to avoid:**
- All *what*, no *so what*: the reader finishes asking "and?".
- *So what* without *what*: feels like an unsupported opinion.
- *Now what* that does not follow from the *so what*: feels tacked-on.

---

## Pattern 3: SCIPAB (executive memo)

**Use when:** writing for an executive audience asking for a decision or alignment. Especially good for one-page memos and exec updates.

**Shape:**

1. **Situation** — the stable backdrop the reader already knows.
2. **Complication** — what changed or what is now in tension with the situation.
3. **Implication** (or **I**ssue / **Q**uestion) — the question the reader needs to answer because of the complication.
4. **Position / Answer** — your recommended answer to the question.
5. **Benefit** — what the reader gets by accepting the answer.

**Example shape:**

> *Situation:* We currently route all customer support tickets through Tier-1, then escalate. *Complication:* Ticket volume from the new enterprise segment is 3x our forecast and Tier-1 wait times have doubled. *Question:* How do we keep enterprise SLAs without doubling Tier-1 headcount? *Answer:* Stand up a dedicated enterprise queue with a senior pod of 4 by `2026-Q3`. *Benefit:* protects SLA, contains hiring to a single small pod, and frees Tier-1 to recover wait times within 30 days.

**Failure modes to avoid:**
- Skipping the situation (the exec has to construct it themselves).
- Conflating complication and implication (the reader does not see why the question follows).
- Hiding the answer at the end as if it were a reveal.
- **Showing your work as headings.** SCIPAB is a *thinking pattern*, not a section template. Do not put `**Situation**`, `**Complication**`, etc. as visible bold headings in the final document — those labels are jargon and make the memo feel like a worksheet. Let the structure be implicit; the reader feels the flow without needing the labels.

---

## Pattern 4: Problem → Solution (proposal)

**Use when:** proposing a change, a project, an investment, or a policy. Adjacent to SCIPAB but more space for the solution.

**Shape:**

1. **Problem** — what hurts, who it hurts, how badly.
2. **Goal** — the outcome a good solution would produce, in measurable terms when possible.
3. **Solution** — what you propose, in enough detail to evaluate.
4. **Tradeoffs** — what the solution costs and what it does not solve. (Skip at your peril; readers smell missing tradeoffs.)
5. **Asks** — what you need from the reader to move forward (decision, budget, headcount, deadline).

**Failure modes to avoid:**
- Solution before problem (reader does not know why to care).
- No tradeoffs section (reads as a sales pitch, not a proposal).
- Vague asks ("any thoughts?") that produce no decision.

---

## Pattern 5: Narrative arc (creative)

**Use when:** writing creatively — stories, personal essays, narrative-style blogs that prioritize engagement over scannability.

**Shape (a stripped-down hero's journey):**

1. **Setup** — who, where, what is normal.
2. **Inciting incident** — what disrupts the normal.
3. **Rising action** — what is tried, what fails, what is learned.
4. **Climax** — the turning point.
5. **Resolution** — the new normal, and what changed.

This pattern *deliberately* breaks the answer-first rule: the value is in the unfolding. Use it sparingly in business contexts; use it freely in creative ones.

**Failure modes to avoid:**
- Too long a setup (modern readers leave).
- Climax without stakes (no reason to care about the turning point).
- Resolution that does not follow from the climax (feels arbitrary).
- **Beats as visible H3 headings.** The five beats are *story beats*, not section headings. In most narrative writing — blog posts, personal essays, internal stories — the reader feels the arc without seeing it labeled. Visible "Setup / Inciting Incident / Rising Action / Climax / Resolution" headings make the piece read like a screenplay outline rather than a story. Use these as internal scaffolding only, except in genres that genuinely call for labeled acts (a multi-act feature article, a structured case study).

---

## Pattern 6: Step-by-step (instructional)

**Use when:** the reader needs to *do* something — runbooks, tutorials, checklists, how-to docs.

**Shape:**

1. **Outcome** — what the reader will have done by the end (one sentence).
2. **Prerequisites** — what they need before they start.
3. **Steps** — numbered, imperative, one action per step. Include the expected observation after each meaningful step.
4. **Verification** — how the reader knows they succeeded.
5. **Troubleshooting** — common ways this fails and how to recover.

**Failure modes to avoid:**
- Burying prerequisites in the middle of the steps.
- Steps that bundle multiple actions ("install and configure and start").
- No verification (the reader cannot tell if they succeeded).

---

## Mixing patterns

Long pieces often nest patterns. A blog post might use *narrative arc* overall, with a *problem → solution* section in the middle. An RFC might use *answer-first* at the top (the recommendation) and *problem → solution* in the body. This is fine — pick the outer pattern for the shape of the whole, and let inner sections take the shape that fits their purpose.

When mixing, restate the outer pattern's anchor at the top of each major section so the reader does not lose orientation.
