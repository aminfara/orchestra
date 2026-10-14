# Flow: new product

From an idea to an approved architecture and UX design, and later to a built and accepted MVP (minimum viable product). Use it when the user wants to build something that does not exist yet, with no codebase to start from.

The flow works backward from the customer to the system. The product manager carries one context from market research through the PR/FAQ and the requirements to the UX design. The architect joins once the requirements exist, and carries one context from checking them through technical research to the architecture. Resume each instance from phase to phase rather than starting fresh. Through phase 6 there are three briefings and three review gates.

Phases 7 to 9 (roadmap, build, acceptance) are not built yet. In this version the flow ends when phase 6 is approved.

## Phase 1: Intake

**Who:** you, with the user, using `orchestra:briefing`.

**Produces:** `brief.md` in the run folder, with these sections: the problem, from the user's side; the target user, specific enough that you could find one; why now; constraints (time, money, people, must-use or must-avoid); success signals the user could observe; non-goals.

**Exit criteria:** every section is filled from the user's answers or marked as an assumption the user accepted; a reader who was not in the conversation knows what is being built, for whom, and what is ruled out.

**Checkpoint:** briefing. It ends with the open question the briefing skill closes on, not with a separate confirmation.

## Phase 2: Discovery

**Who:** the product manager, with `orchestra:research`, through the market and user lenses.

**Inputs:** `brief.md`.

**Produces:** `research/market.md`, covering who else solves the problem and how, and who has it and how they cope today, ending with open questions for the user.

**Exit criteria:** the document answers the questions its brief set; every factual claim carries a source or is marked as inference; open questions are phrased as decisions the user can make.

**Checkpoint:** peer check by a fresh product manager instance, briefed as a critic. Keep this critic for phase 4.

## Phase 3: Findings

**Who:** you, with the user.

**Produces:** an updated `brief.md`, and the user's decisions in the run log.

**Exit criteria:** every open question from the report is answered, deferred by the user, or delegated to a role; the brief reflects what discovery changed.

**Checkpoint:** briefing, built from the report's questions and recommendations.

## Phase 4: Working backwards

**Who:** the same product manager, with `writing-studio` in its PR/FAQ format.

**Inputs:** `brief.md`, `research/market.md`.

**Produces:** `<root>/docs/product/prfaq.md`, with the rough wireframes the format calls for.

**Exit criteria:** the press release keeps to the brief's problem, user and non-goals; the Internal FAQ names the hard problems, the promises the product manager judges expensive or uncertain to deliver, and what success would be measured by; a reader who was not in the session can follow it.

**Checkpoint:** peer check by the critic from phase 2, resumed with the PR/FAQ and these criteria, then review gate.

## Phase 5: Requirements

**Who:** you, with the user, then the same product manager.

**Inputs:** for the product manager, `brief.md` and `<root>/docs/product/prfaq.md`.

**Produces:** first, a requirements section in `brief.md` from a briefing on what the PR/FAQ leaves open: expected users and load, responsiveness, availability, offline use, accessibility, data (what is stored, how sensitive, how long it is kept), budget, hosting and stack preferences. Ask the product manager for the questions that matter most before you start, and brief from its answer. Then `<root>/docs/product/requirements.md` from the product manager, with these sections: the functional requirements, each traced to the PR/FAQ promise it serves; the non-functional requirements; the MVP's scope, in and out; the success criteria, each one something acceptance could check; and the constraints the design must respect.

**Exit criteria:** an architect could design the system from this document and the PR/FAQ without asking what the product must do; every MVP promise in the PR/FAQ has requirements, and every requirement serves a promise or a constraint; each requirement and success criterion can be checked.

**Checkpoint:** briefing; then peer check by a fresh architect instance, as the document's next consumer, which continues into phase 6; then review gate.

## Phase 6: Architecture and UX

**Who:** the same architect, first with `orchestra:research` through the technical lens and then with `orchestra:architecture`. In parallel, when the product has a user interface, the same product manager, with `orchestra:ux-design`. Give each the other's agent ID; the UX design and the architecture constrain each other.

**Inputs:** for both, `<root>/docs/product/requirements.md` and `<root>/docs/product/prfaq.md`; for the architect, the requirements section of `brief.md`.

**Produces:** `research/technical.md`, scoped to the choices the requirements and constraints leave open; `<root>/docs/architecture.md`, ADRs under `<root>/docs/adr/`, and `<root>/docs/glossary.md` from the architect; `<root>/docs/product/ux/` from the product manager.

**Exit criteria:** an engineer could start building without asking how the parts fit; every requirement traces to the parts that deliver it, and every MVP promise to a journey in the UX design; every one-way-door decision has an ADR with three options; the UX design covers the main journeys, including first use, empty states and errors, and meets the usability and accessibility bars in its skill; the architecture and the UX design agree with each other and use the glossary's terms.

**Checkpoint:** peer check by a fresh architect instance, which has seen none of this run's work, briefed as a critic: its job is to find where the design breaks, such as under concurrent use, at the edges of the requirements, or where the architecture and the UX design disagree. Give it both artifacts, the requirements, the PR/FAQ and these criteria, and the ledger details for both authors. Then one review gate for both artifacts. The reviewer role takes over this check once it exists.
