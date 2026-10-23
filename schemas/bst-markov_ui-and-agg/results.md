# bst-markov_ui-and-agg/1: the results schema

Draft, begun on 2026-10-22; see the [README](../README.md).

A results file for this family follows [`bst/1`'s](../bst-1/results.md) design. It is JSON, written by a program and
checked by a validator. It reports quantities that the [model schema](model.md) defines, at arguments that the toolkit
does not choose, and it reports what the toolkit solved, its **effective member**, in numbers free of any representation
of the laws ([`effective-member.md`](../effective-member.md)). It never reports a toolkit's grid, histogram or
interpolant. Items are **required** unless they are marked optional.

This first version carries what the paper's estimation and its other moments use, as the owner ruled on 2026-10-22: the
rule and the constraint in force by employment state, the employment shares, the wealth statistics by group and pooled
over groups, and the paper's MPC. The rule's special points, welfare and marginal welfare, and the recession regime's
rule wait for a later version ("Not in this version", at the end).

**Units.** Values are ratios to permanent income, in BST's notation, except the statistics in levels, which are in the
units of the newborn's level law: for the paper's members, thousands of dollars a quarter. The rule is the optimizer's,
c̃(m̃, j), in its own units, as the toolkit solves it ([the splurge](model.md#the-splurge-as-an-observation-map)). The
household's resources, consumption and MPC follow from it by the observation map, which the checker can apply. Household
wealth is (1 − ℷ) a relative to permanent income and A = (1 − ℷ) a 𝐩 in levels, with a the optimizer's end-of-period
assets in its own units: the measure the paper's moments use. With ℷ = 0 the optimizer is the household.

## Identity and provenance

As in `bst/1`: the family, its version and the parameter file's hash; the hashes of the method file, the settings
element and the request file; the toolkit and its version; the hardware and the threads, and no run time; optionally the
numerical environment, the driver and the parameter file's path.

## The effective member, for each group

A group has its own growth factor and chain, so the effective member is reported group by group:
- **The chain** the toolkit solved with: the normal regime's rows over J = (E, U_2, U_1, X) and the recession's. These
  are parameters, not approximations, and must be the member's.
- **The expectations by next state**, under the toolkit's own approximation of the laws, for each j′ in J: E[𝒢(j′) ψ′ |
  j′], E[(𝒢(j′) ψ′)^(1−ϱ) | j′], E[(𝒢(j′) ψ′)^(−1) | j′], E[log ψ′ | j′] and E[ψ′ log ψ′ | j′]; and E[θ], the employed
  draw's mean. In a state where ψ is fixed, under `grows` and `frozen`, the toolkit reports the fixed values. The means
  are reported, not required to be one.
- **The lowest values by state**: ψ_min(j), the lowest value of ψ in j, and ξ_min(j), the lowest income in j. These are
  the infima the representation carries with its nodes, at zero probability where no node reaches them, which are the
  laws' own: everything computed from the bounds, the natural limits and the lowest value of human wealth among them,
  is then the same at every number of nodes (the owner's ruling of 2026-10-22). And `p_worst(j)`, the probability from j
  of next quarter's worst income at those infima: zero where the worst income is a continuous law's infimum, positive
  only into a state whose income there is an atom, as in the unemployed states under `grows` and `frozen`.
- **The derived parameters by state**, in the household's units: the natural limits `a_Nat(j)` and the constraint in
  force `a_min(j)`, the fixed points from those lowest values, without and with the artificial limit; and the worst
  income ξ_min(j) ψ_min(j).
- **For each type, every condition** of the [conditions](conditions.md) table: the factor, the bound and the verdict,
  and for a condition by state, one entry for each state. GIC-Harmenberg with ℒ = 1 is reported as `not computed` until
  its chain is stated.
- **The population's representation**, optional, under `population`, as in `bst/1`: the same expectations and lowest
  values, when the toolkit pushes the population forward under a representation other than the one it solved the
  household with.

The checker verifies what needs no representation: that the chain is the member's; each factor as the dominant
eigenvalue, or the arithmetic by state, of the reported expectations and rows; each verdict against its factor; each
status against the verdicts; the lowest values and `p_worst` against the stated member's, the laws' infima and their
masses there; and the natural limits and the constraint in force by state as the fixed points of
[conditions](conditions.md#the-constraint-in-force-by-state) from the reported lowest values.

## Comparison points

A separate request file holds them, as in `bst/1`, so that asking for more points never changes the model's hash. For
each group and type they are:
- the stationary quantiles of m̃ over the type's population, all states pooled, at u = 0.01, 0.05, 0.1, 0.2, …, 0.9,
  0.95 and 0.99;
- for each state, the lower end of m̃ in that state: its own infimum where consumption is positive there, else the
  state's 0.001 quantile;
- several points above the 99th percentile.

Each point is rounded to three significant figures. Every state's rule is reported at the same points, with that state's
lower end added.

## The rule, for each group, type and employment state

- **At the comparison points:** c̃(m̃, j) and the optimizer's MPC c̃′(m̃, j), as a derivative, not a finite difference.
- **The exported rule:** each state's rule at dense points of the toolkit's choosing, with the range stated.

## The stationary population, for each group and type

The normal regime's stationary population over (m̃, j), under the population measure:
- **The employment shares**, the population's distribution over J. Since newborns are born employed, they are μ = (1 −
  ℒ) e_E (I − ℒ P)^(−1), not the chain's stationary distribution ([conditions](conditions.md#implications)), and the
  checker verifies them against μ.
- **Household wealth relative to permanent income**, (1 − ℷ) a: its generalized Lorenz ordinates at bst/1's
  probabilities, 0.01 to 0.999 and 1, and its median.
- **The paper's MPC**: the mean over the population of

      1 − (1 − ℷ) ¼ Σ_{n=1}^{4} (1 − c̃′)^n,

  the expected share of a lottery win spent in the year in which it arrives. In the quarter of the win the household
  spends ℷ + (1 − ℷ) c̃′ of it; the rest is spent at the rate c̃′ in each of the year's remaining quarters, whose number
  is 0, 1, 2 or 3 with equal chance. This is the exact expectation of the published code's random draw. It is not a
  function of the mean MPC, since it is nonlinear in c̃′, so the mean of c̃′ is reported beside it.

## Statistics in levels, for each group and pooled

Household wealth in levels, A = (1 − ℷ) a 𝐩, over the stationary population of a group's types weighted by their shares,
and over all groups weighted by theirs:
- **For each group:** the generalized Lorenz ordinates of A at p = 0.2, 0.4, 0.6, 0.8 and 1, GL(1) being the group's
  mean wealth; the median of (1 − ℷ) a over the group's population; and the paper's MPC, with the mean of c̃′.
- **Pooled over groups:** the generalized Lorenz ordinates of A at p = 0.25, 0.5, 0.75 and 1; and, within each quartile
  of A so pooled, the paper's MPC and the mean of c̃′, and the same over the whole population.

The paper's moments follow exactly, as ratios: a group's Lorenz share at p is GL_g(p)/GL_g(1); its share of total wealth
is s_g GL_g(1)/Σ_h s_h GL_h(1), with s_g the group's share; and a pooled quartile's share of wealth is the difference of
the pooled ordinates at its ends, divided by GL(1).

GL(p) for p < 1 is defined whenever the population is. GL(1), and so every share, needs the mean of A to be finite,
which needs the income measure to exist ([conditions](conditions.md#domain-rules)); where it does not, GL(1) and the
shares are `undefined`. For the paper's members the mean is finite and the variance is not, since permanent income has a
Pareto tail with index between 1 and 2 (about 1.21 to 1.47 by group under `continues`): estimates of these statistics
from a simulation converge slowly, and carry their standard errors and sample sizes.

## Diagnostics that need no reference solution (required)

**Euler residuals, at each comparison point, for each group, type and state**, as in `bst/1`, with the expectation over
next quarter's state and shocks, in the optimizer's units:

    ĉ(m̃, j) = (u′)^(−1)( β̊_i R Σ_{j′} P[j, j′] E[(𝒢(j′) ψ′)^(−ϱ) u′(c̃(m̃′, j′)) | j′] ),
    m̃′ = R (m̃ − c̃(m̃, j))/(𝒢(j′) ψ′) + ξ′(j′),

    r(m̃, j) = min( ĉ − c̃(m̃, j),  m̃ − ã_min(j) − c̃(m̃, j) ) / c̃(m̃, j),

with ã_min(j) = a_min(j)/(1 − ℷ) the optimizer's constraint in force, and m̃′ kept at or above the next state's,
ã_min(j′), below which the rule is not defined. Where c̃ = 0, at a natural limit, the residual is not defined and is left
out. The expectation is the part `diagnostics.expectation`: taken against the stated member's laws, by a method
different from the household's own, and stated with its precision. Report r at each point and the maximum of |r|.

**The stationarity residual, for each group and type**: push the reported distribution over (m̃, j) forward one quarter
under the reported rule, the chain and the shock laws, and report the largest change in the employment shares and in the
generalized Lorenz ordinates of (1 − ℷ) a.

## Status values, errors and precision, and the comparison

As in [`bst/1`](../bst-1/results.md#status-values): `undefined` where a domain rule fails, decided by the toolkit's own
verdicts; `not computed` for an optional value left out; each value with the toolkit's error estimate where it has one,
and a simulated value with its standard error and sample size; and two files compared only when their parameter-file
hashes match, with tolerances from measured convergence.

## Not in this version

- **The rule's special points by state**: the buffer stock target, the pseudo-target and the kink; the employed state's
  would come first, since nothing in the paper uses the others.
- **Welfare, mean felicity and marginal welfare.** The paper computes welfare in its experiments, from simulated total
  consumption discounted at 1/R; the stationary population's mean value is a new object, and a toolkit's value function
  is the optimizer's, not the household's with the splurge.
- **The recession regime's rule**, from which the experiments layer would start.
- **The income measure's statistics**, consumption over income by group, and the distributions of m̃ and c.

## Sketch of the form

The validator is [`results.schema.json`](results.schema.json). The shape is roughly:

```json
{
  "family": "bst-markov_ui-and-agg/1",
  "parameter_file_sha256": "…", "method_file_sha256": "…", "settings_sha256": "…", "request_file_sha256": "…",
  "toolkit": {"name": "…", "version": "…"},
  "provenance": {"hardware": "…", "threads": 1},
  "groups": [
    {
      "name": "highschool",
      "effective_member": {
        "chain": {"normal": [[0.969, 0.031, 0, 0], "…"], "recession": ["…"]},
        "by_state": {"E": {"growth": 1.0045, "growth_pow_1_minus_rho": 0.995, "growth_inverse": 0.997,
                           "psi_log": -0.0015, "psi_log_psi": 0.0015, "psi_lowest": 0.85, "income_lowest": 0.29,
                           "worst_income_probability": 0.0}, "U_2": {"…": "…"}, "U_1": {"…": "…"}, "X": {"…": "…"}},
        "theta_mean": 1.0,
        "derived": {"natural_limit": {"E": -0.23, "…": "…"}, "constraint_in_force": {"E": 0.0, "…": "…"},
                    "worst_income": {"E": 0.25, "…": "…"}}
      },
      "types": [
        {
          "beta": 0.929, "share": 0.143,
          "conditions": {"FVAC": {"factor": 0.98, "bound": 1, "holds": true},
                         "GIC-Mod": {"by_state": {"E": {"factor": 0.97, "bound": 1, "holds": true}, "…": "…"}},
                         "GIC-Harmenberg": {"status": "not computed"}, "…": "…"},
          "comparison_points": [0.42, 0.61, "…"],
          "rule": {"E": {"m": [0.42, 0.61, "…", 0.29], "c": [0.40, 0.55, "…"], "mpc": [0.91, 0.42, "…"]}, "…": "…"},
          "exported_rule": {"E": {"m": ["…"], "c": ["…"], "range": [0.29, 60.0]}, "…": "…"},
          "employment_shares": {"E": 0.956, "U_2": 0.029, "U_1": 0.0097, "X": 0.0048},
          "wealth": {"gl": {"0.01": 0.0, "…": "…", "1": 1.3}, "median": 0.7},
          "paper_mpc": {"mean": 0.42, "mean_mpc": 0.21},
          "euler_residuals": {"by_state": {"E": {"r": [1e-6, -2e-6], "max_abs": 2e-6}, "…": "…"}, "max_abs": 2e-6,
                              "expectation_method": "…", "expectation_precision": 1e-9},
          "stationarity_residual": 3e-9
        }
      ],
      "levels": {"gl": {"0.2": 0.4, "0.4": 2.9, "0.6": 9.6, "0.8": 24.0, "1": 52.0}, "median_ratio": 0.7,
                 "paper_mpc": {"mean": 0.42, "mean_mpc": 0.21}}
    }
  ],
  "pooled": {"levels": {"gl": {"0.25": 1.1, "0.5": 7.3, "0.75": 25.0, "1": 63.0},
                        "paper_mpc": {"mean": 0.42, "mean_mpc": 0.21},
                        "paper_mpc_by_quartile": [{"mean": 0.6, "mean_mpc": 0.4}, "…"]}}
}
```
