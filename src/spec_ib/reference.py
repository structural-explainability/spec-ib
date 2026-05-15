"""reference.py - Scaffold and validate reference/ artifacts from Lean 4 source.

Reads reference/index.toml, walks each artifact, and either validates
existing entries against current Lean declarations or adds stub entries
for symbols not yet in the registry.

Existing human-authored fields (description, name, cite_id) are never
overwritten unless run_scaffold is called with overwrite=True.

Artifacts with generated=true or format=json are always skipped.
proof-registry.json is Lean-generated; this module does not touch it.

Entry points:
  run_scaffold(dry_run, overwrite) -> int
  run_ref_validate(strict)         -> int

Copy this file unchanged to each theory repo.  _find_repo_root() locates
the repo root via pyproject.toml, so the same source works in all three.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from spec_ib.ref_utils import (
    SECTION_LEAN_KINDS,
    LeanDecl,
    extract_decls,
    extract_for_section,
    extract_spec_ids,
    find_repo_root,
    infer_core_modules,
    infer_spec_module,
    load_toml,
    module_to_path,
    section_entries,
    source_modules_in_registry,
    write_registry_toml,
)

# ---------------------------------------------------------------------------
# Per-artifact processing
# ---------------------------------------------------------------------------


@dataclass
class _ArtifactResult:
    artifact_id: str
    ok: bool = True
    messages: list[str] = field(default_factory=list)
    wrote: bool = False
    added: int = 0
    orphaned: int = 0

    def _emit(self, prefix: str, msg: str) -> None:
        self.messages.append(f"  {prefix}  {msg}")

    def fail(self, msg: str) -> None:
        self.ok = False
        self._emit("FAIL", msg)

    def warn(self, msg: str) -> None:
        self._emit("warn", msg)

    def added_sym(self, msg: str) -> None:
        self._emit("+   ", msg)

    def note(self, msg: str) -> None:
        self._emit("    ", msg)


def _process_artifact(
    artifact: dict,
    repo_root: Path,
    lean_root: Path,
    index_surface_module: str,
    dry_run: bool,
    overwrite: bool,
    all_registered: set[str] | None = None,
) -> _ArtifactResult:
    """Process a single artifact from the index, returning an _ArtifactResult with details and messages."""
    art_id = artifact.get("id", "<unnamed>")
    rel_path = artifact.get("path", "")
    fmt = artifact.get("format", "toml")
    generated = artifact.get("generated", False)
    kind = artifact.get("kind", "")
    section = _kind_to_section(kind)
    result = _ArtifactResult(artifact_id=art_id)

    if generated or fmt != "toml":
        result.note("skipped (generated or non-toml)")
        return result

    art_path = repo_root / rel_path
    existing_data: dict = {}

    if art_path.exists():
        try:
            existing_data = load_toml(art_path)
        except Exception as exc:
            result.fail(f"TOML parse error: {exc}")
            return result
    else:
        result.note("no existing file; will create")

    # Source module resolution
    source_modules: list[str] = []
    if "source_module" in artifact:
        source_modules = [artifact["source_module"]]
    if not source_modules and existing_data:
        source_modules = source_modules_in_registry(existing_data)
    if not source_modules:
        surface = existing_data.get("surface_module", index_surface_module)
        source_modules = infer_core_modules(surface, lean_root)
        if source_modules:
            result.note("source modules inferred: " + ", ".join(source_modules))
        else:
            derived = surface.replace("Surface", "Core")
            source_modules = [derived]
            result.note(f"source module inferred: {derived}")

    # Scan Lean files
    all_decls: list[LeanDecl] = []
    for mod in source_modules:
        lean_file = module_to_path(mod, lean_root)
        if not lean_file.exists():
            result.fail(f"lean file not found: {lean_file}")
            continue
        all_decls.extend(extract_for_section(lean_file, section))

    if not result.ok:
        return result

    lean_by_name: dict[str, LeanDecl] = {d.name: d for d in all_decls}

    # All declared symbols regardless of kind used to disambiguate orphans
    # from kind-mismatches (e.g. inductive refactored to abbrev).
    all_lean_by_name: dict[str, LeanDecl] = {}
    sym_to_mod: dict[str, str] = {}
    for mod in source_modules:
        for d in extract_decls(module_to_path(mod, lean_root)):
            all_lean_by_name.setdefault(d.name, d)
            sym_to_mod.setdefault(d.name, mod)
    existing_entries = section_entries(existing_data, section)
    existing_symbols: set[str] = {
        e["lean_symbol"] for e in existing_entries.values() if "lean_symbol" in e
    }

    # Orphaned entries
    for sym in sorted(existing_symbols - set(lean_by_name)):
        if sym in all_lean_by_name:
            actual = all_lean_by_name[sym].kind
            result.warn(
                f"lean_symbol declared as {actual!r} not {section!r}: {sym!r}"
                f"  (kind mismatch - intentional refactor?)"
            )
        else:
            result.warn(f"lean_symbol no longer in Lean: {sym!r}  (orphaned)")
            result.orphaned += 1

    # Missing entries
    section_data: dict = existing_data.setdefault(section, {})
    for name in sorted(set(lean_by_name) - existing_symbols):
        if all_registered and name in all_registered:
            result.note(f"skipped: {name!r} already registered in another artifact")
            continue
        decl = lean_by_name[name]
        stub = _make_stub(decl, sym_to_mod.get(name, source_modules[0]))
        if name in section_data:
            section_data[name] = _merge(section_data[name], stub, overwrite)
        else:
            section_data[name] = stub
            result.added_sym(f"stub added: {section}.{name}")
            result.added += 1

    # When overwrite=True, re-merge all existing entries against fresh stubs.
    if overwrite:
        for name, decl in lean_by_name.items():
            if name in section_data:
                stub = _make_stub(decl, sym_to_mod.get(name, source_modules[0]))
                section_data[name] = _merge(section_data[name], stub, overwrite=True)

    # Required-field validation. Only applies to Lean symbol sections.
    # Dependency and traceability registries use a different schema and are
    # hand-authored; their entries intentionally omit lean_symbol/source_module.
    if section in SECTION_LEAN_KINDS:
        required = _REQUIRED_BASE | (
            {"status"} if section in _REQUIRED_STATUS else set()
        )
        for entry_id, entry in section_entries(existing_data, section).items():
            for req in sorted(required):
                if req not in entry:
                    result.warn(f"missing field {req!r} on {section}.{entry_id}")
        spec_module = infer_spec_module(index_surface_module)
        spec_file = module_to_path(spec_module, lean_root)
        spec_ids = extract_spec_ids(spec_file)
        _validate_cite_ids_against_spec(
            existing_data,
            section,
            spec_ids,
            result,
        )

    if result.orphaned == 0 and result.added == 0:
        result.note("all lean_symbols match")

    # Ensure header metadata for new files
    existing_data.setdefault("schema", f"se-{kind}-1")
    existing_data.setdefault("repo", repo_root.name)
    existing_data.setdefault("surface_module", index_surface_module)

    # Write
    if not dry_run and (result.added > 0 or not art_path.exists() or overwrite):
        art_path.parent.mkdir(parents=True, exist_ok=True)
        write_registry_toml(art_path, existing_data)
        result.wrote = True

    return result


def _kind_to_section(artifact_kind: str) -> str:
    """'substrate-type-registry' -> 'type', 'se-theorem-registry' -> 'theorem'."""
    without_suffix = artifact_kind.removesuffix("-registry")
    return (
        without_suffix.rsplit("-", 1)[-1] if "-" in without_suffix else without_suffix
    )


def _validate_cite_ids_against_spec(
    existing_data: dict,
    section: str,
    spec_ids: set[str],
    result: _ArtifactResult,
) -> None:
    """Warn when reference cite_id values are absent from Spec.lean."""
    if not spec_ids:
        result.warn("no Spec.lean citation IDs found")
        return

    for entry_id, entry in section_entries(existing_data, section).items():
        cite_id = entry.get("cite_id")
        if not cite_id:
            continue
        if cite_id not in spec_ids:
            result.warn(
                f"cite_id not declared in Spec.lean on {section}.{entry_id}: "
                f"{cite_id!r}"
            )


# ---------------------------------------------------------------------------
# Stub generation and merge
# ---------------------------------------------------------------------------

_PLACEHOLDER = ""
_HUMAN_FIELDS = {"description", "name", "cite_id"}
_REQUIRED_BASE = {"id", "cite_id", "lean_symbol", "source_module", "description"}
_REQUIRED_STATUS = {"theorem"}  # axioms are postulated in Lean, not proved/pending


def _make_stub(decl: LeanDecl, source_module: str) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "id": decl.name,
        "cite_id": _PLACEHOLDER,
        "name": _PLACEHOLDER,
        "lean_symbol": decl.name,
        "source_module": source_module,
        "description": _PLACEHOLDER,
    }
    if decl.section in _REQUIRED_STATUS:
        entry["status"] = "pending"
    return entry


def _merge(existing: dict, stub: dict, overwrite: bool) -> dict:
    result = dict(existing)
    for key, val in stub.items():
        if (
            key not in existing
            or overwrite
            or key in _HUMAN_FIELDS
            and existing[key] == _PLACEHOLDER
        ):
            result[key] = val
    return result


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------


def run_ref_validate(strict: bool = False) -> int:
    """Validate reference artifacts without adding any stubs.

    Returns:
        0 on success, 1 on any failure or (with strict) any warning.
    """
    repo_root = find_repo_root()
    lean_root = repo_root
    index_path = repo_root / "reference" / "index.toml"

    if not index_path.exists():
        print(f"error: reference/index.toml not found in {repo_root}")
        return 1

    try:
        index = load_toml(index_path)
    except Exception as exc:
        print(f"error: cannot parse reference/index.toml: {exc}")
        return 1

    index_surface_module = index.get("surface_module", "")

    all_registered: set[str] = set()
    for artifact in index.get("artifact", []):
        path = repo_root / artifact.get("path", "")
        if path.exists() and artifact.get("format", "toml") == "toml":
            try:
                data = load_toml(path)
                for sv in data.values():
                    if isinstance(sv, dict):
                        for e in sv.values():
                            if isinstance(e, dict) and "lean_symbol" in e:
                                all_registered.add(e["lean_symbol"])
            except Exception:  # noqa: S110
                pass
    all_ok = True

    for artifact in index.get("artifact", []):
        # dry_run=True, overwrite=False: validate only, no writes, no additions
        r = _process_artifact(
            artifact,
            repo_root,
            lean_root,
            index_surface_module,
            dry_run=True,
            overwrite=False,
            all_registered=all_registered,
        )
        has_warnings = any("warn" in m and "kind mismatch" not in m for m in r.messages)
        tag = "ok  " if r.ok else "FAIL"
        print(f"  [{tag}]  {r.artifact_id}")
        for msg in r.messages:
            if "skipped" not in msg:
                print(msg)
        if not r.ok or (strict and has_warnings):
            all_ok = False

    return 0 if all_ok else 1
