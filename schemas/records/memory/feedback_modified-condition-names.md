---
name: feedback_modified-condition-names
description: "A modified version of a condition is named with its modifier after the base name: FVAC-PF, not PF-FVAC, as GIC-Mod and GIC-Liv already are (ruled 2026-11-01)"
metadata:
  type: feedback
---

On 2026-11-01 the owner had the ontology write the perfect-foresight finite value of autarky as `fvac-pf`, not
`pf-fvac`. The rule is implicit in the other names: a modified version of a condition is indicated by a signifier for
the modification following the condition's base name, as in GIC-Mod, GIC-Liv, GIC-Szeidl and GIC-Harmenberg.

**Why:** the base name says which condition it is, and the suffix how it is modified. Names then sort and read by
condition, and a family of variants shares its prefix.

**How to apply:**
- The ontology: the condition `fvac-pf` (FVAC-PF), its factor `value-of-autarky-factor-pf`, and the results named for it.
  Identifiers are unchanged.
- The schemas' checker, the results schema, both families' `conditions.md` and BST (`\PFFVAC`) still spell it
  PF-FVAC. Changing the schemas is a schema change, to be proposed first ([[feedback_iterate-and-propose]]); the
  ontology's tests map FVAC-PF to the checker's PF-FVAC until then.
- New condition names follow the rule. A condition that is not a modification of another, such as Ma, Stachurski and
  Toda's MST-βR, is not covered by it.
