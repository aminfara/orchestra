# Universal Rules

The writing rules, in two groups: **always-on** rules that hold for almost all professional writing, and **conditional** rules that depend on the format, tone, or medium. Apply them with judgment, not as a checklist. When two rules collide, serve the reader's understanding for *this* audience and purpose. Each rule notes, where relevant, when it does not apply and how to soften it.

---

## Part A: Always-on rules

These hold regardless of format or tone. Breaking one is almost always a bug, not a style choice.

### A1. Lead with the point

Conclusion or recommendation first, support after; a reader who stops early still gets the gist. *Soften for:* deliberately suspenseful or narrative pieces, where the point can be the thesis in the opening paragraph rather than the first sentence. Format decides.

### A2. Be clear

Plain language. Define terms the audience may not know; assume only the prior knowledge they actually have. One idea per paragraph. If a sentence needs two reads, rewrite it.

### A3. Be specific

Replace vague terms with concrete ones: who, when, what, how much. "We improved performance" → "p95 latency dropped from 800ms to 300ms in May." *Does not apply when* the source lacks the specifics — then name the dimension and mark `[CLARIFY: source]` rather than inventing a number (A9).

### A4. Be concise

Cut words that do not change meaning: *very, really, just, basically, actually, in order to, the fact that, at this point in time, going forward, in terms of*. Cut redundancy and hidden verbs ("make a decision" → "decide", "provide assistance" → "help").

### A5. Use active voice and name the actor

"The team shipped X on Tuesday", not "X was shipped." Passive is fine when the actor is unknown or irrelevant, or when naming them would assign blame in a blameless context (then depersonalize: "the on-call rotation", not a passive dodge).

### A6. Simple words, varied sentences

Prefer the plain word (*use* not *utilize*, *help* not *facilitate*). Keep most sentences short, but vary length; uniform length is itself an AI tell (see ai-patterns.md).

### A7. Correct grammar, spelling, dates, data

Proofread. Use an unambiguous date format (prefer ISO `2026-06-19` or a spelled month). Numbers must be accurate and internally consistent.

### A8. Write for the reader

Calibrate vocabulary, length, and assumed knowledge to the actual audience. An exec brief and an onboarding doc on the same topic are different documents.

### A9. Never fabricate (anti-hallucination protocol)

The most important rule for GENERATE mode. After drafting, classify every **specific factual claim** (number, name, date, quote, vendor/product fact, external statistic):

- **Verified** — you have a source, or the user gave it. Keep.
- **Inferred** — plausible but unconfirmed. Ask, soften to a clearly non-factual statement, or mark `[CLARIFY: ...]`.
- **Unknown** — you do not actually know it. Strip it or ask; do **not** smooth it over with a confident sentence.

Never invent quantification, citations, names, or dates to sound complete. A named gap beats a false fact.

### A10. Cite external claims

Attribute anything from an outside source (a statistic, a third-party fact). If you cannot attribute it, treat it as Unknown (A9).

### A11. Inclusive, globally-readable language

Avoid untranslatable idioms, single-region examples, time-zone-loaded phrasing ("by end of day" — whose day?), and ableist or gendered defaults. Write for any teammate in any office.

### A12. Consistent, canonical names

Spell product, vendor, team, and people names the same way every time, using their official spelling. Inconsistent names propagate through a knowledge base as downstream tools and readers repeat the error.

### A13. Expand abbreviations on first use

On first appearance, give the full term with the short form in parentheses, then use the short form: "single-threaded leader (STL)", then "STL." *Skip for* abbreviations universal to the audience (e.g. "API", "URL", "CEO" for a general business audience); judge by the actual reader (A8). When in doubt, expand; re-expand if the term reappears far from first use in a long document.

### A14. Use prose for ideas; lists for things

Reserve bullet and numbered lists for *things* — discrete, parallel items (days of the week, colors in a palette, the fields of a record). Use narrative prose for *ideas, reasoning, and actions*: fragments hide the logic and relationships that full sentences make explicit, so convert "idea bullets" into paragraphs. *Soften for* ultra-scannable media (chat, status, release notes; see B4) and genuine enumerations. Heuristic: if items connect with *because, therefore, then,* or *but*, write prose.

---

## Part B: Conditional rules (gated by format / tone / purpose)

Genuine best practices that damage some writing if applied blindly. Each format file says which to enforce or relax; defaults below.

### B1. Quantify the impact

Attach numbers to claims (cost, time, %, count). **Enforce for:** proposals, status updates, exec briefs, reports, anything persuasive or evaluative. **Relax for:** visionary or inspirational writing where the thing cannot be measured yet, since forced metrics read as fake precision. Never satisfy this by inventing numbers (A9 wins).

### B2. Positive, forward-looking framing

Prefer constructive, solution-oriented phrasing; treat past misses as learning. **Enforce for:** most business and team communication. **Relax for:** incident reports and post-mortems, which must state failures plainly. Stay blameless, but do not soften the facts.

### B3. Strict answer-first structure

Hard BLUF: the first sentence is the conclusion. **Enforce for:** decision docs, exec briefs, status updates, busy-reader channels. **Relax for:** narratives, PR/FAQs, and blogs that legitimately open with a hook before the thesis.

### B4. Brevity vs. depth

**Ultra-brief for:** chat and short email — one screen, front-loaded, often no preamble. **Dense and complete for:** narrative memos and proposals, where full sentences and reasoning are the point and bullet-fragmentation would hide the argument.

### B5. Persuasive section titles

Name sections for the reader's benefit ("Your return on investment", not "Pricing"). **Enforce for:** outward-facing persuasive or marketing documents. **Relax for:** internal decision docs and technical writing, where neutral, scannable headings aid navigation.

---

## Tone overlay

Voice (the writer's personality) stays constant; **tone shifts with audience, medium, and subject.** Match the tone the user asks for; do not impose a house tone. Presets:

- **Formal** — no contractions or slang; measured; complete sentences. Contracts, legal, senior-exec external comms.
- **Neutral / professional** — the default for most business writing. Plain, direct, light contractions.
- **Friendly / conversational** — contractions, warmth, "you/we", short sentences. Team comms, onboarding, many chat messages.
- **Persuasive** — confident claims anchored to evidence; benefit-framed; a clear ask. Proposals, pitches.
- **Authoritative** — declarative, decisive, minimal hedging. Decision docs, security guidance.
- **Visionary / inspirational** — bigger-picture, future-tense, story over statistics. Vision blogs, keynotes. Relax B1.
- **Urgent** — lead with the action and deadline; cut everything non-essential. Incidents, time-critical asks.

Honor a free-form tone ("warm but direct") over the presets. When tone is unspecified, default by format (stated in the format file).

## Medium overlay

Medium changes the surface, not *what* the document is. Adjust:

- **Email** — subject line earns the open; first line states the purpose; one primary ask; short paragraphs.
- **Chat** — one screen max; front-load the ask or answer; threads for detail; minimal formatting; no "Hi all, I hope this finds you well" preamble.
- **Wiki page / document** — headings and a short lead summary; the reader scans first, reads second; link out rather than inline everything.
- **Issue tracker** — terse, factual, action-oriented; structured fields over prose where the field exists.
- **Printed page** — complete prose, no reliance on links or interactivity; appendix for data.

When medium and format conflict (e.g. a full proposal pasted into a chat channel), prefer a short summary in the channel with the full document linked.
