---
name: coach
description: Improve how the Orchestra team works from the evidence in its feedback ledgers, outside any flow. Reads the ledger's signals and findings across runs and projects, decides whether each recurring problem needs nothing, a concept in a skill, a tool, or a note in the project, proposes lighter review or cheaper models where a role has earned it, evaluates changes that already landed, and records every decision. Use when the user asks for a retro or to run the coach, when a session-start message says Orchestra's improvement loop has signals, or after a milestone. Not for fixing one run's artifact, and never from inside a running flow.
---

# Coach

Turn what the ledger shows about many runs into a few changes that help agents reason better and cost less.

## Overview

The coach runs the improvement loop. It reads Orchestra's feedback ledgers, which every check, review, acceptance and gate writes to, and the signals the ledger script computes from them. For each pattern it decides where the fix belongs, proposes it with its evidence, and records the user's decision. Later it checks whether the changes it landed helped, restores what did not, and looks for review and model spend the evidence says is no longer needed.

A finding fixed once and forgotten recurs, and a finding turned into a rule costs attention in every future run. Neither makes the team better. The coach's job is to find the misunderstanding behind a group of findings and fix it once, as a concept that covers cases nobody has seen yet, or as a tool that costs no attention at all. Most findings deserve no change; they are what checks exist to catch.

A good retro ends with a handful of proposals, each explaining several findings, each approved or rejected by the user and recorded in the ledger. Skills come out the same length or shorter. Every trial has a signal that will undo it, and every landed change is evaluated a few runs later.

## When to use this skill

- The user asks for a retro, or to run the coach.
- A session-start message reported that Orchestra's improvement loop has signals, or the conductor reported them when a run closed.
- A milestone or a series of runs has finished and the user wants to know what to change.

### When NOT to use this skill

- During a flow, or to improve one run's artifact. The run's checks and gates do that.
- To add a rule because one thing went wrong once.

## Constraints

- **Stay outside the delivery loop.** Never join a run, message a role, or change something a run in progress depends on.
- **Read the ledger, not the runs.** Open an artifact only when a finding cannot be understood without it, and quote nothing from it.
- **One finding never changes a skill.** Every concept change explains several findings and passes the four tests in Step 4.
- **The user approves every change.** Proposals are written in general terms, with no project names, code or quoted content, because Orchestra is a public repository.

## Inputs

- **The ledgers.** This project's `.orchestra/feedback.jsonl`, or every ledger on this machine through the registry the session-start hook keeps, `${CLAUDE_PLUGIN_DATA}/ledgers.json`.
- **Where Orchestra lives.** If the working folder is the Orchestra repository, changes to skills and agents are made there on a branch. Anywhere else, they are written as patches for the user to apply there.

## Output

- Proposal and decision events in the ledgers, written with the feedback script.
- For each accepted change: the diff on a branch of the Orchestra repository or a patch in `.orchestra/proposals/<id>.md`; for a concept change, an eval case under the skill's `evals/`; for a trial, the change in the project's `.orchestra/config.toml`.
- A retro marker, so the next window starts after this retro.

## Workflow

### Step 1: Read the signals and the history

Run the feedback script, `python3 ${CLAUDE_PLUGIN_ROOT}/skills/feedback/scripts/feedback.py`, with `signals`, `summary` and `proposals`, passing `--ledger <path>` for this project or `--registry ${CLAUDE_PLUGIN_DATA}/ledgers.json` for all of them. Signals marked `act` come first. The proposals list shows what was tried before: a rejected change comes back only with new evidence, and the note on the rejection says what that would be. Read individual findings only for the groups the signals and the summary point to.

### Step 2: Handle what is hurting now

A `trial-regressed` signal means a lighter review or a cheaper model let problems through: propose a `restore` for that role at once. An `escape` is a finding that got past every check; ask what the checker was told to look for and why it did not catch this, because an escape usually says more about the check's exit criteria than about the author.

### Step 3: Decide where each fix belongs

For each group of related findings choose one answer, with the first as the default:

- **Nowhere.** One-offs, and exactly what checks exist to catch, stay in the ledger.
- **A concept in a skill.** When findings recur and share a cause, name the idea the agent was missing or misapplying and express it as a clarified principle, a sharper quality bar or one good example. "Check the discount field for null" is a rule; "a value is optional until the domain says otherwise, so model its absence explicitly" is a concept that explains that finding and the next five like it.
- **A tool.** Mechanical findings (format, naming, a forbidden call, a report that skips its ledger IDs) become a linter rule, a test, a script or a hook.
- **The project.** Findings about one project's conventions or domain go to that project's CLAUDE.md, glossary or ADRs, where only its agents read them.

### Step 4: Test each proposal

Answer four questions for every concept change, and drop or generalize it if any answer is weak:

1. Does it explain more than one finding? A change that fixes exactly one past finding is a rule in disguise.
2. Would an agent reading it reason better about a case nobody has seen yet?
3. Is it phrased as what good looks like, rather than as a prohibition?
4. What does it replace? Name what it shortens, merges or removes; a `skill-growth` signal means the answer is overdue.

### Step 5: Evaluate, save and remove

For each `evaluate-change` signal, compare the findings in that skill and category per closed run before and after the change landed, and propose `kept` or a `restore`. For a `clean-streak`, propose a trial in the project's `.orchestra/config.toml`: `[review] <role> = "sample"` to check a sample of that role's work, or `[models] <role> = "<model>"` for a cheaper model; the ledger raises `trial-regressed` by itself if problems start escaping. To shorten a skill, run its eval cases with skill-creator with one guideline removed, in a subagent, and propose a `removal` when they still pass.

### Step 6: Decide with the user and land

Record each proposal with `propose --kind <kind> --target <skills/name, agents/name, hooks, or config:key; comma-separated for several> --summary "..." --evidence <finding ID>...` (plus `--role` for a trial or restore). Present them in batches through AskUserQuestion, each with its evidence, its answers to the four questions and the diff. Land each accepted change: edit the skill or agent and lint it with skill-linter, or write the patch file; add an eval case for a concept change, built from the pattern rather than any project's content. Then record each answer with `decide --id <id> --decision accepted|rejected|kept|reverted --note "..."`, giving a rejection's reason; deciding after landing stamps the skill versions the change produced, which later evaluations compare against. Finish with `retro --note "<what was decided>"`, and tell the user they can schedule a recurring retro once the loop has proved itself.
