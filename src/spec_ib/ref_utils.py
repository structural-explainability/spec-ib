"""Shared reference/ validation utilities for SE theory repositories."""

from dataclasses import dataclass
from pathlib import Path
import re
import tomllib
from typing import Any

LEAN_DECL_TO_SECTION: dict[str, str] = {
    "inductive": "type",
    "structure": "type",
    "theorem": "theorem",
    "lemma": "theorem",
    "axiom": "axiom",
    "def": "predicate",
    "abbrev": "predicate",
}

SECTION_LEAN_KINDS: dict[str, set[str]] = {
    "type": {"inductive", "structure"},
    "predicate": {"def", "abbrev"},
    "theorem": {"theorem", "lemma"},
    "axiom": {"axiom"},
    "requirement": {"def"},
    "witness": {"def", "abbrev"},
}

DECL_RE = re.compile(
    r"^(?:private\s+|protected\s+)?(?:noncomputable\s+)?"
    r"(theorem|lemma|def|abbrev|inductive|structure|axiom|class|instance)\s+(\w+)",
    re.MULTILINE,
)

SPEC_STRING_RE = re.compile(
    r"def\s+(\w+)\s*:\s*String\s*:=\s*\"([^\"]+)\"",
    re.MULTILINE,
)


@dataclass(frozen=True)
class LeanDecl:
    """Lean declaration with name, kind, and reference section."""

    name: str
    kind: str
    section: str


def find_repo_root(start: Path | None = None) -> Path:
    """Walk up from start until pyproject.toml is found."""
    origin = start or Path(__file__).resolve()
    for parent in origin.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError(
        f"Cannot locate repo root: no pyproject.toml found above {origin}"
    )


def load_toml(path: Path) -> dict[str, Any]:
    """Load TOML from a path."""
    return tomllib.loads(path.read_text(encoding="utf-8"))


def section_entries(data: dict[str, Any], section: str) -> dict[str, dict[str, Any]]:
    """Return table entries for a reference section."""
    return {
        key: value
        for key, value in data.get(section, {}).items()
        if isinstance(value, dict)
    }


def source_modules_in_registry(data: dict[str, Any]) -> list[str]:
    """Return unique source modules declared by registry entries."""
    seen: set[str] = set()
    result: list[str] = []

    for section_value in data.values():
        if not isinstance(section_value, dict):
            continue
        for entry in section_value.values():
            if not isinstance(entry, dict):
                continue
            module = entry.get("source_module", "")
            if module and module not in seen:
                seen.add(module)
                result.append(module)

    return result


def module_to_path(module: str, lean_root: Path) -> Path:
    """Convert a Lean module name to a file path."""
    parts = module.split(".")
    return lean_root.joinpath(*parts[:-1]) / f"{parts[-1]}.lean"


def path_to_module(path: Path, lean_root: Path) -> str:
    """Convert a Lean file path to a module name."""
    rel = path.relative_to(lean_root).with_suffix("")
    return ".".join(rel.parts)


def infer_core_modules(surface_module: str, lean_root: Path) -> list[str]:
    """Infer Core modules under the surface namespace."""
    if not surface_module.endswith(".Surface"):
        return []

    root_module = surface_module.removesuffix(".Surface")
    root_dir = lean_root.joinpath(*root_module.split("."))

    if not root_dir.exists():
        return []

    core_files = sorted(root_dir.rglob("Core.lean"))

    root_core = root_dir / "Core.lean"
    if root_core in core_files:
        core_files.remove(root_core)
        core_files.insert(0, root_core)

    return [path_to_module(path, lean_root) for path in core_files]


def infer_spec_module(surface_module: str) -> str:
    """Infer the Spec module from the public surface module."""
    if surface_module.endswith(".Surface"):
        return surface_module.removesuffix(".Surface") + ".Spec"
    return surface_module + ".Spec"


def kind_to_section(artifact_kind: str) -> str:
    """Map artifact kind to registry section name."""
    without_suffix = artifact_kind.removesuffix("-registry")
    without_suffix = without_suffix.removesuffix("-definitions")
    return (
        without_suffix.rsplit("-", 1)[-1] if "-" in without_suffix else without_suffix
    )


def extract_decls(lean_file: Path) -> list[LeanDecl]:
    """Extract top-level Lean declarations from a Lean file."""
    if not lean_file.exists():
        return []

    text = lean_file.read_text(encoding="utf-8")
    return [
        LeanDecl(
            name=match.group(2),
            kind=match.group(1),
            section=LEAN_DECL_TO_SECTION.get(match.group(1), "unknown"),
        )
        for match in DECL_RE.finditer(text)
    ]


def extract_for_section(lean_file: Path, target_section: str) -> list[LeanDecl]:
    """Extract Lean declarations matching a reference section."""
    wanted = SECTION_LEAN_KINDS.get(target_section)
    if wanted is None:
        return []
    return [decl for decl in extract_decls(lean_file) if decl.kind in wanted]


def extract_spec_ids(spec_file: Path) -> set[str]:
    """Extract stable citation IDs from a Spec.lean file."""
    if not spec_file.exists():
        return set()

    text = spec_file.read_text(encoding="utf-8")
    return {match.group(2) for match in SPEC_STRING_RE.finditer(text)}


def toml_value(value: Any) -> str:
    """Format a minimal TOML value."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(item) for item in value) + "]"
    return str(value)


def write_registry_toml(path: Path, data: dict[str, Any]) -> None:
    """Write a simple registry TOML file."""
    header_keys = ["schema", "repo", "surface_module", "namespace"]
    lines: list[str] = []

    for key in header_keys:
        if key in data and not isinstance(data[key], dict):
            lines.append(f"{key} = {toml_value(data[key])}")

    lines.append("")

    for section_key, section_value in data.items():
        if section_key in header_keys or not isinstance(section_value, dict):
            continue
        for entry_id, entry in section_value.items():
            if not isinstance(entry, dict):
                continue
            lines.append(f"[{section_key}.{entry_id}]")
            for field_key, field_value in entry.items():
                lines.append(f"{field_key} = {toml_value(field_value)}")
            lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
