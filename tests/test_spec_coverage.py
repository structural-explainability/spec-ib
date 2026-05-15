"""Tests for SPEC.md requirement coverage."""

from spec_ib.export import SPEC_ID
from spec_ib.extractor_utils import (
    assert_alphabetical_order,
    assert_exact_identifier_coverage,
    extract_heading_identifiers,
    extract_identifier_notes,
)
from spec_ib.load import load_text
from spec_ib.paths import repo_root


def test_spec_covers_all_canonical_identifiers() -> None:
    """SPEC.md contains exactly the canonical requirement identifiers."""
    root = repo_root()

    requirements = extract_identifier_notes(
        load_text(root / "IDENTIFIERS.md"),
        expected_prefix=SPEC_ID,
    )
    canonical_ids = [requirement.id for requirement in requirements]

    spec_ids = extract_heading_identifiers(
        load_text(root / "SPEC.md"),
        expected_prefix=SPEC_ID,
    )

    assert_exact_identifier_coverage(
        canonical_ids=canonical_ids,
        found_ids=spec_ids,
        source_name="SPEC.md",
    )


def test_spec_identifier_headings_are_alphabetical() -> None:
    """SPEC.md requirement headings are alphabetical."""
    root = repo_root()

    spec_ids = extract_heading_identifiers(
        load_text(root / "SPEC.md"),
        expected_prefix=SPEC_ID,
    )

    assert_alphabetical_order(spec_ids, source_name="SPEC.md")


def test_spec_has_no_duplicate_identifier_headings() -> None:
    """SPEC.md has no duplicate requirement headings."""
    root = repo_root()

    spec_ids = extract_heading_identifiers(
        load_text(root / "SPEC.md"),
        expected_prefix=SPEC_ID,
    )

    assert len(spec_ids) == len(set(spec_ids))


def test_spec_has_non_empty_identifier_sections() -> None:
    """Each SPEC.md requirement heading has section content."""
    root = repo_root()
    spec_text = load_text(root / "SPEC.md")
    spec_ids = extract_heading_identifiers(spec_text, expected_prefix=SPEC_ID)

    for index, identifier in enumerate(spec_ids):
        section_start = spec_text.index(f"## {identifier}")
        if index + 1 < len(spec_ids):
            section_end = spec_text.index(f"## {spec_ids[index + 1]}")
        else:
            section_end = len(spec_text)

        section_text = spec_text[section_start:section_end].strip()

        assert section_text
        assert section_text != f"## {identifier}"
