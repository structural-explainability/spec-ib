# Interpretation Boundary Specification (IB)

[![Repo](https://img.shields.io/badge/repo-GitHub-black?logo=github)](https://github.com/structural-explainability/spec-ib)
[![Tooling](https://img.shields.io/badge/python-3.15%2B-blue?logo=python)](./pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)

[![CI](https://github.com/structural-explainability/spec-ib/actions/workflows/ci-python.yml/badge.svg?branch=main)](https://github.com/structural-explainability/spec-ib/actions/workflows/ci-python.yml)
[![Links](https://github.com/structural-explainability/spec-ib/actions/workflows/links.yml/badge.svg?branch=main)](https://github.com/structural-explainability/spec-ib/actions/workflows/links.yml)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-brightgreen.svg)](https://github.com/structural-explainability/spec-ib/security)

> Authoritative specification of Interpretation Boundary (IB).

GB and IB are normative boundary specifications that protect the stack
and govern how downstream layers may use it.

## Overview

The Interpretation Boundary (IB) specification defines how
external frameworks, meanings, theories, domains, or explanatory commitments
may attach to SE outputs without leaking back into the neutral substrate.

IB is a downstream specification that conforms to Structural Explainability (SE).
All SE neutrality constraints apply.

IB protects the core from interpretive capture.

IB answers questions like:

- Where may a domain framework interpret a structural result?
- What must remain outside the neutral substrate?
- How do we prevent explanation from becoming ontology?
- How do we keep causal, legal, ethical, or policy claims external?

IB introduces no epistemic, causal, or normative commitments.
IB records interpretation structure only, not interpretation outcomes.

## Purpose

The purpose of IB is to specify what interpretation-level structures
may be represented so that coordination, traceability, and accountability
are possible without altering the neutral substrate.

IB defines constraints on:

- interpretation artifacts (e.g., specifications, adapters, profiles, appendices)
- interpretive attachment records over artifacts (e.g., attachment, reference, qualification, supersession)
- the relationship between interpretation and substrate records

IB does not define meaning, enforcement, or correctness of interpretive attachment records.

IB protects the neutral substrate and downstream structural artifacts from a specific failure mode:

- Interpretive, causal, normative, legal, ethical, or domain-specific meaning
   being treated as if it were part of the neutral substrate.

## Versioning and Stability

IB v1 defines a closed set of interpretation structures for the purpose of conformance.

For IB v1:

- interpretation artifacts are structurally constrained as specified by IB requirement identifiers

Closure applies to structural shape only and does not assert institutional finality.

## Extension Policy

Extension is explicitly permitted only under a new
version of the specification.

Any extension MUST:

- preserve conformance with Structural Explainability
- introduce explicit structural definitions and constraints via new identifiers
- demonstrate non-overlap with existing structures
- remain neutral with respect to epistemic, causal, and normative interpretation

Extensions are expected to be rare and explicitly justified.

## Scope

This specification defines:

- structural interpretation artifacts
- adapter identity, scope, and compatibility claims
- canonical encoding requirements
- structural dependency graphs among interpretation artifacts
- interpretive attachment records over artifacts
- structural provenance for interpretation lifecycle events
- versioning rules for interpretation artifacts and specifications

This specification does NOT define:

- domain vocabularies
- behavioral models
- causal explanations
- epistemic evaluation
- normative judgment or enforcement
- exchange or interaction mechanisms
- explanation or attestation overlay systems
- neutral substrate identity or persistence rules
- graph evolution semantics

These concerns are explicitly out of scope.

## Relationship to Other Work

- IB **conforms to** the Structural Explainability Specification.
- IB operates downstream of neutral substrate specifications but does not depend on their internal semantics.
- IB provides structural guardrails under which interpretation artifacts may
  attach to the neutral substrate without modifying it.
- Interpretation, evaluation, and enforcement remain external.

## Repository Contents

- [SPEC.md](./SPEC.md) - Normative specification
- [IDENTIFIERS.md](./IDENTIFIERS.md) - Stable requirement identifiers
- [CONFORMANCE.md](./CONFORMANCE.md) - Conformance checklist
- [ANNOTATIONS.md](./ANNOTATIONS.md) - Annotation standards
- [LICENSE](./LICENSE) - licensing terms
- [CITATION.cff](./CITATION.cff) - Citation metadata
- [CHANGELOG.md](./CHANGELOG.md) - Version history

## Clarifying Statement

Interpretation Boundary defines structural interpretation, not interpretation outcomes.

An interpretation artifact or action recorded under IB specifies
how interpretation information is structured, not whether
it is valid, correct, legitimate, authoritative, or enforced in any context.

IB exists so that interpretation structure can remain stable
across reinterpretation, disagreement, and changing interpretive or institutional frameworks.

## Command Reference

<details>
<summary>Show command reference</summary>

### In a machine terminal

Open a machine terminal where you want the project:

```shell
git clone https://github.com/structural-explainability/spec-ib

cd spec-ib
code .
```

### In a VS Code terminal

```shell
uv self update
uv python pin 3.15
uv sync --extra dev --extra docs --upgrade

# install git hooks once per clone
uvx pre-commit install

# generate/check registry artifacts
uv run se-validate
uv run se-ref-export
uv run se-ref-export --check
uv run se-ref-validate
uv run se-validate --strict

# autofix and manual fix issues
git add -A
uvx pre-commit run --all-files
# repeat if changes were made
git add -A
uvx pre-commit run --all-files

# do chores
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build

# save progress
git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Citation

[CITATION.cff](./CITATION.cff)

## License

[MIT](./LICENSE)

## Manifest

[SE_MANIFEST.toml](./SE_MANIFEST.toml)
