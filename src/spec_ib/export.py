# src/spec_ib/export.py
"""Export generated IB machine-readable specification artifacts."""

from dataclasses import asdict, dataclass
import json
from pathlib import Path

from spec_ib.extractor_utils import (
    Requirement,
    assert_alphabetical_order,
    assert_exact_identifier_coverage,
    extract_heading_identifiers,
    extract_identifier_notes,
)
from spec_ib.load import load_text
from spec_ib.paths import data_spec_path, repo_root

SPEC_ID = "IB"
SPEC_NAME = "Interpretation Boundary"
SPEC_STATUS = "normative"


@dataclass(frozen=True)
class RequirementExport:
    """Generated requirements export."""

    schema: str
    spec: dict[str, str]
    requirements: list[Requirement]


@dataclass(frozen=True)
class ScopeExclusionExport:
    """Generated scope exclusions export."""

    schema: str
    spec: dict[str, str]
    excluded: list[str]


@dataclass(frozen=True)
class ConformanceCheck:
    """Generated conformance check section."""

    id: str
    checks: list[str]
    failure_conditions: list[str]


@dataclass(frozen=True)
class ConformanceExport:
    """Generated conformance checks export."""

    schema: str
    spec: dict[str, str]
    checks: list[ConformanceCheck]


def spec_metadata(version: str) -> dict[str, str]:
    """Return shared IB metadata."""
    return {
        "id": SPEC_ID,
        "name": SPEC_NAME,
        "version": version,
        "status": SPEC_STATUS,
    }


def canonical_requirements(root: Path | None = None) -> list[Requirement]:
    """Return canonical requirements from IDENTIFIERS.md."""
    repo = root or repo_root()
    return extract_identifier_notes(
        load_text(repo / "IDENTIFIERS.md"),
        expected_prefix=SPEC_ID,
    )


def canonical_ids(root: Path | None = None) -> list[str]:
    """Return canonical requirement identifiers."""
    return [requirement.id for requirement in canonical_requirements(root)]


def build_requirements_export(
    *,
    version: str,
    root: Path | None = None,
) -> RequirementExport:
    """Build requirements.json content."""
    repo = root or repo_root()
    requirements = canonical_requirements(repo)
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

    return RequirementExport(
        schema="se-boundary-requirements-1",
        spec=spec_metadata(version),
        requirements=requirements,
    )


def extract_scope_exclusions(markdown: str) -> list[str]:
    """Extract bullets from the IB.SCOPE.EXCLUSIONS section."""
    lines = markdown.splitlines()
    exclusions: list[str] = []
    in_section = False

    for line in lines:
        stripped = line.strip()

        if stripped == "## IB.SCOPE.EXCLUSIONS":
            in_section = True
            continue

        if in_section and stripped.startswith("## "):
            break

        if in_section and stripped.startswith("- "):
            exclusions.append(stripped.removeprefix("- ").strip())

    if not exclusions:
        raise ValueError("No scope exclusions found in IB.SCOPE.EXCLUSIONS.")

    return exclusions


def build_scope_exclusions_export(
    *,
    version: str,
    root: Path | None = None,
) -> ScopeExclusionExport:
    """Build scope-exclusions.json content."""
    repo = root or repo_root()
    exclusions = extract_scope_exclusions(load_text(repo / "SPEC.md"))

    return ScopeExclusionExport(
        schema="se-boundary-scope-exclusions-1",
        spec=spec_metadata(version),
        excluded=exclusions,
    )


def extract_conformance_checks(markdown: str, ids: list[str]) -> list[ConformanceCheck]:
    """Extract check bullets and failure conditions from CONFORMANCE.md."""
    lines = markdown.splitlines()
    checks: list[ConformanceCheck] = []

    for index, line in enumerate(lines):
        stripped = line.strip()

        if not stripped.startswith("## IB."):
            continue

        identifier = stripped.removeprefix("## ").strip()
        if identifier not in ids:
            raise ValueError(f"Unknown conformance identifier: {identifier}")

        section_lines: list[str] = []
        cursor = index + 1

        while cursor < len(lines):
            candidate = lines[cursor].strip()
            if candidate.startswith("## "):
                break
            section_lines.append(candidate)
            cursor += 1

        section_checks = [
            item.removeprefix("- ").strip()
            for item in section_lines
            if item.startswith("- ") and not item.startswith("- Fail if:")
        ]

        failure_conditions = [
            item.removeprefix("- Fail if:").strip()
            for item in section_lines
            if item.startswith("- Fail if:")
        ]

        failure_conditions.extend(
            item for item in section_lines if "constitutes non-conformance" in item
        )

        checks.append(
            ConformanceCheck(
                id=identifier,
                checks=section_checks,
                failure_conditions=failure_conditions,
            )
        )

    assert_exact_identifier_coverage(
        canonical_ids=ids,
        found_ids=[check.id for check in checks],
        source_name="CONFORMANCE.md",
    )

    return checks


def build_conformance_export(
    *,
    version: str,
    root: Path | None = None,
) -> ConformanceExport:
    """Build conformance-checks.json content."""
    repo = root or repo_root()
    ids = canonical_ids(repo)
    checks = extract_conformance_checks(load_text(repo / "CONFORMANCE.md"), ids)

    return ConformanceExport(
        schema="se-boundary-conformance-checks-1",
        spec=spec_metadata(version),
        checks=checks,
    )


def export_all(
    *,
    version: str,
    root: Path | None = None,
    check: bool = False,
) -> list[Path]:
    """Generate or check all data/spec JSON artifacts."""
    repo = root or repo_root()

    outputs = [
        (
            data_spec_path("requirements.json", repo),
            build_requirements_export(version=version, root=repo),
        ),
        (
            data_spec_path("scope-exclusions.json", repo),
            build_scope_exclusions_export(version=version, root=repo),
        ),
        (
            data_spec_path("conformance-checks.json", repo),
            build_conformance_export(version=version, root=repo),
        ),
    ]

    written_paths: list[Path] = []

    for path, data in outputs:
        rendered = json.dumps(asdict(data), indent=2, ensure_ascii=False) + "\n"

        if check:
            if not path.exists():
                raise FileNotFoundError(f"Missing generated artifact: {path}")
            current = path.read_text(encoding="utf-8")
            if current != rendered:
                raise ValueError(f"Generated artifact is stale: {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(rendered, encoding="utf-8")

        written_paths.append(path)

    return written_paths
