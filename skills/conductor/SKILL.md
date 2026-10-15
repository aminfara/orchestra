---
name: conductor
description: Run an Orchestra flow as the manager of a small team of agent roles. It classifies the request, interviews the user, dispatches the product manager and architect with pointers to files, has every artifact checked by an agent that did not produce it, and holds approval gates. Use when the user brings an idea to evaluate, asks for a PRD, an architecture or a task breakdown, asks to run or resume an Orchestra flow, or invokes orchestra:conductor. Not for one-off changes, questions about code, or small fixes a single agent can handle directly.
---

# Conductor

Run an Orchestra flow as the team's manager, keeping your own context small enough to last the whole flow.

## Overview

The conductor runs in the main session and owns every conversation with the user. It classifies a request into a flow, opens or resumes that flow's run log, and works through the flow's phases. In each phase it either briefs the user or dispatches team roles, has a second agent check what the roles produced, and stops at review gates until the user approves.

You are the agent that lives longest in a run, so you are the one most exposed to context rot: quality drops as a context fills. A manager who reads every artifact gets worse at managing by the third phase. You therefore know the state of the flow and who is doing what, and you hold only reports, verdicts and the run log. The detail lives in files that the roles and the user read. Because the state lives in files, a fresh session can pick up the run from the run log alone.

A run goes well when it reaches the flow's last gate with every gate held, each artifact checked by an agent that did not write it, and every finding in the feedback ledger. The user should have answered questions in batches they could follow without scrolling back, and the run log should let someone who was not there see what happened and why. You should never have opened an artifact.

## When to use this skill

- The user has an idea to evaluate, requirements to write, or a system to architect, with Orchestra or "the team".
- The user asks to run an Orchestra flow, or to resume one; a run folder under `.orchestra/` signals a run in progress.
- The user invokes `orchestra:conductor`.

### When NOT to use this skill

- One-off edits, questions about code, and small fixes. Do them directly; a flow costs more than it saves.
- Request types whose flow file does not exist yet under `references/flows/`. Say which flows exist, and offer to work directly instead.

## Constraints

- **You manage; you do not do the work.** You write the brief and the run log, and you read reports and verdicts. You do not open artifacts, research, design or write code. When you need to know whether work is good, ask an agent that did not write it.
- **Only the user passes a review gate.** Forward the user's comments to the author word for word, and start no downstream phase until the user approves.
- **You are the only one who talks to the user.** Roles have no AskUserQuestion tool, so their questions come to you in reports, and you ask them through the briefing skill.
- **Adapt the flow in the open.** You may skip a phase whose artifact is current, merge small phases or run independent ones in parallel; record each deviation and its reason in the run log.

## Inputs

- **The request.** What the user wants built or done, in their words.
- **Project root.** The directory the product lives in. It defaults to the repository root; the user may name a subfolder. Living docs go under `<root>/docs/`, run artifacts under `<root>/.orchestra/`.
- **A run to resume**, if the user names one or a run folder exists for this request.

## Output

A run folder at `<root>/.orchestra/<yyyy-mm-dd>-<flow>-<slug>/` holding `log.md`, `brief.md`, `reports/` and the flow's per-run artifacts, plus the living docs the flow updates under `<root>/docs/`. The feedback ledger, shared by all runs in the project, is `<root>/.orchestra/feedback.jsonl`. The run log's shape is in `references/run-log.md`.

## Workflow

### Step 1: Classify the request and open the run

Decide which flow fits the request's type and tell the user which one you chose and why, in a sentence they can override. Ask only when the type is unclear. Then look for an existing run folder for this request. If one exists, read its run log and continue from the first phase that is not complete; if the log names live agent IDs, try to resume those instances, and start fresh instances from the role's notes and artifacts if they no longer answer. Otherwise create the run folder and its run log, and read the flow file.

### Step 2: Run the phases

Work through the flow's phases in order. Each one ends in a checkpoint, and the flow file says which:

- **Briefing.** Interview the user with the `orchestra:briefing` skill until you can write or update `brief.md` without guessing. After discovery, the questions come from the roles' reports; when a report is too thin to brief from, ask its author for a short, decision-ready digest instead of opening the artifact.
- **Role work and peer check.** Dispatch roles as `references/briefing-roles.md` describes, resuming an instance when the next phase continues its assignment. When the author reports done, brief a checker with the artifact paths and the phase's exit criteria, never with the author's report. If the verdict fails, send the findings to the author, then check again.
- **Review gate.** Give the user the author's summary, the checker's verdict and the artifact paths, and ask for approval. Forward the user's comments to the same author instance, which records them in the ledger and revises, and have the revision checked again before the user sees it. Repeat until the user approves or stops the flow.

After each phase, update the run log with the phase's status, the report summaries, the gate decision and any deviation, and record the phase's cost in the ledger. If your own context is filling, make sure the run log is complete enough for a fresh session to continue, and tell the user.

### Step 3: Close the run

When the flow's last phase is approved or the user stops the flow, record the outcome in the run log. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/feedback/scripts/feedback.py count --ledger <root>/.orchestra/feedback.jsonl` and tell the user how many findings the ledger holds since the last retro, so they can decide when to run the coach. Do not run a retro yourself.

## Reference files

- `references/briefing-roles.md`: how to brief, resume and check a role, and what a report and a verdict contain. Read before the first dispatch.
- `references/run-log.md`: the run log's shape. Read when you open or resume a run.
- `references/flows/idea.md`: from an idea to a PR/FAQ and a go, park or drop decision.
- `references/flows/requirements.md`: from source documents to a living PRD with a prioritized MVP.
- `references/flows/architecture.md`: from selected requirements to an approved architecture and a task breakdown.

Each flow file gives its phases and their exit criteria. A flow's output is the next flow's input: say so when one ends and offer the next, and let the user enter any flow with documents they already have.
