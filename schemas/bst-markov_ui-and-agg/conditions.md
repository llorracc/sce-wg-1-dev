# bst-markov_ui-and-agg/1: conditions and implications

Draft, 2026-10-18; see the [README](../README.md) and the [model schema](model.md).

This document carries [`bst/1`'s conditions](../bst-1/conditions.md) over to the family with the employment chain. It
keeps that document's four kinds of statement, validity conditions, domain rules, implications and the simulation phase,
all computed exactly by the checker from the parameter file, the chain and the [shock laws'](../shock-laws.md)
closed-form moments. What changes: the household's state carries the employment state j; the growth factor and the law
of the permanent shock vary with j under `grows` and `frozen`; income in the unemployed states is an atom; the borrowing
constraint in force depends on the state; and the conditions that are scalar inequalities in `bst/1` become conditions
on a matrix over the chain, which reduce to `bst/1`'s under `continues`. The stationary problem is the normal regime's,
since normal is absorbing, so the chain below is the normal regime's. The derivations are of 2026-10-18 and are
deductions unless a check is named.

## Notation

For one group and its type i:
- P is the normal regime's chain over J = {E, U_2, U_1, X}, with `sep` and `find` the normal-times probabilities, and π
  its stationary distribution. With `sep` > 0 and `find` > 0 the chain is irreducible and aperiodic.
- 𝒢(j) and the law of ψ given j are the model schema's: 𝒢(E) = 𝒢 with ψ drawn from its law; in a quarter of
  unemployment, 𝒢(j) = 𝒢 with ψ drawn under `continues`, 𝒢(j) = 𝒢 with ψ = 1 under `grows`, and 𝒢(j) = 1 with ψ = 1
  under `frozen`.
- `ξ_min(j)` is the lowest income in state j: e `θ_min` in E, ξ_u in U_2 and U_1, ξ_x in X; and `ψ_min(j)` is the lowest
  value of ψ in j, the law's lowest value where ψ is drawn and 1 where it is fixed.
- Þ̊_i = (R β̊_i)^(1/ϱ), with β̊_i = β_i ℒ, is the absolute patience factor with survival, and `κ_min` = max(0, 1 −
  Þ̊_{R,i}) is its limiting MPC as m → ∞, as in `bst/1`.
- For a function f of next quarter's state and shock, M_f is the matrix with entries M_f[j, j′] = P[j, j′] E[f(j′, ψ′) |
  j′], and λ(M_f) is its dominant eigenvalue, which exists and is positive since the entries are. Under `continues`, f
  depends on j′ only through 𝒢(j′) = 𝒢 and the law of ψ is the same in every state, so M_f = E[f] P and λ(M_f) = E[f]:
  every condition below is then `bst/1`'s with the group's 𝒢.

## The constraint in force, by state

With u(0) = −∞ the household never lets next quarter's worst income force zero consumption, in any state it can reach,
and it never ends a quarter below the artificial limit `a_Art`. A state's limit must therefore keep feasible the
constraint in force, artificial or natural, in every state that can follow, and the constraint in force solves, over the
states,

    a_min(j) = max( a_Art,  max over j′ with P[j, j′] > 0 of  (𝒢(j′) ψ_min(j′)/R) (a_min(j′) − ξ_min(j′)) ),

a fixed point that a few iterations from zero reach, each bracket being nonpositive. HARK's Markov solver computes the
same recursion: a state's natural bound comes from the next states' lowest resources, which already carry the artificial
limit. The **natural limits** `a_Nat(j)` are the same recursion without `a_Art`: the constraint in force of a member
written with `borrowing_constraint: natural`. In `bst/1`, one state, the recursion gives `a_min` = max(`a_Art`, `a_Nat`)
with `a_Nat` = −`ξ_min` `ψ_min`/(ℛ − `ψ_min`) and ℛ = R/𝒢. In the chain the artificial limit has to sit inside the
recursion: taking max(`a_Art`, `a_Nat(j)`) after the fact understates the limit of a state that can be followed by one
in which the artificial limit binds, since the first must leave room for the second. Consequences:
- With lognormal laws, `θ_min` = 0 and `ψ_min` = 0 in the employed state, which can follow every state, so its term is
  zero, every other term is negative, and `a_min(j)` = max(`a_Art`, 0) = 0 in every state and under every value of the
  switch. The stage file's single limit, with `a_Nat: 0.0`, is therefore exact for every member it states.
- With truncated laws the limits are negative and can differ by state. They are the same in every state when the
  employed state's term, a candidate everywhere, is the largest, as at the paper's calibration under `continues`. They
  differ when a state's own worst income is low enough for its term to be the larger, as for the paper's low-benefits
  member, whose exhaustion income lies below the employed floor; and an artificial limit above the lowest natural limit
  binds in some states and, through the recursion, tightens the limits of the states that can precede them. A larger
  multiplier 𝒢(j′) `ψ_min(j′)`/R, which the unemployed states have under `grows` and `frozen`, makes a state's term more
  negative and so can only loosen the limits of the states before it.
- A stage file with bounded laws needs the per-state limits, which the language can state as four calibrated values
  selected by j, computed by the checker until the language can derive them. A toolkit's effective member, whose laws
  are discrete, has state-dependent limits in general and reports them per state. With the paper's `a_Art` = 0 the
  constraint in force is zero in every state, whatever the laws.

## Validity conditions

A member that fails any of these is rejected:
- the parameter domains of the [model schema](model.md) and the rules of the [shock laws](../shock-laws.md); the shares
  summing to one within each group and across groups;
- `a_Art` ≤ 0 and, for one written form, above the lowest of the natural limits `a_Nat(j)`, since an artificial limit at
  or below it binds in no state and describes the same model as `natural`; or `natural`, for no artificial limit;
- for every group and type, the FVAC and the RIC or the WRIC of the table below.

BST's existence theorem is for independent income with bounded support and ϱ > 1. For the chain the family requires the
analogous conditions, with the dominant eigenvalue in place of the expectation; a theorem is an open point.

## The conditions

Each condition is `bst/1`'s with the chain's matrix in place of the scalar; the right-hand column gives the `continues`
form, which is `bst/1`'s with the group's 𝒢.

| Condition | Inequality | Under `continues` |
|---|---|---|
| AIC | Þ̊ < 1 | the same |
| RIC | Þ̊_R < 1 | the same |
| WRIC | `p_worst(j)`^(1/ϱ) Þ̊_R < 1 in every state, with `p_worst(j)` the probability from j that next quarter's income is its worst | Þ̊_R < 1 when no law has an atom at its floor, since `p_worst` = 0 |
| FHWC | λ(M_f) < 1 with f = 𝒢(j′) ψ′/R | 𝒢/R < 1 |
| PF-FVAC | λ(M_f) < 1 with f = β̊ 𝒢(j′)^(1−ϱ) | β̊ 𝒢^(1−ϱ) < 1 |
| FVAC | λ(M_f) < 1 with f = β̊ (𝒢(j′) ψ′)^(1−ϱ) | β̊ 𝒢^(1−ϱ) E[ψ^(1−ϱ)] < 1 |
| GIC, by state | R (1 − `κ_min`) < E[𝒢(j′) ψ′ \| j] | ℛ (1 − `κ_min`) < 1 |
| GIC-Mod, by state | R (1 − `κ_min`) E[1/(𝒢(j′) ψ′) \| j] < 1 | ℛ (1 − `κ_min`) E[ψ^(−1)] < 1 |
| GIC-Szeidl | with ℒ = 1: log(R (1 − `κ_min`)) < Σ_z π(j) (log 𝒢(j) + E[log ψ \| j]) | log(ℛ (1 − `κ_min`)) < E[log ψ] |
| GIC-Harmenberg | with ℒ = 1: the same under the income measure's chain and E[ψ log ψ \| j] | ℛ (1 − `κ_min`) < exp(E[ψ log ψ]) |
| GIC-Liv | ℒ λ(M_f) < 1 with f = R (1 − `κ_min`)/𝒢(j′) | ℒ ℛ (1 − `κ_min`) < 1 |

The worst-income probability `p_worst(j)` is the probability, from j, of reaching next quarter a state whose income
floor is the worst reachable one and of drawing that floor there: zero unless both the state's income is an atom and ψ
there is fixed or has mass at its floor. Under `grows` and `frozen` the unemployed states' income is an atom and ψ there
is fixed, so from U_1 and X the probability of the exhaustion income ξ_x next quarter is 1 − `find`; whether that is the
worst income from those states depends on whether ξ_x lies below the employed floor e `θ_min` `ψ_min`, which for the
paper's calibration it does not under truncated laws and cannot under lognormal ones, where the employed floor is zero
and has no mass.

## Domain rules

A quantity a member does not define is reported as `undefined`.

The special points of the rule, in each state j:
- **The buffer stock target m̂_i(j)**, where E[m′ | m, j] = m for a survivor, needs the GIC-Mod of state j, as the table
  writes it.
- **The pseudo-target m̌_i(j)**, where E[𝐦′ | j]/𝐦 equals the expected growth of permanent income from j, E[𝒢(j′) ψ′ |
  j], needs the GIC of state j, as the table writes it.
- **The kink m*_i(j)** needs the artificial limit to be the constraint in force in that state and to lie strictly above
  the limit the following states impose: `a_min(j)` = `a_Art` > max over successors j′ of (𝒢(j′)
  `ψ_min(j′)`/R)(`a_min(j′)` − `ξ_min(j′)`).

The stationary population over (m, j), for each group and type:

**With ℒ < 1:**
- **Population measure.** It exists for every valid member: a mixture over ages with geometric weights, the fixed point
  of a map that contracts at rate ℒ, as in `bst/1`, the chain adding a finite state.
- **Its moments.** The moment of order q of m is finite exactly when q < ε, where ε > 0 solves ℒ λ(M_f) = 1 with
  f = (R (1 − `κ_min`)/(𝒢(j′) ψ′))^ε; when no root exists every moment is finite. Under `continues` this is `bst/1`'s
  root ℒ E[(ℛ (1 − `κ_min`)/ψ)^ε] = 1.
- **Income measure.** It exists when ℒ λ(M_f) < 1 with f = 𝒢(j′) ψ′, which is ℒ 𝒢 < 1 under `continues`. Its moment of
  order q is finite exactly when ℒ λ(M_f) < 1 with f = (R (1 − `κ_min`)/(𝒢(j′) ψ′))^q 𝒢(j′) ψ′, which under `continues`
  is ℒ 𝒢 (ℛ (1 − `κ_min`))^q E[ψ^(1−q)] < 1. Under `continues` the measure's transition factorizes, permanent income
  being independent of the state; under `grows` and `frozen` it is computed on the joint law of (m, j, 𝐩).

**With ℒ = 1:** the population measure needs the GIC-Szeidl and the income measure the GIC-Harmenberg, in the forms of
the table, with the moments' roots as above without the factor ℒ.

**The levels.** Statistics in levels need the distribution of permanent income 𝐩 itself, a mixture over ages of the
newborn's level law carried forward by the state-dependent growth. Its moment of order q is finite exactly when q < ε_𝐩,
where ε_𝐩 solves ℒ λ(M_f) = 1 with f = (𝒢(j′) ψ′)^ε, which under `continues` is ℒ 𝒢^ε E[ψ^ε] = 1. The mean of 𝐩 is
finite exactly when the income measure exists. For the paper's calibration ε_𝐩 is a little above one, so the mean of 𝐩
is finite and its variance is not: the Pareto tail of permanent income that perpetual youth with lifelong growth
produces, which the levels Lorenz curve of wealth inherits in its upper tail. A pooled statistic in levels is defined
when it is defined for every group and type.

Statistics that need less: the generalized Lorenz ordinates for p < 1 whenever the distribution exists; a pooled
statistic when every component is defined.

**Population welfare** W_i, the mean felicity F_i and marginal welfare M_i are defined when the stationary population
exists and the welfare conditions of the simulation phase hold.

## Implications

Exact consequences of the parameters, which the comparison tests a results file against:
- **The limiting MPC.** In every state, c_i′(m, j) → 1 − Þ̊_{R,i} as m → ∞ under the RIC, and → 0 when it fails.
- **The constraint in force by state**, from the fixed point above, and the natural limits by state; zero in every state
  under lognormal laws.
- **The worst income by state**, `ξ_min(j)` `ψ_min(j)`, and the probability `p_worst(j)`.
- **The newborn's lowest resources.** A newborn's m is at least e `θ_min`, and exactly that when θ has mass at its
  floor.
- **The employment marginal of the stationary population.** Since newborns are born employed, it is not the chain's
  stationary distribution π but μ = (1 − ℒ) e_E (I − ℒ P)^(−1), with e_E the unit row of the employed state: the chain's
  distribution with a flow (1 − ℒ) reborn into E each quarter. With ℒ = 1 it is π. A toolkit that places newborns
  otherwise will miss it.
- **The tail exponents** ε of the two measures and ε_𝐩 of the level distribution.
- **Consistency of the rule and the distribution.** The laws of a and c under the stationary population are the images
  of the law of (m, j) under the rule and the observation map.
- **The reduction to `bst/1`.** A member written as the [model schema](model.md) describes solves the same problem as
  its `bst/1` original, so every statistic of the two agrees exactly, the natural constraint, the targets and the tail
  exponents included.

## The simulation phase

**Positivity.** Survivors satisfy it by the constraint in force in their state, an implication of ϱ > 1. Newborns
satisfy it by the family's convention: born employed with no assets, so m = e θ > 0 under every shock law.

**The welfare conditions.** As in `bst/1`, W_i and F_i are finite exactly when E[(m − `m_min(j)`)^(−(ϱ−1))] is under the
stationary population, and M_i exactly when E[(m − `m_min(j)`)^(−ϱ)] is, with `m_min(j)` the lowest resources in state j
from which positive consumption is feasible. The cases are `bst/1`'s, taken state by state:
- Where the artificial limit is the constraint in force and lies strictly above the limit the following states impose,
  the rule keeps consumption above a positive value in that state.
  With truncated laws and the paper's `a_Art` = 0 this is every state, and all three means are finite.
- With lognormal laws, every state's limit is zero, the natural one, and an artificial limit of zero binds nowhere;
  resources near zero are reached only in the employed state, with a density that vanishes faster than any power, since
  θ is lognormal, while the unemployed states' incomes are positive atoms. Every moment is then finite, as in `bst/1`'s
  thin-density case.
- A member with an atom at the worst income and no binding constraint, such as `income_without_benefits` below the
  employed floor under truncated laws with `borrowing_constraint: natural`, falls under `bst/1`'s atom case with the
  chain's runs in place of the i.i.d. runs: the condition is ℒ λ(M_f) < 1 with f = `p_worst(j′)`^(1 − q/ϱ) (𝒢(j′)
  ψ′/Þ̊_i)^q on the states where the atom is the worst income, at q = ϱ − 1 for W_i and F_i and q = ϱ for M_i. That form
  is a deduction from `bst/1`'s, not yet checked.

So every member of the paper's calibration, in any of the three worlds and with either family of laws, defines W, F and
M; the checker reports the case it falls under.

## The stated member and the effective member

As for [`bst/1`](../bst-1/conditions.md#the-stated-member-and-the-effective-member): every statement above is defined
for the stated member and for a toolkit's effective member alike, and decided for each by the same arithmetic on its own
expectations. Here the expectations a toolkit reports are conditional on the next state, E[(𝒢(j′) ψ′)^k | j′] for the
powers the conditions use, E[log ψ | j′] and E[ψ log ψ | j′], with the chain's rows, from which the dominant eigenvalues
are arithmetic; and the lowest values by state, `ξ_min(j)` and `ψ_min(j)`, from which the constraints in force by state
are the fixed point above. The definition of a law's lowest value as the limit of a representation's bottommost point,
and its consequence that truncated laws keep every effective member in the stated member's regime, carry over unchanged.

## Open points

- **A theorem.** Existence of the household's problem's solution with the chain, and the Kesten–Goldie-type result
  behind the tail exponents with a Markov-modulated factor, are not cited; the forms above are the natural
  generalizations and reduce to `bst/1`'s, which were checked numerically for the atom case.
- **The per-state limits in a stage file with bounded laws**: four calibrated limits selected by j, which the language
  can state (tested 2026-10-19); they wait for the truncated lognormal's family in Bellman-SYM.
- **The targets by state** are defined by analogy and have not been checked against a solution.
- **The income measure's chain** for the GIC-Harmenberg with ℒ = 1 is stated in words only.
- **The boundary cases.** Equality in any condition is left open.
