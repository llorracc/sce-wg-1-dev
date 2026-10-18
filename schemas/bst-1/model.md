# bst/1: the model schema

Draft; see the [README](../README.md).

This document states the math of the family `bst/1` ("buffer-stock theory, version 1"). A parameter file names one member of
the family by giving every free parameter. Together with this document, it is a complete statement of a model, with no
numerical content. The companion documents give the family's [regularity conditions](regularity.md) and its
[results schema](results.md). The [shock laws](../shock-laws.md) and the treatment of [numerical methods](../numerics.md) are
shared with other families.

## Population

- A continuum of agents of unit mass, in K permanent types. Type k has population share ω_k and discount factor β_k. Every other
  primitive is common to all types.
- Perpetual youth: an agent alive at the end of period t−1 survives into t with probability L, with 0 < L ≤ 1, independently of
  everything else. A dead agent is replaced at once by a **newborn** of its type, so the shares never change.

## Income

- Permanent income: P_t = G ψ_t P_{t−1}, where ψ is a positive shock with E[ψ] = 1.
- Transitory income is θ_t P_t:
  - with probability ℧ (unemployment), θ = μ, with μ ≥ 0;
  - otherwise θ = ξ (1 − ℧μ)/(1 − ℧), where ξ is a positive shock with E[ξ] = 1.

  Hence E[θ] = 1.
- ψ, ξ and the unemployment event are independent of each other, over time and across agents.
- The laws of ψ and ξ are parameters, each one of the [shock laws](../shock-laws.md). The usual choice is a truncated lognormal.

## Events within a period, in order

1. Survival is drawn.
2. A survivor draws ψ_t and θ_t. Then P_t = G ψ_t P_{t−1}, and market resources are M_t = R A_{t−1} + θ_t P_t.
3. A newborn arrives with P_t = 1 and no assets. It draws θ_t but not ψ_t, so M_t = θ_t.
4. The agent consumes C_t, and end-of-period assets are A_t = M_t − C_t ≥ −b P_t.

In ratios to permanent income, a survivor's resources evolve as

    m_{t+1} = R a_t / (G ψ_{t+1}) + θ_{t+1}.

## Preferences and markets

- Utility is u(C) = C^(1−ρ)/(1−ρ), with ρ > 0, and log utility when ρ = 1. Lifetime utility is E Σ_s (β_k L)^s u(C_{t+s}).
- Death ends utility, and there is no bequest motive.
- There is no annuity market: survivors earn R, not R/L. What becomes of the assets of the dead is outside the household's
  problem.
- The borrowing limit b ≥ 0 is a parameter, and may not exceed the natural borrowing limit. With μ = 0 the natural limit is
  zero, so b = 0.

## The household's problem, one for each type

    v_k(m) = max over 0 < c ≤ m + b of  u(c) + β_k L E[(G ψ')^(1−ρ) v_k(m')],
    m'     = R (m − c)/(G ψ') + θ'.

Its solution is the **consumption rule** c_k(m) and the value v_k(m). The **Euler equation** in ratio form is

    u'(c_k(m)) ≥ β_k L R E[(G ψ')^(−ρ) u'(c_k(m'))],

with equality wherever c_k(m) < m + b.

## The stationary population

For each type, the stationary population is the distribution of m that the events above leave unchanged. Equivalently, it is
the distribution of a at the end of the period. It is counted under two measures:
- the **population measure**, which gives each agent weight one;
- the **income measure**, which weights each agent by its permanent income P and is normalized to total weight one. This is the
  permanent-income-neutral measure of Harmenberg (2021).

[Regularity conditions](regularity.md) says when each exists and which of its moments are finite. Pooled statistics weight the
types by their shares ω_k.

## What the family fixes, so that no parameter file can state it

- E[ψ] = 1, E[ξ] = 1, and the scaling of the employed draw.
- A newborn's P = 1 and a = 0, and its first transitory draw without ψ.
- The order of events above.

## Addressable parts

A method file ([numerical methods](../numerics.md)) says how a toolkit computes each part of the model. It names the part by
one of the addresses below, or by a kind, such as `expectation`, which covers every part of that kind. The parts belong to the
model, not to any method.

| Address | Kind | The part |
|---|---|---|
| `household.choice` | `maximization` | the maximization over c in the household's problem |
| `household.expectation.permanent_shock` | `expectation` | the expectation over ψ′ in the household's problem |
| `household.expectation.transitory_shock` | `expectation` | the expectation over θ′, unemployment included, in the household's problem |
| `household.rule` | `representation` | how c_k(m) is represented between the points where it is computed |
| `population.transition.permanent_shock` | `transition` | ψ in the population's law of motion |
| `population.transition.transitory_shock` | `transition` | θ in the population's law of motion |
| `population.distribution` | `distribution` | the computation of the stationary population |
| `diagnostics.expectation` | `expectation` | the expectation in the Euler residuals of the [results](results.md), which must differ from the household's |

Each part exists once for each type, and a method may be given for all types or for one.

## The parameter file

A parameter file is YAML in a strict subset, with no anchors, tags or merge keys. It holds the free parameters, under these
names:
- `crra` (ρ);
- `types`, a list of `{beta, share}`;
- `survival` (L);
- `return` (R);
- `borrowing_limit` (b);
- `income`, holding `growth` (G), `permanent_shock` (the law of ψ), `unemployment: {prob, income}` (℧ and μ) and
  `employed_shock` (the law of ξ).

Every free parameter appears, and nothing is left to a toolkit's defaults. A member with the usual truncated laws:

    family: bst/1
    period: quarter
    crra: 2.0
    types: [{beta: 0.98, share: 0.5}, {beta: 0.99, share: 0.5}]
    survival: 0.99375
    return: 1.01
    borrowing_limit: 0.0
    income:
      growth: 1.0
      permanent_shock: {TruncatedLogNormal: {sd_log: 0.0548, bot: -3.0, top: 3.0}}
      unemployment: {prob: 0.05, income: 0.15}
      employed_shock: {TruncatedLogNormal: {sd_log: 0.3464, bot: -3.0, top: 3.0}}

The community library's buffer-stock model (QuantEcon community-library pull request 5, annual period) is the member with:
- K = 1 and L = 1;
- ℧ = 0.005 and μ = 0;
- G = 1.03, R = 1.04, β = 0.96 and ρ = 2;
- untruncated lognormal ψ and ξ, each with standard deviation of the log 0.1.

    family: bst/1
    period: year
    crra: 2.0
    types: [{beta: 0.96, share: 1.0}]
    survival: 1.0
    return: 1.04
    borrowing_limit: 0.0
    income:
      growth: 1.03
      permanent_shock: {LogNormal: {sd_log: 0.1}}
      unemployment: {prob: 0.005, income: 0.0}
      employed_shock: {LogNormal: {sd_log: 0.1}}

Two names collide with the community library's. It writes the full transitory shock as ξ and its lognormal part as θ, the
reverse of this document. And it uses b for the bank balance R a/(G ψ), where this document uses b for the borrowing limit.
