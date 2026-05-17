# Tone and Writing-Type Calibration

Tone is the felt register of writing — formal vs. informal, warm vs. cool, persuasive vs. neutral, playful vs. serious. Type is the genre — technical, business, creative. The two interact: a *technical* piece can be *informal* (a developer blog), and a *business* piece can be *creative* (a brand-led launch narrative). This file gives the agent a small set of calibration knobs so the same principles apply differently across these combinations.

The skill's job is to *match* the tone the writer wants, not to enforce a house tone. When the writer has a strong existing voice, preserve it; only flag tone when it actively breaks down (e.g., legalese in an internal Slack post, slang in a customer contract).

## How to use this file

Use the type sections to calibrate vocabulary, sentence length, and structural defaults. Use the tone sections to calibrate register and word choice on top of that. Read only the sections relevant to the piece in front of you.

---

## Writing types

### Technical
- **Audience assumption:** the reader has shared technical vocabulary or can be expected to look it up.
- **Vocabulary:** precise terms of art beat plain synonyms. Use the exact name of the system, command, or concept.
- **Sentence length:** average ~15-20 words. Code, identifiers, and exact values can ride longer.
- **Voice:** mostly active, but methods and procedures often legitimately use passive ("the request is signed before sending").
- **Structure default:** *answer-first* for explanations and decisions; *step-by-step* for runbooks and tutorials.
- **What to preserve:** terminology consistency, accurate command/code samples, exact version numbers.
- **Common drift to fix:** unnecessary hedging ("might want to consider"), missing prerequisites, missing verification steps.

### Business
- **Audience assumption:** the reader has limited time and is scanning for the decision or the impact.
- **Vocabulary:** plain language. Avoid jargon that does not travel outside the originating team.
- **Sentence length:** average ~12-18 words. Short opening sentences carry the most weight.
- **Voice:** active and direct. Name the actor; pin the date.
- **Structure default:** *answer-first* for updates and recommendations; *SCIPAB* for executive memos; *problem → solution* for proposals.
- **What to preserve:** numbers, dates, names of decision-makers, the ask.
- **Common drift to fix:** burying the ask, false precision (round numbers presented as if measured), passive constructions that hide who decided.

### Creative
- **Audience assumption:** the reader has chosen to read this and will give some attention to voice.
- **Vocabulary:** the writer's choice. Imagery, metaphor, and idiom are tools, not violations.
- **Sentence length:** varied deliberately for rhythm. Long-short-short can be a feature.
- **Voice:** whatever serves the piece. Passive voice can be used for effect.
- **Structure default:** *narrative arc* for stories; *what / so what / now what* for essays and reflective blogs.
- **What to preserve:** the writer's voice and rhythm. If a "rule violation" is doing real work, leave it.
- **Common drift to fix:** wandering openings (no inciting incident), unearned conclusions, decorative language that signifies nothing.

---

## Tones

### Formal
- **When to use:** external comms, legal and regulatory writing, executive comms to senior audiences, anything that will be read by people outside the writer's regular orbit.
- **Vocabulary:** standard professional register. Avoid contractions ("do not" not "don't"). Avoid colloquialisms.
- **Tone signals:** measured, complete sentences; "we" rather than "I" when representing an organization; explicit hedges where uncertainty is real.
- **Calibration:** clarity still wins. Formal does not mean ornate or longer.
- **Watch for over-correction:** legalese, third-person stiffness, passive voice everywhere. These are not "more formal" — they are harder to read.

### Informal
- **When to use:** internal team comms, blogs, friendly emails, chat-style updates, internal docs where team members are the only audience.
- **Vocabulary:** contractions are welcome ("we're", "it's"). Idioms and team-specific shorthand are fine if everyone knows them.
- **Tone signals:** "I" and "you" are fine; sentence fragments for emphasis are fine; humor in moderation is fine.
- **Calibration:** still organize the piece. Informal is not unstructured.
- **Watch for over-correction:** going so casual that the piece reads as careless or excludes anyone outside the in-group.

### Persuasive
- **When to use:** proposals, recommendations, marketing copy, opinion pieces, anything whose success is measured by whether the reader changes their mind or takes an action.
- **Vocabulary:** concrete and vivid; emotional anchors paired with evidence (Principle 1.3 softens here).
- **Tone signals:** strong verbs; clear thesis; direct asks; counter-arguments acknowledged and answered.
- **Calibration:** persuasion that is not anchored to evidence reads as hype. For every emotional claim, give one concrete fact.
- **Watch for over-correction:** purple prose, superlatives stacked ("absolutely critical", "uniquely powerful"), promises the writer cannot keep.

### Humorous
- **When to use:** developer blogs, brand voices that have established humor, internal team docs that the team enjoys reading, creative pieces.
- **Vocabulary:** specific and surprising beats general and clever. The funniest line is usually a specific, true detail.
- **Tone signals:** timing — humor lives in the rhythm of sentences and the placement of beats. Aside-style parentheticals and short callbacks tend to land.
- **Calibration:** humor is a multiplier, not a substitute. A clear point with one well-placed joke beats a muddled point with five jokes.
- **Watch for over-correction:** humor that punches down, in-jokes that exclude the audience, sustained sarcasm (exhausting to read).

### Neutral
- **When to use:** documentation, reference material, news-style reporting, factual updates, anything where the writer's stance should be invisible.
- **Vocabulary:** plain and precise. No emotional loading either direction.
- **Tone signals:** subject-verb-object sentences; explicit attribution for any opinion or claim.
- **Calibration:** neutral is not flavorless — it is *unobtrusive*. The reader should notice the content, not the voice.
- **Watch for over-correction:** drifting into corporate-speak ("synergize", "leverage"), or into mush ("things were done by the team").

---

## Combining type and tone

Some common combinations and what they look like:

- **Technical + informal** → developer blog. Precise terms with contractions and a personal voice. *Example feel:* "I tried `cursor.fetchall()` first, but it loaded the whole result set into memory. Switching to `cursor.fetchmany(1000)` cut peak memory by ~80%."
- **Technical + formal** → external API documentation, security advisory. Precise terms, no contractions, careful hedges where uncertainty is real.
- **Business + persuasive** → proposal, pitch, exec memo asking for a decision. SCIPAB or problem-solution shape, vivid concrete asks.
- **Business + neutral** → status update, board update, KPI report. Answer-first, dates, numbers paired with insight.
- **Creative + humorous** → branded blog post, conference talk script. Narrative arc with deliberate timing.
- **Creative + formal** → speech, opinion essay for a serious publication. Narrative arc with measured vocabulary.

When the requested type and tone clash with the source text, surface the mismatch as a finding rather than silently rewriting. The writer may have a reason.

---

## When to break tone deliberately

A single line in a contrasting tone can be powerful: a serious aside in a humorous piece, a moment of warmth in a formal one. Preserve these — they are usually the writer's best lines, not violations.

If the agent is writing rather than reviewing, use this sparingly: at most one tonal break per page, and only when it earns its place by sharpening a point.
