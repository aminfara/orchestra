# Flow: architecture

From selected requirements to an approved architecture and a breakdown into implementation tasks. Use it after the requirements flow for a new product or a new feature on an existing system. It can also start at phase 3 when scope changed and the architecture still stands.

The architect carries one context through the flow, researching, designing and breaking the work down. The UX design, if the product has one, was approved in the requirements flow and is an input here, so the architect and the product manager do not negotiate while they work. There is one review gate per phase.

If a codebase exists but no current architecture doc, run the understand flow first.

## Phase 1: Selection

**Who:** you, with the user.

**Inputs:** the selected requirements in `<root>/docs/product/prd.md` (the PRD's status column names them), and the existing architecture doc and glossary if they exist. Give the architect their paths; do not open them.

**Produces:** the list of selected requirement IDs in `brief.md`, plus any technical constraints the PRD leaves open that the user can answer.

**Exit criteria:** the selected requirements are explicit, and the user's technical constraints (existing stack, hosting, team skills, must-use or must-avoid) are recorded.

**Checkpoint:** briefing, closing on the open question. Skip it when the PRD and the user's request already settle both.

## Phase 2: Architecture

**Who:** the architect, first with `orchestra:research` through the technical lens, scoped to the choices the requirements leave open, and then with `orchestra:architecture`. It may send bulk reading to subagents that return digests.

**Inputs:** the selected requirements and the rest of the PRD, the PR/FAQ if one exists, the approved UX design, and the existing architecture doc, glossary and ADRs.

The architect designs for the selected requirements, then reads the existing architecture and the remaining unselected requirements to check that the design extends to them without rework. It records where the design stays open on purpose and what it would cost to add the next likely requirements.

**Produces:** `research/technical.md`; the new or updated `<root>/docs/architecture.md`, ADRs under `<root>/docs/adr/`, and `<root>/docs/glossary.md`.

**Exit criteria:** an engineer could start building without asking how the parts fit; every selected requirement traces to the parts that deliver it, and every journey in the UX design can be delivered by them; every one-way-door decision has an ADR with three options; the design names the remaining requirements it was checked against and where it would need to change for them; the architecture and the UX design agree and use the glossary's terms. A change to an existing architecture states what changes and why.

**Checkpoint:** peer check by a fresh architect instance that has seen none of this run's work, briefed as a critic: find where the design breaks, such as under concurrent use, at the edges of the requirements, where it fails to extend to the remaining requirements, or where the architecture cannot deliver a journey in the approved UX design. Give it the architecture, the UX design, the PRD and these criteria, and the ledger details for both authors. Then review gate. The reviewer role takes over this check once it exists.

If the architect or its checker reports that a selected requirement is too costly, conflicts with the existing design, or cannot deliver an approved journey, pause the gate, take the question to the user, and reopen the requirements flow for the affected requirements or the UX design.

## Phase 3: Breakdown

Not built yet; it arrives with M2, the `planning` skill and the `tasks` script. In this version the flow ends when phase 2 is approved.

**Who:** the same architect, with `orchestra:planning`.

**Produces:** for each selected requirement, features and stories with acceptance criteria taken from the requirement's definition of done, dependency edges between stories, and a sequence that shows what can run in parallel, created through `tasks`.

**Exit criteria:** an engineer could start any ready story without asking a question; every definition of done is covered by a story's acceptance criteria.

**Checkpoint:** peer check by the product manager (the stories keep the requirements' intent and the MVP's most important promises), then review gate. This phase can be reopened alone when scope changes.
