#!/usr/bin/env python3
"""
tasks: Orchestra's task store, with one small interface for every role.

Operations (each prints one JSON object on stdout):

    create   --kind feature|story|task --title T [--parent ID] [--milestone M]
             [--blocked-by ID]... [--acceptance TEXT]... [--description TEXT]
    ready    [--kind story] [--milestone M]       unblocked, unclaimed work
    claim    ID --by WHO                          first claim wins
    release  ID --by WHO                          give a claim back
    show     ID                                   one task in full
    note     ID --by WHO --text TEXT              append a progress note or ruling
    close    ID --by WHO [--link REF]             mark done, with the change
    edit     ID [--title] [--acceptance]... [--blocked-by]... [--milestone]
             [--description] [--status todo|dropped]
    list     [--kind] [--status] [--milestone]    compact overview

Global option: --root PATH, the project root holding .orchestra/config.toml.
Without it, the script looks upward from the current folder.

Errors print {"error": NAME, "message": TEXT} on stderr and exit 1. NAME is
one of UnknownTask, AlreadyClaimed, Blocked, InvalidState, InvalidValue,
BackendUnavailable or ConfigError.

The Git adapter keeps one Markdown file per task on a dedicated branch
(default orchestra/tasks), written with Git plumbing so no worktree ever
checks it out. Every write is a compare-and-swap: locally through
`git update-ref <new> <old>`, across machines through a non-forced push. A
writer that loses the race reloads and tries again, so the first claim wins.

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
import tomllib
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

KINDS = {"feature": "F", "story": "S", "task": "T"}
STATUSES = ("todo", "in_progress", "done", "dropped")
FIELDS = ("id", "kind", "title", "status", "parent", "milestone", "blocked_by",
          "assignee", "acceptance", "notes", "link", "created", "updated")
MAX_ATTEMPTS = 8


class TaskError(Exception):
    name = "TaskError"


class UnknownTask(TaskError):
    name = "UnknownTask"


class AlreadyClaimed(TaskError):
    name = "AlreadyClaimed"


class Blocked(TaskError):
    name = "Blocked"


class InvalidState(TaskError):
    name = "InvalidState"


class InvalidValue(TaskError):
    name = "InvalidValue"


class BackendUnavailable(TaskError):
    name = "BackendUnavailable"


class ConfigError(TaskError):
    name = "ConfigError"


# ---------------------------------------------------------------------------
# Core: tasks as values, operations as pure functions over a board
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Task:
    id: str
    kind: str
    title: str
    status: str
    parent: str | None
    milestone: str | None
    blocked_by: tuple[str, ...]
    assignee: str | None
    acceptance: tuple[str, ...]
    description: str
    notes: tuple[dict, ...]
    link: str | None
    created: str
    updated: str

    def as_json(self) -> dict:
        return {f: list(v) if isinstance(v := getattr(self, f), tuple) else v
                for f in (*FIELDS, "description")}


Board = dict[str, Task]


def render(task: Task) -> str:
    data = task.as_json()
    head = "".join(f"{f}: {json.dumps(data[f], ensure_ascii=False)}\n" for f in FIELDS)
    body = task.description + "\n" if task.description else ""
    return f"---\n{head}---\n{body}"


def parse(text: str) -> Task:
    _, head, body = text.split("---\n", 2)
    data = {}
    for line in head.splitlines():
        key, value = line.split(": ", 1)
        data[key] = json.loads(value)
    for f in ("blocked_by", "acceptance"):
        data[f] = tuple(data[f])
    data["notes"] = tuple(data["notes"])
    data["description"] = body[:-1] if body.endswith("\n") else body
    return Task(**data)


def number(task_id: str) -> int:
    return int(task_id.split("-", 1)[1])


def next_id(kind: str, board: Board) -> str:
    prefix = KINDS[kind]
    used = [number(i) for i in board if i.startswith(prefix + "-")]
    return f"{prefix}-{max(used, default=0) + 1}"


def sorted_tasks(tasks) -> list[Task]:
    return sorted(tasks, key=lambda t: (list(KINDS).index(t.kind), number(t.id)))


def unmet_blockers(board: Board, task: Task) -> list[str]:
    return [b for b in task.blocked_by
            if b not in board or board[b].status not in ("done", "dropped")]


def ready(board: Board, kind: str, milestone: str | None) -> list[Task]:
    return sorted_tasks(
        t for t in board.values()
        if t.kind == kind and t.status == "todo" and t.assignee is None
        and (milestone is None or t.milestone == milestone)
        and not unmet_blockers(board, t)
    )


def get(board: Board, task_id: str) -> Task:
    if task_id not in board:
        raise UnknownTask(f"no task '{task_id}'")
    return board[task_id]


def check_refs(board: Board, ids) -> tuple[str, ...]:
    for i in ids:
        get(board, i)
    return tuple(ids)


def create(board: Board, *, kind: str, title: str, parent: str | None,
           milestone: str | None, blocked_by, acceptance, description: str,
           now: str) -> Task:
    if kind not in KINDS:
        raise InvalidValue(f"kind '{kind}' is not one of: {', '.join(KINDS)}")
    if kind == "task" and parent is None:
        raise InvalidValue("a task needs --parent, the story it belongs to")
    if parent is not None:
        get(board, parent)
    return Task(
        id=next_id(kind, board), kind=kind, title=title, status="todo",
        parent=parent, milestone=milestone, blocked_by=check_refs(board, blocked_by),
        assignee=None, acceptance=tuple(acceptance), description=description,
        notes=(), link=None, created=now, updated=now,
    )


def claim(board: Board, task_id: str, *, by: str, now: str) -> Task:
    t = get(board, task_id)
    if t.assignee == by and t.status == "in_progress":
        return t
    if t.assignee is not None:
        raise AlreadyClaimed(f"{task_id} is claimed by {t.assignee}")
    if t.status != "todo":
        raise InvalidState(f"{task_id} is {t.status}, not todo")
    if blockers := unmet_blockers(board, t):
        raise Blocked(f"{task_id} waits on {', '.join(blockers)}")
    return replace(t, status="in_progress", assignee=by, updated=now)


def release(board: Board, task_id: str, *, by: str, now: str) -> Task:
    t = get(board, task_id)
    if t.assignee is None:
        raise InvalidState(f"{task_id} is not claimed")
    if t.assignee != by:
        raise AlreadyClaimed(f"{task_id} is claimed by {t.assignee}")
    return replace(t, status="todo", assignee=None, updated=now)


def note(board: Board, task_id: str, *, by: str, text: str, now: str) -> Task:
    t = get(board, task_id)
    return replace(t, notes=(*t.notes, {"at": now, "by": by, "text": text}), updated=now)


def close(board: Board, task_id: str, *, by: str, link: str | None, now: str) -> Task:
    t = get(board, task_id)
    if t.assignee is not None and t.assignee != by:
        raise AlreadyClaimed(f"{task_id} is claimed by {t.assignee}")
    if t.status in ("done", "dropped"):
        raise InvalidState(f"{task_id} is already {t.status}")
    return replace(t, status="done", link=link, updated=now)


def edit(board: Board, task_id: str, *, changes: dict, now: str) -> Task:
    t = get(board, task_id)
    if "status" in changes and changes["status"] not in ("todo", "dropped"):
        raise InvalidValue("edit can only set status to todo or dropped")
    if changes.get("status") == "todo":
        changes = {**changes, "assignee": None}
    if "blocked_by" in changes:
        changes = {**changes, "blocked_by": check_refs(board, changes["blocked_by"])}
    if "acceptance" in changes:
        changes = {**changes, "acceptance": tuple(changes["acceptance"])}
    return replace(t, **changes, updated=now)


# ---------------------------------------------------------------------------
# Git adapter
# ---------------------------------------------------------------------------


class GitFailed(Exception):
    def __init__(self, stderr: str):
        super().__init__(stderr)
        self.stderr = stderr


class GitStore:
    """Tasks as files under tasks/ on one branch, updated by compare-and-swap."""

    def __init__(self, root: Path, branch: str, remote: str | None):
        self.root = root
        self.ref = f"refs/heads/{branch}"
        self.branch = branch
        self.remote = remote
        self.tracking = f"refs/remotes/{remote}/{branch}" if remote else None

    def git(self, *args: str, input: str | None = None, env: dict | None = None) -> str:
        try:
            p = subprocess.run(
                ["git", "-C", str(self.root), *args], input=input, capture_output=True,
                text=True, env={**os.environ, **(env or {})},
            )
        except FileNotFoundError as e:
            raise BackendUnavailable("git is not installed") from e
        if p.returncode != 0:
            raise GitFailed(p.stderr.strip())
        return p.stdout

    def resolve(self, ref: str) -> str | None:
        try:
            return self.git("rev-parse", "--verify", "-q", ref).strip() or None
        except GitFailed:
            return None

    def load(self) -> tuple[str | None, Board]:
        if self.remote:
            try:
                self.git("fetch", "-q", self.remote, f"+{self.ref}:{self.tracking}")
                base = self.resolve(self.tracking)
            except GitFailed as e:
                if "couldn't find remote ref" not in e.stderr:
                    raise BackendUnavailable(f"fetching {self.remote}: {e.stderr}") from e
                base = None
        else:
            base = self.resolve(self.ref)
        return base, self.read(base) if base else {}

    def read(self, commit: str) -> Board:
        listing = self.git("ls-tree", "-r", commit, "tasks/")
        shas = [line.split()[2] for line in listing.splitlines() if line.endswith(".md")]
        if not shas:
            return {}
        out = subprocess.run(
            ["git", "-C", str(self.root), "cat-file", "--batch"],
            input=("\n".join(shas) + "\n").encode(), capture_output=True, check=True,
        ).stdout
        board, pos = {}, 0
        for _ in shas:
            header_end = out.index(b"\n", pos)
            size = int(out[pos:header_end].split()[2])
            start = header_end + 1
            task = parse(out[start:start + size].decode("utf-8"))
            board[task.id] = task
            pos = start + size + 1
        return board

    def save(self, base: str | None, changed: list[Task], message: str) -> bool:
        """Write the changed tasks on top of base. False means someone else won."""
        with tempfile.TemporaryDirectory() as tmp:
            env = {"GIT_INDEX_FILE": str(Path(tmp) / "index")}
            try:
                self.git("read-tree", *([base] if base else ["--empty"]), env=env)
                for t in changed:
                    sha = self.git("hash-object", "-w", "--stdin", input=render(t)).strip()
                    self.git("update-index", "--add", "--cacheinfo",
                             f"100644,{sha},tasks/{t.id}.md", env=env)
                tree = self.git("write-tree", env=env).strip()
                parents = ["-p", base] if base else []
                commit = self.git("commit-tree", tree, *parents, "-m", message).strip()
            except GitFailed as e:
                raise BackendUnavailable(f"writing tasks: {e.stderr}") from e
        if self.remote:
            return self.push(commit)
        try:
            self.git("update-ref", self.ref, commit, base or "")
        except GitFailed:
            return False
        return True

    def push(self, commit: str) -> bool:
        try:
            self.git("push", "-q", self.remote, f"{commit}:{self.ref}")
        except GitFailed as e:
            if any(s in e.stderr for s in ("rejected", "non-fast-forward", "fetch first")):
                return False
            raise BackendUnavailable(f"pushing to {self.remote}: {e.stderr}") from e
        self.git("update-ref", self.ref, commit)
        self.git("update-ref", self.tracking, commit)
        return True


def transact(store: GitStore, change: Callable[[Board], tuple[dict, list[Task]]],
             message: str, sleep: Callable[[float], None] = time.sleep) -> dict:
    """Load, apply, save; on a lost race, reload and apply again."""
    for attempt in range(MAX_ATTEMPTS):
        base, board = store.load()
        result, changed = change(board)
        if not changed or store.save(base, changed, message):
            return result
        sleep(random.uniform(0, 0.05 * (attempt + 1)))
    raise BackendUnavailable(f"gave up after {MAX_ATTEMPTS} conflicting writes")


# ---------------------------------------------------------------------------
# Configuration and CLI
# ---------------------------------------------------------------------------


def find_root(start: Path) -> Path:
    for folder in (start, *start.parents):
        if (folder / ".orchestra" / "config.toml").is_file():
            return folder
    return start


def open_store(root: Path) -> GitStore:
    path = root / ".orchestra" / "config.toml"
    try:
        config = tomllib.loads(path.read_text()) if path.is_file() else {}
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"{path}: {e}") from e
    section = config.get("tasks", {})
    adapter = section.get("adapter", "git")
    if adapter != "git":
        raise ConfigError(f"adapter '{adapter}' is not available; only 'git' is")
    return GitStore(root, section.get("branch", "orchestra/tasks"), section.get("remote") or None)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def summary(t: Task, *fields: str) -> dict:
    data = t.as_json()
    return {f: data[f] for f in fields}


def command(args: argparse.Namespace, store: GitStore, clock: Callable[[], str]) -> dict:
    ts = clock()
    one = lambda t: ({"id": t.id}, [t])  # noqa: E731

    def write(fn: Callable[[Board], Task], shape: Callable[[Task], dict]) -> dict:
        def change(board: Board):
            t = fn(board)
            return shape(t), ([] if board.get(t.id) == t else [t])
        return transact(store, change, f"{args.command} {args.id or ''} {args.by or ''}".strip())

    match args.command:
        case "create":
            return transact(store, lambda b: one(create(
                b, kind=args.kind, title=args.title, parent=args.parent,
                milestone=args.milestone, blocked_by=args.blocked_by or [],
                acceptance=args.acceptance or [], description=args.description or "",
                now=ts)), f"create {args.kind}")
        case "ready":
            _, board = store.load()
            return {"ready": [summary(t, "id", "title", "milestone", "parent")
                              for t in ready(board, args.kind, args.milestone)]}
        case "list":
            _, board = store.load()
            picked = [t for t in sorted_tasks(board.values())
                      if (args.kind is None or t.kind == args.kind)
                      and (args.status is None or t.status == args.status)
                      and (args.milestone is None or t.milestone == args.milestone)]
            return {"tasks": [summary(t, "id", "kind", "title", "status", "assignee",
                                      "milestone", "parent") for t in picked]}
        case "show":
            _, board = store.load()
            return get(board, args.id).as_json()
        case "claim":
            return write(lambda b: claim(b, args.id, by=args.by, now=ts),
                         lambda t: summary(t, "id", "status", "assignee"))
        case "release":
            return write(lambda b: release(b, args.id, by=args.by, now=ts),
                         lambda t: summary(t, "id", "status"))
        case "note":
            return write(lambda b: note(b, args.id, by=args.by, text=args.text, now=ts),
                         lambda t: {"id": t.id, "notes": len(t.notes)})
        case "close":
            return write(lambda b: close(b, args.id, by=args.by, link=args.link, now=ts),
                         lambda t: summary(t, "id", "status", "link"))
        case "edit":
            changes = {k: v for k, v in (
                ("title", args.title), ("acceptance", args.acceptance),
                ("blocked_by", args.blocked_by), ("milestone", args.milestone),
                ("description", args.description), ("status", args.status),
            ) if v is not None}
            return write(lambda b: edit(b, args.id, changes=changes, now=ts),
                         lambda t: {"id": t.id})
    raise InvalidValue(f"unknown command {args.command}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Orchestra task store")
    p.add_argument("--root", type=Path)
    sub = p.add_subparsers(dest="command", required=True)

    def cmd(name: str, with_id: bool = False, by: bool = False) -> argparse.ArgumentParser:
        sp = sub.add_parser(name)
        sp.set_defaults(id=None, by=None)
        if with_id:
            sp.add_argument("id")
        if by:
            sp.add_argument("--by", required=True)
        return sp

    c = cmd("create")
    c.add_argument("--kind", required=True)
    c.add_argument("--title", required=True)
    c.add_argument("--parent")
    c.add_argument("--milestone")
    c.add_argument("--blocked-by", action="append")
    c.add_argument("--acceptance", action="append")
    c.add_argument("--description")

    r = cmd("ready")
    r.add_argument("--kind", default="story")
    r.add_argument("--milestone")

    li = cmd("list")
    li.add_argument("--kind")
    li.add_argument("--status", choices=STATUSES)
    li.add_argument("--milestone")

    cmd("show", with_id=True)
    cmd("claim", with_id=True, by=True)
    cmd("release", with_id=True, by=True)
    n = cmd("note", with_id=True, by=True)
    n.add_argument("--text", required=True)
    cl = cmd("close", with_id=True, by=True)
    cl.add_argument("--link")

    e = cmd("edit", with_id=True)
    e.add_argument("--title")
    e.add_argument("--acceptance", action="append")
    e.add_argument("--blocked-by", action="append")
    e.add_argument("--milestone")
    e.add_argument("--description")
    e.add_argument("--status")
    return p


def main(argv: list[str] | None = None, clock: Callable[[], str] = now) -> int:
    args = build_parser().parse_args(argv)
    try:
        root = (args.root or find_root(Path.cwd())).resolve()
        result = command(args, open_store(root), clock)
    except TaskError as e:
        print(json.dumps({"error": e.name, "message": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
