# The buffer-stock families: the model schema

Draft; see the [README](../README.md).

This document states the four buffer-stock families, one for each borrowing-constraint scenario
([`constraint-scenarios.md`](../constraint-scenarios.md)). Their model is that of Carroll's *Theoretical Foundations of
Buffer Stock Saving* (BST), with discount-factor types, perpetual youth, and a transitory shock whose worst value may be
positive. Their notation is BST's, with SolvingMicroDSOPs' where BST is silent. They replace the single family `bst/1`.

Two of the families are principal: `bst-natural/1`, under the natural constraint, and `bst-artificial/1`, under a
binding artificial one. Their folders are in this one. The other two, `bst-natural-no-point-mass/1` and
`bst-zero-infima/1`, are in [`other/`](other/). That is the owner's ruling of 2026-11-01: the model is in practice
solved numerically under an artificial constraint, which covers the zero-infima scenario's laws once they are truncated,
and the natural scenario without a point mass is of more theoretical than practical interest. The other two remain valid families,
with their own stage files, checks and members.

| family | folder | the constraint in force | the shocks' laws | the stage file |
|---|---|---|---|---|
| `bst-natural/1` | [`natural/`](natural/) | the natural one, a > −`h_min`, never reached: the joint worst income is a point mass | bounded, with strictly positive floors and finite ceilings | [`natural.bl`](natural/bellman/natural.bl): truncated lognormals and BST's zero-income event, so `h_min` = 0 |
| `bst-natural-no-point-mass/1` | [`other/natural-no-point-mass/`](other/natural-no-point-mass/) | the natural one, a ≥ −`h_min`, reached only if ϱ < k: the joint worst income has probability zero | bounded, as above | [`natural-no-point-mass.bl`](other/natural-no-point-mass/bellman/natural-no-point-mass.bl): truncated lognormals |
| `bst-artificial/1` | [`artificial/`](artificial/) | the artificial one, a ≥ `a_Art`, strictly above −`h_min`; it binds | the floors of ψ and of ξ strictly positive | [`artificial.bl`](artificial/bellman/artificial.bl): truncated lognormals |
| `bst-zero-infima/1` | [`other/zero-infima/`](other/zero-infima/) | a ≥ 0, from both constraints, since the laws' infima are zero; it binds | ψ's or θ's infimum zero, E[θ^(−ϱ)] finite, and no zero-income event | [`zero-infima.bl`](other/zero-infima/bellman/zero-infima.bl): lognormals |

Each family's household problem is stated in Bellman-SYM in its stage file, the foundation of its statement. The files'
names are this document's plain-text names, given in the notation below, except ℘, which the language refuses and the
files spell `p_zero`. No stage file carries the natural limit as a parameter. `natural-no-point-mass.bl` writes it out
from the laws' bounds, −`h_min` = −`ξ_min` 𝒢`ψ_min`/(R − 𝒢`ψ_min`), since Bellman-SYM has no derived parameters, and the
others need none. This document adds what the language does not yet state: the population of types, the newborn, the
stationary population, the shock laws outside the stage files' families, and the conditions. A parameter file names one
member of a family by giving every free parameter. The companion documents give the families'
[conditions and implications](conditions.md) and their shared [results schema](results.md); the
[shock laws](../shock-laws.md) and the treatment of [numerical methods](../numerics.md) are shared with other families.

## Notation

Each symbol has two spellings.
- **Typeset,** in LaTeX, MathJax or MyST, a symbol is written as BST writes it. A minimum is underlined, as in
  `\underline{\psi}`, and a subscript that is a word is set upright, as in `\underline{a}_{\mathrm{Art}}`, never
  `a_{Art}`. A level is bold italic, as in `\boldsymbol{\mathit{p}}`, econ-ark's `\pLvl`.
- **In plain text,** in these documents' prose, the stage file's identifiers and code, a minimum, underlined when
  typeset, is a name in code font, as `ψ_min` is; so is a symbol whose subscript is a word, as `a_Art` is. Marks above a
  letter, a hat, a check or a tilde, stay as they are, since terminals draw them on their letters.

A plain-text name is never pasted into LaTeX as it stands: `ξ_min` is `\underline{\xi}`, or `\xi_{\min}`, when typeset.

| typeset | plain text | meaning | source |
|---|---|---|---|
| `\psi`, `\underline{\psi}` | ψ, `ψ_min` | the permanent shock, E[ψ] = 1, and its lowest value | BST |
| `\xi`, `\underline{\xi}` | ξ, `ξ_min` | the transitory shock, the ratio of income to permanent income, and its lowest value, the worst transitory income: the lower of ξ_u and the employed draw's lowest value `θ_min` (1 − ℘ξ_u)/(1 − ℘) | BST |
| `\theta`, `\underline{\theta}` | θ, `θ_min` | the employed draw, E[θ] = 1, and its lowest value | BST |
| `\sigma_{\psi}`, `\sigma_{\theta}` | σ_ψ, σ_θ | the standard deviations of log ψ and log θ, the parameters of the lognormal laws `zero-infima.bl` writes | BST |
| `\mu_{\psi}`, `s_{\psi}`, `\mu_{\theta}`, `s_{\theta}` | μ_ψ, s_ψ, μ_θ, s_θ | the location and the scale of log ψ and log θ before truncation, the parameters, with the bounds, of the truncated lognormals the other stage files write; the location makes the mean one after truncation | this family |
| `\bar{\psi}`, `\bar{\theta}` | `ψ_max`, `θ_max` | the highest values of ψ and θ, finite in the natural scenarios | BST |
| `\underline{h}` | `h_min` | the minimum present value of future noncapital income, as a ratio to permanent income: `ξ_min` 𝒢`ψ_min`/(R − 𝒢`ψ_min`), finite when 𝒢`ψ_min` < R; the natural limit is −`h_min` | HARK's hNrmMin, the owner's name for it |
| `\wp` | ℘, `p_zero` in the stage file | the probability of unemployment, whatever ξ_u; BST's zero-income event when ξ_u = 0 | BST; econ-ark's `\pZero`, HARK's `UnempPrb` |
| `\xi_{\mathrm{u}}` | ξ_u | income while unemployed, as a ratio to permanent income; 0 in BST, where it is the lowest value of ξ; in general it need not be the lowest | BST's ξ, subscripted as the Markov family writes it; econ-ark's `\IncUnemp`, HARK's `IncUnemp` |
| `p_{\mathrm{worst}}` | `p_worst` | the probability of the worst income ψξ; ℘ in BST's case | this family; econ-ark's `\pWorst`, HARK's `WorstIncPrb` |
| `\mathcal{L}` | ℒ | the probability of surviving into the next period | BST |
| `\mathcal{G}` | 𝒢 | the growth factor of permanent income | BST (SolvingMicroDSOPs: Γ) |
| `\mathsf{R}`, `\beta`, `\varrho` | R, β, ϱ | the return factor, the discount factor, relative risk aversion | BST; econ-ark's `\Rfree`, `\DiscFac` and `\CRRA` |
| `m`, `c`, `a` | m, c, a | market resources, consumption and end-of-period assets, as ratios to permanent income | BST |
| `\underline{m}` | `m_min` | the lowest market resources from which positive consumption is feasible | BST |
| `\boldsymbol{\mathit{p}}`, `\boldsymbol{\mathit{m}}`, `\boldsymbol{\mathit{c}}`, `\boldsymbol{\mathit{a}}` | 𝐩, 𝐦, 𝐜, 𝐚 | permanent income, and market resources, consumption and end-of-period assets in levels | BST; econ-ark's `\pLvl`, `\mLvl`, `\cLvl` and `\aLvl` |
| `k`, `b` | k, b | beginning-of-period kapital (last period's a) and bank balances b = R k/(𝒢ψ) | BST |
| `\underline{a}_{\mathrm{Art}}`, `\underline{a}_{\mathrm{Nat}}`, `\underline{a}` | `a_Art`, `a_Nat`, `a_min` | the artificial borrowing constraint, the natural one, −`h_min`, and the one in force: `a_Nat` in the natural scenarios, `a_Art` in the artificial one, 0 in the zero-infima one | SolvingMicroDSOPs' `\underline{a}`; HARK's names |
| `\mathring{\beta}` | β̊ | β ℒ, the discount factor with survival | econ-ark's `\DiscFacEff` |
| `\mathring{\textbf{Þ}}` | Þ̊ | the absolute patience factor with survival, (R β̊)^(1/ϱ); Þ̊_R = Þ̊/R and Þ̊_𝒢 = Þ̊/𝒢 are the return and growth patience factors | econ-ark's `\APFacEff`, `\RPFacEff` and `\GPFacEff`; BST's Þ |
| `\underline{\kappa}` | `κ_min` | the limiting MPC as m → ∞, max(0, 1 − Þ̊_R); the saving share a/m tends to 1 − `κ_min` | BST; econ-ark's `\MPCmin` |
| `\mathcal{R}` | ℛ | R/𝒢, the return factor normalized by growth | BST; econ-ark's `\RNrmByG` |

## Population

- A continuum of agents of unit mass, in K permanent types. Type i has population share ω_i and discount factor β_i.
  Every other primitive is common to all types.
- Perpetual youth: an agent alive at the end of period t−1 survives into t with probability ℒ, with 0 < ℒ ≤ 1,
  independently of everything else. A dead agent is replaced at once by a **newborn** of its type, so the shares never
  change.

## Income

- Permanent income: 𝐩_t = 𝒢 ψ_t 𝐩_{t−1}, where ψ is a positive shock with E[ψ] = 1.
- Transitory income is ξ_t 𝐩_t:
  - with probability ℘, the unemployment event, ξ = ξ_u, with ξ_u ≥ 0; BST's baseline is ξ_u = 0, the zero-income event;
  - otherwise ξ = θ (1 − ℘ξ_u)/(1 − ℘), where θ is a positive shock with E[θ] = 1.

  Hence E[ξ] = 1. The scale needs 0 ≤ ℘ < 1 and ℘ξ_u < 1, so that employed income is positive.
- ψ, θ and the unemployment event are independent of each other, over time and across agents. The expectation over (ψ′,
  ξ′) is over the product of their laws; a method that treats the two shocks separately composes as the product rule.
- The laws of ψ and θ are parameters, each one of the [shock laws](../shock-laws.md), within what the family's scenario
  allows. BST assumes bounded support for both shocks, with strictly positive floors, and the natural scenarios require
  it. The artificial scenario needs only positive floors, and the zero-infima scenario a zero infimum.

## Events within a period, in order

1. Survival is drawn.
2. A survivor draws ψ_t and ξ_t. Then 𝐩_t = 𝒢 ψ_t 𝐩_{t−1}, bank balances are b_t = R k_t/(𝒢 ψ_t) with k_t = a_{t−1}, and
   market resources are m_t = b_t + ξ_t.
3. A newborn is **born employed**: it arrives with 𝐩_t = 1 and k_t = 0, and its first transitory draw is the employed
   branch of ξ, so m_t = θ_t (1 − ℘ξ_u)/(1 − ℘) > 0. No newborn can draw the unemployment event.
4. The agent consumes c_t, and end-of-period assets are a_t = m_t − c_t ≥ `a_min`.

In ratios to permanent income, a survivor's resources evolve as

    m_{t+1} = R a_t / (𝒢 ψ_{t+1}) + ξ_{t+1}.

## Preferences and markets

- Utility is u(c) = c^(1−ϱ)/(1−ϱ) with ϱ > 1, as BST assumes; log utility is outside the family for now. Lifetime
  utility is E Σ_s β̊_i^s u(𝐜_{t+s}).
- Death ends utility, and there is no bequest motive.
- There is no annuity market: survivors earn R, not R/ℒ. What becomes of the assets of the dead is outside the
  household's problem.
- The natural constraint `a_Nat` = −`h_min` is an implication of the model, given in [conditions](conditions.md): no
  household ends a period below it, since next period's worst income could then force consumption to zero or below. With
  ℛ = R/𝒢, `a_Nat` = −`ξ_min` `ψ_min`/(ℛ − `ψ_min`), where `ξ_min` and `ψ_min` are the lowest values of ξ and ψ. With
  BST's zero-income event, or with a law whose infimum is zero, `a_Nat` = 0.
- The constraint in force, `a_min`, is the family's: `a_Nat` in the natural scenarios; the artificial constraint
  `a_Art` ≤ 0, a parameter strictly above `a_Nat`, in the artificial scenario; and 0 in the zero-infima scenario, where
  both constraints give it. Only the artificial family's parameter file states a constraint, so that each model has one
  written form, by the owner's decision of 2026-11-01.
- **The zero-infima constraint is still imposed.** Its stage file states a ≥ 0 itself, in the set of a, the feasible set
  and the Euler equation's clause, since the natural limit there comes from the laws' infima, which are zero. A toolkit
  imposes it as stated. One that took the natural limit from a discretization's lowest values would find it below zero
  and let its agents borrow, which the model rules out; HARK's adapter therefore passes `BoroCnstArt = 0.0` for such a
  member. A paper that states the constraint as an artificial one, as HAFiscal's does, writes the same model.
- **Reaching the limit.** No household ends a period below `a_min`. Whether one ends a period exactly at it, consuming c
  = m − `a_min`, is the scenario's mark: never, when the joint worst income is a point mass; only when ϱ < k, without
  one; and for m below a kink, in the artificial and zero-infima scenarios
  ([`constraint-scenarios.md`](../constraint-scenarios.md)).

## Parameter domains

β_i > 0, with no upper bound of one (the validity conditions bound it); ω_i > 0 with Σ ω_i = 1; ϱ > 1; 0 < ℒ ≤ 1;
R > 0; 𝒢 > 0; 0 ≤ ℘ < 1; ξ_u ≥ 0 with ℘ξ_u < 1; in the artificial scenario `a_Nat` < `a_Art` ≤ 0. Each scenario adds its
own requirements on the laws ([conditions](conditions.md), "Validity conditions").

## The household's problem, as the stage files state it

Each stage file states one type's problem in five blocks, read here in BST's notation. k is last period's a, the arrival
state; `[>]` marks next period's value and `[<]` this period's arrival value. The blocks are the same in the four files
except where the scenario's constraint and laws enter.

- **Sets and parameters.** m ∈ ℝ, or ℝ₊₊ where the constraint keeps resources positive; a in the set of the scenario's
  constraint: (0, ∞) in `natural.bl`; [−`h_min`, ∞) in `natural-no-point-mass.bl`; [`a_Art`, ∞) in `artificial.bl`;
  [0, ∞) in `zero-infima.bl`. The employment state j ∈ {employed, unemployed}. The parameters β, ℒ, ϱ, R, 𝒢 and ℘, with,
  by file, ξ_u, `a_Art`, and the laws' parameters.
- **Shocks.** In the truncated files, ψ ~ TruncatedLogNormal(μ_ψ, s_ψ, `ψ_min`, `ψ_max`) and θ ~
  TruncatedLogNormal(μ_θ, s_θ, `θ_min`, `θ_max`); in `zero-infima.bl`, ψ ~ LogNormal(−σ_ψ²/2, σ_ψ) and θ ~
  LogNormal(−σ_θ²/2, σ_θ); j ~ Bernoulli(℘). The three are independent of each other and of the state. A member with
  another law, such as a discrete one, needs a stage file written with that law's family.
- **Arrival to decision** (`arvl_to_dcsn`): ξ = ξ_u in the unemployment event (0 in `natural.bl`), else
  θ (1 − ℘ξ_u)/(1 − ℘); m = R k/(𝒢 ψ) + ξ.
- **Decision to continuation** (`dcsn_to_cntn`): a = m − c.
- **Continuation to decision** (`cntn_to_dcsn`): V = u(c) + β̊ V[>]; D_{m}V = u′(c), V's derivative in m.
- **Decision to arrival** (`dcsn_to_arvl`): V[<] = E_{ψ,θ,j}[(𝒢 ψ)^(1−ϱ) V]; D_{k}V[<] = E_{ψ,θ,j}[R (𝒢 ψ)^(−ϱ) D_{m}V].
- **The policy** (`policy`): c = argmax over the feasible set of u(c) + β̊ V[>], written as documentation. The operative
  line is the Euler equation: with equality, u′(c) = β̊ D_{a}V[>], in `natural.bl`, where the limit is never reached;
  with its complementarity clause, u′(c) = β̊ D_{a}V[>] ⟂ m − c ≥ `a_min`, in the other three.

Composing the blocks across the period gives the recursion in the form BST writes it, for type i:

    v_i(m) = max over 0 < c ≤ m − a_min of  u(c) + β̊_i E[(𝒢 ψ′)^(1−ϱ) v_i(m′)],
    m′     = R (m − c)/(𝒢 ψ′) + ξ′,

whose solution is the **consumption rule** c_i(m) and the value v_i(m), and the **Euler equation** in ratio form,

    u′(c_i(m)) ≥ β̊_i R E[(𝒢 ψ′)^(−ϱ) u′(c_i(m′))],

with equality wherever c_i(m) < m − `a_min`. The identification of V[>] with next period's V[<], and the stationarity of
v_i, are what the stage file does not impose: it states one period, and the family states the fixed point.

## The stationary population

For each type, the stationary population is the distribution of m that the events above leave unchanged. Equivalently,
it is the distribution of a at the end of the period. It is counted under two measures:
- the **population measure**, which gives each agent weight one;
- the **income measure**, which weights each agent by its permanent income 𝐩 and is normalized to total weight one. This
  is the permanent-income-neutral measure of Harmenberg (2021).

**Population welfare** of type i is W_i = E[v_i(m)] under its stationary population, and pooled welfare is Σ ω_i W_i.
The [results](results.md) also report the mean felicity E[u(c_i(m))] and the mean marginal utility E[u′(c_i(m))], which
is the marginal welfare of a unit of resources. [Conditions](conditions.md) says when each measure exists, which of its
moments are finite, and when these means are finite. Pooled statistics weight the types by their shares ω_i.

## Derived parameters

Quantities the parameters determine that enter the model's statement. The checker computes each for the stated member,
in closed form for the admitted laws; a toolkit solves its effective member on that member's own terms, so it uses its
effective member's own values and reports them ([results](results.md), [`effective-member.md`](../effective-member.md)).

| Derived parameter | Formula | Inputs | Where it enters |
|---|---|---|---|
| the employed-income scale | (1 − ℘ξ_u)/(1 − ℘) | ℘, ξ_u | the income map, so that E[ξ] = 1; fixed by the family and the same under every representation |
| the worst income | `ξ_min` `ψ_min`, with `ξ_min` the lowest value of ξ and `ψ_min` of ψ | the laws' lowest values | the natural limit; the lower tail of the stationary population |
| its probability `p_worst` | the mass at the worst income | the laws' masses at their lowest values | the WRIC; the MPC at the lower limit; the atom case of the welfare conditions |
| the minimum human wealth `h_min` | `ξ_min` 𝒢`ψ_min`/(R − 𝒢`ψ_min`); infinite when 𝒢`ψ_min` ≥ R | `ξ_min`, `ψ_min`, 𝒢, R | the natural limit |
| the natural borrowing limit `a_Nat` | −`h_min`, that is −`ξ_min` `ψ_min`/(ℛ − `ψ_min`) with ℛ = R/𝒢 | `h_min` | the constraint in force in the natural scenarios; the bound `a_Art` must exceed |
| the constraint in force `a_min` | `a_Nat`, `a_Art` or 0, by the scenario | the family, `a_Art`, `a_Nat` | the budget; the kink's existence |

A law's lowest value is defined as the limit of a representation's bottommost point as its number of points grows: for
the admitted laws, the truncation point, or zero for a law unbounded below ([conditions](conditions.md)).

## What the family fixes, so that no parameter file can state it

- E[ψ] = 1, E[θ] = 1, and the scaling (1 − ℘ξ_u)/(1 − ℘) of the employed draw.
- A newborn's 𝐩 = 1 and k = 0, and that it is born employed.
- The order of events above.

## Method targets

A method file ([numerical methods](../numerics.md)) says how a toolkit computes each part of the model. It names the
part by the stage file's own target, as Bellman's methods files do: a block's id, a line's id, or an operator's name,
which covers every occurrence. A method attaches only where the stage gives the computation a place of its own:
- an expectation's method goes on its operator, never on the block or the line that holds it;
- the policy's solution goes on the operator that solves the Euler line, and the rule's interpolation on the policy
  block;
- where the computation has a tag, such as `!quadrature`, the method is that tag. A toolkit's own routine is
  named as the entry's handler, and a setting the tag does not name is read by a handler, or stays in the toolkit's own
  map;
- each target takes one method.

Two parts have no target in the stage, since it states one period and no population; they keep names of the schema's
own. Each part exists once for each type, and a method may be given for all types or for one.

| Target | What it computes | Comment |
|---|---|---|
| `policy.euler.solve` | the choice of c: the root of the Euler line, iterated to the stationary rule | `!time-iteration` or `!root-find`. The stage writes the Euler equation, not a method's steps, so a toolkit's endogenous grid method is named as the handler: `!egm` attaches only to a stage that writes the method's own lines, the inverted Euler equation and the endogenous grid |
| `policy` | the rule c_i(m) between the points where it was computed | the rule's interpolation, such as `!Linear`. A cubic Hermite whose slopes are the solution's own MPCs, as HARK's is, has no tag and is named as the handler |
| `E_ψ_θ_j` | the expectation E_{ψ,θ,j} over ψ′, θ′ and the unemployment event, in the value and the marginal-value lines | the operator's name, which covers both lines: `!quadrature` for nodes that approximate the laws, `!monte-carlo` for a mean over draws, and `!sum` only where every law has finitely many outcomes. The block `dcsn_to_arvl` and its lines take no method |
| `cntn_to_dcsn.value` | the value V, and hence population welfare | `value-function` keeps it; a method that drops it reports welfare from simulated utility instead |
| `arvl_to_dcsn` | the population's transition: how ψ, θ and the event move the forward measure | the forward builder's method, such as `!histogram`, for a toolkit that pushes a distribution rather than agents |
| `population.distribution` | the stationary population, the fixed point of the forward map | no stage target: Monte Carlo, a histogram, or the eigenvector of a transition matrix |
| `diagnostics.expectation` | the expectation in the Euler residuals of the [results](results.md) | no stage target; its method must differ from the one on `E_ψ_θ_j` |

## The parameter file

A parameter file is YAML in a strict subset, with no anchors, tags or merge keys. It holds the free parameters, under
these names:
- `family`, one of the four families' keys, which chooses the scenario, its stage file and its validator;
- `crra` (ϱ);
- `types`, a list of `{beta, share}` (β_i, ω_i), in increasing order of `beta`, with no repeat;
- `survival` (ℒ);
- `return` (R);
- in `bst-artificial/1` only, `borrowing_constraint` (`a_Art`), a number no greater than 0 and strictly above `a_Nat`;
- `income`, holding `growth` (𝒢), `permanent_shock` (the law of ψ), `unemployment: {prob, income}` (℘ and ξ_u) and
  `employed_shock` (the law of θ).

Every free parameter appears, and nothing is left to a toolkit's defaults. With `prob` 0, `income` is 0, so that the
file has one written form. The toy of the buffer-stock benchmark, with its true model's truncated laws, in the
artificial scenario ([`artificial/members/toy.yaml`](artificial/members/toy.yaml)):

    family: bst-artificial/1
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

The same laws with no artificial constraint are `bst-natural-no-point-mass/1`'s member
[`toy-natural`](other/natural-no-point-mass/members/toy-natural.yaml), and the toy with untruncated lognormals is
`bst-zero-infima/1`'s [`toy-untruncated`](other/zero-infima/members/toy-untruncated.yaml).

The community library's buffer-stock model (QuantEcon community-library pull request 5, annual period) is BST's own
version, in the natural scenario with a point mass: K = 1 and ℒ = 1; ℘ = 0.005 with ξ_u = 0; 𝒢 = 1.03, R = 1.04, β =
0.96 and ϱ = 2; lognormal ψ and θ, each with standard deviation of the log 0.1. The community library's laws are
untruncated, and BST's natural scenario needs bounded ones, so the member truncates them at three standard deviations,
by the owner's decision of 2026-11-01 ([`natural/members/library.yaml`](natural/members/library.yaml)):

    family: bst-natural/1
    period: year
    crra: 2.0
    types: [{beta: 0.96, share: 1.0}]
    survival: 1.0
    return: 1.04
    income:
      growth: 1.03
      permanent_shock: {TruncatedLogNormal: {sd_log: 0.1, bot: -3.0, top: 3.0}}
      unemployment: {prob: 0.005, income: 0.0}
      employed_shock: {TruncatedLogNormal: {sd_log: 0.1, bot: -3.0, top: 3.0}}

The community library follows BST's notation: bold ξ for the transitory shock and θ for its positive part, b for the
bank balance relative to next period's permanent income, 𝒢 for growth, ℘ for the probability of unemployment, and bold
letters for levels. It departs in one name: it writes relative risk aversion as γ, where BST and these schemas write ϱ.

## The restrained-limit suite: the liquidity-constrained solution as a limit

Every toolkit's solution of the buffer-stock families is to be run on four members that state BST's experiment "The
Liquidity Constrained Solution as a Limit" (the owner's ruling of 2026-11-01). As the probability ℘ of the zero-income
event falls to zero, the consumption rule under the natural constraint converges to that of BST's "restrained"
consumer, who has no zero-income event and c ≤ m. The precautionary motive acts like a smoothed version of the
liquidity constraint.

| member | family | ℘ | constraint |
|---|---|---|---|
| [`bst-p-zero-0.005`](natural/members/bst-p-zero-0.005.yaml) | `bst-natural/1` | 0.005, BST's own; the same model as `library` | natural, a > 0, never reached |
| [`bst-p-zero-0.0005`](natural/members/bst-p-zero-0.0005.yaml) | `bst-natural/1` | 0.0005 | natural, a > 0, never reached |
| [`bst-p-zero-0.00005`](natural/members/bst-p-zero-0.00005.yaml) | `bst-natural/1` | 0.00005 | natural, a > 0, never reached |
| [`bst-restrained`](artificial/members/bst-restrained.yaml) | `bst-artificial/1` | 0 | artificial, a ≥ 0, which binds |

All four have BST's calibration (its table "Microeconomic Model Calibration"): annual; 𝒢 = 1.03, R = 1.04, β = 0.96,
ϱ = 2 and ℒ = 1; ψ and θ lognormal with standard deviation of the log 0.1, truncated at three standard deviations; and
ξ_u = 0. They differ only in ℘ and the constraint, which the checker's tests confirm. A toolkit passes when each rung's
rule is closer to the restrained rule than the rung before.

Solved with the HARK adapter's own route at precision level 1, on 2026-11-01, the largest gap between a rung's rule and
the restrained rule over m in (0, 10] is 0.138, 0.061 and 0.027 for the three rungs. It is largest at m ≈ 0.98, the
restrained rule's kink, and falls by a factor of about 2.3 for each tenfold fall in ℘. That route is HARK's Markov
consumer with two states, employed and the zero-income event, whose chain is not persistent. It implements either
scenario without changing HARK's i.i.d. solver.

## The toy-hafiscal suite: estimated types, steady states and Jacobians

The second suite every toolkit's solution is to be run on is a simplified HAFiscal, `toy-hafiscal`, specified by the
owner on 2026-11-01:
- **The model.** `bst-artificial/1` with the values of the Markov family's `iid-ui-artificial` for everything but the
  discount factors: quarterly; unemployment with probability 0.05 every quarter, whatever the last, paying 0.5 of
  permanent income; employed income scaled to mean one; the toy's laws, truncated at three standard deviations, and its
  growth, survival, return and ϱ; a ≥ 0. There is one group, no splurge and no recession. Its counterpart in the Markov
  family is `iid-ui-artificial` with the same types.
- **The types.** Three discount-factor types with equal shares, set by a center β and a spread ∇: the midpoints of
  three equal parts of [β − ∇, β + ∇], that is β − 2∇/3, β and β + 2∇/3, as HAFiscal sets its seven.
- **The calibration.** HARK's and HAFiscal's tools choose (β, ∇) to match HAFiscal's targets for the Lorenz curve of
  wealth and the whole profile of the intertemporal MPC, the iMPC. The estimation is theirs alone; no other toolkit
  estimates anything. What they deliver is a member file with the three types fixed, and a record of the targets, the
  fit and the code that produced it.
- **What every toolkit does.** It takes the member and solves and simulates the steady state: each type's consumption
  rule and the ergodic distribution, as the results schema already asks. It also exposes what is needed to compute its
  sequence-space Jacobians, so that the SSJ exercise can be done on every toolkit's steady state.

The targets, as HAFiscal's published package states and computes them (llorracc/HAFiscal-QE,
`Code/HA-Models/Target_AggMPCX_LiquWealth/Estimation_BetaNablaSplurge.py`, the model of its first estimation step,
which has one population and a one-quarter unemployment event):
- **The Lorenz curve of liquid wealth,** from the 2004 Survey of Consumer Finances (`Code/Empirical/make_liquid_wealth.py`):
  checking and savings times 1.05, plus certificates of deposit, mutual funds, stocks and bonds, less credit-card
  balances, for heads aged 25 to 62 with positive income, without the bottom 5% by permanent income or negative liquid
  wealth, with the survey's weights. The targets are the shares of total liquid wealth held by the bottom 20, 40, 60
  and 80% of households ranked by liquid wealth: 0.029%, 0.354%, 1.84% and 7.42% (`lorenz_target`).
- **The iMPC profile,** Fagereng, Holm and Natvik (2021), Figure 2: the share of a lottery prize spent in years 0 to 4,
  0.5056845, 0.1759051, 0.1035106, 0.0444222 and 0.0336616 (`Agg_MPCX_target`). The quarterly model maps to years by
  letting each winner win in a quarter of year 0 drawn uniformly and summing, in levels, each year's four quarters of
  consumption with the win less consumption without it, over the prize; year 0 so counts one to four quarters.
- **The ratio of aggregate liquid wealth to aggregate quarterly income,** 6.60 (`KY_target`), which the Lorenz shares
  cannot pin, since they do not depend on the level of wealth.
- **The objective:** the sum of squared gaps over the five years of the profile and over the four Lorenz points, with
  equal weights, plus ((K/Y − 6.60)/6.60)², as the package writes that block. The published objective's fourth block,
  on the year-0 share by wealth quartile, is left out.
- **The prize:** one prize for every winner, as the published code has it: 7,129 USD, which the code converts to 0.9602
  of quarterly permanent income. The paper describes prizes drawn across Fagereng, Holm and Natvik's sizes; the code's
  switch for that never runs.

These choices are the owner's, of 2026-11-01. Not yet settled:
- where the 6.60 is computed: the paper states it, and the package's data script does not produce it;
- what a toolkit exposes for the Jacobians, a change to what results carry that is to be drawn up with the toolkits and
  put to the owner before it is made.

