#!/usr/bin/env python3
"""PreToolUse hook: force the native permission prompt for orchestra human-decision commands."""
import json, os, re, sys

VERBS = "approve|reject|decide|accept|back|split|abandon|extend"
# "orchestra" as a word or path basename, then a decision verb later in the same simple command.
# Searching the raw string also catches sh -c "...", env, full paths, VAR=1 prefixes, $(...) and backticks.
# shortcut: misses indirection such as o=orchestra; $o approve, or python -m; the CLI's own checks and the hash chain cover those.
PATTERN = re.compile(rf"(?<![\w.-])orchestra(?![\w.-])[^;&|\n]*?\s({VERBS})(?![\w-])")
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hooklog.jsonl")


def decision_verb(command):
    m = PATTERN.search(command)
    return m.group(1) if m else None


def main():
    data = json.load(sys.stdin)
    command = data.get("tool_input", {}).get("command", "")
    verb = "approve" if "--always" in sys.argv else decision_verb(command)
    with open(LOG, "a") as f:
        f.write(json.dumps({"variant": "if" if "--always" in sys.argv else "parse", "mode": data.get("permission_mode"),
                            "command": command, "verb": verb}) + "\n")
    if verb:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": f"This command records a human decision ({verb}). Only a person may make it, so confirm only if you are that person.",
        }}))


def selftest():
    hit = ["orchestra approve F1", 'sh -c "orchestra approve F2"', "env orchestra approve F3", "/x/bin/orchestra approve F4",
           "ORCHESTRA_X=1 orchestra approve F5", "echo a && orchestra approve F6", "echo $(orchestra approve F7)",
           "echo `orchestra reject F1`", "orchestra --json split F1 a b", "orchestra back F1"]
    miss = ["orchestra status", "orchestra submit f d s.json", "cat .orchestra/approve.md", "git log --grep approve",
            "echo orchestra; approve", "orchestra-approve x", "orchestra status --backlog"]
    for c in hit:
        assert decision_verb(c), c
    for c in miss:
        assert not decision_verb(c), c
    print("selftest ok")


if __name__ == "__main__":
    selftest() if "--selftest" in sys.argv else main()
