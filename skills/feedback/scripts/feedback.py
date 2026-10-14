#!/usr/bin/env python3
"""
feedback: append findings to Orchestra's feedback ledger and summarize it.

The ledger is a JSON Lines file, append-only. Each line is one event:

    finding  a checker or the user found a problem in an artifact
    outcome  a finding was fixed, deferred or overridden
    cost     rework rounds and tokens spent on one phase by one role
    retro    the coach finished a retro; later counts start from here

Usage:
    feedback.py record  --ledger PATH --run RUN --flow FLOW --phase N
                        --artifact PATH --role ROLE --skill SKILL
                        --model MODEL --effort EFFORT --found-by WHO
                        --category CATEGORY --severity SEVERITY
                        --finding TEXT --why TEXT
    feedback.py resolve --ledger PATH --id ID --outcome OUTCOME [--note TEXT]
    feedback.py cost    --ledger PATH --run RUN --phase N --role ROLE
                        [--rounds N] [--tokens N]
    feedback.py count   --ledger PATH
    feedback.py summary --ledger PATH [--all]
    feedback.py retro   --ledger PATH [--note TEXT]

Every command prints one JSON object on stdout. Errors print a JSON object
with an "error" name on stderr and exit with status 1.

Standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

CATEGORIES = (
    "gap",           # something the artifact needed is missing
    "error",         # something stated is wrong
    "unsupported",   # a claim without a source or evidence
    "inconsistent",  # contradicts itself or another artifact
    "unclear",       # a reader who was not there cannot follow it
    "scope",         # goes beyond the brief, or falls short of it
    "infeasible",    # cannot be built as described
    "other",
)
SEVERITIES = ("high", "medium", "low")
OUTCOMES = ("fixed", "deferred", "overridden")

PLUGIN_ROOT = Path(__file__).resolve().parents[3]


class LedgerError(Exception):
    name = "LedgerError"


class InvalidValue(LedgerError):
    name = "InvalidValue"


class UnknownSkill(LedgerError):
    name = "UnknownSkill"


class UnknownFinding(LedgerError):
    name = "UnknownFinding"


@dataclass(frozen=True)
class SkillVersion:
    name: str
    version: str  # first 10 hex chars of the SKILL.md sha256, or "none"
    lines: int


def skill_version(name: str, root: Path = PLUGIN_ROOT) -> SkillVersion:
    name = name.removeprefix("orchestra:")
    if name == "none":
        return SkillVersion("none", "none", 0)
    path = root / "skills" / name / "SKILL.md"
    if not path.is_file():
        raise UnknownSkill(f"no SKILL.md for skill '{name}' under {root / 'skills'}")
    data = path.read_bytes()
    return SkillVersion(name, hashlib.sha256(data).hexdigest()[:10], data.count(b"\n"))


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_events(ledger: Path) -> list[dict]:
    if not ledger.exists():
        return []
    with ledger.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def append_event(ledger: Path, event: dict) -> None:
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def choice(value: str, allowed: tuple[str, ...], field: str) -> str:
    if value not in allowed:
        raise InvalidValue(f"{field} '{value}' is not one of: {', '.join(allowed)}")
    return value


def since_last_retro(events: list[dict]) -> tuple[list[dict], str | None]:
    """Return the events after the last retro marker, and that marker's time."""
    last = None
    for i, e in enumerate(events):
        if e["type"] == "retro":
            last = i
    if last is None:
        return events, None
    return events[last + 1:], events[last]["ts"]


def findings_with_outcomes(events: list[dict]) -> list[dict]:
    """Fold outcome events into their findings; unresolved findings are 'open'."""
    outcomes = {e["finding"]: e["outcome"] for e in events if e["type"] == "outcome"}
    return [
        {**e, "outcome": outcomes.get(e["id"], "open")}
        for e in events
        if e["type"] == "finding"
    ]


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_record(args: argparse.Namespace) -> dict:
    skill = skill_version(args.skill)
    event = {
        "type": "finding",
        "id": "f-" + uuid.uuid4().hex[:8],
        "ts": now(),
        "run": args.run,
        "flow": args.flow,
        "phase": args.phase,
        "artifact": args.artifact,
        "role": args.role,
        "skill": skill.name,
        "skill_version": skill.version,
        "skill_lines": skill.lines,
        "model": args.model,
        "effort": args.effort,
        "found_by": args.found_by,
        "category": choice(args.category, CATEGORIES, "category"),
        "severity": choice(args.severity, SEVERITIES, "severity"),
        "finding": args.finding,
        "why": args.why,
    }
    append_event(args.ledger, event)
    return {"id": event["id"]}


def cmd_resolve(args: argparse.Namespace) -> dict:
    outcome = choice(args.outcome, OUTCOMES, "outcome")
    known = {e["id"] for e in read_events(args.ledger) if e["type"] == "finding"}
    if args.id not in known:
        raise UnknownFinding(f"no finding with id '{args.id}' in {args.ledger}")
    append_event(args.ledger, {
        "type": "outcome", "ts": now(), "finding": args.id,
        "outcome": outcome, "note": args.note,
    })
    return {"id": args.id, "outcome": outcome}


def cmd_cost(args: argparse.Namespace) -> dict:
    append_event(args.ledger, {
        "type": "cost", "ts": now(), "run": args.run, "phase": args.phase,
        "role": args.role, "rounds": args.rounds, "tokens": args.tokens,
    })
    return {"recorded": True}


def cmd_count(args: argparse.Namespace) -> dict:
    events = read_events(args.ledger)
    recent, last_retro = since_last_retro(events)
    findings = findings_with_outcomes(events)
    recent_ids = {e["id"] for e in recent if e["type"] == "finding"}
    return {
        "findings": len(findings),
        "open": sum(1 for f in findings if f["outcome"] == "open"),
        "since_retro": len(recent_ids),
        "last_retro": last_retro,
    }


def cmd_summary(args: argparse.Namespace) -> dict:
    events = read_events(args.ledger)
    window, last_retro = (events, None) if args.all else since_last_retro(events)
    window_ids = {e["id"] for e in window if e["type"] == "finding"}
    findings = [f for f in findings_with_outcomes(events) if f["id"] in window_ids]

    def tally(key) -> dict:
        return dict(Counter(key(f) for f in findings).most_common())

    costs = [e for e in window if e["type"] == "cost"]
    return {
        "window": "all" if args.all else "since_retro",
        "last_retro": last_retro,
        "findings": len(findings),
        "runs": sorted({f["run"] for f in findings}),
        "by_role": tally(lambda f: f["role"]),
        "by_skill": tally(lambda f: f"{f['skill']}@{f['skill_version']} ({f['skill_lines']} lines)"),
        "by_category": tally(lambda f: f["category"]),
        "by_severity": tally(lambda f: f["severity"]),
        "by_found_by": tally(lambda f: f["found_by"]),
        "by_outcome": tally(lambda f: f["outcome"]),
        "by_model": tally(lambda f: f"{f['model']}/{f['effort']}"),
        "found_by_user": [
            {k: f[k] for k in ("id", "run", "phase", "role", "category", "finding")}
            for f in findings if f["found_by"] == "user"
        ],
        "rework_rounds": sum(c["rounds"] or 0 for c in costs),
        "tokens": sum(c["tokens"] or 0 for c in costs),
    }


def cmd_retro(args: argparse.Namespace) -> dict:
    append_event(args.ledger, {"type": "retro", "ts": now(), "note": args.note})
    return {"recorded": True}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Orchestra feedback ledger")
    sub = p.add_subparsers(dest="command", required=True)

    def command(name: str, fn) -> argparse.ArgumentParser:
        sp = sub.add_parser(name)
        sp.add_argument("--ledger", type=Path, required=True)
        sp.set_defaults(fn=fn)
        return sp

    r = command("record", cmd_record)
    for flag in ("run", "flow", "artifact", "role", "skill", "model", "effort",
                 "found-by", "category", "severity", "finding", "why"):
        r.add_argument(f"--{flag}", required=True)
    r.add_argument("--phase", type=int, required=True)

    s = command("resolve", cmd_resolve)
    s.add_argument("--id", required=True)
    s.add_argument("--outcome", required=True)
    s.add_argument("--note")

    c = command("cost", cmd_cost)
    c.add_argument("--run", required=True)
    c.add_argument("--phase", type=int, required=True)
    c.add_argument("--role", required=True)
    c.add_argument("--rounds", type=int)
    c.add_argument("--tokens", type=int)

    command("count", cmd_count)

    m = command("summary", cmd_summary)
    m.add_argument("--all", action="store_true", help="include findings before the last retro")

    t = command("retro", cmd_retro)
    t.add_argument("--note")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = args.fn(args)
    except LedgerError as e:
        print(json.dumps({"error": e.name, "message": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
