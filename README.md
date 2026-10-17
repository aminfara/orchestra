# orchestra

Multi-agent development environment: a Claude Code plugin in which a conductor runs software engineering flows with a small team of agent roles. The plan is in [docs/plans/orchestra/README.md](docs/plans/orchestra/README.md).

## Install for development

The repo is its own local marketplace, `orchestra-local`, whose one plugin, `orchestra`, loads in place from the checkout:

```bash
claude plugin marketplace add /path/to/orchestra
claude plugin install orchestra@orchestra-local
```

Where managed settings block local marketplaces, load it for one CLI session instead:

```bash
claude --plugin-dir /path/to/orchestra
```

## Use

Orchestra has two entry points, each for its own session.

- **`orchestra:conductor`** runs the delivery loop. Tell it what you want, and it picks a flow, says which and why, and runs it with the team: the product manager, the architect, engineers and reviewers. It interviews you in batches, holds a review gate at each artifact, and never passes a gate without your approval.
- **`orchestra:coach`** runs the improvement loop, outside any flow. It reads the feedback ledgers that every check and gate writes to, and proposes a few changes to skills, tools, project notes, review intensity or models, each with its evidence, for you to approve.

| Flow | Use it for | Ends with |
| --- | --- | --- |
| idea | An idea worth judging | A PR/FAQ and a go, park or drop decision |
| requirements | A PR/FAQ, research or feature request | A living PRD with a ranked MVP, and the UX design |
| architecture | Selected requirements | An architecture, ADRs, a glossary, and stories in the task store |
| build | A breakdown | Reviewed, integrated and accepted milestones |
| feature task | One story in a build under way | The story integrated |
| new feature | A feature on an existing product | The flows above, chained and scoped to the feature |
| bug fix | A known defect | A reviewed fix with a regression test |
| troubleshoot | A symptom without a known cause | A diagnosis, with no code changed |
| understand | An unfamiliar codebase | An as-is architecture, glossary and risk map |
| rewrite | A system to rebuild | A target, a migration, parity tests, and the build |

Orchestra writes living docs to `docs/` in the project (`docs/product/`, `docs/architecture.md`, `docs/adr/`, `docs/glossary.md`), and per-run files, the task store's settings and the feedback ledger to `.orchestra/`. Commit `.orchestra/config.toml`. Tasks live on a branch, `orchestra/tasks`, that no one checks out.

### Settings

`.orchestra/config.toml` is optional. Every table has defaults.

```toml
[tasks]
adapter = "git"
branch = "orchestra/tasks"
remote = "origin"        # share the board across machines; omit for one machine

[build]
parallel = 3             # engineers working at once

[review]
engineer = "all"         # or "sample", usually set by a coach trial

[models]
engineer = "sonnet"      # override an agent's default model

[coach]
retro_runs = 3           # thresholds for the ledger's signals
```

### Hooks

The plugin installs two hooks. When a session starts, one finds the project's feedback ledgers, registers them so the coach can read across projects, and shows you one line when the ledger says the coach has something to act on. When an Orchestra role stops, the other sends it back once if its report has no status or verdict line or cites findings it never recorded, and logs its token use to the ledger. Neither adds anything to an agent's context.

## Requirements

Python 3.11 or later and Git. The scripts use the standard library only.

## Develop

```bash
python3 skills/tasks/tests/test_tasks.py
```

```bash
python3 skills/feedback/tests/test_feedback.py
```

```bash
python3 hooks/tests/test_hooks.py
```

```bash
python3 skills/skill-linter/scripts/lint.py skills/<name>
```

The plan and its design notes are in [docs/plans/orchestra/](docs/plans/orchestra/README.md).

## Dependencies

### Skills

- skill-creator, used by the coach for eval runs
