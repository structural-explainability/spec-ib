# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this specification are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.9.1] – 2026-05-15

### Added

- Python validation and export utilities for GB specification consistency checks.
- Generated `data/spec/` artifacts for requirements, conformance checks, and scope exclusions.
- Tests for identifier extraction, specification coverage, conformance coverage,
  and generated export consistency.
- Shared command entry points for validation, reference export, reference validation,
  and manifest version synchronization.

### Changed

- Aligned manifest version synchronization with `se-manifest-schema`.
- Tightened IB metadata and validation workflow for downstream contract consumption.

---

## [0.9.0] – 2025-12-31

### Added

- Initial normative specification.
- Stable requirement identifiers.
- Conformance checklist.
- Repository structure, citation metadata, and licensing.

---

## Notes on Versioning and Releases

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

- **MAJOR** versions indicate breaking changes to normative requirements,
  identifiers, or conformance criteria.
- **MINOR** versions indicate backward-compatible additions or clarifications.
- **PATCH** versions indicate editorial fixes, documentation updates, or
  non-normative changes.

Versions are defined by git tags of the form `vX.Y.Z`.
Tagged releases are the authoritative source of version state.

Documentation and badges, where present, should reference the latest tagged
release.

## Release Procedure (Required)

Follow these steps exactly when creating a new release.

### Task 1. Update release metadata (manual edits)

1.1. `CITATION.cff` - update `version` and `date-released`
1.2. CHANGELOG.md: add section, move unreleased entries, update links
1.3. `pyproject.toml` - update `fallback-version` near end of file

### Task 2. Validate

```shell
uv sync --extra dev --extra docs --upgrade

uv run se-validate
uv run se-ref-export
uv run se-ref-export --check
uv run se-ref-validate
uv run se-validate --strict

git add -A
uvx pre-commit run --all-files
uv run python -m pyright
uv run python -m pytest
git add -A
uvx pre-commit run --all-files
```

### Task 4. Commit, tag, push

```shell
git add -A
git commit -m "Prep X.Y.Z"
git push -u origin main
```

Verify actions run on GitHub. After success:

```shell
git tag vX.Y.Z -m "X.Y.Z"
git push origin vX.Y.Z
```

### Task 5. Verify tag consistency

```shell
uv run python -m se_manifest_schema validate --strict --require-tag
```

Confirms CITATION.cff version matches the pushed git tag.
Run this after `git push origin vX.Y.Z`; it will fail before that point.

## Only As Needed (delete a tag)

```shell
git tag -d vX.Z.Y
git push origin :refs/tags/vX.Z.Y
```

## Links

[Unreleased]: https://github.com/structural-explainability/spec-ib/compare/v0.9.1...HEAD
[0.9.1]: https://github.com/structural-explainability/spec-ib/releases/tag/v0.9.1
[0.9.0]: https://github.com/structural-explainability/spec-ib/releases/tag/v0.9.0
