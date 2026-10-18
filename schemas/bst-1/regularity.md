# bst/1: regularity conditions

Draft; see the [README](../README.md).

These are the conditions on the parameters of [`bst/1`](model.md) that decide two things: whether a member has a solution, and
which reported quantities the member defines. The list includes every condition that uncertainty modifies. The **checker**
evaluates each one exactly, from the [shock laws'](../shock-laws.md) closed-form moments, never from a toolkit's quadrature. A
condition computed from a discretized shock depends on the number of nodes. A results file reports the checker's verdicts.

## Notation

For type k:
- the absolute patience factor is Þ_k = (R β_k L)^(1/ρ);
- the return patience factor is Þ_k/R, and the growth patience factor is Þ_k/G;
- Þ̄_k = min(Þ_k, R).

As m → ∞, the saving share a/m of the rule tends to Þ̄/R. When the RIC holds, the MPC tends to 1 − Þ/R and Þ̄ = Þ. When it
fails, the MPC tends to zero and Þ̄ = R. For large m, then, m′ ≈ (Þ̄/(G ψ′)) m.

The moments of the permanent shock that the conditions use are E[ψ^k] for real k, E[log ψ] and E[ψ log ψ], with the infimum of
its support.

℘ is the probability that income ψθ takes its lowest possible value:
- with μ = 0, ℘ = ℧, since income is then zero whatever ψ is;
- with μ > 0, ℘ = P(θ at its infimum) · P(ψ at its infimum). It is zero unless both put mass at their infima. θ has mass ℧
  at μ, and μ is its infimum when it lies below the lowest employed value.

## The conditions

Each condition carries its name in Buffer Stock Theory and HARK's name for its factor. They are listed as they are stated in
the literature, with Þ.

| Condition | Inequality | What it governs | HARK factor |
|---|---|---|---|
| AIC, absolute impatience | Þ < 1 | consumption growth as m → ∞ is below one | `APFac` |
| RIC, return impatience | Þ/R < 1 | the MPC as m → ∞ is 1 − Þ/R > 0 | `RPFac` |
| WRIC, weak return impatience | ℘^(1/ρ) Þ/R < 1 | stands in for the RIC for existence; the MPC at the lower limit of m is 1 − ℘^(1/ρ) Þ/R | `WRPFac` |
| FHWC, finite human wealth | G/R < 1 | human wealth is finite | `FHWFac` |
| PF-FVAC, perfect-foresight finite value of autarky | β L G^(1−ρ) < 1 | the perfect-foresight value of autarky is finite | `PFVAFac` |
| FVAC, finite value of autarky | β L G^(1−ρ) E[ψ^(1−ρ)] < 1 | the value of autarky is finite | `VAFac` |
| GIC, growth impatience | Þ/G < 1 | the pseudo-target m̂ exists | `GPFacRaw` |
| GIC-Mod, strong growth impatience | Þ E[ψ^(−1)]/G < 1 | the buffer stock target m̌ exists | `GPFacMod` |
| GIC-Szeidl, log growth impatience | log(Þ/G) < E[log ψ] | with L = 1, the stationary population exists under the population measure; on strict failure, households escape to infinite m | `check_GICSdl`, from `ELogPermShk` |
| GIC-Harmenberg | Þ/G < exp(E[ψ log ψ]) | with L = 1, the stationary population exists under the income measure; weaker than the GIC, since E[ψ log ψ] ≥ 0 | `GPFacHrm` |
| GIC-Liv, mortality-adjusted growth impatience | L Þ/G < 1 | aggregate balanced growth with Modigliani-style destruction of estates | `GPFacLiv` |
| The rate condition | (R/G)(Þ/G) compared with E[ψ²] | only how fast c(m) approaches its perfect-foresight bound; not a validity condition | none |

Notes:
- Under a lognormal ψ, the GIC, GIC-Szeidl and GIC-Mod are one inequality, Þ/G < e^(kσ²), at k = 0, −1/2 and −1. Under the
  other laws they differ in other ways, which is why the checker uses each law's own moments.
- HARK's released `VAFac` leaves out L. Draft pull request econ-ark/HARK#1855 adds it.
- HARK also computes `GPFacLivMod` as L·`GPFacLiv`. Since HARK's `APFac` already contains L, that factor carries the survival
  probability twice relative to L Þ/G. No HARK check uses it.

## Validity conditions

A member that fails any of these is rejected outright:
- the parameter ranges of the [model schema](model.md) and the [shock laws](../shock-laws.md);
- b within the natural borrowing limit;
- for every type, the FVAC, and the RIC or the WRIC.

Buffer Stock Theory's existence theorem assumes shocks with bounded support and ρ > 1. Existence for unbounded laws, such as
the untruncated lognormal, is set aside for now.

## Domain rules

These decide whether a member defines each reported quantity. A quantity a member does not define is reported with the status
`undefined` ([results](results.md)).

The special points of the rule:
- **The buffer stock target m̌_k** needs Þ̄ E[ψ^(−1)]/G < 1.
- **The pseudo-target m̂_k** needs Þ̄/G < 1.
- **The kink m*_k** needs the borrowing constraint to bind somewhere. For example, it fails when μ = 0 and b = 0.

When the RIC holds these are the GIC-Mod and the GIC. When it fails, the slope argument above replaces Þ by R. That is a
deduction, not yet checked against a published result. Both targets are defined conditional on survival, with L entering only
through Þ. Their existence also uses three properties of the rule: it exists, it crosses each locus once (as a concave rule
does), and it is asymptotically linear with saving share Þ̄/R.

The stationary population, for each type:

**With L < 1:**
- **Population measure.** The distribution exists for every valid member. It is a mixture over ages with geometric weights
  (1 − L) L^s, the unique fixed point of a map that contracts at rate L.
- **Its moments.** The moment of order j is finite exactly when ζ > j, where ζ > 0 solves L E[(Þ̄/(G ψ))^ζ] = 1. When no root
  exists, which happens when Þ̄/G is at most the infimum of ψ, every moment is finite. In particular, the mean is finite exactly
  when L Þ̄ E[ψ^(−1)]/G < 1.
- **Income measure.** It is defined when L G < 1. Its moment of order j is finite exactly when L G (Þ̄/G)^j E[ψ^(1−j)] < 1, so
  its mean is finite exactly when L Þ̄ < 1. When L G ≥ 1 it is `undefined` for `bst/1`.

**With L = 1:**
- The population measure needs the GIC-Szeidl. Its moment of order j is finite exactly when j < ζ, where
  E[(Þ̄/(G ψ))^ζ] = 1, so its mean is finite exactly when Þ̄ E[ψ^(−1)]/G < 1.
- The income measure needs the GIC-Harmenberg. Its moment of order j is finite exactly when (Þ̄/G)^j E[ψ^(1−j)] < 1, so its
  mean is finite exactly when Þ̄/G < 1.

Statistics that need less:
- The generalized Lorenz ordinates GL(p) = ∫₀^p Q(u) du are finite for p < 1 whenever the distribution exists. Only GL(1), the
  mean, needs a finite first moment.
- A pooled statistic is defined when it is defined for every type.

These conditions differ from the GIC-Liv, which concerns aggregate growth, because newborns here enter at P = 1, not at the
population's mean permanent income.

## Open points

- **A proof of the tail conditions.** The moment conditions follow from the asymptotic recurrence m′ ≈ (Þ̄/(G ψ′)) m. A proof
  would need a Kesten–Goldie-type result for a multiplicative process killed at rate 1 − L. None is cited yet.
- **The income measure when L < 1 and L G ≥ 1.** The cross-section normalized by aggregate permanent income may still
  converge, to the stationary law of the income-weighted chain, when the GIC-Harmenberg holds. That is unverified.
- **The boundary cases.** Equality in any condition is left open.
