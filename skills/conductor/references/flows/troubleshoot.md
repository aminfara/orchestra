# Flow: troubleshoot

From a symptom without a known cause, such as an outage, a slowdown, errors after a deploy, or a broken environment, to a diagnosis the user can act on. Troubleshooting changes no product code; anything that touches a running system goes to the user as a proposal.

One engineer instance gathers the evidence and diagnoses, reading the architecture doc itself rather than consulting the architect, so the evidence and the reasoning stay in one context. If the diagnosis finds a defect, the same instance can carry it into the bug-fix flow.

## Phase 1: Intake

**Who:** you, with the user, using `orchestra:briefing`.

**Produces:** `brief.md` with the symptom in the user's words, when it started and how often it happens, what changed around that time, which environments are affected, what the agent may access (logs, metrics, dashboards, a staging copy) and how, and what it must not touch.

**Exit criteria:** an engineer knows where to look and what is off limits without asking.

**Checkpoint:** briefing, closing on the open question.

## Phase 2: Diagnose

**Who:** an `orchestra:engineer` instance, with `orchestra:debugging`. It may send bulk log or code reading to subagents that return digests.

**Brief:** `brief.md`, the architecture doc, glossary and ADRs if they exist, the run folder for scratch scripts, the artifact path `diagnosis.md`, the report path, and a reminder that this flow changes no product code and nothing in running systems.

**Produces:** `diagnosis.md`: the root cause or the remaining candidates, ranked; the evidence for and against each, with the commands or queries that produced it; what was ruled out; and the recommended next step, with any mitigation written as a proposal.

**Exit criteria:** the conclusion explains every symptom in the brief, or says which ones it does not; every claim carries evidence someone else could rerun.

**Checkpoint:** peer check by a fresh `orchestra:reviewer` instance, briefed as a critic of the diagnosis: does the evidence support the conclusion, and what other explanation fits the same facts? It records findings with `orchestra:feedback`. Give it `diagnosis.md`, `brief.md` and the ledger details for the engineer.

## Phase 3: Findings

**Who:** you, with the user.

Briefing from the engineer's report: the cause or candidates, the recommended next step and the proposals, each as a question with the engineer's recommendation. Ask for a short digest from the engineer if the report is too thin to brief from. If the cause is a defect and the user wants it fixed, offer the bug-fix flow and resume the same engineer for it with `diagnosis.md` as its brief. Mitigations the user approves are theirs to carry out, or a separate request.
