# Format: Proposal (base)

A proposal argues for a decision: do this, fund this, build this, choose this option. It exists to get a "yes" (or a well-reasoned "no") from a specific decision-maker.

This is an **internal decision/strategy proposal**. The audience is internal: a manager, a leadership group, a review forum. The goal is a decision, not a sale. The style is a decision document or design-doc register: clear prose, an explicit recommendation, honest trade-offs, and pre-empted objections.

> Not for selling to a prospective customer, and not for pitching a new product vision. For a product/vision pitch, use the PR/FAQ format — a different shape with a different job.

This is the **base** file: what a proposal is, when to use it, the default axes, the canonical section library, and the rules. It does not prescribe how much to write. That depends on **completeness level** (below). Always load this base plus exactly one level file.

## When to use vs. adjacent formats

- **Proposal** (this format): you want a specific decision from internal stakeholders, backed by problem → solution → impact → cost → plan → risks.
- **PR/FAQ** (separate format): you are pitching a new product or initiative as a vision, working backward from the customer.
- **RFC / design doc** (separate format): the decision is primarily technical and the emphasis is on the design and its alternatives.

If the request is "convince leadership to do X / fund X / pick X", this format is right.

## Completeness levels

A proposal is an idea at a stage of maturity, and the same idea can be written at different depths. The lifecycle runs both ways: a quick floater can grow into a full doc, and a full doc can be summarized back down.

- **Floater** (`proposal-floater.md`) — a few sentences to test interest. The idea, why it matters, and the ask. Often a chat message or short email, written before any doc exists.
- **One-pager** (`proposal-onepager.md`) — a tight written pitch: recommendation, problem, solution, rough cost and risk. Enough to take a small decision or to justify writing the full version.
- **Full** (`proposal-full.md`) — every section at full depth. The real argument for a significant or irreversible decision.

Resolve the level from the request (see SKILL.md). Load the base + the matching level file only; do not pull all three into context.

## Default axes

- **Purpose:** persuade / recommend / secure a decision.
- **Tone:** authoritative and neutral, anchored to evidence. Confident but not promotional.
- **Medium:** varies by level. Floater → chat or short email; one-pager → email or wiki; full → document or wiki page. Medium is an overlay (length and packaging); it does not change what a proposal is. A full proposal can live in a long email; a floater can live in a doc comment.
- **Audience:** name the actual decision-maker(s) and write to their priorities and prior knowledge.

## Section library

Every section a proposal can contain, defined once. Level files say **which sections to include and at what depth**; they do not redefine meaning. Section names can be adapted to the topic; keep the logical flow.

- **TL;DR / recommendation + ask** — what / so what / now what: what you recommend, why it matters, the decision you want now. Then state it precisely: the concrete **ask** (headcount / budget / timeline / direction / exception, with numbers — "1 FTE for 6 months", not "some help"), the **decision type** (two-way door / one-way door / reversible at cost; for one-way doors name the rollback), and the **decision needed by** date and what happens if deferred.
- **Problem statement** — the situation, why it matters, why now. Shared facts and assumptions. Include the **baseline**: current-state numbers (today's metric, cost, SLA, headcount) that the rest of the proposal moves. Without a baseline, impact claims are unanchored.
- **Impact of doing nothing** — a quantified view of the status quo: what it costs to NOT act (revenue at risk, churn, operational burden, debt compounding, opportunity lost) and how it worsens over time. The forcing function for the decision.
- **Proposed solution** — what specifically you will do and the scope. Name the lead and top work streams so the *how* and *who* are not hand-waved.
- **Alternatives considered** — 2-3 genuine options (including "do nothing"), scored against the criteria that matter (cost, time, risk, reversibility, fit), and why the recommended option wins. No strawmen, no single-option theater.
- **Impact and success metrics** — outcomes as **metric = [baseline] → [target] by [date]**, plus when you will evaluate. Unknown numbers get `[CLARIFY: ...]`, not invented values.
- **Cost, timeline, and return on investment** — effort, headcount, spend, timeline, set against the return. Tag each figure **[known]** or **[estimate]**. Include **opportunity cost**: what this team stops doing if this starts.
- **Ownership and plan** — who owns delivery, major milestones and dates, key dependencies. Name the **steady-state owner** and rough ongoing operational burden (on-call, maintenance) after launch.
- **Dependencies and stakeholder alignment** — other teams or parties needed and their status ([bought-in / consulted / unaware]), outstanding approval gates, objections already raised. Surface hidden blockers.
- **Risks and mitigations** — real, specific risks (not platitudes), each with a concrete mitigation. Close with a posture line: **Confidence: [X%]. Key unknowns: [list]. If [unknown] proves false, the recommendation likely changes.**
- **Appendix (optional)** — short citations and supporting links. Substantive evidence belongs in the body where the decision-maker will see it, not buried here.

## Rules for this format

- **Enforce:**
  - A1 (lead with the recommendation — the TL;DR is the BLUF).
  - A9 (anti-hallucination — a proposal lives or dies on credible facts; never invent metrics, costs, or ROI).
  - B1 (quantify impact — real numbers on impact, cost, ROI).
  - B3 (strict answer-first — the TL;DR states the ask first).
  - B2 (forward-looking framing), except state the cost-of-inaction plainly.
- **Relax:**
  - B5 (persuasive section titles) — internal readers want neutral, scannable headings.
- **Watch:**
  - The decision-maker must know exactly what they are approving: the concrete ask, the decision type (reversibility), and the deadline.
  - Anchor everything to a baseline; without current-state numbers, impact and ROI are unverifiable.
  - Do not fabricate numbers. Unknown figures get `[CLARIFY: ...]`; tag others [known] or [estimate].
  - Keep "alternatives considered" honest: real options scored against criteria.
- **Length:** as short as the decision allows; the level file sets the target. A short proposal that earns a yes beats a long one that goes unread.
