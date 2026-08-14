# RACI — One-pager level

The durable artifact on a wiki page or document: the matrix as a table, with the legend, expectations, decision rights, and gaps around it. Read with `raci.md` (the base) for what each section and letter means.

**"One-pager" is conceptual, not physical.** The framing sections stay to roughly a page of reading. The activity table runs as long as the work genuinely needs — a thirty-row matrix is still a one-pager if everything around it is tight. This is the deepest level RACI has; a document that needs more than this is an operating model, not a RACI.

## Goal

Be the standing answer to "who owns what here" — for the people in the work now, and for whoever joins in three months and reads it cold.

## Sections to include

All of them, from the base section library, in this order:

1. **Title and context header** — scope, what is explicitly out of scope, overall accountable owner, maintainer, last reviewed, review cadence. A short field table.
2. **Shared outcome** — one or two sentences, before any letters appear.
3. **Legend** — the duty-framed table from the base. Keep the duty column even when trimming; that column is what stops letters becoming shields.
4. **Parties key** — role title → named person. The roles appear in the matrix cells and the people are resolved here, so the matrix survives a re-org.
5. **Assignments matrix** — the table. Rows are activities, grouped by phase or theme. Columns are the four letters, fixed; each cell holds the roles carrying that letter for that activity.
6. **Consult and inform expectations** — how each C's input is collected and by when; what the I's receive, through which channel, at what cadence.
7. **Decision rights and escalation** — default decider per recurring decision area, who is consulted, and where it goes when stalled. Link out to a DACI for any single large decision rather than absorbing it here.
8. **Gaps and unassigned** — explicit rows, each with a proposed owner and a resolve-by date. Also note any party carrying an implausible share of the R's.
9. **How to challenge this** — corrections invited, to whom, by when, plus the cross-row flagging line.
10. **Change log** — date, what changed, who. Optional on day one, mandatory by the first revision.

## Depth and shape

- **Framing sections** (everything except the matrix): 400-700 words total. Over one page of reading, cut prose, not sections. Every section here is load-bearing; a RACI missing expectations or escalation is a grid, not an agreement.
- **Matrix:** no word cap, but group rows into phases or themes past about 15, and split into linked per-phase matrices past about 30. Length is a correctness problem, not a style one: a matrix nobody reads assigns nothing.
- **Columns are the four letters — R, A, C, I, in that order — never the parties.** Two reasons this beats a role-per-column grid: the table width is fixed however many stakeholders the work has, and a reader answers "who is doing X?" by reading one row left to right. Add a column only for a genuine variant letter (S, V) under the base's variant guidance.
- **Cells hold role labels and nothing else.** One role per line inside the cell, or comma-separated if short. The A cell holds exactly one role that resolves to exactly one person. An empty cell is legitimate: write "—", not "none". Anything needing a sentence goes in section 6 or a footnote row beneath the table.
- **A crowded C cell is a diagnosis, not a layout problem.** This shape makes C inflation visible on sight: a row whose C cell runs to four or five roles needs cutting before you ship, not a wider column.
- **Cover the one thing this shape costs.** A reader can no longer find their own name by scanning a single column. Spell every role and person canonically (A12) so search and @mentions find them, and where the party list is long, give the parties key a short "owns" note per party.
- Row wording: verb-led with an identifiable output. "Publish the weekly launch update", not "communications".
- Add a one-paragraph "how to read this" only if the audience is new to RACI. Otherwise the legend carries it.
- Status markers and dates belong to the header and the gaps table. Keep delivery status out; that is the project one-pager's job.

## Skeleton

```text
# RACI: [scope]

| Field | Value |
| --- | --- |
| Scope | [what this covers] |
| Out of scope | [what it does not] |
| Overall accountable | [one named person] |
| Maintainer | [name] |
| Last reviewed / cadence | [date] / [quarterly, or on team change] |

## What we are all aiming at
[One or two sentences: the shared outcome. This RACI splits the work, not the goal.]

## Legend
[Duty-framed table from raci.md]

## Who is who
| Role | Person |
| --- | --- |
| [role] | [name] |

## Assignments
| Activity | R — does the work | A — owns it (one) | C — input before | I — told after |
| --- | --- | --- | --- | --- |
| **[Phase or theme]** | | | | |
| [verb-led activity] | [role] | [role] | [role], [role] | [role] |
| [verb-led activity] | [role], [role] | [role] | — | [role] |

## Consulted and informed: what that means here
[Per C: how input is collected, by when. Per I: what they get, where, how often.]

## Decision rights and escalation
| Decision area | Decides (A) | Consulted | Escalates to |
| --- | --- | --- | --- |
| [area] | [name] | [names] | [forum or person] |

## Gaps
| Unowned activity | Proposed owner | Resolve by |
| --- | --- | --- |
| [activity] | [name or UNASSIGNED] | [date] |

## If this is wrong
[Corrections to [name] by [date]. Spotting a problem in someone else's row is
expected, not overstepping — raise it in [channel].]

## Change log
| Date | Change | By |
| --- | --- | --- |
```

## Extra gates for this level

1. Do the framing sections fit roughly one page of reading, with none dropped?
2. Does every activity row carry exactly one role in the A cell and at least one in R?
3. Do the cells hold role labels rather than bare personal names, with the people resolved in the parties key?
4. Do the consult expectations give a real date or channel for every C in the matrix?
5. Is there an escalation path for the case where the A and a C disagree?
6. Are gaps listed as rows rather than left off the table?
