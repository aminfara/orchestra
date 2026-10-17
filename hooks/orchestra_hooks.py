#!/usr/bin/env python3
"""
Orchestra's hooks: the deterministic edge of the improvement loop.

    session-start   On a new session, find the project's feedback ledgers,
                    add them to the plugin's registry of ledgers (so the coach
                    can read across projects), and, when the ledger's signals
                    say a retro is worth running, tell the user in one line.
                    It tells the user, never the agent, so no session carries
                    the improvement loop in its context.

    subagent-stop   When an Orchestra role stops, check that it ended with a
                    report or a verdict, and that every ledger ID a verdict
                    cites was recorded. If not, send it back once with the
                    reason. Then record the stop, with its status and the
                    tokens it used, as an agent event in the ledger.

Both read the hook's JSON payload on stdin and print JSON only when they have
something to say. A hook must never break a session, so any failure exits 0
silently and is logged to the plugin data folder when there is one.

Standard library only.
"""

from __future__ import annotations

import json
import os
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PLUGIN_ROOT / "skills" / "feedback" / "scripts"))

import feedback  # noqa: E402

SKIP_DIRS = {".git", "node_modules", "target", "dist", "build", ".venv", "venv",
             "__pycache__", ".next", ".cache", "vendor"}
MAX_DEPTH = 3
STATUS = re.compile(r"^\W*(status|verdict)\W*:\**\s*(.+)$", re.IGNORECASE | re.MULTILINE)
LEDGER_ID = re.compile(r"\bf-[0-9a-f]{8}\b")
STATUSES = ("done with concerns", "done", "blocked", "needs a decision")


# ---------------------------------------------------------------------------
# Reading a role's final report
# ---------------------------------------------------------------------------


def status_of(text: str) -> str:
    m = STATUS.search(text or "")
    if not m:
        return "unknown"
    kind, value = m.group(1).lower(), m.group(2).strip().strip("*").strip().lower()
    first = value.split()[0].strip(".,;:!") if value else "unknown"
    if kind == "verdict":
        return "verdict: " + next((v for v in ("revise", "pass") if value.startswith(v)), first)
    return next((s for s in STATUSES if value.startswith(s)), first)


def check(text: str, known: set[str]) -> str | None:
    """Return why the role should not stop yet, or None."""
    if not text.strip():
        return None
    m = STATUS.search(text)
    if not m:
        return ("End with your report (or, if you were checking, your verdict) in the shape "
                "your brief gives, starting with its Status or Verdict line, and write it to "
                "the report path in your brief.")
    cited = set(LEDGER_ID.findall(text))
    if missing := sorted(cited - known):
        return (f"Your verdict cites ledger IDs that are not in the feedback ledger: "
                f"{', '.join(missing)}. Record each finding with orchestra:feedback and cite "
                f"the IDs the script printed.")
    if status_of(text) == "verdict: revise" and not cited:
        return ("A revise verdict needs its findings in the ledger. Record each one with "
                "orchestra:feedback and list the IDs in your verdict.")
    return None


def transcript_entries(path: Path) -> list[dict]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    entries = []
    for line in lines:
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def final_text(payload: dict) -> str:
    """The role's report: its last message, or what it handed back through a tool."""
    text = payload.get("last_assistant_message") or ""
    if STATUS.search(text):
        return text
    path = payload.get("agent_transcript_path")
    if path:
        for entry in reversed(transcript_entries(Path(path))):
            content = (entry.get("message") or {}).get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if (isinstance(block, dict) and block.get("type") == "tool_use"
                        and block.get("name") == "SubagentHandback"):
                    return (block.get("input") or {}).get("message") or text
    return text


def usage(path: Path) -> tuple[int, int]:
    """Total and output tokens in a transcript, counting each message once."""
    seen, total, output = set(), 0, 0
    for entry in transcript_entries(path):
        message = entry.get("message") or {}
        u = message.get("usage")
        if entry.get("type") != "assistant" or not isinstance(u, dict):
            continue
        if message.get("id") in seen:
            continue
        seen.add(message.get("id"))
        total += sum(u.get(k) or 0 for k in ("input_tokens", "output_tokens",
                                             "cache_read_input_tokens",
                                             "cache_creation_input_tokens"))
        output += u.get("output_tokens") or 0
    return total, output


# ---------------------------------------------------------------------------
# Finding ledgers
# ---------------------------------------------------------------------------


def find_ledgers(root: Path, max_depth: int = MAX_DEPTH) -> list[Path]:
    found = []
    for folder, dirs, _ in os.walk(root):
        depth = len(Path(folder).relative_to(root).parts)
        ledger = Path(folder) / ".orchestra" / "feedback.jsonl"
        if ledger.is_file():
            found.append(ledger)
        dirs[:] = [] if depth >= max_depth else [
            d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
    return sorted(found)


def register(registry: Path, ledgers: list[Path]) -> None:
    known = set(feedback.read_registry(registry)) if registry.is_file() else set()
    merged = sorted({str(p) for p in known} | {str(p) for p in ledgers})
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(json.dumps({"ledgers": merged}, indent=2) + "\n")


def choose_ledger(text: str, ledgers: list[Path]) -> Path | None:
    """The ledger of the run the report belongs to, when that is unambiguous."""
    if len(ledgers) == 1:
        return ledgers[0]
    matches = [p for p in ledgers
               if any(d.is_dir() and d.name in text for d in p.parent.iterdir())]
    return matches[0] if len(matches) == 1 else None


def known_ids(ledgers: list[Path]) -> set[str]:
    return {e["id"] for p in ledgers for e in feedback.read_ledger(p) if e["type"] == "finding"}


def project_root(payload: dict, env: dict) -> Path:
    return Path(env.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd())


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------


def session_start(payload: dict, env: dict) -> dict | None:
    root = project_root(payload, env)
    ledgers = find_ledgers(root)
    if env.get("CLAUDE_PLUGIN_DATA") and ledgers:
        register(Path(env["CLAUDE_PLUGIN_DATA"]) / "ledgers.json", ledgers)
    if not ledgers:
        return None
    signals = feedback.compute_signals(feedback.view(ledgers), feedback.load_config(ledgers))
    if not signals:
        return None
    urgent = [s for s in signals if s["level"] == "act"]
    lead = (urgent or signals)[0]["detail"]
    more = f" (and {len(signals) - 1} more)" if len(signals) > 1 else ""
    return {"systemMessage": (
        f"Orchestra's improvement loop has {len(signals)} signal(s) for {root.name}, "
        f"{len(urgent)} needing action: {lead}{more}. When you have a moment, start "
        f"orchestra:coach in a separate session.")}


def subagent_stop(payload: dict, env: dict) -> dict | None:
    agent_type = payload.get("agent_type") or ""
    if not agent_type.startswith("orchestra:"):
        return None
    text = final_text(payload)
    ledgers = find_ledgers(project_root(payload, env))
    if not payload.get("stop_hook_active"):
        reason = check(text, known_ids(ledgers))
        if reason:
            return {"decision": "block", "reason": reason}
    ledger = choose_ledger(text, ledgers)
    if ledger:
        path = payload.get("agent_transcript_path")
        total, output = usage(Path(path)) if path else (0, 0)
        feedback.append_event(ledger, {
            "type": "agent", "ts": feedback.now(),
            "role": agent_type.removeprefix("orchestra:"),
            "agent_id": payload.get("agent_id"), "status": status_of(text),
            "tokens": total or None, "output_tokens": output or None,
        })
    return None


HANDLERS = {"session-start": session_start, "subagent-stop": subagent_stop}


def main(argv: list[str]) -> int:
    env = dict(os.environ)
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        result = HANDLERS[argv[0]](payload, env)
        if result:
            print(json.dumps(result))
    except Exception:  # a hook must never break the session
        data = env.get("CLAUDE_PLUGIN_DATA")
        if data:
            try:
                log = Path(data) / "hook-errors.log"
                log.parent.mkdir(parents=True, exist_ok=True)
                with log.open("a") as f:
                    f.write(f"{datetime.now(timezone.utc).isoformat()} {argv}\n{traceback.format_exc()}\n")
            except OSError:
                pass
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
