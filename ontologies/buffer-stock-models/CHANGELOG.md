# Changelog

Each entry says whether a change alters a class (its axioms), a term's meaning (a definition or a formula), a written
form, or only labels and text.

## 0.1.0-draft.2 (unreleased)

The ontology stated in Bellman-SYM's terms, after a consultation with the bellman session and Matsya on 2026-10-31. By
the owner's instruction of 2026-11-01, it names no toolkit.

**New terms.** Rows `BSM_0000160` to `BSM_0000205`:
- the three perches, the stage and the trellis;
- the arrival and continuation values;
- the three derivative terms of the values;
- the end-of-period value and its marginal value;
- the arrival and decision laws of motion and the connector;
- the backward stage operator and the forward distribution operator;
- the feasible set;
- two divergences: 𝕄 in two senses, and the schemas' stage files still writing a retired role word;
- the natural and the artificial constraint: the constrained perfect-foresight benchmark and its axiom; four
  properties, among them that the constraint in force binds; and eleven results:
  - the constrained benchmark's taxonomy, and a vanishing MPC without the RIC;
  - the natural constraint never binding, and an artificial one binding (deduced);
  - the WRIC needing no artificial constraint (stated);
  - the problem with ℘ = 0 as a case of Ma, Stachurski and Toda, and the compact feasible set;
  - among the conditions alone, that the RIC without the GIC means finite human wealth;
- Ma, Stachurski and Toda's conditions:
  - the liquidity-constrained class, a ≥ 0 with a positive lowest income, and its axiom;
  - the moment E[ψ^(−ϱ)], the discounted-return factor and their condition, MST-βR;
  - four results: existence under the FVAC and MST-βR; a stationary distribution, adding the RIC; MST-βR implying
    the GIC-Mod, tested on sampled models; and, from their 2022 paper, existence with no condition on the return when
    there are no permanent shocks.

**Meanings changed.**
- The value function is the decision value, `value-decision`.
- The consumption function is the policy.
- The dynamic budget constraint is a law of motion, the composite of the decision law, the connector and the next
  period's arrival law.
- The Euler equation is a relation, and its clause covers the natural constraint too.
- The expectation and the cross-sectional mean are operations.
- BST's T is related to the stage operator.
- The life-cycle class binds each primitive to the stage occurrence that reads it.
- The bounds are properties of the laws.
- The unemployment and survival events are shocks on two-point sets; the category of event is removed.
- The measures' perches are stated, and the income measure is a second forward problem.
- The constrained perfect-foresight results are stated within the new constrained benchmark. That benchmark, and the
  paper's limit as ℘ ↓ 0, are limits of the liquidity-constrained class.
- The WRIC's necessity without an artificial constraint is treated as true until the paper proves it, by the owner's
  decision of 2026-11-01.
- The deduction that an artificial constraint binds is stated for a borrowing limit, a_Art ≤ 0.

**Written forms.**
- The ontology names no toolkit. HARK's names for the terms, its sources and its ten divergences moved to HARK's Rosetta
  Stone in the schemas, among them the cyclical index, with the owner's ruling of 2026-10-31 that the solver and the
  simulation are to be consistent. Their identifiers are retired. The realization role and the approximation kind of divergence are
  removed.
- Each format has a role: notation or calibration.
- Objects carry their perch, their state, the set a state takes values in, and Bellman-SYM's concept where it has one.
- A result can name the class its limit lies in (`limit_in`), and a benchmark can be a subclass of another class.
- Every divergence has a kind: meaning, notation, convention or absence.
- Two papers are sources, cited by their own numbering: Ma, Stachurski and Toda (2020) and (2022), in their arXiv
  versions. A condition's short name may carry Greek letters.

47 tests.

## 0.1.0-draft.1 (unreleased)

The first draft, with rows `BSM_0000001` to `BSM_0000159`, of which `BSM_0000151`, a divergence withdrawn on checking,
is retired. The design: the eleven kinds; membership axioms and hypotheses as two tiers; buffer-stock saving as a
property of the solution; the perfect-foresight model as the class's benchmark, outside it; formulas in the ontology of
probability distributions' syntax; written forms in five formats; and citations pinned to BST's published page,
econ-ark's registry 8.0.0, HARK at `4c285e86` and HAFiscal-QE at `1afdf80`.

The rows:
- **classes:** the class, BST's own, the benchmark, and nine extensions;
- **axioms:** seven membership axioms of the class, the owner's ruling of 2026-10-31 on the atom at the worst
  transitory shock among them; seven hypotheses of BST's class; and the benchmark's one;
- **terms:** forty objects, the four moments of the permanent shock, and sixteen quantities;
- **conditions and results:** eleven conditions, twelve properties, and twenty-five results, eleven of them
  implications among the conditions;
- **identities, families and divergences:** seven identities, the schemas' two families, and fourteen divergences, ten
  in HARK and four in the published HAFiscal paper and code.
