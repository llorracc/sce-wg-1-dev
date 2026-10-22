# bst/1: the model schema

Draft; see the [README](../README.md).

This document states the family `bst/1` ("buffer-stock theory, version 1"): the model of Carroll's *Theoretical Foundations
of Buffer Stock Saving* (BST), with discount-factor types, perpetual youth, and a transitory shock whose worst value may be
positive. Its notation is BST's, with SolvingMicroDSOPs' where BST is silent. The household's problem is also stated in
Bellman-SYM, in [`bellman/buffer_stock.bl`](bellman/buffer_stock.bl); that stage file is the foundation of the statement.
The file's names are this document's plain-text names, given in the notation below, except ℘, which the language refuses
and the file spells `p_zero`. It writes the constraint in force as `max(a_Art, a_Nat)`, with `a_Nat` an entry of the
calibration that the laws determine; the language records `max` as a callable the solver supplies, as it does `log`, so a
solver bound to the stage must honor it. This document adds what the language does not yet state: the population of types, the newborn, the stationary population,
the shock laws outside Bellman's families, and the conditions. A parameter file names one member of the family by giving
every free parameter. The companion documents give the family's [conditions and implications](conditions.md) and its
[results schema](results.md); the [shock laws](../shock-laws.md) and the treatment of [numerical methods](../numerics.md)
are shared with other families.

## Notation

Each symbol has two spellings.
- **Typeset,** in LaTeX, MathJax or MyST, a symbol is written as BST writes it. A minimum is underlined, as in
  `\underline{\psi}`, and a subscript that is a word is set upright, as in `\underline{a}_{\mathrm{Art}}`, never `a_{Art}`. A
  level is bold, as in `\mathbf{p}`.
- **In plain text,** in these documents' prose, the stage file's identifiers and code, a minimum, underlined when
  typeset, is a name in code font, as `ψ_min` is; so is a symbol whose subscript is a word, as `a_Art` is. Marks above a
  letter, a hat, a check or a tilde, stay as they are, since terminals draw them on their letters.

A plain-text name is never pasted into LaTeX as it stands: `ξ_min` is `\underline{\xi}`, or `\xi_{\min}`, when typeset.

| typeset | plain text | meaning | source |
|---|---|---|---|
| `\psi`, `\underline{\psi}` | ψ, `ψ_min` | the permanent shock, E[ψ] = 1, and its lowest value | BST |
| `\xi`, `\underline{\xi}` | ξ, `ξ_min` | the transitory shock, the ratio of income to permanent income, and its lowest value, the worst transitory income: the lower of ξ_U and the employed draw's lowest value `θ_min` (1 − ℘ξ_U)/(1 − ℘) | BST |
| `\theta`, `\underline{\theta}` | θ, `θ_min` | the employed draw, E[θ] = 1, and its lowest value | BST |
| `\sigma_{\psi}`, `\sigma_{\theta}` | σ_ψ, σ_θ | the standard deviations of log ψ and log θ, the parameters of the lognormal laws the stage file writes | BST |
| `\wp` | ℘, `p_zero` in the stage file | the probability of the unemployment event, BST's zero-income event | BST |
| `\xi_{\mathrm{U}}` | ξ_U | income while unemployed, as a ratio to permanent income; 0 in BST, where it is the lowest value of ξ; in general it need not be the lowest | BST's ξ, subscripted as the Markov family writes it; econ-ark's `\IncUnemp` and HARK's `IncUnemp` |
| `p_{\mathrm{worst}}` | `p_worst` | the probability of the worst income ψξ; ℘ in BST's case | this family |
| `\mathcal{L}` | ℒ | the probability of surviving into the next period | BST |
| `\mathcal{G}` | 𝒢 | the growth factor of permanent income | BST (SolvingMicroDSOPs: Γ) |
| `R`, `\beta`, `\rho` | R, β, ρ | the return factor, the discount factor, relative risk aversion | BST |
| `m`, `c`, `a` | m, c, a | market resources, consumption and end-of-period assets, as ratios to permanent income | BST |
| `\underline{m}` | `m_min` | the lowest market resources from which positive consumption is feasible | BST |
| `\mathbf{p}`, `\mathbf{m}`, `\mathbf{c}`, `\mathbf{a}` | 𝐩, 𝐦, 𝐜, 𝐚 | permanent income, and market resources, consumption and end-of-period assets in levels | BST |
| `k`, `b` | k, b | beginning-of-period capital (last period's a) and bank balances b = R k/(𝒢ψ) | BST |
| `\underline{a}_{\mathrm{Art}}`, `\underline{a}_{\mathrm{Nat}}`, `\underline{a}` | `a_Art`, `a_Nat`, `a_min` | the artificial borrowing constraint, the natural one, and the one in force, max(`a_Art`, `a_Nat`) | SolvingMicroDSOPs' `\underline{a}`; HARK's names |
| `\textbf{Þ}` | Þ | the absolute patience factor (R β ℒ)^(1/ρ) | BST |
| `\underline{\kappa}` | `κ_min` | the limiting MPC as m → ∞, max(0, 1 − Þ/R); the saving share a/m tends to 1 − `κ_min` | BST; econ-ark's `\MPCmin` |
| `\mathcal{R}` | ℛ | R/𝒢, the return factor normalized by growth | BST; econ-ark's `\RNrmByG` |

## Population

- A continuum of agents of unit mass, in K permanent types. Type i has population share ω_i and discount factor β_i. Every other
  primitive is common to all types.
- Perpetual youth: an agent alive at the end of period t−1 survives into t with probability ℒ, with 0 < ℒ ≤ 1, independently
  of everything else. A dead agent is replaced at once by a **newborn** of its type, so the shares never change.

## Income

- Permanent income: 𝐩_t = 𝒢 ψ_t 𝐩_{t−1}, where ψ is a positive shock with E[ψ] = 1.
- Transitory income is ξ_t 𝐩_t:
  - with probability ℘, the unemployment event, ξ = ξ_U, with ξ_U ≥ 0; BST's baseline is ξ_U = 0, the zero-income event;
  - otherwise ξ = θ (1 − ℘ξ_U)/(1 − ℘), where θ is a positive shock with E[θ] = 1.

  Hence E[ξ] = 1. The scale needs 0 ≤ ℘ < 1 and ℘ξ_U < 1, so that employed income is positive.
- ψ, θ and the unemployment event are independent of each other, over time and across agents. The expectation over (ψ′, ξ′)
  is over the product of their laws; a method that treats the two shocks separately composes as the product rule.
- The laws of ψ and θ are parameters, each one of the [shock laws](../shock-laws.md). The usual choice is a truncated lognormal.
  BST assumes bounded support for both shocks.

## Events within a period, in order

1. Survival is drawn.
2. A survivor draws ψ_t and ξ_t. Then 𝐩_t = 𝒢 ψ_t 𝐩_{t−1}, bank balances are b_t = R k_t/(𝒢 ψ_t) with k_t = a_{t−1}, and market
   resources are m_t = b_t + ξ_t.
3. A newborn is **born employed**: it arrives with 𝐩_t = 1 and k_t = 0, and its first transitory draw is the employed branch of
   ξ, so m_t = θ_t (1 − ℘ξ_U)/(1 − ℘) > 0. No newborn can draw the unemployment event.
4. The agent consumes c_t, and end-of-period assets are a_t = m_t − c_t ≥ `a_min`.

In ratios to permanent income, a survivor's resources evolve as

    m_{t+1} = R a_t / (𝒢 ψ_{t+1}) + ξ_{t+1}.

## Preferences and markets

- Utility is u(c) = c^(1−ρ)/(1−ρ) with ρ > 1, as BST assumes; log utility is outside the family for now. Lifetime utility
  is E Σ_s (β_i ℒ)^s u(𝐜_{t+s}).
- Death ends utility, and there is no bequest motive.
- There is no annuity market: survivors earn R, not R/ℒ. What becomes of the assets of the dead is outside the household's
  problem.
- The borrowing constraint in force is `a_min` = max(`a_Art`, `a_Nat`). The artificial constraint `a_Art` ≤ 0 is a parameter; the natural
  constraint `a_Nat` is an implication of the model, given in [conditions](conditions.md): with u(0) = −∞ the household never
  lets next period's worst income force zero consumption, so `a_Nat` = −`ξ_min` `ψ_min`/(ℛ − `ψ_min`) with ℛ = R/𝒢,
  where `ξ_min` and `ψ_min` are the lowest values of ξ and ψ. With BST's zero-income event, or with any law unbounded
  below, `a_Nat` = 0.
- For one written form, a parameter file writes `a_Art` no lower than `a_Nat`: a looser artificial constraint never binds and would
  describe the same model.

## Parameter domains

β_i > 0 (the validity conditions bound it above); ω_i > 0 with Σ ω_i = 1; ρ > 1; 0 < ℒ ≤ 1; R > 0; 𝒢 > 0; 0 ≤ ℘ < 1;
ξ_U ≥ 0 with ℘ξ_U < 1; `a_Nat` ≤ `a_Art` ≤ 0.

## The household's problem, as the stage file states it

The stage file [`bellman/buffer_stock.bl`](bellman/buffer_stock.bl) states one type's problem in five blocks, read here in
BST's notation. k is last period's a, the arrival state; `[>]` marks next period's value and `[<]` this period's arrival
value.

- **Sets and parameters.** m ∈ ℝ; a ∈ [`a_min`, ∞) with `a_min` = max(`a_Art`, `a_Nat`); the unemployment event e ∈ {employed,
  unemployed}; the parameters β, ℒ, ρ, R, 𝒢, `a_Art`, `a_Nat`, σ_ψ, σ_θ, ℘ and ξ_U, with the domains above. The stage
  file writes one law family, the lognormal, for ψ and θ; the family allows any of the shock laws, and a member with
  another law needs a stage file written with that law's family. A discrete law can be written today as a mixture of
  point masses, and the uniform with Bellman-SYM's `Uniform(a, b)`, since 2026-10-20. The truncated lognormal's family is
  in review, and the tabulated law has none yet. The file declares σ_ψ and σ_θ positive: a zero spread is the degenerate
  law, another family in the language.
- **Shocks.** ψ ~ LogNormal(−σ_ψ²/2, σ_ψ); θ ~ LogNormal(−σ_θ²/2, σ_θ); e ~ Bernoulli(℘). The three are independent of each
  other and of the state.
- **Arrival to decision** (`arvl_to_dcsn`): ξ = ξ_U in the unemployment event, else θ (1 − ℘ξ_U)/(1 − ℘); m = R k/(𝒢 ψ)
  + ξ.
- **Decision to continuation** (`dcsn_to_cntn`): a = m − c.
- **Continuation to decision** (`cntn_to_dcsn`): V = u(c) + β ℒ V[>]; dV = u′(c).
- **Decision to arrival** (`dcsn_to_arvl`): V[<] = E_{ψ,θ,e}[(𝒢 ψ)^(1−ρ) V]; dV[<] = E_{ψ,θ,e}[R (𝒢 ψ)^(−ρ) dV].
- **The policy** (`policy`): c = argmax over 0 < c ≤ m − `a_min` of u(c) + β ℒ V[>], written as documentation; the operative line
  is the Euler equation with its complementarity clause, u′(c) = β ℒ dV[>] ⟂ m − c ≥ `a_min`.

Composing the blocks across the period gives the recursion in the form BST writes it, for type i:

    v_i(m) = max over 0 < c ≤ m − a_min of  u(c) + β_i ℒ E[(𝒢 ψ′)^(1−ρ) v_i(m′)],
    m′     = R (m − c)/(𝒢 ψ′) + ξ′,

whose solution is the **consumption rule** c_i(m) and the value v_i(m), and the **Euler equation** in ratio form,

    u′(c_i(m)) ≥ β_i ℒ R E[(𝒢 ψ′)^(−ρ) u′(c_i(m′))],

with equality wherever c_i(m) < m − `a_min`. The identification of V[>] with next period's V[<], and the stationarity of v_i, are
what the stage file does not impose: it states one period, and the family states the fixed point.

## The stationary population

For each type, the stationary population is the distribution of m that the events above leave unchanged. Equivalently, it is
the distribution of a at the end of the period. It is counted under two measures:
- the **population measure**, which gives each agent weight one;
- the **income measure**, which weights each agent by its permanent income 𝐩 and is normalized to total weight one. This is the
  permanent-income-neutral measure of Harmenberg (2021).

**Population welfare** of type i is W_i = E[v_i(m)] under its stationary population, and pooled welfare is Σ ω_i W_i.
The [results](results.md) also report the mean felicity E[u(c_i(m))] and the mean marginal utility E[u′(c_i(m))], which
is the marginal welfare of a unit of resources. [Conditions](conditions.md) says when each measure exists, which of its
moments are finite, and when these means are finite. Pooled statistics weight the types by their shares ω_i.

## Derived parameters

Quantities the parameters determine that enter the model's statement. The checker computes each for the stated member, in
closed form for the admitted laws; a toolkit solves its effective member on that member's own terms, so it uses its
effective member's own values and reports them ([results](results.md), [`effective-member.md`](../effective-member.md)).

| Derived parameter | Formula | Inputs | Where it enters |
|---|---|---|---|
| the employed-income scale | (1 − ℘ξ_U)/(1 − ℘) | ℘, ξ_U | the income map, so that E[ξ] = 1; fixed by the family and the same under every representation |
| the worst income | `ξ_min` `ψ_min`, with `ξ_min` the lowest value of ξ and `ψ_min` of ψ | the laws' lowest values | the natural limit; the lower tail of the stationary population |
| its probability `p_worst` | the mass at the worst income | the laws' masses at their lowest values | the WRIC; the MPC at the lower limit; the atom case of the welfare conditions |
| the natural borrowing limit `a_Nat` | −`ξ_min` `ψ_min`/(ℛ − `ψ_min`) with ℛ = R/𝒢; none when `ψ_min` ≥ ℛ | `ξ_min`, `ψ_min`, 𝒢, R | the constraint in force |
| the constraint in force `a_min` | max(`a_Art`, `a_Nat`) | `a_Art`, `a_Nat` | the budget; the kink's existence |

A law's lowest value is defined as the limit of a representation's bottommost point as its number of points grows: for the
admitted laws, the truncation point, or zero for a law unbounded below ([conditions](conditions.md)).

## What the family fixes, so that no parameter file can state it

- E[ψ] = 1, E[θ] = 1, and the scaling (1 − ℘ξ_U)/(1 − ℘) of the employed draw.
- A newborn's 𝐩 = 1 and k = 0, and that it is born employed.
- The order of events above.

## Method targets

A method file ([numerical methods](../numerics.md)) says how a toolkit computes each part of the model. It names the part by
the stage file's own target, as Bellman's methods files do: a block's id, a block's line, or an operator's name, which covers
every occurrence. Two parts have no target in the stage, since it states one period and no population; they keep names of
the schema's own. Each part exists once for each type, and a method may be given for all types or for one.

| Target | What it computes | Comment |
|---|---|---|
| `policy` | the choice of c: the root of the Euler line, or the maximization | the endogenous grid method, time iteration or value iteration attach here |
| `evaluate` | the rule c_i(m) between the points where it was computed | linear, cubic Hermite or spline interpolation; Bellman's name for the policy's evaluation |
| `dcsn_to_arvl` | the expectation over ψ′, θ′ and the unemployment event in the value and marginal-value lines | the quadrature of each shock is a setting of this one part, since the stage writes one joint expectation; `dcsn_to_arvl.value` and `dcsn_to_arvl.marginal` name the two lines separately |
| `E_{ψ,θ,e}` | every occurrence of the joint expectation | the operator-name form, which covers both lines at once |
| `cntn_to_dcsn.value` | the value V, and hence population welfare | `value-function` keeps it; a method that drops it reports welfare from simulated utility instead |
| `arvl_to_dcsn` | the population's transition: how ψ, θ and the event move the forward measure | the forward builder's method, for a toolkit that pushes a distribution rather than agents |
| `population.distribution` | the stationary population, the fixed point of the forward map | no stage target: Monte Carlo, a histogram, or the eigenvector of a transition matrix |
| `diagnostics.expectation` | the expectation in the Euler residuals of the [results](results.md) | no stage target; its method must differ from the one on `dcsn_to_arvl` |

## The parameter file

A parameter file is YAML in a strict subset, with no anchors, tags or merge keys. It holds the free parameters, under these
names:
- `crra` (ρ);
- `types`, a list of `{beta, share}` (β_i, ω_i), in increasing order of `beta`, with no repeat;
- `survival` (ℒ);
- `return` (R);
- `borrowing_constraint` (`a_Art`), a number no greater than 0 and no less than `a_Nat`, or the word `natural` for `a_Art` = `a_Nat`;
- `income`, holding `growth` (𝒢), `permanent_shock` (the law of ψ), `unemployment: {prob, income}` (℘ and ξ_U) and
  `employed_shock` (the law of θ).

Every free parameter appears, and nothing is left to a toolkit's defaults. With `prob` 0, `income` is 0, so that the file has
one written form. The toy of the buffer-stock benchmark, with its true model's truncated laws:

    family: bst/1
    period: quarter
    crra: 2.0
    types:
      - {beta: 0.822, share: 0.14285714285714285}
      - {beta: 0.850, share: 0.14285714285714285}
      - {beta: 0.878, share: 0.14285714285714285}
      - {beta: 0.906, share: 0.14285714285714285}
      - {beta: 0.934, share: 0.14285714285714285}
      - {beta: 0.962, share: 0.14285714285714285}
      - {beta: 0.990, share: 0.14285714285714285}
    survival: 0.99375
    return: 1.01
    borrowing_constraint: 0.0
    income:
      growth: 1.0019026
      permanent_shock: {TruncatedLogNormal: {sd_log: 0.05477225575051661, bot: -3.0, top: 3.0}}
      unemployment: {prob: 0.044, income: 0.7}
      employed_shock: {TruncatedLogNormal: {sd_log: 0.34641016151377546, bot: -3.0, top: 3.0}}

The community library's buffer-stock model (QuantEcon community-library pull request 5, annual period) is BST's own version:
K = 1 and ℒ = 1; ℘ = 0.005 with ξ_U = 0; 𝒢 = 1.03, R = 1.04, β = 0.96 and ρ = 2; untruncated lognormal ψ and θ, each
with standard deviation of the log 0.1:

    family: bst/1
    period: year
    crra: 2.0
    types: [{beta: 0.96, share: 1.0}]
    survival: 1.0
    return: 1.04
    borrowing_constraint: 0.0
    income:
      growth: 1.03
      permanent_shock: {LogNormal: {sd_log: 0.1}}
      unemployment: {prob: 0.005, income: 0.0}
      employed_shock: {LogNormal: {sd_log: 0.1}}

The community library follows BST's notation: bold ξ for the transitory shock and θ for its positive part, b for the bank
balance relative to next period's permanent income, 𝒢 for growth, ℘ for the zero-income probability, and bold letters for
levels. It departs in one name: it writes relative risk aversion as γ, where BST and these schemas write ρ.
