# Writing Principles (with context)

This is the durable rule catalog the skill applies. Each principle is grouped by intent, and each one explicitly says **when it applies**, **when it does NOT**, and **how to soften it** outside its core domain. The skill's job is to apply judgment, not to flag every possible violation.

When two principles conflict in a given passage, prefer the one that serves the reader's understanding for this audience and purpose. When in doubt, prefer clarity over conformity.

## How to use this file

Skim the section headings first and only read the principles you need for the current text. For a short email you may need only **clarity** and **concision**; for a long narrative you'll need **structure** and **evidence** as well; for creative writing **voice** dominates and the others soften considerably.

Each principle below uses this shape:

> **Principle name.** What it asks for. *Applies when:* … *Does not apply when:* … *Softening:* …

---

## 1. Clarity

### 1.1 Lead with the answer
Put the point first; supporting reasoning after. *Applies when:* the writing answers a question, makes a recommendation, or reports a result. *Does not apply when:* the writing is a story or a deliberate suspenseful piece (creative narrative, dramatic case study). *Softening:* in long persuasive narratives, the "answer" can be the thesis stated in the opening paragraph rather than the first sentence.

### 1.2 Avoid weasel words and hedges
Words and phrases that hide responsibility, vagueness, or weak commitment make the reader work harder and signal lack of confidence. Examples to watch for: *about, around, almost, somewhat, perhaps, possibly, may, might, could, seems, appears, fairly, quite, generally, typically, often, in some cases, it is felt that*. *Applies when:* the writer knows the answer or can take a position. *Does not apply when:* the uncertainty is real and material (forecasts, hypotheses, security caveats, anything where false precision would mislead). *Softening:* keep one hedge per genuinely uncertain claim, but never two stacked together ("may possibly", "might perhaps").

### 1.3 Avoid emotional and loaded language
Loaded words bias the reader and erode trust in technical, business, and journalistic writing. *Applies when:* the writing is meant to be objective. *Does not apply when:* the genre is persuasive, marketing, or creative — there, deliberate emotion is the point. *Softening:* in persuasive writing, allow emotional language but anchor it to a concrete fact in the same paragraph.

### 1.4 Be specific
Replace vague terms with concrete ones: who, when, what, how much. *Applies when:* the writer has the specifics. *Does not apply when:* the source genuinely lacks them — see Principle 4.1 (Do not invent quantification). *Softening:* if a number is unknown, name the dimension and mark `[CLARIFY: source]` rather than inventing.

### 1.5 Define the who and the when
Sentences with no subject ("a decision was made") or no time anchor ("recently we shipped") force the reader to guess. Name the actor and pin dates. *Applies when:* the writing reports on actions or events. *Does not apply when:* the actor is irrelevant or anonymizing is intentional (security postmortems, learning-focused retros). *Softening:* if naming the actor would assign blame, depersonalize ("the team", "the on-call rotation") rather than going passive.

---

## 2. Concision

### 2.1 Cut filler
Words that do not change meaning: *very, really, just, basically, actually, literally, simply, quite, in order to, the fact that, due to the fact that, at this point in time, going forward, in terms of, with regard to, needless to say*. *Applies when:* the writing is informational. *Does not apply when:* a filler word is doing real rhythmic or tonal work in creative or persuasive writing. *Softening:* remove fillers that add nothing; keep ones that change tone or pacing in a way the writer intended.

### 2.2 Eliminate redundancy
Doublets that say the same thing twice: *each and every, first and foremost, end result, future plans, past history, completely eliminate, advance planning, basic fundamentals, exact same, free gift*. Pick one. *Applies when:* always. *Does not apply when:* the doublet is an idiom the audience expects ("aid and abet" in legal writing). *Softening:* none usually needed.

### 2.3 Surface hidden verbs (nominalizations)
Convert noun forms back into verbs: *make a decision* → *decide*; *conduct an investigation of* → *investigate*; *give consideration to* → *consider*; *provide a summary of* → *summarize*. *Applies when:* the writing leans bureaucratic or feels heavy. *Does not apply when:* the noun form is the term of art (e.g., *the investigation* as a named workstream). *Softening:* fix the worst offenders; do not chase every nominalization.

### 2.4 Use short sentences for one idea each
Aim for sentences under ~25 words and one idea each. Break long sentences with conjunctions into shorter ones. *Applies when:* the writing is informational, instructional, or fast-moving. *Does not apply when:* the rhythm of the piece deliberately calls for longer sentences (literary prose, formal speeches). *Softening:* let one or two longer sentences ride per paragraph for variety; the rule is about average density, not a hard cap.

### 2.5 Prefer simple words
Choose the shorter, more common word when it carries the same meaning: *use* over *utilize*, *help* over *assistance*, *start* over *commence*, *show* over *demonstrate*, *because* over *due to the fact that*, *after* over *subsequent to*, *try* over *endeavor*, *near* over *in the vicinity of*. *Applies when:* the audience is general or mixed. *Does not apply when:* the longer word is the precise technical term (medical, legal) and the audience expects it. *Softening:* in technical writing, use the precise term and gloss it once for outsiders.

---

## 3. Structure

### 3.1 Use the Pyramid Principle
Top idea first, then 2-4 supporting groups, then details under each. The reader who stops after the first paragraph still has the main point. *Applies when:* business, technical, and most informational writing. *Does not apply when:* the genre's value is in the unfolding (mystery, narrative essay, certain creative pieces). *Softening:* even in narrative, the *opening* should orient the reader to the stakes; the pyramid relaxes after that.

### 3.2 Prefer narrative paragraphs over bullets for ideas
Bullets are for *things* (lists of items, options, days of the week). Narrative paragraphs are for *ideas* and *reasoning*. Bullets fragment argument and hide the connective tissue between thoughts. *Applies when:* the writing develops an argument, explains a decision, or tells a story. *Does not apply when:* the content is genuinely a list (steps, options, criteria, configuration). *Softening:* short writing with a strong scannability requirement (release notes, executive summaries) can lean more on bullets.

### 3.3 Match paragraph shape to purpose
- **Answering a question:** answer → reasoning → caveats → further reading.
- **Telling a narrative:** what → so what → now what (what happened, why it matters, what to do next).
- **Persuasive memo:** situation → complication → question → answer → benefit (SCIPAB), detailed in `structures.md`.

*Applies when:* always — but choose the right shape per `structures.md`. *Does not apply when:* the source already follows a strong shape that fits the purpose; do not impose a new one.

### 3.4 One idea per paragraph
Each paragraph should have a topic sentence, supporting evidence, and a transition out. *Applies when:* informational and persuasive writing. *Does not apply when:* literary prose where paragraph breaks are rhythmic or thematic. *Softening:* don't chop a coherent flow of thought just to enforce one-idea-per-paragraph; coherence beats neatness.

---

## 4. Evidence and accuracy

### 4.1 Do not invent quantification
Quantify only what the source supports. *Applies when:* always. *Does not apply when:* — never. This is a hard rule.

*How to handle missing data:* there are two cases — load-bearing and color.

- **Load-bearing missing data** — a number the argument depends on (the budget, the date, the success metric). Mark inline with `[CLARIFY: <what is missing>]` so a reviewer cannot miss it. Inline markers exist for facts the calling agent or the user must fill in before the writing is usable.
- **Color details** — flavor that strengthens prose but is not load-bearing (what type of business, exact wording of an apology, the precise minute something happened). Pick one plausible choice, write the prose with it, and list the assumption in the Notes sidecar at the end of the document under "assumptions made". Inline `[CLARIFY: ...]` markers in narrative prose break the reader's flow and signal an unfinished draft — reserve them for facts that are genuinely required.

As a guideline: if a piece under ~1000 words has more than 2-3 inline CLARIFY markers, most are color and should be moved to the sidecar.

Anecdotes, future work, and forward-looking statements often *cannot* be quantified — say so plainly rather than invent a number.

### 4.2 Pair data with insight
Numbers without interpretation force the reader to guess what to do with them. State the insight the data supports, then show the data. Use both relative and absolute when possible: *"increased 18% (from 1,100 to 1,300 weekly active users)"*. *Applies when:* the writing presents data. *Does not apply when:* the data is a raw appendix or table the reader will analyze themselves. *Softening:* in dashboards and tables, the headline above the chart carries the insight.

### 4.3 Use consistent date and number formats
- Exact moment: `YYYY-MM-DD HH:MM TZ`
- Calendar date: pick one of `YYYY-MM-DD` (international, recommended) or `MM/DD/YYYY` (US) and use it throughout.
- Month-year: `Apr 2025` (three-letter month).
- Quarter: `Q1 2025`.
- If a half-year is implied, ask which quarter.

*Applies when:* always. *Does not apply when:* the genre's convention overrides (legal docs may require spelled-out dates). *Softening:* when mixing formats is unavoidable, footnote the convention once.

### 4.4 Cite or attribute claims that are not common knowledge
If a claim is contested, surprising, or load-bearing, attribute it (link, source, person, document). *Applies when:* technical and business writing. *Does not apply when:* opinion pieces and creative writing where the writer is the source. *Softening:* in informal writing, "(per X)" or a parenthetical is enough; full citations are not required.

---

## 5. Voice and register

### 5.1 Prefer active voice
Active voice (subject-verb-object) is shorter, clearer, and assigns responsibility. *Applies when:* the actor matters or the sentence reads better active. *Does not apply when:*
- The recipient of the action is the focus (methods sections: *"the samples were analyzed"*).
- The actor is unknown, irrelevant, or already obvious.
- Naming the actor would assign blame in a context that is meant to be learning-focused.

*Softening:* mixed voice within a piece is fine; the goal is not 100% active, it is *intentional* voice.

### 5.2 Use positive, forward-looking framing
Frame past misses around learning and future prevention rather than blame. Prefer present tense for ongoing realities. *Applies when:* business writing, retros, status updates, team comms. *Does not apply when:* a frank assessment of past failure is the entire point (postmortems where causes must be named bluntly, journalism). *Softening:* even in blunt postmortems, "what we'll do differently" should appear by the end.

### 5.3 Match tone to audience and genre
Formal for executive audiences and external comms; informal for team chat and internal blogs; persuasive when asking for a decision; humorous only where it fits the genre and audience. See `tones.md` for calibration guidance. *Applies when:* always. *Does not apply when:* the writer has a strong, established personal voice and the request is to preserve it. *Softening:* when in doubt, lean one notch *less* formal than your default — most business writing is over-formalized.

### 5.4 Use correct grammar and spelling for the target dialect
Pick a dialect (typically US or UK English) and stay consistent. Expand abbreviations on first use unless they are universally known to the audience. Avoid local slang that does not travel. *Applies when:* always. *Does not apply when:* dialect or slang is a deliberate stylistic choice. *Softening:* domain jargon that the audience uses daily is fine without expansion (treat it like vocabulary, not abbreviation).

---

## How rules combine in review mode

When reviewing, walk the principles in this order and stop at the first level that yields meaningful findings:

1. **Structure** (Section 3) — does the shape fit the purpose? If not, fix this first; sentence-level findings made on a misshapen draft will be wasted.
2. **Substance** (Section 4) — are claims supported, dates consistent, evidence paired with insight?
3. **Sentence-level** (Sections 1, 2, 5) — clarity, concision, voice. Group repeated instances into a single pattern finding with examples; do not list every passive verb.

A short piece may need findings only at level 3. A long AI-generated draft almost always needs the most leverage at levels 1-2.
