# src/spec_ib/extractor_utils.py
"""Strict Markdown extraction utilities for boundary specifications."""

from dataclasses import dataclass
import re

IDENTIFIER_RE = re.compile(r"^[A-Z][A-Z0-9]*\.[A-Z0-9_]+(?:\.[A-Z0-9_]+)*$")
CANONICAL_LIST_HEADING = "## Canonical Identifier List (Alphabetical, with Notes)"


@dataclass(frozen=True)
class Requirement:
    """A canonical requirement identifier and explanatory note."""

    id: str
    note: str
    normative_source: str


def validate_identifier(identifier: str, expected_prefix: str) -> None:
    """Validate a requirement identifier."""
    if not IDENTIFIER_RE.fullmatch(identifier):
        raise ValueError(f"Invalid identifier: {identifier}")

    expected_start = f"{expected_prefix}."
    if not identifier.startswith(expected_start):
        raise ValueError(
            f"Identifier {identifier} does not use expected prefix {expected_prefix}."
        )


def extract_identifier_notes(
    identifiers_markdown: str,
    *,
    expected_prefix: str,
) -> list[Requirement]:
    """Extract canonical identifiers and notes from IDENTIFIERS.md."""
    lines = identifiers_markdown.splitlines()
    requirements: list[Requirement] = []
    in_canonical_list = False
    index = 0

    while index < len(lines):
        line = lines[index].strip()

        if line == CANONICAL_LIST_HEADING:
            in_canonical_list = True
            index += 1
            continue

        if in_canonical_list and line.startswith("## "):
            break

        if in_canonical_list and line.startswith(f"{expected_prefix}."):
            identifier = line
            validate_identifier(identifier, expected_prefix)

            note_index = index + 1
            while note_index < len(lines) and not lines[note_index].strip():
                note_index += 1

            if note_index >= len(lines):
                raise ValueError(f"Missing note for {identifier}")

            note_line = lines[note_index].strip()
            if not note_line.startswith("- "):
                raise ValueError(f"Identifier {identifier} must have one note bullet.")

            note = note_line.removeprefix("- ").strip()
            if not note:
                raise ValueError(f"Identifier {identifier} has an empty note.")

            following_index = note_index + 1
            while following_index < len(lines) and not lines[following_index].strip():
                following_index += 1

            if following_index < len(lines):
                following_line = lines[following_index].strip()
                if following_line.startswith("- "):
                    raise ValueError(f"Identifier {identifier} has multiple notes.")

            requirements.append(
                Requirement(
                    id=identifier,
                    note=note,
                    normative_source=f"SPEC.md#{identifier}",
                )
            )

            index = following_index
            continue

        index += 1

    identifiers = [requirement.id for requirement in requirements]

    if not identifiers:
        raise ValueError("No canonical identifiers found.")

    assert_unique(identifiers, source_name="IDENTIFIERS.md")
    assert_alphabetical_order(identifiers, source_name="IDENTIFIERS.md")

    return requirements


def extract_heading_identifiers(
    markdown: str,
    *,
    expected_prefix: str,
) -> list[str]:
    """Extract level-2 requirement headings from Markdown."""
    identifiers: list[str] = []

    for line in markdown.splitlines():
        stripped = line.strip()

        if not stripped.startswith("## "):
            continue

        heading = stripped.removeprefix("## ").strip()

        if heading.startswith(f"{expected_prefix}."):
            validate_identifier(heading, expected_prefix)
            identifiers.append(heading)

    return identifiers


def assert_unique(identifiers: list[str], *, source_name: str) -> None:
    """Assert that identifiers are unique."""
    duplicates = sorted(
        identifier
        for identifier in set(identifiers)
        if identifiers.count(identifier) > 1
    )
    if duplicates:
        raise ValueError(f"{source_name} has duplicate identifiers: {duplicates}")


def assert_alphabetical_order(
    identifiers: list[str],
    *,
    source_name: str,
) -> None:
    """Assert that identifiers are alphabetical."""
    if identifiers != sorted(identifiers):
        raise ValueError(f"{source_name} identifiers are not alphabetical.")


def assert_exact_identifier_coverage(
    *,
    canonical_ids: list[str],
    found_ids: list[str],
    source_name: str,
) -> None:
    """Assert exact coverage of canonical identifiers."""
    canonical_set = set(canonical_ids)
    found_set = set(found_ids)

    missing = sorted(canonical_set - found_set)
    unknown = sorted(found_set - canonical_set)

    if missing:
        raise ValueError(f"{source_name} is missing identifiers: {missing}")

    if unknown:
        raise ValueError(f"{source_name} has unknown identifiers: {unknown}")

    assert_unique(found_ids, source_name=source_name)
