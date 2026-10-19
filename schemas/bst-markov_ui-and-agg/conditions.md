# bst-markov_ui-and-agg/1: conditions and implications

Draft, 2026-10-18; see the [README](../README.md) and the [model schema](model.md).

This document carries [`bst/1`'s conditions](../bst-1/conditions.md) over to the family with the employment chain. It keeps
that document's four kinds of statement, validity conditions, domain rules, implications and the simulation phase, all
computed exactly by the checker from the parameter file, the chain and the [shock laws'](../shock-laws.md) closed-form
moments. What changes: the household's state carries the employment state z; the growth factor and the law of the
permanent shock vary with z under `grows` and `frozen`; income in the unemployed states is an atom; the natural borrowing
constraint depends on the state; and the conditions that are scalar inequalities in `bst/1` become conditions on a matrix
over the chain, which reduce to `bst/1`'s under `continues`. The stationary problem is the normal regime's, since normal is
absorbing, so the chain below is the normal regime's. The derivations are of 2026-10-18 and are deductions unless a check is
named.

## Notation

For one group and its type i:
- P is the normal regime's chain over Z = {E, U_2, U_1, X}, with π_eu and π_ue the normal-times probabilities, and π its
  stationary distribution. With π_eu > 0 and π_ue > 0 the chain is irreducible and aperiodic.
- Γ(z) and the law of ψ given z are the model schema's: Γ(E) = 𝒢 with ψ drawn from its law; in a quarter of unemployment,
  Γ = 𝒢 with ψ drawn under `continues`, Γ = 𝒢 with ψ = 1 under `grows`, and Γ = 1 with ψ = 1 under `frozen`.
- ξ̲(z) is the lowest income in state z: e θ̲ in E, ξ_U in U_2 and U_1, ξ_X in X; and ψ̲(z) is the lowest value of ψ in z, the
  law's lowest value where ψ is drawn and 1 where it is fixed.
- Þ_i = (R β_i ℒ)^(1/ρ) is the absolute patience factor, and Þ̄_i = min(Þ_i, R), as in `bst/1`.
- For a function f of next quarter's state and shock, M_f is the matrix with entries M_f[z, z′] = P[z, z′] E[f(z′, ψ′) | z′],
  and λ(M_f) is its dominant eigenvalue, which exists and is positive since the entries are. Under `continues`, f depends on
  z′ only through Γ(z′) = 𝒢 and the law of ψ is the same in every state, so M_f = E[f] P and λ(M_f) = E[f]: every condition
  below is then `bst/1`'s with the group's 𝒢.

## The natural borrowing constraint, by state

With u(0) = −∞ the household never lets next quarter's worst income force zero consumption, in any state it can reach. The
natural constraint therefore solves, over the states,

    a̲_Nat(z) = max over z′ with P[z, z′] > 0 of  (Γ(z′) ψ̲(z′)/R) (a̲_Nat(z′) − ξ̲(z′)),

a fixed point that a few iterations from zero reach, each bracket being nonpositive. When the chain is i.i.d. and the
state has one income floor, this is `bst/1`'s a̲_Nat = −ξ̲_min κ/(1 − κ) with κ = ψ̲ 𝒢/R. Three consequences:
- With lognormal laws, θ̲ = 0 and ψ̲ = 0 in the employed state, which is reachable from every state, so a̲_Nat(z) = 0 for every
  z; the calibration files' `a_Nat: 0.0` is right for them.
- With truncated laws the natural constraint is negative, and it can differ by state. The employed state is reachable from
  every state, so its term is a candidate everywhere; the constraint is the same in every state whenever that term is the
  largest, which it is when the employed floor e θ̲ ψ̲ is the lowest income and the multipliers are equal, as under
  `continues` at the paper's calibration, where a̲_Nat is then `bst/1`'s formula with ξ̲_min = e θ̲. It differs by state when
  an unemployed branch's term is larger: a replacement income below the employed floor, as in the paper's low-benefits
  member, or a larger multiplier on the unemployed branch, as under `frozen`, where Γ ψ̲ is 1 rather than 𝒢 ψ̲.
- The constraint in force in state z is a̲(z) = max(a̲_Art, a̲_Nat(z)). The stage file carries one entry `a_Nat`; a per-state
  entry, selected by z, is proposed to the owner, since a member whose natural constraint differs by state and whose
  `borrowing_constraint` is `natural` has no single value to write. With the paper's a̲_Art = 0 the constraint in force is 0
  in every state and the point is moot.

## Validity conditions

A member that fails any of these is rejected:
- the parameter domains of the [model schema](model.md) and the rules of the [shock laws](../shock-laws.md); the shares
  summing to one within each group and across groups;
- a̲_Nat(z) ≤ a̲_Art ≤ 0 for every z, for one written form, or `natural`, which means a̲_Art = a̲_Nat(z) in each state;
- for every group and type, the FVAC and the RIC or the WRIC of the table below.

BST's existence theorem is for independent income with bounded support and ρ > 1. For the chain the family requires the
analogous conditions, with the dominant eigenvalue in place of the expectation; a theorem is an open point.

## The conditions

Each condition is `bst/1`'s with the chain's matrix in place of the scalar; the right-hand column gives the `continues` form,
which is `bst/1`'s with the group's 𝒢.

| Condition | Inequality | Under `continues` |
|---|---|---|
| AIC | Þ < 1 | the same |
| RIC | Þ/R < 1 | the same |
| WRIC | p̲(z)^(1/ρ) Þ/R < 1 in every state, with p̲(z) the probability from z that next quarter's income is its worst | Þ/R < 1 when no law has an atom at its floor, since p̲ = 0 |
| FHWC | λ(M_f) < 1 with f = Γ(z′) ψ′/R | 𝒢/R < 1 |
| PF-FVAC | λ(M_f) < 1 with f = β ℒ Γ(z′)^(1−ρ) | β ℒ 𝒢^(1−ρ) < 1 |
| FVAC | λ(M_f) < 1 with f = β ℒ (Γ(z′) ψ′)^(1−ρ) | β ℒ 𝒢^(1−ρ) E[ψ^(1−ρ)] < 1 |
| GIC, by state | Þ̄ < E[Γ(z′) ψ′ \| z] | Þ̄/𝒢 < 1 |
| GIC-Mod, by state | Þ̄ E[1/(Γ(z′) ψ′) \| z] < 1 | Þ̄ E[ψ^(−1)]/𝒢 < 1 |
| GIC-Szeidl | with ℒ = 1: log Þ̄ < Σ_z π(z) (log Γ(z) + E[log ψ \| z]) | log(Þ̄/𝒢) < E[log ψ] |
| GIC-Harmenberg | with ℒ = 1: the same under the income measure's chain and E[ψ log ψ \| z] | Þ̄/𝒢 < exp(E[ψ log ψ]) |
| GIC-Liv | ℒ λ(M_f) < 1 with f = Þ̄/Γ(z′) | ℒ Þ̄/𝒢 < 1 |

The worst-income probability p̲(z) is the probability, from z, of reaching next quarter a state whose income floor is the
worst reachable one and of drawing that floor there: zero unless both the state's income is an atom and ψ there is fixed or
has mass at its floor. Under `grows` and `frozen` the unemployed states' income is an atom and ψ there is fixed, so from U_1
and X the probability of the exhaustion income ξ_X next quarter is 1 − π_ue; whether that is the worst income from those
states depends on whether ξ_X lies below the employed floor e θ̲ ψ̲, which for the paper's calibration it does not under
truncated laws and cannot under lognormal ones, where the employed floor is zero and has no mass.

## Domain rules

A quantity a member does not define is reported as `undefined`.

The special points of the rule, in each state z:
- **The buffer stock target m̌_i(z)**, where E[m′ | m, z] = m for a survivor, needs the GIC-Mod of state z with Þ̄.
- **The pseudo-target m̂_i(z)**, where E[M′ | z]/M equals the expected growth of permanent income from z, E[Γ(z′) ψ′ | z],
  needs the GIC of state z with Þ̄.
- **The kink m*_i(z)** needs the artificial constraint to bind in that state: a̲_Art > a̲_Nat(z).

The stationary population over (m, z), for each group and type:

**With ℒ < 1:**
- **Population measure.** It exists for every valid member: a mixture over ages with geometric weights, the fixed point of a
  map that contracts at rate ℒ, as in `bst/1`, the chain adding a finite state.
- **Its moments.** The moment of order j of m is finite exactly when j < ζ, where ζ > 0 solves ℒ λ(M_f) = 1 with
  f = (Þ̄/(Γ(z′) ψ′))^ζ; when no root exists every moment is finite. Under `continues` this is `bst/1`'s root
  ℒ E[(Þ̄/(𝒢 ψ))^ζ] = 1.
- **Income measure.** It exists when ℒ λ(M_f) < 1 with f = Γ(z′) ψ′, which is ℒ 𝒢 < 1 under `continues`. Its moment of order
  j is finite exactly when ℒ λ(M_f) < 1 with f = (Þ̄/(Γ(z′) ψ′))^j Γ(z′) ψ′, which under `continues` is
  ℒ 𝒢 (Þ̄/𝒢)^j E[ψ^(1−j)] < 1. Under `continues` the measure's transition factorizes, permanent income being independent of
  the state; under `grows` and `frozen` it is computed on the joint law of (m, z, P).

**With ℒ = 1:** the population measure needs the GIC-Szeidl and the income measure the GIC-Harmenberg, in the forms of the
table, with the moments' roots as above without the factor ℒ.

**The levels.** Statistics in levels need the distribution of permanent income P itself, a mixture over ages of the newborn's
level law carried forward by the state-dependent growth. Its moment of order j is finite exactly when j < ζ_P, where ζ_P
solves ℒ λ(M_f) = 1 with f = (Γ(z′) ψ′)^ζ, which under `continues` is ℒ 𝒢^ζ E[ψ^ζ] = 1. The mean of P is finite exactly when
the income measure exists. For the paper's calibration ζ_P is a little above one, so the mean of P is finite and its
variance is not: the Pareto tail of permanent income that perpetual youth with lifelong growth produces, which the levels
Lorenz curve of wealth inherits in its upper tail. A pooled statistic in levels is defined when it is defined for every group
and type.

Statistics that need less: the generalized Lorenz ordinates for p < 1 whenever the distribution exists; a pooled statistic
when every component is defined.

**Population welfare** W_i, the mean felicity F_i and marginal welfare M_i are defined when the stationary population exists
and the welfare conditions of the simulation phase hold.

## Implications

Exact consequences of the parameters, which the comparison tests a results file against:
- **The limiting MPC.** In every state, c_i′(m, z) → 1 − Þ_i/R as m → ∞ under the RIC, and → 0 when it fails.
- **The natural borrowing constraint by state**, from the fixed point above; zero in every state under lognormal laws.
- **The worst income by state**, ξ̲(z) ψ̲(z), and the probability p̲(z).
- **The newborn's lowest resources.** A newborn's m is at least e θ̲, and exactly that when θ has mass at its floor.
- **The employment marginal of the stationary population.** Since newborns are born employed, it is not the chain's
  stationary distribution π but μ = (1 − ℒ) e_E (I − ℒ P)^(−1), with e_E the unit row of the employed state: the chain's
  distribution with a flow (1 − ℒ) reborn into E each quarter. With ℒ = 1 it is π. A toolkit that places newborns otherwise
  will miss it.
- **The tail exponents** ζ of the two measures and ζ_P of the level distribution.
- **Consistency of the rule and the distribution.** The laws of a and c under the stationary population are the images of the
  law of (m, z) under the rule and the observation map.
- **The reduction to `bst/1`.** A member written as the [model schema](model.md) describes solves the same problem as its
  `bst/1` original, so every statistic of the two agrees exactly, the natural constraint, the targets and the tail exponents
  included.

## The simulation phase

**Positivity.** Survivors satisfy it by the natural constraint of their state, an implication of ρ > 1. Newborns satisfy it
by the family's convention: born employed with no assets, so m = e θ > 0 under every shock law.

**The welfare conditions.** As in `bst/1`, W_i and F_i are finite exactly when E[(m − m̲(z))^(−(ρ−1))] is under the
stationary population, and M_i exactly when E[(m − m̲(z))^(−ρ)] is, with m̲(z) the lowest resources in state z from which
positive consumption is feasible. The cases are `bst/1`'s, taken state by state:
- Where the artificial constraint binds, a̲_Art > a̲_Nat(z), the rule keeps consumption above a positive value in that state.
  With truncated laws and the paper's a̲_Art = 0 this is every state, and all three means are finite.
- With lognormal laws, a̲_Nat(z) = a̲_Art = 0 and the constraint binds nowhere; resources near zero are reached only in the
  employed state, with a density that vanishes faster than any power, since θ is lognormal, while the unemployed states'
  incomes are positive atoms. Every moment is then finite, as in `bst/1`'s thin-density case.
- A member with an atom at the worst income and no binding constraint, such as `income_without_benefits` below the employed
  floor under truncated laws with `borrowing_constraint: natural`, falls under `bst/1`'s atom case with the chain's runs in
  place of the i.i.d. runs: the condition is ℒ λ(M_f) < 1 with f = p̲(z′)^(1 − q/ρ) (Γ(z′) ψ′/Þ_i)^q on the states where the
  atom is the worst income, at q = ρ − 1 for W_i and F_i and q = ρ for M_i. That form is a deduction from `bst/1`'s, not yet
  checked.

So every member of the paper's calibration, in any of the three worlds and with either family of laws, defines W, F and M;
the checker reports the case it falls under.

## The stated member and the effective member

As for [`bst/1`](../bst-1/conditions.md#the-stated-member-and-the-effective-member): every statement above is defined for
the stated member and for a toolkit's effective member alike, and decided for each by the same arithmetic on its own
expectations. Here the expectations a toolkit reports are conditional on the next state, E[(Γ(z′) ψ′)^k | z′] for the
powers the conditions use, E[log ψ | z′] and E[ψ log ψ | z′], with the chain's rows, from which the dominant eigenvalues
are arithmetic; and the lowest values by state, ξ̲(z) and ψ̲(z), from which the natural limits by state are the fixed
point above. The definition of a law's lowest value as the limit of a representation's bottommost point, and its
consequence that truncated laws keep every effective member in the stated member's regime, carry over unchanged.

## Open points

- **A theorem.** Existence of the household's problem's solution with the chain, and the Kesten–Goldie-type result behind
  the tail exponents with a Markov-modulated factor, are not cited; the forms above are the natural generalizations and
  reduce to `bst/1`'s, which were checked numerically for the atom case.
- **The per-state natural constraint in the stage file**, proposed to the owner above.
- **The targets by state** are defined by analogy and have not been checked against a solution.
- **The income measure's chain** for the GIC-Harmenberg with ℒ = 1 is stated in words only.
- **The boundary cases.** Equality in any condition is left open.
