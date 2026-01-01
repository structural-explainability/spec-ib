# Interpretation Boundary Specification (IB)

Status: Normative

This document defines the normative requirements for conformance with the
Interpretation Boundary (IB).

IB is a downstream specification that conforms to Structural Explainability (SE).
All SE neutrality constraints apply.

IB constrains **how interpretation may relate to the neutral substrate**.
It does not govern interpretation itself.

## How to Read This Spec

Keywords MUST, MUST NOT, SHOULD, and MAY
are to be interpreted as described in RFC 2119.

Use of terms such as "canonical" denotes structural role only and
does not imply epistemic, causal, or normative preference.

This specification does not prescribe editorial structure,
terminology preference, or documentation layout beyond identifier semantics.

## Representation vs Constraint Classes

Some requirements describe what interpretation structures MAY be recorded,
while others constrain how interpretation MUST NOT interact with the substrate.

Overlap between these classes is intentional:
permission to record interpretation does not imply interpretive authority,
correctness, or endorsement.

## Identifier Semantics and Stability

Each requirement in this document is identified by a stable identifier
of the form `IB.*`.

Identifiers are the sole normative reference for conformance.
Textual wording MAY be clarified over time without changing meaning;
any change that alters the requirement MUST result in a new identifier.

Renaming, reordering, or relocating identifiers constitutes a semantic
change and is therefore intentionally diff-visible.

Repository paths, filenames, and section ordering are non-normative
and do not affect identifier meaning.

---

## IB.CONFORMANCE.SE.REQUIRED

Any system claiming conformance with this specification MUST also conform to
the Structural Explainability (SE) specification.

IB MUST NOT weaken, override, or reinterpret any SE neutrality constraints.

## IB.DEFINITION.CORE

Interpretation Boundary defines a structural boundary governing how
interpretive acts, claims, or frameworks may be associated with
substrate records without entering the substrate.

IB defines constraints on:

- interpretation artifacts
- interpretation actions
- the relationship between interpretation and substrate records

IB does not define interpretation semantics, correctness, authority, or enforcement.

## IB.ATTACHMENT.NON_MUTATING

Interpretation MAY be structurally attached to substrate records
only in ways that do not alter:

- identity
- structure
- recorded change
- evolution semantics

Any interpretation that modifies substrate records constitutes non-conformance.

## IB.INTERPRETATION.ADMISSIBILITY

IB MUST define the conditions under which interpretive artifacts or acts
are admissible for attachment to substrate records.

Admissibility:

- is structural only
- does not imply truth, correctness, or legitimacy
- does not require consensus or shared ontology

## IB.INTERPRETATION.PROHIBITIONS

IB MUST define behaviors and assertions that interpretations MUST NOT perform.

Prohibited behaviors include:

- asserting causal effects on substrate records
- redefining identity or persistence
- introducing implicit semantics into substrate structure
- enforcing interpretive authority through structural means

## IB.PROVENANCE

IB MUST define structural provenance for interpretive acts and artifacts.

Interpretive provenance:

- records who interpreted what, when, and under what context
- remains interpretation-neutral
- MUST NOT assert epistemic validity, correctness, or legitimacy

## IB.VERSIONING

IB MUST define versioning rules for interpretation artifacts and specifications.

Interpretation versioning:

- MUST be explicit
- MUST be stable
- MUST NOT allow silent or implicit change

## IB.SCOPE.EXCLUSIONS

This specification does not define:

- domain vocabularies
- behavioral models
- causal explanations
- epistemic evaluation
- normative judgment or enforcement
- governance, approval, or lifecycle rules
- governance semantics for versioning or dependency management
- explanation interfaces or evidence structures

These concerns are explicitly out of scope.

---

## Key Design Clarification (non-normative)

Interpretation Boundary does **not** govern interpretation.
It governs **how interpretation is prevented from contaminating the substrate**.

Governance of interpretation (approval, lifecycle, versioning) belongs to
the Governance Boundary (GB).

Interfaces for expressing interpretation belong to
Contextual Evidence and Explanation (CEE).

IB exists solely to preserve neutrality by enforcing structural separation.
