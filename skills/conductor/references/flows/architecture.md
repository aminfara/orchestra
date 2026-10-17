# Flow: architecture

From selected requirements to an approved architecture and a breakdown into stories in the task store. Use it after the requirements flow for a new product or a new feature on an existing system. It can also start at phase 3 when scope changed and the architecture still stands.

The architect carries one context through the flow, researching, designing and breaking the work down. The UX design, if the product has one, was approved in the requirements flow and is an input here, so the architect and the product manager do not negotiate while they work. There is one review gate per phase.

Before phase 3, make sure `<root>/.orchestra/config.toml` exists. If it does not, write it with a `[tasks]` table (`adapter = "git"`, `branch = "orchestra/tasks"`), and ask the user once whether the board should be shared across machines through a remote; if so, add `remote = "<name>"`.

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

**Checkpoint:** peer check by a fresh architect instance that has seen none of this run's work, briefed as a critic: find where the design breaks, such as under concurrent use, at the edges of the requirements, where it fails to extend to the remaining requirements, or where the architecture cannot deliver a journey in the approved UX design. Give it the architecture, the UX design, the PRD and these criteria, and the ledger details for both authors. Then review gate. This check stays with an architect rather than the reviewer, because judging a design needs the whole-system view; the reviewer judges changes to code.

If the architect or its checker reports that a selected requirement is too costly, conflicts with the existing design, or cannot deliver an approved journey, pause the gate, take the question to the user, and reopen the requirements flow for the affected requirements or the UX design.

## Phase 3: Breakdown

**Who:** the same architect, resumed, with `orchestra:planning` and `orchestra:tasks`.

**Inputs:** the approved architecture, ADRs and glossary, the selected requirements, and the approved UX design. The architect already holds them; name only the project root for the task store and the run folder for `plan.md`.

**Produces:** features and stories in the task store, each story with acceptance criteria taken from the requirements' definitions of done, its milestone and its blocking edges; `plan.md` in the run folder with the MVP scope in and out, the milestones and what each demonstrates, and the reasoning behind the sequence.

**Exit criteria:** an engineer could start any ready story without asking a question; every selected requirement's definition of done is covered by some story's acceptance criteria; the first milestone ends in something the user can see working; blocking edges are real dependencies, including stories that would change the same files; `tasks ready` lists the stories the plan says start first.

**Checkpoint:** peer check by a fresh product manager instance, briefed as a critic from the customer's side: do the stories keep the requirements' intent, do the acceptance criteria check what the definitions of done promise, and does the first milestone show the MVP's most important promise? Give it `plan.md`, the PRD, the UX design, the project root so it can read the board with `tasks list` and `tasks show`, and the ledger details for the architect. Then review gate.

This phase can be reopened alone when scope changes: resume the architect if it is still current, or start a fresh one from the architecture docs and `plan.md`, and brief it with the changed requirements. It edits, adds or drops stories rather than rebuilding the board.

## After the gates

The breakdown is the input to the build flow. Offer it, and tell the user which stories `tasks ready` lists for the first milestone.
