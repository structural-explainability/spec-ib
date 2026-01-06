# Interpretation Boundary Specification (IB)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/license/MIT)
![Build Status](https://github.com/structural-explainability/spec-ib/actions/workflows/ci-hygiene.yml/badge.svg?branch=main)
[![Check Links](https://github.com/structural-explainability/spec-ib/actions/workflows/links.yml/badge.svg)](https://github.com/structural-explainability/spec-ib/actions/workflows/links.yml)

> Authoritative specification of Interpretation Boundary (IB).

## Overview

The Interpretation Boundary (IB) specification defines the structural requirements
for representing interpretation artifacts and actions whose identity, scope,
and traceability must remain explicit and stable under reinterpretation.

IB is a downstream specification that conforms to Structural Explainability (SE).
All SE neutrality constraints apply.

IB introduces no epistemic, causal, or normative commitments.
IB records interpretation structure only, not interpretation outcomes.

## Purpose

The purpose of IB is to specify what interpretation-level structures
may be represented so that coordination, traceability, and accountability
are possible without altering the neutral substrate.

IB defines constraints on:

- interpretation artifacts (e.g., specifications, adapters, profiles, appendices)
- interpretation actions over artifacts (e.g., attachment, reference, qualification, supersession)
- versioning, dependency, and provenance structures

IB does not define meaning, enforcement, or correctness of interpretation actions.

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
- interpretation actions over artifacts
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
- IB provides structural guardrails under which interpretation artifacts may attach to the neutral substrate without modifying it.
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

## Developer (running pre-commit)

Steps to run pre-commit locally. Install `uv`.

Initialize once:

```shell
uv self update
uvx pre-commit install
uvx pre-commit run --all-files
```

Save progress as needed:

```shell
git add -A
# If pre-commit makes changes, re-run `git add -A` before committing.
git commit -m "update"
git push -u origin main
```
