#!/usr/bin/env python3
"""
feedback: Orchestra's feedback ledger, and the signals that start the coach.

The ledger is a JSON Lines file per project, append-only. Each line is one event:

    finding    a checker, acceptance or the user found a problem in an artifact
    outcome    a finding was fixed, deferred or overridden
    cost       rework rounds (and tokens, if known) for one phase by one role
    agent      a role instance stopped: its status and the tokens it used
    run        a run closed, with its outcome
    proposal   the coach proposed a change to how the team works
    decision   the user accepted or rejected a proposal, or a landed change
               was later kept or reverted
    retro      the coach finished a retro; later windows start from here

Usage:
    feedback.py record    --ledger PATH --run RUN --flow FLOW --phase N
                          --artifact PATH --role ROLE --skill SKILL
                          --model MODEL --effort EFFORT --found-by WHO
                          --category CATEGORY --severity SEVERITY
                          --finding TEXT --why TEXT
    feedback.py resolve   --ledger PATH --id ID --outcome OUTCOME [--note TEXT]
    feedback.py cost      --ledger PATH --run RUN --phase N --role ROLE
                          [--rounds N] [--tokens N]
    feedback.py agent     --ledger PATH --role ROLE --agent-id ID --status S
                          [--tokens N] [--output-tokens N]
    feedback.py close-run --ledger PATH --run RUN --flow FLOW --outcome TEXT
    feedback.py count     --ledger PATH...
    feedback.py summary   --ledger PATH... [--all]
    feedback.py signals   --ledger PATH...
    feedback.py propose   --ledger PATH... --kind KIND --target TARGET
                          --summary TEXT [--evidence ID]... [--role ROLE]
    feedback.py decide    --ledger PATH... --id ID --decision DECISION [--note TEXT]
    feedback.py proposals --ledger PATH... [--status STATUS]
    feedback.py retro     --ledger PATH... [--note TEXT]

Commands marked PATH... accept --ledger more than once, to read or write
several projects' ledgers together; --registry FILE adds every ledger listed
in a JSON registry, such as the one Orchestra's SessionStart hook keeps.

Every command prints one JSON object on stdout. Errors print a JSON object
with an "error" name on stderr and exit with status 1.

Standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tomllib
import uuid
from collections import Counter, defaultdict
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
PROPOSAL_KINDS = (
    "concept",   # a clarified principle, quality bar or example in a skill
    "tool",      # a linter rule, test, script or hook
    "project",   # a note in one project's CLAUDE.md, glossary or ADRs
    "trial",     # lighter review or a cheaper model for one role, reversible
    "removal",   # delete a guideline that evals show is no longer needed
    "restore",   # undo a trial or a change that did not help
)
DECISIONS = ("accepted", "rejected", "kept", "reverted")
ESCAPED_BY = ("user", "acceptance")  # found after every check had passed

DEFAULTS = {
    "retro_findings": 20,   # findings since the last retro
    "retro_runs": 3,        # runs closed since the last retro
    "recurring": 3,         # findings with one skill and category, across 2+ runs
    "evaluate_runs": 3,     # runs closed since a change landed
    "clean_phases": 5,      # phases since a role's last medium or high finding
    "rework_phases": 2,     # phases that needed two rounds of revision
    "skill_growth": 0.25,   # growth in a skill's length across the ledger
}

PLUGIN_ROOT = Path(__file__).resolve().parents[3]


class LedgerError(Exception):
    name = "LedgerError"


class InvalidValue(LedgerError):
    name = "InvalidValue"


class UnknownSkill(LedgerError):
    name = "UnknownSkill"


class UnknownFinding(LedgerError):
    name = "UnknownFinding"


class UnknownProposal(LedgerError):
    name = "UnknownProposal"


@dataclass(frozen=True)
class SkillVersion:
    name: str
    version: str  # first 10 hex chars of the SKILL.md sha256, or "none"
    lines: int


def skill_version(name: str, root: Path = PLUGIN_ROOT) -> SkillVersion:
    name = name.removeprefix("orchestra:").removeprefix("skills/")
    if name == "none":
        return SkillVersion("none", "none", 0)
    path = root / "skills" / name / "SKILL.md"
    if not path.is_file():
        raise UnknownSkill(f"no SKILL.md for skill '{name}' under {root / 'skills'}")
    data = path.read_bytes()
    return SkillVersion(name, hashlib.sha256(data).hexdigest()[:10], data.count(b"\n"))


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def choice(value: str, allowed: tuple[str, ...], field: str) -> str:
    if value not in allowed:
        raise InvalidValue(f"{field} '{value}' is not one of: {', '.join(allowed)}")
    return value


# ---------------------------------------------------------------------------
# Reading and writing ledgers
# ---------------------------------------------------------------------------


def read_ledger(ledger: Path) -> list[dict]:
    if not ledger.exists():
        return []
    with ledger.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def append_event(ledger: Path, event: dict) -> None:
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def since_last_retro(events: list[dict]) -> tuple[list[dict], str | None]:
    """Return the events after the last retro marker, and that marker's time."""
    last = None
    for i, e in enumerate(events):
        if e["type"] == "retro":
            last = i
    if last is None:
        return events, None
    return events[last + 1:], events[last]["ts"]


def merge(streams: list[list[dict]]) -> list[dict]:
    """Merge events from several ledgers in time order, dropping duplicates."""
    seen, merged = set(), []
    for stream in streams:
        for pos, e in enumerate(stream):
            key = json.dumps(e, sort_keys=True)
            if key not in seen:
                seen.add(key)
                merged.append((e["ts"], pos, e))
    return [e for _, _, e in sorted(merged, key=lambda x: (x[0], x[1]))]


@dataclass(frozen=True)
class View:
    """Every event across the ledgers, and the ones since each ledger's last retro."""
    events: list[dict]
    recent: list[dict]
    last_retro: str | None


def view(ledgers: list[Path]) -> View:
    per_ledger = [read_ledger(p) for p in ledgers]
    windows = [since_last_retro(evs) for evs in per_ledger]
    retros = [ts for _, ts in windows if ts]
    return View(merge(per_ledger), merge([w for w, _ in windows]), max(retros, default=None))


def findings_with_outcomes(events: list[dict]) -> list[dict]:
    """Fold outcome events into their findings; unresolved findings are 'open'."""
    outcomes = {e["finding"]: e["outcome"] for e in events if e["type"] == "outcome"}
    return [
        {**e, "outcome": outcomes.get(e["id"], "open")}
        for e in events
        if e["type"] == "finding"
    ]


def proposals_with_decisions(events: list[dict]) -> list[dict]:
    decisions = defaultdict(list)
    for e in events:
        if e["type"] == "decision":
            decisions[e["proposal"]].append(e)
    folded = []
    for e in events:
        if e["type"] != "proposal":
            continue
        history = decisions.get(e["id"], [])
        accepted = next((d for d in history if d["decision"] == "accepted"), None)
        folded.append({
            **{k: v for k, v in e.items() if k != "type"},
            "status": history[-1]["decision"] if history else "proposed",
            "note": history[-1].get("note") if history else None,
            "accepted_at": accepted["ts"] if accepted else None,
            "skill_version": accepted.get("skill_version") if accepted else None,
        })
    return folded


def load_config(ledgers: list[Path]) -> dict:
    config = dict(DEFAULTS)
    if ledgers:
        path = ledgers[0].parent / "config.toml"
        if path.is_file():
            try:
                config.update(tomllib.loads(path.read_text()).get("coach", {}))
            except tomllib.TOMLDecodeError as e:
                raise InvalidValue(f"{path}: {e}") from e
    return config


# ---------------------------------------------------------------------------
# Signals: deterministic triggers for the improvement loop
# ---------------------------------------------------------------------------


def signal(name: str, level: str, detail: str, evidence: list[str] | None = None,
           **extra) -> dict:
    return {"signal": name, "level": level, "detail": detail,
            "evidence": evidence or [], **extra}


def compute_signals(v: View, config: dict) -> list[dict]:
    """Return the reasons, if any, to run the coach now.

    'act' signals point at something that went wrong after the checks had
    passed, or at a trial that is hurting; 'consider' signals point at
    patterns worth a retro.
    """
    out: list[dict] = []
    recent_findings = [e for e in v.recent if e["type"] == "finding"]
    recent_runs = [e for e in v.recent if e["type"] == "run"]

    if len(recent_findings) >= config["retro_findings"] or len(recent_runs) >= config["retro_runs"]:
        out.append(signal("retro-due", "consider",
                          f"{len(recent_findings)} findings and {len(recent_runs)} closed runs since the last retro"))

    groups = defaultdict(list)
    for f in recent_findings:
        groups[(f["skill"], f["category"])].append(f)
    for (skill, category), fs in sorted(groups.items()):
        if len(fs) >= config["recurring"] and len({f["run"] for f in fs}) >= 2:
            out.append(signal("recurring", "consider",
                              f"{len(fs)} '{category}' findings against {skill} across {len({f['run'] for f in fs})} runs",
                              [f["id"] for f in fs]))

    for f in recent_findings:
        if f["found_by"] in ESCAPED_BY and f["severity"] in ("high", "medium"):
            out.append(signal("escape", "act" if f["severity"] == "high" else "consider",
                              f"{f['severity']} '{f['category']}' finding on {f['role']}'s work got past its checks ({f['found_by']})",
                              [f["id"]]))

    reworked = [c for c in v.recent if c["type"] == "cost" and (c.get("rounds") or 0) >= 2]
    if len(reworked) >= config["rework_phases"]:
        out.append(signal("rework", "consider",
                          f"{len(reworked)} phases needed two rounds of revision; the first checks may be missing things"))

    events = v.events
    index = {id(e): i for i, e in enumerate(events)}
    for p in proposals_with_decisions(events):
        if not p["accepted_at"] or p["status"] in ("kept", "reverted"):
            continue
        after = [e for e in events if e["ts"] > p["accepted_at"]]
        if p["kind"] == "trial":
            escapes = [e for e in after if e["type"] == "finding" and e["role"] == p.get("role")
                       and e["found_by"] in ESCAPED_BY and e["severity"] in ("high", "medium")]
            if escapes:
                out.append(signal("trial-regressed", "act",
                                  f"trial '{p['summary']}' for {p['role']} let {len(escapes)} finding(s) escape; restore it",
                                  [e["id"] for e in escapes], proposal=p["id"]))
                continue
        runs_after = [e for e in after if e["type"] == "run"]
        if len(runs_after) >= config["evaluate_runs"]:
            out.append(signal("evaluate-change", "consider",
                              f"'{p['summary']}' landed {len(runs_after)} runs ago; compare findings before and after",
                              proposal=p["id"]))

    on_trial = {p.get("role") for p in proposals_with_decisions(events)
                if p["kind"] == "trial" and p["status"] == "accepted"}
    last_serious = {}
    for e in events:
        if e["type"] == "finding" and e["severity"] in ("high", "medium"):
            last_serious[e["role"]] = index[id(e)]
    phases = Counter()
    for e in events:
        if e["type"] == "cost" and index[id(e)] > last_serious.get(e["role"], -1):
            phases[e["role"]] += 1
    for role, n in sorted(phases.items()):
        if n >= config["clean_phases"] and role not in on_trial:
            out.append(signal("clean-streak", "consider",
                              f"{role} has finished {n} phases without a medium or high finding; consider lighter review or a cheaper model"))

    first, last = {}, {}
    for e in events:
        if e["type"] == "finding" and e["skill"] != "none":
            first.setdefault(e["skill"], e["skill_lines"])
            last[e["skill"]] = e["skill_lines"]
    for skill in sorted(last):
        if first[skill] and (last[skill] - first[skill]) / first[skill] > config["skill_growth"]:
            out.append(signal("skill-growth", "consider",
                              f"{skill} grew from {first[skill]} to {last[skill]} lines; look for what can be shortened or removed"))
    return out


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def single(args: argparse.Namespace) -> Path:
    if len(args.ledgers) != 1:
        raise InvalidValue(f"'{args.command}' writes to exactly one ledger")
    return args.ledgers[0]


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
    append_event(single(args), event)
    return {"id": event["id"]}


def cmd_resolve(args: argparse.Namespace) -> dict:
    ledger = single(args)
    outcome = choice(args.outcome, OUTCOMES, "outcome")
    known = {e["id"] for e in read_ledger(ledger) if e["type"] == "finding"}
    if args.id not in known:
        raise UnknownFinding(f"no finding with id '{args.id}' in {ledger}")
    append_event(ledger, {
        "type": "outcome", "ts": now(), "finding": args.id,
        "outcome": outcome, "note": args.note,
    })
    return {"id": args.id, "outcome": outcome}


def cmd_cost(args: argparse.Namespace) -> dict:
    append_event(single(args), {
        "type": "cost", "ts": now(), "run": args.run, "phase": args.phase,
        "role": args.role, "rounds": args.rounds, "tokens": args.tokens,
    })
    return {"recorded": True}


def cmd_agent(args: argparse.Namespace) -> dict:
    append_event(single(args), {
        "type": "agent", "ts": now(), "role": args.role, "agent_id": args.agent_id,
        "status": args.status, "tokens": args.tokens, "output_tokens": args.output_tokens,
    })
    return {"recorded": True}


def count(v: View) -> dict:
    findings = findings_with_outcomes(v.events)
    return {
        "findings": len(findings),
        "open": sum(1 for f in findings if f["outcome"] == "open"),
        "since_retro": sum(1 for e in v.recent if e["type"] == "finding"),
        "last_retro": v.last_retro,
    }


def cmd_count(args: argparse.Namespace) -> dict:
    return count(view(args.ledgers))


def cmd_close_run(args: argparse.Namespace) -> dict:
    append_event(single(args), {
        "type": "run", "ts": now(), "run": args.run, "flow": args.flow, "outcome": args.outcome,
    })
    v = view(args.ledgers)
    signals = compute_signals(v, load_config(args.ledgers))
    return {"recorded": True, "count": count(v), "signals": signals, "due": bool(signals)}


def cmd_summary(args: argparse.Namespace) -> dict:
    v = view(args.ledgers)
    window = v.events if args.all else v.recent
    window_ids = {e["id"] for e in window if e["type"] == "finding"}
    findings = [f for f in findings_with_outcomes(v.events) if f["id"] in window_ids]

    def tally(key) -> dict:
        return dict(Counter(key(f) for f in findings).most_common())

    costs = [e for e in window if e["type"] == "cost"]
    agents: dict[str, dict] = {}
    for e in window:
        if e["type"] == "agent":
            a = agents.setdefault(e["role"], {"stops": 0, "tokens": 0, "statuses": Counter()})
            a["stops"] += 1
            a["tokens"] += e.get("tokens") or 0
            a["statuses"][e["status"]] += 1
    return {
        "window": "all" if args.all else "since_retro",
        "last_retro": v.last_retro,
        "findings": len(findings),
        "runs": sorted({f["run"] for f in findings}),
        "runs_closed": sum(1 for e in window if e["type"] == "run"),
        "by_role": tally(lambda f: f["role"]),
        "by_skill": tally(lambda f: f"{f['skill']}@{f['skill_version']} ({f['skill_lines']} lines)"),
        "by_category": tally(lambda f: f["category"]),
        "by_severity": tally(lambda f: f["severity"]),
        "by_found_by": tally(lambda f: f["found_by"]),
        "by_outcome": tally(lambda f: f["outcome"]),
        "by_model": tally(lambda f: f"{f['model']}/{f['effort']}"),
        "found_by_user": [
            {k: f[k] for k in ("id", "run", "phase", "role", "category", "finding")}
            for f in findings if f["found_by"] in ESCAPED_BY
        ],
        "rework_rounds": sum(c["rounds"] or 0 for c in costs),
        "tokens": sum(c["tokens"] or 0 for c in costs)
                  + sum(a["tokens"] for a in agents.values()),
        "agents": {r: {**a, "statuses": dict(a["statuses"])} for r, a in agents.items()},
    }


def cmd_signals(args: argparse.Namespace) -> dict:
    signals = compute_signals(view(args.ledgers), load_config(args.ledgers))
    return {"signals": signals, "due": bool(signals)}


def cmd_propose(args: argparse.Namespace) -> dict:
    kind = choice(args.kind, PROPOSAL_KINDS, "kind")
    if kind in ("trial", "restore") and not args.role:
        raise InvalidValue(f"a {kind} proposal needs --role, the role whose review or model it changes")
    event = {
        "type": "proposal", "id": "p-" + uuid.uuid4().hex[:8], "ts": now(),
        "kind": kind, "target": args.target, "summary": args.summary,
        "evidence": args.evidence or [], "role": args.role,
    }
    for ledger in args.ledgers:
        append_event(ledger, event)
    return {"id": event["id"]}


def cmd_decide(args: argparse.Namespace) -> dict:
    decision = choice(args.decision, DECISIONS, "decision")
    v = view(args.ledgers)
    proposal = next((e for e in v.events if e["type"] == "proposal" and e["id"] == args.id), None)
    if proposal is None:
        raise UnknownProposal(f"no proposal with id '{args.id}'")
    event = {"type": "decision", "ts": now(), "proposal": args.id,
             "decision": decision, "note": args.note}
    if decision == "accepted" and proposal["target"].startswith("skills/"):
        try:
            event["skill_version"] = skill_version(proposal["target"]).version
        except UnknownSkill:
            event["skill_version"] = None
    for ledger in args.ledgers:
        append_event(ledger, event)
    return {"id": args.id, "decision": decision}


def cmd_proposals(args: argparse.Namespace) -> dict:
    found = proposals_with_decisions(view(args.ledgers).events)
    if args.status:
        found = [p for p in found if p["status"] == args.status]
    return {"proposals": found}


def cmd_retro(args: argparse.Namespace) -> dict:
    event = {"type": "retro", "ts": now(), "note": args.note}
    for ledger in args.ledgers:
        append_event(ledger, event)
    return {"recorded": True}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def read_registry(path: Path) -> list[Path]:
    if not path.is_file():
        return []
    return [Path(p) for p in json.loads(path.read_text()).get("ledgers", [])]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Orchestra feedback ledger")
    sub = p.add_subparsers(dest="command", required=True)

    def command(name: str, fn) -> argparse.ArgumentParser:
        sp = sub.add_parser(name)
        sp.add_argument("--ledger", dest="ledgers", type=Path, action="append", default=[])
        sp.add_argument("--registry", type=Path)
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

    a = command("agent", cmd_agent)
    a.add_argument("--role", required=True)
    a.add_argument("--agent-id", required=True)
    a.add_argument("--status", required=True)
    a.add_argument("--tokens", type=int)
    a.add_argument("--output-tokens", type=int)

    cr = command("close-run", cmd_close_run)
    cr.add_argument("--run", required=True)
    cr.add_argument("--flow", required=True)
    cr.add_argument("--outcome", required=True)

    command("count", cmd_count)

    m = command("summary", cmd_summary)
    m.add_argument("--all", action="store_true", help="include findings before the last retro")

    command("signals", cmd_signals)

    pr = command("propose", cmd_propose)
    pr.add_argument("--kind", required=True)
    pr.add_argument("--target", required=True)
    pr.add_argument("--summary", required=True)
    pr.add_argument("--evidence", action="append")
    pr.add_argument("--role")

    d = command("decide", cmd_decide)
    d.add_argument("--id", required=True)
    d.add_argument("--decision", required=True)
    d.add_argument("--note")

    ps = command("proposals", cmd_proposals)
    ps.add_argument("--status", choices=("proposed", *DECISIONS))

    t = command("retro", cmd_retro)
    t.add_argument("--note")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.registry:
            args.ledgers = [*args.ledgers, *read_registry(args.registry)]
        if not args.ledgers:
            raise InvalidValue("give at least one --ledger, or a --registry that lists some")
        result = args.fn(args)
    except LedgerError as e:
        print(json.dumps({"error": e.name, "message": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
