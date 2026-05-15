# src/spec_ib/orchestrate.py
"""Validation orchestration."""

from pathlib import Path

from spec_ib.export import export_all
from spec_ib.validate import validate_all


def run_validate(
    *,
    version: str,
    root: Path | None = None,
    strict: bool = False,
) -> None:
    """Run validation checks."""
    validate_all(version=version, root=root)

    if strict:
        export_all(version=version, root=root, check=True)


def run_ref_export(
    *,
    version: str,
    root: Path | None = None,
    check: bool = False,
) -> list[Path]:
    """Run reference export checks.

    For GB, reference export means generated data/spec artifacts.
    """
    return export_all(version=version, root=root, check=check)


def run_ref_validate(
    *,
    version: str,
    root: Path | None = None,
) -> None:
    """Validate generated reference artifacts."""
    export_all(version=version, root=root, check=True)
