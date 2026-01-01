# Conformance Checklist

This document defines the criteria for determining whether an artifact
conforms to the Interpretation Boundary (IB) specification.

Identifiers referenced in this document are the sole normative reference.
Section ordering, formatting, and presentation are non-normative.

An artifact may be a specification, schema, implementation, repository,
or other deliverable claiming conformance.

## Conformance Overview

An artifact CONFORMS if and only if:

- all mandatory requirements are satisfied
- no prohibited assertions are present
- conformance with Structural Explainability (SE) is preserved

Failure of any single check constitutes non-conformance.

---

## IB.CONFORMANCE.SE.REQUIRED

- [ ] The artifact explicitly claims conformance with Structural Explainability.
- [ ] No requirement weakens or contradicts SE neutrality constraints.
- Fail if: conformance is asserted without explicit SE conformance.

## IB.DEFINITION.CORE

- [ ] The artifact defines interpretation artifacts and interpretation actions as structural constructs.
- [ ] The artifact limits scope to interpretation boundary constraints only.
- Fail if: interpretation semantics, authority, or enforcement are defined.

## IB.ATTACHMENT.NON_MUTATING

- [ ] Interpretation artifacts are attachable only without mutating substrate identity, structure, or change.
- [ ] No interpretation alters recorded evolution or persistence rules.
- Fail if: interpretation modifies substrate records.

## IB.INTERPRETATION.ADMISSIBILITY

- [ ] Conditions for admissible interpretation attachment are structurally defined.
- [ ] Admissibility does not imply correctness, legitimacy, or authority.
- Fail if: admissibility implies evaluative or epistemic judgment.

## IB.INTERPRETATION.PROHIBITIONS

- [ ] Prohibited interpretive behaviors are explicitly constrained.
- [ ] Interpretation does not redefine identity, causality, or authority.
- Fail if: interpretation leaks semantics into substrate structure.

## IB.PROVENANCE

- [ ] Structural provenance for interpretation actions is recorded.
- [ ] Provenance records attribution and process structure only.
- Fail if: provenance asserts truth, correctness, or legitimacy.

## IB.VERSIONING

- [ ] Interpretation artifacts include explicit version identifiers.
- [ ] Versioning rules for interpretation artifacts are structural and deterministic.
- Fail if: versioning is implicit, informal, or interpretation-dependent.

## IB.SCOPE.EXCLUSIONS

Verify that the artifact does not define:

- [ ] domain vocabularies
- [ ] behavioral models
- [ ] causal explanations
- [ ] epistemic evaluation
- [ ] normative judgment or enforcement
- [ ] governance, approval, or lifecycle rules
- [ ] governance semantics for versioning or dependency management
- [ ] explanation or evidence interfaces

Presence of any of the above constitutes non-conformance.

---

## Final Determination

An artifact CONFORMS if:

- all checks above pass, and
- no prohibited assertions are present.

Otherwise, the artifact is NON-CONFORMANT.

## Conformance Declaration

Artifacts claiming conformance SHOULD include a declaration of the form:

```text
Conforms to: IB Specification vx.y
Conforms to: SE Specification vx.y
```
