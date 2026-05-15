# src/spec_ib/commands/root.py
"""Root command dispatcher."""

import argparse

from spec_ib.commands.manifest import sync_main
from spec_ib.commands.reference import ref_export_main, ref_validate_main
from spec_ib.commands.validate import validate_main


def main(argv: list[str] | None = None) -> int:
    """Dispatch spec_ib commands."""
    parser = argparse.ArgumentParser(description="spec-ib command line interface.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("validate")
    subparsers.add_parser("ref-validate")
    subparsers.add_parser("ref-export")
    subparsers.add_parser("sync")

    args, remaining = parser.parse_known_args(argv)

    if args.command == "validate":
        return validate_main(remaining)

    if args.command == "ref-validate":
        return ref_validate_main(remaining)

    if args.command == "ref-export":
        return ref_export_main(remaining)

    if args.command == "sync":
        return sync_main(remaining)

    parser.print_help()
    return 0
