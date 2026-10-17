# Flow: understand

From an existing codebase to a usable map: an as-is architecture doc, a glossary, and a risk and debt map, walked through with the user. Use it when a codebase has no current architecture doc, before a new feature in an unfamiliar area, or before a rewrite. Scope it to an area when only part of the codebase matters.

One architect instance holds the whole-system view from the first survey to the synthesis. The detailed reading of each area is independent work, so it fans out to parallel architect instances that each return one area's map.

## Phase 1: Scope

**Who:** you, with the user, using `orchestra:briefing`.

**Produces:** `brief.md` with why the user wants the map (a feature, a rewrite, onboarding, an audit), which areas matter, how deep to go, and anything the user already knows to be true or broken.

**Exit criteria:** the purpose and scope are explicit enough to decide which areas get mapped in detail.

**Checkpoint:** briefing, closing on the open question.

## Phase 2: Survey and map

**Who:** an `orchestra:architect` instance, the surveyor, with `orchestra:architecture` in its as-is mode; then one fresh `orchestra:architect` instance per area, in parallel.

The surveyor maps the top level from the code and its build: entry points, modules and their boundaries, data stores, external dependencies, how it builds, tests and deploys. It writes `research/areas.md`, which splits the scope into areas that can be read independently, with a question list per area drawn from the brief's purpose. Brief one area architect per area with `research/areas.md`, its area and its questions; each writes `research/areas/<area>.md`: responsibilities, public interfaces, data it owns, what it depends on and what depends on it, the domain terms it uses, and its risks and debt, each claim pointing to the files that show it.

**Exit criteria:** every area in scope has a map, and every claim in a map points to code.

**Checkpoint:** none; the synthesis is checked.

## Phase 3: Synthesis

**Who:** the surveyor, resumed.

**Produces:** `<root>/docs/architecture.md` as it is, `<root>/docs/glossary.md`, `<root>/docs/risks.md` (risks and debt, ranked by what they would cost the purpose in the brief), and ADRs under `<root>/docs/adr/` for decisions the code makes visible, each marked as recovered rather than decided.

**Exit criteria:** an engineer new to the codebase could find where any behaviour in scope lives and how the parts fit; the glossary's terms are the code's terms; the risk map serves the brief's purpose.

**Checkpoint:** peer check by a fresh architect instance briefed as a critic: sample the docs' claims against the code, look for areas the map misses, and test whether the risk ranking follows from the evidence. Then review gate.

## Phase 4: Walkthrough

**Who:** you, with the user.

Ask the surveyor for a short digest aimed at the brief's purpose, and walk the user through it as a briefing. Forward the user's questions to the surveyor word for word and relay its answers; record any correction as a finding found by `user`. Offer the next flow the purpose points to, such as new feature or rewrite, and resume the surveyor for it if its context is still current.
