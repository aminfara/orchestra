#!/usr/bin/env python3
"""Spikes 3 and 4: agent loading, pinning and sandboxing. Throwaway; logs everything to spike34.log."""
import json, os, shutil, subprocess, time, uuid
from pathlib import Path

S = Path(__file__).resolve().parent
PLUG = S / "probe-plugin"
W = S / "work"            # stands in for a feature worktree
O = S / "outside"         # outside the work dir, still under the scratchpad
HOME_PROBE = Path.home() / ".orchestra-spike34-probe.txt"
PIN, PIN_SBX, EMPTY_MCP = S / "pin.json", S / "pin-sandbox.json", S / "empty-mcp.json"
LOG = open(S / "spike34.log", "w")
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
                    log("TOOL_USE:", json.dumps(c.get("input"))[:400], c.get("name"))
                elif c.get("type") == "text":
                    log("TEXT:", c["text"][:400])
        elif typ == "user":
            for c in ev.get("message", {}).get("content", []) if isinstance(ev.get("message", {}).get("content"), list) else []:
                if c.get("type") == "tool_result":
                    content = c.get("content")
                    log("TOOL_RESULT:", (json.dumps(content) if not isinstance(content, str) else content)[:400], "is_error=", c.get("is_error"))
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
        d.mkdir()
    subprocess.run(["git", "init", "-q", str(W)])
    log("claude version:", subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip())
    plug = ["--plugin-dir", str(PLUG), "--strict-mcp-config", "--mcp-config", str(EMPTY_MCP)]
    ask_secret = "What is the secret word from the skill preloaded into your context? Do not use any tools. If you do not know it, answer UNKNOWN."

    # ---- Spike 3 ----
    run("3a1 --agent probe-agent (bare)", plug + ["--tools", "", "--agent", "probe-agent"], "Reply with only: ok")
    run("3a2 --agent probe-plugin:probe-agent", plug + ["--tools", "", "--agent", "probe-plugin:probe-agent"], "Reply with only: ok")
    run("3a3 --agent no-such-agent", plug + ["--tools", "", "--agent", "no-such-agent"], "Reply with only: ok")
    run("3a4 --agent other-plugin:probe-agent", plug + ["--tools", "", "--agent", "other-plugin:probe-agent"], "Reply with only: ok")
    run("3c1 hidden skill via probe-agent", plug + ["--tools", "", "--agent", "probe-plugin:probe-agent"], ask_secret)
    run("3c2 hidden skill via probe-agent-ns (namespaced skill ref)", plug + ["--tools", "", "--agent", "probe-plugin:probe-agent-ns"], ask_secret)
    run("3c3 visible skill via probe-visible-agent", plug + ["--tools", "", "--agent", "probe-plugin:probe-visible-agent"], ask_secret)
    run("3c4 control agent, no skill", plug + ["--tools", "", "--agent", "probe-plugin:probe-control"], ask_secret)
    for i, ref in enumerate(["probe-skill", "probe-plugin:probe-skill"], 1):
        inline = json.dumps({"inline-probe": {"description": "Inline probe agent", "prompt": "Always begin every reply with the word KESTRELMARK, then a space, then the answer.", "skills": [ref]}})
        run(f"3d{i} --agents inline, skills=[{ref}]", plug + ["--tools", "", "--agents", inline, "--agent", "inline-probe"], ask_secret)

    # ---- Spike 4a: setting sources ----
    hello = "Reply with exactly two words: first ok, then YES if your context contains a markdown heading named 'Gates', otherwise NO."
    run("4a0 baseline: no source flags, no strict mcp", ["--plugin-dir", str(PLUG)], hello)
    a1 = run("4a1 --setting-sources ''", plug + ["--setting-sources", ""], hello)
    run("4a2 --setting-sources project,local", plug + ["--setting-sources", "project,local"], hello)
    run("4a3 --setting-sources local --settings pin.json", plug + ["--setting-sources", "local", "--settings", str(PIN)], hello)
    run("4a4 --setting-sources '' --settings pin.json", plug + ["--setting-sources", "", "--settings", str(PIN)], hello)
    run("4a5 user sources + --settings pin.json", plug + ["--settings", str(PIN)], hello)
    ok_empty = any(e.get("type") == "result" and not e.get("is_error") for e in a1)
    src = "" if ok_empty else "local"
    log(f"\nPINNED setting-sources value chosen: {src!r}")
    pinned = plug + ["--setting-sources", src, "--settings", str(PIN), "--permission-mode", "default", "--permission-prompts", "none"]

    # ---- 4b: real denial ----
    cmds = f"Run these Bash commands one at a time, each as its own Bash call, and report each outcome in one line: (1) ls {W} (2) touch {W}/denied.txt (3) date (4) echo hi > {W}/echo.txt"
    run("4b1 pinned, denial test", pinned, cmds)
    exists_report(W / "denied.txt", W / "echo.txt")
    run("4b2 user sources + pin.json + default mode, same commands", plug + ["--settings", str(PIN), "--permission-mode", "default", "--permission-prompts", "none"], cmds)
    exists_report(W / "denied.txt", W / "echo.txt")
    for f in ("denied.txt", "echo.txt"):
        (W / f).unlink(missing_ok=True)

    # ---- 4c: tool restriction ----
    run("4c1 pinned + --tools Read,Bash --allowedTools 'Bash(touch *)' --disallowedTools 'Bash(ls *)'",
        pinned + ["--tools", "Read,Bash", "--allowedTools", "Bash(touch *)", "--disallowedTools", "Bash(ls *)"],
        f"Do these one at a time and report each outcome in one line: (1) Bash: ls {W} (2) Bash: touch {W}/allowed.txt (3) use the Write tool to create {W}/w.txt containing hi")
    exists_report(W / "allowed.txt", W / "w.txt")

    # ---- 4d: sandbox ----
    sbx = plug + ["--setting-sources", src, "--settings", str(PIN_SBX), "--permission-prompts", "none"]
    run("4d1 sandbox, default mode, Bash writes",
        sbx + ["--permission-mode", "default"],
        f"Run these Bash commands one at a time, each as its own Bash call, and report each outcome verbatim in one line: (1) touch {W}/inside.txt (2) touch {O}/outside.txt (3) touch {HOME_PROBE}")
    exists_report(W / "inside.txt", O / "outside.txt", HOME_PROBE)
    run("4d2 sandbox, acceptEdits, Write tool",
        sbx + ["--permission-mode", "acceptEdits"],
        f"Use the Write tool (not Bash) twice and report each outcome in one line: (1) create {W}/w-inside.txt containing hi (2) create {O}/w-outside.txt containing hi")
    exists_report(W / "w-inside.txt", O / "w-outside.txt")

    # ---- 4e: MCP ----
    run("4e1 user sources, no strict mcp", ["--plugin-dir", str(PLUG), "--tools", ""], "Reply with only: ok")
    run("4e2 setting-sources pinned, no strict mcp", ["--plugin-dir", str(PLUG), "--tools", "", "--setting-sources", src, "--settings", str(PIN)], "Reply with only: ok")
    run("4e3 strict mcp + empty config", plug + ["--tools", ""], "Reply with only: ok")

    # ---- 4f: full template, session file, resume ----
    schema = json.dumps({"type": "object", "properties": {"status": {"type": "string"}, "word": {"type": "string"}}, "required": ["status"]})
    tmpl = pinned + ["--agent", "probe-plugin:probe-agent", "--json-schema", schema, "--autocompact", "150000"]
    sid = str(uuid.uuid4())
    run("4f1 full template, new session", tmpl, "Remember the word PELICAN. Submit status=ready.", session_id=sid, stream=False)
    files = list((Path.home() / ".claude" / "projects").glob(f"*/{sid}.jsonl"))
    log("SESSION FILE for", sid, ":", [str(f) for f in files])
    run("4f2 full template, resume", tmpl, "Submit status=done and word=<the word I asked you to remember>.", resume=sid, stream=False)

    # ---- cleanup and session listing ----
    log("\n===== session files =====")
    for s in dict.fromkeys(SESSIONS):
        log(s, [str(f) for f in (Path.home() / ".claude" / "projects").glob(f"*/{s}.jsonl")])
    shutil.rmtree(W, ignore_errors=True)
    shutil.rmtree(O, ignore_errors=True)
    HOME_PROBE.unlink(missing_ok=True)
    log("CLEANUP done: work, outside, home probe removed")
    log("SPIKE34 DONE")


if __name__ == "__main__":
    main()
