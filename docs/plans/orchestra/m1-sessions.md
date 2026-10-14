# M1 sessions

Part of the [Orchestra plan](README.md). How M1 runs across two interactive sessions, and the prompt to start each one.

## Order

Start the overseer session first. The dogfood session has nothing to run until the overseer has packaged the plugin and built the M1 skeleton (the conductor, the product manager and architect roles, and their skills), so the overseer says when the dogfood session can start.

The single-agent baseline, which M1's done criteria compare against, runs later in a third plain session without Orchestra. The overseer prepares its prompt and the blind comparison once the dogfood run reaches an approved architecture.

## How the sessions share work

The dogfood session runs in a terminal as `claude --plugin-dir <main checkout> -w dogfood`, because managed settings block local marketplaces (see spike 5), so it runs whatever is on `main`. The overseer develops in its own worktree and merges to `main` (fast-forward or squash, never `--no-ff`) when a change is ready. The dogfood session picks the change up at its next session start or `/reload-plugins`. Merging is how a skill change lands between phases rather than during one.

The dogfood session writes the todo app, its living docs and its `.orchestra/` folder under `dogfood/todo/` in its own worktree, and tells you that path at each phase boundary. The overseer reads the run log, the feedback ledger and the reports from there. Like the coach, it does not read the dogfood run's artifacts in detail unless a finding calls for it.

## Overseer session prompt

```text
You are the overseer for Orchestra's M1. Read docs/plans/orchestra/README.md first, then the design notes only as you need them. Work in this order:

1. Packaging. Add .claude-plugin/plugin.json and a local marketplace manifest so this repo installs as the `orchestra` plugin from its main checkout. Give me the exact steps to register and install it in the desktop app, then check how edits are picked up there (new session or /reload-plugins) and record the result in the M1 spikes section of the README.
2. Spike 2. With a throwaway skill marked `context: fork`, test whether a forked skill can ask me questions through AskUserQuestion. Record the result in the README's M1 spikes section and in conductor.md, then delete the test skill.
3. M1 skeleton. Build the conductor skill with its references and the new-product flow (phases 1 to 6), the product-manager and architect agents, and the briefing, research, ux-design, architecture and feedback skills, including the feedback ledger script. Follow the plan's tenets: short skills built on concepts and quality bars, no rule lists. Lint every SKILL.md with skill-linter. Merge to main when the skeleton is ready, and tell me the dogfood session can start.
4. Oversight. While the dogfood run goes, read its run log, feedback ledger and reports (the dogfood session will tell me their path), act as the coach, and bring me proposed skill changes with their evidence. Land approved changes by merging to main between phases.

Ask me decisions in batches with the question tool, each question self-contained with a recommendation. This repo is public: no employer names or internal content in files or commit messages.
```

## Dogfood session prompt

```text
Use orchestra:conductor to run the new-product flow. The product is a collaborative todo web app, and its project root is dogfood/todo/ in this repo. Use Orchestra's skills and agents as they are; do not edit anything under skills/, agents/ or .claude-plugin/. At each phase boundary, tell me the full path of the run log and the feedback ledger so the overseer session can read them. Stop when phase 6 (architecture and UX) is approved.
```
