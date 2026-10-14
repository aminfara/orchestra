# Flow: new product

From an idea to an approved architecture and UX design, and later to a built and accepted MVP (minimum viable product). Use it when the user wants to build something that does not exist yet, with no codebase to start from.

The flow has three briefings and, through phase 6, two review gates. The product manager carries one context from market research through the PR/FAQ to the UX design, and the architect carries one from technical research through the architecture. Resume each instance from phase to phase rather than starting fresh.

Phases 7 to 9 (roadmap, build, acceptance) are not built yet. In this version the flow ends when phase 6 is approved.

## Phase 1: Intake

**Who:** you, with the user, using `orchestra:briefing`.

**Produces:** `brief.md` in the run folder, with these sections: the problem, from the user's side; the target user, specific enough that you could find one; why now; constraints (time, money, people, must-use or must-avoid); success signals the user could observe; non-goals.

**Exit criteria:** every section is filled from the user's answers or marked as an assumption the user accepted; a reader who was not in the conversation knows what is being built, for whom, and what is ruled out.

**Checkpoint:** briefing. The user confirms the brief.

## Phase 2: Discovery

**Who:** the product manager (market and user lenses) and the architect (technical lens), in parallel, each with `orchestra:research`. Give each its own research questions, and each other's agent IDs as `references/briefing-roles.md` describes, so they can compare notes directly.

**Inputs:** `brief.md`.

**Produces:** `research/market.md` from the product manager, covering who else solves the problem and how, and who has it and how they cope today. `research/technical.md` from the architect, covering candidate technologies, their maturity, and the risks the product's hard parts carry. Each ends with open questions for the user.

**Exit criteria:** each document answers the questions its brief set; every factual claim carries a source or is marked as inference; open questions are phrased as decisions the user can make; where the two documents disagree, the disagreement is named.

**Checkpoint:** peer check. Each role checks the other's research, resumed with the other document and these criteria.

## Phase 3: Findings

**Who:** you, with the user.

**Produces:** an updated `brief.md`, and the user's decisions in the run log.

**Exit criteria:** every open question from both reports is answered, deferred by the user, or delegated to a role; the brief reflects what discovery changed.

**Checkpoint:** briefing, built from the two reports' questions and recommendations.

## Phase 4: Working backwards

**Who:** the same product manager, with `orchestra:writing-studio` in its PR/FAQ format.

**Inputs:** `brief.md`, `research/market.md`, `research/technical.md`.

**Produces:** `<root>/docs/product/prfaq.md`, with the rough wireframes the format calls for.

**Exit criteria:** the press release keeps to the brief's problem, user and non-goals; every customer promise is feasible according to the technical research, or the Internal FAQ names it as a risk; the Internal FAQ names the hard problems and what success would be measured by; a reader who was not in the session can follow it.

**Checkpoint:** peer check by the same architect, resumed with the PR/FAQ and these criteria, then review gate.

## Phase 5: Technical intake

**Who:** you, with the user.

**Produces:** a technical section in `brief.md`: stack preferences, hosting, budget, data (what is stored, how sensitive, how long it is kept), and non-functional requirements (expected users, responsiveness, availability, offline use, accessibility).

**Exit criteria:** each item is decided by the user or explicitly delegated to the architect.

**Checkpoint:** briefing. Ask the architect for the questions that matter most for its design before you start, and brief from its answer.

## Phase 6: Architecture and UX

**Who:** the same architect, with `orchestra:architecture`. In parallel, when the product has a user interface, the same product manager, with `orchestra:ux-design`. Give each the other's agent ID; the UX design and the architecture constrain each other.

**Inputs:** for both, `brief.md` and `<root>/docs/product/prfaq.md`; for the architect, `research/technical.md`; for the product manager, `research/market.md`.

**Produces:** `<root>/docs/architecture.md`, ADRs under `<root>/docs/adr/`, and `<root>/docs/glossary.md` from the architect; `<root>/docs/product/ux/` from the product manager.

**Exit criteria:** an engineer could start building without asking how the parts fit; every PR/FAQ promise in the MVP traces to the parts that deliver it and to a journey in the UX design; every one-way-door decision has an ADR with three options; the UX design covers the main journeys, including first use, empty states and errors, and meets the usability and accessibility bars in its skill; the architecture and the UX design agree with each other and use the glossary's terms.

**Checkpoint:** peer check by a fresh architect instance, which has seen none of this run's work, briefed as a critic: its job is to find where the design breaks, such as under concurrent use, at the edges of the PR/FAQ's promises, or where the architecture and the UX design disagree. Give it both artifacts, the brief, the PR/FAQ and these criteria, and the ledger details for both authors. Then one review gate for both artifacts. The reviewer role takes over this check once it exists.
