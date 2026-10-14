# Backlog tools for Orchestra

Sources: the two repositories, shallow-cloned and read on 2026-10-14 (README, CLI reference, docs, and Backlog.md's own task files), plus their GitHub pages for stars and releases.

## Recommendation

Use Beads. It stores state once per repository rather than per branch, so every engineer worktree sees the same task state at once. `bd ready --claim --json` atomically hands one ready task to one agent, which matches the conductor and engineer loop with no glue code. The cost is a heavy, fast-moving tool: parallel writers on one machine need Dolt server mode, and Orchestra should pin a version. Backlog.md is the simpler fallback if a single process (the conductor) performs every write.

## Comparison table

| | Backlog.md | Beads (`bd`) |
|---|---|---|
| Canonical repo | github.com/MrLesk/Backlog.md | github.com/gastownhall/beads (steveyegge/beads now resolves there) |
| Storage | Markdown + YAML frontmatter in `backlog/tasks/`, committed on the branch | Dolt SQL database in `.beads/`, gitignored; shared by all worktrees |
| Ready query | `backlog task list --ready` | `bd ready` |
| Atomic claim | No | Yes, `--claim` |
| Cross-worktree state | Branch-local in v1.53.0 | Shared immediately |
| Interface | CLI (default) and MCP | CLI + hooks (preferred); MCP via separate `beads-mcp` |
| JSON | `--json`, versioned schema | `--json` on most commands |
| Runtime | npm/Homebrew/Nix; Bun-built native binary | Go binary via Homebrew, npm, or install script |
| License | MIT | MIT |
| Stars (GitHub, 2026-10-14) | 7.0k | 27.9k |
| Latest release | v1.53.0, 2026-09-24 | v1.3.1, 2026-09-30 (v1.3.2-rc.2 on 2026-10-10) |
| Last commit | 2026-10-14 | 2026-10-14 |

## Backlog.md

Backlog.md is a Markdown task manager with a terminal Kanban board and a local web UI. Each task is one file such as `backlog/tasks/back-760 - <title>.md`, with YAML frontmatter (status, assignee, dependencies, priority) and marked sections for description, acceptance criteria, Definition of Done, plan, notes, and final summary. Acceptance criteria are an indexed checklist (`--ac`, `--check-ac 1`), so a reviewer can read and tick them directly.

Dependencies are declared with `--dep`. `task list --ready` returns unfinished tasks whose dependencies are all completed, and fails closed on unknown or ambiguous IDs. `task view --json` adds a `readiness` object naming the blocking dependencies. The list JSON has about 20 compact fields per task (no bodies), plus `--limit`, `--max-count`, and status, assignee, and label filters. `--plain` gives text output for agents.

Claiming means editing the task: `task edit 7 -s "In Progress" -a @agent`. Nothing makes this exclusive. The project's open task BACK-759 would make `-a` refuse an assigned task; it is still To Do.

The CLI is the default agent interface, and `backlog instructions overview` prints workflow guidance. MCP is optional: `claude mcp add backlog --scope user -- backlog mcp start`, with tools including `task_list` (which has a ready filter), `task_view`, `task_edit`, and `task_complete`. `backlog init` can write the CLAUDE.md instructions or configure MCP for Claude Code. It needs no server or account, and Git is optional.

The project is active: six releases between 2026-08-03 and 2026-09-24, and its own backlog is kept in the repo.

## Beads

Beads is a "distributed graph issue tracker for AI agents, powered by Dolt". By default it runs Dolt embedded in the `bd` process with data in `.beads/embeddeddolt/`. The database directory is gitignored. Sync between machines uses `bd dolt push/pull` against `refs/dolt/data`, and `.beads/issues.jsonl` is an export, not the source of truth. IDs are hashes (`bd-a1b2`), with hierarchical children (`bd-a3f8.1`) for epics.

`bd dep add` creates edges, and the edge types include blocks, waits-for, parent-child, and related. `bd ready` excludes in-progress, blocked, and deferred issues and supports `--json`, `--limit` (default 100), `--unassigned`, `--parent`, label filters, and `--explain`. `bd update <id> --claim` atomically sets the assignee and `in_progress`; the first claim wins and repeating your own claim is idempotent. `bd close <id> --reason` finishes the task. Issues have a dedicated `--acceptance` field, separate from design and notes, and `bd show <id> --json` reads it.

The docs prefer CLI plus hooks over MCP for context efficiency. They claim MCP schemas cost 10-50k tokens versus about 1-2k for `bd prime`. `bd setup claude` installs a SessionStart hook running `bd prime --hook-json`. A Claude Code plugin installs with `/plugin marketplace add gastownhall/beads`. A Python MCP server (`beads-mcp`, PyPI) exists for MCP-only clients.

The scope is broad: molecules, gates, messaging, federation, an experimental HTTP backend, and Jira, Linear, and GitHub sync. The README documents schema migrations and a schema-version guard that blocks an older binary.

## Worktree and parallelism concerns

This is where the two tools differ most. Backlog.md task state lives in files on the branch. Its own task BACK-760, written against v1.53.0, records that when one worktree sets a task In Progress and assigns it, other worktrees still show it as To Do and unassigned, before and after the commit, so "a second agent can take the same task and neither is told". BACK-760 also notes that task files edited on two branches produce merge conflicts, even on adjacent frontmatter lines. The planned fix (shared metadata in a Git ref outside the branches, exclusive assignment) is not implemented. Backlog.md would work today only if Orchestra routed every `backlog` call to the main checkout (for example via `BACKLOG_CWD`) and the conductor serialized claims. That is our inference, not a documented pattern.

In Beads, all linked worktrees discover the repository's single `.beads` workspace, and issue changes never touch Git branches, so status updates cause no merge conflicts. Embedded mode, however, is "single-writer (enforced via file lock)", and the FAQ says to use server mode for "multiple concurrent processes on one machine". Server mode auto-starts a local `dolt sql-server` and requires the separate `dolt` CLI. It is local and needs no account, but it is a background process.

## Open questions

- With several engineers calling `bd` at once in embedded mode, do callers wait for the lock or fail with "database is locked"? The docs do not say, and the code sets a 30-second Dolt open timeout. Test this before choosing between embedded and server mode.
- Does Orchestra accept a locally auto-started Dolt server as "no server"?
- The exact field set of `bd ready --json` is not documented on the `ready` page; measure its size per task.
- Beads ships schema migrations often. Which version should Orchestra pin, and who runs `bd migrate`?
- If Backlog.md ships BACK-760, it would remove its main gap; no target date is documented.
