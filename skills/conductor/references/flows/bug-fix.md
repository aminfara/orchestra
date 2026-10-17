# Flow: bug fix

From a known defect to a reviewed fix with a regression test. Use it when the user reports something that behaves wrongly and can say, at least roughly, what should happen instead. When the cause is unknown and the problem is a symptom of a running system, use the troubleshoot flow first.

One engineer instance diagnoses and fixes the defect in the same context, because the understanding that finds a cause is the one that should change the code. A fresh reviewer checks the change, and the user confirms it.

## Phase 1: Intake

**Who:** you, with the user, using `orchestra:briefing`.

**Produces:** `brief.md` with the defect (what happens, what should happen), how to reproduce it, its impact (who is affected, how often, how badly), the behaviour around it that must not change, and the branch the fix should build on. If the user hands over a troubleshoot run's diagnosis, its path replaces most of this.

**Exit criteria:** an engineer could try to reproduce the defect without asking anything, and the must-not-change behaviour is explicit.

**Checkpoint:** briefing. Skip the questions the user's report already answers; close on the open question.

## Phase 2: Diagnose and fix

**Who:** an `orchestra:engineer` instance, with `orchestra:debugging` and `orchestra:tdd-programming`. If a troubleshoot run diagnosed this defect, resume that run's engineer instead, so the diagnosis stays in one context.

**Brief:** `brief.md`, the base branch, the branch `fix/<slug>`, the architecture doc sections and glossary for the area if they exist, the report path, the ledger details.

**Produces:** a branch with a regression test that failed before the fix and passes after, the fix at the root cause, and a report naming the cause in a sentence.

**Exit criteria:** the cause explains every symptom in the brief; the regression test sits at the lowest level that catches the defect; the whole affected suite and the must-not-change checks pass.

**Checkpoint:** none, unless the engineer reports "needs a decision" because the fix is large or hits a stop condition. Then hold a review gate on the root cause and the proposed fix before any change is made; if the fix changes the architecture, resume or start an architect to rule first.

## Phase 3: Review

**Who:** a fresh `orchestra:reviewer` instance, with `orchestra:review` and `orchestra:verification`.

**Brief:** the branch and its base, `brief.md` (the defect and the must-not-change behaviour are its criteria), the ledger details for the engineer, the verdict path. Never the engineer's report.

**Exit criteria:** the reviewer has reproduced the defect on the base and seen it fixed on the branch, and the verdict passes, within the two rounds of `references/briefing-roles.md`.

## Phase 4: Confirm

**Who:** you, with the user.

Review gate: give the user the cause in a sentence, the reviewer's verdict, the branch and how to see the fix. On approval, resume the engineer to rebase onto the latest base and rerun the suite, then ask whether to merge the branch into the base with `git merge --ff-only` or open a pull request, and do what they choose. If the project keeps a board, the engineer records the fix as a closed story so the history shows it.
