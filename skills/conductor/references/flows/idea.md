# Flow: idea

From a raw idea to a PR/FAQ the user can judge, and a decision to go on, park or drop it. Use it when the user has an idea and wants to know whether it is worth building. Most ideas do not become products, so this flow ends in a decision, not in a commitment.

The product manager carries one context from market research to the PR/FAQ. Resume that instance from phase to phase. There are two briefings and one review gate. When the idea is novel, the same product manager also checks feasibility.

## Phase 1: Intake

**Who:** you, with the user, using `orchestra:briefing`.

**Produces:** `brief.md` in the run folder, with these sections: the problem, from the user's side; the target user, specific enough that you could find one; why now; constraints (time, money, people, must-use or must-avoid); success signals the user could observe; non-goals. Also record whether the idea is novel, meaning the user doubts it can be built with known techniques, and say so in the brief.

**Exit criteria:** every section is filled from the user's answers or marked as an assumption the user accepted; a reader who was not in the conversation knows what is being considered, for whom, and what is ruled out.

**Checkpoint:** briefing. It ends with the open question the briefing skill closes on, not with a separate confirmation.

## Phase 2: Market research and feasibility

**Who:** the product manager, with `orchestra:research` through the market and user lenses. It fans out in two steps: one subagent finds the three major alternatives (competitors, or what customers do today); then one subagent per alternative studies that solution, its strengths, pricing, gaps, and what its customers complain about or ask for. The product manager reads their reports and writes the synthesis: what the alternatives have in common, which needs they leave unmet, and which missing features customers want most.

When the idea is novel, the product manager then runs `orchestra:feasibility` on the promises that look risky, in the same context, so it knows what the market research found. It may send bulk reading to subagents that return digests.

**Inputs:** `brief.md`.

**Produces:** `research/market.md`, ending with open questions for the user. For a novel idea, also `research/feasibility.md`: what is possible with known techniques, what is unproven, the smallest experiment that would settle it, and a verdict (feasible, feasible with a stated risk, or not known to be feasible).

**Exit criteria:** the documents answer the questions the brief set; every factual claim carries a source or is marked as inference; the synthesis names the common ground, the gaps and the customers' unmet wants separately; open questions are phrased as decisions the user can make.

**Checkpoint:** peer check by a fresh product manager instance briefed as a critic, who checks both documents and loads `orchestra:feasibility` for the feasibility one. Keep this critic for phase 4.

## Phase 3: Findings

**Who:** you, with the user.

**Produces:** an updated `brief.md`, and the user's decisions in the run log. The decision includes whether the idea still looks worth a PR/FAQ; the user may park or drop it here.

**Exit criteria:** every open question from the reports is answered, deferred by the user, or delegated to a role; the brief reflects what the research changed.

**Checkpoint:** briefing, built from the reports' questions and recommendations. It closes on the open question the briefing skill ends with.

## Phase 4: Working backwards

**Who:** the same product manager, with `writing-studio` in its PR/FAQ format.

**Inputs:** `brief.md`, `research/market.md`, and `research/feasibility.md` if it exists.

**Produces:** `<root>/docs/product/prfaq.md`, with the rough wireframes the format calls for.

**Exit criteria:** the press release keeps to the brief's problem, user and non-goals and builds on the gaps the research found; the Internal FAQ names the hard problems, the promises the product manager judges expensive or uncertain to deliver (including any feasibility risk), and what success would be measured by; a reader who was not in the session can follow it.

**Checkpoint:** peer check by the critic from phase 2, resumed with the PR/FAQ and these criteria, then review gate. At the gate the user also decides what happens to the idea: go on to the requirements flow, park it, or drop it. Record the decision in the run log.
