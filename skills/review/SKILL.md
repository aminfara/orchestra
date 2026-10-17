---
name: review
description: Review a code change against what it was meant to do, without the author's claims, through the lenses its risk calls for (function and quality always; security and performance when the change touches them), with evidence from running it, and triage each finding as fix now, defer, or back to the plan. Use when checking another engineer's change before it is integrated, or when asked to review a diff, branch or pull request. Not for reviewing documents, which the feedback skill's checks cover, or for acceptance of a whole milestone, which is verification.
---

# Review

Judge a change by what it does against what it was meant to do, and say exactly what must change before it lands.

## Overview

This skill reviews one code change: a diff against its base, with the story or defect it was meant to deliver. The reviewer reads the change, runs it, and returns a verdict with findings the author can act on alone. Every finding goes to the feedback ledger against the author's role and skill.

An author's account of a change is the least reliable evidence about it, because it describes what the author intended. Three frameworks found the same thing independently, and Orchestra builds it in: the reviewer gets the diff, the acceptance criteria and the docs, never the author's report. Review effort should follow risk. A small change inside one module needs a careful read through two lenses; a change to authentication or a hot query path needs the lens that knows where those go wrong.

A good review catches the problems that would otherwise reach acceptance or the user, and nothing else. Each finding says where it is, what it fails and why it matters; the verdict passes when nothing of medium or high severity is left; and the review is complete the first time, so a second round only confirms fixes.

## When to use this skill

- An engineer's change for a story or defect is ready, and must be checked before it is integrated.
- The user asks for a review of a diff, a branch or a pull request.

### When NOT to use this skill

- Documents such as a PRD or an architecture. Check those against their exit criteria with the feedback skill.
- A milestone's acceptance, where the whole product is run against its requirements. Use verification.
- Fixing the change. A reviewer who fixes what it reviews is no longer independent; report the finding instead.

## Constraints

- **Judge the change, not the author's account of it.** Work from the diff, the acceptance criteria and the docs; check every claim in code comments or commit messages.
- **Evidence over impression.** Run the tests and, where it matters, the product; a finding about behaviour names the command and what it showed.
- **Review what changed and what it touches.** Code the change did not affect is out of scope unless the change makes it wrong.
- **Severity follows effect.** High breaks an acceptance criterion, a security property or data; medium would make the next engineer or the user guess or work around it; low is polish.

## Inputs

- **The change:** a branch and the base it is compared against.
- **What it was for:** the story's acceptance criteria from the task store, or the defect and the behaviour that must not change.
- **The docs** the brief names: architecture sections, ADRs, the glossary, UX screens.
- **The ledger details** for the author.

## Output

A verdict, in the shape the feedback skill gives, plus an evidence line per command run. The findings themselves are in the ledger.

## Workflow

### Step 1: Know what the change must do

Read the acceptance criteria and the docs before the diff, and note what you expect to see: the behaviours, the edge cases real input reaches, and the parts of the architecture the change should and should not touch. Then read `git diff <base>...<branch>` and the files around it.

### Step 2: Choose the lenses

Function and quality apply to every change:

- **Function.** Does it do what each acceptance criterion says, including the empty, failing and concurrent cases? Do the tests check behaviour through the public interface, and would they fail if the behaviour broke? Where it is cheap, run the new tests against the base to see them fail.
- **Quality.** Does the code follow the programming principles in `orchestra:tdd-programming` and the project's conventions, keep module boundaries, use the glossary's terms, and read clearly to the next engineer?

Add a lens when the change's risk calls for it:

- **Security**, when it handles input from outside, authentication or authorization, secrets, or data another user owns: trust boundaries, injection, access checks on every path, secrets in code or logs.
- **Performance**, when it is on a hot path or works over data that grows: unbounded queries or loops, repeated calls inside loops, missing indexes, work that could block a request.

For a large or high-risk change, run each added lens in its own subagent with the diff and the criteria, and merge what they find.

### Step 3: Run it

Run the project's test suite on the change, and the linters and type checks it uses. When an acceptance criterion is about behaviour a user sees, exercise it through the product's real entry point as `orchestra:verification` describes. Record each command and what it showed.

### Step 4: Triage and record

Sort each finding: **fix now** when it blocks the change; **defer** when it is real but belongs in another story, which you name in the finding; **back to the plan** when the story's criteria or the architecture are what is wrong, which the conductor takes to the architect. Record every finding with `orchestra:feedback`, then write the verdict. Pass when no fix-now finding of medium or high severity is open.

### Step 5: Re-check narrowly

When the author revises, confirm each finding is fixed, resolve it in the ledger, and look only at what the revision changed. Keep a finding open if the fix did not address it.
