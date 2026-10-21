# bst/1: the results schema

Draft; see the [README](../README.md).

A results file is JSON, written by a program and checked by a validator. It reports quantities that the
[model schema](model.md) defines, at arguments that the toolkit does not choose, and it reports what the toolkit solved: its
**effective member**, known through the expectations the family names, the conditions decided on it and the derived
parameters it used, never through a form of its laws ([`effective-member.md`](../effective-member.md)). It never reports a
toolkit's grid, histogram or interpolant. Every value is a ratio to permanent income, in BST's notation. Items are
**required** unless they are marked optional.

## Identity and provenance

- The family, its version and the parameter file's hash.
- The hash of the method file and of the settings element ([numerical methods](../numerics.md)).
- The hash of the request file, which holds the comparison points.
- The toolkit and its version.
- The hardware, the threads and the wall time.
- Optional: the numerical environment, a free-form object of library versions; the driver, the program that assembled the
  file when the toolkit has more than one; and the parameter file's path. The hash, not the path, identifies the member.

## The effective member

What the toolkit solved, reported in numbers free of any representation:
- **The expectations** the [conditions](conditions.md) name, under the toolkit's own approximation of the laws: E[ψ],
  E[θ], E[ψ^(1−ρ)], E[ψ^(−1)], E[log ψ], E[ψ log ψ], E[ψ²], E[ψ^(ρ−1)], E[ψ^ρ], and p̲, the mass at the worst income. The
  means are reported, not required to be one, since an approximation need not preserve them.
- **The lowest values** of ψ and of income under that approximation, which lie at or above the stated member's infima.
- **The derived parameters** the toolkit used, its effective member's own: the natural limit, the constraint in force, the
  worst income and the employed-income scale ([model schema](model.md#derived-parameters)).
- **For each type, every condition** of the family's table: the factor the toolkit computed, the bound, and the verdict,
  holds or fails; and the two welfare conditions with their lower-tail case. Required in full: each is arithmetic on the
  expectations and the parameters.
- **The population's representation**, optional, under `population`: the same expectations and lowest values, present
  only when the toolkit pushes the population forward under a representation other than the one it solved the household
  with, as a transition-matrix method with its own node count does. When present it decides the conditions on the
  stationary population, the GIC-Szeidl, the GIC-Harmenberg, the two welfare conditions and the tail exponents; the
  household's block decides everything else, the natural limit and the constraint in force among them. When absent, the
  household's block decides everything.

The checker verifies what needs no representation: each factor as the arithmetic of the reported expectations, each
verdict against its factor, each status against the verdicts, each derived parameter as the arithmetic of the lowest values,
the lowest values against the stated infima, and the expectations against what every law obeys. The expectations' values
themselves are the toolkit's to compute and are trusted. The stated member's own verdicts, which are statements about a
limit, do not appear in a results file; the checker's report of the member carries them.

## Comparison points

The right points in m depend on the parameterization, so no fixed list serves every member. A separate **request file** holds
them. It is kept out of the parameter file, so that asking for more points never changes the model's hash.

Its points come, by a stated rule, from a quick solution of the member. For each type they are:
- the stationary quantiles of m at u = 0.01, 0.05, 0.1, 0.2, …, 0.9, 0.95 and 0.99;
- the lower end of m: the member's own infimum of m when consumption is positive there, else the 0.001 quantile, never a
  point of the toolkit's grid;
- several points above the 99th percentile.

Each point is rounded to three significant figures.

## The rule, for each type

**At the comparison points:**
- c_i(m);
- the MPC c_i′(m), as a derivative, not a finite difference.

**At the special points.** Each value is reported with its status, `undefined` when its domain rule fails in the toolkit's
effective member, by the toolkit's own verdicts ([conditions](conditions.md)):
- **The kink m*_i,** the largest m at which the artificial borrowing constraint binds, with the rule's slope on each side.
- **The buffer stock target m̌_i,** where E[m_{t+1}] = m_t for a survivor, with c and the MPC there.
- **The pseudo-target m̂_i,** where E[𝐦_{t+1}]/𝐦_t = 𝒢 for a survivor, with c and the MPC there.

For a survivor, E[m′] = R a(m) E[ψ^(−1)]/𝒢 + 1, so m̌ solves R a(m) E[ψ^(−1)]/𝒢 + 1 = m. In levels, E[𝐦_{t+1}] = R 𝐚_t + 𝒢 𝐩_t,
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
- The coverage of the representation (optional; see below).

Under the **income measure**, for m and a:
- the GL ordinates at the same probabilities;
- the mass at the borrowing constraint;
- the mean of a;
- the mean MPC, the weighting that aggregate consumption responses use;
- the coverage of the representation (optional), as under the population measure.

Each ordinate or moment whose finiteness condition fails is reported as `undefined`. GL(p) for p < 1 is defined whenever the
distribution is.

**The coverage of the representation** lets a reader judge whether GL(0.999) and GL(1) have converged. It gives a point `top`
of m or a, the mass `top_mass` that the representation puts at or above it, and `beyond_top`, what the representation does
with the mass the dynamics send beyond `top`:
- `clipped`: a grid that puts that mass on its highest point, `top`. `top_mass` is the mass held there. In a lottery it also
  holds part of the last cell's mass, so it is an upper bound on the mass the dynamics send beyond `top` each period: it
  measures how much the top binds, not the model's mass above `top`.
- `dropped`: a grid that drops that mass and renormalizes. `top_mass` is the mass dropped each period.
- `kept`: a simulation, which loses nothing. `top` is a point the toolkit states, `top_mass` the sample's share at or above
  it, and `sample_size` the number of agent-periods pooled. A share of zero means only that the mass is below about
  3/`sample_size`, and pooled periods are correlated.

An optional list `tail` gives points below `top`, ascending, each with the mass at or above it. Along a Pareto tail that
mass falls as x^(−α), so mass on the top far above what the tail's points extrapolate to is piling up there. With a tail
exponent α > 1, which the checker's report gives for each type, a clipped representation misses about
`top` · `top_mass`/(α − 1) of the mean; at α ≤ 1 the mean is infinite, as the domain rules say. When `top_mass` is well
below 0.001, Q(0.999) lies below the top, so neither it nor GL(0.999) reads the mass held there. In the pooled blocks
the coverage is given only when the types share a top, with share-weighted masses.

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
quadrature as exact. Report r at each point and the maximum of |r|. The expectation is taken against the stated member's
law, so the residual measures the whole error of the toolkit's solution as an approximation to the stated problem, and the
method states its own precision, measured for instance by refining it once more. Optionally the same residuals under the
toolkit's own representation of the laws, which measure the solution's error on its effective member alone.

**The stationarity residual, for each type and measure.** Push the reported stationary distribution of m forward one period,
under the reported rule and the shock laws, by a method stated for that purpose. Report the largest absolute difference between
the GL ordinates of m before and after the step, over the reported probabilities. It is zero for an exactly stationary
distribution, and it detects a toolkit that reports a transient. For a distribution obtained by a linear solve of a discretized
transition, the residual is that solve's own residual and tests nothing further; the diagnostic bites on iterated and simulated
distributions.

**The Bellman residual** at the comparison points, in consumption-equivalent units, for methods that compute a value
(optional).

## Status values

- `undefined`: the member defines no such value, because a domain rule fails.
- `not computed`: the toolkit did not compute an optional value.

A status is the toolkit's own, decided on its effective member by the verdicts it reports. The checker's report of the
member gives the stated member's verdict beside it, which is a statement about a limit, `undecided` when the closed form's
margin is within its precision.

## Errors and precision

- Each value may carry the toolkit's own error estimate.
- A simulated value carries its standard error and its sample size.
- One run, at the toolkit's `high` level, is required; `low` and `medium` are optional. The levels are named elements of a
  settings suite ([numerical methods](../numerics.md)): settings, not error targets. No level promises a relative error, since
  what a level reaches depends on the method; the first measurement, HARK's equiprobable discretization near the kink, is in
  the [records](../records/findings/2026-10-18_checker-and-emitter.md). The only source of a tolerance is measured
  convergence, as the comparison below says.

## The comparison

- Two results files are compared only when their parameter-file hashes match.
- A quantity agrees when the two values differ by no more than its tolerance. The tolerance comes from measured convergence
  across each toolkit's suite, widened by the standard errors of simulated values.
- If two toolkits each converge within their own errors and still disagree, at least one is wrong or is solving a different model.
  The diagnostics above help say which.
- Two toolkits whose effective members sit on opposite sides of a condition's boundary report opposite verdicts, and
  opposite statuses for the quantity the condition governs. The comparison reports that as a difference of regime, with
  both factors and the stated member's limit verdict where the closed form gives one, rather than as a disagreement of
  values.

## Sketch of the form

The validator is [`results.schema.json`](results.schema.json). The shape is roughly:

```json
{
  "family": "bst/1",
  "parameter_file_sha256": "…",
  "method_file_sha256": "…",
  "settings_sha256": "…",
  "request_file_sha256": "…",
  "toolkit": {"name": "…", "version": "…", "driver": "…"},
  "effective_member": {
    "expectations": {"psi_mean": 1.0, "psi_inverse": 1.003, "psi_log": -0.0015, "…": "…"},
    "lowest": {"psi": 0.85, "income": 0.29},
    "derived": {"natural_limit": -0.23, "constraint_in_force": 0.0, "worst_income": 0.25, "employed_scale": 1.014}
  },
  "types": [
    {
      "conditions": {"GIC-Mod": {"factor": 0.97, "bound": 1, "holds": true}, "…": "…"},
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
