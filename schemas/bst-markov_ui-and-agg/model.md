# bst-markov_ui-and-agg/1: the model schema

Draft, 2026-10-18; see the [README](../README.md) and the design note
[Describing HAFiscal's household models](../hafiscal-models-and-test-suite.md), whose decisions this document states.

This document states the family `bst-markov_ui-and-agg/1`: buffer-stock theory with Markov employment and
unemployment-insurance states and an aggregate regime, the household problem of HAFiscal (Carroll, Crawley, Du,
Frankovic and Tretvoll, *Welfare and Spending Effects of Consumption Stimulus Policies*). It is
[`bst/1`](../bst-1/model.md) with five additions and one convention change: employment as a Markov chain with a benefit
countdown and exhaustion; groups of types; a level law for the newborn's permanent income; the splurge, as an
observation map on the standard rule; the aggregate regime, normal or recession, as a Markov state; and employed income
e θ with the scale e a parameter. Its notation is BST's, with SolvingMicroDSOPs' where BST is silent. The household's
problem is stated in Bellman-SYM, in [`bellman/bst_markov_ui.bl`](bellman/bst_markov_ui.bl); that stage file is the
foundation of the statement, and this document adds what the language does not state: the groups and types, the newborn,
the splurge, the stationary population, the shock laws outside Bellman's families, and the conditions. A parameter file
names one member by giving every free parameter. The family's [conditions](conditions.md) and [results
schema](results.md) are companion documents; the [shock laws](../shock-laws.md) and the treatment of [numerical
methods](../numerics.md) are shared with other families.

## Notation

Everything in [`bst/1`'s table](../bst-1/model.md#notation) keeps its meaning. The family adds:

| typeset | plain text | meaning | source |
|---|---|---|---|
| `z` | z | the employment state, in Z = {E, U_2, U_1, X}: employed; unemployed with two quarters of benefits left, this one included; unemployed with one quarter left; unemployed without benefits | the paper's chain, named as the stage file names it |
| `\mathrm{reg}` | `reg` | the regime, normal or recession; not r, which is the interest rate in econ-ark's notation | the paper |
| `\mathcal{G}` | 𝒢 | the group's growth factor of permanent income; the paper writes Γ_e | BST |
| `\mathcal{G}_{t}`, `\mathcal{G}(z)` | 𝒢_t, 𝒢(z) | the growth factor applied in quarter t, and as a function of the state: 𝒢 when employed, and 𝒢, 𝒢 or 1 in a quarter of unemployment by the switch; the stage file writes `𝒢_t` | BST's 𝒢, dated |
| `e` | e | the scale of employed income, e θ; 1 in the paper | the convention change |
| `\xi_{\mathrm{U}}`, `\xi_{\mathrm{X}}` | ξ_U, ξ_X | income with benefits and without, as ratios to permanent income; the paper's ρ_b and ρ_nb, renamed because ρ is risk aversion | BST's ξ |
| `\mathrm{sep}`, `\mathrm{find}` | `sep`, `find`; by regime, `sep_n`, `sep_r`, `find_n` and `find_r` in the stage file | the probabilities of losing a job and of finding one, each by regime; `sep` is the group's | econ-ark's notation (`\sepRte`, `\jobFindPrb`); the paper's π_eu and π_ue |
| `p_{\mathrm{exit}}` | `p_exit` | the probability that a recession ends in a quarter; not h, which is human wealth | the paper's expected recession length |
| `P_{\mathrm{u}}` | P_u | the switch for permanent income in a quarter of unemployment: `continues`, `grows` or `frozen` | this family |
| `\gimel` | ℷ | the splurge, the share of income consumed before the choice | econ-ark's notation (`\splurge`); the paper writes ς |
| `\underline{\xi}(z)`, `\underline{\psi}(z)` | `ξ_min(z)`, `ψ_min(z)` | the lowest income and the lowest permanent shock in state z | BST's minima, by state |
| `\underline{a}(z)`, `\underline{a}_{\mathrm{Nat}}(z)`, `\underline{m}(z)` | `a_min(z)`, `a_Nat(z)`, `m_min(z)` | the constraint in force in state z, the natural limit in state z, and the lowest market resources in state z | this family |
| `p_{\mathrm{worst}}(z)` | `p_worst(z)` | the probability of the worst income in state z | this family |

The two spellings follow [`bst/1`'s rule](../bst-1/model.md#notation).

## Population

- Groups, each with a population share, a growth factor 𝒢, a job-loss probability by regime, a level law for the
  newborn's permanent income, and a list of types. The paper's groups are dropout, high school and college. A group is
  referred to by its name, never by an index.
- Within a group, K types with shares and discount factors β_i; a type's weight in the population is its group's share
  times its share within the group. Every other primitive is common.
- Perpetual youth: survival into the next quarter with probability ℒ, 0 < ℒ ≤ 1, independent of everything else, with no
  maximum age. A dead household is replaced at once by a newborn of its group and type.

## The chains

Two Markov states are drawn each quarter, the regime first.

- **The regime** `reg_t` is drawn from the row of `reg_{t−1}`: from normal, normal with probability one; from recession,
  normal with probability `p_exit` and recession otherwise. Normal is absorbing: a recession never begins inside the
  household's problem. The onset of a recession is an event of the experiments layer, which moves the population into
  the recession regime at a date; the household then knows the hazard `p_exit` of its ending.
- **The employment state** z_t is drawn from the row of z_{t−1}, with the probabilities of this quarter's regime
  `reg_t`:
  - from E: to U_2 with probability `sep`(`reg_t`), else E;
  - from U_2: to E with probability `find`(`reg_t`), else U_1;
  - from U_1: to E with probability `find`(`reg_t`), else X;
  - from X: to E with probability `find`(`reg_t`), else X.

  So a spell of unemployment pays benefits for two quarters, the quarter of job loss included, and then nothing until a
  job is found. The stage file states this two-quarter chain; a member with another number of benefit quarters is of the
  family but has no stage file until one is written for its chain, with its states named the same way.
- The regime is one for the whole economy; the employment draws are independent across households given the regime.

## Income

- **Permanent income:** 𝐩_t = 𝒢_t ψ_t 𝐩_{t−1}, with 𝒢_t and the law of ψ_t set by the employment state and the switch:
  - employed: 𝒢_t = 𝒢 and ψ_t is drawn from its law;
  - in a quarter of unemployment under `continues`: the same, 𝒢_t = 𝒢 and ψ_t drawn;
  - under `grows`: 𝒢_t = 𝒢 and ψ_t = 1;
  - under `frozen`: 𝒢_t = 1 and ψ_t = 1, so 𝐩 is unchanged.

  `continues` is the family's standard: it is the model the paper's text states, and it is the only value under which
  permanent income follows one law in every state and so is independent of the employment state. `grows` is the world of
  the paper's corrected code; `frozen` reproduces the published numbers.
- **Transitory income** is ξ_t 𝐩_t with ξ_t set by the state: e θ_t when employed, ξ_U in U_2 and U_1, ξ_X in X, where θ
  is a positive shock with E[θ] = 1. So E[ξ | employed] = e, and employed income is not rescaled for the unemployment
  probability, as it is in `bst/1`.
- ψ and θ are independent of each other, of the chains, over time and across households; θ is drawn every quarter and
  used only when employed. Their laws are parameters, each one of the [shock laws](../shock-laws.md), common to all
  groups; the paper's are untruncated lognormals, and the truncated lognormal is the recommended variant.

## Events within a quarter, in order

1. Survival is drawn.
2. The regime `reg_t` is drawn, then the employment state z_t.
3. A survivor draws ψ_t and θ_t. Then 𝐩_t = 𝒢_t ψ_t 𝐩_{t−1}, bank balances are b_t = R k_t/(𝒢_t ψ_t) with k_t = a_{t−1},
   and market resources are m_t = b_t + ξ_t.
4. A newborn is **born employed**, as in `bst/1`: z_t = E, k_t = 0, no ψ in its first quarter, and its first transitory
   draw is the employed branch, e θ_t; its permanent income 𝐩_t is drawn from its group's level law. So its market
   resources are m_t = e θ_t, in levels e θ_t 𝐩_t: a newborn holds no assets and its resources are its first income
   draw.
5. The household consumes c_t and ends the quarter with a_t = m_t − c_t ≥ `a_min(z_t)`, the constraint in force in its
   state, through the observation map below.

In ratios to permanent income, a survivor's resources evolve as

    m_{t+1} = R a_t / (𝒢_{t+1} ψ_{t+1}) + ξ_{t+1}.

## The splurge, as an observation map

The paper's household consumes a share ℷ of its income mechanically, before any choice, and chooses the rest. By
homotheticity this is the standard problem rescaled: the optimizer receives the share 1 − ℷ of income and solves the
problem the stage file states, in units of (1 − ℷ) 𝐩. With m the household's resources and ξ its income, both as ratios
to 𝐩, and c̃ the stage file's rule,

    m̃ = (m − ξ)/(1 − ℷ) + ξ,      c = (1 − ℷ) c̃(m̃) + ℷ ξ,      a = (1 − ℷ)(m̃ − c̃(m̃)).

The household's borrowing constraint a ≥ `a_min` is the optimizer's constraint m̃ − c̃ ≥ `a_min`/(1 − ℷ); the parameter
file states `a_Art` in the household's units. With ℷ = 0 the map is the identity. The MPC out of a transitory income
gain is ℷ + (1 − ℷ) c̃′(m̃), and every MPC the [results](results.md) report says which definition it uses.

## Preferences and markets

- Utility is u(c) = c^(1−ρ)/(1−ρ) with ρ > 1; lifetime utility is E Σ_s β̊_i^s u(𝐜_{t+s}), over the household's total
  consumption. Death ends utility, with no bequest motive.
- There is no annuity market: survivors earn R, not R/ℒ.
- The borrowing constraint in force depends on the employment state: `a_min(z)` is the fixed point given in
  [conditions](conditions.md), with the artificial limit `a_Art` inside the recursion, since a state's limit must keep
  feasible the constraint in force in every state that can follow. The artificial limit `a_Art` ≤ 0 is a parameter; the
  natural limits `a_Nat(z)`, the same recursion without it, are implications of the laws and the chain. With lognormal
  laws the employed state's lowest income is zero, since employed income e θ 𝐩 has infimum zero, and that state can
  follow every state, so every state's limit is zero; with truncated laws the limits are negative, can differ by state,
  and depend on the switch.
- For one written form, a parameter file writes `a_Art` above the lowest of the natural limits `a_Nat(z)`, or the word
  `natural`: an artificial limit at or below the lowest natural limit binds in no state.

## Parameter domains

β_i > 0 (the validity conditions bound it above); shares positive and summing to one within each group and across
groups; ρ > 1; 0 < ℒ ≤ 1; R > 0; 𝒢 > 0 for each group; e > 0; ξ_U > 0 and ξ_X > 0; `sep` and `find` in [0, 1] for each
regime; `p_exit` in [0, 1]; 0 ≤ ℷ < 1; `a_Art` ≤ 0 and above the lowest `a_Nat(z)`, or `natural`; the newborn's level
law has a positive mean and a standard deviation of the log that may be zero.

## The household's problem, as the stage file states it

The stage file [`bellman/bst_markov_ui.bl`](bellman/bst_markov_ui.bl) states one type's problem, for one group, in the
optimizer's units, in five blocks, read here in BST's notation. k is last quarter's a, the arrival state; `[>]` marks
next quarter's value and `[<]` this quarter's arrival value. A selector `(…)[z]` or `(…)[P_u]` in the file is read as
cases.

- **Sets and parameters.** m ∈ ℝ; a ∈ [`a_min`, ∞) with `a_min` = max(`a_Art`, `a_Nat`), one limit for every state,
  which is exact for the file's lognormal laws, under which every state's limit is zero, while a stage file with bounded
  laws needs the per-state limits of [conditions](conditions.md); z ∈ Z = {E, U_2, U_1, X}; `reg` ∈ {normal, recession};
  P_u ∈ {continues, grows, frozen}; the parameters β, ℒ, ρ, R, 𝒢, `a_Art`, `a_Nat`, σ_ψ, σ_θ, e, ξ_U, ξ_X, `p_exit`,
  `sep` and `find` by regime, with the domains above. The file writes one law family, the lognormal, for ψ and θ; the
  family allows any of the shock laws, and a member with another law needs a stage file written with that law's family:
  a discrete law can be written today as a mixture of point masses, while the truncated lognormal, the uniform and the
  tabulated law have no family in Bellman-SYM yet, the truncated lognormal's being planned.
- **Shocks.** `reg` ~ Categorical over the row of `reg_prev`; z ~ Categorical over the row of z_prev with the
  probabilities of `reg`; ψ ~ LogNormal(−σ²/2, σ) with σ = σ_ψ when employed, and in a quarter of unemployment σ_ψ under
  `continues` and 0 otherwise; θ ~ LogNormal(−σ_θ²/2, σ_θ), drawn but unused when unemployed.
- **Arrival to decision** (`arvl_to_dcsn`): 𝒢_t = 𝒢 when employed, and 𝒢, 𝒢 or 1 in a quarter of unemployment by the
  switch; ξ = e θ, ξ_U, ξ_U or ξ_X by the state; m = R k/(𝒢_t ψ) + ξ; the state and the regime are carried forward.
- **Decision to continuation** (`dcsn_to_cntn`): a = m − c, with the state and the regime carried.
- **Continuation to decision** (`cntn_to_dcsn`): V = u(c) + β̊ V[>]; dV = u′(c).
- **Decision to arrival** (`dcsn_to_arvl`): V[<] = E_{reg,z,ψ,θ}[(𝒢_t ψ)^(1−ρ) V]; dV[<] = E_{reg,z,ψ,θ}[R (𝒢_t ψ)^(−ρ)
  dV], the expectation over this quarter's regime, state and shocks given last quarter's state and regime.
- **The policy** (`policy`): c = argmax over 0 < c ≤ m − `a_min` of u(c) + β̊ V[>], written as documentation; the
  operative line is the Euler equation with its complementarity clause, u′(c) = β̊ dV[>] ⟂ m − c ≥ `a_min`. The language
  records `max` as a callable the solver supplies, as it does `log`, so a solver bound to the stage must honor the
  constraint in force.

Composing the blocks across the quarter gives the recursion in the form BST writes it, for type i of a group, with the
state (m, z, `reg`):

    v_i(m, z, `reg`) = max over 0 < c ≤ m − `a_min(z)` of  u(c) + β̊_i E[(𝒢′ ψ′)^(1−ρ) v_i(m′, z′, `reg′`) | z, `reg`],
    m′           = R (m − c)/(𝒢′ ψ′) + ξ′,

whose solution is the **consumption rule** c_i(m, z, `reg`) and the value v_i(m, z, `reg`), and the **Euler equation**
in ratio form,

    u′(c_i(m, z, `reg`)) ≥ β̊_i R E[(𝒢′ ψ′)^(−ρ) u′(c_i(m′, z′, `reg′`)) | z, `reg`],

with equality wherever c_i(m, z, `reg`) < m − `a_min(z)`. Since normal is absorbing, the rule in the normal regime is
the solution of the problem with the regime removed, and the rule in the recession regime is solved given it. The
identification of V[>] with next quarter's V[<], and the stationarity of v_i, are what the stage file does not impose:
it states one quarter, and the family states the fixed point.

## The stationary population

For each group and type, the stationary population is the joint distribution of (m, z) in the normal regime that the
events above leave unchanged; equivalently, the distribution of (a, z) at the end of the quarter. It is counted under
two measures:
- the **population measure**, which gives each household weight one;
- the **income measure**, which weights each household by its permanent income 𝐩 and is normalized to total weight one,
  Harmenberg's permanent-income-neutral measure. Under `continues`, 𝐩 is independent of z, so the income measure's
  transition factorizes as in `bst/1`; under `grows` and `frozen` it does not, and the measure is computed on the joint
  law of (m, z, 𝐩).

Statistics in levels, such as the wealth Lorenz curve the paper's estimation targets and the means test of the paper's
stimulus check, need the distribution of 𝐩 itself, which depends on the group's growth, the newborn's level law and
survival; the [results](results.md) say what is reported in levels.

**Population welfare** of a type is W_i = E[v_i(m, z, normal)] under its stationary population, with the value of the
household's total consumption, splurge included; pooled welfare weights types by their population weights. The results
also report the mean felicity and the mean marginal utility; [conditions](conditions.md) says when each is finite.

## Derived parameters

As in [`bst/1`](../bst-1/model.md#derived-parameters), computed for the stated member by the checker and used by a
toolkit from its own effective member, which it reports: the worst income by state, `ξ_min(z)` `ψ_min(z)`, and its
probability from each state; the constraint in force by state, the fixed point stated in [conditions](conditions.md)
with the artificial limit inside the recursion; and the natural limits by state, the same recursion without it. The
employed-income scale e is a parameter of this family, not a derived one.

## What the family fixes, so that no parameter file can state it

- E[ψ] = 1 and E[θ] = 1; the laws common to all groups.
- The chain's states, its transitions and the two-quarter benefit countdown of the stage file; normal absorbing.
- The three worlds of the switch, and that ψ = 1 and 𝒢_t = 1 are what `frozen` means.
- The newborn: born employed, no first-quarter ψ, the employed branch's draw, zero assets, 𝐩 from the group's level law.
- The order of events, and the form of the observation map.

## Method targets

A method file ([numerical methods](../numerics.md)) names the part it computes by the stage file's own target. Each part
exists once for each group and type, and a method may be given for all or for one.

| Target | What it computes | Comment |
|---|---|---|
| `policy` | the choice of c for each (m, z, `reg`): the root of the Euler line, or the maximization | the endogenous grid method in a Markov solver, time iteration or value iteration attach here |
| `evaluate` | the rule c_i(m, z, `reg`) between the points where it was computed | interpolation in m, state by state |
| `dcsn_to_arvl` | the expectation over `reg′`, z′, ψ′ and θ′ in the value and marginal-value lines | the quadrature of each shock and the summation over the chains are settings of this one part; `.value` and `.marginal` name the two lines |
| `E_{reg,z,ψ,θ}` | every occurrence of the joint expectation | the operator-name form |
| `cntn_to_dcsn.value` | the value V, and hence population welfare | `value-function` keeps it; a method that drops it reports welfare from simulated utility |
| `arvl_to_dcsn` | the population's transition: how the chains and the shocks move the forward measure | the forward builder's method |
| `population.distribution` | the stationary population over (m, z), the fixed point of the forward map | no stage target: Monte Carlo, a histogram, or the eigenvector of a transition matrix |
| `diagnostics.expectation` | the expectation in the Euler residuals of the [results](results.md) | no stage target; its method must differ from the one on `dcsn_to_arvl` |

## The parameter file

A parameter file is YAML in the strict subset of `bst/1`. It holds the free parameters, under these names:
- `crra` (ρ), `survival` (ℒ), `return` (R), `splurge` (ℷ), and `borrowing_constraint` (`a_Art`, a number no greater than
  0 and above the lowest natural limit `a_Nat(z)`, or the word `natural`);
- `shocks`, holding `permanent_shock` (the law of ψ) and `employed_shock` (the law of θ);
- `regimes`, holding `recession: {exit_hazard}` (`p_exit`); the normal regime has no key, since it is absorbing;
- `employment`, holding `benefit_quarters` (two for the stage file's chain), `job_finding: {normal, recession}` (`find`
  by regime), `income_employed` (e), `income_with_benefits` (ξ_U), `income_without_benefits` (ξ_X) and
  `unemployed_permanent_income` (P_u, one of `continues`, `grows` and `frozen`; never omitted);
- `groups`, a list, each with `name`, `share`, `growth` (𝒢), `job_loss: {normal, recession}` (`sep` by regime),
  `newborn_income: {mean, sd_log}` (the level law, a lognormal in the levels of the period's units) and `types`, a list
  of `{beta, share}` in increasing order of `beta` with no repeat.

Every free parameter appears, and nothing is left to a toolkit's defaults. The paper's normal-times calibration in the
family's standard world, with the laws the published code discretized:

    family: bst-markov_ui-and-agg/1
    period: quarter
    crra: 2.0
    splurge: 0.246
    survival: 0.99375
    return: 1.01
    borrowing_constraint: 0.0
    shocks:
      permanent_shock: {LogNormal: {sd_log: 0.0548}}
      employed_shock:  {LogNormal: {sd_log: 0.346}}
    regimes:
      recession: {exit_hazard: 0.1666666666666667}
    employment:
      benefit_quarters: 2
      job_finding: {normal: 0.6666666666666667, recession: 0.25}
      income_employed: 1.0
      income_with_benefits: 0.7
      income_without_benefits: 0.5
      unemployed_permanent_income: continues
    groups:
      - name: dropout
        share: 0.093
        growth: 1.0036
        job_loss: {normal: 0.062, recession: 0.051}
        newborn_income: {mean: 6200.0, sd_log: 0.32}
        types:
          - {beta: 0.943271, share: 0.142857142857142857}
          - {beta: 0.950414, share: 0.142857142857142857}
          - {beta: 0.957557, share: 0.142857142857142857}
          - {beta: 0.964700, share: 0.142857142857142857}
          - {beta: 0.971843, share: 0.142857142857142857}
          - {beta: 0.978986, share: 0.142857142857142857}
          - {beta: 0.986129, share: 0.142857142857142857}
      - name: highschool
        share: 0.527
        growth: 1.0045
        job_loss: {normal: 0.031, recession: 0.024}
        newborn_income: {mean: 11100.0, sd_log: 0.42}
        types: [the seven points of 0.98051 ± 0.01676]
      - name: college
        share: 0.380
        growth: 1.0049
        job_loss: {normal: 0.018, recession: 0.014}
        newborn_income: {mean: 14500.0, sd_log: 0.53}
        types: [the seven points of 0.99160 ± 0.00480]

The same file with `unemployed_permanent_income: frozen` is the member that reproduces the published numbers; with
`TruncatedLogNormal` laws at ±3 it is the truncated variant the shock-law document recommends. The recession's job-loss
probabilities are below the normal ones, which is consistent: with job finding falling from two thirds to a quarter, the
dropout group's steady-state unemployment rate roughly doubles, as the paper states.

## A `bst/1` member as a member of this family

One group with the `bst/1` types and `growth` = 𝒢; `job_loss` = ℘ and `job_finding` = 1 − ℘ in both regimes, so that the
chain is unemployment with probability ℘ every quarter whatever the previous state; `income_with_benefits` =
`income_without_benefits` = the `bst/1` member's ξ_U; `income_employed` = (1 − ℘ξ_U)/(1 − ℘); `splurge` 0;
`unemployed_permanent_income` `continues`; any `benefit_quarters`; `newborn_income: {mean: 1.0, sd_log: 0.0}`; and the
recession's exit hazard irrelevant, since its parameters equal the normal ones. The two families then produce the same
rule and the same stationary population exactly, the newborn convention being the same. That cross-family consistency
test belongs in the suite.
