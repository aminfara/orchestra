# Orchestra plan

A Claude Code plugin that runs a team of agents through software engineering flows. Draft, 2026-10-14; the decisions below were made with Ali the same day.

## Summary

Orchestra has four layers. A `conductor` skill runs in the main session and owns every conversation with the user. A library of flows (idea, requirements, architecture, new feature, feature task, bug fix, troubleshoot, understand, rewrite) tells the conductor which phases exist and where the user decides. Four team roles (product manager, architect, engineer, reviewer) do the work and hand it back as files, and a coach outside the team improves how they work. Each role combines several short craft skills and keeps one context across the activities that share its view, the way a small real team does.

The conductor acts as the team's manager. It knows the state of the flow and who is doing what, and it reads short reports, never the artifacts or the code. When it needs to know whether work is good, it asks another agent to check. Every context window stays scoped to one job, which is the reason to use subagents at all.

Orchestra runs two loops. The delivery loop is the software development lifecycle: the conductor and the four team roles run a flow and ship the work, and every check, review and user gate along the way records its findings in a feedback ledger. The improvement loop sits outside it: a coach, started in its own session with its own entry point, reads the ledger across many runs and proposes changes to how the team works. It turns recurring findings into better concepts in the skills, into tools, or into project docs, never into one rule per finding, and proposes lighter review and cheaper models where a role has earned trust. The coach never joins a flow, never talks to a role, and never changes anything mid-run. You approve each of its changes, and the following runs show whether it helped.

The craft skills are Orchestra's own. A survey of ten frameworks (Superpowers, GSD, Addy Osmani's agent-skills, Matt Pocock's skills and six others) found good ideas in each, found that almost all are written as rigid procedures, and found that none publishes evidence that its multi-agent loop beats a single agent. Orchestra borrows the ideas, writes them as concepts and quality bars, and measures itself against a single-agent baseline from the first milestone.

## Tenets

**Focused attention over exhaustive instruction.** Every line an agent reads competes with the task in front of it, so skills and contexts carry only what helps the agent think clearly about its job. A skill states the concepts that matter, what good work looks like, and where the agent's authority ends; it does not script steps or try to anticipate every mistake. A rule added for one past failure costs attention in every future run, and over-prescription backfires. Skills stay short, prefer concepts to rules, and get shorter when they can.

**The conductor manages; it does not do the work.** GSD defines context rot as "the quality degradation that accumulates as an AI fills its context window", and the conductor, which runs the whole flow, is the agent most at risk. It decides who works on what, gives each agent the context, skills and tools it needs, and reads only their reports. It does not learn the details of the architecture, a task or the code, and it does not open an artifact to judge it.

**Verify with another agent, not by reading.** When the conductor needs to know whether an artifact meets its quality bar, a second agent checks it and the conductor reads the verdict. The checker gets the artifact and its exit criteria, never the author's report, so the author's confidence cannot sway it. Where possible the checker is the role that consumes the artifact next.

**Learn concepts from reviews, not rules.** A finding fixed once and forgotten recurs. Orchestra records every finding against the role, skill and model that produced the work, and the coach looks for the misunderstanding behind recurring findings. The fix is a concept that helps agents reason about a whole class of cases, a deterministic tool, or a note in the project's own docs. Most findings change nothing.

**Draw context boundaries where the information changes, not at job titles.** A context is one agent's attention. It should hold what the next piece of work needs and nothing that distracts from it. Work that builds on the same research, such as the product manager sizing a requirement it just researched, stays in one context, because handing it to another agent loses detail, costs time and lowers accuracy. A new context is justified in four cases: a checker must be independent of the author; units of work are parallel and independent (stories, competitors, codebase areas); bulk raw material goes to a subagent and only a digest returns; or the context is full and the agent writes a note for a fresh one. Skills are the way to share capabilities between contexts: estimation, feasibility and research can be loaded by any agent that needs them, at the depth the moment calls for. Agents stay few; skills carry the specialisms.

**Let the request's type choose the ceremony.** A one-line fix does not need a PR/FAQ. The conductor classifies each request by type and runs the matching flow, whose ceremony fits that type. It states which flow it chose and why, and the user can override.

**Files are the contract between agents.** A subagent starts with an empty context and returns one final message, so every handoff goes through an artifact on disk, and anything a role needs is on disk before it is spawned. The conductor passes file paths without reading the files. Because the state lives in files, a fresh session can resume a flow halfway through.

**Keep living docs small, and pass them only when needed.** Every role that reads the architecture doc or the glossary pays for it, and more roles read them as a project grows. Each living doc stays short enough to read in one sitting and points to detail instead of inlining it. Each brief lists only the docs that role needs, down to the section.

**The conductor talks to the user; roles do not.** Claude Code removes the AskUserQuestion tool from subagents ([sub-agents docs](https://code.claude.com/docs/en/sub-agents.md)), so briefings and review gates run in the main session. The conductor asks in batches through that tool, and each question carries its own context and a recommended answer. Roles put questions for the user in their reports and talk to each other directly.

## Design notes

Each note covers one part and can be read on its own.

- [Prior art](prior-art.md): what the survey found and the decision table for 18 concerns.
- [Conductor](conductor.md): briefs, reports, checkpoints, agents talking to each other, the run log and where files live.
- [Roles and craft skills](roles-and-skills.md): the four team roles and the coach, when an instance continues or starts fresh, the engineer's stop conditions, and which role uses which skill.
- [Flows](flows.md): the idea, requirements and architecture flows phase by phase, and the other flows.
- [Tasks](tasks.md): the six task operations, the Git adapter, and tracker adapters after the MVP.
- [Feedback loop](feedback-loop.md): how findings become concepts, tools or project notes, and how Orchestra gets leaner and cheaper.
- [M1 sessions](m1-sessions.md): how the overseer and dogfood sessions share work, and the prompt to start each.

## Plugin layout

```text
orchestra/                         plugin root (this repo)
  .claude-plugin/plugin.json
  skills/
    conductor/                     entry point for the delivery loop
      SKILL.md                     classify the request, pick a flow, run its phases, hold the gates
      references/
        briefing-roles.md          how to brief a role and what a report looks like
        run-log.md                 shape of the run log
        flows/                     one file per flow
    coach/                         entry point for the improvement loop; runs in its own session
    briefing/  research/  feasibility/  estimation/  ux-design/  architecture/
    planning/  test-first/
    review/  verification/  debugging/  tasks/  feedback/
    writing-studio/                existing; PR/FAQ and other human-facing docs
    skill-linter/                  existing
  agents/                          one file per team role
```

The repo already keeps skills under `skills/`, which is the plugin layout. Turning it into a plugin means adding `.claude-plugin/plugin.json` and an `agents/` folder ([plugin components docs](https://code.claude.com/docs/en/plugins/components.md)).

## Build plan

| Milestone | Scope | Done when |
| --- | --- | --- |
| M0 (done) | Prior-art survey and your review of the decision table | Done 2026-10-14; five rows revised from your answers |
| M1 | Plugin manifest; conductor with its references; idea, requirements and architecture flows up to the approved architecture; product manager and architect roles, with instances resumed across phases; briefing, research, feasibility, estimation, ux-design and architecture skills; the feedback skill and ledger, with checkers recording from the first run; five spikes, run first (see below) | One dogfood run on the collaborative todo app reaches an approved architecture, every gate holds, the conductor never opens an artifact, a reader who was not in the session can follow each artifact, the artifacts compare favorably with a single-agent baseline on the same idea, and a coach retro run by hand turns the ledger into proposals you can judge |
| M2 | The architecture flow's breakdown phase, the planning skill, the breakdown gate, and the `tasks` script with the Git adapter, tested with parallel claims from two worktrees and two machines | The breakdown from the M1 run contains stories an engineer could start without asking a question |
| M3 | Engineer and reviewer roles; test-first, review and verification skills; acceptance; worktree isolation; merge order; the coach skill as its own entry point, with its first review-sampling and model trials | The M1 idea's MVP is built and passes acceptance |
| M4 | New-feature, feature-task, bug-fix and troubleshoot flows; debugging skill | Each flow completes on the product built in M3 |
| M5 | Understand and rewrite flows, with architect instances mapping a codebase in parallel | The understand flow produces a usable map of an existing open-source codebase |

M3 carries the most risk, because it is the first milestone where agents change code in parallel. Matt Pocock's upstream `implement-spec` skill (parallel implementers, one worktree per ticket, a merger subagent on an integration branch) is the prior art to study before starting it.

### M1 spikes

M1 starts with five throwaway tests of Claude Code behaviour the design depends on. All five ran on 2026-10-14 from desktop app sessions; the results are below and in the design notes they affect.

1. **Resuming an instance: passed within a session.** A subagent stored three facts and finished; resumed with SendMessage, it recalled all three exactly. Resuming from a different session, for example after an app restart, is untested; the dogfood run tests it, and the role's note to itself covers the gap.
2. **Forked briefings: failed.** The overseer session ran two throwaway skills marked `context: fork` on 2026-10-14, one with `background: false` and one in the background. Neither had AskUserQuestion in its tool list or among its deferred tools, so neither could ask a question. The sub-agents docs' remark that forks keep the main session's tools applies to forking the conversation, not to a skill's `context: fork`. Briefings therefore run in the main session, from the roles' reports.
3. **Agents talking to each other: passed with plain subagents.** One background subagent sent a message to a finished sibling by its agent ID; the send resumed the sibling, which reported the exact text. Subagents have SendMessage but not ListAgents, so a role can only message an agent whose ID is in its brief. Agent teams are not needed for this.
4. **Nesting from a background agent: passed.** A background subagent spawned a nested foreground subagent, which replied as asked. The GSD notes' claim does not hold here. The background subagent also lacked AskUserQuestion, as the docs say.
5. **Loading the plugin locally: `--plugin-dir`, in a CLI session.** The docs say `--plugin-dir` and `/reload-plugins` are documented for the CLI but not for the desktop app, and that a local-path marketplace loads its plugin in place, with edits applied at the next session start or after `/reload-plugins` ([plugin loading docs](https://code.claude.com/docs/en/plugins/loading.md)). On 2026-10-14 the overseer found that this machine's managed settings block local directory marketplaces, so `claude plugin marketplace add` fails. `claude --plugin-dir <main checkout>` works: a headless session listed both agents and the craft skills under the `orchestra:` prefix, and a plugin agent loaded `orchestra:feedback` with the Skill tool. A skill that is also installed under the same path as a personal skill (writing-studio and skill-linter are symlinked into `~/.claude/skills/`) loads once, under its personal name without the prefix, so briefs name it `writing-studio`. The dogfood session therefore runs as a CLI session started with `--plugin-dir`, and picks up merged changes at its next start or `/reload-plugins`; the dogfood run confirms `/reload-plugins` the first time a change lands.

### Dogfooding

The dogfood product is a collaborative todo web app. It lives inside this repo, in `dogfood/todo/`, because agents in these sessions cannot reach a separate repo. Orchestra treats that folder as the project root (living docs in `dogfood/todo/docs/`, run artifacts in `dogfood/todo/.orchestra/`), and the Git adapter and engineer worktrees use this repo.

Two interactive sessions run side by side. The dogfood session runs the conductor on the todo app and nothing else; it uses the skills, it does not edit them. The overseer session watches the dogfood run through its run log, feedback ledger and reports, acts as the coach, and develops the skills and agents in `skills/` and `agents/`. A skill change made in the overseer session reaches the dogfood session the next time it loads that skill, so changes should land between phases, not during one.

The single-agent baseline in M1 exists because no surveyed framework publishes evidence that its loop beats one well-prompted agent. One Claude session gets the same idea and the same craft skills, and you compare the two sets of artifacts blind. If Orchestra does not do better, the plan changes before M2.

Each milestone ends the same way: lint every new skill with skill-linter, run trigger evals on the conductor's description with skill-creator, and keep notes from the dogfood run, including how full the conductor's context got at each phase. From M1 on, the coach's proposals are how the skills change: each milestone's dogfood run feeds the ledger, and the next milestone starts by deciding on the open proposals.

## Risks

- **Unproven benefit.** None of the ten frameworks surveyed shows that its multi-agent loop beats a single agent. The M1 baseline is the defense.
- **Trusting summaries too far.** A conductor that never reads artifacts can pass on a confident report that hides a weak result. Peer checks that never see the author's claims, plus your own reading at review gates, are the defense. If a bad artifact gets past both, sharpen the checker's exit criteria rather than letting the conductor read more.
- **Conductor context creep.** Context still grows over a long flow, through reports, run-log updates and gate conversations. If it fills before the flow ends, the run log must be enough for a fresh session to take over.
- **Rule accretion.** GSD shows where this leads: each real failure added a patch until workflows passed 1,000 lines. An automated coach could do the same faster. The defenses are the four tests every proposal must pass ([feedback loop](feedback-loop.md)), the rule that one finding never changes a skill, tracked skill length, periodic removal trials, and your approval of every change.
- **Loosening review too fast.** The coach could reduce review on a role before its quality is proven. Problems that reach acceptance or you after a reduction trigger a proposal to restore it.
- **Parallel engineers conflicting.** A worktree subagent branches from the default branch, not from the parent's HEAD ([sub-agents docs](https://code.claude.com/docs/en/sub-agents.md)), so a task that depends on unmerged work cannot start in parallel with it. The architect's dependency edges between stories decide what runs concurrently, and the conductor merges in dependency order. Task claims must also stay consistent across worktrees and machines; M2 tests the Git adapter's approach before anything depends on it.
- **Context rot inside a role.** A product manager or architect instance that carries its context across several phases can fill up just as the conductor can. When that happens, the role writes a note to itself and the conductor continues from a fresh instance; M1 should show how often that is needed.
- **Cost.** The build phase spawns two agents per story, and risky changes add review lenses. I have no estimate yet; the ledger records cost per task from M1.
- **Leaking project content into a public repo.** Proposals from work in other projects could carry their names or code into this repo. The coach writes proposals in general terms, routes project-specific lessons to the project's own docs, and you check each proposal at the gate.

## Decisions

Made on 2026-10-14:

- **Plugin root:** this repo's root becomes the plugin. writing-studio and skill-linter ship with it unchanged.
- **Name:** the orchestrator skill stays `conductor`, invoked as `orchestra:conductor`.
- **Doc layout:** living docs under `docs/`, kept small; per-run artifacts under `.orchestra/`. `config.toml` is always committed; whether run folders are committed is decided after the first dogfood run.
- **Skill overlap:** you will uninstall the overlapping Matt Pocock skills, so Orchestra's craft skills can trigger directly outside a flow.
- **Ceremony:** the conductor picks the flow from the request's type, and each flow sets its own ceremony. The briefings and review gates of the idea, requirements and architecture flows are accepted.
- **Engineer autonomy:** five stop conditions (irreversible, security-sensitive, out of scope, architectural, or a backward-incompatible change to a released API not behind a feature gate). Backward-compatible API changes do not stop.
- **Briefing:** batched questions through the AskUserQuestion tool, each self-contained with its context and a recommended answer.
- **Architecture and models:** one architect, who sets out three options for every one-way-door decision. Opus at high effort for research, quality assurance and architecture; Sonnet at medium effort for engineers; reviewers on a different model from the author; reviews kept light.
- **Roles:** four team roles split by view (product manager, architect, engineer, reviewer). Each combines several skills and keeps its context across activities that share its view. The product manager is the voice of the customer and also does user experience design when the product has a user interface.
- **Coach:** necessary, and outside the delivery loop. It has its own entry point and session, reads only the feedback ledger, and works across runs rather than within one.
- **Task store:** Orchestra's own `tasks` script with pluggable adapters; only the Git adapter is in the MVP.
- **Agent-to-agent runtime:** plain subagents can message each other with SendMessage by agent ID (spike 3), but the idea, requirements and architecture flows use files instead. Messaging stays available for later flows, such as an engineer asking about an interface.
- **Plugin loading during development:** this repo was to be registered as a local plugin marketplace, but managed settings block local marketplaces, so the dogfood session loads it with `--plugin-dir` in a CLI session instead; names keep the `orchestra:` prefix (2026-10-14).
- **Dogfooding:** a collaborative todo web app in `dogfood/todo/` inside this repo, run from a dogfood session while an overseer session watches it and develops the skills.
- **M1 order:** spikes first, then the build.
- **Architecture check in M1:** a fresh architect instance briefed as a critic, until the reviewer role exists (2026-10-14).
- **Skill loading:** roles load each craft skill when a phase's brief names it; agent files preload none (2026-10-14).
- **New-product flow after the first dogfood phases (2026-10-14):** discovery is the product manager's alone, and technical research moves to the start of architecture, scoped by the requirements; a requirements phase with its own PRD (product requirements document) and gate sits between the PR/FAQ and the architecture; briefings close with an open "anything else?" question instead of a confirmation gate; a phase gets at most two rounds of check and revision, and the first check aims to be complete. Applies from the next run, not the one in progress.
- **Three flows replace the new-product flow (2026-10-15):** new products are rare and new ideas are common, and not every idea gets built. The idea flow (brief, market research with a fan-out over three competitors, optional feasibility study for novel ideas, findings briefing, PR/FAQ) ends in a go, park or drop decision. The requirements flow turns a PR/FAQ, research or any idea document into a living PRD, in which each requirement has a what, a why, a definition of done, a value and an effort, ranked into an MVP scope; it also serves new features on existing systems. The architecture flow designs for the selected requirements while checking the existing architecture and the remaining requirements, then breaks the work into tasks. Work breakdown stays a phase of the architecture flow, with its own gate, so the architect keeps its context; it can be reopened alone. Findings that break a selected requirement send the conductor back to the requirements flow.
- **Context boundaries follow information, not roles (2026-10-15):** the product manager researches, checks feasibility, sizes requirements with the estimation skill, writes the PRD and designs the UX, all in one context, because each step needs what the last found. The architect starts from the approved PRD and UX and does technical research, architecture and breakdown. There is one handoff. Estimation is a coarse ranking skill that uses the existing architecture doc when there is one; feasibility is a paper check with a smallest-experiment proposal. A requirement that cannot be sized on paper goes to a spike subagent with one question. UX moves from a parallel architecture-flow phase to the end of the requirements flow, so the two roles no longer negotiate.
- **Feedback loop:** a core part of Orchestra from M1. It turns recurring findings into concepts, tools or project notes, never one rule per finding, so the team gets better and cheaper without losing focus.

## Open questions

1. **Running the product for acceptance.** The reviewer needs a way to run and drive the product (the built-in run skill, a browser tool, or test scripts only). This can wait until M3.
