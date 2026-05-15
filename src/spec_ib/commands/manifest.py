"""Manifest command entry points."""

from se_manifest_schema.sync import sync_all


def sync_main() -> int:
    """Sync version metadata."""
    sync_all()
    return 0
