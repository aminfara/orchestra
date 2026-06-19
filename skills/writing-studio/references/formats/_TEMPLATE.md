# Format: <NAME>

<!--
Scaffold for adding a new format. Copy this file to <name>.md, fill every section,
then add a line to the "Currently supported" list in SKILL.md.
Keep it concrete. A thin format file is worse than none, because it implies coverage that isn't there.

TWO SHAPES — pick one:
1. Single file (default): <name>.md with everything below. Use when the format is
   written at one depth (e.g. blog post, release notes).
2. Base + completeness levels: a folder <name>/ with a base <name>.md (what it is,
   when to use, default axes, a SECTION LIBRARY defining each section once, and the
   rules) PLUS thin level files (<name>-floater.md, <name>-onepager.md,
   <name>-full.md, or whatever levels fit). Use when the same artifact is legitimately
   written at different maturities/depths and you want low-completeness work to load
   cheaply. See references/formats/proposal/ for a worked example.
   In the base+levels shape: the base owns section MEANING; each level file says which
   sections to include and at what DEPTH, and links back to the base. SKILL.md loads
   the base + exactly one level file. Completeness levels are optional; not every
   format needs them.
-->

One or two sentences: what is this format, and what job does it do for the reader?

## When to use vs. adjacent formats

How a writer (or the agent) tells this format apart from similar ones. Name the nearest neighbors and the distinguishing question. If the format has variants/flavors, list them and give the one disambiguating question to pick between them.

## Default axes

- **Purpose:** <primary purpose(s)>
- **Tone:** <default tone, and when it shifts>
- **Medium:** <typical medium; what to do if delivered elsewhere>
- **Audience:** <who reads it; what they know; how much attention>

## Template

```text
<the section-by-section skeleton the agent should start from,
with a one-line note in each section saying what goes there>
```

## Rules for this format

- **Enforce:** <which always-on (A*) and conditional (B*) rules to apply strictly, and why>
- **Relax:** <which conditional rules to relax for this format, and why>
- **Watch:** <the failure modes specific to this format — the things that make it bad>
- **Length:** <typical length and the hard cap, if any>

## Quick checklist before presenting

1. <format-specific gate>
2. <...>
3. Did you run the ai-patterns pass?
