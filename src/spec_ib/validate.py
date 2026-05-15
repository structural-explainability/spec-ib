# src/spec_ib/validate.py
"""Validate GB specification consistency."""

from pathlib import Path

from spec_ib.export import SPEC_ID, build_conformance_export, build_requirements_export
from spec_ib.extractor_utils import (
    assert_alphabetical_order,
    assert_exact_identifier_coverage,
    extract_heading_identifiers,
    extract_identifier_notes,
)
from spec_ib.load import load_text
from spec_ib.paths import repo_root


def validate_markdown(root: Path | None = None) -> None:
    """Validate IDENTIFIERS.md, SPEC.md, and CONFORMANCE.md consistency."""
    repo = root or repo_root()

    requirements = extract_identifier_notes(
        load_text(repo / "IDENTIFIERS.md"),
        expected_prefix=SPEC_ID,
    )
    ids = [requirement.id for requirement in requirements]

    spec_ids = extract_heading_identifiers(
        load_text(repo / "SPEC.md"),
        expected_prefix=SPEC_ID,
    )
    conformance_ids = extract_heading_identifiers(
        load_text(repo / "CONFORMANCE.md"),
        expected_prefix=SPEC_ID,
    )

    assert_exact_identifier_coverage(
        canonical_ids=ids,
        found_ids=spec_ids,
        source_name="SPEC.md",
    )
    assert_exact_identifier_coverage(
        canonical_ids=ids,
        found_ids=conformance_ids,
        source_name="CONFORMANCE.md",
    )

    assert_alphabetical_order(spec_ids, source_name="SPEC.md")
    assert_alphabetical_order(conformance_ids, source_name="CONFORMANCE.md")


def validate_exports(
    *,
    version: str,
    root: Path | None = None,
) -> None:
    """Validate that export builders can construct all generated artifacts."""
    repo = root or repo_root()
    build_requirements_export(version=version, root=repo)
    build_conformance_export(version=version, root=repo)


def validate_all(
    *,
    version: str,
    root: Path | None = None,
) -> None:
    """Run all GB validation checks."""
    repo = root or repo_root()
    validate_markdown(repo)
    validate_exports(version=version, root=repo)
