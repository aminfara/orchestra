---
name: ux-design
description: Design the user experience of a product's MVP from its approved PR/FAQ, as user journeys, an information architecture and low-fidelity wireframes, with simple clickable HTML prototypes where a journey's feel is uncertain, held to usability and accessibility bars. Use when a product with a user interface needs its main journeys and screens designed before it is built, or when an existing UX design needs checking against its PR/FAQ or architecture.
---

# UX Design

Design how the MVP's main journeys work for the customer, from the promises in an approved PR/FAQ.

## Overview

This skill designs the user experience of a product's MVP. It turns the promises in an approved PR/FAQ into the journeys a customer takes, the places in the product where those journeys happen, and low-fidelity wireframes of the screens that matter. Where a journey's feel is uncertain, it adds a simple clickable prototype in plain HTML.

The PR/FAQ's own wireframes are rough by design: they show the customer experience well enough to judge the idea. Before anyone builds, the team needs more than that. It needs to know what the customer does first, what they see when there is nothing there yet, how they recover from a mistake, and how each promise becomes a path through real screens. Designing that from the customer's view, in the same context that wrote the PR/FAQ, keeps the design faithful to the promises rather than re-derived from them.

A good UX design lets an engineer build the screens without asking what goes where, and lets the product manager trace each PR/FAQ promise to a journey. Each journey's next step is obvious, the most frequent job takes the fewest steps, and every screen works with a keyboard and a screen reader.

## When to use this skill

- A product with a user interface has an approved PR/FAQ, and its MVP needs its journeys and screens designed before it is built.
- An existing UX design needs checking against its PR/FAQ, against the architecture, or against the usability and accessibility bars.

### When NOT to use this skill

- The product has no user interface, such as a library or an API. The PR/FAQ and architecture cover it.
- The PR/FAQ is not approved yet. Its rough wireframes are enough until it is.
- Visual design: colours, typography, brand. This skill stops at structure and behaviour.

## Constraints

- **Design the MVP, from the customer's side.** Every journey serves a PR/FAQ promise in the MVP's scope; name the user's goal, not the feature.
- **Low fidelity on purpose.** Wireframes show structure, content and behaviour, not style, so they stay cheap to change.
- **Usability and accessibility are quality bars, not extras.** Treat the Web Content Accessibility Guidelines (WCAG) 2.2 at level AA as the reference.

## Inputs

- **The selected requirements** in the PRD, the **approved PR/FAQ** if one exists, and the brief.
- **The existing architecture doc**, if the system exists, for constraints such as what can happen in real time or offline.
- **The artifact folder**, usually `<root>/docs/product/ux/`.

## Output

```text
docs/product/ux/
  README.md          journeys, information architecture, and an index of the wireframes
  wireframes/        one file per key screen state, as Markdown with a text sketch, or as HTML
  prototype/         optional; plain HTML and CSS, no build step, only for uncertain journeys
```

Each journey in `README.md` names the user's goal, the trigger, the steps, the screens it passes through, the PR/FAQ promise it serves, and what happens when it goes wrong.

## Workflow

### Step 1: Map the journeys

From the PR/FAQ, list the jobs the customer comes to do, in their words. For each, write the journey from trigger to done: first use, the everyday case, and what happens on error or with nothing there yet. Order the journeys by how often a customer will take them.

### Step 2: Lay out the information architecture

Decide the places in the product (screens, panels, dialogs) and what lives in each, so that every journey has a path. Name each place in the customer's vocabulary and use the same terms as the glossary, agreeing new terms with the architect.

### Step 3: Wireframe the key screens

Draw a wireframe for each screen state the journeys depend on, including empty, loading and error states. Show what is on the screen, what the customer can do, and what happens next. Where a journey's feel is uncertain, such as several people editing the same list at once, build a small clickable prototype instead of describing it.

### Step 4: Check against the bars

Walk each journey as the customer would and check it: the next step is obvious; the frequent job is short; mistakes can be undone or recovered from; everything works by keyboard, has a visible focus and a text label, and never relies on colour alone. Check that each MVP promise in the PR/FAQ has a journey and that the architect agrees each one can be built as designed. Fix what fails before you report.
