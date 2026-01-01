# Interpretation Boundary Identifiers (IB)

This document defines the stable requirement identifiers used by the
Interpretation Boundary (IB) specification.

Identifiers are the sole normative reference mechanism.
Section ordering, formatting, and presentation are non-normative.

## Overview

Defines the stable set of identifiers.

## Identifier Semantics and Ordering

Identifiers are the sole normative reference mechanism.
Section ordering, formatting, and presentation are non-normative.

Identifiers are listed in strict alphabetical order to remove
editorial discretion and ensure deterministic placement.

## Identifier Naming Rules

All identifiers follow this pattern:

IB.<CATEGORY>.<SUBCATEGORY>.<QUALIFIER>

Identifiers are:

- semantic, not positional
- stable across versions
- reusable across prose, code, and formal proofs
- language-agnostic
- suitable for direct mapping to Lean theorem names

Identifiers MUST NOT be renamed or repurposed.
New identifiers MAY be added only in a new major version of this document.

## Identifier Notes

Each identifier MUST be followed by exactly one note.

- The note MUST be expressed as a single bullet.
- The bullet text MAY wrap across lines.
- No additional bullets, sublists, or structural markers are permitted.
- Notes are explanatory only and do not introduce additional requirements.

## Canonical Identifier List (Alphabetical, with Notes)

IB.ATTACHMENT.NON_MUTATING

- Requires that interpretation may attach to substrate records only in ways that do not alter identity, structure, or recorded change.

IB.CONFORMANCE.SE.REQUIRED

- States that Interpretation Boundary conforms to the Structural Explainability specification and preserves all neutrality constraints.

IB.DEFINITION.CORE

- Defines Interpretation Boundary as a structural specification constraining how interpretation may relate to the neutral substrate without entering it.

IB.INTERPRETATION.ADMISSIBILITY

- Defines the conditions under which an interpretive act or framework may be structurally attached to substrate records.

IB.INTERPRETATION.PROHIBITIONS

- Defines assertions and behaviors that interpretations MUST NOT perform with respect to substrate identity, structure, or evolution.

IB.PROVENANCE

- Defines structural provenance for interpretive acts without asserting correctness, validity, or authority.

IB.VERSIONING

- Defines explicit versioning requirements for interpretation artifacts so they remain stably referenceable over time without silent change.

IB.SCOPE.EXCLUSIONS

- Defines what Interpretation Boundary explicitly does not specify.

## Cross-Artifact Consistency Rule

Each identifier in this list MUST appear:

- exactly once in SPEC.md
- exactly once in CONFORMANCE.md
- exactly once as a field in the Lean `ConformanceEvidence` structure
- exactly once in the Lean requirements list

Alphabetical order SHOULD be preserved across all artifacts.
