# Prior art

Part of the [Orchestra plan](README.md). What ten existing frameworks do, and what Orchestra takes from them. The full notes are in [`docs/research/prior-art/`](../../research/prior-art/).

## What the survey found

Five research notes cover [Superpowers](../../research/prior-art/superpowers.md), [GSD](../../research/prior-art/gsd.md), [Addy Osmani's agent-skills](../../research/prior-art/addy-osmani.md), [Matt Pocock's skills](../../research/prior-art/matt-pocock.md), and [six others](../../research/prior-art/others.md) (GitHub Spec Kit, BMAD-METHOD, Kiro, OpenSpec, wshobson/agents, Anthropic's feature-dev plugin). A sixth note compares [backlog tools](../../research/prior-art/backlog-tools.md). Most of the surveyed frameworks are MIT-licensed (wshobson's conductor plugin is Apache 2.0, Kiro is closed-source, and feature-dev's license was not shown), and Orchestra borrows ideas, not text.

The frameworks agree on more than they differ. All of them put a written spec or plan in front of code and have a human review it before implementation. All but feature-dev keep that state in Markdown files in the repo rather than in chat memory. Most keep standing project context (a constitution, steering files, a glossary) apart from per-change specs.

GSD makes context rot its central concern and has the most worked-out answer. Its orchestrator "does not reason about the domain, does not write code", passes file paths only, reads only the frontmatter of subagent outputs, and routes on short fixed status blocks. Plans hold two or three tasks and should finish within about half of the executor's context. Superpowers reaches the same place from a different direction: dispatch prompts must not carry session history, and the reviewer prompt says "Do Not Trust the Report".

Three frameworks independently found that reviewers should not see the author's claims. GSD's verifier says "Do NOT trust SUMMARY.md claims", Superpowers' reviewer gets the diff and the requirements only, and Addy Osmani's doubt-driven review passes "only the artifact and its contract". BMAD adds a related finding: "One model voicing five personas tends to make them agree", which argues for real subagents wherever independent judgment matters.

Addy Osmani names a "sequential orchestrator that paraphrases" as an anti-pattern, which is close to our conductor. His two objections are that hand-off summaries drift and that human checkpoints disappear. Matt Pocock's README makes a related point: frameworks like GSD, BMAD and Spec Kit "take away your control" by owning the process. Orchestra answers both. The conductor passes file paths and forwards review comments verbatim instead of paraphrasing, the user holds every review gate, and the flows are guidelines the conductor adapts in the open.

On instruction style, Superpowers, GSD, Addy Osmani's skills, Spec Kit and wshobson/agents are highly prescriptive: Iron Laws, capitalized STOP commands, rationalization tables, and GSD workflow files over 1,000 lines long. OpenSpec ("fluid not rigid") and BMAD v7 are the exceptions. Superpowers' own repo reports, in a 2026-06-10 design spec, that prohibitions on how to compose output backfired in its tests while positive recipes worked. We have not verified that result, but it supports the tenet of focused attention.

Two findings changed the first draft of the plan. Matt Pocock's to-spec, to-tickets and implement skills are user-invoked, so the conductor cannot call them. And the local copy of his skills drifted from upstream within two months (`CONTEXT.md` became `GLOSSARY.md`, and one skill left the manifest). Depending on installed third-party skills at runtime would be fragile, so Orchestra ships its own.

None of the ten frameworks publishes evidence that its multi-agent loop beats a single well-prompted agent. That is why M1 includes a single-agent baseline.

## Decisions per concern

Reviewed with you on 2026-10-14.

| Concern | What prior art does | Orchestra's choice |
| --- | --- | --- |
| Conductor context | GSD passes paths and reads frontmatter only; Superpowers bans session history in dispatches | Conductor reads reports only; briefs carry paths, not content |
| Handoff and state | Markdown in the repo everywhere; OpenSpec keeps a living spec that changes merge into | Small living docs in `docs/` (architecture, glossary, ADRs, PR/FAQ); per-run artifacts in `.orchestra/` |
| Resume | GSD `STATE.md`, Superpowers ledger, wshobson `state.json` | A Markdown run log, with progress also inferable from which artifacts exist; task state behind Orchestra's own `tasks` interface |
| Ceremony | BMAD routes by size; Superpowers sizes in brainstorming; Kiro and GSD have quick paths | Conductor classifies the request by type (idea, requirements, architecture, new feature, task within a feature under way, bug fix, troubleshooting, understand, rewrite); each flow carries the ceremony that type needs |
| Briefing the user | Matt: question rounds with a recommended answer; Addy: each question carries a guess and a confidence; Superpowers: one question per message | `briefing` skill: questions batched through the AskUserQuestion tool, each carrying its own context (what is asked and why it matters) and a recommended answer; the agent finds facts, the user makes decisions |
| Roles | GSD ships 33 narrow agents; feature-dev uses narrow explorer, architect and reviewer subagents; BMAD uses five personas (analyst, product manager, architect, developer, UX designer) | Four team roles split by view (product manager, architect, engineer, reviewer) plus a coach; an instance continues across activities that share its view |
| Research | GSD runs four parallel researchers and a synthesizer; Matt's research skill is thin | `research` skill used by the product manager (market and user lenses) and the architect (technical lens), in parallel; every claim sourced or marked as inference |
| Architecture | feature-dev runs two or three architects with divergent briefs; Matt's codebase-design says "design it twice" | `architecture` skill; one architect, who sets out three options for every one-way-door decision (one that is hard to reverse); ADRs record those decisions |
| Planning | GSD caps plans by context share; Matt uses tracer-bullet slices with blocking edges; Superpowers: a plan is "the set of decisions the implementer cannot make alone" | `planning` skill at two altitudes: the architect cuts features, stories and a roadmap; the engineer breaks its story into tasks; vertical slices, explicit dependency edges, work sized to fit one context |
| Engineering autonomy | Superpowers logs "Rulings" instead of stalling; GSD's executor stops for architectural changes | Engineer decides and logs; stops only for irreversible, security-sensitive, out-of-scope or architectural changes, or a backward-incompatible change to a released API that is not behind a feature gate |
| Review | feature-dev and BMAD use three lenses; Matt uses two axes; three frameworks hide the author's claims | `review` skill: one reviewer per change by default, on a different model from the author; extra lenses only for risky changes; no author claims; findings triaged as fix now, defer, or back to the plan |
| Verification | GSD's goal-backward verifier; Superpowers requires evidence from a fresh command run | `verification` skill: work backward from the goal; evidence is a command run fresh, not a report |
| Debugging | Matt requires a failing feedback loop before any hypothesis; Superpowers escalates after three failed fixes; Kiro records unchanged behavior | `debugging` skill with those three ideas as guidelines |
| Human gates | All gate the spec before code; GSD batches human checks per phase; feature-dev offers "Fix now / Fix later / Proceed as-is" | Accepted for the idea, requirements and architecture flows: briefings and review gates before code, then human checks batched per build milestone |
| Agent-to-agent talk | No surveyed framework does direct peer messaging; Addy uses agent teams for competing-hypothesis debugging | New ground for us; tested in an M1 spike |
| Model tiers | Superpowers, GSD and wshobson assign tiers per role | Opus at high effort for judgment roles, Sonnet at medium effort for executors, reviewers on a different model from the author; a rule of thumb the feedback loop tunes |
| Instruction style | Mostly high prescription; OpenSpec and BMAD v7 lower | Short skills built on concepts and quality bars; no Iron Laws, capitalized commands, or numeric thresholds stated as rules |
| Learning from reviews | Addy logs rejected skill changes and runs routing evals; Superpowers analyzes transcripts for skill misfires; GSD calibrates plan token estimates against measured history; BMAD's loop ends in "Learn and adjust"; Matt's upstream adds a retro skill | Feedback ledger and coach: recurring findings become concepts in a skill, a tool, or project docs, never one rule per finding; proven roles get lighter review and cheaper models; you approve every change |
