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


if __name__ == "__main__":
    unittest.main()
