# Flow: rewrite

From an existing system to a new one that keeps the behaviour that must stay, replaced incrementally where possible. Use it when the user wants to rebuild a system or a large part of it on a new architecture or stack.

The architect who maps the system designs its replacement and the migration, in one context, because the understanding of what exists is what makes the target and the path safe. Parity is proved by tests written against the old system before anything is replaced.

## Phase 1: Understand

Run the understand flow first, unless its docs are current, with the rewrite as its purpose so the risk map ranks what the rewrite must care about. Keep its surveyor instance for this run.

## Phase 2: Intent

**Who:** you, with the user, using `orchestra:briefing`.

**Produces:** `brief.md` with why the rewrite is happening and what it must achieve, the behaviour that must stay identical, what may change, the constraints on migration (downtime, data migration, parallel running, deadlines), and how success will be measured.

**Exit criteria:** the must-stay behaviour is specific enough to test, and the success measures are observable.

**Checkpoint:** briefing, closing on the open question.

## Phase 3: Target and migration

**Who:** the surveyor from the understand flow, resumed, with `orchestra:architecture`, and `orchestra:research` through the technical lens for any new technology.

**Produces:** the target architecture as a new version of `<root>/docs/architecture.md` that states what changes and why, ADRs for its one-way doors, and an ADR for the migration strategy with three options (for example incremental replacement behind the existing interfaces, a parallel run with comparison, or a single cutover) and the chosen one.

**Exit criteria:** every must-stay behaviour traces to how the target keeps it; the migration keeps the system working at every step, or says where and for how long it does not; the risk map's top risks each have an answer.

**Checkpoint:** peer check by a fresh architect instance briefed as a critic, then review gate.

## Phase 4: Breakdown

**Who:** the same architect, with `orchestra:planning` and `orchestra:tasks`.

**Produces:** the board and `plan.md`, as in the architecture flow's breakdown, with parity stories first: characterization tests that pin the must-stay behaviour against the old system, so the same tests can run against the new one. Each later story replaces one slice behind those tests.

**Exit criteria:** every must-stay behaviour has a parity story; every slice can be verified against the parity tests before the old code it replaces is removed.

**Checkpoint:** peer check by a fresh product manager instance when users see the behaviour, otherwise by a fresh architect, then review gate.

## Phase 5: Build

Run the build flow. Acceptance for each milestone includes the parity tests passing against the new system and, where the migration runs both systems, a comparison of their outputs.
