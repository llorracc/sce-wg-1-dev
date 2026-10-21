# HARK's Rosetta Stone for `bst/1`

Draft, begun on 2026-10-21; see the [Rosetta Stones](README.md). The toolkit is HARK's `IndShockConsumerType`.
- **Where it was read.** What follows was read on HARK's main branch at commit `4c285e86`, of 2026-10-07, by the HARK
  session, unless a draft pull request is named.
- **The cards** are in [`hark.cards.yaml`](hark.cards.yaml).

## The lexicon

- **Timing.** Element t of `Rfree`, `PermGroFac` and `IncShkDstn` governs the move from t to t + 1, and is used to solve
  period t. `LivPrb[t]` is survival at the end of t. An infinite horizon is `cycles = 0` with `T_cycle = 1`.
- **Normalization.** Variables are normalized by permanent income, as in `bst/1`: `mNrm`, `aNrm` and `cNrm` are m, a and c.

| `bst/1` | HARK | timing and normalization | where HARK differs, and what the adapter does |
|---|---|---|---|
| ρ, `crra` | `CRRA` | a number | — |
| β, `types[].beta`, with the shares, `types[].share` | `DiscFac` | a number | each of `bst/1`'s types is a separate agent: the adapter solves one `IndShockConsumerType` per type and pools them with the shares |
| ℒ, `survival` | `LivPrb`, a list per period | survival at the end of t. It enters only the effective discount factor, `DiscFac`·`LivPrb`. R is not divided by ℒ, and the assets of the dead vanish | — |
| R, `return` | `Rfree`, a list per period | element t governs the move from t to t + 1 | — |
| 𝒢, `income.growth` | `PermGroFac`, a list per period | as `Rfree`. In `simulate()` the drawn `PermShk` includes it, as ψ𝒢; in the model file it does not | — |
| ψ, `income.permanent_shock` | `PermShkStd`, the σ of log ψ, and `PermShkCount` | `MeanOneLogNormal(σ)`, with log ψ ~ N(−σ²/2, σ²). It is cut into `PermShkCount` equiprobable nodes at the conditional means of their bins, so that E[ψ] = 1 at the nodes | HARK's main has no truncated law. The adapter gives HARK the member's own nodes. It assigns `IncShkDstn`, then calls `construct("PermShkDstn", "TranShkDstn")`, since the condition factors and the targets read those two |
| θ, `income.employed_shock` | `TranShkStd` and `TranShkCount` | as ψ | as ψ |
| ℘, `income.unemployment.prob` | `UnempPrb` | `MixtureTranIncShk`: an unemployed node ξ̲ with probability ℘, and the employed nodes scaled by (1 − ℘ξ̲)/(1 − ℘), each with probability (1 − ℘)/N | none: this is `bst/1`'s ξ exactly |
| ξ̲, `income.unemployment.income` | `IncUnemp` | a ratio to permanent income | none. Retirement's `UnempPrbRet` and `IncUnempRet` are off at `T_retire = 0` |
| ψ and ξ jointly | `IncShkDstn` | the independent product; its atoms are ψ and ξ | — |
| a̲_Art, `borrowing_constraint` | `BoroCnstArt`, or `None` for `natural` | a bound on end-of-period a. The constraint in force is the larger of `BoroCnstNat` and `BoroCnstArt` | `IndShockConsumerType`'s default is 0.0 |
| a̲_Nat | `BoroCnstNat`, computed by HARK | from the lowest nodes, not from the laws' infima | where the laws' own limit is tighter than the nodes', as with truncated laws and ξ̲ > 0, the adapter imposes it through `BoroCnstArt`. Draft pull request econ-ark/HARK#1861 records a discretized law's true bounds with its nodes; nothing reads them yet |
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
| the rule c(m) at the request points | `solution[0].cFunc` | a `LinearInterp`, or a cubic with `CubicBool`. Above the grid it approaches the limiting linear function, with intercept `MPCmin`·`hNrm` and slope `MPCmin`, under a lower envelope with the constraint |
| the value v(m) | `solution[0].vFunc`, with `vFuncBool` | a `ValueFuncCRRA` over a cubic in pseudo-inverse value. V = P^(1−ρ)·v(m) |
| the MPC | `cFunc.derivative(m)`, or `eval_with_derivative` | a linear interpolant's MPC is piecewise constant |
| the limiting MPCs | `solution[0].MPCmin`, as m → ∞, and `MPCmax`, at the lower limit | `bilt["MPCmin"]` and `bilt["MPCmax"]` are the perfect-foresight values, not these |
| the target, and the balanced-growth point | `solution[0].mNrmTrg`, where E[m′] = m, and `mNrmStE` | computed in `post_solve` only when `cycles = 0`, `T_cycle = 1` and the type is exactly `IndShockConsumerType`. A subclass needs `force = True` |
| human wealth | `solution[t].hNrm` | this excludes current income, so it is BST's h − 1. `bilt["hNrm"]` = 1/(1 − 𝒢/R) includes it |
| the condition factors | `check_conditions`, which sets `conditions` and `bilt`: `APFac`, `GPFacRaw`, `GPFacMod`, `GPFacLiv`, `GPFacHrm`, `RPFac`, `WRPFac`, `FHWFac`, `PFVAFac`, `VAFac` and `WorstPrb` | `VAFac` leaves ℒ out, where `APFac` and `PFVAFac` include it. The checker computes the factors itself from the reported expectations, so HARK's serve for comparison only |
| the stationary distribution, on a grid | `initialize_sym()`; then `_simulator.make_transition_matrices(grid_specs, norm=None)`, `find_steady_state()`, and `get_long_run_dstn("mNrm")` or `get_long_run_average(...)` | Harmenberg's measure is `norm = "G"`. Its docstring says the tilt by `PermShk` alone is exact only without growth or without mortality. The newborns are this simulator's, not `bst/1`'s |
| the stationary distribution, by simulation | `simulate()`, with `track_vars` and `history`; `income_shuffle`, `init_shuffle` and `death_shuffle` give exact quotas | for Harmenberg's measure: solve with `neutral_measure = False`; then set it, rebuild `IncShkDstn`, `PermShkDstn` and `TranShkDstn`, and simulate. Set before the solve, it changes the policy |
| welfare | none | the adapter computes it from `vFunc` |

## The method

- **The solution:** `solve_one_period_ConsIndShock`, the endogenous grid method. It is iterated over an infinite horizon
  until the distance between successive solutions is below `tolerance`, by default 10⁻⁶.
  - The stage's `policy` block writes the maximization for the reader. Its operative line is the Euler equation with its
    complementarity clause, and HARK's endogenous grid method solves that relation.
  - The stage's `max(a_Art, a_Nat)` is HARK's own: the larger of `BoroCnstArt` and `BoroCnstNat`.
- **The grid:** `aXtraGrid`, end-of-period assets above the natural limit, nested multi-exponentially. Its settings are
  `aXtraMin` (by default 0.001), `aXtraMax` (20), `aXtraCount` (48), `aXtraNestFac` (3) and `aXtraExtra`.
- **The interpolation:** linear, or cubic with `CubicBool`. `vFuncBool` keeps the value function.
- **The expectation:** over the nodes of `IncShkDstn`, which the adapter supplies. The method file's quadrature is
  therefore the adapter's choice of nodes, not HARK's.
- **The diagnostics' expectation:** the Euler residuals are taken with a finer quadrature of the stated laws than the
  household's, for example HARK's `expected` over a finer `IncShkDstn`.

## The adapter

The adapter in use is the HAFiscal-Latest session's emitter of results files, in the buffer-stock benchmark. It is private
for now; whether it is published is the owner's decision. In this stone's terms:
- **Encode.** The lexicon's names, with HARK's own income inputs left as placeholders. `IncShkDstn` is replaced by the
  laws' nodes, and then `construct("PermShkDstn", "TranShkDstn")` is called. After the solve, the emitter asserts that HARK
  did not rebuild them.
- **The call:** `solve()`.
- **Decode.**
  - HARK's `cFunc` and `vFunc` are read, and the constraint in force is read and asserted equal to the member's.
  - The targets and the conditions come from the laws' nodes.
  - The stationary population is computed outside HARK, by a linear lottery on an asset grid, with a node at an artificial
    constraint. Deaths come at the rate 1 − ℒ, and newborns from the member's newborn law.
  - It has two measures: the households', with ψ's law as given; and the income measure, with the probabilities tilted
    by ψ and the survivors' share ℒ𝒢.

**How it departs from HARK alone:**
- the population is the emitter's own;
- above the top of the solution grid, the rule is HARK's extrapolation, an exponential approach to the limiting linear
  function, not a power law;
- the newborns are the emitter's own.

## The evidence

- **Verified files.** The emitter's seven results files of 2026-10-20 validate and pass `check.py --verify-results`. They
  cover the first two levels of the three members and the toy's third ([the emitter's
  ladder](../records/findings/2026-10-20_emitter-ladder.md)).
- **A second HARK implementation** of the same model is in QuantEcon's community library of baseline models, at
  `solutions/buffer-stock/001-hark-egm/`. QuantEcon/community-library#5 added it as `projects/HARK/buffer-stock/`, and
  #15 moved it there. It uses HARK alone, at `econ-ark` 0.17.1. Its checks include an independent endogenous-grid solver
  written in NumPy and SciPy, and its calibration is `bst/1`'s `library` member.
- **A check against QuantEcon's form.** The recasting of `bst/1` for QuantEcon's code was checked against HARK's solution
  of a member: see [`quantecon-jax.md`](quantecon-jax.md).

## Sources

- **HARK itself:** its main branch at `4c285e86`, read by the HARK session, and the drafts econ-ark/HARK#1859, #1860 and
  #1861.
- **HARK's names:** NARK (econ-ark/NARK), the naming conventions that left HARK's repository in 2024. It maps HARK's code
  names to LaTeX macros.
- **A notation registry.** econ-ark/econ-ark-tools has one, `notation.yml` v0.6.0, which glosses some symbols with HARK's
  names. Two of its names, `mTrgNrm` and `mBalLvl`, are HARK's `mNrmTrg` and `mNrmStE`, which this stone uses.
- **Bellman's documentation:** its page *ConsIndShock — Formal MDP Document* tables HARK's variables against the stage's
  perches.
