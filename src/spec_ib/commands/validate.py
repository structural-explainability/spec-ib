"""Validation command."""

import argparse
from pathlib import Path

from spec_ib.load import load_fallback_version
from spec_ib.orchestrate import run_validate
from spec_ib.ref_utils import find_repo_root


def validate_main(argv: list[str] | None = None) -> int:
    """Run GB validation."""
    parser = argparse.ArgumentParser(description="Validate spec-ib.")
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--version", default=None)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)

    root = find_repo_root(args.repo_root)

    if args.version is None:
        args.version = load_fallback_version(root)

    run_validate(
        version=args.version,
        root=root,
        strict=args.strict,
    )

    print("spec-ib validation passed.")
    return 0
