---
name: verification
description: Decide whether work actually achieves its goal by working backward from the outcome to evidence gathered fresh, by running the tests, the product's real entry points and the commands that would show it working, rather than from anyone's report. Use for a milestone's acceptance against stories' acceptance criteria and the PRD's definitions of done, for judging a built product against the PR/FAQ's promises from the customer's side, or before claiming any work is done. Not for a line-by-line code review.
---

# Verification

Prove the outcome happened, with evidence you produced yourself just now.

## Overview

This skill checks that work achieved what it was for. It starts from the goal, such as a milestone's stories, a requirement's definition of done or a promise in the PR/FAQ, works backward to what would have to be observably true, and then makes each of those things happen in front of it: it runs the suite, starts the product, drives it through its real entry points and reads the output.

A report that work is done is a statement of intent. Tasks can all be closed while the outcome is missing: a screen exists but nothing calls it, an endpoint returns a stub, a test passes because it asserts nothing. Checking the goal rather than the task list, and only trusting evidence gathered fresh, is what catches those.

A good verification leaves a short document in which every criterion is met, not met, or not verifiable, each with the command or action that showed it and what was observed. Anyone can repeat it. Failures are specific enough to become stories or bug fixes without another investigation.

## When to use this skill

- A milestone's integrated product needs acceptance against its stories' criteria and the PRD's definitions of done.
- The product manager judges the built product against the PR/FAQ's promises and the UX journeys, from the customer's side.
- Any role is about to report work as done and needs to know it is.

### When NOT to use this skill

- Reviewing a change's code and tests line by line. Use review.
- Finding the cause of a failure. Use debugging once verification shows what fails.

## Constraints

- **Evidence is something you ran or observed in this session.** Reports, commit messages, closed tasks and earlier runs are claims to check.
- **Use the real entry point.** A behaviour a user sees is verified through the interface a user uses, not by reading the code that should produce it.
- **Say "not verifiable" when it is.** If something cannot be exercised here, say what would be needed rather than inferring it passed.

## Inputs

- **The goal:** the stories in the milestone and their acceptance criteria, the PRD's definitions of done for the requirements they deliver, and, for the customer view, the PR/FAQ and the UX journeys.
- **The product:** the branch or build to check, and how the project runs and tests it (its README, scripts or CLAUDE.md).

## Output

`acceptance.md` in the run folder, or the path in the brief:

- How to run the product, as commands someone else can paste.
- One row per criterion: the criterion, met, not met or not verifiable, the evidence (command or action and what was observed), and the ledger ID when it failed.
- The checks only a person can make, such as how a screen feels to use, listed for the user's review gate.
- The verdict lines from the feedback skill.

## Workflow

### Step 1: Work backward from the goal

For each criterion, write what must be observably true if it is met, at three depths: it exists (the screen, endpoint or command is there), it is real (it does the work rather than returning a placeholder), and it is connected (the journey reaches it and its result reaches the user). Most failures hide at the third.

### Step 2: Produce the evidence

Build the product from a clean state, run the whole test suite, and start the product the way the project says. Exercise each criterion through its real entry point: HTTP requests for an API, the command line for a CLI, and for a user interface a browser automation tool if one is available (a built-in browser, Claude in Chrome, or Playwright), or the project's end-to-end tests if not. Keep each command and the part of its output that shows the result.

### Step 3: Judge each criterion

Mark each criterion met, not met or not verifiable, with its evidence. For the customer view, walk each UX journey as the customer would and judge it against the PR/FAQ's promise it serves, not only against the letter of the criteria. Record each failure with `orchestra:feedback`, with `--found-by acceptance` when you are running acceptance on built work.

### Step 4: Write it up

Write the document so someone who was not there can rerun every check and see what you saw. List separately the checks that need a person, so the conductor can batch them for the user's review gate.
