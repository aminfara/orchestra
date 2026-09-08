# Format: Poster (Program / Project)

A poster is the durable front door to an established program or project: one to two pages that state what it is, why it exists, which company goal it ladders up to, what is in and out of scope, and the tenets by which the team decides. It orients a reader who arrives knowing nothing, and it stands on its own well enough that an executive can read it cold and correctly describe the work to someone else.

A poster does not seek a decision. The decision was already taken; the poster records the settled *what* and *why* so that nobody has to re-derive them from a chat thread.

A poster is also not a reporting mechanism. It carries the definition of the work, not its condition. That is the line that governs every choice below.

## When to use vs. adjacent formats

- **Poster** (this format): the program or project already exists and you want a stable page a newcomer, a partner team, or an exec can read in three minutes to understand what it is and why it matters.
- **Proposal** (`proposal/`): you want a decision — approve, fund, pick this option. If the text argues, weighs alternatives, or ends in an ask, it is a proposal. A poster often *links* to the proposal that created the program.
- **Status update**: what changed recently and whether the work is on track. Time-bound by nature. A poster links to the live status surface; it never contains status.
- **RACI** (`raci/`): who is responsible, accountable, consulted, informed, in detail. A poster names the owner and sponsor and links to the RACI; it does not reproduce the matrix.
- **RFC / design doc**: how the thing is built. A poster stays above the architecture.

Disambiguating question: **is this the definition of the work, or its current condition?** Definition belongs on the poster. Condition belongs on a status page, a roadmap, or a board, and the poster links to it.

One adjacent artifact shares the name and causes real confusion. Several planning traditions use "poster" for a *workshop* artifact: a wall-chart a team fills in over several sessions to interrogate a problem, test assumptions, and decide whether to proceed. That version is pre-decision and deliberately churns — it has sections like "what we still need to find out". This format is the opposite end of the lifecycle. If the user wants to validate a problem, stress-test assumptions, or run a team session, they want the workshop version; say so and use its structure, not this one.

### On the name

"Poster" is the term most teams reach for, so this format answers to it. Treat it as answering equally to **program brief**, **program overview**, **program profile**, and **project charter**, since all four describe the same artifact in different houses. Two cautions when the user picks a name: a *charter* elsewhere usually means an approval artifact with a sign-off block, which this is not, and *one-pager* is already a completeness level on other formats in this skill, so avoid it here.

### Variants

Two flavors, differing in one section only:

- **Program poster** — the work is a set of related projects or workstreams pursued over multiple quarters or years. "Shape of the work" lists the constituent workstreams.
- **Project poster** — the work is a single bounded effort. "Shape of the work" lists the major phases instead.

Pick by asking: does this thing contain other named pieces of work that have their own owners? If yes, program.

### When a poster is warranted

Do not write one for small work; an unread poster is worse than no poster. The gate: the work runs longer than about a month, involves people outside the immediate team, or a leader has asked for visibility into it. If none of those hold, a paragraph on the team's page is enough.

## Default axes

- **Purpose:** orient and inform. Give a cold reader a bird's-eye view of the work and why the company is doing it.
- **Tone:** neutral and declarative. Descriptive, not persuasive; the argument is over. Confident about scope and tenets, plain about everything else.
- **Medium:** a wiki or intranet page, usually the parent page of the program's space or the top of its project tree. Headings, a short metadata table, and links out.
- **Audience:** anyone who lands on the program cold — new joiners, partner and dependent teams, leadership doing portfolio review, auditors of scope. Assume no prior context and no patience. Write for someone meeting the work for the first time: no assumed context, and lead with what the work delivers rather than the history of how it came to be.

## Inputs to collect

Gather these before drafting. Infer silently when clear; ask only when a key input is genuinely unclear.

- **variant** (required) — program or project (see Variants).
- **name and one-line description** (required) — the official name, spelled the way the org spells it.
- **why it exists, and why now** (required) — the problem or opportunity, and the reason the company decided to spend on it. Ask for *why now* as a separate question; it is the point most often missing and the one that explains the work's urgency.
- **goal linkage** (required) — the **exact name and wording** of the company or org goal, objective, or key result this ladders up to, plus the identifier of its canonical record. Ask for the real text; do not paraphrase from memory and never invent a goal name or key (A9, A12).
- **owner and sponsor** (required) — the single accountable owner (role plus person), sometimes called the directly responsible individual (DRI), and the executive sponsor.
- **scope in / out** (required) — what the work covers, and at least two things people reasonably assume it covers but it does not.
- **success measures** (required) — the outcome-level measures the work is judged on over its lifetime, not this quarter's target. Ask specifically for a **guardrail measure**: the metric that must not regress.
- **tenets source** (required for tenets) — either existing tenets, or the raw material to derive them. To get the raw material, ask: *what do you and the team keep re-arguing?* and *what trade-off have you already settled that a new joiner would get wrong?* Tenets come from settled arguments, not from values posters.
- **shape of the work** (required) — the constituent workstreams (program) or major phases (project), one line each, each with its owning team.
- **links** (required) — live status surface, backlog or board, the founding proposal or decision doc, the team channel, the RACI if one exists.
- **durable constraints** (optional) — a fixed regulatory date, a hard budget envelope, a platform the work must build on. Include only if it will hold for the lifetime.
- **glossary terms** (required) — every program-specific term, acronym, internal codename, and system name that will appear on the page. Ask for these explicitly; authors are the worst judges of which of their own words are jargon, so collect the candidate list and prune it rather than waiting for the user to volunteer terms.

## The orientation contract

A poster is only a poster if a reader who has never heard of the work can finish it and correctly answer all six:

1. What is this?
2. Why does it exist, and why now?
3. Which company goal does it ladder up to, and what does it contribute to that goal?
4. What is in scope, and what is deliberately out?
5. How will we know it worked?
6. Who owns it, and where do I go for current detail?

Six of the template's sections exist to answer these, one each. Three more earn their place separately: "Tenets" and "Shape of the work" make the work's judgement and its structure legible, and the "Glossary" is what lets the page answer its own vocabulary. Every section in the template is mandatory. If an input is missing, mark it `[CLARIFY: ...]` rather than dropping the section. A visible gap tells the reader something is unresolved; a missing section tells them nothing.

The contract has a second half: the reader must be able to answer all six **without opening a link and without asking anyone**. Links are for going deeper, not for completing the story, and an unexplained term is the same dependency in a smaller package. A poster that only makes sense alongside three other pages, or alongside someone who can translate its vocabulary, has failed at the one job that distinguishes it.

## The durability rule

A poster is revised when the *definition* of the work changes — its scope, its owner, its tenets, or the goal it serves. It is not revised because time passed or numbers moved. In practice, aim for a page whose every sentence is still true a year from now, and expect to touch it a small number of times across the work's life.

This is not the same as a page that never changes, and it is not an excuse to leave a stale page up. It is a rule about *what kind of fact* the poster is allowed to carry.

So move anything whose truth expires off the poster and link to it: current status, RAG colour and lifecycle phase, percent complete, sprint or quarter names, this quarter's key-result targets, live risks and their mitigations, named individuals below owner and sponsor, current headcount, dated milestones, open questions.

Three mechanical consequences:

- Carry a review stamp in the header — **last reviewed** and **next review**, six months apart — so staleness is visible rather than silent. The review asks one question: has the definition changed?
- Prefer naming a measure ("time to first successful call") over stating its current value ("down to 4.2 minutes"). The name is durable; the value is not.
- Where the poster is the parent page of a tree, say so: *"This page is the program's source of truth. If scope, ownership, or the goal it serves changes here, update the affected child pages at the same time."*

## Template

```text
# [Program or project name]

[One sentence: what this is, for whom. This is the line people will quote in other documents.]

## At a glance

| | |
|---|---|
| **Type** | Program / Project |
| **Owner** | [Role — Name] |
| **Executive sponsor** | [Role — Name] |
| **Contributing teams** | [teams, not individuals] |
| **Ladders up to** | [exact goal / objective / key-result name] |
| **Canonical record** | [link to the project or goal record] |
| **Started** | [YYYY-MM] |
| **Horizon** | [e.g. multi-year, or "through FY27"] |
| **Live status** | [link — never a status value] |
| **Team channel** | [link] |
| **Last reviewed / Next review** | [YYYY-MM] / [YYYY-MM] |

## What this is

[Two to four sentences a newcomer can read once and then repeat accurately to someone
else. Concrete nouns. No vision vocabulary. Lead with what the work delivers, not the
history. If the reader still cannot picture the work after this paragraph, the paragraph
has failed.]

## Why it exists

[The problem or opportunity in the world, and why the company chose to spend on it.
State it as settled fact, not as an argument. Two to four sentences. Then one sentence on
**why now**: what changed that made this the moment. Include the cost of the status quo
only if it is a durable fact rather than a projection that will age.]

## How this ladders up

[Name the exact goal or key result, then state what this work contributes to it: the
mechanism, not the fact of alignment. "Aligns with Objective 3" is a name-drop;
"Objective 3 targets X; this program moves X by doing Y" is a line of sight.

For a program serving a large company objective, the strongest shape is a two-column
table mapping each thing the objective asks for to what this program delivers:

| What [goal name] asks for | What this program contributes |
|---|---|
| [ask] | [contribution] |

One short paragraph is enough for a project. Two goals is usually the honest maximum;
four means the connection to each is weak.]

## Tenets

[Three to five numbered trade-off statements that predict how the team decides. See
"Writing tenets" below. Number them so people can cite them, and close with the line
that keeps them open to challenge.]

1. [Tenet]
2. [Tenet]
3. [Tenet]

These are our tenets unless we find better ones.

## Scope

**In scope:** [what the work covers, at the level of capability or outcome, not task.]

**Out of scope:** [at least two things a reasonable reader would assume are included but
are not, each with a half-sentence on where that work lives instead. This list is what
makes the scope real and what stops adjacent teams assuming you cover their problem.]

## What success looks like

[The outcome-level measures the work is judged on across its lifetime, named rather than
valued. Include a guardrail.

- **Primary:** [the measure that decides whether this worked.]
- **Supporting:** [one or two others.]
- **Guardrail:** [the measure that must not regress, and the threshold that would force
  a rethink.]

Where a lifetime target genuinely exists and is fixed, state it as
metric = [baseline] → [target] by [date]. Otherwise name the measure and its direction
and link to the live target.]

## Shape of the work

[Program: one line per workstream — name, what it covers, owning team, link.
Project: one line per phase — name, what it delivers, rough sequence.
This is the bird's-eye view. No dates, no percentages, no status.]

## Who's involved

[Owner, executive sponsor, contributing teams, and the forum where decisions on this work
get made. Link to the RACI or DACI rather than reproducing it.]

## Where to go next

[A link block: live status, board or backlog, the founding proposal or decision doc, team
channel, deeper design docs. This is the poster's job as a hub: get the reader to the
right next page in one hop.]

## Glossary

[Every program-specific term, acronym, internal codename, and system name used on this
page, one line each. Two to eight entries is typical. A reader who lands mid-page must be
able to resolve any unfamiliar word here rather than by asking someone.

If the work genuinely has no specialist vocabulary, keep the heading and say so: "None —
this page uses no program-specific terminology." That is a useful statement, and it is
also a prompt to check again, because a program with zero jargon is rare.]
```

## Writing tenets

Tenets are the hardest section and the one most often written badly. A tenet resolves a tension between two genuine goods, so that someone facing that tension can decide without escalating. Tenets are the team's rubric for hard calls, which is why they read as trade-offs rather than aspirations.

Three shapes that work:

- "We favour [X] over [Y], even when [Y] is faster or cheaper."
- "When forced to choose between [X] and [Y], we choose [X]."
- "We accept [concrete cost] in order to get [concrete benefit]."

Two tests every tenet must pass:

- **The reversal test.** Could a competent team hold the opposite tenet and still be sensible? If not, it is a platitude. "We value quality" fails; nobody argues for low quality. "We ship a narrow capability completely before a broad one partially" passes, because the opposite is a real strategy.
- **The decision test.** Name a specific decision this tenet would have settled. If you cannot, cut it.

Conventions: three to five tenets, numbered. Close with *"these are our tenets unless we find better ones"* — it invites challenge and signals the list is owned rather than handed down. A tenet set nobody may argue with stops getting used. Do not restate company values as program tenets; a tenet is specific to this work.

## Rules for this format

- **Enforce:**
  - A1 (lead with the point) — the one-sentence description under the title, then "What this is", carry the whole message for a reader who stops there.
  - A2 and A13 (be clear, expand abbreviations) — hard, and doubled. Every program-specific term and acronym gets expanded at first use *and* listed in the glossary. The redundancy is deliberate: readers scan a poster and jump to the middle section they care about, so first-use expansion alone strands them.
  - A3 (be specific) — abstraction is the enemy of a poster. "Improve the developer experience" describes nothing.
  - A9 (never fabricate) — the goal name, its record identifier, the owner, the sponsor, and the measures must be real. An invented goal reference is worse than a gap, because other documents will copy it.
  - A12 (canonical names) — the poster is where the rest of the org copies the program's name, the goal's name, and the team names from. Get them exactly right.
  - A14 (prose for ideas, lists for things) — "What this is", "Why it exists", and the laddering are prose. Scope, workstreams, tenets, measures, and links are lists.
- **Relax:**
  - B1 (quantify the impact) — partially, and deliberately. Name the measures; do not carry current values or this quarter's targets, which expire (see the durability rule). Durable baselines and lifetime targets are welcome.
  - B2 (forward-looking framing) — a poster is descriptive rather than motivational. State the problem plainly; do not sell.
  - B5 (persuasive section titles) — neutral, scannable headings. Readers navigate this page by heading.
- **Watch:**
  - **The poster that is secretly a proposal.** Arguing for the work, weighing alternatives, or ending in an ask. The decision is already made; describe, do not persuade. If the user's material is all argument, tell them they want a proposal.
  - **The poster that is secretly a status report.** Dates, RAG colours, lifecycle phase, percent complete, current risks, sprint names. This is the most common failure by a wide margin, because a poster is often the page leadership visits, so status accretes onto it. Link instead.
  - **Business as usual in disguise.** If "What this is" would be equally true of the team's work before the program existed, the problem was never interrogated and the poster has nothing to say.
  - **Vision-word soup.** "Transform", "world-class", "seamless", "next-generation", "unlock". A cold reader learns nothing from these and a skeptical one stops reading. Replace each with the concrete noun it stands in for.
  - **Laddering by name-drop.** "Aligns with Objective 3" with no contribution mechanism. Also watch for laddering to four goals, which usually means each connection is weak.
  - **Scope with no out-of-scope.** The most valuable section is the shortest one to skip.
  - **Fake tenets.** Platitudes that fail the reversal test, or company values copied down a level.
  - **Load-bearing links.** A page that only makes sense once you have opened three others fails the second half of the orientation contract.
  - **A glossary that defines the easy words.** Expanding a well-known industry acronym while leaving the program's own codenames and internal system names unexplained is the usual shape of this failure. The test is not "is this term technical", it is "would a competent outsider know it".
  - **Assumed context.** Referring to a prior initiative, reorg, or debate the reader was not part of, without a clause explaining it.
  - **Duplication.** Reproducing the RACI, the roadmap, or the design doc inside the poster. Every duplicated fact is a fact that will diverge. Link.
  - **Named individuals below owner and sponsor.** People move; the poster then lies about who to ask. Name teams and roles.
  - **No review stamp.** Without one, the reader has no way to judge whether to trust the page.
- **Length:** 450 to 700 words of prose, hard cap 800, excluding the At-a-glance table, the link block, and the glossary. Those three are reference matter that a reader consults rather than reads, so they do not compete with the prose budget. That lands at one to two pages. If the content will not fit, cut depth from "Shape of the work" first, then compress "Why it exists"; do not cut a section and do not raise the cap. The glossary is never the thing you trim, since it is what the length discipline depends on: terse prose is only readable when its vocabulary is resolved somewhere on the page. A program too large to describe in 800 words is usually two programs, and worth saying so.

## Quick checklist before presenting

1. Can a reader with zero context answer all six questions in the orientation contract, without opening a link and without asking anyone what a word means?
2. Does every sentence carry a definition rather than a condition? Move anything whose truth expires.
3. Is the goal named in the org's exact wording, with a stated contribution mechanism rather than a name-drop?
4. Does each tenet pass the reversal test and the decision test, and does the set close with the invitation to challenge it?
5. Does "Out of scope" name at least two things a reader would otherwise assume are included?
6. Are success measures named rather than carrying this quarter's values, and is there a guardrail?
7. Is every program-specific term, acronym, codename, and system name on the page expanded at first use and present in the glossary? Read the page as an outsider and list what you could not resolve.
8. Are individuals named only at owner and sponsor level, with teams and roles everywhere else?
9. Does the header carry last-reviewed and next-review dates?
10. Would "What this is" still be true of the team's work before this program existed? If yes, rewrite it.
11. Is the prose within 800 words, and does it read as description rather than argument?
12. Did you run the ai-patterns pass?
