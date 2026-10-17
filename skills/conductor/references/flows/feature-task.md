# Flow: feature task

One story or task inside a build that is already under way: an extra story the architect added, a story reopened after acceptance, or a small change the user asks for within a feature's scope. It is the build flow's phase 2 for one piece of work, without its ceremony.

## Phase 1: Pick up the run

**Who:** you.

Find the build run this work belongs to and read its run log; the integration branch and the team are there. If the work is not yet a story in the task store, resume the architect who owns the breakdown, or start a fresh one with the architecture docs and `plan.md`, to add it with acceptance criteria. If the request changes a requirement or the UX, it is not a feature task: tell the user, and offer the requirements flow.

**Exit criteria:** the work is a story in the task store with acceptance criteria, and its blockers are done.

## Phase 2: Build, review, integrate

**Who:** the engineer instance that owns the story if it is still current, otherwise a fresh `orchestra:engineer`; a fresh `orchestra:reviewer` per change.

Brief, review and integrate exactly as the build flow's phase 2 does, with the same two-round limit. There is no briefing or review gate unless the engineer reports "needs a decision" or the reviewer finds the plan is wrong; then handle it as the build flow says.

**Exit criteria:** the story is closed with a link to its integrated change.

Record the outcome in the build run's log, under the milestone the story belongs to. The milestone's acceptance and gate, in the build flow, cover this story too.
