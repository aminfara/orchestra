---
name: feasibility
description: Judge whether an idea or a requirement can be built and delivered with known techniques, naming the unproven parts and the smallest experiment that would settle each, and end with a verdict. Use when an idea is novel, when a PR/FAQ promise looks expensive or uncertain, or when a requirement is marked unknown by estimation. Not for choosing between known technologies, which is architecture.
---

# Feasibility

Decide whether something can be built, and find the cheapest way to learn what you do not know.

## Overview

This skill checks an idea or a requirement for the risk that it cannot be done, or not at a viable cost, with known techniques. It reads what is documented and proven, separates it from what is hoped for, and ends with a verdict and the smallest experiment that would settle any open question. It produces a paper judgment, not a design.

Most ideas are feasible with ordinary work, and the check should say so quickly. A few depend on something unproven, such as a capability no one has shipped, a data source that may not exist, a performance need beyond known systems, or a legal or platform limit. Finding that early is the point, because a market study and a PR/FAQ built on an impossible promise waste everyone's time.

A good feasibility check is short. It names each risky promise, what is known about it with sources, what is not, a verdict, and for each open question the smallest test that would answer it, with its cost.

## When to use this skill

- An idea is novel, meaning its builder doubts that known techniques can deliver it.
- A promise in a PR/FAQ or a requirement looks expensive or uncertain.
- Estimation marked a requirement unknown, and the answer could move the MVP cut line.

### When NOT to use this skill

- The question is which of several known technologies to use. That is architecture.
- The question is size. Use estimation.

## Constraints

- **Name the unproven part.** A verdict of "feasible" without saying what was checked and what it rests on is not a finding.
- **Sources or marked inference.** Follow the research skill's rule: every factual claim carries a source or is marked as inference.
- **Smallest test first.** Propose the cheapest experiment that settles a question, with its cost, before suggesting a build.
- **Stay on paper unless told otherwise.** Run a spike only when the brief asks for one.

## Inputs

- **The idea or the requirements** to check, and which promises look risky.
- **The brief** and any market research.
- **Existing architecture docs**, if the system exists.

## Output

A section of `research/feasibility.md` per risky promise: what is claimed, what is known and proven (with sources), what is unproven, the verdict (feasible, feasible with a stated risk, or not known to be feasible), and the smallest experiment with its cost. A one-line overall verdict at the top.

## Workflow

### Step 1: List the risky promises

From the brief, PR/FAQ or requirements, pick the promises that depend on something not routine. Leave the routine ones out and say so in one line.

### Step 2: Check what is known

For each promise, find what is documented, shipped or measured, using `orchestra:research` through the technical lens. Separate proven from hoped for.

### Step 3: Give the verdict and the test

Write the verdict for each, and for each open question the smallest experiment that settles it. End with the overall verdict.
