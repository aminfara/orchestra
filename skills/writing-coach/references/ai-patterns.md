# AI Writing Patterns to Avoid

Large language models have a statistical pull toward a generic, puffy register: vocabulary that sounds impressive but says little, decorative formatting that fragments meaning, and `-ing` clauses that pad sentences without adding information. These patterns are not "wrong" in any individual sentence, but they accumulate into prose that reads as bland, corporate, or evasive — and they are now distinctive enough that human readers recognize them as "AI slop" and lower their trust in the writer.

This file lists the patterns the agent should actively suppress when drafting, and actively flag when reviewing AI-generated text. Read it once per draft or review; it is short on purpose.

## The patterns

### 1. Puffery vocabulary
Words that signal importance without delivering it. Cut or replace with the concrete thing.

- *crucial, vital, pivotal, essential, paramount, key (as adjective)*
- *testament to, hallmark of, cornerstone of, embodiment of*
- *enduring legacy, profound impact, transformative, revolutionary, game-changing*
- *seamless, robust, cutting-edge, state-of-the-art, world-class, best-in-class*
- *navigate (as a generic verb), unlock, harness, foster, empower (when not literal)*

**Test:** if you remove the word, does the sentence lose meaning or only lose volume? If only volume, cut.

### 2. Empty `-ing` clauses
`-ing` phrases tacked onto a sentence to make it sound like more is happening than is.

- *…, ensuring reliability across the platform.*
- *…, showcasing the team's commitment to excellence.*
- *…, highlighting the importance of collaboration.*
- *…, demonstrating the power of modern tooling.*
- *…, providing users with a seamless experience.*

**Test:** can the `-ing` clause be deleted without losing factual content? If yes, delete. If the clause has real content, rewrite as its own sentence.

### 3. Overused AI vocabulary
Words that LLMs reach for far more often than human writers do. Not banned — but if you find yourself using more than one or two per page, swap them for plainer alternatives.

- *delve, dive deep, deep dive*
- *leverage* (use *use*)
- *multifaceted, holistic, comprehensive*
- *foster, cultivate*
- *realm, landscape, ecosystem, tapestry, mosaic*
- *navigate the complexities of …*
- *in today's fast-paced world / in an ever-evolving landscape*
- *whether you are X, Y, or Z (an AI catchphrase opener)*

### 4. Promotional adjectives stacked
Two or three adjectives in front of a noun, each doing the same job.

- *a powerful, intuitive, modern platform*
- *a robust, scalable, enterprise-grade solution*
- *a comprehensive, end-to-end, holistic approach*

**Test:** keep at most one adjective per noun. If three are needed, the noun is too vague — replace it with something concrete instead.

### 5. False balance and mealy hedges
Hedging language that sounds careful but commits to nothing.

- *while X has its merits, Y also offers benefits*
- *it is important to note that…*
- *it is worth mentioning that…*
- *one could argue that…*
- *there are many factors to consider*

**Test:** if the writer has a position, state it. If they do not, ask the question rather than fake-balancing.

### 6. Decorative formatting
Formatting that fragments prose without adding scannability.

- A bullet list of three items where each item is a full sentence and the list adds nothing over a paragraph.
- Bolding every other phrase in a paragraph (the bolds cancel out).
- Emoji decorations on every heading or list item in a non-casual context.
- A nested heading hierarchy four levels deep for a 200-word section.

**Test:** would the reader scan this section, or read it linearly? Use bullets and headings only for scanning. For reading, use prose.

### 7. The "It is X that Y" opener
Padded sentence openers that delay the subject.

- *It is important that we ship by Q3* → *We must ship by Q3.*
- *It is the case that performance has degraded* → *Performance has degraded.*
- *There exist three primary causes* → *Three causes drive this.*

### 8. Vague abstractions for concrete things
Replacing a specific term with a fuzzy abstraction.

- *solutions* (which solutions?), *capabilities, offerings, experiences*
- *stakeholders* (which stakeholders?), *users, customers, individuals*
- *the space, the domain, the area*

**Test:** can the reader picture or point at what you mean? If not, name the thing.

### 9. Symmetrical or formulaic conclusions
LLM-generated text often closes with a "as we have seen, X is Y, ensuring Z" beat that mirrors the opening. It rings hollow.

- *In conclusion, …*
- *Ultimately, the journey toward …*
- *As organizations continue to evolve, …*

**Test:** delete the closing paragraph. Does the piece end well one paragraph earlier? If yes, delete.

### 10. Over-use of em-dashes and parentheticals
LLMs love em-dashes and parentheticals as a default joining device. Used well, they are great. Used by reflex, they fragment sentences.

**Test:** count em-dashes per page. More than three or four is usually too many. Convert some to commas, periods, or rewrites.

---

## How the agent uses this file

When **writing**, run this list as a final pass before returning the draft. Cut the patterns that fired. The result will sound less impressive and more credible — that is the point.

When **reviewing** AI-generated text, surface these patterns as a single grouped finding under "Sentence-level": *"AI patterns detected: puffery (`crucial`, `seamless`), empty `-ing` clauses (3 instances in §2), `delve` overused (5x). Recommended pattern fix: cut puffery vocabulary; rewrite `-ing` clauses as their own sentences; replace `delve` with `look at` / `examine`."*

Do not list every instance — pattern findings are more useful than instance lists.

## Final-pass checklist (do this every time)

Before returning a draft or finishing a review, walk this checklist as a literal counting exercise. Do not skip it; the patterns above slip in at a rate that surprises every model.

1. **Count puffery words** in the draft: `crucial`, `vital`, `pivotal`, `essential`, `seamless`, `robust`, `cutting-edge`, `transformative`, `comprehensive`, `holistic`, `critical` (when used as filler). If any appear, rewrite the host sentence with the concrete thing the word was supposed to mean.
2. **Count `-ing` clauses** at sentence ends starting with `…, ensuring …`, `…, showcasing …`, `…, highlighting …`, `…, demonstrating …`, `…, providing …`. Each one: delete the clause or split it into its own factual sentence.
3. **Count em-dashes** per page. More than three or four per page is overuse — convert some to commas, periods, or rewrites.
4. **Check the closing paragraph** for *In conclusion / Ultimately / As we have seen / This represents / This demonstrates*. If the closing rings a formulaic note, delete it; the previous paragraph is probably a stronger ending.
5. **Check abstractions**: `solutions`, `capabilities`, `offerings`, `experiences`, `stakeholders`, `the space`, `the landscape`, `the ecosystem`. Replace each with the concrete noun it stood in for, or cut.
6. **Check overused vocabulary**: `delve`, `leverage`, `multifaceted`, `foster`, `realm`, `tapestry`, `navigate the complexities of`. More than one or two per page is too many.

Pass the checklist before declaring the draft done. The skill's value is largely measured by how well this final pass removes generic register from AI-generated prose.
