# Clean-room log: HARK's part of the adapter, written from the stone and the hub

Written on 2026-11-06 in the sandbox. Sources used: `rosetta/` (README, `hark.md`, `hark.cards.yaml`),
`harness/adapters/hark/ladder.yaml`, `harness/README.md`, `harness/adapters/common.py`, `schemas/`, and HARK 0.17.2 as
installed in the pinned environment (`site-packages/HARK`, commit `11852805`). Nothing under the repositories, no git
history, no web. "The stone" is `hark.md`; "the cards" are `hark.cards.yaml`; "the hub" is `schemas/` with `common.py`
and `harness/README.md`. Line numbers of HARK are those of the installed files.

## The runs

Both ran and verified at the first attempt. Two later edits, the placeholders' form and one more key in the solver
report, changed no number; the two members' files in `out/` are the final adapter's, 200 lines, and a second run of
each gives the same `results.json` byte for byte (SHA-256 `c78fec9c…` and `65621a36…`).

| member, at `low`, with its request file | the adapter | `check.py --verify-results` |
|---|---|---|
| `bst-restrained` | exit 0; "results.json validates against bst/results.schema.json" | "out/bst-restrained/results.json: validates, and its report is consistent with the member 6e8651cdf2cd…" |
| `bst-p-zero-0.005` | exit 0; "results.json validates against bst/results.schema.json" | "out/bst-p-zero-0.005/results.json: validates, and its report is consistent with the member b2e365cd24b4…" |

The adapter's own lines:
- `bst-restrained`: kink 0.9768573961411718 (Euler 0.976857400280578), target 1.0364768532462578, mean a 0.07250,
  W −16.924610093740075, max|r| 1.82e-03 (precision 6.4e-07, own nodes 9.9e-06), stationarity 1.2e-14, arrivals
  135,240; HARK's `completed_cycles` 722, distance 9.93·10⁻⁹.
- `bst-p-zero-0.005`: no kink, target 1.3919851178411946, mean a 0.41209, W −16.858163178942885, max|r| 1.05e-03
  (precision 4.7e-11, own nodes 4.9e-07), stationarity 1.5e-12, arrivals 224,000; `completed_cycles` 723, distance
  9.97·10⁻⁹.

Beyond the task, under `out/others/` and `out/levels/`, all verified by the checker: the other two natural rungs at
`low` with their request files; `toy` (seven types, ξ_u = 0.7, ℒ < 1) and `library` at `low` with no request file, so
through the shared code's request rule; and `bst-restrained` at `medium` and `high`. The `high` file was written
before the adapter's last two edits (the placeholders' form, and one more key in the solver report); on two other
runs those edits changed the solver report and nothing else in `results.json` (`out/before-last-edit/`).
`out/repeat/` holds the second runs.

Against the figures the hub quotes for HARK's committed runs, which are all the sandbox holds of them:

| the hub's figure | where | this adapter |
|---|---|---|
| the rungs' largest gap to the restrained rule, 0.138, 0.061 and 0.027 at level 1 over m in (0, 10], largest at m ≈ 0.98 | `model.md` | 0.137, 0.061 and 0.026 at `low`, at the request points, at m = 0.98, 0.975 and 0.975 |
| at the finest level a kink near 0.974, a target near 1.041, a mass at the constraint near 0.213, a mean MPC near 0.456 | `for-toolkit-authors.md` | at `high`: 0.97440, 1.04140, 0.21274, 0.45559 |
| the largest Euler residual under the stated laws at the finest level about 2.1·10⁻⁴ | `for-toolkit-authors.md`, `comparing-solutions.md` | at `high`: 2.06·10⁻⁴ |
| the rule's movement from medium to high about 3.5·10⁻³ at the request points up to m = 20 | `for-toolkit-authors.md` | 3.48·10⁻³ |
| the MPC at the natural constraint carried to one part in 10¹⁴ | `comparing-solutions.md` | 1.2·10⁻¹⁶ relative, at `low` |

## A. Lookups

### Needed, and absent or incomplete in the documents; found in HARK's source

- **How to build a state's distribution.**
  - Needed: the constructor's arguments and the layout of the atoms.
  - Found: `HARK/distributions/discrete.py:616-706`, `DiscreteDistributionLabeled.__init__(pmv, atoms, seed=None,
    limit=None, name=..., attrs=None, var_names=None, var_attrs=None)`; `:186-209`, the base class: `atoms` is
    two-dimensional, one row per variable, the last axis the atom, and `pmv.size` must equal `atoms.shape[-1]`. The
    import, `from HARK.distributions import DiscreteDistributionLabeled`: `HARK/distributions/__init__.py`.
  - The stone: only the cards name the class, "one DiscreteDistributionLabeled over PermShk and TranShk per state";
    the prose has "`PermShk` in each state's distribution in `IncShkDstn`". The arguments and the layout: absent.
- **The order and the labels the solver requires.**
  - Needed: which row is which shock, and whether the names matter.
  - Found: `ConsMarkovModel.py:374-375` and `:422-424` read `atoms[0]` as the permanent and `atoms[1]` as the
    transitory shock, by position; `:455-467` read `S["PermShk"]` and `S["TranShk"]`, by label. Both the order and
    the two names are binding.
  - The stone: "over PermShk and TranShk" (cards). The positional requirement: absent.
- **The form of `limit`.**
  - Needed: how the laws' infima and suprema are recorded so that HARK reads them.
  - Found: `ConsMarkovModel.py:382-388`, `PermShkInfNext, TranShkInfNext = IncShkDstn_list[j].limit["infimum"]`;
    `discrete.py:197-202`: a dict, filled when omitted with the atoms' own minima and maxima under `"infimum"` and
    `"supremum"`, one entry per variable; `IncomeProcesses.py:196-203`: HARK's own distributions carry more keys
    (`dist`, `method`, `N`, `endpoints`), of which the Markov solver reads none.
  - The stone: "which the adapter records as each distribution's `limit`"; the cards: "each with the laws' infima
    and suprema as its limit, which HARK reads for the natural limit". The keys and the per-variable order: absent.
- **The Python type of "one value per state".**
  - Needed: what `Rfree[t]`, `LivPrb[t]`, `PermGroFac[t]`, `MrkvArray[t]` and `IncShkDstn[t]` must be.
  - Found: `ConsMarkovModel.py:855-915`, `check_markov_inputs`, run by `pre_solve`: the first three must be
    `np.ndarray` of shape `(StateCount,)`, `MrkvArray[t]` an `np.ndarray` `(N, N)`, `IncShkDstn[t]` a Python `list`
    of length N. By trial, a list `[[R, R]]` or a scalar `[R]` is refused at `solve()`: "Rfree[t] not the right
    shape, it should be an array of Rfree of all the states."
  - The stone: "are arrays with one value per state, here two" (the States bullet) and "a list per period of one
    value per state" (the rows). That a numpy array is required and a list refused, and that `IncShkDstn`'s inner
    container must be a list: absent.
- **The Markov consumer's defaults that the encode must override or may rely on.**
  - Needed: what "left at zero", "placeholders" and "passes no `aXtraExtra`" mean as arguments.
  - Found: `ConsMarkovModel.py:751-824`: `UnempPrb = np.array([0.05, 0.05])` and `IncUnemp = np.array([0.3, 0.3])`,
    so "left at zero" means passing zeros, and the type's own form is one value per state; `PermShkStd =
    np.array([[0.1, 0.1]])`, `PermShkCount = 7`; `BoroCnstArt = 0.0`, so a natural member must pass `None`
    explicitly; `cycles = 1`; `CubicBool = vFuncBool = False`; `aXtraExtra = None`, so passing none is the default;
    `MrkvPrbsInit = [1, 0]`; `NewbornTransShk = False`; `BoroCnstInfimum = True`.
  - The stone: "`UnempPrb`, the standard consumer's way, is left at zero"; "`IncUnemp` is left at zero";
    "`PermShkStd` and `PermShkCount` are placeholders". It gives the standard consumer's default constraint
    ("`IndShockConsumerType`'s default is `0.0`"), not the Markov consumer's. The values and their forms: absent.
- **How the infinite-horizon solve ends.**
  - Needed: what to report as "how the solve ended" (`provenance.solver`), and whether a solve can end unconverged.
  - Found: `core.py:2366-2392`, `solve_agent`: it stops when `solution_distance <= tolerance` or, without a word,
    after `max_cycles = 5000`; it sets `agent.solution_distance` and `agent.completed_cycles` (the count before the
    last cycle, so one less than the cycles solved).
  - The stone: "iterated over an infinite horizon until the distance between successive solutions is below
    `tolerance`". The cap and the two attributes: absent.
- **The types HARK requires of two grid settings.**
  - Found: `utilities.py:164-172`, `type(aXtraNestFac) is int`; by trial, `aXtraNestFac=3.0` raises "Please ensure
    aXtraNestFac is either -1 or a positive integer." and `aXtraCount=300.0` raises a TypeError. The shared loader
    returns Python ints for the ladder's `3` and `300` (trial), so nothing breaks; the adapter casts all the same.
  - The ladder file: "aXtraCount points from aXtraMin to aXtraMax, equally spaced after log(1 + x) is taken
    aXtraNestFac times". The type requirement: absent.
- **A distribution's seed.**
  - Found: `distributions/base.py:68-110`: `Distribution.__init__(seed=None)`, and a missing seed is drawn from the
    system's entropy. `rosetta/README.md` asks that "any randomness has an explicit seed".
  - The stone: absent.
- **The version and the commit.**
  - Needed: what `version()` and `commit()` return.
  - Found: `HARK.__version__` is "0.17.2"; the environment's `site-packages/econ_ark-0.17.2.dist-info/direct_url.json`
    holds `vcs_info.commit_id = 1185280590b21fe2ddac80cadcfea66476e45380`. The distribution's name is `econ-ark`,
    not `HARK`.
  - The stone: "The adapter's pin is `11852805`"; the cards: `read_at: {..., commit: 11852805, ...}`. How the
    adapter obtains either: absent.
- **That nothing else needs switching off.**
  - Found: `core.py:822-828`: a constructor set to `None` restores the value passed in, which is what keeps the
    adapter's objects through every `construct()`; `IncomeProcesses.py:1159-1178` with `discrete.py:576-613`:
    `PermShkDstn` and `TranShkDstn` stay on and are derived from the supplied `IncShkDstn` by `make_univariate`,
    which works on the adapter's distributions; `ConsMarkovModel.py:917-932`: `pre_solve` rebuilds only
    `solution_terminal`.
  - The cards give the expression, `dict(init_indshk_markov['constructors'], MrkvArray=None, IncShkDstn=None)`. For
    the standard consumer the stone says "An assigned `IncShkDstn` must therefore be followed by
    `construct("PermShkDstn", "TranShkDstn")`"; for the Markov consumer: absent.
- **Where the top of the solution grid in m can be read** (for the solver report only).
  - Found: `ConsMarkovModel.py:631-642` with `interpolation.py:2028-2037`: `cFunc[i]` is
    `LowerEnvelope(cFuncNowUnc, cFuncNowCnst)`, so `cFunc[0].functions[0].x_list[-1]` is the relaxed rule's last knot.
  - The stone: "so the adapter reports the rule inside the grid only". Where that top is: absent.

### Found by trial and error

- **The constructors left on.** With HARK's `MrkvArray` constructor left on, the adapter's matrix was replaced by
  `[[0.9, 0.1], [0.6, 0.4]]`, as the stone says. With HARK's `IncShkDstn` constructor left on and scalar zeros as
  placeholders, construction raised "The last dimension of PermShkStd, TranShkStd, IncUnemp, and UnempPrb must all
  be K, the number of discrete states"; the placeholders are now one zero per state.
- **The two states.** Their rules, MPCs and values are identical bit for bit on both members and on the toy; both
  states' `mNrmMin` are exactly 0.0 on both members. The 10⁻¹² and the 10⁻⁹ are never approached.
- **`limit` left out.** On these two members it changes nothing: `mNrmMin` is `[0, 0]` and the rule is the same to
  the last bit. The recorded infima matter only for a member whose natural limit is in force and not zero.
- **Below `mNrmMin`** (not needed). Under natural HARK's rule returns NaN with a RuntimeWarning; under an artificial
  constraint it returns the relaxed rule's value, 0.471 at m = −0.01 on `bst-restrained`, since the constraint line
  has no lower extrapolation and the Markov solver's envelope skips NaN (`ConsMarkovModel.py:642`; the standard
  solver's, `ConsIndShockModel.py:788`, is built with `nan_bool=False`). `common.py` never evaluates there.
- **The strict YAML.** `yaml.safe_dump` quotes the key `on` and the tags that begin with `!`, and the shared hash
  function took both files. Booleans were not tried: `numerics.md` excludes them, so the two switches are written
  as 1.
- **A check of the encoding inside HARK** (not asked for). Solved with `IndShockConsumerType` on the same joint
  nodes, the rule and the value agree with the adapter's Markov solution to 8.4·10⁻¹⁶ and 2.0·10⁻¹⁵ relative or
  better (`bst-restrained`, `bst-p-zero-0.005`, the toy's first type), against the stone's "2.3·10⁻¹⁴ relative or
  better". A standard consumer built with `quiet=True` fails in `post_solve` ("The check_conditions method must be
  run before the calc_stable_points method"); `verbose=0` works.
- **The MPC at the natural constraint.** On `bst-p-zero-0.005` the rule's slope at `mNrmMin` is 0.9320633779513243
  against the closed form 1 − ℘^(1/ϱ) Þ̊/R = 0.9320633779513242.

### Read in HARK's source, where the documents already gave the fact

- `ConsMarkovModel.py:276-717`, the solver: the lower limit of each state is the largest of the atoms' one-period
  limit, `BoroCnstArt` and the infima's one-period limit (`:368-412`), as the stone's `a_Nat` row says; survival
  multiplies the end-of-period values by the current state's `LivPrb` (`:547-555`); the cubic's slopes are the
  solution's MPCs (`:611-637`); the rule is the lower envelope of the relaxed rule and the constraint line
  (`:627-642`); the value is a cubic in pseudo-inverse value (`:652-693`); `mNrmMin`, `hNrm`, `MPCmin` and `MPCmax`
  are arrays by state (`:712-716`).
- `core.py:1145-1205`: `tolerance` is an argument of `AgentType.__init__`, default 10⁻⁶, taken with the other
  keyword arguments, as the cards' `solution_tolerance: tolerance` implies; `cycles = 0` is the infinite horizon.
- `utilities.py:135-246`: `make_assets_grid` builds `aXtraGrid` from the four settings, as "HARK builds its grid
  from them itself" says.
- `ConsIndShockModel.py:1349-1364` and `:1943-1963`: `post_solve` calls `calc_stable_points`, which returns at once
  for a child class, as "HARK computes no targets for the Markov consumer" says; `:2470-2513`: `solve()` registers
  `BoroCnstInfimum` as a solver option, on by default.
- `interpolation.py:169-262`, `:1087-1253`, `:2040-2100`: `cFunc(m)`, `cFunc.derivative(m)` and `vFunc(m)` take
  scalars or arrays, which the protocol's "callable on m, with .derivative" needs.
- `metric.py` with `ConsIndShockModel.py:126-186`: the distance is over `vPfunc`, so over the cubic's knots, values
  and slopes, and not over the limiting line, which is why "Human wealth and the limiting MPC lag".
- By run, the stone's figures reproduce at the pin: at HARK's defaults `hNrm` 44.99 against 50.50, c off by 0.0115
  at m = 60 and 0.035 at m = 100, and 3.6·10⁻⁵ within the grid; the toy's lowest employed node 0.558.

### Needed, and given only by the hub's code, not by its prose or by the stone

- **What `nodes` is.** `(p_psi, psi, p_th, th)`, the employed draw unscaled: `common.py`, `shocks()` and `run()`.
  The protocol's header says only "solve(member, beta, nodes, own)".
- **`common.state_shocks`.** It gives each state's probabilities, ψ and ξ in the product's order. It is defined in
  `common.py` and called nowhere in it; neither the header nor the stone says the toolkit's part should call it.
- **The member object.** Its attributes (`rho`, `R`, `G`, `L`, `wp`, `xi_u`, `a_art`, `natural`, `psi` and `theta`
  with `infimum` and `supremum`) are `bst1.py`'s. `a_art` of a natural member holds the stated laws' natural limit
  and is never `None`, so "none for a member of `bst-natural/1`" has to be coded on `member.natural`.
- **The schema's demands on the protocol's strings.** `toolkit.version` must be a nonempty string;
  `provenance.solver` is a free object, "How the solve ended, as the toolkit reports it": `results.schema.json`.

## B. Open decisions

- **The placeholders.** `UnempPrb` and `IncUnemp` are passed as `np.zeros(2)`, one zero per state; `PermShkStd`,
  `PermShkCount`, `TranShkStd` and `TranShkCount` are left at HARK's defaults. The stone gives no values or forms.
- **The numbers in `limit`.** `PermShk`: the ψ law's infimum and supremum, in both states. `TranShk`, employed:
  (1 − ℘ξ_u)/(1 − ℘) times the θ law's infimum and supremum; unemployed: ξ_u for both. The stone says "the laws'
  infima and suprema" and not which numbers the transitory variable takes in each state.
- **The order of the atoms.** `common.state_shocks`' order, ψ major and θ minor, with probabilities
  `np.outer(p_psi, p_th).ravel()`. It decides the order of the sums in HARK's expectations, so the last bits.
- **Seeds.** 0 for both distributions; the agent's own seed left at HARK's default, 0. Nothing draws.
- **The order of calls.** Every argument is given to `MarkovConsumerType(...)` at once, the tolerance among them;
  nothing is assigned afterwards; then `solve()`; then the checks.
- **"HARK solved with the adapter's chain and income process".** After the solve, `agent.MrkvArray[0]` and each
  state's `pmv`, `atoms` and the two entries of `limit` are compared, for exact equality, with ones rebuilt from the
  member and the nodes. The stone does not say how the assertion is made.
- **Where the two states are compared.** At 400 points, `mNrmMin` plus a geometric sequence from `aXtraMin` to
  `aXtraMax`, so inside the grid. The measure is |x − y| ≤ 10⁻¹²·max(|x|, |y|). The MPCs are compared as well, which
  the stone does not list.
- **The constraint in force, for the 10⁻⁹ check.** max(`member.a_art`, −`ξ_min` `ψ_min`/(R/𝒢 − `ψ_min`)) on the
  nodes' lowest values, `ξ_min` the lower of ξ_u (when ℘ > 0) and the lowest scaled employed node; `member.a_art`
  alone when 𝒢`ψ_min` ≥ R. For a natural member `member.a_art` is the checker's stated limit. Absolute, on both
  states.
- **A solve that hits HARK's 5000-cycle cap** fails: the adapter asserts `solution_distance <= tolerance`.
- **What `solve` returns.** HARK's own objects, unwrapped: `cFunc[0]`, `vFunc[0]` and `float(mNrmMin[0])`. Nothing
  in the toolkit's part restricts evaluation to the grid; that every reported point lies inside it follows from the
  shared code's tops and the ladder's `aXtraMax` being the same numbers (under Errors, "Inside the grid only").
- **The level's settings.** `level_settings` returns the ladder's element as `common.ladder` reads it; `aXtraCount`
  and `aXtraNestFac` are cast to int and the rest to float before HARK sees them.
- **The newborn's switches.** `MrkvPrbsInit = [1, 0]` and `NewbornTransShk = True` are set as the stone says, though
  nothing reads them, since HARK's simulation is not used. `kLogInitMean` and the rest stay at HARK's defaults.
- **The five strings.** `name` is "HARK"; `driver` is "harness/adapters/hark/adapter.py, with
  harness/adapters/common.py"; `description`, `representation` and `diagnostics_method` are in words of my own, the
  last from the cards' entry on `diagnostics.expectation` with the shared code's 32 nodes. No document gives any.
- **`version()` and `commit()`.** `HARK.__version__`, and the full 40-character id from the installed
  distribution's `direct_url.json`, `None` when the environment records none.
- **The method file.** Seven entries, one per target of `model.md`. `method` is the cards' `method_tag` where the tag
  names what runs (`!time-iteration`, `!quadrature`, `!histogram`), the cards' words otherwise; `handler` is the
  cards' where they name one. For `policy` the method is "a cubic Hermite whose slopes are the solution's own MPCs",
  with no tag and no handler: the adapter sets `CubicBool`, so `!Linear` would misstate it (under Errors, "The method
  on `policy`").
- **The settings file.** A flat map: `level`, the number; HARK's five settings under HARK's names, as the ladder
  states them; `CubicBool: 1` and `vFuncBool: 1`; and the shared code's settings under names of my own,
  `nodes_per_shock`, `transition_nodes_per_shock`, `histogram_points`, `histogram_top`, `target_search_top` and
  `diagnostics_nodes`. The cards' shared names (`grid_min`, `grid_points` and the rest) were the other candidate
  (under Errors, "The cards against the ladder").
- **`solver`.** `{"handler": ..., "types": [{beta, completed_cycles, solution_distance, tolerance, gridpoints,
  top_gridpoint_m}]}`, one entry per type, replaced when a type is solved again.
- **Not written.** No `prepare`; no `gridpoints.py`; no gate. The task asks for `adapter.py`.
- **The import of the shared module.** The adapters' folder is put on `sys.path` and `common` imported by name.

## C. Errors: wrong, stale or contradictory

- **The tolerance on `mNrmMin` under natural.** The stone (Decode, and the cards' `decode.mNrmMin`): both states'
  `mNrmMin` equal the constraint in force "to 10⁻⁹". `common.py`, `run()`: under natural it accepts
  `-1e-9 < mNrmMin - a_lo < 1e-6`, with the comment "HARK: 4e-9 on the toy at level 1". A natural member whose limit
  HARK reaches by iterating would fail the adapter's check before reaching the shared code's wider one. No such
  member exists in today's families, where a natural member has ξ_u = 0 and the limit is exactly 0.
- **The method on `policy`.** Three statements that cannot all hold for a method file. The cards: `method_tag:
  "!Linear"` beside "with CubicBool, as the adapter sets it, a cubic Hermite ... which no tag names", and no handler.
  `model.md`: "has no tag and is named as the handler". `test_rosetta.py`: a part the whole-stage handler honors
  names no handler. `for-toolkit-authors.md` lists `!Linear` among the method file's tags.
- **The cards against the ladder.** The cards' `toolkit_settings_to_kwargs` and `methods[].settings` use shared names
  (`grid_min`, `grid_max`, `grid_points`, `grid_nesting`, `solution_tolerance`, `histogram_points`); the ladder file
  and the stone's table state the same settings "in HARK's own names". The cards never mention the ladder file or
  the levels' names, and no document says which names `settings.yaml` carries. `numerics.md` says a settings file
  gives a value "to every setting that the method file's methods declare, and to nothing else", and the method
  registry that would declare them is not written.
- **The cards are behind the stone.** Their header says "revised on 2026-10-22", yet they carry the pin of
  2026-11-01 (`11852805`, #1862); the stone says "revised on 2026-10-22 and 2026-11-01". `examples.members` and
  `evidence.verify_results` name the untruncated toy with no note that its family was abolished on 2026-11-03,
  which the stone's evidence has.
- **The limiting MPCs.** The stone: "The adapter reads neither: the checker computes the limits from the effective
  member's expectations." `bst1.py:356-357` computes `limiting_mpc` and `mpc_at_lower_limit` for the stated member,
  from its closed forms, in the member's report; `verify_results` computes neither, and a results file carries
  neither.
- **The cited lines are main's, not the pin's.** The stone says where each was read (`4c285e86`), but the adapter
  runs the pin, where they are elsewhere. `ConsIndShockModel.py:2063` (the default constraint) is a blank line and
  the default is at `:2077`; `:775`, `:719`, `:757` and `:766` (the envelope, the line, c̃) are at `:788`, `:732`
  and about `:770-784`; `:698` (`BoroCnstNat`) is at `:703`; `ConsMarkovModel.py:429` and `:583-588` (survival by
  state) are the worst income's probability and human wealth, survival being at `:446-447` and `:547-555`.
- **"The adapter" in the stone is two programs.** The stone says the adapter "builds the nodes itself", "computes
  the effective member's natural limit itself", decides the conditions, finds the targets, builds the population and
  takes the Euler residuals. In the code all of that is `common.py`'s, which hands the toolkit's part its nodes; the
  toolkit's part does only Encode, the call and the first Decode bullet. The stone never draws that line. The hub's
  own ruling (`results.md`, `experiments.md`: the representation is never prescribed by "code the adapters share")
  is contradicted by `common.py` prescribing the nodes, which `harness.md` records as a departure to be undone.
- **The constraint in force under natural.** The stone's `a_Nat` row: "the constraint in force the larger of `a_Art`
  and it", it being the nodes' limit. A natural member has no `a_Art`; the sentence holds only with the checker's
  convention that such a member's constraint is the stated laws' limit (`bst1.py:195-196`), which the stone does not
  state.
- **The protocol's `version()`.** `common.py`'s header: "version() and commit() (strings, or None)". The results
  schema requires `toolkit.version` as a string of at least one character, and `run()` writes it unconditionally, so
  a `None` version fails validation; only the commit may be `None`.
- **Inside the grid only.** The stone: "The population and every reported point lie below the solution grid's top".
  That rests on two tables no document ties together: `common.py`'s `LEVELS` (`solve_top` 100, 200, 400, 800;
  `dist_top` 60, 120, 240, 480) and the ladder's `aXtraMax` (100, 200, 400, 800), with request files that stop at
  m = 50. A ladder edited alone would break it silently. At low the grid's top in m is 105.4 and 106.1 on the two
  members.
- **`results.md` against its validator.** It marks the distributions of permanent income and of wealth in levels
  "(required)"; `results.schema.json`'s `TypeResults` admits neither (`additionalProperties: false`), and
  `common.py` writes neither. The document's header says the validator is to follow.
- **`for-toolkit-authors.md` on the protocol.** It gives `solve(member, beta, nodes, lev)`, receiving "the module's
  level dictionary"; `common.py` gives `solve` the toolkit's own `level_settings` when it has them.
- **`rosetta/README.md`, "The workflow".** "Not yet written: the other toolkits' adapters", while the same file's
  opening describes dolo's and quantecon-egm's adapters as running, and `harness.md` builds on "Two adapters".
- **"exactly `IndShockConsumerType`".** The stone says `calc_stable_points` runs only for that type; at the pin it
  also runs for exactly `PerfForesightConsumerType` (`ConsIndShockModel.py:1960-1963`). Of no consequence here.

## What could not be done

- **The method and settings files, and the strings, of the existing adapter cannot be reproduced.** No document
  states them, so `method_file_sha256`, `settings_sha256`, `toolkit.driver`, `effective_member.representation`,
  `euler_residuals.expectation_method` and `provenance.solver` will differ from the existing adapter's whatever its
  numbers are.
- **The stone's evidence could not be checked against its sources.** The findings, the records, the ontology, the
  other stones and the test of the toolkits' grids are not in the sandbox, so the gate's figures, the claim that
  HARK's grid is dolo's point for point, and byte identity with committed files are untested here.
- **`gridpoints.py` and the gate** that the stone names beside the adapter were not written; the task asks for
  `adapter.py`.
- **The project's memory was not read.** The repository's instructions ask every session to read
  `schemas/records/MEMORY.md` first; it lies under the repositories the clean room excludes, so it was left unread.
- **Two looks outside the sandbox, to check my own runs:** a process listing, to see whether the long run was still
  going, which showed another adapter's processes by their command lines; and the names in `~/.cache/numba`, to see
  whether HARK had written a cache. Nothing was read from either, and nothing was written into the pinned
  environment.
