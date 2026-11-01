# The ontology of buffer-stock models, draft.2: the stage files, the two constraints, Ma, Stachurski and Toda

2026-10-31 evening to 2026-11-01. The draft is `ontologies/buffer-stock-models/`, version 0.1.0-draft.2, on branch
`buffer-stock-ontology`; its [changelog](../../../ontologies/buffer-stock-models/CHANGELOG.md) lists every row it adds or
changes. 193 rows, with 12 identifiers retired.

## What the tests establish, and what they do not

The 47 tests run with the command in the ontology's README.
- They check the ontology itself. The generated files are current, the Turtle parses, the generator refuses twelve
  deliberately broken sources, the classes form a tree, and no row names a toolkit.
- They check that it agrees with the schemas. Each parameter-file key and stage-file name it cites exists. On each type of
  bst/1's three members, its formulas give the checker's verdict for eleven conditions, and its factor for nine of them
  to 10⁻¹². The new condition MST-βR is outside the checker, and the test names it as the one exception.
- They check its algebra:
  - the five moments match the mean-one lognormal's closed forms;
  - the thirteen implications among the conditions hold on 6000 sampled parameter sets, each premise met at least 50
    times;
  - MST-βR's factor equals E[(Þ̊_𝒢/ψ)^ϱ] computed directly, and equals Þ̊_𝒢^ϱ when ψ is degenerate;
  - Þ̊_R ℛ E[ψ⁻¹] is the GIC-Mod's factor.
- **None solves a model.** Every result about a solution is recorded with its source: proved in BST, cited there, stated
  without proof, or deduced here. Among them are existence, a binding constraint, a target and a stationary
  distribution. No test checks them. Checking them would mean solving members, which belongs to the results files.

## The stage files' rewrite (#15)

Both families' stage files, rewritten with the derivative terms D_{m}V, D_{k}V[<] and D_{a}V[>] and with marginal
utility as the derivative of utility, elaborate on Bellman-SYM's current main. Their earlier versions are refused there
at the headers that declared marginal values as fields. The checker's 175 tests pass on the branch. Until #15 merges, the
ontology keeps the divergence that records the old form (`BSM_0000179`), and a test of the spellings still pending.

## The two constraints

Seventeen rows (`BSM_0000180` to `BSM_0000196`) tell the natural and the artificial constraint apart in behavior,
conditions and limits, not only in membership. That an artificial constraint binds is a deduction. As first written it
took next period's lowest resources to be R a_Art/(𝒢ψ_min) + ξ_min for any a_Art. That holds only for a borrowing limit,
a_Art ≤ 0, and the row now says so ([defects](../defects.md)).

## Ma, Stachurski and Toda in the ontology's terms

Read in the arXiv versions 1905.13045v3 (the 2020 paper) and 2012.00219v2 (the 2022 paper). Their constraint is a ≥ 0,
so the ontology states their results within a new class, `liquidity-constrained`: a ≥ 0 with a positive lowest income.
BST's remark maps the normalized problem onto theirs, with discount factor β̊(𝒢ψ′)^(1−ϱ), return R/(𝒢ψ′) and income ξ′.
Under that mapping:

| their assumption | in the ontology's terms | how it maps |
|---|---|---|
| 2.1, G_β < 1 | the FVAC | G_β = β̊ 𝒢^(1−ϱ) E[ψ^(1−ϱ)], as BST's footnote notes |
| 2.2, G_βR < 1 | MST-βR, new: β̊ R 𝒢^(−ϱ) E[ψ^(−ϱ)] < 1 | the mean of the product of discount and return, with iid shocks |
| 2.3, E[Y] < ∞ and E[u′(Y)] < ∞ | holds in the class | the lowest income is positive. With a zero-income event it fails, which is why BST's remark takes ℘ = 0 |
| 3.1, s̄ G_R < 1 with s̄ satisfying their (19) | the RIC with the GIC-Mod | (19) holds exactly for s̄ ≥ Þ̊_R, and Þ̊_R G_R = Þ̊_𝒢 E[ψ⁻¹] |

**What follows:**
- **Existence** (their Theorem 2.2): under the FVAC and MST-βR, a unique optimal policy in their candidate class. Time
  iteration converges to it from any policy in that class, and the last period's rule c = m is one of them. So the
  finite-horizon consumption functions converge to it, and the limiting solution is non-degenerate. That last step is
  deduced here. Neither the RIC nor the WRIC is needed.
- **A lower bound on consumption:** with the RIC, their s̄ is Þ̊_R, and their Proposition 2.6 gives c(m) ≥ (1 − Þ̊_R) m.
- **A stationary distribution** (their Theorem 3.1): under the FVAC, MST-βR and the RIC. Their households do not die, so
  a population that replaces its dead is not covered.
- **MST-βR implies the GIC-Mod**, by Jensen's inequality with ϱ > 1. The tests check this on sampled models.
- **MST-βR is sufficient, not necessary.** The 2022 paper needs no condition on the return under a constant discount
  factor below one, utility bounded above and inf E u(income) > −∞. The normalized problem has a constant discount
  factor only when ψ is degenerate at one, and then MST-βR is the GIC. So without permanent shocks an optimal policy
  exists whether or not the GIC holds. That paper does not show that the consumption functions converge, so the row
  concludes no property.

**What this does not establish:**
- **A continuous ψ.** Their model gives the discount factor, the return and income separate innovations, while the
  normalized problem's discount factor and return share ψ′. That fits exactly when ψ has finite support, by taking ψ as
  their Markov state. For a continuous law of ψ it rests on their proofs not needing the separation, which has not
  been checked.
- **Random discounting in the 2022 approach.** Their footnote calls the extension straightforward but does not give it,
  so with permanent shocks the 2022 result is not established for the normalized problem.
- **Other constraints.** Nothing is stated for a borrowing limit strictly between the natural one and zero, nor for
  ℘ > 0 with a positive benefit and a ≥ 0. That case meets their income assumption, but its natural limit relative to
  zero has not been worked out.
- **Necessity of the FVAC.** Their necessity result for the discount condition assumes positive utility, which ϱ > 1
  rules out.

## No toolkit in the ontology

On the owner's ruling of 09:23:51, the ontology lost:
- 48 HARK names: 3 of classes, 19 of objects, 13 of quantities, 11 of conditions and 2 of properties;
- HARK's source pin and the HARK sources of three rows;
- the realization role of a format;
- the approximation kind of a divergence.

HARK's ten departures from its terms (`BSM_0000138` to `140`, `144`, `154` to `159`) are retired there and kept in
[HARK's stone](../../rosetta/hark.md#the-ontologys-terms-in-hark) with their sources at HARK's `4c285e86`.

Three HAFiscal divergences stay, each a use of a term in the HAFiscal paper. The fourth, about its code's cap on β, is
retired. By the owner's ruling of 10:18:27, the cap is an implementation detail that keeps parameters away from the
boundary, where the solution slows drastically. The public package's comments explain it otherwise. At HAFiscal-QE
`1afdf80`, `Code/HA-Models/FromPandemicCode/EstimParameters.py` lines 392–440:
- call the bound "the BST-textbook condition that is necessary and sufficient for a stationary distribution of
  normalized assets to exist";
- say the growth patience factor "must stay below 1";
- explain the margin 0.9995 by a fit to College's wealth concentration.

None says the cap guards against slow solutions near the boundary.
