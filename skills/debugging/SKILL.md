---
name: debugging
description: Find the root cause of a defect or a symptom by first building a feedback loop that shows the failure on demand, recording the behaviour that must not change, then testing one hypothesis at a time against evidence, and stepping back to question the design when fixes keep failing. Use when a test, build or product misbehaves and the cause is not obvious, when fixing a reported bug, or when troubleshooting an outage, slowdown or broken environment. Not for writing new features, and not for reviewing someone else's change.
---

# Debugging

Make the failure happen on demand, then let evidence, not intuition, say why.

## Overview

This skill finds why something fails. For a known defect it ends in a failing regression test and a fix at the root cause. For a symptom with no known cause, such as an outage, a slowdown or a broken environment, it ends in a diagnosis: the cause, or the candidates that remain, with the evidence for each and a recommended next step.

Most wasted debugging time goes into hypotheses tested against nothing. Without a way to make the failure appear on demand, every guess looks plausible and every change looks like it might have helped. A feedback loop that goes red reliably turns debugging into an experiment: change one thing, run the loop, read the result. The same discipline protects what already works, because a fix that breaks behaviour someone relies on is a new defect.

A good outcome names the cause in a sentence that explains every observed symptom, shows the evidence that rules out the alternatives, and changes the code at the place where the wrong assumption lives rather than where the symptom surfaced. For a fix, a test that failed before and passes after guards it; for a diagnosis, someone else could rerun the evidence and reach the same conclusion.

## When to use this skill

- A test, a build or the product misbehaves and the cause is not obvious after a first look.
- A reported bug needs its root cause found and fixed.
- A symptom in a running system needs diagnosing: errors, slowness, a broken environment, a failure after a change.

### When NOT to use this skill

- The cause is obvious and the fix is one line. Fix it with a regression test under `orchestra:tdd-programming`.
- Reviewing someone else's change. Use review, and debug only a failure it finds.

## Constraints

- **No hypothesis before a feedback loop.** If the failure cannot be reproduced yet, making it reproducible is the work.
- **Change one thing at a time, and keep what you learn.** Every experiment's result goes into your notes, including the ones that ruled something out.
- **Protect the behaviour that must not change.** Record it before you fix anything, and check it after.
- **Diagnosing changes nothing you did not create.** Steps that touch production, shared data, infrastructure or files others left on the machine, cleanup included, go to the user as proposals.

## Workflow

### Step 1: Build the feedback loop

Find the fastest reliable way to see the failure: a failing test at the lowest level that shows it, a script, a request, a command against a copy of the data. For an intermittent failure, make it frequent enough to observe (loop it, add load, pin the timing) before explaining it. For a symptom in a running system, the loop may be a query over logs or metrics that shows the bad behaviour and when it started. Write down what the loop shows now; it is the baseline every experiment is judged against.

### Step 2: Record what must not change

List the behaviour around the failure that callers and users rely on, and make sure some test or check covers it. For a symptom, list what is known to work, so the search can narrow.

### Step 3: Narrow down with evidence

Gather the facts before the theories: the exact error and where it is raised, the inputs that trigger it and those that do not, and what changed between working and broken (commits, dependencies, configuration, data, load). Then rank hypotheses that each explain all the facts, and test the cheapest decisive one first: an assertion, a log line at a boundary, a bisect, a minimal input. Tag temporary instrumentation so it is easy to remove. Stop when one cause explains every symptom and the experiments rule out the others.

### Step 4: Step back when fixes keep failing

When a third attempted fix does not hold, or each fix moves the failure somewhere else, the problem is probably an assumption rather than a line of code. Stop patching. Write down what you believed about the design that the evidence contradicts, read the architecture doc and ADRs for the part involved, and report "needs a decision" if the fix would change the architecture.

### Step 5: Fix or report

For a defect, turn the reproduction into a regression test at the lowest level that catches it, see it fail, fix the cause with `orchestra:tdd-programming`, and run the whole affected suite plus the must-not-change checks. Remove the instrumentation. For a symptom, write the diagnosis: the cause or the ranked candidates, the evidence for and against each with the commands that produced it, what was ruled out, and the recommended next step, including any mitigation as a proposal.
