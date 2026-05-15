# src/spec_ib/load.py
"""load.py - Loading and parsing helpers."""

from importlib.resources import files
import json
from pathlib import Path
import tomllib
from typing import Any


def load_fallback_version(repo_dir: Path) -> str:
    """Load the stable fallback version from pyproject.toml."""
    pyproject_path = repo_dir / "pyproject.toml"

    if not pyproject_path.exists():
        raise FileNotFoundError(f"Missing pyproject.toml: {pyproject_path}")

    data = load_toml(pyproject_path)

    try:
        version = data["tool"]["hatch"]["version"]["fallback-version"]
    except KeyError as e:
        raise ValueError(
            "pyproject.toml does not define [tool.hatch.version] fallback-version."
        ) from e

    if not isinstance(version, str) or not version.strip():
        raise ValueError("fallback-version must be a non-empty string.")

    return version.strip()


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
