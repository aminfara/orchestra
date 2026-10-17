---
name: tasks
description: Create, find, claim, annotate and close Orchestra's features, stories and tasks through one small command-line script whose adapter keeps them in the project's chosen store (a dedicated Git branch by default). Use when an architect writes a breakdown into tasks, when an engineer claims, notes or closes its story, when the conductor asks what is ready to start, or when anyone needs one task's acceptance criteria.
---

# Tasks

Read and change task state through one script, so every role sees the same board at the cost of a few lines of JSON.

## Overview

This skill is the interface to Orchestra's task store. Features hold stories, stories hold optional tasks, and each item has a title, acceptance criteria, blocking edges, a milestone, a status, an assignee and notes. Roles never call a tracker directly; they call `scripts/tasks.py`, which passes each operation to the adapter named in `.orchestra/config.toml`.

The store is shared state between agents that cannot see each other. Engineers in separate worktrees, or on separate machines, must agree on who owns which story, and the conductor must know what is ready without reading anyone's work. A script with a fixed interface and specific errors makes that agreement cheap and the same every time: the first claim wins, and the loser gets `AlreadyClaimed` instead of a merge conflict.

Used well, the board is the single source of task state. The architect's breakdown lives there rather than in a document, an engineer's rulings are notes on its story, and the conductor's view of the build is the output of `ready` and `list`.

## When to use this skill

- The architect writes the breakdown: features, stories with acceptance criteria and blocking edges, and milestones.
- The conductor needs the stories that can start now, or an overview of who holds what.
- An engineer claims a story, records a ruling or progress note, splits the story into tasks, or closes it with the change that delivered it.
- A reviewer or the product manager needs one story's acceptance criteria.

### When NOT to use this skill

- MVP scope, milestones' reasoning and sequencing rationale. Those go in the run's `plan.md`.
- Design decisions. Those go in ADRs; a story note can point to one.

## Constraints

- **The board is shared state; change it only through the script.** Never edit the task branch or its files by hand.
- **Claim before you work, and close only what you claimed.** The `--by` value is your agent name from the brief, the same on every call.
- **React to the error name, not the message.** `AlreadyClaimed`, `Blocked` and `UnknownTask` each have an obvious next move; `BackendUnavailable` means stop and report.

## Workflow

### Step 1: Find the script and the project root

Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/tasks/scripts/tasks.py --root <project root> <operation> ...`. The root is the folder holding `.orchestra/config.toml`; your brief names it. Without a config the script uses a local branch called `orchestra/tasks`. A `[tasks]` table can set `branch`, and `remote = "origin"` to share the board across machines.

### Step 2: Use the operation that fits

- `create --kind feature|story|task --title T [--parent ID] [--milestone M] [--blocked-by ID]... [--acceptance TEXT]... [--description TEXT]` prints the new ID. A task needs its story as `--parent`. Create blockers before what they block.
- `ready [--kind story] [--milestone M]` lists unblocked, unclaimed work as IDs and titles.
- `claim ID --by WHO` takes ownership. `Blocked` means a dependency is unfinished; `AlreadyClaimed` means someone else got there first, so pick another ready story.
- `show ID` returns one item in full, including its acceptance criteria and notes.
- `note ID --by WHO --text T` appends a ruling, a decision with its cost if wrong, or progress worth keeping.
- `close ID --by WHO --link REF` marks it done with the commit or branch that delivered it. `release ID --by WHO` hands a claim back when you stop without finishing.
- `edit ID [--title] [--acceptance]... [--blocked-by]... [--milestone] [--description] [--status todo|dropped]` is for the architect when scope changes; repeated flags replace the whole list.
- `list [--kind] [--status] [--milestone]` gives the conductor its overview.

### Step 3: Keep the output small

Each operation prints one JSON object. Read what you need from it and move on; do not paste board listings into reports. A report names the story IDs it touched.

## Reference files

- `scripts/tasks.py`: the script and its Git adapter. Its header documents every operation and error.
