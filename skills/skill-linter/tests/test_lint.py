"""
Fixture-based test suite for skill-linter.

Each fixture lives under tests/fixtures/<name>/SKILL.md and asserts that the
linter produces the expected set of findings (by rule ID).

Run with:
    python tests/test_lint.py
or
    pytest tests/test_lint.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make scripts/ importable
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import lint  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures"


def rules_fired(skill_dir: Path, strict: bool = False) -> set[str]:
    """Run the linter and return the set of rule IDs that fired."""
    _, findings = lint.lint(skill_dir, strict=strict)
    return {f.rule for f in findings}


def severities(skill_dir: Path, strict: bool = False) -> dict[str, str]:
    """Map rule -> highest severity that fired (error > warning > info)."""
    _, findings = lint.lint(skill_dir, strict=strict)
    rank = {"info": 0, "warning": 1, "error": 2}
    out: dict[str, str] = {}
    for f in findings:
        if f.rule not in out or rank[f.severity] > rank[out[f.rule]]:
            out[f.rule] = f.severity
    return out


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------


def test_valid_skill_passes() -> None:
    fired = rules_fired(FIXTURES / "valid-skill")
    # No errors or warnings should fire on the canonical fixture.
    expected_clean = fired - {"optional-section-omitted"}
    assert expected_clean == set(), f"Valid skill should be clean; got: {expected_clean}"


def test_valid_skill_strict_passes() -> None:
    fired = rules_fired(FIXTURES / "valid-skill", strict=True)
    expected_clean = fired - {"optional-section-omitted"}
    assert expected_clean == set(), f"Valid skill should pass strict mode; got: {expected_clean}"


def test_missing_overview_fires_R005() -> None:
    fired = rules_fired(FIXTURES / "missing-overview")
    assert "missing-section" in fired, "R005 should fire for missing Overview"


def test_missing_constraints_fires_R005() -> None:
    fired = rules_fired(FIXTURES / "missing-constraints")
    assert "missing-section" in fired, "R005 should fire for missing Constraints"


def test_non_canonical_heading_fires_R006() -> None:
    fired = rules_fired(FIXTURES / "non-canonical-heading")
    assert "non-canonical-heading" in fired, "R006 should fire for ## Process"
    # And R005 should also fire because Workflow is missing.
    assert "missing-section" in fired, "R005 should also fire (Workflow absent)"


def test_loop_no_exit_fires_R013() -> None:
    fired = rules_fired(FIXTURES / "loop-no-exit")
    assert "loop-without-exit-condition" in fired, "R013 should fire for unbounded loop"


def test_constraints_too_many_warning() -> None:
    sevs = severities(FIXTURES / "constraints-too-many")
    assert sevs.get("constraints-too-many") == "warning", (
        f"R022 should fire as warning for 5 constraints; got {sevs.get('constraints-too-many')}"
    )


def test_constraints_polyglot_signal() -> None:
    sevs = severities(FIXTURES / "constraints-polyglot")
    assert "polyglot-skill" in sevs, "Polyglot warning should fire from 7+ constraints"
    assert sevs.get("constraints-too-many") == "warning", "R022 should also warn at 7"


def test_h1_mismatch_fires_R002() -> None:
    fired = rules_fired(FIXTURES / "h1-mismatch")
    assert "h1-name-mismatch" in fired, "R002 should fire when H1 has zero overlap with kebab name"


def test_h1_acronym_passes_R002() -> None:
    """Tier 1: acronym-cased H1 (e.g. 'OK' vs 'Ok') must NOT fire R002."""
    fired = rules_fired(FIXTURES / "h1-acronym-ok")
    assert "h1-name-mismatch" not in fired, "R002 must not fire when H1 differs only in acronym capitalisation"


def test_h1_overlap_passes_R002() -> None:
    """Tier 2: H1 with ≥50% word overlap must NOT fire R002."""
    fired = rules_fired(FIXTURES / "h1-overlap-ok")
    assert "h1-name-mismatch" not in fired, "R002 must not fire when H1 shares ≥50% tokens with kebab name"


def test_h1_overlap_boundary_passes_R002() -> None:
    """Tier 2 boundary: H1 with exactly 50%+ overlap (2/3 tokens) must NOT fire R002."""
    fired = rules_fired(FIXTURES / "h1-overlap-boundary")
    assert "h1-name-mismatch" not in fired, "R002 must not fire at the 50% overlap boundary"


def test_h1_overlap_fail_fires_R002() -> None:
    """Tier 2 rejection: H1 with 0% token overlap MUST fire R002."""
    fired = rules_fired(FIXTURES / "h1-overlap-fail")
    assert "h1-name-mismatch" in fired, "R002 must fire when H1 has no token overlap with kebab name"


def test_h1_acronym_real_passes_R002() -> None:
    """Tier 1 real-world case: 'Azure AI Fixture' for 'azure-ai-fixture' — AI vs Ai must NOT fire."""
    fired = rules_fired(FIXTURES / "h1-acronym-real")
    assert "h1-name-mismatch" not in fired, "R002 must not fire on real-world acronym capitalisation (AI vs Ai)"


def test_reference_files_ok_passes() -> None:
    fired = rules_fired(FIXTURES / "reference-files-ok")
    # Should not flag Reference files for being out of order or non-canonical.
    forbidden = {
        "section-out-of-order",
        "non-canonical-heading",
        "non-canonical-section",
        "missing-section",
    }
    overlap = fired & forbidden
    assert overlap == set(), f"Reference files in correct position should be clean; got: {overlap}"


def test_missing_h1_fires_R001() -> None:
    fired = rules_fired(FIXTURES / "missing-h1")
    assert "missing-h1-title" in fired, "R001 should fire when H1 is absent"


def test_missing_pitch_fires_R003() -> None:
    fired = rules_fired(FIXTURES / "missing-pitch")
    assert "missing-pitch-line" in fired, "R003 should fire when no pitch line follows H1"


def test_pitch_multiline_fires_R004() -> None:
    fired = rules_fired(FIXTURES / "pitch-multiline")
    assert "pitch-not-one-line" in fired, "R004 should fire when pitch spans multiple lines"


def test_section_out_of_order_fires_R007() -> None:
    fired = rules_fired(FIXTURES / "section-out-of-order")
    assert "section-out-of-order" in fired, "R007 should fire when sections are reordered"


def test_overview_paragraph_count_fires_R008() -> None:
    fired = rules_fired(FIXTURES / "overview-paragraph-count")
    assert "overview-paragraph-count" in fired, "R008 should fire when Overview has <3 paragraphs"


def test_overview_subheading_fires_R009() -> None:
    fired = rules_fired(FIXTURES / "overview-subheading")
    assert "overview-has-subheadings" in fired, "R009 should fire when Overview has sub-headings"


def test_workflow_no_steps_fires_R010() -> None:
    fired = rules_fired(FIXTURES / "workflow-no-steps")
    assert "workflow-missing-steps" in fired, "R010 should fire when Workflow has no Step headings"


def test_workflow_step_numbering_fires_R011() -> None:
    fired = rules_fired(FIXTURES / "workflow-step-numbering")
    assert "workflow-step-numbering" in fired, "R011 should fire when steps skip numbers"


def test_empty_step_single_warning() -> None:
    sevs = severities(FIXTURES / "empty-step-single")
    assert sevs.get("empty-workflow-step") == "warning", (
        f"R012 should fire as warning for one empty step; got {sevs.get('empty-workflow-step')}"
    )


def test_empty_step_multiple_error() -> None:
    sevs = severities(FIXTURES / "empty-step-multiple")
    assert sevs.get("empty-workflow-step") == "error", (
        f"R012 should escalate to error for >=2 empty steps; got {sevs.get('empty-workflow-step')}"
    )


def test_polyglot_pitch_fires_R014() -> None:
    fired = rules_fired(FIXTURES / "polyglot-pitch")
    assert "polyglot-skill" in fired, "R014 should fire on a strong second-workflow pitch marker"


def test_unreadable_fires_R016() -> None:
    fired = rules_fired(FIXTURES / "unreadable")
    assert "skill-md-unreadable" in fired, "R016 should fire when SKILL.md is missing"
    # When unreadable, no other rules should run (terminal).
    assert fired == {"skill-md-unreadable"}, f"R016 must be terminal; got: {fired}"


def test_non_canonical_strict_only() -> None:
    fired_default = rules_fired(FIXTURES / "non-canonical-strict", strict=False)
    fired_strict = rules_fired(FIXTURES / "non-canonical-strict", strict=True)
    assert "non-canonical-section" not in fired_default, "R017 must not fire in default mode"
    assert "non-canonical-section" in fired_strict, "R017 must fire in strict mode"


def test_constraints_empty_fires_R020() -> None:
    fired = rules_fired(FIXTURES / "constraints-empty")
    assert "constraints-empty" in fired, "R020 should fire when Constraints has no bullets"


def test_constraints_not_bullets_fires_R021() -> None:
    fired = rules_fired(FIXTURES / "constraints-not-bullets")
    assert "constraints-not-bullets" in fired, "R021 should fire when Constraints contains paragraphs"


# ---------------------------------------------------------------------------
# v0.5 rules (R024–R029)
# Each rule has a positive test (rule fires on a fixture designed to break it)
# AND a negative test against valid_skill/ (zero-false-positive doctrine).
# ---------------------------------------------------------------------------


def test_name_matches_directory_fires_R024() -> None:
    fired = rules_fired(FIXTURES / "name_mismatch_dir" / "skill-renamed-dir")
    assert "name-matches-directory" in fired, "R024 should fire when name != directory"


def test_name_matches_directory_negative_R024() -> None:
    """Zero-false-positive: R024 must NOT fire on the compliant valid_skill fixture."""
    fired = rules_fired(FIXTURES / "valid-skill")
    assert "name-matches-directory" not in fired, "R024 must not fire on a compliant skill"


def test_references_only_text_fires_R025() -> None:
    fired = rules_fired(FIXTURES / "references-with-binary")
    assert "references-only-text" in fired, "R025 should fire when references/ has non-text files"


def test_references_only_text_negative_R025() -> None:
    """Zero-false-positive: R025 must NOT fire when references/ is absent or only contains .md/.txt."""
    fired = rules_fired(FIXTURES / "valid-skill")
    assert "references-only-text" not in fired, "R025 must not fire when references/ is absent"


def test_body_not_empty_fires_R026() -> None:
    fired = rules_fired(FIXTURES / "body-too-short")
    assert "body-not-empty" in fired, "R026 should fire when body has <50 substantive chars"


def test_body_not_empty_negative_R026() -> None:
    """Zero-false-positive: R026 must NOT fire on a normally-sized body."""
    fired = rules_fired(FIXTURES / "valid-skill")
    assert "body-not-empty" not in fired, "R026 must not fire on a normally-sized body"


def test_body_leanness_fires_R028() -> None:
    fired = rules_fired(FIXTURES / "body-too-long")
    assert "body-leanness" in fired, "R028 should fire when body exceeds 300 lines"


def test_body_leanness_negative_R028() -> None:
    """Zero-false-positive: R028 must NOT fire on a small fixture."""
    fired = rules_fired(FIXTURES / "valid-skill")
    assert "body-leanness" not in fired, "R028 must not fire on a small body"


def test_line_budget_negative_R027() -> None:
    """Zero-false-positive: R027 must NOT fire on small skills."""
    fired = rules_fired(FIXTURES / "valid-skill")
    assert "line-budget" not in fired, "R027 must not fire on a short SKILL.md"


def test_reference_pointers_broken_fires_R029() -> None:
    fired = rules_fired(FIXTURES / "reference-pointers-broken")
    assert "reference-files-pointers-resolve" in fired, (
        "R029 should fire when Reference files lists missing paths"
    )


def test_render_markdown_format() -> None:
    """v0.8: --format md must produce a grouped markdown report with severity sections."""
    parsed, findings = lint.lint(FIXTURES / "missing-overview")
    report = lint.build_report(FIXTURES / "missing-overview", parsed, findings)
    md = lint.render_markdown(report)
    # Header
    assert md.startswith("# Skill Lint Report"), "Markdown report must start with H1 title"
    assert "**Status:** ❌ FAILED" in md or "**Status:** ✅ PASSED" in md, "Status line required"
    # Summary table
    assert "| Severity | Count |" in md, "Summary table must be present"
    # Severity sections (this fixture has at least one error)
    assert "## ❌ Errors" in md, "Errors section must be present when errors exist"
    # Each finding rendered with rule code-quoted
    assert "`missing-section`" in md, "Findings must be rendered with rule names"


def test_render_markdown_clean_skill() -> None:
    """v0.8: a clean fixture must yield a 'No findings' markdown body, not error sections."""
    parsed, findings = lint.lint(FIXTURES / "valid-skill")
    # Filter to non-info findings (info doesn't gate but does render)
    report = lint.build_report(FIXTURES / "valid-skill", parsed, findings)
    md = lint.render_markdown(report)
    # Clean (or near-clean) skill should report PASSED status.
    assert "**Status:** ✅ PASSED" in md, "Clean skill must show PASSED status in markdown report"


def test_references_alias_accepted() -> None:
    """v0.7: '## References' is a canonical alias for '## Reference files'.
    R006 (non-canonical-heading) and R007 (section-out-of-order) MUST NOT fire on it."""
    fired = rules_fired(FIXTURES / "references-alias-ok")
    assert "non-canonical-heading" not in fired, "R006 must not fire on the canonical alias '## References'"
    assert "section-out-of-order" not in fired, "R007 must not fire when alias is in correct position"
    # And in strict mode, R017 must not fire either.
    fired_strict = rules_fired(FIXTURES / "references-alias-ok", strict=True)
    assert "non-canonical-section" not in fired_strict, "R017 must not fire on the canonical alias even in strict mode"


def test_reference_pointers_negative_R029() -> None:
    """Zero-false-positive: R029 must NOT fire when all referenced paths exist."""
    fired = rules_fired(FIXTURES / "reference-files-ok")
    # reference_files_ok lists scripts/foo.py and references/bar.md which DO NOT exist
    # in that fixture either, so R029 SHOULD fire there. To get a true negative,
    # we use valid_skill which has no Reference files section at all.
    fired_valid = rules_fired(FIXTURES / "valid-skill")
    assert "reference-files-pointers-resolve" not in fired_valid, (
        "R029 must not fire when there is no Reference files section"
    )


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------


def main() -> int:
    tests = [
        ("valid_skill_passes", test_valid_skill_passes),
        ("valid_skill_strict_passes", test_valid_skill_strict_passes),
        ("missing_overview_fires_R005", test_missing_overview_fires_R005),
        ("missing_constraints_fires_R005", test_missing_constraints_fires_R005),
        ("non_canonical_heading_fires_R006", test_non_canonical_heading_fires_R006),
        ("loop_no_exit_fires_R013", test_loop_no_exit_fires_R013),
        ("constraints_too_many_warning", test_constraints_too_many_warning),
        ("constraints_polyglot_signal", test_constraints_polyglot_signal),
        ("h1_mismatch_fires_R002", test_h1_mismatch_fires_R002),
        ("h1_acronym_passes_R002", test_h1_acronym_passes_R002),
        ("h1_overlap_passes_R002", test_h1_overlap_passes_R002),
        ("h1_overlap_boundary_passes_R002", test_h1_overlap_boundary_passes_R002),
        ("h1_overlap_fail_fires_R002", test_h1_overlap_fail_fires_R002),
        ("h1_acronym_real_passes_R002", test_h1_acronym_real_passes_R002),
        ("reference_files_ok_passes", test_reference_files_ok_passes),
        ("missing_h1_fires_R001", test_missing_h1_fires_R001),
        ("missing_pitch_fires_R003", test_missing_pitch_fires_R003),
        ("pitch_multiline_fires_R004", test_pitch_multiline_fires_R004),
        ("section_out_of_order_fires_R007", test_section_out_of_order_fires_R007),
        ("overview_paragraph_count_fires_R008", test_overview_paragraph_count_fires_R008),
        ("overview_subheading_fires_R009", test_overview_subheading_fires_R009),
        ("workflow_no_steps_fires_R010", test_workflow_no_steps_fires_R010),
        ("workflow_step_numbering_fires_R011", test_workflow_step_numbering_fires_R011),
        ("empty_step_single_warning", test_empty_step_single_warning),
        ("empty_step_multiple_error", test_empty_step_multiple_error),
        ("polyglot_pitch_fires_R014", test_polyglot_pitch_fires_R014),
        ("unreadable_fires_R016", test_unreadable_fires_R016),
        ("non_canonical_strict_only", test_non_canonical_strict_only),
        ("constraints_empty_fires_R020", test_constraints_empty_fires_R020),
        ("constraints_not_bullets_fires_R021", test_constraints_not_bullets_fires_R021),
        # v0.5 rules
        ("name_matches_directory_fires_R024", test_name_matches_directory_fires_R024),
        ("name_matches_directory_negative_R024", test_name_matches_directory_negative_R024),
        ("references_only_text_fires_R025", test_references_only_text_fires_R025),
        ("references_only_text_negative_R025", test_references_only_text_negative_R025),
        ("body_not_empty_fires_R026", test_body_not_empty_fires_R026),
        ("body_not_empty_negative_R026", test_body_not_empty_negative_R026),
        ("body_leanness_fires_R028", test_body_leanness_fires_R028),
        ("body_leanness_negative_R028", test_body_leanness_negative_R028),
        ("line_budget_negative_R027", test_line_budget_negative_R027),
        ("reference_pointers_broken_fires_R029", test_reference_pointers_broken_fires_R029),
        ("reference_pointers_negative_R029", test_reference_pointers_negative_R029),
        # v0.7
        ("references_alias_accepted", test_references_alias_accepted),
        # v0.8
        ("render_markdown_format", test_render_markdown_format),
        ("render_markdown_clean_skill", test_render_markdown_clean_skill),
    ]
    passed = 0
    failed: list[tuple[str, str]] = []
    for name, fn in tests:
        try:
            fn()
            passed += 1
            print(f"  ✓ {name}")
        except AssertionError as e:
            failed.append((name, str(e)))
            print(f"  ✗ {name}: {e}")
        except Exception as e:
            failed.append((name, f"{type(e).__name__}: {e}"))
            print(f"  ✗ {name}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed, {len(failed)} failed")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
