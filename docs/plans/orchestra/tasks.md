# Tasks

Part of the [Orchestra plan](README.md). One task interface for every role, with an adapter per tracking system.

## Interface

Teams track work in different systems (Jira, GitHub Issues, Linear, or nothing beyond the repo), and Orchestra should not care which. Roles never call a tracker directly. They call one small command-line script, `tasks`, which exposes the handful of operations Orchestra needs and passes them to an adapter for the system the project has chosen. The interface is defined by what the roles consume, not by what any tracker offers.

| Operation | Who calls it | What it does |
| --- | --- | --- |
| `create` | architect, engineer | The architect adds features and stories with acceptance criteria, blocking edges and a milestone; an engineer adds tasks under its story |
| `ready` | conductor | Lists stories that are unblocked and unclaimed, as compact JSON with IDs and titles only |
| `claim` | engineer | Assigns a story to the caller and marks it in progress; fails if someone else claimed it first |
| `show` | engineer, reviewer | Returns one task, including its acceptance criteria |
| `note` | engineer | Appends a progress note or a ruling |
| `close` | engineer | Marks the task done, with a link to the change |

Every operation returns short JSON, so reading task state costs the conductor a few lines of context rather than a tracker's full payload. Errors are specific (`AlreadyClaimed`, `UnknownTask`, `BackendUnavailable`) so a role can react to the error instead of parsing prose. A project chooses its adapter in `.orchestra/config.toml`, which the setup step writes once.

`plan.md` keeps only what a task list cannot hold: MVP scope in and out, milestones, and the reasoning behind the sequence.

## Git adapter (MVP)

Tasks are Markdown files, one per task, on a dedicated branch (`orchestra/tasks`) that no feature work touches. Keeping them off feature branches avoids the problem Backlog.md documents in its task BACK-760, where a claim made in one worktree stays invisible in the others and task edits on two branches conflict ([backlog tools notes](../../research/prior-art/backlog-tools.md)).

On one machine, every worktree shares the repository's refs, so the script's writes to that branch are visible to all engineers at once. The script updates the branch with Git's low-level commands and never checks it out, because Git allows a branch to be checked out in only one worktree at a time.

Across machines, a claim is a commit pushed to the shared remote. Git rejects a push that is not a fast-forward, so if two people claim the same task, the second push fails, the script fetches, sees the task is taken, and reports `AlreadyClaimed`. That gives first-claim-wins across machines with nothing installed beyond Git. A collaborator's agent on another computer can pick up a task this way, provided it can push to the same remote. M2 tests parallel claims from two worktrees and from two machines before anything depends on this.

## Tracker adapters (after the MVP)

GitHub Issues through `gh`, Jira through its REST API or command-line client, and Linear through its API, each mapping the six operations onto that system's issues, assignees and blocking links. I know of no atomic claim in these trackers' APIs (each adapter should verify this), so these adapters assign, read back, and back off if someone else's name is there. Beads or Backlog.md could also sit behind the same interface if a team already uses one.

## Implementation

The script lives in its own skill, `skills/tasks/`, whose SKILL.md tells roles which operation to use when. It is written in Python with the standard library only, like skill-linter, so it runs anywhere Python 3 does. Matt Pocock's setup skill solves the same problem with prose instructions per tracker in `docs/agents/issue-tracker.md`. A script with a fixed interface costs fewer tokens per call and behaves the same way every time.
