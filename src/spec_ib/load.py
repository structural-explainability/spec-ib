# src/spec_ib/load.py
"""load.py - Loading and parsing helpers."""

from importlib.resources import files
import json
from pathlib import Path
import tomllib
from typing import Any


def load_text(path: Path) -> str:
    """Load text from the specified path."""
    return path.read_text(encoding="utf-8")


def load_toml(path: Path) -> dict[str, Any]:
    """Load and return TOML data from the specified path."""
    return tomllib.loads(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict[str, Any]:
    """Load and return JSON data from the specified path."""
    return json.loads(path.read_text(encoding="utf-8"))


def load_manifest_schema() -> dict[str, Any]:
    """Load manifest-schema.toml from se_manifest_schema."""
    schema_path = files("se_manifest_schema") / "manifest-schema.toml"
    with schema_path.open("rb") as f:
        return tomllib.load(f)


def load_reference_index(repo_dir: Path) -> dict[str, Any]:
    """Load reference/index.toml from the repository root."""
    return load_toml(repo_dir / "reference" / "index.toml")
