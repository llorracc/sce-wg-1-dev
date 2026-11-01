# The ontology of buffer-stock models: its first draft, and what it found

2026-10-31. The draft is `ontologies/buffer-stock-models/`, version 0.1.0-draft.1, on branch `buffer-stock-ontology`.

**Update of 2026-11-01.** HARK's divergences below moved out of the ontology to
[HARK's Rosetta Stone](../../rosetta/hark.md#the-ontologys-terms-in-hark), since the ontology names no toolkit. The owner's
ruling on the cyclical index is that the solver and the simulation be consistent, not that the solver is right
([the rulings of 2026-11-01](../rulings/2026-11-01_ontology-decisions.md)). Draft.2's findings are
[their own](2026-11-01_ontology-draft2.md).

## What the tests establish

The 36 tests run with the command in the ontology's README.
- **The ontology agrees with the checker.** The ontology's own formulas reproduce the checker's verdict for each of its
  eleven conditions. They reproduce its factor for each of the nine plain ones, to 10⁻¹². This holds for every type of
  bst/1's three members (`library`, `toy`, `toy-untruncated`).
- **The implications hold.** All eleven implications among the conditions hold on 6,000 sampled models, each premise met
  at least 50 times. A third of the models have a mean-one lognormal ψ by Gauss–Hermite; the rest have random mean-one
  discrete laws of one to five atoms; ϱ is drawn from 1.01 to 8.
- **The conditions stay distinct.** Models are found that satisfy each weaker condition and fail the stronger one:
  GIC but not GIC-Szeidl, GIC-Szeidl but not GIC-Mod, WRIC but not RIC, GIC-Harmenberg but not GIC, and GIC-Liv but not
  GIC.
- **The moments agree with the closed forms.** The moments' formulas match the mean-one lognormal's closed forms.
- **The axioms classify the members.** `library` is a member and meets every hypothesis of BST's class. `toy` is a
  member, its artificial constraint above the natural one. `toy-untruncated` is not a member: it sits at the edge, and its
  lowest transitory shock has no atom.
- **The written forms exist.** Every parameter-file key the ontology names is in bst/1's validator, and every stage-file
  name is in the stage file.
- **The generator refuses broken sources:** a dangling reference, an undefined symbol, an unpinned anchor or registry
  key, a repeated identifier, an unknown parent class, a law that is not a row of the probability distributions, and an
  expectation outside a moment.

**What they do not establish.**
- They prove no theorem. An implication holding on samples is evidence; BST's proofs, or a deduction recorded in the
  row, carry the claim.
- The properties (a target exists, a distribution is invariant) are not computed; they are tied to conditions only by
  the results' sources.
- The HARK names are not checked by a test. They were read at `4c285e86` when written.

## What the consultations found

**In HARK, main at `4c285e86`** (the HARK and HARK-dev sessions, checked against the source where cited):
- the targets are `mNrmTrg` and `mNrmStE`; only the GIC is tested before either is computed;
- HARK's Þ includes survival, so `APFac` is Þ̊;
- the PF-FVAC's message omits the ℒ its factor carries, and VAFac omits it altogether;
- the WRIC's message drops the power 1/ϱ;
- two objects are named `hNrm`, with and without this period's income;
- `WorstPrb` and the natural limit are taken over the discretized atoms;
- the message on a failing RIC states the FHWC's failure without the FVAC, and for ϱ < 1 as well, where even the FVAC
  does not make it true;
- the log target m̃ that BST says Econ-ARK computes is not computed;
- Blanchard's annuity is in `AggShockConsumerType`, and only there.

None of these has been filed as a HARK issue.

**HARK's time-varying lists in a cyclical model.** In every model, the solution for period t takes the expectation over
the move from t to t+1, with the rule of t+1. A life-cycle model's solver passes entry t, so entry k is the move out of
k. A cyclical model's passes entry t+1, so entry k is the move into k. The simulation reads entry s − 1 on entering s in
both.

The cyclical order arrived with commit `54083db5` of 2021-07-09 (issue #1022, pull request #1039). That commit moved the
simulation of death to match, and rotated the four-period example's growth so its solution stayed the same. It left the
simulation's shocks, growth and return as they were, so the example's simulated growth moved by a period. The
ontology records this without a verdict on which side should change.

**In the published HAFiscal paper and code** (HAFiscal-QE at `1afdf80`):
- ξ names the employed draw, BST's θ;
- "target" names a data moment, and "MPC" the share of a windfall spent within a year;
- the cap on β bounds ℒ (Rβ)^(1/ϱ) E[ψ⁻¹]/𝒢, with survival outside the patience factor. The ontology's GIC-Mod puts it
  inside, and the GIC-Liv as ruled is ℒ Þ̊_𝒢.

The cap replaced an earlier formula, which the session's first citations came from; those were in a checkout on no
remote branch.

**In BST's text.** Its mortality-adjusted condition does not say whether Þ carries survival. The owner's registry ruling
of 2026-10-22 settles the ontology's reading: ℒ Þ̊_𝒢. The published page lacks passages the paper's working copy has,
such as the converse of Szeidl's theorem and the table of which condition governs which phenomenon.

## Pending

- The owner's rulings on the draft's open questions ([the rulings](../rulings/2026-10-31_ontology-decisions.md)).
- The proposals for the schemas: the ontology's identifiers on the schemas' keys, and the atom axiom as a bst/1 validity
  condition.
- The Markov family's conditions, which are conditions on matrices, and the risky asset's, in the ontology.
- A test that HARK's names exist at the pinned commit.
- The pinned anchors refreshed when BST's published page is rebuilt.
