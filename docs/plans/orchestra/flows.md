# Flows

Part of the [Orchestra plan](README.md). The conductor picks a flow from the request's type, and each flow sets the ceremony that type needs. Roles are described in [Roles and craft skills](roles-and-skills.md); "the same instance" means the conductor resumes the agent from the earlier phase instead of starting a fresh one.

## New product

This is the worked example, and the first flow to build.

| Phase | Who | Produces | Checkpoint |
| --- | --- | --- | --- |
| 1. Intake | conductor with the user | `brief.md`: problem, target user, why now, constraints, success signals, non-goals | Briefing; user confirms the brief |
| 2. Discovery | product manager (market and user lenses) and architect (technical lens), in parallel | `research/market.md`, `research/technical.md`, each with sources and open questions | Peer check: each reads the other's research for claims that are unsourced or contradict its own |
| 3. Findings | conductor with the user | updated brief; decisions in the run log | Briefing |
| 4. Working backwards | the same product manager | `docs/product/prfaq.md`, with the rough wireframes its format calls for | Peer check by the architect (feasible, consistent with the technical research), then review gate |
| 5. Technical intake | conductor with the user | technical section of the brief: stack preferences, hosting, budget, data, non-functional requirements | Briefing |
| 6. Architecture and UX | the same architect, setting out three options for every one-way-door decision, with prototype spikes where a question is risky; in parallel, when the product has a user interface, the same product manager designs the main journeys and wireframes for the MVP | `docs/architecture.md`, `docs/adr/`, glossary; `docs/product/ux/` | Peer check by a reviewer (buildable, covers the PR/FAQ, consistent with the UX design); until the reviewer role exists in M3, a fresh architect instance briefed as a critic; then one review gate for both |
| 7. Roadmap | the same architect | `plan.md` (MVP scope in and out, milestones, sequencing) plus features and stories with acceptance criteria and dependencies, created through `tasks` | Peer check by the product manager (the MVP keeps the PR/FAQ's most important promises), then review gate |
| 8. Build | one engineer instance per ready story, each in its own worktree, breaking its story into tasks and carrying it through tests, code, refactoring and docs; one reviewer per change | merged code, tests and docs | Peer check by the reviewer per change; review gate per milestone with a demo and batched human checks |
| 9. Acceptance | a reviewer runs the product against the acceptance criteria; the same product manager judges the result against the PR/FAQ and, for a user interface, the UX design | `acceptance.md` | Review gate; user accepts the MVP |

The product manager carries one context from market research through the PR/FAQ to acceptance, and the architect carries one from technical research through the architecture to the roadmap. If either context fills before its work is done, the role writes a note to itself and the conductor continues from a fresh instance.

Phase 9 closes the loop: the PR/FAQ written in phase 4 becomes the yardstick for the finished MVP. Every run, in this flow and all the others, feeds the feedback ledger; the coach reads it later, outside the flow.

## Other flows

**New feature.** The architect maps the affected area, unless the architecture doc and glossary are current. The conductor briefs the user, the product manager writes a spec (a PR/FAQ only for large features), and the same architect writes a design note plus ADRs if the architecture changes, then breaks the feature into stories. A review gate follows, then the build and acceptance phases from the new-product flow. Anthropic's feature-dev plugin is the closest prior art for this flow.

**Feature task.** One story or task inside a feature whose run is already under way. The conductor resumes that run's log and gives the work to an engineer, continuing the instance that owns the story if it is still current. One reviewer checks the change. There is no briefing or review gate unless the work hits an engineer stop condition or changes the plan; then it goes back to the architect.

**Bug fix.** A known defect. The conductor briefs the user on the defect, reproduction steps, impact, and which behavior must not change. An engineer uses the debugging skill to build a failing feedback loop and find the root cause, then writes a failing regression test and fixes the bug. A review gate on the root cause comes before the change only if the fix is large or hits a stop condition. A reviewer checks the change before the user confirms.

**Troubleshoot.** A symptom without a known cause, such as an outage, a slowdown, or a broken environment. An engineer gathers evidence (logs, metrics, recent changes) and uses the debugging skill to test hypotheses against it, consulting the architect when the cause may lie in how components interact. The output is a diagnosis in the run folder: the root cause or the remaining candidates, the evidence, and a recommended next step. Troubleshooting changes no code, and mitigation steps that touch running systems go to the user as proposals. If the cause is a defect, the conductor proposes a bug-fix flow.

**Understand.** Architect instances fan out over the codebase, one per area, and one of them synthesizes their maps into an as-is architecture doc, a glossary, and a risk and debt map. The conductor closes with a briefing that walks the user through the result and answers questions. Its output often feeds a new-feature or rewrite flow, and the synthesizing architect can continue into that flow with its context intact.

**Rewrite.** This flow runs the understand flow first. A briefing establishes why the rewrite is happening and what behavior must stay identical. The same architect proposes a target architecture and a migration strategy (incremental replacement, parallel run, or a single cutover) with ADRs, and the user reviews it. The architect then writes an incremental roadmap whose first stories are parity tests, the build phase runs, and acceptance checks parity.
