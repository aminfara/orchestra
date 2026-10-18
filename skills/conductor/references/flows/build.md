# Flow: build

From a breakdown in the task store to working software, one milestone at a time, with every change reviewed and every milestone accepted. Use it after the architecture flow's breakdown, or to continue a build whose run is under way.

Each story belongs to one engineer instance, which plans it, builds it, fixes what review finds and integrates it, so the context that wrote the code is the one that changes it. Each change gets a fresh reviewer, and each milestone gets an acceptance check by a reviewer and by the product manager, then a review gate with the user.

## Phase 1: Setup

**Who:** you.

**Inputs:** the breakdown's run folder (its `plan.md`), the project root, and `<root>/.orchestra/config.toml`.

**Produces:** in the run log, the milestone to build, the base branch the user works on, and the integration branch, `orchestra/build/<run slug>`, created from the base with `git branch <integration> <base>` and never checked out by anyone (engineers update it with `git push . HEAD:<integration>`, which Git refuses for a checked-out branch). Note the config's `[build]`, `[review]` and `[models]` tables if present; `references/briefing-roles.md` says what they change.

**Exit criteria:** the integration branch exists and contains the committed living docs the briefs point to (engineers and reviewers read them from their worktrees), and `tasks ready --milestone <m>` lists the milestone's first stories.

**Checkpoint:** none, unless the user has not said which milestone to build or which branch to start from; then ask in one batch.

## Phase 2: Build the stories

Repeat this phase until every story in the milestone is done or the user stops it.

**Who:** one `orchestra:engineer` instance per ready story, in its own worktree, up to the config's `[build] parallel` at once (default 3); a fresh `orchestra:reviewer` instance per change.

**Engineer brief:** the story ID; the project root; the integration branch as the base, and `story/<ID>` as its branch; the agent name to claim with (`engineer-<ID>`); the docs it needs, down to the section (architecture, ADRs, glossary, the UX screens for the story); skills `orchestra:planning`, `orchestra:tdd-programming`, `orchestra:debugging`, `orchestra:tasks`; the report path; the ledger details. Stories that `tasks ready` lists together have no blocking edges between them and can run in parallel.

**Review brief:** the branch and the integration branch as its base, the story ID, the docs the engineer was given, skills `orchestra:review` and `orchestra:verification`, the ledger details for the engineer (role, `tdd-programming`, its model and effort), and the verdict path. Never the engineer's report.

**Loop for each story:** the engineer reports done; the reviewer checks; on revise, resume the engineer with the "for the author" section and then the same reviewer to re-check, within the two rounds of `references/briefing-roles.md`; on pass, resume the engineer to integrate and close the story. After each story closes, run `tasks ready` again, since closing it may unblock others.

**Stops:** when an engineer reports "needs a decision" for a change to the architecture, resume the architect from the architecture flow if it is current, or start a fresh one with the architecture docs, and let it rule within the architecture's intent; take it to the user when the ruling changes a requirement, the UX or an ADR's decision. Other stop conditions go to the user at once, in one batch with any others waiting. A reviewer's "back to the plan" finding goes to the architect the same way, which edits the story or adds one.

**Exit criteria:** every story in the milestone is closed with a link to its integrated change, and every review passed or its open findings were deferred by the user.

## Phase 3: Acceptance

**Who:** a fresh `orchestra:reviewer` instance, then a fresh `orchestra:product-manager` instance.

**Inputs:** the integration branch; the milestone's stories in the task store; the PRD's definitions of done for the requirements they deliver; for the product manager, also the PR/FAQ and the UX design.

The reviewer runs acceptance with `orchestra:verification`: it builds the integration branch from clean, runs the whole suite, exercises every story's acceptance criteria through the product's real entry points, and writes `acceptance.md` in the run folder, recording failures with `--found-by acceptance`. The product manager then reads `acceptance.md`, runs the product itself, and judges it from the customer's side against the definitions of done and the PR/FAQ's promises, with `orchestra:verification`, appending its verdict to the same file.

**Exit criteria:** every acceptance criterion is met, or each failure is a story in the task store (a defect becomes a story with the failing behaviour as its acceptance criterion), and the checks that need a person are listed.

**Checkpoint:** if failures became stories, return to phase 2 for them before the gate.

## Phase 4: Milestone gate

**Who:** you, with the user.

Give the user the milestone's summary, how to run it from `acceptance.md`, the checks only a person can make, the deferred findings, and the acceptance verdicts, and ask for approval. Comments become findings found by `user`: forward each to the engineer of the story it concerns (or a fresh engineer if that instance is spent), or to the architect when it changes the plan, then back through review.

When the user approves, either start the next milestone from phase 2, or, when it was the last, ask whether to merge the integration branch into the base or open a pull request, and do what they choose. Merging is the user's call because it changes their branch.
