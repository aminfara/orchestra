---
name: feedback
description: Record findings from peer checks, reviews and user review gates in Orchestra's feedback ledger, a JSON Lines file, through a bundled script that stamps each finding with the role, skill version, model and effort that produced the work. Also guides a retro that reads the ledger and proposes concept-level changes to skills rather than one rule per finding. Use when checking another agent's artifact, when a user requests changes at a review gate, when closing a run and counting findings, or when running a retro over the ledger.
---

# Feedback

Record each finding where the team can learn from it, against the role, skill and model that produced the work.

## Overview

This skill writes findings to the project's feedback ledger, `.orchestra/feedback.jsonl`, through `scripts/feedback.py`. A finding is one problem a checker or the user found in an artifact. The script stamps it with the run, the phase, the role and craft skill that produced the artifact, the skill's version and length, the model and effort, who found it, a category, a severity, and the finder's one-sentence view of why it happened. Later events record whether it was fixed, deferred or overridden.

A finding fixed once and forgotten recurs. The ledger is how Orchestra notices that the same misunderstanding keeps producing the same kind of finding, and fixes it once in the skill, as a concept that covers a whole class of cases. That only works if each finding is specific, honestly classified, and carries a guess at its cause. The same ledger shows where review can be lighter or a model cheaper, so findings that did not happen matter too: a check that finds nothing is recorded in its verdict.

A good record lets someone who never saw the artifact understand what went wrong and why, from the finding and its cause alone. A good retro, run later over many records, ends with a few proposals that each explain several findings, and leaves most findings where they are.

## When to use this skill

- You are checking another agent's artifact against exit criteria, and need to record what you found.
- The user asks for changes at a review gate, and each requested change is a finding.
- A run is closing, and the conductor counts the findings since the last retro.
- A retro reads the ledger to propose changes to how the team works.

### When NOT to use this skill

- Notes to yourself, or a role's rulings. Those go in reports.
- Praise and preferences. A finding is a gap between the artifact and its criteria, the brief, or the facts.

## Constraints

- **One finding per problem, written for a reader who was not there.** Say where it is, what is wrong, and which criterion or fact it fails.
- **The cause is a guess, and that is the point.** Say in one sentence what the author seems to have misunderstood or missed, not what they should have done.
- **Check without the author's claims.** Judge the artifact against its criteria and inputs, never against the author's report of it.

## Inputs

From the brief that asked for the check, or from the conductor at a gate:

- **The ledger path, run ID, flow and phase.**
- **The author's role, craft skill, model and effort**, which the ledger records against the finding.
- **The artifact paths and exit criteria**, when checking.

## Output

Ledger events, one JSON object per line, written only by the script. A checker also returns a verdict to the conductor:

- **Verdict:** pass, or revise.
- **Findings:** a count by severity, with the ledger IDs.
- **For the author:** each finding in a sentence, specific enough to act on without you present.

## Workflow

### Step 1: Check the artifact

Read the artifact against its exit criteria and the inputs the author worked from. Note each problem with where it is and which criterion it fails. Classify it with one category: `gap` (something required is missing), `error` (something stated is wrong), `unsupported` (a claim without evidence), `inconsistent` (contradicts itself or another artifact), `unclear` (a reader who was not there cannot follow it), `scope` (beyond the brief or short of it), `infeasible`, or `other`. Rate its severity by its effect on the next reader: `high` if it breaks a promise or blocks the next role, `medium` if the next role would have to ask or guess, `low` if it is polish.

### Step 2: Record each finding

Record each finding with the script, which prints its ID:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/feedback.py record --ledger <ledger> \
  --run <run> --flow <flow> --phase <n> --artifact <path> \
  --role <author role> --skill <author skill> --model <model> --effort <effort> \
  --found-by <your role, or user> --category <category> --severity <severity> \
  --finding "<what is wrong, where>" --why "<what the author seems to have missed>"
```

Name the craft skill as `research` or `orchestra:research`, or `none` when no skill applies. When the findings are the user's comments on your own work, record each comment as the user made it, with `--found-by user`; there is no artifact to check first. When you check a revision, resolve each finding your brief lists, yours or the user's, that the revision fixed, with `resolve --ledger <ledger> --id <id> --outcome fixed`; findings it did not fix stay open. When the user defers or overrides a finding at a gate, the conductor resolves it as `deferred` or `overridden`.

### Step 3: Return the verdict

Write the verdict in the shape above to the path in your brief, and return the same text. Pass when no finding of high or medium severity remains open; otherwise ask for a revision.

## Reference files

- `scripts/feedback.py`: the ledger script. `count` gives findings since the last retro; `summary` groups them for a retro; `cost` records rework rounds and tokens for a phase; `retro` marks a retro done.
- `references/retro.md`: how to read the ledger and turn recurring findings into proposals. Read only when running a retro.
