# Retro

How to read the feedback ledger and propose changes to how the team works. A retro runs outside any flow, never during one, and reads the ledger, not the runs' artifacts.

## Read the ledger

Start with `feedback.py summary --ledger <ledger>`, which groups the findings since the last retro by role, skill and version, category, severity, who found them, outcome and model. Findings found by the user got past every check, so they say something about the checkers as well as the authors. Read individual findings only for the groups that recur.

## Decide where each fix belongs

For each group of related findings, there are four answers, and the first is the default:

- **Nowhere.** Most findings are one-offs, or exactly what checks exist to catch. They stay in the ledger and change nothing. A single finding never changes a skill.
- **A concept in a skill.** When findings recur and share a cause, name the idea the agent was missing or misapplying, and express it as a clarified principle, a sharper quality bar, a reframed guideline or one good example. "Check the discount field for null" is a rule; "a value is optional until the domain says otherwise, so model its absence explicitly" is a concept that explains that finding and the next five like it.
- **A tool.** When the finding is mechanical (format, naming, a forbidden call), propose a linter rule, a formatter, a test or a hook. A deterministic check costs no attention.
- **The project.** When the finding reflects one project's conventions or domain, the fix belongs in that project's CLAUDE.md, glossary or ADRs, not in Orchestra.

## Test each proposal

Before proposing a concept change, answer four questions, and include the answers with the proposal:

1. Does it explain more than one finding? A change that fixes exactly one past finding is a rule in disguise.
2. Would an agent reading it reason better about a case nobody has seen yet?
3. Is it phrased as what good looks like, rather than as a prohibition?
4. What does it replace? Name what it shortens, merges or removes; the ledger shows each skill's length by version.

## Look for savings

A role whose work keeps passing its checks with few findings may need less review, such as a sampled check instead of every one, or a trial on a cheaper model or lower effort. Propose these as trials, with the signal that would undo them: findings reaching the user after the change.

## Propose

Each proposal is a diff to a skill or agent with its evidence (the finding IDs, across how many runs) and its answers to the four questions. Write it in general terms, with no project names, code or quoted content, because the skills live in a public repository. The user approves each one. After the retro, mark it with `feedback.py retro --ledger <ledger> --note "<what was proposed>"`.
