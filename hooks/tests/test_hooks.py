"""
Tests for Orchestra's hooks.

Run with:
    python3 hooks/tests/test_hooks.py
"""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOKS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HOOKS))

import orchestra_hooks as hooks  # noqa: E402

REPORT = """**Status:** done
**Summary:** Three components, Postgres.
**Artifacts:** docs/architecture.md
"""


def verdict(text: str) -> str:
    return f"- **Verdict:** {text}\n- **Findings:** 1 medium (f-0000abcd)\n"


def finding(fid: str, **over) -> dict:
    return {"type": "finding", "id": fid, "ts": "2026-10-18T00:00:00.000001+00:00",
            "run": "2026-10-18-build-todo", "flow": "build", "phase": 1, "artifact": "x",
            "role": "engineer", "skill": "none", "skill_version": "none", "skill_lines": 0,
            "model": "sonnet", "effort": "medium", "found_by": "reviewer",
            "category": "gap", "severity": "medium", "finding": "x", "why": "y", **over}


def project(tmp: str, *events: dict, sub: str = "") -> Path:
    root = Path(tmp) / "project"
    ledger = root / sub / ".orchestra" / "feedback.jsonl"
    ledger.parent.mkdir(parents=True)
    ledger.write_text("".join(json.dumps(e) + "\n" for e in events))
    (ledger.parent / "2026-10-18-build-todo").mkdir()
    return root


class CheckTest(unittest.TestCase):
    def test_report_with_status_passes(self) -> None:
        self.assertIsNone(hooks.check(REPORT, known=set()))

    def test_final_message_without_report_shape_is_sent_back(self) -> None:
        reason = hooks.check("I have finished the work.", known=set())
        self.assertIn("report", reason)

    def test_empty_text_cannot_be_judged(self) -> None:
        self.assertIsNone(hooks.check("", known=set()))

    def test_verdict_citing_unrecorded_finding_is_sent_back(self) -> None:
        reason = hooks.check(verdict("revise"), known=set())
        self.assertIn("f-0000abcd", reason)
        self.assertIsNone(hooks.check(verdict("revise"), known={"f-0000abcd"}))

    def test_revise_without_any_ledger_id_is_sent_back(self) -> None:
        reason = hooks.check("**Verdict:** revise\n**For the author:** fix it", known=set())
        self.assertIn("orchestra:feedback", reason)

    def test_pass_without_findings_is_fine(self) -> None:
        self.assertIsNone(hooks.check("**Verdict:** pass\n**Findings:** none", known=set()))

    def test_status_is_read_from_report_or_verdict(self) -> None:
        self.assertEqual(hooks.status_of(REPORT), "done")
        self.assertEqual(hooks.status_of("**Status:** needs a decision\n"), "needs a decision")
        self.assertEqual(hooks.status_of(verdict("pass")), "verdict: pass")
        self.assertEqual(hooks.status_of("nothing"), "unknown")
        self.assertEqual(hooks.status_of("**Verdict:** none. Nothing to review."), "verdict: none")
        self.assertEqual(hooks.status_of("**Status:** finished, mostly"), "finished")


class TranscriptTest(unittest.TestCase):
    def write(self, tmp: str, *entries: dict) -> Path:
        path = Path(tmp) / "agent.jsonl"
        path.write_text("".join(json.dumps(e) + "\n" for e in entries) + "not json\n")
        return path

    def test_usage_counts_each_message_once_at_its_final_count(self) -> None:
        usage = {"input_tokens": 10, "output_tokens": 5,
                 "cache_read_input_tokens": 100, "cache_creation_input_tokens": 20}
        streaming = {**usage, "output_tokens": 1}
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(
                tmp,
                {"type": "assistant", "message": {"id": "m1", "usage": streaming, "content": []}},
                {"type": "assistant", "message": {"id": "m1", "usage": usage, "content": []}},
                {"type": "assistant", "message": {"id": "m2", "usage": usage, "content": []}},
                {"type": "user", "message": {"content": "hi"}},
            )
            self.assertEqual(hooks.usage(path), {"tokens": 270, "output_tokens": 10,
                                                 "cache_read_tokens": 200, "peak_context": 130})

    def test_report_handed_back_through_a_tool_is_found(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, {"type": "assistant", "message": {"id": "m1", "content": [
                {"type": "tool_use", "name": "SubagentHandback", "input": {"message": REPORT}}]}})
            payload = {"last_assistant_message": "Done.", "agent_transcript_path": str(path)}
            self.assertEqual(hooks.final_text(payload), REPORT)

    def test_missing_transcript_falls_back_to_last_message(self) -> None:
        payload = {"last_assistant_message": REPORT, "agent_transcript_path": "/nope.jsonl"}
        self.assertEqual(hooks.final_text(payload), REPORT)
        self.assertEqual(hooks.usage(Path("/nope.jsonl"))["tokens"], 0)


class LedgerDiscoveryTest(unittest.TestCase):
    def test_finds_ledgers_in_subfolders_and_skips_heavy_ones(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp, sub="dogfood/todo")
            hidden = root / "node_modules" / "x" / ".orchestra"
            hidden.mkdir(parents=True)
            (hidden / "feedback.jsonl").write_text("")
            self.assertEqual(hooks.find_ledgers(root),
                             [root / "dogfood" / "todo" / ".orchestra" / "feedback.jsonl"])

    def test_registry_keeps_every_ledger_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "data" / "ledgers.json"
            hooks.register(registry, [Path("/a/.orchestra/feedback.jsonl")])
            hooks.register(registry, [Path("/a/.orchestra/feedback.jsonl"),
                                      Path("/b/.orchestra/feedback.jsonl")])
            self.assertEqual(json.loads(registry.read_text())["ledgers"],
                             ["/a/.orchestra/feedback.jsonl", "/b/.orchestra/feedback.jsonl"])


class SessionStartTest(unittest.TestCase):
    def test_quiet_project_says_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp, finding("f-00000001"))
            out = hooks.session_start({"source": "startup"}, {"CLAUDE_PROJECT_DIR": str(root)})
            self.assertIsNone(out)

    def test_due_signals_reach_the_user_not_the_agent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp, finding("f-00000001", found_by="user", severity="high"))
            data = Path(tmp) / "plugin-data"
            out = hooks.session_start({"source": "startup"}, {
                "CLAUDE_PROJECT_DIR": str(root), "CLAUDE_PLUGIN_DATA": str(data)})
            self.assertIn("orchestra:coach", out["systemMessage"])
            self.assertNotIn("hookSpecificOutput", out)
            self.assertTrue((data / "ledgers.json").is_file())

    def test_project_without_ledger_says_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = hooks.session_start({"source": "startup"}, {"CLAUDE_PROJECT_DIR": tmp})
            self.assertIsNone(out)


class SubagentStopTest(unittest.TestCase):
    def payload(self, text: str, **over) -> dict:
        return {"agent_type": "orchestra:reviewer", "agent_id": "a1",
                "last_assistant_message": text, "stop_hook_active": False, **over}

    def ledger_events(self, root: Path) -> list[dict]:
        path = root / ".orchestra" / "feedback.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines()]

    def test_unrecorded_finding_blocks_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            env = {"CLAUDE_PROJECT_DIR": str(root)}
            out = hooks.subagent_stop(self.payload(verdict("revise")), env)
            self.assertEqual(out["decision"], "block")
            again = hooks.subagent_stop(self.payload(verdict("revise"), stop_hook_active=True), env)
            self.assertIsNone(again)

    def test_good_stop_records_agent_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp, finding("f-0000abcd"))
            out = hooks.subagent_stop(self.payload(verdict("revise")),
                                      {"CLAUDE_PROJECT_DIR": str(root)})
            self.assertIsNone(out)
            agent = self.ledger_events(root)[-1]
            self.assertEqual((agent["type"], agent["role"], agent["status"]),
                             ("agent", "reviewer", "verdict: revise"))

    def test_findings_in_a_worktree_outbox_reach_the_ledger_before_the_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            outbox = root / ".claude" / "worktrees" / "agent-a1" / ".orchestra" / "outbox"
            outbox.mkdir(parents=True)
            (outbox / "feedback.jsonl").write_text(json.dumps(finding("f-0000abcd")) + "\n")
            out = hooks.subagent_stop(self.payload(verdict("revise")),
                                      {"CLAUDE_PROJECT_DIR": str(root)})
            self.assertIsNone(out)
            types = [(e["type"], e.get("id")) for e in self.ledger_events(root)]
            self.assertEqual(types, [("finding", "f-0000abcd"), ("agent", None)])

    def test_outbox_is_found_from_the_transcript_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            worktree = Path(tmp) / "elsewhere"
            (worktree / ".orchestra" / "outbox").mkdir(parents=True)
            (worktree / ".orchestra" / "outbox" / "feedback.jsonl").write_text(
                json.dumps(finding("f-0000abcd")) + "\n")
            transcript = Path(tmp) / "agent-a1.jsonl"
            transcript.write_text("")
            (Path(tmp) / "agent-a1.meta.json").write_text(json.dumps({"worktreePath": str(worktree)}))
            out = hooks.subagent_stop(
                self.payload(verdict("revise"), agent_transcript_path=str(transcript)),
                {"CLAUDE_PROJECT_DIR": str(root)})
            self.assertIsNone(out)
            self.assertEqual(self.ledger_events(root)[0]["id"], "f-0000abcd")

    def test_first_stop_in_a_run_starts_the_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            (root / ".orchestra" / "2026-10-18-idea-trip").mkdir(parents=True)
            out = hooks.subagent_stop(self.payload(REPORT, agent_type="orchestra:product-manager"),
                                      {"CLAUDE_PROJECT_DIR": str(root)})
            self.assertIsNone(out)
            agent = self.ledger_events(root)[-1]
            self.assertEqual((agent["role"], agent["status"]), ("product-manager", "done"))

    def test_project_without_orchestra_folder_gets_no_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            hooks.subagent_stop(self.payload(REPORT), {"CLAUDE_PROJECT_DIR": tmp})
            self.assertFalse((Path(tmp) / ".orchestra").exists())

    def test_other_agents_are_left_alone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            out = hooks.subagent_stop(self.payload("whatever", agent_type="Explore"),
                                      {"CLAUDE_PROJECT_DIR": str(root)})
            self.assertIsNone(out)
            self.assertEqual(self.ledger_events(root), [])


class CommandLineTest(unittest.TestCase):
    def test_bad_input_never_breaks_the_session(self) -> None:
        p = subprocess.run([sys.executable, str(HOOKS / "orchestra_hooks.py"), "subagent-stop"],
                           input="not json", capture_output=True, text=True)
        self.assertEqual((p.returncode, p.stdout), (0, ""))


if __name__ == "__main__":
    unittest.main()
