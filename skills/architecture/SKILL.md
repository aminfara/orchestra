---
name: architecture
description: Design a system's target architecture from selected requirements in a PRD (product requirements document), or describe an existing system's as-is architecture, as a short architecture doc, a domain glossary and architecture decision records (ADRs), setting out three options for every decision that is expensive to reverse and spiking risky questions with throwaway prototypes. Use when a product needs its architecture designed before it is built, when a codebase's architecture needs documenting, or when an architecture needs checking for whether it is buildable and covers its requirements.
---

# Architecture

Decide how a system is built and what is expensive to change later, and write it down small enough to read in one sitting.

## Overview

This skill designs a system's architecture and records it in three living docs: a short architecture doc, a glossary of the domain's terms, and an architecture decision record (ADR) for each decision that is expensive to reverse. For a new product it designs the target architecture from the brief, the PR/FAQ and the technical research; for an existing system it describes the architecture as it is.

Architecture is the set of decisions that are expensive to change. Most decisions are two-way doors: if one turns out wrong, the team walks back through it at little cost, so it should be made quickly and noted. A few are one-way doors, such as the data model, the sync model for a collaborative product, a hosting platform or a public API, and those deserve deliberate comparison. Spending design effort in proportion to the cost of reversal keeps the architecture both careful and small.

A good architecture lets an engineer start any story without asking how the parts fit. Every promise the product makes traces to the parts that deliver it, every one-way door has an ADR with three real options and the reason for the choice, the riskiest assumptions have been tested rather than asserted, and the architecture doc reads in one sitting because it points to ADRs for the detail.

## When to use this skill

- A product needs its architecture designed before it is built, from selected requirements, the existing architecture if any, and technical research.
- A codebase's architecture needs documenting as it is, with its glossary and its risks.
- An architecture needs checking for whether it is buildable, covers its requirements and can deliver its UX design.

### When NOT to use this skill

- A local design question inside one module, such as the shape of a function or a class. Decide it in the code.
- Breaking an approved architecture into features, stories and a roadmap. That is planning, a later activity.

## Constraints

- **Three options for every one-way door.** Each is a design someone could defend, with what it costs and what it makes hard later; recommend one, and record it in an ADR.
- **Choose the simplest design the quality attributes allow.** Every component, service and technology must earn its place against a requirement in the brief.
- **Keep the architecture doc small.** It describes the whole system at one altitude and points to ADRs and the glossary for detail.
- **Leave the user's decisions to the user.** When a one-way door turns on the user's values, such as cost against operational effort, put it in your report as a question with your recommendation.

## Inputs

- **The selected requirements** in the PRD, the rest of the PRD, the brief with its technical section, and the **technical research**; the PR/FAQ if one exists.
- **The existing architecture doc, glossary and ADRs**, if the system already exists.
- **The approved UX design**, when the product has a user interface.
- **For an as-is architecture**, the codebase and the areas to cover.

## Output

- `<root>/docs/architecture.md`: context and scope; the quality attributes that drive the design; components and their responsibilities; the domain model at the level of concepts; the key flows through the system; deployment; risks and open questions. Each section links the ADRs it rests on.
- `<root>/docs/adr/NNNN-<decision>.md`: one per one-way-door decision, in the shape in `references/adr.md`.
- `<root>/docs/glossary.md`: each domain term with a one-line definition, used the same way in docs, UX and code.

## Workflow

### Step 1: Find the forces

Read the selected requirements, the brief, the existing architecture and the research. Write down the quality attributes that will shape the design (how many users, how fast, how available, offline or not, what data and how sensitive), and the product's hardest problems. These are what the design is judged against.

### Step 2: Sort the decisions

List the decisions the design needs and mark each as a one-way or a two-way door by asking what it would cost to reverse once the product is built. Make the two-way doors quickly and note them in the architecture doc. For each one-way door, set out three options with their costs and consequences, choose one, and write its ADR.

### Step 3: Spike what is risky

Where a decision rests on an assumption you cannot confirm from documentation, such as whether a sync library handles concurrent edits the way the design needs, test it with a throwaway prototype in a scratch folder outside the product. Record what the spike showed in the ADR, and delete the prototype.

### Step 4: Write the docs

Write the architecture doc, the glossary and the ADRs. Trace each selected requirement to the parts that deliver it, check the design against the PRD's remaining requirements and note where it would have to change to carry them, so the next feature extends the system instead of reworking it, and use the glossary's terms from the approved UX design. If the design cannot deliver a journey, report it as a finding instead of changing the UX. Before you report, read the architecture doc as an engineer about to start work would, and fill each gap that would force a question.

## Reference files

- `references/adr.md`: the shape of an ADR. Read before writing the first one.
