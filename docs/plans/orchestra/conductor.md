# Conductor

Part of the [Orchestra plan](README.md). How the orchestrator runs a flow while keeping its own context small.

## What it does

The conductor is a skill loaded into the main session and is never forked, because forking would cut it off from the user. It classifies the request into a flow (asking only when the type is genuinely unclear), opens or resumes a run log, and works through the flow's phases. In each phase it either briefs the user or spawns roles, has a second agent check the result against the phase's exit criteria, and stops at gates.

The conductor may adapt a flow. It can skip a phase whose artifact already exists and is current, merge two small phases, or run independent phases in parallel. It records each deviation and its reason in the run log. It never passes a review gate without the user's approval.

When the conductor spawns a role, the brief states the goal, the input file paths, the artifact path and its expected shape, the quality bar, the skills and tools to use, what is out of scope, and the agent IDs of the roles it may talk to directly. The brief carries pointers, not content: the conductor tells the architect where the PR/FAQ is and does not summarize it. It lists only the living docs that role needs, and names the section when one section is enough. For parallel instances, such as the product manager and architect researching at once, each brief differs so the answers differ for a reason, as feature-dev does with its architects.

When the next phase continues a role's assignment, the conductor resumes that role's existing instance instead of spawning a fresh one, so the architect who researched the technology designs the architecture with that understanding intact. The brief for a resumed instance names only what is new. The conductor starts a fresh instance when work is independent, when a check is needed, or when an instance's context is spent (see [Roles and craft skills](roles-and-skills.md)).

To pass skill-linter, `conductor/SKILL.md` follows the canonical template. Its Workflow section stays at the level of "classify the request and choose the flow", "run the phases", "close the run"; the flow files carry everything specific.

## Reports

Every role ends with a report to the conductor, and the report is all the conductor reads. It is short (a few hundred words at most) and has a fixed shape:

- **Status:** done, done with concerns, blocked, or needs a decision.
- **Summary:** what was produced, at the altitude a manager needs. For an architecture, that means "three services, Postgres, one risky integration spiked and confirmed", not the service boundaries.
- **Artifacts:** paths written or changed.
- **Rulings:** decisions the role made on its own, each with what it costs if wrong.
- **Questions for the user:** decisions only the user can make.
- **Risks and assumptions:** anything the next role or the user should know.

The conductor copies the status and summary into the run log and forgets the rest. If a report is too detailed, the conductor asks the role to shorten it instead of reading on.

## Checkpoints

Every phase ends in one of three checkpoints:

- **Briefing.** The conductor interviews the user with the briefing skill until it can write or update the brief without guessing. Questions come in batches through the AskUserQuestion tool; each states what is being asked and why it matters without leaning on earlier discussion, and leads with a recommended answer. Used at intake, after research, and before architecture.
- **Review gate.** The conductor stops and gives the user the author's summary, the checker's verdict and the artifact path, then waits. The user reads the artifact; the conductor does not. The conductor forwards the user's comments verbatim to the author role, resuming the same agent so it keeps its context, instead of paraphrasing them. No downstream phase starts until the user approves. Revisions loop until the user approves or stops the flow.
- **Peer check.** A second agent checks the artifact against the phase's exit criteria and returns a verdict; the conductor reads only the verdict. If the check fails, the conductor sends the findings to the author and asks for a revision. A peer check also runs before every review gate, so the user never reviews work that has not been checked.

Every finding a checker returns, and every change the user asks for at a gate, is recorded in the feedback ledger (see [Feedback loop](feedback-loop.md)).

Some briefings need detail the conductor should not hold, such as walking the user through research findings or technical trade-offs. Running them in a forked skill would keep that detail out of the conductor's context, but spike 2 showed it cannot work: a skill marked `context: fork`, in the foreground or the background, has no AskUserQuestion tool. The conductor therefore runs every briefing itself, from the roles' reports. Where a briefing needs more than a report holds, the conductor asks the author role for a short, decision-ready digest (the options, what each costs, and the role's recommendation) and briefs from that, rather than opening the artifact.

## Agents talking to each other

Roles sometimes need each other more than they need the conductor: an engineer has a question about an interface the architect designed, or a reviewer and an engineer disagree about a change. Routing those exchanges through the conductor would fill its context with exactly the detail it should not hold. Roles therefore talk directly, and each conversation ends as one line in the next report ("agreed with the architect to split the auth module; ADR 0007 updated").

None of the surveyed frameworks does this; they all route through files and the orchestrator. An M1 spike on 2026-10-14 showed plain subagents can do it in the desktop app: a subagent sent a message to a finished sibling by its agent ID, the send resumed the sibling, and the sibling received the exact text. Subagents have SendMessage but not ListAgents, so they cannot discover each other. The conductor therefore lists in each brief the agent IDs a role may talk to ("questions about the architecture go to the architect, agent ID ..."). Agent teams, which are experimental, are not needed for this.

Nesting also works: a background subagent can spawn its own subagents ([sub-agents docs](https://code.claude.com/docs/en/sub-agents.md); confirmed by the same spikes, contrary to the GSD notes). A role can therefore run its own helpers, such as a reviewer running one lens per subagent, without the conductor seeing them.

## Run log and artifacts

Orchestra writes two kinds of files into a target project. Living docs describe the current system and are updated in place by each flow, following OpenSpec's living spec: `docs/product/prfaq.md`, `docs/architecture.md`, `docs/adr/` and the domain glossary. They read as the project's own documentation, so they stay under `docs/`. Each one stays short enough to read in one sitting and points to detail (an ADR, a module doc) instead of inlining it, because every role that reads it pays in tokens and attention.

Per-run artifacts belong to one run of one flow and sit in a hidden folder, `.orchestra/<yyyy-mm-dd>-<flow>-<slug>/`, holding `log.md`, `brief.md`, `research/`, `plan.md` and `acceptance.md`. Tasks live behind the [`tasks` interface](tasks.md) rather than in `plan.md`. `.orchestra/config.toml` is always committed; whether run folders are committed is decided after the first dogfood run.

When the conductor closes a run, it records the outcome and tells you how many new findings the feedback ledger holds since the last retro, so you can decide when to run the coach. It does not run the coach itself.

The run log records the flow and why it was chosen, each phase's status, gate decisions with dates, artifact paths, rulings, open questions, and deviations from the flow with their reasons. It is the conductor's memory across sessions. Standing project context stays in the repo's existing CLAUDE.md or AGENTS.md; Orchestra does not add a constitution file.
