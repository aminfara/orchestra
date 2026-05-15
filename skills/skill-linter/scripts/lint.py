#!/usr/bin/env python3
"""
skill-linter: Lint a SKILL.md body against the canonical v0.5 template.

Usage:
    python lint.py <skill_path> [--output <path>] [--no-handoff] [--strict]

Outputs a JSON report describing structural findings (errors, warnings, info)
and prints a hand-off message for skill-creator unless --no-handoff is given.

Operating doctrine:
- Suggestions are SYNTACTIC: they describe the shape of a fix, not its content.
- ZERO false positives: when a check is ambiguous, prefer to pass over to flag.
  Better to miss a real issue than to flag a non-issue.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    rule: str
    severity: str  # "error" | "warning" | "info"
    location: str
    suggestion: str
    found: Optional[str] = None
    expected: Optional[str] = None

    def to_dict(self) -> dict:
        d = {
            "rule": self.rule,
            "severity": self.severity,
            "location": self.location,
            "found": self.found,
            "expected": self.expected,
            "suggestion": self.suggestion,
        }
        return d


@dataclass
class Heading:
    level: int
    text: str
    line_no: int  # 1-based


@dataclass
class ParsedSkill:
    name: str
    description: str
    body: str
    body_start_line: int  # 1-based line in the file where the body begins
    headings: list[Heading] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_SECTIONS = ["## Overview", "## When to use this skill", "## Constraints", "## Workflow"]
OPTIONAL_SECTIONS = ["## Inputs", "## Output", "## Reference files"]
CANONICAL_ORDER = [
    "## Overview",
    "## When to use this skill",
    "## Constraints",
    "## Inputs",
    "## Output",
    "## Workflow",
    "## Reference files",
]
CONSTRAINTS_SOFT_WARN = 4   # > this → warning
CONSTRAINTS_HARD_ERROR = 8  # > this → error
CONSTRAINTS_POLYGLOT = 7    # >= this → polyglot signal

# v0.5 thresholds
BODY_MIN_CHARS = 50          # R026: substantive body must be >= this
LINE_BUDGET_INFO = 500       # R027: file lines > this → info
BODY_LEANNESS_WARN = 300     # R028: body lines > this → warning
REFERENCES_ALLOWED_EXTS = {".md", ".txt"}  # R025: allowed file types in references/

# Synonyms that should be flagged as non-canonical replacements.
SYNONYM_MAP = {
    "## Process": "## Workflow",
    "## Steps": "## Workflow",
    "## How it works": "## Workflow",
    "## How It Works": "## Workflow",
    "## Procedure": "## Workflow",
    "## Usage": "## Workflow",
    "## What it does": "## Overview",
    "## Summary": "## Overview",
    "## Description": "## Overview",
    "## Intro": "## Overview",
    "## Introduction": "## Overview",
    "## When to use": "## When to use this skill",
    "## When to Use": "## When to use this skill",
    "## Triggers": "## When to use this skill",
    "## Input": "## Inputs",
    "## Outputs": "## Output",
    "## Output Format": "## Output",
    # Note: "## References" is intentionally NOT in SYNONYM_MAP — it is a CANONICAL ALIAS
    # accepted as equivalent to "## Reference files" (see CANONICAL_ALIASES below).
    "## Reference Files": "## Reference files",  # different capitalization
    "## Reference": "## Reference files",
    "## Resources": "## Reference files",
    "## Bundled resources": "## Reference files",
    "## Files": "## Reference files",
}

# CANONICAL_ALIASES map heading variants that are accepted as equivalent to a canonical
# heading WITHOUT triggering a rename (R006). This is for cases where multiple spellings
# are widely used and equally clear. Currently used for "## References" ↔ "## Reference files"
# based on real-world skill audit (3/5 skills used "## References").
CANONICAL_ALIASES = {
    "## References": "## Reference files",
}


def canonicalize(label: str) -> str:
    """Normalize a heading label through CANONICAL_ALIASES."""
    return CANONICAL_ALIASES.get(label, label)

LOOP_SIGNAL_RE = re.compile(
    r"\b(repeat|loop|iterate|keep going|while|go back to step|return to step|until)\b",
    re.IGNORECASE,
)
EXIT_CONDITION_RE = re.compile(
    r"\b(until\s+(the\s+user|[a-z]+\s+(is|are|has|have|completes|finishes|stops|says|reports|confirms))"
    r"|when\s+[a-z]+|once\s+[a-z]+|if\s+[a-z].*?,\s*(stop|exit|return|break)"
    r"|stop\s+when|exit\s+when|break\s+when)",
    re.IGNORECASE,
)

POLYGLOT_OVERVIEW_RE = re.compile(
    r"\b(also|in addition|or alternatively|as well as)\b", re.IGNORECASE
)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def parse_skill_md(skill_path: Path) -> Optional[ParsedSkill]:
    """Parse SKILL.md into name, description, body. Returns None if unreadable."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None

    content = skill_md.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Frontmatter
    if not lines or lines[0].strip() != "---":
        return None
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None

    name = ""
    description = ""
    fm_lines = lines[1:end_idx]
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        if line.startswith("name:"):
            name = line[len("name:"):].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            value = line[len("description:"):].strip()
            if value in (">", "|", ">-", "|-"):
                cont: list[str] = []
                i += 1
                while i < len(fm_lines) and (fm_lines[i].startswith("  ") or fm_lines[i].startswith("\t")):
                    cont.append(fm_lines[i].strip())
                    i += 1
                description = " ".join(cont)
                continue
            else:
                description = value.strip('"').strip("'")
        i += 1

    body_start_line = end_idx + 2  # 1-based, line after closing ---
    body_lines = lines[end_idx + 1:]
    body = "\n".join(body_lines)

    if not body.strip():
        return None

    headings = parse_headings(body_lines, body_start_line)

    return ParsedSkill(
        name=name,
        description=description,
        body=body,
        body_start_line=body_start_line,
        headings=headings,
    )


def parse_headings(body_lines: list[str], body_start_line: int) -> list[Heading]:
    """Parse markdown ATX headings, skipping fenced code blocks."""
    headings: list[Heading] = []
    in_fence = False
    for offset, line in enumerate(body_lines):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            headings.append(Heading(level=level, text=text, line_no=body_start_line + offset))
    return headings


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def title_case_kebab(name: str) -> str:
    """Convert kebab-case to Title Case (e.g., skill-creator -> Skill Creator)."""
    return " ".join(part.capitalize() for part in name.split("-") if part)


def h1_matches_name(h1_text: str, kebab_name: str) -> bool:
    """
    Decide whether an H1 title is a close-enough match to the kebab skill name.

    Two-tier match (zero-false-positive doctrine: prefer to pass):

    Tier 1 — case-insensitive exact match after title-casing the kebab name.
      Fixes the acronym false positive: "Azure AI" matches "azure-ai"
      because 'ai'.lower() == 'ai'.lower() even though 'AI' != 'Ai'.

    Tier 2 — 50% word-overlap tolerance.
      If the H1 doesn't exactly match the title-cased kebab, we check whether
      at least half of the kebab's tokens appear (case-insensitively) in the H1.
      This allows deliberate human titles like "React Composition Patterns" for
      "vercel-composition-patterns" (3/4 tokens match: composition, patterns, react
      is a substitute for vercel — overlap = 2/4 = 50%) while still catching
      clearly unrelated titles like "Microsoft Foundry Skill" for "microsoft-foundry"
      (adds "Skill" as noise — but 2/2 tokens match, so this passes tier 2).

    Wait — "Microsoft Foundry Skill" for "microsoft-foundry": tokens are
    ['microsoft', 'foundry'], both appear in H1 → 2/2 = 100% overlap → passes.
    That means this is NOT flagged. Is that right? Yes — the author knows their
    skill; "Microsoft Foundry Skill" is a reasonable human title. The trailing
    "Skill" is noise but not harmful. We should not force-rename it.

    Tier 2 threshold: ≥ 50% of kebab tokens appear in H1 words (case-insensitive).
    This catches truly unrelated H1s while tolerating intentional author choices.

    Returns True if the H1 is an acceptable match (do NOT flag), False if mismatch.
    """
    # Strip trailing punctuation from H1
    h1_clean = re.sub(r"[^\w\s]+$", "", h1_text).strip()

    # Tier 1: case-insensitive exact match against mechanical title-casing
    expected = title_case_kebab(kebab_name)
    if h1_clean.lower() == expected.lower():
        return True

    # Tier 2: 50% token overlap (case-insensitive)
    kebab_tokens = {t.lower() for t in kebab_name.split("-") if t}
    h1_words = {w.lower() for w in re.findall(r"[a-zA-Z0-9]+", h1_clean)}
    if not kebab_tokens:
        return True  # degenerate case, don't flag
    overlap = kebab_tokens & h1_words
    overlap_ratio = len(overlap) / len(kebab_tokens)
    return overlap_ratio >= 0.5


def heading_label(h: Heading) -> str:
    """Return canonical heading label, e.g., '## When to use this skill'."""
    return ("#" * h.level) + " " + h.text


def get_section_body(parsed: ParsedSkill, heading: Heading) -> str:
    """Extract body lines under a heading until the next heading of equal or lower level."""
    body_lines = parsed.body.split("\n")
    start_offset = heading.line_no - parsed.body_start_line + 1
    if start_offset >= len(body_lines):
        return ""
    end_offset = len(body_lines)
    for h in parsed.headings:
        if h.line_no > heading.line_no and h.level <= heading.level:
            end_offset = h.line_no - parsed.body_start_line
            break
    return "\n".join(body_lines[start_offset:end_offset])


def strip_comments_and_code(text: str) -> str:
    """Remove HTML comments and fenced code blocks for content checks."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"~~~.*?~~~", "", text, flags=re.DOTALL)
    return text


def count_paragraphs(text: str) -> int:
    """Count non-empty paragraphs (separated by blank lines), ignoring comments/code/headings."""
    cleaned = strip_comments_and_code(text)
    paragraphs = []
    for chunk in re.split(r"\n\s*\n", cleaned):
        stripped = chunk.strip()
        if not stripped:
            continue
        # Skip if it's a heading
        if stripped.startswith("#"):
            continue
        paragraphs.append(stripped)
    return len(paragraphs)


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------


def lint(skill_path: Path, strict: bool = False) -> tuple[Optional[ParsedSkill], list[Finding]]:
    findings: list[Finding] = []
    parsed = parse_skill_md(skill_path)
    if parsed is None:
        findings.append(
            Finding(
                rule="skill-md-unreadable",
                severity="error",
                location=str(skill_path / "SKILL.md"),
                suggestion="Ensure `SKILL.md` exists, has valid YAML frontmatter, and a non-empty body.",
            )
        )
        return parsed, findings

    # R001 — missing-h1-title
    h1s = [h for h in parsed.headings if h.level == 1]
    if not h1s:
        findings.append(
            Finding(
                rule="missing-h1-title",
                severity="error",
                location="SKILL.md body",
                suggestion="Add an `# <Human-Readable Skill Title>` H1 at the very top of the SKILL.md body.",
            )
        )
    else:
        h1 = h1s[0]

        # R002 — h1-name-mismatch
        # Uses two-tier matching: case-insensitive exact (fixes acronyms like AI/Ai)
        # then 50% word-overlap tolerance (allows deliberate author title choices).
        # See h1_matches_name() for the full rationale.
        if parsed.name:
            expected_title = title_case_kebab(parsed.name)
            if not h1_matches_name(h1.text, parsed.name):
                findings.append(
                    Finding(
                        rule="h1-name-mismatch",
                        severity="error",
                        location=f"line {h1.line_no}",
                        found=h1.text,
                        expected=expected_title,
                        suggestion=(
                            "The H1 title has low word overlap with the kebab `name`. "
                            "Ensure the H1 is a human-readable form of the skill name "
                            "(at least half the name's words should appear in the H1)."
                        ),
                    )
                )

        # R003 / R004 — pitch line checks
        body_lines = parsed.body.split("\n")
        h1_offset = h1.line_no - parsed.body_start_line
        # Walk forward from line after H1 until we hit non-blank or another heading
        pitch_lines: list[str] = []
        i = h1_offset + 1
        # Skip leading blank lines
        while i < len(body_lines) and body_lines[i].strip() == "":
            i += 1
        # Collect contiguous non-blank, non-heading lines
        while i < len(body_lines):
            line = body_lines[i]
            stripped = line.strip()
            if stripped == "":
                break
            if stripped.startswith("#"):
                break
            pitch_lines.append(stripped)
            i += 1

        if not pitch_lines:
            findings.append(
                Finding(
                    rule="missing-pitch-line",
                    severity="error",
                    location=f"after H1 (line {h1.line_no})",
                    suggestion="Add a single-sentence pitch directly under the H1 title, before any other heading.",
                )
            )
        elif len(pitch_lines) > 1:
            findings.append(
                Finding(
                    rule="pitch-not-one-line",
                    severity="error",
                    location=f"after H1 (line {h1.line_no})",
                    found=" ⏎ ".join(pitch_lines),
                    suggestion="Collapse the pitch into a single line directly under the H1.",
                )
            )

    # Build map of canonical-section presence using exact match on h2 text.
    h2_headings = [h for h in parsed.headings if h.level == 2]
    # Build h2_labels canonicalized: "## References" -> "## Reference files".
    # SYNONYM_MAP entries still appear as their raw label here so R006 can flag them.
    h2_labels = [canonicalize(heading_label(h)) for h in h2_headings]

    # R006 — non-canonical-heading (synonyms used in place of canonical)
    for h in h2_headings:
        label = heading_label(h)
        if label in SYNONYM_MAP:
            findings.append(
                Finding(
                    rule="non-canonical-heading",
                    severity="error",
                    location=f"line {h.line_no}",
                    found=label,
                    expected=SYNONYM_MAP[label],
                    suggestion=f"Rename `{label}` to its canonical equivalent `{SYNONYM_MAP[label]}`.",
                )
            )

    # R017 — non-canonical-section (strict mode only): any h2 not in canonical list
    if strict:
        allowed_h2s = set(CANONICAL_ORDER)
        for h in h2_headings:
            label = heading_label(h)
            canonical = canonicalize(label)
            if canonical in allowed_h2s or label in SYNONYM_MAP:
                # Skip canonical (incl. aliases) and synonyms (already handled by R006)
                continue
            findings.append(
                Finding(
                    rule="non-canonical-section",
                    severity="error",
                    location=f"line {h.line_no}",
                    found=label,
                    expected=" | ".join(CANONICAL_ORDER),
                    suggestion=(
                        f"Heading `{label}` is not in the canonical set. Either rename it to a canonical "
                        f"heading, fold its content into the appropriate canonical section, or remove it."
                    ),
                )
            )

    # R005 — missing-section
    for required in REQUIRED_SECTIONS:
        if required not in h2_labels:
            findings.append(
                Finding(
                    rule="missing-section",
                    severity="error",
                    location="SKILL.md body",
                    found=None,
                    expected=required,
                    suggestion=f"Add the required section `{required}` in its canonical position.",
                )
            )

    # R007 — section-out-of-order
    seen_canonical = [
        (canonicalize(heading_label(h)), h.line_no)
        for h in h2_headings
        if canonicalize(heading_label(h)) in CANONICAL_ORDER
    ]
    canonical_indices = [CANONICAL_ORDER.index(label) for label, _ in seen_canonical]
    for j in range(1, len(canonical_indices)):
        if canonical_indices[j] < canonical_indices[j - 1]:
            label, line = seen_canonical[j]
            findings.append(
                Finding(
                    rule="section-out-of-order",
                    severity="error",
                    location=f"line {line}",
                    found=label,
                    expected=" → ".join(CANONICAL_ORDER),
                    suggestion=f"Move `{label}` so that the canonical section ordering is preserved.",
                )
            )

    # R008 / R009 — Overview checks
    overview_h = next((h for h in h2_headings if canonicalize(heading_label(h)) == "## Overview"), None)
    if overview_h:
        body_text = get_section_body(parsed, overview_h)
        # R009 — sub-headings inside overview
        for h in parsed.headings:
            if h.level >= 3 and overview_h.line_no < h.line_no:
                # Check if h is inside overview section (before next h2)
                next_h2_line = None
                for h2 in h2_headings:
                    if h2.line_no > overview_h.line_no:
                        next_h2_line = h2.line_no
                        break
                if next_h2_line is None or h.line_no < next_h2_line:
                    findings.append(
                        Finding(
                            rule="overview-has-subheadings",
                            severity="error",
                            location=f"line {h.line_no}",
                            found=heading_label(h),
                            suggestion="Remove all sub-headings from `## Overview`; keep it as plain paragraphs only.",
                        )
                    )
        # R008 — paragraph count
        n_paragraphs = count_paragraphs(body_text)
        if n_paragraphs < 3 or n_paragraphs > 5:
            findings.append(
                Finding(
                    rule="overview-paragraph-count",
                    severity="error",
                    location=f"## Overview (line {overview_h.line_no})",
                    found=f"{n_paragraphs} paragraphs",
                    expected="3 to 5 paragraphs",
                    suggestion="Adjust `## Overview` to contain between 3 and 5 paragraphs (3 is encouraged).",
                )
            )

    # Workflow checks
    workflow_h = next((h for h in h2_headings if canonicalize(heading_label(h)) == "## Workflow"), None)
    if workflow_h:
        # Find step headings (### Step N: ...) inside Workflow
        step_pattern = re.compile(r"^Step\s+(\d+)\s*:\s*(.*)$", re.IGNORECASE)
        next_h2_line = None
        for h2 in h2_headings:
            if h2.line_no > workflow_h.line_no:
                next_h2_line = h2.line_no
                break
        step_headings: list[tuple[Heading, int, str]] = []  # (heading, step_num, title)
        for h in parsed.headings:
            if h.level == 3 and workflow_h.line_no < h.line_no and (next_h2_line is None or h.line_no < next_h2_line):
                m = step_pattern.match(h.text.strip())
                if m:
                    step_headings.append((h, int(m.group(1)), m.group(2)))

        # R010 — workflow-missing-steps
        if not step_headings:
            findings.append(
                Finding(
                    rule="workflow-missing-steps",
                    severity="error",
                    location=f"## Workflow (line {workflow_h.line_no})",
                    suggestion="Convert the workflow body into numbered `### Step N: <Title>` sub-headings.",
                )
            )
        else:
            # R011 — workflow-step-numbering
            expected_nums = list(range(1, len(step_headings) + 1))
            actual_nums = [n for _, n, _ in step_headings]
            if actual_nums != expected_nums:
                findings.append(
                    Finding(
                        rule="workflow-step-numbering",
                        severity="error",
                        location=f"## Workflow (line {workflow_h.line_no})",
                        found=str(actual_nums),
                        expected=str(expected_nums),
                        suggestion="Renumber the `### Step N:` headings so they are sequential starting at 1.",
                    )
                )

            # R012 — empty-workflow-step
            empty_steps: list[tuple[Heading, int]] = []
            for sh, num, _title in step_headings:
                step_body = get_section_body(parsed, sh)
                cleaned = strip_comments_and_code(step_body).strip()
                if len(cleaned) < 10:
                    empty_steps.append((sh, num))

            if len(empty_steps) == 1:
                sh, num = empty_steps[0]
                findings.append(
                    Finding(
                        rule="empty-workflow-step",
                        severity="warning",
                        location=f"### Step {num} (line {sh.line_no})",
                        suggestion=f"Add instructions to `### Step {num}`, remove it, or merge it with an adjacent step.",
                    )
                )
            elif len(empty_steps) >= 2:
                locations = ", ".join(f"### Step {n} (line {sh.line_no})" for sh, n in empty_steps)
                findings.append(
                    Finding(
                        rule="empty-workflow-step",
                        severity="error",
                        location=locations,
                        suggestion="Multiple empty workflow steps detected. Either flesh out each step's instructions, remove the empty steps, or merge them into adjacent steps.",
                    )
                )

            # R013 — loop-without-exit-condition
            for sh, num, _title in step_headings:
                step_body = get_section_body(parsed, sh)
                cleaned = strip_comments_and_code(step_body)
                if LOOP_SIGNAL_RE.search(cleaned) and not EXIT_CONDITION_RE.search(cleaned):
                    findings.append(
                        Finding(
                            rule="loop-without-exit-condition",
                            severity="warning",
                            location=f"### Step {num} (line {sh.line_no})",
                            suggestion="Add a clear exit condition to the loop in this step so it cannot run forever.",
                        )
                    )

    # R018–R022 — Constraints section checks
    constraints_h = next((h for h in h2_headings if canonicalize(heading_label(h)) == "## Constraints"), None)
    constraints_count = 0
    if constraints_h:
        body_text = get_section_body(parsed, constraints_h)
        cleaned = strip_comments_and_code(body_text)

        # R021 — constraints-not-bullets: any non-blank, non-bullet, non-comment line is a violation.
        # Also flag sub-headings inside.
        non_bullet_lines: list[str] = []
        bullet_lines: list[str] = []
        for raw in cleaned.split("\n"):
            line = raw.rstrip()
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                # Heading inside constraints → flag as not-bullets violation
                non_bullet_lines.append(stripped)
                continue
            if re.match(r"^[-*+]\s+\S", stripped):
                bullet_lines.append(stripped)
                continue
            # Continuation lines that are indented under a bullet are OK; treat as part of last bullet.
            if line.startswith("  ") or line.startswith("\t"):
                continue
            non_bullet_lines.append(stripped)

        constraints_count = len(bullet_lines)

        if non_bullet_lines:
            findings.append(
                Finding(
                    rule="constraints-not-bullets",
                    severity="error",
                    location=f"## Constraints (line {constraints_h.line_no})",
                    found="; ".join(non_bullet_lines[:3]) + ("…" if len(non_bullet_lines) > 3 else ""),
                    suggestion="Reformat `## Constraints` as a bullet list. Remove paragraphs, sub-headings, and code blocks.",
                )
            )

        # R020 — constraints-empty
        if constraints_count == 0:
            findings.append(
                Finding(
                    rule="constraints-empty",
                    severity="error",
                    location=f"## Constraints (line {constraints_h.line_no})",
                    suggestion="Add at least one constraint bullet. Every skill must declare its constraints explicitly (even if minimal).",
                )
            )

        # R022 — constraints-too-many
        if constraints_count > CONSTRAINTS_HARD_ERROR:
            findings.append(
                Finding(
                    rule="constraints-too-many",
                    severity="error",
                    location=f"## Constraints (line {constraints_h.line_no})",
                    found=f"{constraints_count} constraints",
                    expected=f"at most {CONSTRAINTS_HARD_ERROR}",
                    suggestion="More than 8 constraints suggests this skill is over-constrained or polyglot. Split it into narrower skills, or merge related constraints.",
                )
            )
        elif constraints_count > CONSTRAINTS_SOFT_WARN:
            findings.append(
                Finding(
                    rule="constraints-too-many",
                    severity="warning",
                    location=f"## Constraints (line {constraints_h.line_no})",
                    found=f"{constraints_count} constraints",
                    expected=f"at most {CONSTRAINTS_SOFT_WARN} for clarity",
                    suggestion="Consider whether all constraints are essential. Merge overlapping ones, or split the skill if it is doing too much.",
                )
            )
    # Note: R018 (missing-constraints-section) is covered by R005 (missing-section)
    # because '## Constraints' is now in REQUIRED_SECTIONS.
    # R019 (constraints-out-of-order) is covered by R007 (section-out-of-order)
    # because '## Constraints' is now in CANONICAL_ORDER.

    # R014 — polyglot-skill
    polyglot_signals: list[str] = []
    # Pitch joins TWO DISTINCT WORKFLOWS with " and "
    if h1s:
        h1 = h1s[0]
        body_lines = parsed.body.split("\n")
        h1_offset = h1.line_no - parsed.body_start_line
        i = h1_offset + 1
        pitch_text = ""
        while i < len(body_lines) and body_lines[i].strip() == "":
            i += 1
        if i < len(body_lines):
            line = body_lines[i].strip()
            if line and not line.startswith("#"):
                pitch_text = line

        # Tightened heuristic (v0.2): only flag when " and " joins two clauses that
        # each have their own primary verb AND their own primary object. This avoids
        # firing on phrases like "enforces a structure and flags loops" where both
        # verbs operate on a single workflow's outputs.
        #
        # Stronger signal: " and also ", " and additionally ", " and separately ",
        # " and independently " — these explicitly mark a second distinct workflow.
        # Also: presence of multiple gerund/verb pairs each with their own subject
        # (e.g., "creates X and edits Y and improves Z" — 3+ verb-object pairs).
        lower_pitch = pitch_text.lower()
        strong_polyglot_markers = [" and also ", " and additionally ", " and separately ",
                                   " and independently ", " as well as also "]
        if any(marker in lower_pitch for marker in strong_polyglot_markers):
            polyglot_signals.append("pitch uses a strong second-workflow marker (e.g., 'and also')")
        else:
            # Count verb-object-like pairs: a verb followed by a noun phrase, separated by " and "/", "
            # Only fire if there are 3+ such pairs (a single "and" is usually fine).
            # Verb pattern: imperative or 3rd-person singular ending in -s, -es; or gerund -ing.
            verb_obj_pattern = re.compile(
                r"\b(?:[a-z]+(?:s|es|ing))\s+(?:a |an |the )?[a-z][a-z\-]+",
                re.IGNORECASE,
            )
            # Split pitch on " and " and ", " to find clauses
            clauses = re.split(r"\s+and\s+|,\s+", pitch_text)
            verb_obj_clauses = [c for c in clauses if verb_obj_pattern.search(c)]
            if len(verb_obj_clauses) >= 3:
                polyglot_signals.append(
                    f"pitch contains {len(verb_obj_clauses)} verb-object clauses (3+ suggests multiple workflows)"
                )

    # Overview multi-use-case markers
    if overview_h:
        ov_text = strip_comments_and_code(get_section_body(parsed, overview_h))
        if POLYGLOT_OVERVIEW_RE.search(ov_text):
            polyglot_signals.append("Overview uses multi-use-case markers (also/in addition/etc.)")

    # Description contains many DISTINCT WORKFLOW VERBS (v0.6 tightened heuristic).
    # The previous "raw clause count" heuristic produced too many false positives because
    # legitimate enumerations (formats, domains, products) inflate the clause count without
    # implying multiple workflows. Counting distinct verbs from a small allowlist of strong
    # workflow verbs yields a much cleaner signal: a single workflow uses 1-3 verbs; a polyglot
    # skill enumerates 4+ distinct activities.
    workflow_verbs = {
        # creation / modification
        "create", "creates", "make", "makes", "build", "builds", "generate", "generates",
        "draft", "drafts", "write", "writes", "produce", "produces", "construct", "constructs",
        "edit", "edits", "modify", "modifies", "update", "updates", "improve", "improves",
        "refactor", "refactors", "rewrite", "rewrites",
        # analysis / inspection
        "analyze", "analyzes", "lint", "lints", "validate", "validates", "review", "reviews",
        "audit", "audits", "inspect", "inspects", "check", "checks", "verify", "verifies",
        "test", "tests", "evaluate", "evaluates", "benchmark", "benchmarks", "measure", "measures",
        "summarize", "summarizes", "extract", "extracts", "parse", "parses",
        # transformation / movement
        "convert", "converts", "transform", "transforms", "translate", "translates",
        "deploy", "deploys", "package", "packages", "publish", "publishes",
        "import", "imports", "export", "exports", "sync", "syncs",
        # interaction
        "search", "searches", "query", "queries", "fetch", "fetches", "retrieve", "retrieves",
        "send", "sends", "post", "posts", "report", "reports",
        # optimization
        "optimize", "optimizes", "tune", "tunes",
    }
    desc_words = re.findall(r"\b[a-z]+\b", parsed.description.lower())
    distinct_workflow_verbs = {w for w in desc_words if w in workflow_verbs}
    # Normalize verb stems so "create" and "creates" count as one (cheap stemming via -s strip).
    normalized = set()
    for v in distinct_workflow_verbs:
        normalized.add(v[:-1] if v.endswith("s") and v[:-1] in workflow_verbs else v)
    if len(normalized) >= 4:
        polyglot_signals.append(
            f"description uses {len(normalized)} distinct workflow verbs ({', '.join(sorted(normalized))})"
        )

    # Constraint count: many constraints often indicate the skill is over-scoped.
    if constraints_count >= CONSTRAINTS_POLYGLOT:
        polyglot_signals.append(f"{constraints_count} constraints declared (>={CONSTRAINTS_POLYGLOT} suggests over-scoped or polyglot skill)")

    if polyglot_signals:
        findings.append(
            Finding(
                rule="polyglot-skill",
                severity="warning",
                location="SKILL.md",
                found="; ".join(polyglot_signals),
                suggestion="This skill appears polyglot. Consider splitting it into narrower skills, each with a single primary workflow. Skill-creator should decide how to split.",
            )
        )

    # R015 — optional-section-omitted
    for opt in OPTIONAL_SECTIONS:
        if opt not in h2_labels:
            findings.append(
                Finding(
                    rule="optional-section-omitted",
                    severity="info",
                    location="SKILL.md body",
                    expected=opt,
                    suggestion=f"Optional section `{opt}` is omitted. If the skill takes user-provided inputs / produces structured output, consider adding it; otherwise leave omitted.",
                )
            )

    # ---------------------------------------------------------------------
    # v0.5 rules (R024–R029)
    # All five obey the zero-false-positive doctrine: when ambiguous, pass.
    # ---------------------------------------------------------------------

    # R024 — name-matches-directory
    if parsed.name:
        dir_name = skill_path.name
        if dir_name and dir_name != parsed.name:
            findings.append(
                Finding(
                    rule="name-matches-directory",
                    severity="error",
                    location=str(skill_path),
                    found=f"name='{parsed.name}', directory='{dir_name}'",
                    expected=f"name == '{dir_name}'",
                    suggestion="Rename either the skill directory or the frontmatter `name` so they match exactly.",
                )
            )

    # R025 — references-only-text
    references_dir = skill_path / "references"
    if references_dir.exists() and references_dir.is_dir():
        bad_files: list[str] = []
        for child in sorted(references_dir.iterdir()):
            if not child.is_file():
                continue
            if child.name.startswith("."):
                continue  # ignore hidden files
            if child.suffix.lower() not in REFERENCES_ALLOWED_EXTS:
                bad_files.append(child.name)
        if bad_files:
            findings.append(
                Finding(
                    rule="references-only-text",
                    severity="warning",
                    location=str(references_dir),
                    found=", ".join(bad_files[:5]) + ("…" if len(bad_files) > 5 else ""),
                    expected="only .md or .txt files",
                    suggestion="Move non-text files out of `references/` (e.g., into `assets/` or `scripts/`), or convert them to `.md` / `.txt`.",
                )
            )

    # R026 — body-not-empty
    body_substantive = strip_comments_and_code(parsed.body)
    body_substantive = re.sub(r"^#{1,6}\s+.*$", "", body_substantive, flags=re.MULTILINE)
    body_substantive_chars = len(re.sub(r"\s+", "", body_substantive))
    if body_substantive_chars < BODY_MIN_CHARS:
        findings.append(
            Finding(
                rule="body-not-empty",
                severity="warning",
                location="SKILL.md body",
                found=f"{body_substantive_chars} substantive chars",
                expected=f">= {BODY_MIN_CHARS} substantive chars",
                suggestion="Add substantive content to the SKILL.md body. A near-empty skill provides no instructions for the model.",
            )
        )

    # R027 — line-budget (info)
    total_lines = len((skill_path / "SKILL.md").read_text(encoding="utf-8").splitlines())
    if total_lines > LINE_BUDGET_INFO:
        findings.append(
            Finding(
                rule="line-budget",
                severity="info",
                location="SKILL.md",
                found=f"{total_lines} lines",
                expected=f"<= {LINE_BUDGET_INFO} lines",
                suggestion="Consider moving long templates, examples, or detailed steps into `references/` files.",
            )
        )

    # R028 — body-leanness (warning)
    body_lines_count = len(parsed.body.splitlines())
    if body_lines_count > BODY_LEANNESS_WARN:
        findings.append(
            Finding(
                rule="body-leanness",
                severity="warning",
                location="SKILL.md body",
                found=f"{body_lines_count} body lines",
                expected=f"<= {BODY_LEANNESS_WARN} body lines",
                suggestion="Trim the SKILL.md body. Move long templates, checklists, or examples to `references/` and keep the body focused.",
            )
        )

    # R029 — reference-files-pointers-resolve
    # Only check if a Reference files section is present.
    ref_files_h = next((h for h in h2_headings if canonicalize(heading_label(h)) == "## Reference files"), None)
    if ref_files_h:
        ref_body = get_section_body(parsed, ref_files_h)
        ref_body_clean = strip_comments_and_code(ref_body)
        # Look for inline-code-style paths in bullets: `path/to/file.ext`
        # Zero-false-positive: only flag tokens that look unambiguously like a relative path.
        path_pattern = re.compile(r"`([a-zA-Z0-9_./\-]+\.[a-zA-Z0-9]{1,8})`")
        missing: list[str] = []
        for raw in ref_body_clean.split("\n"):
            stripped = raw.strip()
            if not stripped.startswith(("-", "*", "+")):
                continue
            for m in path_pattern.finditer(stripped):
                rel = m.group(1)
                # Skip absolute paths and URLs (zero-false-positive guard).
                if rel.startswith("/") or "://" in rel:
                    continue
                # Skip placeholders that contain the word "file" or angle-style hints.
                if rel.lower() in {"file.py", "file.md", "name.ext"}:
                    continue
                candidate = (skill_path / rel).resolve()
                if not candidate.exists():
                    missing.append(rel)
        if missing:
            findings.append(
                Finding(
                    rule="reference-files-pointers-resolve",
                    severity="warning",
                    location=f"## Reference files (line {ref_files_h.line_no})",
                    found=", ".join(sorted(set(missing))[:5]) + ("…" if len(set(missing)) > 5 else ""),
                    expected="all listed paths exist within the skill directory",
                    suggestion="Update each broken pointer in `## Reference files` to a real file, remove stale entries, or create the missing file.",
                )
            )

    return parsed, findings


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


HANDOFF_MESSAGE = """The skill-linter found the following structural issues in the SKILL.md you just produced.

For each `error` → fix the structural violation while preserving all existing content and intent.
For each `warning` → fix or briefly justify keeping as-is.
For each `info` → revalidate whether the omitted optional section is appropriate.

Do not change the skill's substantive behavior — only its structure and clarity. Suggestions describe the shape of the fix, not the content; you decide the content."""


def build_report(skill_path: Path, parsed: Optional[ParsedSkill], findings: list[Finding]) -> dict:
    counts = {"errors": 0, "warnings": 0, "info": 0}
    for f in findings:
        if f.severity == "error":
            counts["errors"] += 1
        elif f.severity == "warning":
            counts["warnings"] += 1
        elif f.severity == "info":
            counts["info"] += 1
    return {
        "skill_path": str(skill_path),
        "skill_name": parsed.name if parsed else "",
        "passed": counts["errors"] == 0,
        "summary": counts,
        "findings": [f.to_dict() for f in findings],
    }


SEVERITY_EMOJI = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}
SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


def render_markdown(report: dict) -> str:
    """Render a lint report as a grouped markdown document."""
    lines: list[str] = []
    skill_name = report.get("skill_name") or "(unknown)"
    summary = report.get("summary", {})
    passed = report.get("passed", False)
    status = "✅ PASSED" if passed else "❌ FAILED"

    lines.append(f"# Skill Lint Report — `{skill_name}`")
    lines.append("")
    lines.append(f"**Status:** {status}")
    lines.append(f"**Path:** `{report.get('skill_path', '')}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Severity | Count |")
    lines.append("| --- | --- |")
    lines.append(f"| ❌ errors | {summary.get('errors', 0)} |")
    lines.append(f"| ⚠️ warnings | {summary.get('warnings', 0)} |")
    lines.append(f"| ℹ️ info | {summary.get('info', 0)} |")
    lines.append("")

    findings = report.get("findings", [])
    if not findings:
        lines.append("No findings. The skill complies with the canonical template.")
        return "\n".join(lines) + "\n"

    # Group by severity, in order
    by_sev: dict[str, list[dict]] = {"error": [], "warning": [], "info": []}
    for f in findings:
        by_sev.setdefault(f.get("severity", "info"), []).append(f)

    for sev in ("error", "warning", "info"):
        bucket = by_sev.get(sev, [])
        if not bucket:
            continue
        emoji = SEVERITY_EMOJI[sev]
        lines.append(f"## {emoji} {sev.capitalize()}s ({len(bucket)})")
        lines.append("")
        for f in bucket:
            rule = f.get("rule", "")
            location = f.get("location", "")
            found = f.get("found")
            expected = f.get("expected")
            suggestion = f.get("suggestion", "")
            lines.append(f"### `{rule}` — {location}")
            lines.append("")
            if found is not None:
                lines.append(f"- **Found:** `{found}`")
            if expected is not None:
                lines.append(f"- **Expected:** `{expected}`")
            lines.append(f"- **Suggestion:** {suggestion}")
            lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a SKILL.md against the canonical template.")
    parser.add_argument("skill_path", type=str, help="Path to the skill directory containing SKILL.md")
    parser.add_argument("--output", type=str, default=None,
                        help="Where to write the report. If omitted, output is printed to stdout only "
                             "and no file is written. Use this to avoid polluting version-controlled "
                             "skill directories you do not own.")
    parser.add_argument("--no-handoff", action="store_true", help="Do not print the skill-creator hand-off message")
    parser.add_argument("--strict", action="store_true", help="Enable strict mode: flag any h2 that is not in the canonical set")
    parser.add_argument("--format", choices=["json", "md"], default="json",
                        help="Output format: json (default) or md (grouped markdown)")
    args = parser.parse_args()

    skill_path = Path(args.skill_path).resolve()
    parsed, findings = lint(skill_path, strict=args.strict)
    report = build_report(skill_path, parsed, findings)

    if args.format == "md":
        rendered = render_markdown(report)
    else:
        rendered = json.dumps(report, indent=2)

    # Always print to stdout — skill-creator and the user can read it directly.
    print(rendered)

    # Only write a file when --output is explicitly provided.
    # Default is NO file, to avoid polluting third-party or version-controlled skill dirs.
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        file_note = f"\nReport written to: {output_path}"
    else:
        file_note = ""

    if not args.no_handoff:
        print()
        print("=" * 72)
        print(HANDOFF_MESSAGE)
        if file_note:
            print(file_note)

    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
