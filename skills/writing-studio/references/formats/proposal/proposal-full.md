# Proposal — Full level

Every section at full depth: the real argument for a significant or irreversible decision. Usually a document or wiki page. Read with `proposal.md` (the base) for what each section means and the rules to enforce.

## Goal

Make the complete, decision-ready case. The document stands on its own: a reader can approve or reject without a meeting, and the author's reasoning, trade-offs, and risks are all visible.

## Sections to include

All sections from the base library, at full depth, in this order. Use the template below.

```text
# [Proposal: <the decision being asked for>]

<!-- Optional roles line for a formal decision doc:
Driver: <who owns this> · Approver: <who decides> · Contributors: <who informs it> · Informed: <who needs to know> -->

## TL;DR
A short paragraph (what / so what / now what): what you recommend, why it matters, the decision you want now. A reader who stops here knows the ask and the reason. Then state it precisely:

- **Ask:** [headcount / budget / timeline / direction / resource reallocation / exception]. Be concrete ("1 FTE for 6 months", not "some help").
- **Decision type:** [Two-way door (reversible) / One-way door (hard to undo) / Reversible at cost]. For one-way doors, name the rollback or kill-switch.
- **Decision needed by:** [date], because [reason]. What happens if deferred past that date.

## Problem statement
The situation, why it matters, and why now. Shared facts and assumptions. Include the **baseline**: current-state numbers (today's metric, cost, SLA, headcount) that the rest of the proposal moves.

## Impact of doing nothing
A quantified view of the status quo: what it costs to NOT act (revenue at risk, churn, operational burden, debt compounding, opportunity lost) and how it worsens over time.

## Proposed solution
What specifically you will do and the scope. Name the lead and the top work streams, so the *how* and *who* are not hand-waved.

### Alternatives considered
2-3 genuine options (including "do nothing"), evaluated against the criteria that matter (cost, time, risk, reversibility, fit), and why the recommended option wins. No strawmen.

## Impact and success metrics
Outcomes as **metric = [baseline] → [target] by [date]**, and when you will evaluate. Unknown numbers get `[CLARIFY: ...]`, not invented values.

## Cost, timeline, and return on investment
Effort, headcount, spend, timeline, set against the return. Tag each figure **[known]** or **[estimate]**. Include the **opportunity cost**: what this team stops doing if this starts.

## Ownership and plan
Who owns delivery, major milestones and dates, key dependencies. Name the **steady-state owner** and rough ongoing operational burden (on-call, maintenance) after launch.

### Dependencies and stakeholder alignment
Other teams or external parties needed and their status: [bought-in / consulted / unaware]. Outstanding approval gates. Objections already raised.

## Risks and mitigations
Real, specific risks, each paired with a concrete mitigation. End with:
**Confidence: [X%]. Key unknowns: [list]. If [unknown] proves false, the recommendation likely changes.**

## Appendix (optional)
Short citations and supporting links. Substantive evidence belongs in the body, not buried here.
```

## Depth and shape

- Aim for one to two pages. Several sections (the ask, dependencies, confidence) are one or two lines, not pages; depth goes into problem, solution, alternatives, and impact.
- Dense, complete prose (B4). Use the section library's neutral headings (B5 relaxed for internal readers).

## Quick checklist before presenting

1. Does the TL;DR give the recommendation, the why, the concrete ask, the decision type (one-way vs two-way door), and the decision deadline?
2. Is there a baseline (current-state numbers) and a clear, quantified cost of doing nothing?
3. Are there 2-3 genuine alternatives (including do-nothing), scored honestly?
4. Are success metrics written as baseline → target → date?
5. Are cost/ROI figures tagged [known] vs [estimate], with opportunity cost named?
6. Are dependencies and stakeholder alignment (bought-in / consulted / unaware) listed?
7. Are real risks named, each with a mitigation, plus a confidence level and key unknowns?
8. Is every number Verified? Any unknowns flagged, not faked?
9. Did you run the ai-patterns pass (no em-dash spray, no puffery, varied rhythm)?
