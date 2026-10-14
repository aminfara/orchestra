# Architecture decision record

An ADR records one decision that is expensive to reverse: what was decided, what else was considered, and why. It is written once and not rewritten; when a decision changes, a new ADR supersedes the old one and both stay.

Number ADRs in order (`0001`, `0002`, ...) and name the file after the decision, such as `0003-sync-through-a-crdt.md`.

## Shape

```markdown
# NNNN: <the decision, as a short statement>

- **Status:** proposed | accepted | superseded by NNNN
- **Date:** yyyy-mm-dd

## Context

<The forces: the requirement or quality attribute at stake, the constraint, and why this is a one-way door. A few sentences.>

## Options

### <Option A>
<What it is, what it costs (build, run, learn), and what it makes hard later.>

### <Option B>
...

### <Option C>
...

## Decision

<The option chosen, and the reason, in terms of the forces above. Name the spike if one confirmed it.>

## Consequences

<What becomes easier, what becomes harder, and what would make us revisit this.>
```

## What makes a good ADR

The options are real: each is a design a capable engineer would defend, not a straw man set up to lose. The reason for the decision refers back to the forces in the context, so a later reader can tell whether it still holds when the forces change. The consequences name the signal that would justify revisiting it.
