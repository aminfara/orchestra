# Format: RACI (base)

A RACI names, for each activity in a body of work, who does it (**R**esponsible), who owns the result (**A**ccountable), whose input is needed before it lands (**C**onsulted), and who is told after (**I**nformed). It exists to remove "who's got this?" from work that several people touch.

A RACI is a **clarity artifact, not a liability register**. Its job is to make it easier for people to do the right thing, not easier for them to say "not my job". Every letter carries a duty; no letter is an exemption. That principle is not decoration on this format — it drives the mandatory sections and most of the rules below. See "The ownership clause".

This is the **base** file: what a RACI is, when to use it, the default axes, the legend, the ownership clause, the section library, and the rules. It does not prescribe how much to write. That depends on **completeness level** (below). Always load this base plus exactly one level file.

## When to use vs. adjacent formats

- **RACI** (this format): a scope of work with *several activities* and *several parties*, where ownership per activity is the thing in question. Also used for standing, recurring duties across two teams with a seam between them.
- **DACI** (decision framework): *one* decision, now — Driver, Approver, Contributors, Informed. If what you are clarifying is a single call, write a DACI, not a RACI.
- **Roles and responsibilities charter**: whole-role ownership for a standing team ("what does each role own"), not activity-by-activity for a defined scope. Often the workshop output that a RACI is then distilled from.
- **Project one-pager / status update**: delivery governance — dates, progress, risks. A RACI answers *who*, not *when* or *how it is going*. Do not let it drift into a plan.
- **On-call or escalation runbook**: who to page during a live event. A RACI can name the escalation path for decisions, but it is not an incident response path.

Disambiguating question: *is there a list of activities, or a single call to make?* Several activities → RACI. One call → DACI.

**Variants.** RASCI adds **S**upport (helps the R without owning a deliverable); RACI-VS adds **V**erify and **S**ign-off for regulated work. Only introduce a variant if the user asks or the domain requires it. Every added letter costs clarity, and the failure modes below get worse, not better, with more letters.

## Completeness levels

The same RACI is legitimately written at two depths. Beyond the second, it stops being a RACI and becomes an operating model document.

- **Prose** (`raci-prose.md`) — a few lines of plain text in Slack, email, or a comment. Survives copy-paste, no tables, read in the flow of work. Also the right level for socializing a draft before it becomes a page.
- **One-pager** (`raci-onepager.md`) — the durable artifact on a wiki or doc page: the matrix as a table, plus legend, decision rights, escalation, and gaps. "One-pager" is conceptual, not physical: the framing sections stay to about a page of reading, while the activity table runs as long as the work genuinely needs.

Resolve the level from the request (see SKILL.md). "Drop a note in the channel on who owns what" → prose. "Write up the RACI for the migration" → one-pager. Load the base plus the matching level file only.

## Default axes

- **Purpose:** document ownership and get agreement on it. Informational and coordinating, not persuasive.
- **Tone:** neutral, factual, plain. Flat and unhedged: a RACI that reads diplomatically usually reads ambiguously.
- **Medium:** prose level → chat or email; one-pager → wiki page or document. Copy-paste survivability is a hard constraint at prose level (see the level file).
- **Audience:** the named parties themselves, plus whoever joins the work later. They skim to find their own name and stop, so every row must be readable standalone. Assume they will not read the legend.

## Inputs to collect

Gather these before generating or reviewing. Infer silently when clear; ask when the scope boundary or the overall accountable owner is unclear, since guessing either produces a wrong artifact.

- **mode** (required) — `generate` (build a RACI from raw context) or `review` (critique an existing one).
- **level** (required) — `prose` or `onepager`. Infer from the request and the medium.
- **scope** (required) — the work this RACI covers, and explicitly what it does **not** cover. Most RACI arguments are boundary arguments in disguise.
- **activities** (required) — the deliverables, decisions, and recurring duties to assign. Verb-led, each with an identifiable output.
- **parties** (required) — role title plus named person for each party. Note where a party is a team rather than a person.
- **overall accountable owner** (required) — the single person accountable for the whole scope. An unresolved overall A is the most common defect in a RACI; ask rather than assign one by inference.
- **consult and inform expectations** (optional, valuable) — how and by when C's input is wanted; what I's receive and on what cadence. Without this, C and I are decorative.
- **decision rights and escalation** (optional, valuable) — default decider per recurring decision area, and where it goes when stuck.
- **cadence and maintainer** (optional) — who keeps this current and when it is reviewed.
- **existing_raci** (review mode) — the current matrix or text.
- **collaboration status** (optional) — was this agreed in a workshop, or is it a draft one person wrote? This changes how the artifact must be framed (see the ownership clause).

## The legend, written as duties

Each letter is a job, not a label. Generate the legend with the duty stated, not just the definition — the duty column is what stops a letter from becoming a shield.

| Letter | Role | The duty it carries | What it is not |
| --- | --- | --- | --- |
| **R** | Responsible | Does the work and produces the output. At least one per activity; when there are several, name the lead. | Not a helper with no deliverable (that is S, in RASCI). |
| **A** | Accountable | Owns the result, decides, removes blockers, answers for the outcome. Exactly one per activity, and a person, not a team. May delegate the work, never the answerability. | Not a rubber stamp, and not a designated blame target. |
| **C** | Consulted | Owes a considered opinion, before the work lands, by the stated date. Two-way. Having been consulted, does not re-litigate the outcome afterwards. | Not a veto. A voice, not a vote. |
| **I** | Informed | Owes reading what they are sent. One-way after the fact — but still owes a flag if they see a problem. | Not a licence to be surprised later. |
| *(blank)* | Not involved here | Still on the same team. Silence about a risk you can see is never covered by absence from a row. | Not "none of my business". |

**Accountability needs matching authority.** If the person in the A cell cannot unblock the work, reallocate effort, or make the call, the assignment is wrong. Fix the authority or move the A; do not ship a RACI that names someone answerable for something they cannot influence.

## The ownership clause

RACI's two famous failure modes are mirror images. Under-specify and everyone assumes someone else has it. Over-specify and the chart becomes a way to decline work ("I'm only C on that") or a map of who to blame after a miss. This format treats the second as the greater risk, because it is the one a well-made matrix causes.

Three structural counters. All three are **mandatory at both levels**, including prose.

1. **Lead with the shared outcome, not the split.** One sentence naming the outcome every listed party is jointly aiming at, placed before any letters appear. The RACI divides the work; it does not divide the goal.
2. **Define letters as duties** (the legend above), so each row tells a reader what they owe, not just what they are off the hook for.
3. **Invite people to cross rows.** One explicit line stating that raising a problem in someone else's row is expected, not overstepping, and naming where to raise it. Without this line, a RACI teaches people to look away.

Four further rules that follow from it:

- **Assign letters to activities, never to identities.** "You are the A on cutover sign-off", never "you are an A". A letter attached to a person becomes a rank; a letter attached to an activity stays a job.
- **Surface gaps; never let an omission stand in for an owner.** Any activity with no owner is written down explicitly as UNASSIGNED, with a proposed owner and a date to resolve it. Silence reads as "someone is handling it", and nobody is.
- **Write for use before the work, not for use after it.** If a RACI is being cited for the first time in a post-mortem, it failed as a clarity tool and is now functioning as a weapon. Optimize the artifact for the person deciding what to do on Tuesday.
- **Propose, do not impose.** Unless the assignments came out of a workshop with the parties, say plainly that it is a draft and ask for corrections by a date. A RACI written alone and announced is the single most reliable way to trigger the "not my job" reflex it was meant to prevent.

**Do not launder reality.** If the person marked C is in fact doing the design, they are an R. A matrix that flatters the org chart produces false clarity: the team ticks the exercise off and then carries on with their own interpretations. Write what actually happens, or fix what happens and then write it.

## Section library

Every section a RACI can contain, defined once. Level files say **which sections to include and at what depth**; they do not redefine meaning. Three are mandatory at every level: shared outcome, assignments, and how to challenge this.

- **Scope and boundary** — the work covered and, explicitly, what is out. Name the time window if the RACI is phase-specific.
- **Shared outcome** (mandatory) — one or two sentences: the result everyone named is jointly aiming at. Comes before any letters.
- **Context header** — overall accountable owner, maintainer of the document, last reviewed, review cadence, status.
- **Legend** — the duty-framed table above. Full table at one-pager level; compressed to a half-line, or dropped, in prose.
- **Parties key** — role title → named person. Keeps the matrix cells role-based so the artifact survives a re-org.
- **Assignments** (mandatory) — the matrix (one-pager) or one line per activity (prose). Exactly one A per activity; at least one R.
- **Consult and inform expectations** — how C's input is collected and by when; what I's get, through which channel, on what cadence. This is what makes C and I real rather than ornamental.
- **Decision rights and escalation** — default decider per recurring decision area, who is consulted, and the escalation path when it stalls.
- **Gaps and unassigned** — activities with no owner, each with a proposed owner and a resolve-by date. Also flag any party carrying an implausible share of the R's.
- **How to challenge this** (mandatory) — corrections invited, to whom, by when, plus the cross-row flagging line from the ownership clause.
- **Change log** — date, what changed, who changed it. One-pager only; a RACI is a living document and a stale one is worse than none.

## Rules for this format

- **Enforce:**
  - A1 and B3 (answer-first) — scope and the overall accountable owner come first. A reader looking for their own name should not have to hunt.
  - A3 (be specific) — activities are verb-led with an identifiable output ("publish the weekly launch update", not "communications"); parties are named; consult windows carry real dates.
  - A5 (active voice, name the actor) — the whole format is actor-naming. "Priya runs the migration", never "the migration will be run".
  - A12 (canonical names) — spell every person, team, role, and product the same way throughout. A RACI is copied into other documents; inconsistent names propagate.
  - A9 (never fabricate) — do not invent a person, role, team, date, or cadence to complete the grid. Unowned work is UNASSIGNED; unknown facts get `[CLARIFY: ...]`.
  - A13 (expand abbreviations) — expand internal team and system acronyms on first use; the later joiner reading this will not know them.
- **Relax:**
  - B1 (quantify impact) — a RACI has little to quantify. Apply it only to the operational numbers that matter: consult deadlines, inform cadence, review cadence.
  - B5 (persuasive section titles) — neutral, scannable headings. This is a reference document.
  - A14 (prose for ideas, lists for things) — the assignments genuinely are an enumeration of discrete things, so a table or a line list is correct here. The framing sections around it stay prose.
- **Watch:**
  - **Two A's, or none.** The defining defect. Two A's means nobody decides and each waits for the other; none means the work has no owner at all.
  - **No R.** An activity with an A and no R is a wish.
  - **C inflation.** The most common failure in practice: a C for everyone who might have an opinion. Every C adds latency and a stakeholder who expects to be waited for. If someone only needs the result, they are an I.
  - **A team in the A cell.** "Platform team" cannot be answerable. Name a person.
  - **Names without roles.** A matrix keyed only to individuals rots at the first re-org.
  - **Letters that contradict how the work runs** — see "do not launder reality" above.
  - **Drift into a plan.** Dates, milestones, and status do not belong here beyond consult windows and review cadence. That is a different document.
  - **A matrix nobody will read.** Length is a correctness problem: an unread matrix assigns nothing.
  - **Blame framing.** Any sentence about what happens when someone fails their row belongs in a different conversation, not in the artifact.
- **Length:** set by the level file. Prose is capped hard; the one-pager caps its framing sections but not its activity table.

## Quick checklist before presenting

1. Does exactly one person hold A on every activity, and does at least one person hold R?
2. Is every A a named individual with the authority to actually unblock that activity?
3. Is there a shared-outcome sentence before any letters appear?
4. Is there a line inviting people to flag problems outside their own row, and a correction deadline?
5. Is every C someone whose input genuinely changes the work, with a date by which it is wanted? Would any of them be better as an I?
6. Is every activity verb-led with an identifiable output?
7. Are unowned activities written down as UNASSIGNED with a proposed owner, rather than omitted?
8. Do the letters describe how the work actually runs, or how the org chart looks?
9. Are all names, teams, and products spelled consistently, with no invented parties or dates?
10. Did you run the ai-patterns pass?
