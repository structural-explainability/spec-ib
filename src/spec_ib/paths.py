# src/spec_ib/paths.py
"""paths.py - Repository path helpers."""

from pathlib import Path

_REFERENCE_DIR_NAME = "reference"
_REFERENCE_INDEX_NAME = "index.toml"
_DATA_DIR_NAME = "data"
_SPEC_DIR_NAME = "spec"


def repo_root(start: Path | None = None) -> Path:
    """Find and return the repository root."""
    current = (start or Path(__file__)).resolve()

    if current.is_file():
        current = current.parent

    markers = ("pyproject.toml", "SE_MANIFEST.toml", ".git")

    for candidate in (current, *current.parents):
        if any((candidate / marker).exists() for marker in markers):
            return candidate

    raise FileNotFoundError(
        f"Could not find repository root from: {current}. "
        "Expected pyproject.toml, SE_MANIFEST.toml, or .git."
    )


def reference_dir(root: Path | None = None) -> Path:
    """Return the path to reference/."""
    return (root or repo_root()) / _REFERENCE_DIR_NAME


def reference_index_path(root: Path | None = None) -> Path:
    """Return the path to reference/index.toml."""
    return reference_dir(root) / _REFERENCE_INDEX_NAME


def data_dir(root: Path | None = None) -> Path:
    """Return the path to data/."""
    return (root or repo_root()) / _DATA_DIR_NAME


def data_spec_dir(root: Path | None = None) -> Path:
    """Return the path to data/spec/."""
    return data_dir(root) / _SPEC_DIR_NAME


def data_spec_path(name: str, root: Path | None = None) -> Path:
    """Return a path under data/spec/."""
    return data_spec_dir(root) / name


def resolve_repo_path(path: str | Path, root: Path | None = None) -> Path:
    """Resolve a repository-relative path safely."""
    repo = (root or repo_root()).resolve()
    relative_path = Path(path)

    if relative_path.is_absolute():
        raise ValueError(
            f"Expected repo-relative path, got absolute path: {relative_path}"
        )

    resolved = (repo / relative_path).resolve()

    try:
        resolved.relative_to(repo)
    except ValueError as e:
        raise ValueError(f"Path escapes repository root: {relative_path}") from e

    return resolved


def reference_artifact_path(path: str | Path, root: Path | None = None) -> Path:
    """Resolve a declared reference artifact path."""
    resolved = resolve_repo_path(path, root=root)
    reference = reference_dir(root).resolve()

    try:
        resolved.relative_to(reference)
    except ValueError as e:
        raise ValueError(
            f"Reference artifact path is not under reference/: {path}"
        ) from e

    return resolved
