# Format: Peer Feedback

Structured Strengths and Opportunities feedback for a performance review cycle. Turns raw observations into specific, objective, behavior-based prose that is useful to the recipient and their manager.

## When to use vs. adjacent formats

- **Peer feedback** (this format): you are giving formal performance feedback on a colleague — what they did well (Strengths) and where they can grow (Opportunities) — typically in a structured review system.
- **Email / message**: you are sharing casual appreciation or a one-off note. Peer feedback requires SBI structure and role context; a casual note does not.
- **Self-assessment**: a distinct format where the author evaluates their own performance; peer feedback is always written about someone else by a peer.

Use this format for both **generate** (bullets → SBI prose) and **review** (critique and improve existing peer feedback text).

## Default axes

- **Purpose:** inform the recipient's manager (and optionally the recipient) of observed strengths and concrete growth opportunities.
- **Tone:** neutral and professional. Warm but factual for strengths; constructive and forward-looking for opportunities. Never evaluative of personality.
- **Medium:** a structured form in a performance review tool, or a written document. Short paragraphs; no sub-headings inside individual items.
- **Audience:** the recipient's manager (primary reader). The recipient may also read it. Both need specificity and behavioral evidence.

## Inputs to collect

Gather these before generating or reviewing. Infer silently when clear; ask only when a key input is genuinely unclear.

- **mode** (required) — `generate` (turn bullet points into SBI prose) or `review` (critique and improve existing peer feedback).
- **receiver_role** (required) — the receiver's role title and level, e.g., "Staff Engineer", "Senior Product Manager", "Design Lead, L5". Used to assess relevance of each feedback item.
- **role_expectations** (optional but valuable) — any role rubric, performance indicators, or career-level expectations the user can share. The more specific, the sharper the relevance check.
- **org_values** (optional, but prompt for it) — the organization's values that feedback should connect to where natural, e.g., "Customer First, Speed, Integrity". If not provided, skip values connections.
- **strengths** (generate mode) — raw bullet points describing positive observed behaviors or outcomes.
- **opportunities** (generate mode) — raw bullet points describing areas where the receiver can improve.
- **existing_feedback** (review mode) — the existing strengths and opportunities text to review.
- **relationship_context** (optional) — how long and closely you worked together; which project(s) you collaborated on. Helps ground the Situation.

## Role relevance check

After collecting `receiver_role` and any `role_expectations`, evaluate each input bullet before generating prose. Flag any item that appears:

- **Not material to the role's level** — the observation is about basic expected behavior, not growth for that level (e.g., "attends meetings on time" for a Staff Engineer).
- **Off-scope** — the behavior is outside the receiver's function or direct work, with no clear connection.
- **Too vague to be actionable** — "be more proactive" without a concrete example names no real behavior.

Surface flagged items to the user before writing, with a brief note on why each was flagged. Ask: keep as-is, provide more context, or drop. Only generate from confirmed inputs.

## Frameworks

Strengths and Opportunities use different frameworks. Both produce a single flowing paragraph per item — no labeled fields, no headers inside the paragraph.

### Strengths: SBI

Lead with the theme (the main point), then weave Situation, Behavior, and Impact into prose, ending with a recommended next step. The theme leads the paragraph; it should tell the reader what to take away before they read the evidence.

- **Theme** — the main message or pattern; the first sentence of the paragraph.
- **Situation** — the specific context: the project, meeting, or moment when the behavior occurred.
- **Behavior** — the observable action. What the person did, not a personality trait or inferred intent.
- **Impact** — what resulted for the team, product, or organization. Connect to org values here if provided and the connection is natural.
- **Recommended next step** — one forward-looking action: where to continue or apply this further.

### Opportunities: forward-looking recommendation

Do **not** use SBI for opportunities. Describing a past situation and past behavior — even neutrally — puts the receiver on the defensive and frames growth as a past failure. End-of-year peer feedback should open a door, not re-litigate an incident.

Instead, structure each opportunity as a recommendation with rationale and impact:

- **Recommendation** (theme, leads the paragraph) — what you suggest they develop or try: "I recommend / I encourage / One area to develop is..."
- **Rationale** — the context that makes this relevant: what it enables, the situations where it would help. This can reference relevant dynamics you have observed, but framed as opportunity, not critique.
- **Impact** — how developing this helps them, the team, or their goals.

Rough shape: "I recommend [X] to [theme]. [Rationale: context that makes this relevant, framed as opportunity]. This would [impact on their growth, the team, or their goals]."

## Template

```text
## Strengths

[Theme — the main point, stated plainly as the opening sentence. Then: the situation and
behavior woven together in one or two sentences. Then: the impact, with a values connection
if provided and natural. Close with one forward-looking recommended next step.]

[Second strength, same shape.]

## Opportunities

[Recommendation opening: "I recommend..." or "I encourage..." or "One area to develop is..."
Then: the rationale — context or patterns that make this relevant, framed as opportunity, not
past failure. Then: the impact — how this helps them or the team going forward.]

[Second opportunity, same shape.]
```

## Rules for this format

- **Enforce:**
  - A3 (be specific) — every item must name a real situation; "sometimes" or "often" without a concrete example fails this rule.
  - A5 (active voice, name the actor) — "you led the session" not "the session was well-led."
  - A9 (no fabrication) — write only what was observed. Do not invent impact numbers, infer unexpressed intent, or speculate about the receiver's motivation.
  - B2 (forward-looking framing) — opportunities must open a door, not re-litigate an incident. The recommendation framework structurally enforces this; reject any input that inverts it.
- **Relax:**
  - B1 (quantify impact) — use real data when available; do not invent it. Concrete qualitative impact ("the team would leave with a clear decision") is preferable to fabricated percentages.
  - B3 (strict answer-first structure) — strengths use SBI, which builds context before impact; this is intentional. Opportunities lead with the recommendation, which is answer-first.
- **Watch:**
  - **Personality and style descriptors** are the most common failure in strengths. "Wonderful", "brilliant", "difficult" describe personality, not behavior. Replace with the observable action that produced that impression.
  - **SBI applied to opportunities**: if the output describes what went wrong before suggesting improvement, the framework has been misapplied. Opportunities must lead with the recommendation, not the incident.
  - **Generic recommendations**: "develop your communication skills" names a direction, not an action. Name the specific behavior or practice in the receiver's context.
  - **Feedback that is off-level** for the receiver's role: surface this in the relevance check before generating, not silently in the prose.
  - **Feedback sandwich**: do not bury an opportunity inside a strength paragraph. Keep Strengths and Opportunities in separate sections.
- **Length:** 150 words per **section** (all strengths combined; all opportunities combined), hard cap 180 words per section. If the inputs produce more, trim the lower-impact items first, then compress prose — do not raise the cap.

## Quick checklist before presenting

1. Does each strength name a specific situation and observable behavior (not a personality trait)?
2. Does each opportunity lead with a recommendation, not a description of what went wrong?
3. Is every opportunity paragraph free of SBI structure? If it describes a past incident before the suggestion, rewrite.
4. Are Strengths and Opportunities each within 180 words total?
5. Are any personality or style descriptors present? If yes, replace with the observable action.
6. Is each item plausibly relevant to the receiver's role and level?
7. If org values were provided, are relevant connections present and natural (not forced)?
8. Did you run the ai-patterns pass?
