# Flows

Part of the [Orchestra plan](README.md). The conductor picks a flow from the request's type, and each flow sets the ceremony that type needs. Roles are described in [Roles and craft skills](roles-and-skills.md); "the same instance" means the conductor resumes the agent from the earlier phase instead of starting a fresh one.

## Flows from idea to tasks

Three flows chain together, and context boundaries follow information rather than job titles (see [Roles and craft skills](roles-and-skills.md)). Each ends on a reviewed artifact that the next one takes as input, so the user can enter at any of them with documents already in hand: an idea, a PR/FAQ or other source documents, or a PRD with selected requirements. New products are rare and ideas are common, and an idea may end at the first flow. The same flows serve a new feature on an existing system.

### Idea

Question: is this idea worth building? The product manager carries one context throughout.

| Phase | Who | Produces | Checkpoint |
| --- | --- | --- | --- |
| 1. Intake | conductor with the user | `brief.md`: problem, target user, why now, constraints, success signals, non-goals, whether the idea is novel | Briefing, closing with an open "anything else to add?" question |
| 2. Market research and feasibility | product manager; one subagent finds the three major alternatives, one subagent per alternative studies it, and the product manager synthesizes common ground, gaps and missing features customers want; for a novel idea, the product manager then runs a feasibility check in the same context | `research/market.md`; `research/feasibility.md` for a novel idea | Peer check by a fresh product manager as a critic |
| 3. Findings | conductor with the user | updated brief; decisions in the run log, including whether to go on | Briefing |
| 4. Working backwards | the same product manager | `docs/product/prfaq.md`, with rough wireframes | Peer check by the phase 2 critic, then review gate; the user decides to go on, park or drop the idea |

### Requirements

Question: what exactly should be built first, how big is each piece, and how will we know it is done? The product manager carries one context from reading the sources to the UX design. It also runs for a new feature on an existing product.

| Phase | Who | Produces | Checkpoint |
| --- | --- | --- | --- |
| 1. Intake | conductor with the user, from the questions the product manager asks first | requirements section of the brief: appetite, load, availability, offline, accessibility, data, budget, hosting, stack | Briefing |
| 2. Requirements | product manager, sizing each requirement with the estimation skill (using the existing architecture doc if there is one) and checking feasibility where size is unknown; a spike subagent for a question that could move the cut line | `docs/product/prd.md`, a living document: goals and success measures; requirements, each with a stable ID, what, why, definition of done, customer value, effort and risk, status; non-functional requirements; ranking by value against ease; MVP cut line | Peer check by a fresh architect as the next consumer, then review gate where the user confirms the cut line and selects requirements |
| 3. UX design (if there is a user interface) | the same product manager | `docs/product/ux/` for the selected requirements | Peer check by a fresh product manager as a critic, then review gate |

The PRD is updated in place. Source documents (PR/FAQ, market research, other idea documents) are translated into it rather than duplicated.

### Architecture

Question: how do we build the selected requirements so the next ones fit? The architect carries one context and starts from the approved PRD and UX.

| Phase | Who | Produces | Checkpoint |
| --- | --- | --- | --- |
| 1. Selection | conductor with the user | selected requirement IDs and technical constraints in the brief | Briefing, skipped when the PRD and the request settle both |
| 2. Architecture | architect: technical research scoped to the open choices, then the design, checked against the existing architecture and the remaining requirements, three options for every one-way-door decision | `research/technical.md`, `docs/architecture.md`, `docs/adr/`, glossary | Peer check by a fresh architect as a critic that also tests the design against the approved UX (until the reviewer role exists), then review gate |
| 3. Breakdown (M2) | the same architect | features and stories per selected requirement, with acceptance criteria from the definitions of done, dependency edges, sequence, through `tasks` | Peer check by the product manager, then review gate; can be reopened alone when scope changes |

A selected requirement that proves too costly, conflicts with the existing design, or cannot deliver an approved journey sends the conductor back to the requirements flow for that requirement or the UX design only.

### Build and acceptance (M3)

Not yet designed in detail. One engineer instance per ready story, each in its own worktree, one reviewer per change, a review gate per milestone with a demo and batched human checks, then a reviewer runs the product against the acceptance criteria and the product manager judges the result against the PRD's definitions of done and the PR/FAQ.

Every run, in this flow and all the others, feeds the feedback ledger; the coach reads it later, outside the flow.

## Other flows

**New feature.** The architect maps the affected area first, unless the architecture doc and glossary are current. Then the requirements flow extends the PRD (the idea flow runs first only when the feature needs market research or a PR/FAQ, which only large features do), the architecture flow designs and breaks it down, and the build and acceptance phases follow. Anthropic's feature-dev plugin is the closest prior art for this flow.

**Feature task.** One story or task inside a feature whose run is already under way. The conductor resumes that run's log and gives the work to an engineer, continuing the instance that owns the story if it is still current. One reviewer checks the change. There is no briefing or review gate unless the work hits an engineer stop condition or changes the plan; then it goes back to the architect.

**Bug fix.** A known defect. The conductor briefs the user on the defect, reproduction steps, impact, and which behavior must not change. An engineer uses the debugging skill to build a failing feedback loop and find the root cause, then writes a failing regression test and fixes the bug. A review gate on the root cause comes before the change only if the fix is large or hits a stop condition. A reviewer checks the change before the user confirms.

**Troubleshoot.** A symptom without a known cause, such as an outage, a slowdown, or a broken environment. An engineer gathers evidence (logs, metrics, recent changes) and uses the debugging skill to test hypotheses against it, consulting the architect when the cause may lie in how components interact. The output is a diagnosis in the run folder: the root cause or the remaining candidates, the evidence, and a recommended next step. Troubleshooting changes no code, and mitigation steps that touch running systems go to the user as proposals. If the cause is a defect, the conductor proposes a bug-fix flow.

**Understand.** Architect instances fan out over the codebase, one per area, and one of them synthesizes their maps into an as-is architecture doc, a glossary, and a risk and debt map. The conductor closes with a briefing that walks the user through the result and answers questions. Its output often feeds a new-feature or rewrite flow, and the synthesizing architect can continue into that flow with its context intact.

**Rewrite.** This flow runs the understand flow first. A briefing establishes why the rewrite is happening and what behavior must stay identical. The same architect proposes a target architecture and a migration strategy (incremental replacement, parallel run, or a single cutover) with ADRs, and the user reviews it. The architect then writes an incremental roadmap whose first stories are parity tests, the build phase runs, and acceptance checks parity.
