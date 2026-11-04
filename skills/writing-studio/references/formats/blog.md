# Format: Blog post

A first-person post in which the author tells colleagues (or a wider community) something worth their time: an idea, a set of findings, or a direction. It is one person talking to a reader they respect, in a semi-formal voice, short enough to finish in one sitting.

## When to use vs. adjacent formats

- **Blog post** (this format): one author, one takeaway, told in their own voice. Ends with an ask or a next step.
- **Proposal**: a decision document asking named approvers to choose. Neutral, options and trade-offs. If the reader's job is to decide, use proposal.
- **Announcement / status update**: reports what happened or is about to happen. If there is no idea, finding or argument to carry, use those.
- **Incident report**: blameless timeline for the record. A report-variant blog tells the same story for learning, not for the record.
- **Poster / PR/FAQ**: durable orientation or working-backwards artifacts. If the reader will come back to it as a reference, use those.

## Variants

Pick by asking "what does the reader leave with?"

- **Idea**: a technique or way of thinking they can use tomorrow. Also covers a perspective or lesson shared with peers.
- **Report**: findings from something the author ran, measured or shipped, the decision that followed, and what happens next.
- **Direction-setting**: a position, a phased path and an ask, from an author who leads the readers. Sets expectations and leaves the *how* to the team.

## Default axes

- **Purpose:** teach (idea), inform (report), persuade and set direction (direction-setting).
- **Tone:** semi-formal. Write the way a sharp colleague explains something at a whiteboard: contractions, "I", "we" and "you", plain words, no slang. Warm, direct, lightly funny.
- **Medium:** internal wiki or blog, readable on a screen in one pass.
- **Audience:** readers who were not in the author's research or meetings. They skim first, then read the parts that match what they came for.
- **Length** (tables, captions and appendix excluded):

| Variant | Target | Hard cap |
| --- | --- | --- |
| Idea | 500 to 900 words | 1,200 |
| Report | 800 to 1,500 words | 2,500 |
| Direction-setting | 400 to 800 words | 1,000 |

To fit a cap, drop whole points or move detail to a linked appendix. "Short" means fewer points, each in full sentences.

## Inputs to collect

- **variant**: idea, report or direction-setting. Infer from what the author wants the reader to leave with.
- **takeaway**: the one sentence the reader should be able to repeat afterwards. Ask when the author's material supports several.
- **assets**: charts, screenshots, diagrams or demos the author already has. The draft places them and asks for the rest (see Visuals).
- **voice samples** (optional, ask once): two or three posts the author likes the sound of. Match their openers, sentence length, how they introduce evidence, and where they put emoji and jokes.

## Voice

The author speaks. Use **"I"** for what the author saw, read, tried, could not find, or concluded ("I could not find anyone who publishes this"). Use **"we"** for what the team did or will change. Address the reader as "you" in the ask and in how-to passages. A report by several authors uses "we" for the shared work.

Keep the author's working material out of the body: verification tags, confidence labels, method notes and summaries of the author's own analysis go in the notes block below the `---` divider. The body states conclusions as the author's, in sentences a colleague would say aloud.

## Craft rules (all variants)

- **Title.** Promise the specific takeaway: name the idea, the outcome with its number, or the position. A reader who sees only the title should know whether the post is for them.
- **First screen stands alone.** Idea: a bold one-sentence thesis under the title. Report: a summary box. Direction-setting: the position in the opening paragraph. A reader who stops here has the gist. Lead with the conclusion, and tell the path to it afterwards.
- **Scannable.** Headings state the finding and carry information in their first words. Paragraphs hold one idea in one to five sentences. Someone reading only headings, bold text and captions can retell the story.
- **Emoji.** One emoji at the start of each H2 is welcome as a signpost; reuse the same emoji for the same kind of section. A few may appear in body text where the register is semi-formal. Keep them out of the summary numbers and the ask.
- **Humor.** Aim light satire at a situation, a shared habit or the author's own profession ("we engineers love the details"). Two to four touches per post, each beside a point it helps land: an exaggerated bad example, a dry aside, a cartoon or meme visual. Skip it in headline numbers, in anything about harm to people or customers, and in the ask. Leave it out when nothing funny serves the point. Never aim it at a named person or team.
- **Numbers.** Keep a figure when it changes what the reader believes or does, and say what it measures in the same sentence: unit, scope and period ("about 6,300 pull requests in 10 days"). Scale it to something the reader feels ("at that rate it is about $4,000 a day"). Mark each figure as measured or estimated. Make every figure that appears twice match: compare each repeat before presenting. Name what is still unknown next to what is known.
- **Examples.** Show the idea working: a before-and-after exchange, a snippet, or a short case with the point it supports. Include one example where the idea does not apply or fails.
- **Visuals.** Give each visual one job and refer to it in the text.
  - Use a diagram for architecture or flow, a chart for data, a screenshot for evidence, and side-by-side text for before and after.
  - Write the caption as the finding, not the topic ("Failures rose to match traffic after 100 scans an hour"). A chart gets a takeaway title, one highlighted series, a note on the cause, and everything else muted.
  - Give images alt text. A humor image may be decorative; all others earn their place.
  - The agent cannot draw. Place a `[VISUAL: type | what it shows | caption | data source]` placeholder where each visual belongs and list the missing assets in the notes block. Offer a Mermaid diagram for a flow when asked. Never invent chart data.
- **Ending.** End on one ask or next step. A recap that adds nothing is cut (ai-patterns #8).

## Templates

Headings may state the finding (relax B5); merge or drop sections the post does not need. `<emoji>` marks where the section's emoji goes.

### Idea

```text
# <Title: names the idea and the promise>

**<One-sentence thesis: the idea in plain words.>**

<Hook: a short real failure or scene, two to four sentences, that shows why the idea is needed.>

## <emoji> What goes wrong
<The "before": a short exchange or snippet showing the failure, then why it keeps happening.>

## <emoji> The idea
<The technique, named, in two or three parts. The "after": the same scene replayed with the idea applied.>

## <emoji> How to use it
<Three or four short examples from different situations. The last one is the edge case or limit.>

## <emoji> Bottom line
<One action for the reader, and the ask to pass it on or try it.>

<Optional: a pro tip, further reading.>
```

### Report

```text
# <Title: the outcome, with its number or decision>

> **Summary**
> <What we did, when, and at what scale, in one or two sentences.>
> - <Finding 1, with its number.>
> - <Finding 2, with its number.>
> - <Finding 3, with its number.>
> <The decision we made, its date, and what happens next.>
> Authors: <names>

## <emoji> What we set out to do
<Just enough setup for a cold reader: the system, the goal, the risks we knew. A diagram if there is one.>

## <emoji> What we found
### <Finding stated as a claim>
<Evidence with a visual and finding-style caption; what we know of the cause, or "cause unknown" with the conditions we do know; what we did about it.>

## <emoji> Why we decided <decision>
<The options we weighed and the reason this one won.>

## <emoji> What we learned
<Table: lesson | detail. Each lesson states what to do next time.>

## <emoji> What happens next
<Table: action | status | date.>

## References (optional)
```

### Direction-setting

```text
# <Title that states the position>

<Opening paragraph: the direction or claim in plain words, and who stands behind it.>

## <emoji> Why
<Why this matters to this team now. One or two paragraphs, with one pointer to the evidence.>

## <emoji> What changes
<The expectations, stated as outcomes and roles, not procedures.>

## <emoji> How we get there
<The phased path: start small, widen on evidence, adjust as we learn. Name the shape, not the tasks.>

## <emoji> When it goes wrong
<How failure is contained and what we do when it happens.>

## <emoji> What success looks like
<Observable end state, with a date if there is one.>

## <emoji> What I need from you
<One clear ask of the reader.>

## <emoji> Evidence (optional)
<Cases or data that back the claim, at the end so they support the story without interrupting it.>
```

## Rules for this format

- **Enforce:** A1 (the position is in the first screen), A2 and A8 against the actual reader, who was not in the research. Run the **reader-walk** on every paragraph (see SKILL.md Step 4). B1 for the report variant.
- **Explain in sentences.** Each sentence carries a subject, a verb and, where the reader must act on it, the reason. Evidence is told as a short case with the point it supports.
- **Altitude.** Direction-setting posts state what and why and leave the how to the team; ticket keys, thresholds, per-phase mechanics and repository lists belong in a linked backing doc.
- **Relax:** B3 (a hook of up to three sentences may precede the thesis in the idea variant); B1 for the idea variant (one concrete example replaces the numbers) and for visionary claims; B5 (finding-stating headings).
- **Watch:** telegraphic compression (ai-patterns.md #11) when the author asks for "short"; agent working-notes leaking into the body; "we" used for the author's personal research; jokes that outnumber points; figures that disagree between summary and body.

## Basis

Defaults come from these sources; the length targets and humor limits are editorial judgment, because the length studies are SEO surveys and the humor research is mixed.

- [NN/g: Concise, scannable, and objective](https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/) (concise, scannable and objective text each improved measured usability) and [NN/g: Inverted pyramid](https://www.nngroup.com/articles/inverted-pyramid/) (conclusion first).
- [Google technical writing course](https://developers.google.com/tech-writing/one/active-voice) (active voice, one idea per paragraph).
- [Google SRE postmortem culture](https://sre.google/workbook/postmortem-culture/) (summary, impact, lessons, owned actions).
- [Julia Evans: Some blogging myths](https://jvns.ca/blog/2023/06/05/some-blogging-myths/) (a post needs one or two things the reader does not know; qualify what you are unsure of).
- [Dan Luu: Some thoughts on writing](https://danluu.com/writing-non-advice/) (examples reduce misreadings; advice mirrors the author's own style, so match theirs).
- [Orwell: Politics and the English Language](https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/) (short words, active voice, concrete images).

## Quick checklist before presenting

1. Does the title name the takeaway, and does the first screen stand alone?
2. Is every "I" the author's experience and every "we" a team change?
3. Did every paragraph pass the reader-walk, and can a skimmer retell the story from headings, bold text and captions?
4. Does every figure state what it measures, and do repeated figures match?
5. Does every visual have a job, a finding-style caption and a placeholder or asset?
6. Do jokes sit beside a point, and is there at most a handful?
7. Does the post stay within its cap and end on one ask?
8. Did you run the ai-patterns pass, including #11?
