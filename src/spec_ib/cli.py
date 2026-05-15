"""cli.py - Public command-line entry points."""

from spec_ib.commands.manifest import (
    sync_main,
)
from spec_ib.commands.reference import (
    ref_export_main,
    ref_validate_main,
)
from spec_ib.commands.root import main
from spec_ib.commands.validate import validate_main

__all__ = [
    "main",
    "ref_export_main",
    "ref_validate_main",
    "sync_main",
    "validate_main",
]


if __name__ == "__main__":
    raise SystemExit(main())
