# HARK's Rosetta Stone for `bst/1`

Draft, begun on 2026-10-21; see the [Rosetta Stones](README.md). The toolkit is HARK's `IndShockConsumerType`.
- **Where it was read.** What follows was read on HARK's main branch at commit `4c285e86`, of 2026-10-07, unless a draft
  pull request is named. The figures for HARK's defaults were computed with that code.
- **The cards** are in [`hark.cards.yaml`](hark.cards.yaml).

## The lexicon

- **Timing.** Element t of `Rfree`, `PermGroFac` and `IncShkDstn` governs the move from t to t + 1, and is used to solve
  period t. `LivPrb[t]` is survival at the end of t. An infinite horizon is `cycles = 0` with `T_cycle = 1`.
- **Normalization.** Variables are normalized by permanent income, as in `bst/1`: `mNrm`, `aNrm` and `cNrm` are m, a and c.

| `bst/1` | HARK | timing and normalization | where HARK differs, and what the adapter does |
|---|---|---|---|
| ϱ, `crra` | `CRRA` | a number | — |
| β, `types[].beta`, with the shares, `types[].share` | `DiscFac` | a number | each of `bst/1`'s types is a separate agent: the adapter solves one `IndShockConsumerType` per type and pools them with the shares |
| ℒ, `survival` | `LivPrb`, a list per period | survival at the end of t. It enters only the effective discount factor, `DiscFac`·`LivPrb`. R is not divided by ℒ, and the assets of the dead vanish | — |
| R, `return` | `Rfree`, a list per period | element t governs the move from t to t + 1 | — |
| 𝒢, `income.growth` | `PermGroFac`, a list per period | as `Rfree`. In `simulate()` the drawn `PermShk` includes it, as ψ𝒢; in the model file it does not | — |
| ψ, `income.permanent_shock` | `PermShkStd`, the σ of log ψ, and `PermShkCount` | `MeanOneLogNormal(σ)`, with log ψ ~ N(−σ²/2, σ²). It is cut into `PermShkCount` equiprobable nodes at the conditional means of their bins, so that E[ψ] = 1 at the nodes | HARK's main has no truncated law. The adapter gives HARK the member's own nodes. It assigns `IncShkDstn`, then calls `construct("PermShkDstn", "TranShkDstn")`, so that nothing is left stale. `GPFacMod`, `VAFac`, `GPFacHrm`, `ELogPermShk` and the target's E[1/ψ] read `PermShkDstn[0]`; `WorstPrb`, `WRPFac`, `MPCmax` and `bilt["hNrm"]` read `IncShkDstn[0]`; nothing reads `TranShkDstn`, and the target assumes that the transitory nodes have mean one |
| θ, `income.employed_shock` | `TranShkStd` and `TranShkCount` | as ψ | as ψ |
| ℘, `income.unemployment.prob` | `UnempPrb` | `MixtureTranIncShk`: an unemployed node ξ_u with probability ℘, and the employed nodes scaled by (1 − ℘ξ_u)/(1 − ℘), each with probability (1 − ℘)/N | none: this is `bst/1`'s ξ exactly |
| ξ_u, `income.unemployment.income` | `IncUnemp` | a ratio to permanent income | none. Retirement's `UnempPrbRet` and `IncUnempRet` are off at `T_retire = 0` |
| ψ and ξ jointly | `IncShkDstn` | the independent product; its atoms are ψ and ξ | — |
| `a_Art`, `borrowing_constraint` | `BoroCnstArt`, or `None` for `natural` | a bound on end-of-period a. The constraint in force is the larger of the natural limit and `BoroCnstArt` | `IndShockConsumerType`'s default is 0.0 |
| `a_Nat` | none stored: HARK computes a natural limit only as a local variable, inside the solver and `calc_limiting_values` | from the lowest nodes, not from the laws' infima. Where the artificial constraint binds, the solver's local value is a one-period limit from it, not the natural limit | the adapter computes the effective member's natural limit itself, from the nodes' lowest values: −`ξ_min` `ψ_min`/(ℛ − `ψ_min`) with ℛ = R/𝒢, as `model.md` writes it. Here `ξ_min` is the lowest node of ξ, the worst income, which is the lower of ξ_u and the lowest employed node, and `ψ_min` is the lowest node of ψ. On the toy's seven equiprobable nodes the lowest employed node is 0.558, below ξ_u = 0.7. The results file reports it (`effective_member.derived.natural_limit`), with the constraint in force the larger of `a_Art` and it. `solution[0].mNrmMin` equals it only where no artificial constraint binds. The laws' own limit is tighter whenever ξ_u > 0, since the laws reach below their lowest nodes in both ψ and θ: it is 0 when either law is untruncated, and set by the truncation bounds when both are truncated. An adapter could impose that limit through `BoroCnstArt`, but it would then solve a different effective member, and none does. Draft pull request econ-ark/HARK#1861 records a discretized law's true bounds with its nodes; nothing reads them yet |
| the newborn: employed, P = 1, no assets, θ an employed draw | `kLogInitMean`, `kLogInitStd` and `kNrmInitCount`; `pLogInitMean`, `pLogInitStd` and `pLvlInitCount`; `NewbornTransShk` | on main, `simulate()`'s newborn draws ψ and grows, P₀ = P_init·𝒢ψ. It has θ = 1 unless `NewbornTransShk` is set, which draws from the whole mixture, unemployment included. The transition-matrix simulator's newborns draw (ψ, θ) and grow | see the note on the newborn below |

**The newborn.**
- `IndShockConsumerType` cannot state `bst/1`'s newborn, even with the `NewbornPermShk` of draft econ-ark/HARK#1860.
- The employment states of drafts #1859 and #1860 can: `MarkovConsumerType`, with `MrkvPrbsInit = [1, 0]`,
  `NewbornTransShk = True` and `NewbornPermShk = False`.
- Otherwise the adapter builds the newborns' distribution itself.
- k = 0 needs a very negative `kLogInitMean`. The default, −12, gives k ≈ 6·10⁻⁶.

## Where the results file's quantities come from

| results file | HARK | note |
|---|---|---|
| the rule c(m) at the request points | `solution[0].cFunc` | a `LowerEnvelope` of the unconstrained rule, a `LinearInterp` or with `CubicBool` a cubic, and the constraint. Above the grid it approaches the limiting linear function `MPCmin`·(m + `hNrm`), with the iterates' values of both, so the method's tolerance matters there; see the method |
| the value v(m) | `solution[0].vFunc`, with `vFuncBool` | a `ValueFuncCRRA` over a cubic in pseudo-inverse value. V = P^(1−ϱ)·v(m) |
| the MPC | `cFunc.derivative(m)`, or `eval_with_derivative` | a linear interpolant's MPC is piecewise constant, and at an interior knot it is the left segment's slope. The envelope's derivative is the lower piece's, the unconstrained one's at a tie. A cubic's slope is continuous at the knots |
| the limiting MPCs | `bilt["MPCmin"]`, as m → ∞, and `bilt["MPCmax"]`, at the lower limit: the closed forms, max(1 − `RPFac`, 0) and 1 − `WorstPrb`^(1/ϱ)·`RPFac`, or 1 where the artificial constraint binds | `solution[0].MPCmin` and `MPCmax` are the solver's iterates, which approach them and lag at HARK's default tolerance |
| the target, and the balanced-growth point | `solution[0].mNrmTrg`, where E[m′] = m, and `mNrmStE` | computed by `calc_stable_points` in `post_solve`, only when `cycles = 0`, `T_cycle = 1` and the type is exactly `IndShockConsumerType`. They are NaN unless the GICRaw holds, or if Newton's method fails. `post_solve` calls it without `force`, so a subclass must call `calc_stable_points(force=True)` itself after `solve()` |
| human wealth | `solution[t].hNrm` | this excludes current income, so it is BST's h − 1 once it has converged. `bilt["hNrm"]` = E[ψξ]/(1 − 𝒢/R) over `IncShkDstn`'s nodes, which is 1/(1 − 𝒢/R) when they have mean one, includes it, and `bilt["hNrm"]` − 1 is the limit |
| the condition factors | `check_conditions`, which sets `conditions` and `bilt`: `APFac`, `GPFacRaw`, `GPFacMod`, `GPFacLiv`, `GPFacHrm`, `RPFac`, `WRPFac`, `FHWFac`, `PFVAFac`, `VAFac` and `WorstPrb` | `VAFac` leaves ℒ out, where `APFac` and `PFVAFac` include it. The checker computes the factors itself from the reported expectations, so HARK's serve for comparison only |
| the stationary distribution, on a grid | `initialize_sym()`; then `_simulator.make_transition_matrices(grid_specs, norm=None)`, `find_steady_state()`, and `get_long_run_dstn("mNrm")` or `get_long_run_average(...)` | Harmenberg's measure is `norm = "G"`. Its docstring says the tilt by `PermShk` alone is exact only without growth or without mortality. The newborns are this simulator's, not `bst/1`'s |
| the stationary distribution, by simulation | `simulate()`, with `track_vars` and `history`; `income_shuffle`, `init_shuffle` and `death_shuffle` give exact quotas | for Harmenberg's measure: `neutral_measure` is an argument of HARK's own lognormal constructor, which multiplies ψ's weights by ψ, and set before the solve it changes the policy. With the member's nodes, the adapter solves first, then tilts its own ψ weights by ψ, assigns `IncShkDstn`, constructs `PermShkDstn` and `TranShkDstn`, and simulates. Each death is then replaced by one unweighted newborn, so newborns carry a share 1 − ℒ of the income mass where Harmenberg's measure gives them 1 − ℒ𝒢: the tilt alone is exact only when 𝒢 = 1 or ℒ = 1, and weighting each household by 𝒢 to the power of its age corrects it (derived from the code, not measured) |
| welfare | none | the adapter computes it from `vFunc` |

## The method

- **The solution:** `solve_one_period_ConsIndShock`, the endogenous grid method. It is iterated over an infinite horizon
  until the distance between successive solutions is below `tolerance`, by default 10⁻⁶.
  - The distance is measured on the rule's knots alone (`ConsumerSolution.distance_criteria = ["vPfunc"]`), not on
    `hNrm`, `MPCmin` or the limiting function. `hNrm` approaches its limit at the rate 𝒢/R an iteration, so it lags.
  - On HARK's defaults, at the default tolerance, `hNrm` is 44.99 against its limit of 50.50, and c above the grid is
    off by 0.0115 at m = 60 and 0.035 at m = 100, against less than 4·10⁻⁵ within the grid. `bst/1`'s population grids
    reach 60, 120 and 240, so the tolerance must be tighter there: 10⁻⁸ keeps the gap at m = 60 below 10⁻⁴ on those
    defaults.
  - The stage's `policy` block writes the maximization for the reader. Its operative line is the Euler equation with its
    complementarity clause, and HARK's endogenous grid method solves that relation.
  - The stage's `max(a_Art, a_Nat)` is HARK's own: the larger of `BoroCnstArt` and the natural limit it computes from the
    nodes.
- **The grid:** `aXtraGrid`, end-of-period assets above the natural limit, nested multi-exponentially. Its settings are
  `aXtraMin` (by default 0.001), `aXtraMax` (20), `aXtraCount` (48), `aXtraNestFac` (3) and `aXtraExtra`.
- **The interpolation:** linear, or cubic with `CubicBool`. `vFuncBool` keeps the value function.
- **The expectation:** over the nodes of `IncShkDstn`, which the adapter supplies. The method file's quadrature is
  therefore the adapter's choice of nodes, not HARK's.
- **The diagnostics' expectation.** The Euler residuals are taken against the stated laws by a quadrature unlike the
  household's. The emitter's own is Gauss–Legendre in logs, split at the rule's kink. HARK's `expected` would also serve,
  over a finer discretization of the stated laws built apart from the agent's `IncShkDstn`, with the adapter making the
  nodes of a truncated law. A finer law's lowest ψ node is lower than the household's, so with `a_min` < 0 the next m could
  leave the rule's domain.

## The adapter

The adapter in use is the buffer-stock benchmark's emitter of results files, which is not yet public; whether it is
published is the owner's decision. In this stone's terms:
- **Encode.** The lexicon's names, with HARK's own income inputs left as placeholders. `IncShkDstn` is replaced by the
  laws' nodes, and then `construct("PermShkDstn", "TranShkDstn")` is called. The settings it passes are its own, not
  HARK's defaults:
  - `aXtraMin` = 10⁻⁶;
  - `aXtraMax`, `aXtraCount` and `aXtraNestFac` from the level's top, points and nesting, with no `aXtraExtra`;
  - `CubicBool` and `vFuncBool` set;
  - the level's `tolerance`: 10⁻⁸ at the first level, 10⁻¹⁰ at the second, and 10⁻¹² at the third and fourth.
  
  So the grid and the tolerance honor the method file's settings, while the endogenous grid method, the cubic
  interpolation and its approach above the grid are fixed inside.
- **The call:** `solve()`.
- **Decode.**
  - After the solve it asserts three things: that `IncShkDstn` is unchanged; that both marginals are the laws' unique
    nodes, with probabilities summed as HARK sums them; and that HARK's `mNrmMin` equals the effective member's
    constraint in force, to 10⁻⁹.
  - HARK's `cFunc` and `vFunc` are read. The natural limit reported is the emitter's own, computed from the nodes' lowest
    values by the closed form above, which is also HARK's.
  - The targets and the conditions come from the laws' nodes, and the Euler residuals from the emitter's own quadrature
    of the stated laws.
  - The stationary population is computed outside HARK, by a linear lottery on an asset grid, with a node at an artificial
    constraint. Deaths come at the rate 1 − ℒ, and newborns from the member's newborn law.
  - It has two measures: the households', with ψ's law as given; and the income measure, with the probabilities tilted
    by ψ and the survivors' share ℒ𝒢.

**How it departs from HARK alone:**
- the population is the emitter's own;
- above the top of the solution grid, the rule is HARK's extrapolation, an exponential approach to the limiting linear
  function, not a power law. But the population and every reported point lie below the solution grid's top, so the
  extrapolation enters no reported quantity;
- the newborns are the emitter's own.

## The evidence

- **Verified files.** The emitter's eight results files validate and pass `check.py --verify-results`: the first two levels
  of the three members and the toy's third, written on 2026-10-20 ([the emitter's
  ladder](../records/findings/2026-10-20_emitter-ladder.md)), and the toy's fourth, with the population block, rerun on
  2026-10-21.
- **A second HARK implementation** of the same model is in QuantEcon's community library of baseline models, at
  `solutions/buffer-stock/001-hark-egm/`. QuantEcon/community-library#5 added it as `projects/HARK/buffer-stock/`, and
  #15 moved it there. It uses HARK alone, at `econ-ark` 0.17.1. Its checks include an independent endogenous-grid solver
  written in NumPy and SciPy, and its calibration is `bst/1`'s `library` member.
- **A check against QuantEcon's form.** The recasting of `bst/1` for QuantEcon's code was checked against HARK's solution
  of a member: see [`quantecon-jax.md`](quantecon-jax.md).

## Sources

- **HARK itself:** its main branch at `4c285e86`, and the drafts econ-ark/HARK#1859, #1860 and #1861.
- **HARK's names:** NARK (econ-ark/NARK), the naming conventions that left HARK's repository in 2024. It maps HARK's code
  names to LaTeX macros.
- **A notation registry.** econ-ark/econ-ark-tools has one, `notation.yml` v0.6.0, which glosses some symbols with HARK's
  names. Two of its names, `mTrgNrm` and `mBalLvl`, are HARK's `mNrmTrg` and `mNrmStE`, which this stone uses.
- **Bellman's documentation:** its page *ConsIndShock — Formal MDP Document* tables HARK's variables against the stage's
  perches.
