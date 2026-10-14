---
name: briefing
description: Interview the user to turn an idea, findings or trade-offs into a written brief, asking batched, self-contained questions through AskUserQuestion with a recommended answer for each. The agent finds facts itself and asks the user only for decisions and for what only the user knows. Use when a brief, requirements or decisions must come from the user before work starts, when research or design reports raise questions only the user can answer, or when the conductor reaches a briefing checkpoint.
---

# Briefing

Interview the user until the brief can be written without guessing, asking only what the user alone can answer.

## Overview

Briefing turns what the user knows and wants into a written brief that other agents can work from. It asks questions in batches through the AskUserQuestion tool, each question carrying its own context and a recommended answer, and it writes the answers down as decisions, not as a transcript.

A user's attention is the scarcest thing in a run. Questions that the agent could have answered itself, questions that only make sense with the last ten minutes of conversation in mind, and questions without a recommendation all spend that attention badly. The rule of thumb that drives this skill is that the agent finds facts and the user makes decisions.

A good briefing is short. The user answers a few batches, each answerable on its own, and the resulting brief lets a reader who was not there know what is being built, for whom, what is ruled out, and which assumptions were accepted rather than decided.

## When to use this skill

- A flow reaches a briefing checkpoint: intake, findings after research, or technical intake.
- Reports from roles carry questions for the user, and they need answers before the next phase.
- Any task that cannot start well until the user has made decisions only they can make.

### When NOT to use this skill

- The question is a fact you can find in the repository, the reports, or the web. Find it.
- A single yes-or-no confirmation in the middle of other work. Ask it directly.

## Constraints

- **Ask for decisions and private knowledge only.** Goals, priorities, taste, constraints and trade-offs belong to the user; facts belong to you.
- **Every question stands alone.** It says what is being decided and why it matters, without leaning on earlier discussion, and leads with a recommendation marked as such.
- **Write decisions, not conversation.** The brief records what was decided and the reason, in the user's terms.

## Inputs

- **What the brief must cover.** The flow phase names the sections, or the task implies them.
- **What is already known.** The existing brief, reports from roles, and anything the user has already said.

## Output

The brief, or an update to it, at the path the flow names. Each section holds a decision, an assumption the user accepted (marked as such), or an open question with who will answer it.

## Workflow

### Step 1: Find out what you already know

Read the existing brief and the reports you were given, and look up the facts you can. List what the brief still needs. For each gap, decide whether it is a fact you can find or a decision the user must make; only the second kind becomes a question.

### Step 2: Ask in batches

Group the remaining questions so that each AskUserQuestion call holds the ones that can be answered together, and ask first the questions whose answers change the others. Write each question so a reader seeing only it can answer well:

- the decision, in one sentence, ending with a question mark;
- why it matters: what changes downstream depending on the answer;
- the options, with the recommended one first and labelled "(Recommended)", and a short description of what each implies.

When a report carries the question, use the role's recommendation and reasoning, rewritten so it stands alone. When an answer opens a new question, add it to the next batch. Stop asking once every gap is decided, accepted as an assumption, or knowingly left open, and close the last batch with one open question: is there anything else the user wants to add, with "No" as the recommended answer.

### Step 3: Write the brief

Write or update the brief from the answers. State each decision plainly with its reason; mark assumptions as assumptions; list open questions with who answers them and by when. Tell the user what changed in the brief, in a sentence or two, so they can correct it. This is not a gate: the user has just made these decisions, so carry on unless they correct you.
