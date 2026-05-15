"""Tests for CONFORMANCE.md requirement coverage."""

from spec_ib.export import SPEC_ID
from spec_ib.extractor_utils import (
    assert_alphabetical_order,
    assert_exact_identifier_coverage,
    extract_heading_identifiers,
    extract_identifier_notes,
)
from spec_ib.load import load_text
from spec_ib.paths import repo_root


def test_conformance_covers_all_canonical_identifiers() -> None:
    """CONFORMANCE.md contains exactly the canonical requirement identifiers."""
    root = repo_root()

    requirements = extract_identifier_notes(
        load_text(root / "IDENTIFIERS.md"),
        expected_prefix=SPEC_ID,
    )
    canonical_ids = [requirement.id for requirement in requirements]

    conformance_ids = extract_heading_identifiers(
        load_text(root / "CONFORMANCE.md"),
        expected_prefix=SPEC_ID,
    )

    assert_exact_identifier_coverage(
        canonical_ids=canonical_ids,
        found_ids=conformance_ids,
        source_name="CONFORMANCE.md",
    )


def test_conformance_identifier_headings_are_alphabetical() -> None:
    """CONFORMANCE.md requirement headings are alphabetical."""
    root = repo_root()

    conformance_ids = extract_heading_identifiers(
        load_text(root / "CONFORMANCE.md"),
        expected_prefix=SPEC_ID,
    )

    assert_alphabetical_order(conformance_ids, source_name="CONFORMANCE.md")


def test_conformance_has_no_duplicate_identifier_headings() -> None:
    """CONFORMANCE.md has no duplicate requirement headings."""
    root = repo_root()

    conformance_ids = extract_heading_identifiers(
        load_text(root / "CONFORMANCE.md"),
        expected_prefix=SPEC_ID,
    )

    assert len(conformance_ids) == len(set(conformance_ids))


def test_conformance_sections_have_failure_conditions() -> None:
    """Each CONFORMANCE.md section has a failure condition."""
    root = repo_root()
    conformance_text = load_text(root / "CONFORMANCE.md")
    conformance_ids = extract_heading_identifiers(
        conformance_text,
        expected_prefix=SPEC_ID,
    )

    for index, identifier in enumerate(conformance_ids):
        section_start = conformance_text.index(f"## {identifier}")
        if index + 1 < len(conformance_ids):
            section_end = conformance_text.index(f"## {conformance_ids[index + 1]}")
        else:
            section_end = len(conformance_text)

        section_text = conformance_text[section_start:section_end]

        has_fail_bullet = "Fail if:" in section_text
        has_non_conformance_statement = "constitutes non-conformance" in section_text

        assert has_fail_bullet or has_non_conformance_statement
