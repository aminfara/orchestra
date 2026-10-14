# Feedback loop

Part of the [Orchestra plan](README.md). How Orchestra gets better and cheaper with use without growing a rule set that eats its agents' attention.

## Two loops

Orchestra runs two loops that touch at one point. The delivery loop is the software development lifecycle: the conductor and the team roles run flows, and every checker and review gate writes its findings to the ledger. The improvement loop is the coach's: it reads the ledger across runs, proposes changes to skills, roles, review intensity and models, and you decide on them. The ledger is the only thing the two loops share.

Keeping the coach out of the delivery loop protects both. A flow never waits on a retro, and no skill changes while a run depends on it. The coach, for its part, sees patterns across many runs and projects that no single run can show, and it sees them through the ledger rather than through any one run's artifacts.

The coach runs when you start it, in its own session. The conductor's only part is to say, when it closes a run, how many new findings the ledger holds since the last retro, so you can decide when a retro is worth running. A scheduled retro is also possible once the loop has proved itself.

## Purpose

The loop exists to help agents think more clearly, not to give them more to remember. A review finding is evidence that an agent misunderstood or overlooked something. The coach's job is to find that misunderstanding and fix it once, at the level of the concept, so the fix covers a whole class of cases, including ones that have not happened yet.

The failure this loop must avoid is the obvious one: turning each finding into a rule. Every rule added for one past mistake costs attention in every future run, and a skill that grows that way starts to hurt the work it was meant to guide. GSD's workflows show the end state, past 1,000 lines with patches tagged by issue number ([GSD notes](../../research/prior-art/gsd.md)). Superpowers' own repo reports that prohibitions on how to compose output backfired in its tests while positive recipes worked ([Superpowers notes](../../research/prior-art/superpowers.md)); we have not verified that result, but it matches the tenet of focused attention.

## Record

Every checker (peer checks, reviews, acceptance) and every review gate writes its findings to a ledger, `.orchestra/feedback.jsonl`, through a small `feedback` script in the feedback skill. Each line is one finding: the run and flow, the role and skill that produced the artifact (with the skill's version), the model and effort used, who found it (which checker, or the user), a category, a severity, its outcome (fixed, deferred, or overridden), and one sentence on why it happened as the checker sees it. The script also records cost per task where it is available: rework rounds and tokens. The ledger is JSON so the coach can count and group findings without reading prose.

Findings caught late, at acceptance or by the user, also grade the reviewers: each one got past a review, and the ledger records which.

## Learn

When you start a retro, the coach reads the ledger, never the artifacts. For each group of related findings it decides where the fix belongs. There are four answers, and the first is the default.

- **Nowhere.** Most findings are one-offs, or exactly the kind of thing reviews exist to catch. They stay in the ledger and change nothing. A single finding never changes a skill.
- **A concept in the skill.** When findings recur and share a cause, the coach names the idea the agent was missing or misapplying, and proposes to express it in the skill as a clarified principle, a sharper quality bar, a reframed guideline, or one good example. "Check for null on the `discount` field" is a rule; "a value is optional until the domain says otherwise, so model its absence explicitly" is a concept that explains that finding and the next five like it.
- **A tool, not words.** If the finding is mechanical (formatting, naming, an import order, a forbidden call), the fix is a linter rule, a formatter, a test or a hook. A deterministic check costs no attention at all.
- **The project, not Orchestra.** If the finding reflects one project's conventions or domain, the fix belongs in that project's CLAUDE.md, glossary or ADRs, where only agents working on that project read it. This also keeps project content out of this public repo.

Before proposing a concept change, the coach tests it against four questions, and you check the same four at the gate:

1. Does it explain more than one finding? A change that fixes exactly one past finding is a rule in disguise; generalize it or drop it.
2. Would an agent reading it reason better about a case nobody has seen yet?
3. Is it phrased as what good looks like, rather than as a prohibition?
4. What does it replace? Each proposal names what it shortens, merges or removes. The ledger tracks each skill's length across versions, so growth is visible and needs a reason you accept.

## Get leaner

Skills should shrink as models improve. Periodically the coach runs a skill's eval cases with one guideline removed. If the evals pass without it, the coach proposes deleting it. A guideline that once prevented a mistake may no longer be needed, and every line deleted is attention returned to the task.

## Get cheaper

The ledger also shows where effort is wasted. If a role's work keeps passing review without significant findings, the coach proposes reviewing a sample of that role's changes instead of every one. If a role passes its checks consistently, the coach proposes a trial on a cheaper model or a lower effort, and the ledger shows whether quality held. If problems start reaching acceptance or the user after a reduction, the coach proposes restoring it. GSD does something similar for cost alone: it calibrates its plan token estimates against measured history.

## Guard

Every proposal reaches you at a review gate as a diff with its evidence (which findings, across how many runs) and its answers to the four questions; nothing changes a skill silently. Each pattern that leads to a concept change also becomes an eval case, so the change is tested with skill-creator against the failures that prompted it before it is accepted. Rejected proposals go to an append-only log so the same change is not proposed twice, an Addy Osmani practice ([notes](../../research/prior-art/addy-osmani.md)). After a change lands, the coach compares the following runs' findings with the earlier ones and proposes a revert if the change did not help.

Proposals are patches to this repo, because the skills live here. When the coach runs in another project, it writes its proposals to `.orchestra/proposals/` for you to apply here. This repo is public, so the coach writes every proposal in general terms, with no project names, code, or quoted content, and you check that at the gate.
