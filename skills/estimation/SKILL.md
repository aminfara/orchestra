---
name: estimation
description: Size requirements as small, medium or large and flag the ones nobody can size yet, using the existing architecture doc and glossary when the system already exists, or comparable work when it does not. Use when ranking requirements by value against ease, when a PRD needs effort and risk per requirement, or when a scope cut needs a rough cost. Not for task-level planning or a detailed design.
---

# Estimation

Size each requirement well enough to rank it, and say which ones cannot be sized yet.

## Overview

This skill gives every requirement a size (small, medium or large), a risk note, and a confidence (sized, guessed or unknown), without designing the system. It is a ranking tool: the sizes decide the order and the MVP cut line, and the architecture work later replaces them with real numbers.

A designed system is not needed to tell a day of work from a month. When an architecture doc and glossary exist, they show which parts a requirement touches and how much of it is already there. When none exists, comparable work does the same job: a login screen, a sync engine and a payment flow have known weights. Where neither helps, the honest answer is "unknown", which is a finding worth more than a confident guess.

A good estimate fits on one line per requirement, shows what it rests on, and separates the requirements it is sure about from the ones it is not. Large and unknown items name the question that would settle them.

## When to use this skill

- A PRD needs effort and risk per requirement before ranking by value against ease.
- A scope cut or an MVP boundary needs a rough cost per candidate.
- A request changes and the PRD's sizes need a quick refresh.

### When NOT to use this skill

- Breaking a story into tasks. Use planning.
- Settling whether something can be built at all. Use feasibility.
- Designing the system to find out what it costs. That is the architecture flow's job.

## Constraints

- **Rank, do not predict.** Sizes mean small (a day or two), medium (about a week) or large (more than a week or several parts), never dates or hours.
- **Show the basis.** Each size names the part of the existing system it touches or the comparable work it resembles. A size with no basis is "guessed".
- **Say unknown when it is.** A requirement with a hard unknown gets confidence "unknown" and the question that would settle it, not a padded size.
- **Stay shallow.** Reading the architecture doc and glossary is enough. Open code only to settle a size that would change the ranking.

## Inputs

- **The requirements**, each with its what and its definition of done.
- **The architecture doc and glossary**, if the system exists.
- **Any feasibility findings** already written for the idea.

## Output

One line per requirement in the PRD's effort column: size, confidence, basis, and for large or unknown items the question that would settle it. A short list of the requirements that need a spike before the cut line can be trusted.

## Workflow

### Step 1: Gather the basis

Read the architecture doc and glossary if they exist and note which parts each requirement touches. Where they do not exist, pick comparable work for each requirement.

### Step 2: Size and flag

Assign a size from the basis, a confidence, and any risk that would raise the size (new technology, an external dependency, a data migration, an unproven performance need). Mark what you cannot size.

### Step 3: Name the spikes

List the large or unknown requirements whose size could change the MVP cut line, and write the single question a spike must answer for them. The rest keep their rough size, and the architecture flow replaces it with real numbers.
