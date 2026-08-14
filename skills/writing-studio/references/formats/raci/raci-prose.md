# RACI — Prose level

A few lines of plain text in Slack, email, or a document comment. The reader gets ownership settled without opening anything. Read with `raci.md` (the base) for what each section and letter means.

## Goal

Make ownership of a handful of activities unambiguous in the flow of work, and get corrections fast. This is also the right level for floating a draft before anyone builds a page: it is cheap to argue with.

## Sections to include

From the base section library, one line each:

- **Scope and shared outcome** — combined into the opening sentence. The outcome comes first, and it is stated as jointly owned.
- **Assignments** — one line per activity. Six is the practical ceiling; past that, the reader loses the thread and you want a one-pager.
- **Consult and inform expectations** — only where a real date or channel exists ("Dana, your input by the 12th, in this thread").
- **Gaps** — one line, only if something is genuinely unowned. Name a proposed owner and ask them directly.
- **How to challenge this** — the closing line: corrections by a date, plus the invitation to flag across rows.

Out of scope at this level: the legend table, the parties key, decision rights and escalation tables, and the change log. Compress the legend to a half-clause only if the audience is new to RACI; otherwise drop it. Needing any of those sections is the signal to write the one-pager instead.

## Depth and shape

- One screen. Target 80-150 words; hard cap 200.
- **Plain text that survives a paste.** No markdown tables (a pipe table renders as garbage in Slack), no nested bullets, no heading levels, no bold on every other word, no emoji unless the channel already uses them. A flat line-per-activity list is the densest thing that travels safely.
- Line shape: `Activity — A: name. R: name. C: name. I: name.` Omit letters that are empty rather than writing "C: none".
- **For two or three activities, drop the letters and write sentences.** "Ali owns the cutover call, Priya runs the migration and clears it with Security first, and the rest of us get the summary after" carries the same information with less jargon, and lands better with an audience that does not live in RACI. Use letters when the count or the audience makes the grid worth it.
- Keep all three parts of the ownership clause (base): outcome first, duties implied by how you word the lines, flagging invitation at the end. At this length each is a single clause. They are the first thing a writer cuts and the reason the format exists; do not cut them.
- No preamble and no sign-off theatre. First line does work.
- One ask at the end, and make it an easy one: read your line, tell me if it is wrong.

## Example shape

> Goal: billing migration done by 2026-09-30 with no customer-visible downtime. That is on all five of us, whatever your letter below.
>
> Cutover decision — A: Ali. R: Priya. C: Dana (Security), Lee (Support). I: #billing-eng.
> Migration runbook — A: Priya. R: Priya, Sam. C: Ali. I: Dana, Lee.
> Customer comms — A: Lee. R: Lee. C: Ali. I: everyone here.
> Load testing — UNASSIGNED. Sam, can you take this, or name someone by Friday?
>
> Dana, Lee: I want your input before the 12th, in this thread. This is my draft, not a decision. Correct your own line by Friday, and if you see a problem in someone else's line, say so. That is expected, not overstepping.

## Extra gates for this level

1. Does it survive a paste into Slack as written, with no table and no broken formatting?
2. Is it under 200 words, and six activities or fewer?
3. Would the letters be clearer as plain sentences at this size?
4. Is the outcome sentence first, and the flagging invitation present?
