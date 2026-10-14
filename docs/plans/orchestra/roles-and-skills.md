# Roles and craft skills

Part of the [Orchestra plan](README.md). Who does the work, how much context each one keeps, and which skills each one uses.

## Split roles by view, not by activity

A real team working on one product is small. A product manager researches the market and writes the PR/FAQ. An architect researches the technology, designs the system, and breaks it into features and a roadmap. An engineer takes a story, breaks it into tasks, writes the tests and the code, refactors, and documents. Another engineer reviews the change for quality, function and security. Each of them does several kinds of work, and each carries one understanding of their assignment from one activity to the next.

Orchestra follows that shape. A role is defined by its view: the altitude it works at and what it is accountable for. Activities that share a view belong to the same role and use the same context. Activities that need a different view belong to a different role, because a separate context is the point: the product manager should not see the problem through the architect's eyes, and the architect's view of the whole system should not be crowded out by one task's code.

Splitting further than that costs more than it saves. Every new role starts empty and has to be primed with the brief, the research and the architecture before it can work, and each priming spends tokens and loses some of the understanding the previous agent had built. Merging further costs focus, because one context starts holding views that should stay apart.

## Roles

Orchestra has four team roles, which work inside the delivery loop, and a coach, which works outside it.

| Role | View and accountability | Skills | Model, effort | Settings |
| --- | --- | --- | --- | --- |
| product manager | The voice of the customer: what to build and why, how it should feel to use, and whether the result keeps the PR/FAQ's promises | research (market and user lenses), writing-studio (PR/FAQ, specs), ux-design (when the product has a user interface), verification (acceptance from the customer's side) | Opus, high | Writes docs and wireframes only; web access |
| architect | The whole system: how to build it, in what order, and what is expensive to change later | research (technical lens), architecture (target and as-is), planning (features, stories, roadmap), tasks | Opus, high | Writes docs and stories only; web access |
| engineer | One story, end to end | planning (story into tasks), test-first, debugging, tasks, writing-studio (docs) | Sonnet, medium | `isolation: worktree` |
| reviewer | Another engineer's change, judged without the author's claims | review (quality, function, security and performance lenses), verification, debugging, feedback | Opus, high | Read-only, except running tests and the product |
| coach | Orchestra itself over many runs | feedback, skill-creator | Opus, high | Its own session, outside any flow; writes proposals only |

The conductor, which runs in the main session, is the team's engineering manager. The coach is not part of the team and not part of the software development lifecycle. Its view is how the team works across many runs, not any one product, so mixing it into a flow would put the wrong view in the wrong context. The coach is therefore a skill with its own entry point rather than a subagent the conductor dispatches: you start it in a separate session, it reads only the feedback ledger, and it presents its proposals to you directly. It can spawn its own subagents for eval runs and removal trials. It never reads a run's artifacts, talks to a team role, or touches a run in progress. See [Feedback loop](feedback-loop.md).

Some activities move compared with a larger roster. The product manager is the voice of the customer, so it also absorbs user experience design when the product has a user interface: the journeys and wireframes describe the same customer view as the PR/FAQ, and keeping them in one context means the design follows from the customer promises rather than being re-derived from them. The architect absorbs technical research, roadmap planning and codebase mapping, which is the same whole-system view in different activities. The engineer absorbs task breakdown. The reviewer absorbs testing and acceptance verification, using the functional lens and the verification skill. BMAD's five personas (analyst, product manager, architect, developer, UX designer) are the closest prior art to this roster; Orchestra folds the analyst and UX designer into the product manager ([others notes](../../research/prior-art/others.md)).

You set the model rule: Opus at high effort for research, quality assurance and architecture, and Sonnet at medium effort for the engineers who execute. The product manager and coach are judgment roles, so I put them on Opus too. The reviewer runs on Opus while the engineer runs on Sonnet, so the two do not share blind spots. Subagent frontmatter supports `model` and `effort` fields, so each role file sets its own, and the [feedback loop](feedback-loop.md) adjusts them over time.

## Instances and context

A role is a definition; an instance is one running agent with its own context. The question for each piece of work is whether to continue an existing instance or start a new one.

**Continue while the assignment is the same.** The architect who did the technical research designs the architecture and then cuts the roadmap in the same context, because each step builds on the understanding the last one created. The conductor resumes that instance for each phase instead of spawning a fresh one, and forwards your review comments to it verbatim. The same holds for an engineer across the tasks of its story.

**Start a new instance when the work is independent or the context is spent.** Several engineers work in parallel, one instance per story, each in its own worktree. Several architect instances can map different areas of a large codebase, with one of them writing the synthesis. When a long-lived instance's context fills with material its current work no longer needs, it writes a short note to itself (what it decided, what it is in the middle of, which files matter), and the conductor starts a fresh instance from that note and the role's own artifacts. Context rot is a risk inside a role as well as in the conductor.

**Always use a separate instance to check.** The checker must not share the author's context, or it inherits the author's assumptions. A reviewer instance never reviews a change it helped write, and the architect checks the product manager's PR/FAQ rather than the product manager checking its own.

The engineer stops and reports "needs a decision" for five kinds of change: irreversible operations, security-sensitive actions, work outside its story, architectural changes, and a backward-incompatible change to an API that is already released and not behind a feature gate. A backward-compatible API change, or any change behind an unreleased feature gate, is the engineer's call; it logs a ruling and continues.

## Craft skills

Skills are what a role knows how to do; a role composes several. A role loads each skill when a brief names it for the phase, rather than preloading all of them at spawn, so each instance starts lean and carries a long skill such as writing-studio only from the phase that needs it. Each skill stays short, on the order of 100 to 150 lines, and follows the repo's canonical template. It holds the concepts that help an agent think about the activity and the quality bar for its output, and it does not try to anticipate every mistake.

| Skill | Used by | Holds |
| --- | --- | --- |
| briefing | conductor | Interviewing the user: batched, self-contained questions with a recommendation each; the agent finds facts, the user decides |
| research | product manager, architect | Lenses, primary sources, citing, separating fact from inference |
| architecture | architect | Target and as-is architecture, three options for every one-way-door decision, ADRs, the glossary, keeping the architecture doc small |
| planning | architect, engineer | Two altitudes: features, stories and a roadmap from an architecture; tasks from a story. Vertical slices, dependency edges, sizing work to fit one context |
| test-first | engineer | Test-driven development as a design practice |
| debugging | engineer, reviewer | A failing feedback loop before hypotheses, recording behavior that must not change, escalating after repeated failed fixes |
| review | reviewer | Reviewing without the author's claims; quality, function, security and performance lenses, used as the change's risk calls for; triage of findings |
| ux-design | product manager | User journeys, information architecture, wireframes and simple clickable prototypes for the MVP, with usability and accessibility as quality bars; used only when the product has a user interface, and only after the PR/FAQ is approved, because the PR/FAQ's own wireframes stay rough by design |
| verification | reviewer, product manager | Working backward from the goal; evidence from commands run fresh, not from reports |
| tasks | architect, engineer, conductor | The [`tasks` interface](tasks.md) and when to use each operation |
| feedback | reviewer, coach | Recording findings, and how the coach turns them into concepts ([feedback loop](feedback-loop.md)) |
| writing-studio | product manager, engineer | Existing; PR/FAQ, specs and other human-facing docs |
