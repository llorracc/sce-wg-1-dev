# bst/1: conditions and implications

Draft; see the [README](../README.md).

This document collects four kinds of statement about a member of [`bst/1`](model.md), each defined for any member, whatever
its laws:

- **validity conditions**, restrictions on the parameters under which the household's problem has a solution; a member that
  fails one is rejected;
- **domain rules**, which say when a reported quantity exists; a quantity a member does not define is reported as
  `undefined`;
- **implications**, exact consequences of the parameters that a results file can be tested against;
- **the simulation phase**, the conditions under which the stationary population and its welfare are well defined.

Every condition is an inequality between a factor and a bound, and every factor is arithmetic on the parameters and on a
few **expectations** under the laws, which the table below names for each condition. The **checker** evaluates them for the
**stated member**, the one the parameter file names, in closed form for the laws the schemas admit, as the limit a
toolkit's effective member approaches; a **toolkit** evaluates them for its **effective member**, the member it actually
solves with its own approximation of the laws, and reports the expectations, the factors and the verdicts
([results](results.md), [`effective-member.md`](../effective-member.md)). The notation is BST's, as in the
[model schema](model.md).

## Notation

For type i:
- the absolute patience factor is Þ_i = (R β_i ℒ)^(1/ρ);
- the return patience factor is Þ_i/R, and the growth patience factor is Þ_i/𝒢;
- Þ̄_i = min(Þ_i, R).

As m → ∞, the saving share a/m of the rule tends to Þ̄/R. When the RIC holds, the MPC tends to 1 − Þ/R and Þ̄ = Þ. When it
fails, the MPC tends to zero and Þ̄ = R. For large m, then, m′ ≈ (Þ̄/(𝒢 ψ′)) m.

The moments of the permanent shock that the conditions use are E[ψ^k] for real k, E[log ψ] and E[ψ log ψ], with `ψ_min`, the
lowest value of its support, and the mass there.

`ξ_min` is the lowest value of the transitory shock ξ: ξ_U when ℘ > 0 and ξ_U lies below the employed draws, else the
lowest employed draw `θ_min` (1 − ℘ξ_U)/(1 − ℘). `p_worst` is the probability that income ψξ takes its lowest value:
- with ℘ > 0 and ξ_U = 0, BST's case, `p_worst` = ℘, since income is then zero whatever ψ is;
- otherwise `p_worst` = P(ξ = `ξ_min`) · P(ψ = `ψ_min`), which is zero unless both laws put mass at their lowest values.

## Validity conditions

A member that fails any of these is rejected outright:
- the parameter domains of the [model schema](model.md) and the rules of the [shock laws](../shock-laws.md);
- ℘ξ_U < 1, so that employed income is positive;
- `a_Nat` ≤ `a_Art` ≤ 0, for one written form;
- for every type, the FVAC, and the RIC or the WRIC, from the table below.

BST's existence theorem assumes shocks with bounded support and ρ > 1. Existence for unbounded laws, such as the untruncated
lognormal, is set aside for now.

## The conditions

Each condition carries its name in BST, the expectations it rests on, which a toolkit reports for its effective member, and
HARK's name for its factor.

| Condition | Inequality | Rests on | What it governs | HARK factor |
|---|---|---|---|---|
| AIC, absolute impatience | Þ < 1 | the parameters | consumption growth as m → ∞ is below one | `APFac` |
| RIC, return impatience | Þ/R < 1 | the parameters | the MPC as m → ∞ is 1 − Þ/R > 0 | `RPFac` |
| WRIC, weak return impatience | `p_worst`^(1/ρ) Þ/R < 1 | `p_worst`, the mass at the worst income | stands in for the RIC for existence; the MPC at the lower limit of m is 1 − `p_worst`^(1/ρ) Þ/R | `WRPFac` |
| FHWC, finite human wealth | 𝒢/R < 1 | the parameters | human wealth is finite | `FHWFac` |
| PF-FVAC, perfect-foresight finite value of autarky | β ℒ 𝒢^(1−ρ) < 1 | the parameters | the perfect-foresight value of autarky is finite | `PFVAFac` |
| FVAC, finite value of autarky | β ℒ 𝒢^(1−ρ) E[ψ^(1−ρ)] < 1 | E[ψ^(1−ρ)] | the value of autarky is finite | `VAFac` |
| GIC, growth impatience | Þ/𝒢 < 1 | the parameters | the pseudo-target m̌ exists | `GPFacRaw` |
| GIC-Mod, strong growth impatience | Þ E[ψ^(−1)]/𝒢 < 1 | E[ψ^(−1)] | the buffer stock target m̂ exists | `GPFacMod` |
| GIC-Szeidl, log growth impatience | log(Þ/𝒢) < E[log ψ] | E[log ψ] | with ℒ = 1, the stationary population exists under the population measure; on strict failure, households escape to infinite m | `check_GICSdl`, from `ELogPermShk` |
| GIC-Harmenberg | Þ/𝒢 < exp(E[ψ log ψ]) | E[ψ log ψ] | with ℒ = 1, the stationary population exists under the income measure; weaker than the GIC, since E[ψ log ψ] ≥ 0 | `GPFacHrm` |
| GIC-Liv, mortality-adjusted growth impatience | ℒ Þ/𝒢 < 1 | the parameters | aggregate balanced growth with Modigliani-style destruction of estates | `GPFacLiv` |
| The rate condition | (R/𝒢)(Þ/𝒢) compared with E[ψ²] | E[ψ²] | only how fast c(m) approaches its perfect-foresight bound; not a validity condition | none |
| The welfare conditions, below | the atom case's factor below one | E[ψ^(ρ−1)] for W and F, E[ψ^ρ] for M, and `p_worst` | population welfare and marginal welfare are finite | none |

The expectations a toolkit reports are therefore E[ψ], E[θ], E[ψ^(1−ρ)], E[ψ^(−1)], E[log ψ], E[ψ log ψ], E[ψ²],
E[ψ^(ρ−1)], E[ψ^ρ] and `p_worst`, under its own representation of the laws, with the lowest values of ψ and of income beside them.

Notes:
- Under a lognormal ψ, the GIC, GIC-Szeidl and GIC-Mod are one inequality, Þ/𝒢 < e^(kσ²), at k = 0, −1/2 and −1. Under the
  other laws they differ in other ways, which is why the checker uses each law's own moments.
- HARK's released `VAFac` leaves out ℒ. Draft pull request econ-ark/HARK#1855 adds it.
- HARK also computes `GPFacLivMod` as ℒ·`GPFacLiv`. Since HARK's `APFac` already contains ℒ, that factor carries the survival
  probability twice relative to ℒ Þ/𝒢. No HARK check uses it.

## Domain rules

These decide whether a member defines each reported quantity. A quantity a member does not define is reported with the status
`undefined` ([results](results.md)).

The special points of the rule:
- **The buffer stock target m̂_i** needs Þ̄ E[ψ^(−1)]/𝒢 < 1.
- **The pseudo-target m̌_i** needs Þ̄/𝒢 < 1.
- **The kink m*_i** needs the artificial constraint to bind somewhere: `a_Art` > `a_Nat`. It is absent, for example, when
  ξ_U = 0 and `a_Art` = 0.

When the RIC holds these are the GIC-Mod and the GIC. When it fails, the slope argument above replaces Þ by R. That is a
deduction, not yet checked against a published result. Both targets are defined conditional on survival, with ℒ entering only
through Þ. Their existence also uses three properties of the rule: it exists, it crosses each locus once (as a concave rule
does), and it is asymptotically linear with saving share Þ̄/R.

The stationary population, for each type:

**With ℒ < 1:**
- **Population measure.** The distribution exists for every valid member. It is a mixture over ages with geometric weights
  (1 − ℒ) ℒ^s, the unique fixed point of a map that contracts at rate ℒ.
- **Its moments.** The moment of order j is finite exactly when ζ > j, where ζ > 0 solves ℒ E[(Þ̄/(𝒢 ψ))^ζ] = 1. When no
  root exists, which happens when Þ̄/𝒢 is at most `ψ_min`, every moment is finite. In particular, the mean is finite exactly when
  ℒ Þ̄ E[ψ^(−1)]/𝒢 < 1.
- **Income measure.** It is defined when ℒ 𝒢 < 1. Its moment of order j is finite exactly when ℒ 𝒢 (Þ̄/𝒢)^j E[ψ^(1−j)] < 1,
  so its mean is finite exactly when ℒ Þ̄ < 1. When ℒ 𝒢 ≥ 1 it is `undefined` for `bst/1`.

**With ℒ = 1:**
- The population measure needs the GIC-Szeidl. Its moment of order j is finite exactly when j < ζ, where
  E[(Þ̄/(𝒢 ψ))^ζ] = 1, so its mean is finite exactly when Þ̄ E[ψ^(−1)]/𝒢 < 1.
- The income measure needs the GIC-Harmenberg. Its moment of order j is finite exactly when (Þ̄/𝒢)^j E[ψ^(1−j)] < 1, so its
  mean is finite exactly when Þ̄/𝒢 < 1.

Statistics that need less:
- The generalized Lorenz ordinates GL(p) = ∫₀^p Q(u) du are finite for p < 1 whenever the distribution exists. Only GL(1), the
  mean, needs a finite first moment.
- A pooled statistic is defined when it is defined for every type.

**Population welfare** W_i and the mean felicity F_i are defined when the stationary population exists and the welfare
condition of the simulation phase, below, holds; **marginal welfare** M_i, and its bottom-quartile mean, when the marginal
condition holds.

These conditions differ from the GIC-Liv, which concerns aggregate growth, because newborns here enter at 𝐩 = 1, not at the
population's mean permanent income.

## Implications

Exact consequences of the parameters, which the comparison tests a results file against:
- **The limiting MPC.** c_i′(m) → 1 − Þ_i/R as m → ∞ under the RIC, and → 0 when it fails.
- **The MPC at the lower limit.** c_i′(m) → 1 − `p_worst`^(1/ρ) Þ_i/R as m → `a_min` from above, when the artificial constraint does not
  bind there.
- **The natural borrowing constraint.** With u(0) = −∞ the household never lets the worst income force zero consumption, so
  `a_Nat` = −`ξ_min` κ/(1 − κ) with κ = `ψ_min` 𝒢/R when κ < 1, and no finite natural constraint when κ ≥ 1; `a_Nat` = 0 whenever a law
  is unbounded below or ξ_U = 0 with ℘ > 0. The constraint in force is `a_min` = max(`a_Art`, `a_Nat`); the rule
  satisfies c(m) < m − `a_min` wherever the artificial constraint does not bind.
- **The worst-income probability `p_worst`**, as defined above; with it, the natural constraint and the MPC bounds.
- **The newborn's lowest resources.** A newborn's m is at least `θ_min` (1 − ℘ξ_U)/(1 − ℘), and exactly that when θ has
  mass at its lowest value.
- **The tail exponents** ζ of the two measures, which say how the stationary distribution's upper tail decays, and hence which
  moments are finite.
- **Consistency of the rule and the distribution.** The laws of a and c under the stationary population are the images of the
  law of m under the rule, and E[m′] over the population equals 1 + ℒ R E[ψ^(−1)] E[a]/𝒢 under the population measure.

## The simulation phase

**Positivity.** No household, survivor or newborn, arrives at the decision perch with resources at which no positive
consumption is feasible. Survivors satisfy it by the natural borrowing constraint, an implication of ρ > 1. Newborns satisfy
it by the family's convention: born employed, with no assets, so m = θ (1 − ℘ξ_U)/(1 − ℘) > 0 under every shock law; the
one parameter condition this leaves, ℘ξ_U < 1, is among the validity conditions.

**The welfare conditions.** Population welfare W_i = E[v_i(m)] and the mean felicity F_i = E[u(c_i(m))] are finite only if
the stationary population puts little enough mass where v_i and u diverge, and the mean marginal utility M_i = E[u′(c_i(m))]
needs less mass still. With ρ > 1, v_i and u behave like (m − `m_min`)^(1−ρ) near `m_min`, the lowest resources from which positive
consumption is feasible, and u′ like (m − `m_min`)^(−ρ); so W_i and F_i are finite exactly when E[(m − `m_min`)^(−(ρ−1))] is under the
stationary population, and M_i exactly when E[(m − `m_min`)^(−ρ)] is: conditions on the lower tail, the mirror image of the
upper-tail condition ζ > 1 for the mean of m. The lower tail depends on the constraint and on the laws at their lowest values:
- **A binding artificial constraint**, `a_Art` > `a_Nat`, which is the kink's existence: the rule keeps consumption above a
  positive value, and all three means are finite. HAFiscal's model and the toy are in this case. An income floor alone does
  not do this: the natural constraint moves down by the floor's capitalized value and consumption still goes to zero as
  resources approach it, which is BST's own remark on a nonzero minimum of ξ. An earlier version of this document credited
  the floor; the BufferStockTheory session corrected that on 2026-10-18.
- **The natural constraint alone, with an atom at the worst income**, BST's zero-income event with mass ℘, or more generally
  a worst income of mass `p_worst`: the mass near `m_min` comes from runs of worst-income draws. Each shrinks resources above `m_min` by the
  factor `p_worst`^(1/ρ) Þ/(𝒢 ψ), since the MPC at the bottom is 1 − `p_worst`^(1/ρ) Þ/R, and a run continues with probability `p_worst` ℒ per
  period, since death ends it too. The lower tail is then a power law, and

      E[(m − `m_min`)^(−q)] is finite exactly when  `p_worst`^(1 − q/ρ) ℒ (𝒢/Þ_i)^q E[ψ^q] < 1.

  At q = ρ − 1 this is the condition for W_i and F_i. At q = ρ it reads ℒ (𝒢/Þ_i)^ρ E[ψ^ρ] < 1, which the GIC defeats
  without mortality, since E[ψ^ρ] ≥ 1: in BST's baseline the mean marginal utility under the stationary distribution is
  infinite for every growth-impatient household, although each household's is finite; with mortality the condition can hold
  for patient enough households. The BufferStockTheory session checked the tail exponent against an EGM solution at the
  paper's baseline (1.974 measured, 1.977 predicted) and gave a second proof for q = ρ, from the Euler equation integrated
  over the stationary distribution: M_i is infinite whenever (Þ_i/𝒢)^ρ E[ψ^(−ρ)] < 1, which with ψ degenerate is the GIC.
- **The natural constraint alone, with a positive density at the floor in n of the two shocks** (a truncated lognormal, the
  uniform, or a tabulated law rising from its first point; n = 1 when the other shock has an atom at its floor, n = 2 when
  both have densities and the floor income is positive): the mass that lands within a distance x of `m_min` in one step is of
  order x^n, but the stationary tail's exponent is max(n, ρ). For ρ < n the constraint binds on a neighborhood of `m_min` and the
  tail is the landing law's; for ρ > n the Euler equation holds there, the household saves a vanishing amount, and the tail
  steepens to x^ρ up to a logarithmic factor. So E[(m − `m_min`)^(−q)] is finite exactly when q < max(n, ρ): W_i and F_i are
  finite for every ρ, and M_i exactly when ρ < n, never with n = 1 and for ρ < 2 with n = 2. At ρ = n the marginal mean sits
  on the borderline and is infinite. The regimes and the one-density numerics are the BufferStockTheory session's, which
  corrected an earlier statement here that the tail was x^n throughout; the two-density landing law is a deduction, not
  yet run.
- **A density that vanishes at the floor faster than any power**, the untruncated lognormal at zero: every moment is finite.

These derivations are of 2026-10-18; the atom case is checked numerically, the rest are deductions.

The checker classifies each member by these cases and reports population welfare, and marginal welfare with its
bottom-quartile mean, as `undefined` where the moment is infinite; the upper quartiles and the GL ordinates of u′(c) for
p < 1 stay defined. A finite-sample or finite-grid estimate of an infinite mean looks stable and drifts slowly, by about five
percent per decade of truncation at BST's baseline, which is why the status is reported with the number.

## The stated member and the effective member

The member a parameter file names is the **stated member**; the member a toolkit solves, with its own approximation of the
laws in its own representation, is its **effective member** ([`effective-member.md`](../effective-member.md)). Everything
above is defined for both, and is decided for each by the same arithmetic on its own expectations.

- **The lowest value of a law** is defined as the limit of a representation's bottommost point as its number of points
  grows without bound. It is then a property of the law and not of any representation, since every consistent scheme's
  lowest point tends to it; a toolkit's reported lowest value is its approximation of that primitive, as its reported
  E[ψ^(−1)] is of the law's, and it lies at or above the limit. For a truncated law the limit is the truncation point,
  positive and finite, so the stated member has a finite natural limit and a positive worst income, and every effective
  member shares that regime, differing in value only. For a law unbounded below the limit is zero while every finite
  representation's lowest point is positive, so every effective member has a finite natural limit where the stated member
  has none, and a kink under a zero artificial limit where the stated member has none: the regime never converges, only
  the value. That is why the truncated lognormal is the recommended law, and why a member with an untruncated law is a
  limit case, to be read as such.
- **Verdicts.** The checker decides each condition for the stated member and reports the factor with its margin; a verdict
  whose margin lies within the precision of the closed forms is `undecided`. A toolkit decides each condition for its
  effective member and reports the factor and the verdict; the checker recomputes the factor from the reported
  expectations and the parameters, which catches a factor that leaves out a term, and checks that the verdict agrees with
  it and that the statuses of the quantities follow the verdicts. Near a boundary the stated and the effective member can
  sit on opposite sides; the two factors say by how much, and the comparison reports the difference of regime rather than
  counting a disagreement of values.
- **The lower tail of an effective member.** A finite representation has an atom at its lowest value, so an effective
  member whose artificial constraint does not bind falls under the atom case above, with `p_worst` the representation's mass at
  the worst income, whatever the stated member's case; as the representation refines, `p_worst` falls and the effective
  member's welfare verdicts approach the stated member's. Where the artificial constraint binds in the effective member,
  which the exact natural limit of a stated member with truncated laws can make it do even where the stated member's does
  not, every welfare mean is finite there.
- **Two representations in one toolkit.** A toolkit may solve the household under one representation of the laws and
  push the population forward under another. The household's representation is its effective member; it reports the
  population's beside it when the two differ ([results](results.md)), and the population's then decides the conditions
  that are about the stationary population, the GIC-Szeidl, the GIC-Harmenberg, the welfare conditions and the tail
  exponents, while the household's decides the rest, the natural limit and the constraint in force among them.
- **Admission.** A member is admitted to a suite by the stated member's validity conditions. A toolkit whose effective
  member fails one that the stated member passes reports so; the run is read as a discretization too coarse for the
  member, not as a defect of the member.

## Open points

- **A proof of the tail conditions.** The upper-tail conditions follow from the asymptotic recurrence m′ ≈ (Þ̄/(𝒢 ψ′)) m, and
  the welfare condition from the behavior of the rule at the bottom. A proof would need a Kesten–Goldie-type result for a
  multiplicative process killed at rate 1 − ℒ. None is cited yet.
- **The income measure when ℒ < 1 and ℒ 𝒢 ≥ 1.** The cross-section normalized by aggregate permanent income may still
  converge, to the stationary law of the income-weighted chain, when the GIC-Harmenberg holds. That is unverified.
- **The boundary cases.** Equality in any condition is left open.
