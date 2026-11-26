# orchestra

A Claude Code marketplace, `orchestra`, with one plugin, `orchestra`, that holds three skills.

| Skill | Use it for |
| --- | --- |
| `orchestra:programming` | Design principles to read before writing, changing or fixing code |
| `orchestra:writing-studio` | Drafting documents and messages for other people to read |
| `orchestra:skill-linter` | Checking a skill's `SKILL.md` against the house structure |

## Install

```bash
claude plugin marketplace add /path/to/orchestra
claude plugin install orchestra@orchestra
```

Where managed settings block local marketplaces, load it for one CLI session instead:

```bash
claude --plugin-dir /path/to/orchestra
```

## Develop

```bash
python3 skills/skill-linter/tests/test_lint.py
```

```bash
python3 skills/skill-linter/scripts/lint.py skills/<name>
```
