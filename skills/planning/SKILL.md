---
name: planning
description: Break approved work into pieces an agent can finish in one context, at two altitudes: an architecture and its selected requirements into features, vertical-slice stories with acceptance criteria, dependency edges and milestones; or one story into the few tasks an engineer needs. Use when an architect breaks down an approved architecture, when scope changes and a breakdown must be reopened, or when an engineer decides how to build a story. Not for designing the system or sizing requirements for a PRD.
---

# Planning

Cut the work so each piece can be started without a question and finished in one context.

## Overview

This skill turns approved work into a plan at one of two altitudes. From an architecture and its selected requirements, the architect cuts features, stories and milestones and writes them to the task store. From one story, an engineer decides whether it needs tasks at all and, if so, which few. Both altitudes use the same ideas: slice vertically, make dependencies explicit, and size each piece to the context that will carry it.

A plan is the set of decisions the implementer cannot make alone, and nothing more. A story that leaves an engineer guessing what done means wastes a run; a story that dictates file names and function signatures has written the code in prose and taken away the judgment the engineer is there to apply. Parallel engineers need the plan to say what can run at once, because two stories that touch the same files collide when their worktrees merge.

A good breakdown lets any engineer pick up any ready story, read its acceptance criteria and the docs it points to, and start. Every definition of done in the selected requirements is covered by some story's acceptance criteria, the first milestone ends in something the user can see working, and the dependency edges are few and real.

## When to use this skill

- The architect breaks an approved architecture into features, stories and milestones for the selected requirements.
- Scope changed after the breakdown, and the affected stories need to be added, edited or dropped.
- An engineer starts a story and decides how to build it.

### When NOT to use this skill

- Designing components, data models or interfaces. That is architecture, and the breakdown points to it.
- Sizing requirements for a PRD. Use estimation.

## Constraints

- **Slice vertically.** A story delivers one observable behaviour end to end, however thin, rather than one layer of many behaviours.
- **Acceptance criteria are checkable from outside.** Each one states what a user or caller observes, traced to a requirement's definition of done.
- **Add an edge only for a real dependency.** A story is blocked when it needs another's interface or data, or when both would change the same files; otherwise let them run in parallel.
- **Leave the how to the engineer.** Point to the architecture section, ADR or UX screen a story builds on instead of restating it.

## Inputs

- **For a breakdown:** the selected requirements in the PRD, the architecture doc, its ADRs and glossary, and the UX design if there is one.
- **For a story:** the story from the task store and the docs its description points to.

## Output

- **For a breakdown:** features and stories in the task store, and `plan.md` in the run folder.
- **For a story:** tasks under the story in the task store, only when they help.

## Workflow

### Step 1: Find the slices

From the selected requirements, the architecture and the UX journeys, find the thinnest path through the system that a user could see work, and make it the first story: it proves the parts connect. Then add stories that each extend a journey or deliver one more requirement. Group them into features by the requirement or journey they serve. Work that only some stories need, such as a schema or a shared component, belongs inside the first story that needs it, not in a horizontal story of its own. Wide changes to existing code go expand, migrate, contract, each step its own story.

### Step 2: Size each story to one context

A story fits when one engineer can hold its acceptance criteria, the code it touches and its tests with room to spare. When a story needs several unrelated areas of the code, or more than a handful of acceptance criteria, split it along a behaviour boundary. When two stories cannot be tested apart, merge them.

### Step 3: Order the work

Draw the blocking edges, then group stories into milestones that each end in something the user can review working. Name what can run in parallel. Write `plan.md` in the run folder with what the task store cannot hold: the MVP's scope in and out, the milestones and what each demonstrates, and why the sequence is what it is.

### Step 4: Write the board

Create features, then stories in dependency order, with the `orchestra:tasks` skill. Each story gets a title in the user's terms, its acceptance criteria, its milestone, its edges, and a description that points to the docs it builds on. Check that every selected requirement's definition of done appears in some story, and that `ready` lists the stories you expect to start first.

### Step 5: Plan a story, when you are the engineer

Read the story, its acceptance criteria and the docs it points to. Most stories need no tasks: build them. Split into tasks under the story only when the work has separable steps worth tracking, such as a migration before a behaviour change, or when you expect your context to fill before you finish, so a fresh instance could continue from the board.
