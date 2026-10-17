"""
Tests for the tasks script and its Git adapter.

Run with:
    python3 skills/tasks/tests/test_tasks.py

Unit tests exercise the pure core. Integration tests run the CLI against real
Git repositories in temporary folders: one repository with two worktrees for
parallel claims on one machine, and two clones of a bare remote for claims
from two machines.
"""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "tasks.py"
sys.path.insert(0, str(ROOT / "scripts"))

import tasks  # noqa: E402

NOW = "2026-10-18T10:00:00+00:00"


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def init_repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    git(path, "init", "-q", "-b", "main")
    git(path, "config", "user.name", "Test")
    git(path, "config", "user.email", "test@example.com")
    (path / "README.md").write_text("project\n")
    git(path, "add", ".")
    git(path, "commit", "-q", "-m", "init")
    return path


def write_config(root: Path, remote: str | None = None) -> None:
    (root / ".orchestra").mkdir(exist_ok=True)
    lines = ["[tasks]", 'adapter = "git"', 'branch = "orchestra/tasks"']
    if remote:
        lines.append(f'remote = "{remote}"')
    (root / ".orchestra" / "config.toml").write_text("\n".join(lines) + "\n")


def run(root: Path, *argv: str) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = tasks.main(["--root", str(root), *argv])
    text = out.getvalue() if code == 0 else err.getvalue()
    return code, json.loads(text)


def run_process(root: Path, *argv: str) -> tuple[int, dict]:
    p = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), *argv],
        capture_output=True, text=True,
    )
    return p.returncode, json.loads(p.stdout if p.returncode == 0 else p.stderr)


def story(id: str, status: str = "todo", blocked_by: tuple[str, ...] = (),
          assignee: str | None = None, milestone: str | None = "M1") -> tasks.Task:
    return tasks.Task(
        id=id, kind="story", title=f"Story {id}", status=status, parent=None,
        milestone=milestone, blocked_by=blocked_by, assignee=assignee,
        acceptance=("it works",), description="", notes=(), link=None,
        created=NOW, updated=NOW,
    )


# ---------------------------------------------------------------------------
# Pure core
# ---------------------------------------------------------------------------


class CoreTest(unittest.TestCase):
    def test_task_file_round_trips(self) -> None:
        t = story("S-1", blocked_by=("S-0",))
        t = tasks.Task(**{**t.__dict__, "description": "Line one.\n\nLine two.",
                          "notes": ({"at": NOW, "by": "eng", "text": "started"},)})
        self.assertEqual(tasks.parse(tasks.render(t)), t)

    def test_next_id_counts_per_kind(self) -> None:
        existing = {"S-1": story("S-1"), "S-7": story("S-7")}
        self.assertEqual(tasks.next_id("story", existing), "S-8")
        self.assertEqual(tasks.next_id("feature", existing), "F-1")
        self.assertEqual(tasks.next_id("task", existing), "T-1")

    def test_ready_lists_unblocked_unclaimed_stories(self) -> None:
        board = {
            "S-1": story("S-1", status="done"),
            "S-2": story("S-2", blocked_by=("S-1",)),
            "S-3": story("S-3", blocked_by=("S-2",)),
            "S-4": story("S-4", assignee="eng-1", status="in_progress"),
            "S-5": story("S-5", milestone="M2"),
        }
        ids = [t.id for t in tasks.ready(board, kind="story", milestone=None)]
        self.assertEqual(ids, ["S-2", "S-5"])
        ids = [t.id for t in tasks.ready(board, kind="story", milestone="M1")]
        self.assertEqual(ids, ["S-2"])

    def test_dropped_blocker_no_longer_blocks(self) -> None:
        board = {"S-1": story("S-1", status="dropped"),
                 "S-2": story("S-2", blocked_by=("S-1",))}
        self.assertEqual([t.id for t in tasks.ready(board, "story", None)], ["S-2"])

    def test_claim_rules(self) -> None:
        board = {"S-1": story("S-1"), "S-2": story("S-2", blocked_by=("S-1",)),
                 "S-3": story("S-3", status="in_progress", assignee="eng-1")}
        claimed = tasks.claim(board, "S-1", by="eng-2", now=NOW)
        self.assertEqual((claimed.status, claimed.assignee), ("in_progress", "eng-2"))
        with self.assertRaises(tasks.Blocked):
            tasks.claim(board, "S-2", by="eng-2", now=NOW)
        with self.assertRaises(tasks.AlreadyClaimed):
            tasks.claim(board, "S-3", by="eng-2", now=NOW)
        self.assertEqual(tasks.claim(board, "S-3", by="eng-1", now=NOW), board["S-3"])
        with self.assertRaises(tasks.UnknownTask):
            tasks.claim(board, "S-9", by="eng-2", now=NOW)

    def test_close_by_someone_else_is_refused(self) -> None:
        board = {"S-1": story("S-1", status="in_progress", assignee="eng-1")}
        with self.assertRaises(tasks.AlreadyClaimed):
            tasks.close(board, "S-1", by="eng-2", link=None, now=NOW)
        done = tasks.close(board, "S-1", by="eng-1", link="abc123", now=NOW)
        self.assertEqual((done.status, done.link), ("done", "abc123"))


# ---------------------------------------------------------------------------
# CLI against a real Git repository
# ---------------------------------------------------------------------------


class GitAdapterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(Path(self.tmp.name) / "repo")
        write_config(self.repo)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_create_show_and_ready(self) -> None:
        code, f = run(self.repo, "create", "--kind", "feature", "--title", "Sharing")
        self.assertEqual((code, f["id"]), (0, "F-1"))
        _, s1 = run(self.repo, "create", "--kind", "story", "--title", "Invite",
                    "--parent", "F-1", "--milestone", "M1",
                    "--acceptance", "Invitee sees the list", "--acceptance", "Link expires")
        _, s2 = run(self.repo, "create", "--kind", "story", "--title", "Revoke",
                    "--parent", "F-1", "--blocked-by", s1["id"])
        code, shown = run(self.repo, "show", s1["id"])
        self.assertEqual(code, 0)
        self.assertEqual(shown["acceptance"], ["Invitee sees the list", "Link expires"])
        code, out = run(self.repo, "ready")
        self.assertEqual([t["id"] for t in out["ready"]], [s1["id"]])
        self.assertEqual(set(out["ready"][0]), {"id", "title", "milestone", "parent"})

    def test_tasks_never_touch_the_working_branch(self) -> None:
        run(self.repo, "create", "--kind", "story", "--title", "Invite")
        self.assertEqual(git(self.repo, "rev-parse", "--abbrev-ref", "HEAD"), "main")
        self.assertEqual(git(self.repo, "status", "--porcelain"), "?? .orchestra/")
        files = git(self.repo, "ls-tree", "-r", "--name-only", "orchestra/tasks")
        self.assertEqual(files, "tasks/S-1.md")

    def test_story_lifecycle(self) -> None:
        run(self.repo, "create", "--kind", "story", "--title", "Invite")
        run(self.repo, "create", "--kind", "story", "--title", "Revoke", "--blocked-by", "S-1")
        code, c = run(self.repo, "claim", "S-1", "--by", "eng-1")
        self.assertEqual((code, c["status"]), (0, "in_progress"))
        run(self.repo, "note", "S-1", "--by", "eng-1", "--text", "Ruling: tokens expire in 7 days")
        code, _ = run(self.repo, "close", "S-1", "--by", "eng-1", "--link", "abc123")
        self.assertEqual(code, 0)
        _, shown = run(self.repo, "show", "S-1")
        self.assertEqual(shown["status"], "done")
        self.assertEqual(shown["notes"][0]["text"], "Ruling: tokens expire in 7 days")
        _, out = run(self.repo, "ready")
        self.assertEqual([t["id"] for t in out["ready"]], ["S-2"])

    def test_release_returns_story_to_ready(self) -> None:
        run(self.repo, "create", "--kind", "story", "--title", "Invite")
        run(self.repo, "claim", "S-1", "--by", "eng-1")
        code, _ = run(self.repo, "release", "S-1", "--by", "eng-1")
        self.assertEqual(code, 0)
        _, out = run(self.repo, "ready")
        self.assertEqual([t["id"] for t in out["ready"]], ["S-1"])

    def test_edit_and_drop(self) -> None:
        run(self.repo, "create", "--kind", "story", "--title", "Invite")
        code, _ = run(self.repo, "edit", "S-1", "--title", "Invite by link",
                      "--acceptance", "Link works once")
        self.assertEqual(code, 0)
        _, shown = run(self.repo, "show", "S-1")
        self.assertEqual((shown["title"], shown["acceptance"]), ("Invite by link", ["Link works once"]))
        run(self.repo, "edit", "S-1", "--status", "dropped")
        _, out = run(self.repo, "ready")
        self.assertEqual(out["ready"], [])

    def test_task_under_story_needs_existing_parent(self) -> None:
        code, err = run(self.repo, "create", "--kind", "task", "--title", "Schema", "--parent", "S-9")
        self.assertEqual((code, err["error"]), (1, "UnknownTask"))
        code, err = run(self.repo, "create", "--kind", "task", "--title", "Schema")
        self.assertEqual((code, err["error"]), (1, "InvalidValue"))

    def test_specific_errors(self) -> None:
        code, err = run(self.repo, "show", "S-1")
        self.assertEqual((code, err["error"]), (1, "UnknownTask"))
        run(self.repo, "create", "--kind", "story", "--title", "Invite")
        run(self.repo, "claim", "S-1", "--by", "eng-1")
        code, err = run(self.repo, "claim", "S-1", "--by", "eng-2")
        self.assertEqual((code, err["error"]), (1, "AlreadyClaimed"))

    def test_list_filters_by_status(self) -> None:
        run(self.repo, "create", "--kind", "story", "--title", "Invite")
        run(self.repo, "create", "--kind", "story", "--title", "Revoke")
        run(self.repo, "claim", "S-2", "--by", "eng-1")
        _, out = run(self.repo, "list", "--status", "in_progress")
        self.assertEqual([t["id"] for t in out["tasks"]], ["S-2"])
        self.assertEqual(out["tasks"][0]["assignee"], "eng-1")

    def test_parallel_claims_from_two_worktrees(self) -> None:
        run(self.repo, "create", "--kind", "story", "--title", "Invite")
        wt = [Path(self.tmp.name) / f"wt{i}" for i in (1, 2)]
        for i, path in enumerate(wt, 1):
            git(self.repo, "worktree", "add", "-q", "-b", f"story-{i}", str(path))
            write_config(path)
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(
                lambda i: run_process(wt[i], "claim", "S-1", "--by", f"eng-{i + 1}"), range(2)))
        codes = sorted(code for code, _ in results)
        self.assertEqual(codes, [0, 1])
        loser = next(out for code, out in results if code == 1)
        self.assertEqual(loser["error"], "AlreadyClaimed")

    def test_parallel_creates_get_distinct_ids(self) -> None:
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(
                lambda i: run_process(self.repo, "create", "--kind", "story", "--title", f"S{i}"),
                range(4)))
        self.assertEqual(sorted(out["id"] for _, out in results), ["S-1", "S-2", "S-3", "S-4"])


class GitRemoteTest(unittest.TestCase):
    """Two clones of one bare remote stand in for two machines."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        origin = init_repo(base / "seed")
        git(base, "clone", "-q", "--bare", str(origin), "remote.git")
        self.a = base / "a"
        self.b = base / "b"
        for clone in (self.a, self.b):
            git(base, "clone", "-q", str(base / "remote.git"), clone.name)
            git(clone, "config", "user.name", "Test")
            git(clone, "config", "user.email", "test@example.com")
            write_config(clone, remote="origin")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_claim_on_one_machine_is_seen_on_the_other(self) -> None:
        run(self.a, "create", "--kind", "story", "--title", "Invite")
        code, out = run(self.b, "ready")
        self.assertEqual([t["id"] for t in out["ready"]], ["S-1"])
        self.assertEqual(run(self.a, "claim", "S-1", "--by", "eng-a")[0], 0)
        code, err = run(self.b, "claim", "S-1", "--by", "eng-b")
        self.assertEqual((code, err["error"]), (1, "AlreadyClaimed"))

    def test_stale_clone_retries_after_rejected_push(self) -> None:
        run(self.a, "create", "--kind", "story", "--title", "Invite")
        run(self.b, "ready")  # b now has a stale copy of the branch
        run(self.a, "create", "--kind", "story", "--title", "Revoke")
        code, out = run(self.b, "create", "--kind", "story", "--title", "Export")
        self.assertEqual((code, out["id"]), (0, "S-3"))
        _, listed = run(self.a, "list")
        self.assertEqual([t["id"] for t in listed["tasks"]], ["S-1", "S-2", "S-3"])

    def test_unreachable_remote_is_backend_unavailable(self) -> None:
        git(self.a, "remote", "set-url", "origin", str(Path(self.tmp.name) / "missing.git"))
        code, err = run(self.a, "create", "--kind", "story", "--title", "Invite")
        self.assertEqual((code, err["error"]), (1, "BackendUnavailable"))


class ConfigTest(unittest.TestCase):
    def test_unknown_adapter_is_a_config_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = init_repo(Path(tmp) / "repo")
            (root / ".orchestra").mkdir()
            (root / ".orchestra" / "config.toml").write_text('[tasks]\nadapter = "jira"\n')
            code, err = run(root, "ready")
            self.assertEqual((code, err["error"]), (1, "ConfigError"))

    def test_missing_config_defaults_to_git(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = init_repo(Path(tmp) / "repo")
            code, out = run(root, "ready")
            self.assertEqual((code, out["ready"]), (0, []))


if __name__ == "__main__":
    unittest.main(verbosity=2)
