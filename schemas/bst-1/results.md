# bst/1: the results schema

Draft; see the [README](../README.md).

A results file is JSON, written by a program and checked by a validator. It reports quantities that the
[model schema](model.md) defines, at arguments that the toolkit does not choose. It never reports a toolkit's grid, histogram
or interpolant. Every value is a ratio to permanent income, in BST's notation. Items are **required** unless they are marked
optional.

## Identity and provenance

- The family, its version and the parameter file's hash.
- The hash of the method file and of the settings element ([numerical methods](../numerics.md)).
- The hash of the request file, which holds the comparison points.
- The toolkit and its version.
- The hardware, the threads and the wall time.

## Comparison points

The right points in m depend on the parameterization, so no fixed list serves every member. A separate **request file** holds
them. It is kept out of the parameter file, so that asking for more points never changes the model's hash.

Its points come, by a stated rule, from a quick solution of the member. For each type they are:
- the stationary quantiles of m at u = 0.01, 0.05, 0.1, 0.2, …, 0.9, 0.95 and 0.99;
- the lower end of m;
- several points above the 99th percentile.

Each point is rounded to three significant figures.

## The rule, for each type

**At the comparison points:**
- c_i(m);
- the MPC c_i′(m), as a derivative, not a finite difference.

**At the special points.** Each value is reported with its status, `undefined` when its domain rule fails
([conditions](conditions.md)):
- **The kink m*_i,** the largest m at which the artificial borrowing constraint binds, with the rule's slope on each side.
- **The buffer stock target m̌_i,** where E[m_{t+1}] = m_t for a survivor, with c and the MPC there.
- **The pseudo-target m̂_i,** where E[M_{t+1}]/M_t = 𝒢 for a survivor, with c and the MPC there.

For a survivor, E[m′] = R a(m) E[ψ^(−1)]/𝒢 + 1, so m̌ solves R a(m) E[ψ^(−1)]/𝒢 + 1 = m. In levels, E[M_{t+1}] = R A_t + 𝒢 P_t,
so m̂ is where the rule meets the locus a(m) = (𝒢/R)(m − 1).

**The exported rule.** Each type's rule at dense points of the toolkit's choosing, with the kink included and the range stated,
so that a reader can compute dynamics that the results file does not report.

## The stationary population (the numerical ergodic distribution)

**Always reported**, for each type and pooled over types by share.

Under the **population measure**, for m, a and c:
- The **generalized Lorenz ordinates** GL(p) = ∫₀^p Q(u) du, where Q is the quantile function, at p = 0.01, 0.05, 0.1, 0.2, …,
  0.9, 0.95, 0.99, 0.999 and 1. GL(1) is the mean.
- The quantiles at the same probabilities (optional).
- The mean of c, the aggregate ratio of consumption to income.
- The mass at the borrowing constraint, a = a̲, and the fraction with a ≤ 0.
- The mean MPC, and the mean MPC within each quartile of a. The quartiles are defined through the quantile rank, so a mass point
  needs no tie rule.

Under the **income measure**, for m and a:
- the GL ordinates at the same probabilities;
- the mass at the borrowing constraint;
- the mean of a;
- the mean MPC, the weighting that aggregate consumption responses use.

Each ordinate or moment whose finiteness condition fails is reported as `undefined`. GL(p) for p < 1 is defined whenever the
distribution is.

Why generalized Lorenz ordinates:
- They are defined whatever the distribution's mass points and gaps.
- They determine the distribution, since Q is their derivative.
- They are finite for p < 1 even where the mean is not.
- As integrals, they are less noisy than quantiles when the distribution was simulated.
- The difference between two toolkits' ordinates, integrated over p, bounds the Wasserstein distance between their two
  distributions.

A levels Lorenz curve divides by the mean, which may be infinite, and discards the scale. Moments are finite only up to the tail
exponent.

The laws of a and c are images of the law of m under the rule. Reporting all three therefore checks the rule's consistency more
than it adds information: a disagreement in a alone points to the rule.

## Welfare and marginal welfare

**Always reported**, for each type and pooled by share, under the population measure, in utils:
- **W_i = E[v_i(m)]**, the mean of the value function over the stationary population, with v_i the value of the household's
  problem as the [model schema](model.md) states it.
- **F_i = E[u(c_i(m))]**, the mean felicity, the planner's flow welfare; for a stationary population a planner's sum discounted
  at R is F_i/(1 − 1/R) per household.
- **M_i = E[u′(c_i(m))]**, the mean marginal utility of consumption, equal by the envelope condition to the mean marginal
  value of resources E[v_i′(m)]: the first-order welfare effect, in utils, of one unit of normalized resources given to every
  household; and the same mean within each quartile of a and at the borrowing constraint, the value of a targeted unit.
- Optional: the GL ordinates of u′(c) at the standard probabilities, and all of the above under the income measure.

No conversion to consumption units and no bang for the buck are reported. HAFiscal's welfare measure weights each
household's gain by its own marginal utility in normal times, so a uniform marginal transfer in the stationary member scores
one by construction; the measure is built in the experiments layer from these statistics. Each statistic is `undefined`
where the [conditions](conditions.md) say its mean is infinite: W and F fail the welfare condition for impatient enough
members with a zero-income event; M and its bottom-quartile mean fail for every growth-impatient member without mortality
whose worst income is an atom and whose artificial constraint does not bind, BST's baseline among them. The upper quartiles
and the GL ordinates for p < 1 stay defined. A toolkit reports the status with the number, since a finite-sample estimate of
an infinite mean looks stable. How v_i was obtained is the method on the target `cntn_to_dcsn.value`
([numerical methods](../numerics.md)): the value function the solver computes, or discounted utility along simulated paths,
which then carries a standard error; u and u′ at the rule need nothing beyond the rule and the distribution.

## Diagnostics that need no reference solution (required)

Convergence across a suite shows that a toolkit is stable, not that it is right. These diagnostics test a solution against the
model itself.

**Euler residuals, at each comparison point and for each type.** Let

    ĉ(m) = (u′)^(−1)( β_i ℒ R E[(𝒢 ψ′)^(−ρ) u′(c(m′))] ),   m′ = R (m − c(m))/(𝒢 ψ′) + ξ′.

The residual is

    r(m) = min( ĉ(m) − c(m),  m − a̲ − c(m) ) / c(m),

in units of consumption. It is zero for the exact rule:
- where the household saves, c = ĉ;
- where the constraint binds, c = m − a̲ ≤ ĉ.

So the same formula serves at, above and below the kink. The expectation in ĉ is the part `diagnostics.expectation`. It must be
computed by a method different from the household's own expectation, and stated, so that a toolkit cannot score its own
quadrature as exact. Report r at each point and the maximum of |r|.

**The stationarity residual, for each type and measure.** Push the reported stationary distribution of m forward one period,
under the reported rule and the shock laws, by a method stated for that purpose. Report the largest absolute difference between
the GL ordinates of m before and after the step, over the reported probabilities. It is zero for an exactly stationary
distribution, and it detects a toolkit that reports a transient.

**The Bellman residual** at the comparison points, in consumption-equivalent units, for methods that compute a value
(optional).

## Status values

- `undefined`: the member defines no such value, because a domain rule fails.
- `not computed`: the toolkit did not compute an optional value.

## Errors and precision

- Each value may carry the toolkit's own error estimate.
- A simulated value carries its standard error and its sample size.
- One run, at the toolkit's high precision, is required. The precision levels `low` and `medium` are optional elements of a
  suite ([numerical methods](../numerics.md)), with relative errors of about 10⁻² and 10⁻³ against 10⁻⁴ for `high`.

## The comparison

- Two results files are compared only when their parameter-file hashes match.
- A quantity agrees when the two values differ by no more than its tolerance. The tolerance comes from measured convergence
  across each toolkit's suite, widened by the standard errors of simulated values.
- If two toolkits each converge within their own errors and still disagree, at least one is wrong or is solving a different model.
  The diagnostics above help say which.

## Sketch of the form

The validator is not yet written. The shape will be roughly:

```json
{
  "family": "bst/1",
  "parameter_file_sha256": "…",
  "method_file_sha256": "…",
  "settings_sha256": "…",
  "request_file_sha256": "…",
  "toolkit": {"name": "…", "version": "…"},
  "types": [
    {
      "rule": {"m": [0.42, 0.61], "c": [0.40, 0.55], "mpc": [0.91, 0.42]},
      "kink": {"status": "value", "m": 0.38, "slope_below": 1.0, "slope_above": 0.93},
      "target": {"status": "value", "m": 1.39, "c": 1.01, "mpc": 0.07},
      "pseudo_target": {"status": "value", "m": 1.21, "c": 0.99, "mpc": 0.09},
      "population": {"m": {"gl": {"0.01": 0.0031, "1": "undefined"}}},
      "income_measure": {"m": {"gl": {"0.01": 0.0029}}},
      "welfare": {"status": "value", "mean_value": -31.2, "mean_felicity": -1.03},
      "marginal_welfare": {"status": "value", "mean": 1.07, "by_a_quartile": [2.1, 1.1, 0.7, 0.4], "at_constraint": 2.6},
      "euler_residuals": {"r": [1e-6, -2e-6], "max_abs": 2e-6},
      "stationarity_residual": {"population": 3e-5, "income": 4e-5}
    }
  ],
  "pooled": {}
}
```
