---
name: research
description: Research the market, the users or the technology behind a product decision, through a named lens, and write the findings as a short Markdown document in which every factual claim carries a source or is marked as inference. Use when a brief or decision needs evidence about competitors, user needs, candidate technologies or technical risks, when a role is asked for discovery research, or when checking another agent's research for unsourced or contradictory claims.
---

# Research

Find the evidence a product or technical decision depends on, and write it so a skeptical reader can check every claim.

## Overview

This skill researches a question through one or more lenses and writes the findings to a Markdown file. The market lens asks who else solves the problem and how; the user lens asks who has the problem and how they cope today; the technical lens asks what could build it and what makes it hard. Every factual claim in the result carries a source, or is marked as the researcher's inference.

Research exists to change a decision. A survey of everything known about a topic costs its readers attention and changes nothing. Research that starts from the decisions in the brief, separates what the sources say from what the researcher concludes, and ends with what this means for the brief is something the next reader can act on, and argue with.

A good research document is short enough to read in one sitting. It answers the questions it was given, a reader can check any claim in a minute by following its source, inference is visibly inference, and the open questions at the end are decisions a user could make.

## When to use this skill

- A brief needs evidence about the market, the target users, or the technology before a decision is made.
- A role is asked for discovery research in a flow, through a market, user or technical lens.
- Another agent's research needs checking for claims without sources, or claims that contradict your own findings.

### When NOT to use this skill

- The answer is a single fact. Look it up and cite it inline.
- The question is about this codebase. Read the code.

## Constraints

- **A claim without a source is inference, and says so.** Mark it `[inference]`, and say what it rests on.
- **Prefer primary sources.** Official documentation, standards, source code, first-party data and the people who made a thing outrank articles about them. Say when only weaker sources exist.
- **Stay inside the lens you were given.** Note what belongs to another lens as an open question for its owner, rather than researching it.

## Inputs

- **The questions.** What decisions depend on this research. If the brief does not state them, derive them from the brief and list them at the top of the document.
- **The lens or lenses**: market, user, technical.
- **The artifact path** to write.

## Output

```markdown
# <Lens> research: <subject>

## Questions
<The questions this document answers, each tied to a decision in the brief.>

## Findings
<Grouped by question. Each claim cites its source as a link, or is marked [inference].>

## Implications for the brief
<What the findings mean for the decisions: what to do, what to avoid, what to test.>

## Open questions
<Decisions for the user, each with the options and your recommendation.>

## Sources
<Every source cited, with what it is and when it was accessed.>
```

## Workflow

### Step 1: Frame the questions

Read the brief and write down the decisions this research should inform, as questions. Keep the ones your lens can answer; pass the rest on as open questions. Decide what evidence would change each answer, so you know when to stop looking.

### Step 2: Gather evidence

Search for primary sources first and read them, not just their summaries in search results. Note each claim with its source as you go. When sources disagree, keep both and say which you trust more and why. Stop on a question once more evidence would not change the decision.

### Step 3: Write the findings

Write the document in the shape above. Lead each group of findings with the answer, then the evidence. Keep facts, inference and recommendation visibly apart. Before you finish, read it as a skeptic would: any claim you would challenge without a source needs one, or a mark.

### Step 4: Check another's research, when asked

When you are asked to check another role's research, read it against the exit criteria you were given and against your own findings. Look for claims without sources, sources that do not say what is claimed, and conclusions that contradict yours. Record each finding with the `orchestra:feedback` skill and return its verdict.
