# The borrowing-constraint scenarios: one schema and one stage file each

**Status: APPROVED, 2026-11-01 at 12:50:56 EST, with the decisions at the end; APPLIED the same afternoon**, committed on
the branch `buffer-stock-ontology`: the six families, their stage files, the checker, the adapter, the
stones and the ontology ([the findings](records/findings/2026-11-01_constraint-scenarios-applied.md)). The owner asked for the
schemas and the ontology to state every configuration of a valid buffer-stock model, with a separate stage file for
each. This proposal is drawn up with the BST, HARK, HARK-dev and HAFiscal sessions, and their answers are attributed
below. Its decisions are listed at the end.

**Since 2026-11-01, 13:38 EST, two scenarios are principal:** the natural one with a point mass and the artificial one.
Their folders stay where they were; the other two scenarios' folders in `bst/` moved to `other/` (the owner's ruling, in
[`bst/model.md`](bst/model.md)). Every buffer-stock family, stage file and check below still stands.

**Since later that afternoon, the Markov family has one version, the artificial one.** HAFiscal's code never solved the
zero-infima scenario: its published package solves on atoms with positive floors under a ≥ 0. The zero-infima version, its
stage file and calibrations are retired, and `paper-published` and `paper-one-group` state the code's atoms in the
artificial version (the owner's ruling; [`bst-markov_ui-and-agg/model.md`](bst-markov_ui-and-agg/model.md)). What the
HAFiscal paragraph below says of the paper's members is superseded.

## What separates the scenarios

Two facts about the true laws decide where a member falls, never facts about a discretization:
- **hNrmMin**, the minimum present value of future noncapital income, as a ratio to permanent income. It is h_min =
  ξ_min𝒢ψ_min/(R − 𝒢ψ_min), where ξ_min is the worst transitory income (the unemployment event's income included) and
  ψ_min the permanent shock's infimum. It is strictly positive only if ξ_min > 0, ψ_min > 0 and 𝒢ψ_min < R. If ψ_min is
  zero, next period's permanent income can be arbitrarily small, and h_min = 0 whatever ξ_min is (the HARK session).
- **Whether the joint worst income is a point mass**: whether the event that ξ and ψ are both at their infima has
  positive probability, p_worst > 0. With ξ_min = 0, ψ is irrelevant. With ξ_min > 0 and a continuous ψ at ψ_min, a
  point mass in ξ alone gives p_worst = 0 (the BST and HARK sessions). HARK's `WorstIncPrb` is this joint probability.

Then the constraint in force is the natural one, a > −h_min, unless an artificial one, a ≥ a_Art, is tighter.

**Reaching the limit.** No agent ever ends a period below the constraint in force: borrowing past the natural limit
could leave consumption negative after a run of worst incomes, so it is infeasible. What differs between the scenarios
is whether an agent ever chooses to end a period exactly at the limit, a = a_min, consuming c = m − a_min. That happens
when the expected marginal value of the last unit saved stays finite at a_min, so that the optimum can sit on the
boundary. "The constraint binds" means this, here and in the families' documents.

**Why the threshold is ϱ < k.** Save exactly a_min. Next period's resources then exceed their floor by an amount s,
which is small only if every shock that has a density near its floor lands near it. With one such shock, P(s < x) ∝ x
and k = 1; with two, s is the sum of two small gaps, P(s < x) ∝ x², and k = 2. Near the floor consumption is of the
order of s, so the expected marginal utility is like ∫ s^(−ϱ) d(s^k), finite exactly when ϱ < k. k belongs to the
model's laws, so each model has one threshold. Since the class requires ϱ > 1, a model whose laws give k = 1 never
reaches its limit, and one with k = 2 does only when 1 < ϱ < 2.

## The scenarios

| | natural, with a point mass | natural, without one | artificial | zero infima |
|---|---|---|---|---|
| constraint in force | a > −h_min, h_min ≥ 0 | a > −h_min, h_min > 0 | a ≥ a_Art > −h_min, h_min > 0 | a ≥ 0, the natural constraint, which an artificial one at 0 would only repeat |
| the laws | ψ in [ψ_min, ψ_max] and θ in [θ_min, θ_max], all four bounds positive and finite | the same | ψ_min > 0 and ξ_min > 0; no upper bounds needed | ψ_min · θ_min = 0 |
| joint worst income | a point mass, p_worst > 0 | probability zero | either | no point mass at zero income, since E[ξ^(−ϱ)] < ∞ |
| does anyone end a period at the limit itself? | never, at any ϱ; the MPC at the floor tends to 1 − p_worst^(1/ϱ) Þ̊_R | only if ϱ < k, where k = 2 when both shocks have densities at their floors and k = 1 when one does; with ϱ > 1, only k = 2 and ϱ < 2 | yes, on an interval above a_Art, at every ϱ | yes, at every ϱ, when E[θ^(−ϱ)] < ∞ and, if ψ_min = 0, E[ψ^(−ϱ)] < ∞ |
| a mass at the floor | none | none when ϱ > k | if the binding region reaches the lowest attainable m (a matter of calibration) | yes |
| the Euler equation | equality everywhere | Kuhn–Tucker | Kuhn–Tucker | Kuhn–Tucker |
| existence | BST's theorem for its own case (℘ > 0, ξ_u = 0): WRIC and FVAC. Otherwise conjectured, not proved: FVAC, the WRIC with p_worst, and 𝒢ψ_min < R | no theorem | at a_Art = 0: Ma, Stachurski and Toda, FVAC and MST-βR; between −h_min and 0, none stated | Ma, Stachurski and Toda: FVAC, MST-βR and E[ξ^(−ϱ)] < ∞; exact in their framework for a finite-valued ψ, unchecked for a continuous one |
| examples | BST's own model, with h_min = 0; a positive benefit with a discrete ψ; all-discrete laws | a positive benefit with continuous truncated laws and no artificial constraint | `toy`; HAFiscal with laws truncated as `iid-ui-artificial` has them | Ma, Stachurski and Toda's and QuantEcon's lognormal model with a ≥ 0; `toy-untruncated`; HAFiscal's published model, by its stated laws |

Sources: BST's assumption on the shocks and its existence theorem; Ma, Stachurski and Toda (2020), Theorem 2.2 and Lemma
C.2. The thresholds in k come from the BST session's derivation of 2026-10-18, run for one density and not for two. The
binding rules for the zero-infima scenario follow from the Euler equation at a = 0 (the BST and HARK-dev sessions); they
have not been run.

**The scenario that is not one.** Untruncated laws with a zero-income event, `library` as written, fit none of the four.
The laws are unbounded, so it is not natural, and E[ξ^(−ϱ)] = ∞, so a ≥ 0 never binds and it is not the zero-infima
scenario either.

**HAFiscal** (the HAFiscal session). Its published paper states lognormal shocks with no bounds and a ≥ 0, so by its law
it is in the zero-infima scenario. Its published code solves on HARK's seven equiprobable atoms of each law, whose
minima are positive, so it computes the model as if it were in the artificial scenario. Its members in the Markov family
follow: `paper-published` and `paper-one-group` in the zero-infima scenario, `toy-as-hafiscal` in the artificial one.

## The stage files

One for each scenario, in each family that has members there. The parameters follow all four sessions' advice:
- **No stage file carries a_Nat or h_min as a parameter.** A separately carried value is how a discretization's lowest
  atom gets in (the BST session). Each file states its laws, with their bounds and point masses. h_min is a definition
  from those, 𝒢 and R: zero in BST's own case and in the zero-infima scenario, and ξ_min𝒢ψ_min/(R − 𝒢ψ_min) otherwise.
- **The artificial file carries a_Art; the zero-infima file does not,** since a ≥ 0 is its natural constraint and the
  schemas allow one written form (the owner's decision).
- **The laws each file states:**
  - natural, with a point mass: `TruncatedLogNormal` for ψ and θ, and the unemployment event with ℘ > 0. With ξ_u = 0
    that is BST's own model. A positive benefit needs a discrete ψ for the point mass, so it would need a second file.
  - natural, without one: `TruncatedLogNormal` for ψ and θ, ξ_u > 0, and no artificial constraint;
  - artificial: `TruncatedLogNormal`;
  - zero infima: `LogNormal`.
- **The one-period relaxation is method, not stage** (the HARK, HARK-dev and BST sessions). HARK computes, in every
  solver, c(m) = min(c̃(m), m − a_min), where c̃ is consumption with this period's artificial constraint lifted down to
  what next period's worst income can repay, (a_min,t+1 − θ_min)𝒢ψ_min/R. That is one period's natural limit, not
  −h_min. The min is exact for the problem. Numerically, the kink is exact only when a_Art is a grid point. The method
  file and the Rosetta Stones carry it.

## What changes downstream

- **The families.** `bst/1` gives way to one family for each scenario. The Markov family needs the artificial and the
  zero-infima scenarios for its present members.
- **The members:**
  - `library` fits no scenario as written: truncate its laws, which makes it BST's own model in the natural scenario
    with a point mass, or retire it. QuantEcon's community library uses it as a calibration.
  - `toy` is artificial, and `toy-untruncated` is zero-infima.
  - Every member's family key and hash change, and every results file written for the old hashes is stale.
- **The checker** checks each scenario's requirements: the bounds, the joint point mass, h_min > 0 where required, and
  the binding conditions. Each family's `conditions.md` and `model.md` are written for its scenario.
- **The results schema** can stay shared: a kink exists only where the constraint binds, and the limiting MPC at the
  floor only in the natural scenario with a point mass.
- **HARK.**
  - On main, HARK takes the natural limit from the lowest atoms. With its default lognormal laws and no artificial
    constraint, that lets households borrow 1.5 times permanent income, which the true laws rule out (the HARK session).
    The adapter therefore uses the laws' infima: draft econ-ark/HARK#1862, with #1861 and #1863 for the bounds and the
    truncated lognormal.
  - HARK's stone records which scenarios each type can express. The portfolio types accept only `BoroCnstArt = 0.0`, so
    the artificial and zero-infima scenarios; the labor model accepts only `None`, the natural ones.
- **The ontology:**
  - one class for each scenario, under the buffer-stock class, with BST's own model inside the natural scenario with a
    point mass;
  - bounded support becomes a membership axiom of the two natural scenarios, which settles part of the open question on
    the two tiers;
  - the point-mass axiom names the joint worst income;
  - the liquidity-constrained class becomes the a ≥ 0 cases of the artificial and zero-infima scenarios, where Ma,
    Stachurski and Toda apply, with E[ξ^(−ϱ)] < ∞ in place of a positive lowest income.
- **Order.** Pull request #15, the stage files' rewrite, merges first; the new stage files build on it.

## The decisions, as ruled

The owner's answers of 12:50:56 EST on 2026-11-01:
- **The natural scenario's scope:** widened to h_min ≥ 0, so that BST's own model, with h_min = 0, belongs to it.
- **The natural scenario without a point mass:** a scenario of its own.
- **The point mass at the joint worst income,** in place of "the worst transitory realization" in the ruling of
  2026-10-31.
- **`library`:** its laws are truncated.
- **The families' names:**
  - `bst-natural/1`;
  - `bst-natural-no-point-mass/1`;
  - `bst-artificial/1`;
  - `bst-zero-infima/1`;
  - the Markov family's artificial and zero-infima versions.
- **The zero-infima scenario's written form:** `a_Art` is left out, since a ≥ 0 is the natural constraint there.
- **FVAC-PF in the schemas:** PF-FVAC is renamed FVAC-PF in the checker, the results schema and the families' documents.
