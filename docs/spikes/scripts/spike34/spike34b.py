#!/usr/bin/env python3
"""Spikes 3 and 4: agent loading, pinning and sandboxing. Throwaway; logs everything to spike34.log."""
import json, os, shutil, subprocess, time, uuid
from pathlib import Path

S = Path(__file__).resolve().parent
PLUG = S / "probe-plugin"
BASE = Path.home() / ".orchestra-spike34"  # outside /tmp/claude-501, which run 1 showed is auto-writable
W = BASE / "work"
TMPPROBE = S / "tmpprobe.txt"
O = BASE / "outside"
HOME_PROBE = Path.home() / ".orchestra-spike34-probe.txt"
PIN, PIN_SBX, EMPTY_MCP = S / "pin.json", S / "pin-sandbox.json", S / "empty-mcp.json"
LOG = open(S / "spike34b.log", "w")
SESSIONS = []


def log(*a):
    print(*a, file=LOG, flush=True)
    print(*a, flush=True)


def run(label, args, prompt, session_id=None, resume=None, stream=True):
    sid = session_id or (None if resume else str(uuid.uuid4()))
    cmd = ["claude", "-p", "--model", "haiku"]
    cmd += ["--output-format", "stream-json", "--verbose", "--include-hook-events"] if stream else ["--output-format", "json"]
    cmd += ["--resume", resume] if resume else ["--session-id", sid]
    cmd += args  # prompt goes on stdin: variadic flags (--tools, --disallowedTools) would swallow a trailing prompt
    SESSIONS.append(resume or sid)
    log(f"\n===== {label} =====\nCMD: {json.dumps(cmd)}\nSTDIN PROMPT: {prompt}")
    t = time.time()
    try:
        p = subprocess.run(cmd, cwd=W, input=prompt, capture_output=True, text=True, timeout=180)
        rc, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        rc, out, err = "TIMEOUT", (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""), ""
    log(f"EXIT: {rc}  WALL: {time.time() - t:.1f}s")
    if err.strip():
        log("STDERR:", err.strip()[:3000])
    events = []
    for line in out.splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            log("NONJSON:", line[:500])
    for ev in events:
        typ, sub = ev.get("type"), ev.get("subtype")
        if typ == "system" and sub == "init":
            summary = {k: ev.get(k) for k in ("permissionMode", "tools", "mcp_servers", "plugins", "skills", "agents", "slash_commands", "model", "cwd")}
            log("INIT:", json.dumps(summary))
        elif typ == "system" and sub and "hook" in sub:
            log("HOOK:", json.dumps({k: ev.get(k) for k in ("subtype", "hook_name", "hook_event", "output", "stdout", "exit_code", "outcome")})[:600])
        elif typ == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    log("TOOL_USE:", json.dumps(c.get("input"))[:1500], c.get("name"))
                elif c.get("type") == "text":
                    log("TEXT:", c["text"][:1500])
        elif typ == "user":
            for c in ev.get("message", {}).get("content", []) if isinstance(ev.get("message", {}).get("content"), list) else []:
                if c.get("type") == "tool_result":
                    content = c.get("content")
                    log("TOOL_RESULT:", (json.dumps(content) if not isinstance(content, str) else content)[:1500], "is_error=", c.get("is_error"))
        elif typ == "result" or not stream:
            log("RESULT:", json.dumps(ev))
    log("GREP PONYTAIL:", "PONYTAIL" in out, " PROBEHOOKFIRED:", "PROBEHOOKFIRED" in out)
    return events


def exists_report(*paths):
    for p in paths:
        log(f"FILE {p}: {'EXISTS' if Path(p).exists() else 'absent'}")


def main():
    for d in (W, O):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(W)])
    plug = ["--plugin-dir", str(PLUG), "--strict-mcp-config", "--mcp-config", str(EMPTY_MCP)]
    pinned = plug + ["--setting-sources", "", "--settings", str(PIN), "--permission-mode", "default", "--permission-prompts", "none"]
    ask_secret = "What is the secret word from the skill preloaded into your context? Do not use any tools. If you do not know it, answer UNKNOWN."

    # 3c again, with default tools and pinned sources
    run("R3c1 hidden skill, --agent probe-agent, default tools", pinned + ["--agent", "probe-plugin:probe-agent"], ask_secret)
    run("R3c2 visible skill, --agent probe-visible-agent, default tools", pinned + ["--agent", "probe-plugin:probe-visible-agent"], ask_secret)
    run("R3c3 probe-agent as a subagent via Agent tool", pinned + ["--agent", "probe-plugin:probe-control", "--allowedTools", "Agent,Task"],
        "Use the Agent tool with subagent_type probe-plugin:probe-agent and this prompt: 'What is the secret word from the skill preloaded into your context? Do not use any tools. Answer UNKNOWN if you do not know.' Then report the subagent's reply verbatim.")
    run("R3c4 control agent invokes hidden skill via Skill tool", pinned + ["--agent", "probe-plugin:probe-control", "--allowedTools", "Skill"],
        "Use the Skill tool to invoke the skill probe-plugin:probe-skill, then report the secret word it gives.")

    # 4b again, outside the per-user temp dir
    cmds = f"Run these Bash commands one at a time, each as its own Bash call, and report each outcome in one line: (1) ls {W} (2) touch {W}/denied.txt (3) date (4) echo hi > {W}/echo.txt (5) touch {TMPPROBE}"
    run("R4b1 pinned denial test, work dir under home", pinned, cmds)
    exists_report(W / "denied.txt", W / "echo.txt", TMPPROBE)
    for f in (W / "denied.txt", W / "echo.txt", TMPPROBE):
        f.unlink(missing_ok=True)

    run("R4c1 --tools Read,Bash --allowedTools Bash(touch *) --disallowedTools Bash(ls *)",
        pinned + ["--tools", "Read,Bash", "--allowedTools", "Bash(touch *)", "--disallowedTools", "Bash(ls *)"],
        f"Do these one at a time and report each outcome in one line: (1) Bash: ls {W} (2) Bash: touch {W}/allowed.txt (3) use the Write tool to create {W}/w.txt containing hi")
    exists_report(W / "allowed.txt", W / "w.txt")

    # 4d sandbox
    for label, settings, mode in [("R4d1 sandbox+autoAllow, default mode", PIN_SBX, "default"),
                                  ("R4d2 sandbox+autoAllow, acceptEdits", PIN_SBX, "acceptEdits"),
                                  ("R4d3 sandbox+autoAllow+allow Bash(touch *), default mode", S / "pin-sandbox-touch.json", "default")]:
        tag = label.split()[0]
        run(label, plug + ["--setting-sources", "", "--settings", str(settings), "--permission-mode", mode, "--permission-prompts", "none"],
            f"Run these Bash commands one at a time, each as its own Bash call, and report each outcome verbatim in one line: (1) touch {W}/{tag}-in.txt (2) touch {O}/{tag}-out.txt (3) touch {HOME_PROBE}")
        exists_report(W / f"{tag}-in.txt", O / f"{tag}-out.txt", HOME_PROBE)
    run("R4d4 sandbox, acceptEdits, Write tool", plug + ["--setting-sources", "", "--settings", str(PIN_SBX), "--permission-mode", "acceptEdits", "--permission-prompts", "none"],
        f"Use the Write tool (not Bash) twice and report each outcome in one line: (1) create {W}/w-inside.txt containing hi (2) create {O}/w-outside.txt containing hi")
    exists_report(W / "w-inside.txt", O / "w-outside.txt")

    log("\n===== session files =====")
    for s in dict.fromkeys(SESSIONS):
        log(s, [str(f) for f in (Path.home() / ".claude" / "projects").glob(f"*/{s}.jsonl")])
    shutil.rmtree(BASE, ignore_errors=True)
    HOME_PROBE.unlink(missing_ok=True)
    TMPPROBE.unlink(missing_ok=True)
    log("CLEANUP done")
    log("SPIKE34B DONE")


if __name__ == "__main__":
    main()
