"""
Tests for the feedback ledger script.

Run with:
    python3 skills/feedback/tests/test_feedback.py
"""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import feedback  # noqa: E402


def run(*argv: str) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = feedback.main(list(argv))
    text = out.getvalue() if code == 0 else err.getvalue()
    return code, json.loads(text)


class LedgerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger = str(Path(self.tmp.name) / ".orchestra" / "feedback.jsonl")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def record(self, **overrides: str) -> tuple[int, dict]:
        fields = {
            "run": "2026-10-14-new-product-todo", "flow": "new-product", "phase": "4",
            "artifact": "docs/product/prfaq.md", "role": "product-manager",
            "skill": "research", "model": "opus", "effort": "high",
            "found-by": "architect", "category": "unsupported", "severity": "medium",
            "finding": "Market size claim has no source.",
            "why": "The research lens treated a vendor blog as a primary source.",
        }
        fields.update(overrides)
        argv = ["record", "--ledger", self.ledger]
        for k, v in fields.items():
            argv += [f"--{k}", v]
        return run(*argv)

    def test_record_creates_ledger_and_versions_skill(self) -> None:
        code, out = self.record()
        self.assertEqual(code, 0)
        event = json.loads(Path(self.ledger).read_text().splitlines()[0])
        self.assertEqual(event["id"], out["id"])
        self.assertEqual(event["skill"], "research")
        self.assertEqual(len(event["skill_version"]), 10)
        self.assertGreater(event["skill_lines"], 0)

    def test_record_rejects_unknown_category(self) -> None:
        code, err = self.record(category="typo")
        self.assertEqual(code, 1)
        self.assertEqual(err["error"], "InvalidValue")

    def test_record_rejects_unknown_skill(self) -> None:
        code, err = self.record(skill="no-such-skill")
        self.assertEqual(code, 1)
        self.assertEqual(err["error"], "UnknownSkill")

    def test_plugin_prefix_is_stripped(self) -> None:
        code, _ = self.record(skill="orchestra:research")
        self.assertEqual(code, 0)
        event = json.loads(Path(self.ledger).read_text().splitlines()[0])
        self.assertEqual(event["skill"], "research")

    def test_skill_none_is_allowed(self) -> None:
        code, _ = self.record(skill="none")
        self.assertEqual(code, 0)

    def test_resolve_unknown_finding(self) -> None:
        code, err = run("resolve", "--ledger", self.ledger, "--id", "f-missing", "--outcome", "fixed")
        self.assertEqual(code, 1)
        self.assertEqual(err["error"], "UnknownFinding")

    def test_count_and_summary_respect_retro(self) -> None:
        _, first = self.record()
        run("resolve", "--ledger", self.ledger, "--id", first["id"], "--outcome", "fixed")
        run("retro", "--ledger", self.ledger, "--note", "first retro")
        self.record(**{"found-by": "user", "category": "gap"})
        run("cost", "--ledger", self.ledger, "--run", "r", "--phase", "4",
            "--role", "product-manager", "--rounds", "2", "--tokens", "1000")

        _, count = run("count", "--ledger", self.ledger)
        self.assertEqual(count["findings"], 2)
        self.assertEqual(count["open"], 1)
        self.assertEqual(count["since_retro"], 1)
        self.assertIsNotNone(count["last_retro"])

        _, recent = run("summary", "--ledger", self.ledger)
        self.assertEqual(recent["findings"], 1)
        self.assertEqual(recent["by_category"], {"gap": 1})
        self.assertEqual(len(recent["found_by_user"]), 1)
        self.assertEqual(recent["rework_rounds"], 2)

        _, everything = run("summary", "--ledger", self.ledger, "--all")
        self.assertEqual(everything["findings"], 2)
        self.assertEqual(everything["by_outcome"], {"open": 1, "fixed": 1})

    def test_count_on_missing_ledger(self) -> None:
        code, count = run("count", "--ledger", self.ledger)
        self.assertEqual(code, 0)
        self.assertEqual(count["findings"], 0)


class SignalsTest(unittest.TestCase):
    """Deterministic triggers for the improvement loop."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name) / ".orchestra"
        self.ledger = str(self.dir / "feedback.jsonl")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def record(self, ledger: str | None = None, **overrides: str) -> str:
        fields = {
            "run": "run-1", "flow": "build", "phase": "2", "artifact": "src/app.py",
            "role": "engineer", "skill": "tdd-programming", "model": "sonnet",
            "effort": "medium", "found-by": "reviewer", "category": "gap",
            "severity": "medium", "finding": "Missing test for empty list.",
            "why": "Edge cases were left to the reviewer.",
        }
        fields.update(overrides)
        argv = ["record", "--ledger", ledger or self.ledger]
        for k, v in fields.items():
            argv += [f"--{k}", v]
        code, out = run(*argv)
        self.assertEqual(code, 0, out)
        return out["id"]

    def signals(self, *ledgers: str) -> dict:
        argv = ["signals"]
        for ledger in ledgers or (self.ledger,):
            argv += ["--ledger", ledger]
        code, out = run(*argv)
        self.assertEqual(code, 0, out)
        return out

    def names(self, out: dict) -> list[str]:
        return sorted(s["signal"] for s in out["signals"])

    def close_run(self, run_id: str) -> dict:
        code, out = run("close-run", "--ledger", self.ledger, "--run", run_id,
                        "--flow", "build", "--outcome", "complete")
        self.assertEqual(code, 0, out)
        return out

    def propose(self, **overrides: str) -> str:
        fields = {"kind": "concept", "target": "skills/tdd-programming",
                  "summary": "Name edge cases while settling behaviour."}
        fields.update(overrides)
        argv = ["propose", "--ledger", self.ledger]
        for k, v in fields.items():
            argv += [f"--{k}", v]
        code, out = run(*argv)
        self.assertEqual(code, 0, out)
        return out["id"]

    def decide(self, pid: str, decision: str) -> None:
        code, out = run("decide", "--ledger", self.ledger, "--id", pid, "--decision", decision)
        self.assertEqual(code, 0, out)

    def test_quiet_ledger_has_no_signals(self) -> None:
        self.record()
        out = self.signals()
        self.assertEqual((out["signals"], out["due"]), ([], False))

    def test_recurring_needs_several_runs(self) -> None:
        for _ in range(3):
            self.record(run="run-1")
        self.assertNotIn("recurring", self.names(self.signals()))
        self.record(run="run-2")
        out = self.signals()
        rec = next(s for s in out["signals"] if s["signal"] == "recurring")
        self.assertEqual(len(rec["evidence"]), 4)
        self.assertIn("tdd-programming", rec["detail"])

    def test_high_escape_must_be_acted_on(self) -> None:
        self.record(**{"found-by": "user", "severity": "high"})
        out = self.signals()
        self.assertEqual(self.names(out), ["escape"])
        self.assertEqual(out["signals"][0]["level"], "act")
        self.assertTrue(out["due"])

    def test_retro_due_after_runs_close(self) -> None:
        for i in range(2):
            self.close_run(f"run-{i}")
        self.assertNotIn("retro-due", self.names(self.signals()))
        out = self.close_run("run-3")
        self.assertIn("retro-due", [s["signal"] for s in out["signals"]])
        run("retro", "--ledger", self.ledger)
        self.assertNotIn("retro-due", self.names(self.signals()))

    def test_thresholds_come_from_project_config(self) -> None:
        self.dir.mkdir(parents=True)
        (self.dir / "config.toml").write_text("[coach]\nretro_runs = 1\n")
        out = self.close_run("run-1")
        self.assertIn("retro-due", [s["signal"] for s in out["signals"]])

    def test_trial_regresses_on_escape_after_acceptance(self) -> None:
        self.record(**{"found-by": "user", "severity": "high"})
        run("retro", "--ledger", self.ledger)
        pid = self.propose(kind="trial", target="config:review.engineer=sample", role="engineer")
        self.decide(pid, "accepted")
        self.assertNotIn("trial-regressed", self.names(self.signals()))
        self.record(**{"found-by": "acceptance", "severity": "high"})
        out = self.signals()
        reg = next(s for s in out["signals"] if s["signal"] == "trial-regressed")
        self.assertEqual((reg["level"], reg["proposal"]), ("act", pid))
        self.decide(pid, "reverted")
        self.assertNotIn("trial-regressed", self.names(self.signals()))

    def test_landed_change_is_evaluated_after_enough_runs(self) -> None:
        pid = self.propose()
        self.decide(pid, "accepted")
        for i in range(3):
            self.close_run(f"run-{i}")
        self.assertIn("evaluate-change", self.names(self.signals()))
        self.decide(pid, "kept")
        self.assertNotIn("evaluate-change", self.names(self.signals()))

    def test_clean_streak_suggests_savings(self) -> None:
        self.record(role="architect", skill="architecture", severity="medium")
        for phase in range(5):
            run("cost", "--ledger", self.ledger, "--run", "r", "--phase", str(phase),
                "--role", "architect", "--rounds", "0")
        self.record(role="architect", skill="architecture", severity="low")
        streak = next(s for s in self.signals()["signals"] if s["signal"] == "clean-streak")
        self.assertIn("architect", streak["detail"])

    def test_repeated_rework_is_flagged(self) -> None:
        for phase in ("2", "3"):
            run("cost", "--ledger", self.ledger, "--run", "r", "--phase", phase,
                "--role", "product-manager", "--rounds", "2")
        self.assertIn("rework", self.names(self.signals()))

    def test_skill_growth_is_visible(self) -> None:
        self.dir.mkdir(parents=True)
        with open(self.ledger, "a") as f:
            for version, lines in (("aaaa", 80), ("bbbb", 110)):
                f.write(json.dumps({
                    "type": "finding", "id": f"f-{version}", "ts": "2026-10-18T00:00:00+00:00",
                    "run": "r", "flow": "build", "phase": 1, "artifact": "x", "role": "engineer",
                    "skill": "review", "skill_version": version, "skill_lines": lines,
                    "model": "opus", "effort": "high", "found_by": "reviewer", "category": "gap",
                    "severity": "low", "finding": "x", "why": "y"}) + "\n")
        growth = next(s for s in self.signals()["signals"] if s["signal"] == "skill-growth")
        self.assertIn("review", growth["detail"])

    def test_signals_span_ledgers(self) -> None:
        other = str(Path(self.tmp.name) / "other" / ".orchestra" / "feedback.jsonl")
        self.record(run="run-1")
        self.record(run="run-1")
        self.record(ledger=other, run="run-9")
        self.assertIn("recurring", self.names(self.signals(self.ledger, other)))


class ProposalsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger = str(Path(self.tmp.name) / ".orchestra" / "feedback.jsonl")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_proposal_lifecycle(self) -> None:
        code, p = run("propose", "--ledger", self.ledger, "--kind", "concept",
                      "--target", "skills/review", "--summary", "Lens choice follows risk.",
                      "--evidence", "f-1", "--evidence", "f-2")
        self.assertEqual(code, 0)
        _, listed = run("proposals", "--ledger", self.ledger)
        self.assertEqual([(x["id"], x["status"]) for x in listed["proposals"]], [(p["id"], "proposed")])
        run("decide", "--ledger", self.ledger, "--id", p["id"], "--decision", "rejected",
            "--note", "Too narrow.")
        _, rejected = run("proposals", "--ledger", self.ledger, "--status", "rejected")
        self.assertEqual(rejected["proposals"][0]["evidence"], ["f-1", "f-2"])
        self.assertEqual(rejected["proposals"][0]["note"], "Too narrow.")

    def test_accepting_a_skill_change_records_its_new_version(self) -> None:
        _, p = run("propose", "--ledger", self.ledger, "--kind", "concept",
                   "--target", "skills/feedback", "--summary", "x")
        run("decide", "--ledger", self.ledger, "--id", p["id"], "--decision", "accepted")
        _, listed = run("proposals", "--ledger", self.ledger)
        self.assertEqual(len(listed["proposals"][0]["skill_version"]), 10)

    def test_errors_are_specific(self) -> None:
        code, err = run("decide", "--ledger", self.ledger, "--id", "p-none", "--decision", "accepted")
        self.assertEqual((code, err["error"]), (1, "UnknownProposal"))
        code, err = run("propose", "--ledger", self.ledger, "--kind", "rule",
                        "--target", "x", "--summary", "y")
        self.assertEqual((code, err["error"]), (1, "InvalidValue"))
        code, err = run("propose", "--ledger", self.ledger, "--kind", "trial",
                        "--target", "config:models.engineer=haiku", "--summary", "y")
        self.assertEqual((code, err["error"]), (1, "InvalidValue"))

    def test_proposal_written_to_several_ledgers_is_listed_once(self) -> None:
        other = str(Path(self.tmp.name) / "b" / ".orchestra" / "feedback.jsonl")
        run("propose", "--ledger", self.ledger, "--ledger", other, "--kind", "tool",
            "--target", "hooks", "--summary", "x")
        _, listed = run("proposals", "--ledger", self.ledger, "--ledger", other)
        self.assertEqual(len(listed["proposals"]), 1)
        self.assertTrue(Path(other).exists())


class AgentEventsTest(unittest.TestCase):
    def test_summary_tallies_agent_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = str(Path(tmp) / "feedback.jsonl")
            for status, tokens in (("done", 1000), ("blocked", 500)):
                code, _ = run("agent", "--ledger", ledger, "--role", "engineer",
                              "--agent-id", "a1", "--status", status, "--tokens", str(tokens))
                self.assertEqual(code, 0)
            _, out = run("summary", "--ledger", ledger)
            self.assertEqual(out["agents"]["engineer"],
                             {"stops": 2, "tokens": 1500, "statuses": {"done": 1, "blocked": 1}})


if __name__ == "__main__":
    unittest.main()
