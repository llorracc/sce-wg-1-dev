# HARK's Rosetta Stone for `bst/1`

Draft, begun on 2026-10-21 and revised on 2026-10-22; see the [Rosetta Stones](README.md). The toolkit is HARK's
`MarkovConsumerType`, as [HARK's adapter](../adapters/hark/README.md) uses it: on the nonpersistent chain, which writes
a `bst/1` member as a member of the [Markov family](../bst-markov_ui-and-agg/model.md).
- **Where it was read.** The Markov solver was read at the commit of HARK's draft pull request #1858, `03a2c7a1` on the
  fork `llorracc/HARK`. The adapter's pin is `11852805`, the head of draft econ-ark/HARK#1862, stacked on it,
  which computes the natural borrowing constraint from the laws' infima. HARK's standard consumer,
  `IndShockConsumerType`, which the Markov consumer extends and against which the adapter's gate measures it, was read
  on HARK's main branch at `4c285e86`, of 2026-10-07. The figures for HARK's defaults were computed with that code.
- **The cards** are in [`hark.cards.yaml`](hark.cards.yaml).

## The lexicon

- **Timing.** Element t of `Rfree`, `PermGroFac`, `LivPrb`, `MrkvArray` and `IncShkDstn` governs the move from t to
  t + 1, and is used to solve period t. `LivPrb[t]` is survival at the end of t. An infinite horizon is `cycles = 0`
  with `T_cycle = 1`.
- **States.** The Markov consumer's inputs that can differ by state are arrays with one value per state, here two:
  employed, then unemployed. `bst/1` gives both states the same return, growth and survival.
- **Normalization.** Variables are normalized by permanent income, as in `bst/1`: `mNrm`, `aNrm` and `cNrm` are m, a and
  c.

| `bst/1` | HARK | timing and normalization | where HARK differs, and what the adapter does |
|---|---|---|---|
| ϱ, `crra` | `CRRA` | a number | — |
| β, `types[].beta`, with the shares, `types[].share` | `DiscFac` | a number | each of `bst/1`'s types is a separate agent: the adapter solves one `MarkovConsumerType` per type and pools them with the shares |
| ℒ, `survival` | `LivPrb`, a list per period of one value per state | survival at the end of t. It enters only the effective discount factor, `DiscFac`·`LivPrb`. R is not divided by ℒ, and the assets of the dead vanish | the same value in both states |
| R, `return` | `Rfree`, a list per period of one value per state | element t governs the move from t to t + 1 | the same value in both states |
| 𝒢, `income.growth` | `PermGroFac`, a list per period of one value per state | as `Rfree`. In `simulate()` the drawn `PermShk` includes it, as ψ𝒢; in the model file it does not | the same value in both states |
| ψ, `income.permanent_shock` | `PermShk` in each state's distribution in `IncShkDstn` | HARK builds it from `PermShkStd`, the σ of log ψ, and `PermShkCount`: `MeanOneLogNormal(σ)`, cut into equiprobable nodes at the conditional means of their bins | HARK has no truncated law, so the adapter builds the nodes itself: equiprobable bins of the member's law, each node its bin's exact conditional mean, the same in both states. HARK's constructor for `IncShkDstn` is switched off, and `PermShkStd` and `PermShkCount` are placeholders |
| θ, `income.employed_shock` | `TranShk` in the employed state's distribution | as ψ | the adapter's nodes, scaled by (1 − ℘ξ_u)/(1 − ℘) |
| ℘, `income.unemployment.prob` | `MrkvArray`, a list per period of the chain's matrix | row i gives the probabilities of next period's states from state i | both rows are (1 − ℘, ℘): unemployment with probability ℘ whatever the previous state, which is `bst/1`'s ξ. HARK's constructor for `MrkvArray` is switched off, since it would replace the adapter's matrix with its defaults, [[0.9, 0.1], [0.6, 0.4]], at construction. `UnempPrb`, the standard consumer's way, is left at zero |
| ξ_u, `income.unemployment.income` | `TranShk` in the unemployed state's distribution | a ratio to permanent income | ξ_u at every node of ψ, since ψ is drawn in both states. `IncUnemp` is left at zero |
| ψ and ξ jointly | `IncShkDstn`, a list per period of one distribution per state | in each state the independent product of ψ's nodes and that state's ξ | weighted by the chain's row, the two states' distributions are `bst/1`'s joint law of ψ and ξ |
| `a_Art`, `borrowing_constraint` | `BoroCnstArt` | a bound on end-of-period a. The constraint in force in each state is the larger of the natural limit and `BoroCnstArt` | the adapter passes `a_Art`, or none for a member that states `natural`. HARK then computes the natural limit itself from the laws' infima, which the adapter records as each distribution's `limit` (`BoroCnstInfimum`, on by default at the pin); it is the stated laws' limit, the same at every number of nodes |
| `a_Nat` | none stored; the solver's `mNrmMin`, one per state, is the constraint in force | at the pin, the larger of the limit from the laws' recorded infima and the one from the lowest nodes; released HARK has only the second | the adapter computes the effective member's natural limit itself, from the nodes' lowest values: −`ξ_min` `ψ_min`/(ℛ − `ψ_min`) with ℛ = R/𝒢, as `model.md` writes it. Here `ξ_min` is the lowest node of ξ, the worst income, which is the lower of ξ_u and the lowest employed node, and `ψ_min` is the lowest node of ψ. On the toy's seven equiprobable nodes the lowest employed node is 0.558, below ξ_u = 0.7. The results file reports it (`effective_member.derived.natural_limit`), with the constraint in force the larger of `a_Art` and it. The adapter asserts that both states' `mNrmMin` equal that constraint. The laws' own limit is tighter whenever ξ_u > 0, since the laws reach below their lowest nodes in both ψ and θ: it is 0 when either law is untruncated, and set by the truncation bounds when both are truncated. Under `natural` it is the constraint in force, and it binds in the effective member, whose nodes never reach it. Draft pull request econ-ark/HARK#1861 records the true bounds of HARK's own discretized laws |
| the newborn: employed, P = 1, no assets, θ an employed draw | `MrkvPrbsInit`, `NewbornTransShk`; `kLogInitMean`, `kLogInitStd` and `kNrmInitCount`; `pLogInitMean`, `pLogInitStd` and `pLvlInitCount` | in HARK's simulation, a newborn's state is drawn from `MrkvPrbsInit`, and with `NewbornTransShk` its first income from that state's distribution | the adapter sets `MrkvPrbsInit = [1, 0]` and `NewbornTransShk = True`, so that a newborn is employed with an employed draw; P = 1 would also need the `NewbornPermShk = False` of draft econ-ark/HARK#1860. HARK's simulation is not used: the adapter builds the population, newborns included, itself. k = 0 would need a very negative `kLogInitMean`; the default, −12, gives k ≈ 6·10⁻⁶ |

## Where the results file's quantities come from

| results file | HARK | note |
|---|---|---|
| the rule c(m) at the request points | `solution[0].cFunc[0]`, the employed state's | the adapter asserts that the unemployed state's rule, `cFunc[1]`, agrees to 10⁻¹² relative, as it must when every row of the chain is the same. With `CubicBool` the rule is a cubic Hermite whose slopes are the solution's own MPCs. Above the grid, a cubic rule with its limiting line can diverge or jump at the top gridpoint, which draft econ-ark/HARK#1848 fixes, so the adapter reports the rule inside the grid only |
| the value v(m) | `solution[0].vFunc[0]`, with `vFuncBool` | a value function over a cubic in pseudo-inverse value; the two states' values are asserted to agree likewise. V = P^(1−ϱ)·v(m) |
| the MPC | `cFunc[0].derivative(m)` | a cubic's slope is continuous at the knots |
| the limiting MPCs | `solution[0].MPCmin` and `MPCmax`, one per state | the solver's iterates, which approach the limits and lag them. The adapter reads neither: the checker computes the limits from the effective member's expectations |
| the kink and the two targets | none: HARK computes no targets for the Markov consumer | the adapter finds each as a root of the rule |
| the condition factors | none: the Markov consumer has no condition checks | the adapter decides every condition by the checker's arithmetic on its effective member's expectations |
| the stationary distribution | none: HARK has no transition matrix for the Markov consumer | the adapter's own lottery onto an asset grid. Since the next state does not depend on the current one, end-of-period assets are the whole state |
| welfare | none | the adapter computes it from `vFunc` |

## The method

- **The solution:** `solve_one_period_ConsMarkov`, the endogenous grid method, iterated over an infinite horizon until
  the distance between successive solutions is below `tolerance`. In the tags of the
  [method targets](../bst-1/model.md#method-targets) this is `!time-iteration` on `policy.euler.solve`, with
  `MarkovConsumerType` as its handler. The stage writes the Euler equation with its complementarity clause, not the
  endogenous grid method's steps, so `!egm` does not attach to it.
  - **The pin.** Released HARK interpolates each next state's expected marginal value on a grid starting at that state's
    own natural limit, then evaluates it on the current state's grid. When the states' worst incomes differ, as here,
    that adds an interpolation error to the rule and a larger one to the value function. Pull request #1858 evaluates
    each next state's expectation at the current state's points, as the standard solver does
    ([the finding](../records/findings/2026-10-21_hark-markov-for-bst1.md)).
  - **The tolerance.** Human wealth and the limiting MPC lag the rule's convergence. On the standard consumer, at HARK's
    defaults and its default tolerance of 10⁻⁶, `hNrm` is 44.99 against its limit of 50.50, and c above the grid is off
    by 0.0115 at m = 60 and 0.035 at m = 100, against less than 4·10⁻⁵ within the grid. `bst/1`'s population grids reach
    60, 120 and 240, so the adapter's levels set 10⁻⁸ and tighter.
  - The stage's `max(a_Art, a_Nat)` is HARK's own: the larger of `BoroCnstArt` and the natural limit it computes, in
    each state. At the pin that limit comes from the laws' recorded infima, so it is the stated member's `a_Nat`.
- **The grid:** `aXtraGrid`, end-of-period assets above the natural limit, nested multi-exponentially. Its settings are
  `aXtraMin` (by default 0.001), `aXtraMax` (20), `aXtraCount` (48), `aXtraNestFac` (3) and `aXtraExtra`.
- **The interpolation** (`policy`): linear, `!Linear`, or with `CubicBool` a cubic Hermite whose slopes are the
  solution's own MPCs, which no tag names. `vFuncBool` keeps the value function.
- **The expectation** (`E_ψ_θ_j`): over each next state's nodes in `IncShkDstn`, which the adapter supplies, weighted by
  the chain's row: `!quadrature`, since the nodes approximate continuous laws. The method file's quadrature is therefore
  the adapter's choice of nodes, not HARK's.
- **The diagnostics' expectation.** The Euler residuals are taken against the stated laws by a quadrature unlike the
  household's: the adapter's own is Gauss–Legendre in logs, split at the rule's kink.

## The adapter

The adapter is [`schemas/adapters/hark/`](../adapters/hark/README.md). In this stone's terms:
- **Encode.** The lexicon's names. The chain and the income process are the adapter's, with HARK's constructors for both
  switched off, and HARK's own income inputs are placeholders. The settings it passes are its own, not HARK's defaults:
  - `aXtraMin` = 10⁻⁶;
  - `aXtraMax`, `aXtraCount` and `aXtraNestFac` from the level's top, points and nesting, with no `aXtraExtra`;
  - `CubicBool` and `vFuncBool` set;
  - the level's `tolerance`: 10⁻⁸ at the first level, 10⁻¹⁰ at the second, and 10⁻¹² at the third and fourth.

  So the grid and the tolerance honor the method file's settings, while the endogenous grid method, the cubic
  interpolation and its approach above the grid are fixed inside.
- **The call:** `solve()`.
- **Decode.**
  - After the solve it asserts that HARK solved with the adapter's chain and income process; that the two states' rules
    and values agree to 10⁻¹² relative; and that both states' `mNrmMin` equal the effective member's constraint in
    force, to 10⁻⁹.
  - The employed state's `cFunc` and `vFunc` are read. The natural limit reported is the adapter's own, computed from
    the nodes' lowest values by the closed form above, which is also HARK's.
  - The conditions come from the checker's arithmetic on the effective member, the kink and the targets from the rule,
    and the Euler residuals from the adapter's own quadrature of the stated laws.
  - The stationary population is computed outside HARK, by a linear lottery on an asset grid, with a node at an
    artificial constraint. Deaths come at the rate 1 − ℒ, and newborns, employed, from the member's newborn law.
  - It has two measures: the households', with ψ's law as given; and the income measure, with the probabilities tilted
    by ψ and the survivors' share ℒ𝒢.

**How it departs from HARK alone:** the population, the newborns, the conditions and the targets are the adapter's own.
The population and every reported point lie below the solution grid's top, so HARK's rule above it, where a cubic can
diverge or jump, enters no reported quantity.

## The standard consumer

The adapter's gate solves each type again with `IndShockConsumerType` on the same joint nodes, as the measure of the
Markov rule. Read at `4c285e86`:
- **Its income process** is a single `IncShkDstn` per period, the product of ψ's nodes and ξ's, the unemployment node
  among ξ's: `UnempPrb` and `IncUnemp` give an unemployed node with probability ℘ and scale the employed nodes by
  (1 − ℘ξ_u)/(1 − ℘), which is `bst/1`'s ξ exactly. The adapter's gate assigns `IncShkDstn` from the same nodes.
- **What reads which distribution.** `GPFacMod`, `VAFac`, `GPFacHrm`, `ELogPermShk` and the target's E[1/ψ] read
  `PermShkDstn[0]`; `WorstPrb`, `WRPFac`, `MPCmax` and `bilt["hNrm"]` read `IncShkDstn[0]`; nothing reads
  `TranShkDstn`, and the target assumes that the transitory nodes have mean one. An assigned `IncShkDstn` must therefore
  be followed by `construct("PermShkDstn", "TranShkDstn")`.
- **Its newborn** cannot be `bst/1`'s, even with the `NewbornPermShk` of draft econ-ark/HARK#1860: on main, a newborn
  draws ψ and has θ = 1 unless `NewbornTransShk` is set, which draws from the whole mixture, unemployment included. The
  Markov consumer's employment states can, with `MrkvPrbsInit = [1, 0]`, `NewbornTransShk = True` and the
  `NewbornPermShk = False` of draft #1860.
- **Its targets and conditions.** `calc_stable_points` computes the target, `mNrmTrg`, and the balanced-growth point,
  `mNrmStE`, in `post_solve`, only when `cycles = 0`, `T_cycle = 1` and the type is exactly `IndShockConsumerType`;
  `check_conditions` sets the condition factors. The Markov consumer has neither.
- **Its stationary distribution** on a grid comes through `initialize_sym()` and the simulator's transition matrices;
  Harmenberg's measure is `norm = "G"`. In HARK's own lognormal constructor, `neutral_measure` tilts ψ's weights by ψ,
  and set before the solve it changes the policy.

## The evidence

- **The gate.** Over the buffer-stock benchmark's ladder (the first two levels of the toy, the library member and the
  untruncated toy, and the toy's third), the Markov rule agreed with the standard consumer's on the same nodes to
  2.3·10⁻¹⁴ relative or better, and the two employment states' rules were identical. Every number in the adapter's files
  agreed with the benchmark emitter's files to 2.2·10⁻¹² relative and 9.2·10⁻¹³ absolute, and each file passes
  `check.py --verify-results` ([the finding](../records/findings/2026-10-21_hark-markov-for-bst1.md)).
- **The emitter's files** themselves, written with the standard consumer, validate and pass the checker: the first two
  levels of the three members and the toy's third, written on 2026-10-20
  ([the emitter's ladder](../records/findings/2026-10-20_emitter-ladder.md)), and the toy's fourth, rerun on 2026-10-21.
- **A second HARK implementation** of the same model is in QuantEcon's community library of baseline models, at
  `solutions/buffer-stock/001-hark-egm/`. QuantEcon/community-library#5 added it as `projects/HARK/buffer-stock/`, and
  #15 moved it there. It uses HARK alone, at `econ-ark` 0.17.1. Its checks include an independent endogenous-grid solver
  written in NumPy and SciPy, and its calibration is `bst/1`'s `library` member.
- **A check against QuantEcon's form.** The recasting of `bst/1` for QuantEcon's code was checked against HARK's
  solution of a member: see [`quantecon-jax.md`](quantecon-jax.md).

## Sources

- **HARK itself:** the commit `03a2c7a1` of draft econ-ark/HARK#1858, on the fork `llorracc/HARK`, and `11852805` on
  that fork's branch `natural-limit-infimum`, stacked on it; its main branch at
  `4c285e86`; and the drafts econ-ark/HARK#1859, #1860 and #1861.
- **HARK's names:** NARK (econ-ark/NARK), the naming conventions that left HARK's repository in 2024. It maps HARK's
  code names to LaTeX macros.
- **A notation registry.** econ-ark/econ-ark-tools has one, `notation.yml`, which glosses some symbols with HARK's
  names.
- **Bellman's documentation:** its page *ConsIndShock — Formal MDP Document* tables HARK's variables against the stage's
  perches.
