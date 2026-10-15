# Flow: requirements

From source documents to a living product requirements document (PRD) with a prioritized, checkable MVP scope. Use it after the idea flow, or whenever the user has a PR/FAQ, market research or another idea document, or wants to add a feature to an existing product. A new feature needs this flow as much as a new product does.

The product manager carries one context through the flow, from reading the sources to the UX design, so the research behind each requirement stays with whoever sizes it. There is one briefing and two review gates.

The PRD is a living document at `<root>/docs/product/prd.md`. If it exists, this flow extends it in place and does not rewrite it; if not, it creates it.

## Phase 1: Intake

**Who:** you, with the user, using `orchestra:briefing`; first ask the product manager for the questions that matter most, and brief from its answer.

**Inputs:** the source documents the user names (a PR/FAQ, market research, other idea documents), and the existing PRD and architecture doc if they exist. Give the product manager their paths; do not open them.

**Produces:** the requirements section of `brief.md`: how much to build now (appetite), expected users and load, responsiveness, availability, offline use, accessibility, data (what is stored, how sensitive, how long it is kept), budget, hosting and stack preferences. Skip what an existing PRD or architecture doc already settles.

**Exit criteria:** the product manager has what it needs to write requirements without guessing; every item is answered, assumed with the user's consent, or deferred.

**Checkpoint:** briefing, closing on the open question.

## Phase 2: Requirements

**Who:** the product manager, with `writing-studio` for the PRD, `orchestra:estimation` for effort and risk, and `orchestra:feasibility` for any requirement estimation marks unknown. Estimation uses the existing architecture doc and glossary when there are any. A requirement whose size could move the cut line and cannot be settled on paper goes to a spike subagent with one question, which returns a short digest.

**Produces:** the new or updated `<root>/docs/product/prd.md`, with these sections:

- Goals and success measures: what outcome the product or feature should produce and how it will be observed.
- Requirements. Each has a stable ID, its what, its why (the customer need or PR/FAQ promise it serves), a definition of done that acceptance can check, its value to the customer, its effort and risk from estimation, and its status (proposed, selected, built, dropped).
- Non-functional requirements and constraints the design must respect.
- Priority and MVP scope: requirements ranked by customer value against ease of implementation, with the MVP's cut line and what is out.
- Open questions.

**Exit criteria:** an architect could design the system from the PRD without asking what must be built or why; every requirement has a what, a why and a checkable definition of done; every promise in scope in the PR/FAQ has requirements and every requirement serves a promise or a constraint; the ranking shows its reasoning, and expensive but valuable requirements are marked as such rather than hidden.

**Checkpoint:** peer check by a fresh architect instance, as the document's next consumer, briefed as a critic: can it design from this, is any definition of done not checkable, and is any size badly off given the architecture? Then review gate. At the gate the user confirms the MVP cut line and which requirements are selected for the architecture flow.

## Phase 3: UX design

Skip this phase when the product has no user interface.

**Who:** the same product manager, with `orchestra:ux-design`.

**Inputs:** the selected requirements and the rest of the PRD, the PR/FAQ if one exists, and the existing architecture doc for constraints such as what can happen in real time or offline.

**Produces:** `<root>/docs/product/ux/`, covering the selected requirements only.

**Exit criteria:** the UX design covers the main journeys, including first use, empty states and errors, and meets the usability and accessibility bars in its skill; every selected requirement with a user-facing part traces to a journey; it uses the glossary's terms.

**Checkpoint:** peer check by a fresh product manager instance briefed as a critic, then review gate. The architecture flow's checker later tests this design against the architecture; a conflict it finds returns here as a finding.

## After the gates

The selected requirements are marked in the PRD and are the input to the architecture flow. If the architecture flow later finds a selected requirement too costly or in conflict with the existing design, the conductor returns here and reopens only the affected requirements.
