# Briefing roles

How the conductor hands work to a role, continues it, and has it checked.

## The team

| Role | Agent type | Model, effort | View |
| --- | --- | --- | --- |
| product manager | `orchestra:product-manager` | opus, high | The customer: what to build and why, and how it should feel to use |
| architect | `orchestra:architect` | opus, high | The whole system: how to build it, and what is expensive to change later |

A role is a definition; an instance is one running agent with its own context. Each spawn returns an agent ID. Record it in the run log, because it is how you resume the instance and how other roles reach it. The model and effort come from the agent file; the ledger records them against each finding.

The run ID is the run folder's name, such as `2026-10-14-new-product-todo`. Every brief that may lead to a ledger record carries it.

## A brief

A subagent starts with an empty context. Everything it needs is either in the brief or on disk at a path the brief names. A brief carries pointers, not content: say where the PR/FAQ is, do not summarize it. A summary written by you is a paraphrase, and paraphrases drift.

Write each brief with these parts, in plain prose or short labelled lines:

- **Goal.** What this piece of work is for, in a sentence or two.
- **Inputs.** The file paths to read. Name the section when one section is enough, and list only the living docs this role needs.
- **Artifact.** The path to write and its expected shape, or the craft skill whose output shape applies.
- **Quality bar.** The phase's exit criteria from the flow file, as written there.
- **Skill.** The craft skill to use for this activity, by its full name (for example `orchestra:research`).
- **Out of scope.** What this role should leave alone, usually the next phase's work.
- **Peers.** The agent IDs of roles this one may message directly, and what to ask each about.
- **Report.** The path to write the report to, under the run folder's `reports/`, named `<phase>-<role>-<activity>.md`.
- **Ledger.** The ledger path, run ID, flow and phase, so the role can record findings when it checks or when the user's comments reach it.

Parallel instances get briefs that differ for a reason. When the product manager and the architect research at once, each brief names its own lenses and its own questions, so the two answers cover different ground.

## Continue or start fresh

Resume the existing instance with SendMessage when the next phase continues its assignment: the architect who researched the technology designs the architecture. The message names what is new: the phase, the new inputs, the artifact, the quality bar, the skill and the report path, plus the peers and what is out of scope when those change, and any user comments, forwarded word for word.

Start a fresh instance when the work is independent of what the instance did, or when the instance reports its context is spent. In the last case it has written a note to itself under the run folder's `notes/`; brief the fresh instance with that note and the role's artifacts.

Run instances in the background when they can work in parallel, and wait for each to finish before you use its result. To let two parallel instances talk, spawn the first, spawn the second with the first's agent ID in its brief, then send the first the second's ID. Messaging a running instance is untested; if it fails, the two compare notes through each other's files at the peer check.

When a phase closes, record its cost for each role that worked in it: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/feedback/scripts/feedback.py cost --ledger <ledger> --run <run> --phase <n> --role <role> --rounds <revisions> --tokens <tokens>`, with the tokens from the agents' completion notices where they show them.

## A report

Every role ends with a report, written to the path in its brief and returned as its final message. It is the only thing you read from the role:

- **Status:** done, done with concerns, blocked, or needs a decision.
- **Summary:** what was produced, at the altitude a manager needs.
- **Artifacts:** paths written or changed.
- **Rulings:** decisions the role made on its own, each with what it costs if wrong.
- **Questions for the user:** decisions only the user can make, each with the role's recommendation.
- **Risks and assumptions:** what the next role or the user should know.

Copy the status and summary into the run log, carry the questions to the next briefing, and let the rest go. If a report runs past a few hundred words, ask the role to shorten it rather than reading on.

## A check

A checker is an instance that did not write the artifact. Where possible it is the role that consumes the artifact next. The flow file names the checker for each phase, and whether it is a peer instance resumed from earlier phases or a fresh one.

Brief the checker as a critic. Its job is to find where the artifact fails its criteria, not to confirm that it meets them, so it should look hardest at what the artifact assumes, at its edges and at the promises it must keep. Give it the artifact paths, the exit criteria, the inputs the author worked from, and a report path for its verdict, named `<phase>-<role>-check.md`. Never pass the author's report or your summary of it: the checker should judge the artifact, not the author's confidence in it. Add the ledger details the checker needs to record findings with the `orchestra:feedback` skill: the ledger path, run ID, flow, phase, and the author's role, skill, model and effort. When the artifacts have different authors, as in a combined phase, give these for each author; the checker records each finding against the author of the artifact it concerns, and splits "for the author" by role.

The checker returns a verdict:

- **Verdict:** pass, or revise.
- **Findings:** a count by severity, with the ledger IDs.
- **For the author:** each finding in a sentence, specific enough to act on without the checker present.

A check should be complete the first time: the checker reports everything it will object to, so the author can fix it in one pass. A re-check is narrower. It confirms each finding was fixed and looks only at what the revision changed, so it does not open new ground. Brief both that way.

On revise, send the "for the author" section to the author instance, word for word, and ask for a revision and an updated report. Then send the same checker the revised artifact; it marks its findings fixed in the ledger or keeps them open. A phase gets at most two rounds of check and revision. If findings are still open after the second, something went wrong earlier: the first check missed things, or the fixes created new problems. Take the open findings to the user at the gate as known issues instead of starting a third round, and say which of the two it looks like.

## A gate

At a review gate, give the user the author's summary, the checker's verdict and the artifact paths, then ask with AskUserQuestion whether to approve, request changes, or stop. The user reads the artifact; you do not.

When the user requests changes, send their comments to the author instance word for word, and ask it to record each comment in the ledger as a finding found by `user`, using the `orchestra:feedback` skill, before it revises. Then send the revision to the checker with the user's comments and their ledger IDs, so the user never reviews unchecked work; the checker resolves the findings the revision fixed. When the user chooses to defer or override a checker's finding instead, resolve it yourself with `feedback.py resolve --ledger <ledger> --id <id> --outcome deferred` (or `overridden`).
