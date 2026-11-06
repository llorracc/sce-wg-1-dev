# Clean-room log: dolo's part of the adapter, written from the stone and the hub

2026-11-06. The adapter is `harness/adapters/dolo/adapter.py`, 248 lines. Both required runs completed at `low` and
verified. Entries are named, not numbered.

## The outcome

    out/bst-restrained/results.json: validates, and its report is consistent with the member 6e8651cdf2cd…
    out/bst-p-zero-0.005/results.json: validates, and its report is consistent with the member b2e365cd24b4…

Both ran and verified on the first attempt (about ten seconds each; 255 iterations of `egm` each). Later changes
were one constant (the natural grid's start, below) and housekeeping. Each run repeats byte for byte. Beyond the two:
`toy`, `library`, the other two rungs and a variant of the restrained member with `borrowing_constraint: -0.5` run
and verify at `low`; the four experiment members also at `medium` and `high`.

**How far the result can be trusted without the other adapter.** The stone and the hub quote numbers from the
existing adapter's files. This adapter reproduces every one I could compute, to the digits quoted:

| the documents' number | where | this adapter |
|---|---|---|
| restrained kink at `high`: m = 0.974402, slopes 1 and 0.4206 | stone, evidence | 0.974402, 1.0000, 0.4206 |
| restrained mass at the constraint at `high`: 0.21273 | stone, evidence | 0.21273 |
| restrained mass at `low` read as the spline, 0.166; HARK's 0.231 | stone, departure on the rule | 0.1659 as the spline; 0.2310 read linearly |
| gaps to the restrained rule at `high`: 0.137, 0.061, 0.0267; falling by 2.254 and 2.286 | experiments.md; stone | 0.1374, 0.0610, 0.0267; 2.254 and 2.286 |
| MPC at the natural limit 6.1e-5 short at `high` on ℘ = 0.00005, approached by 3.5 to 3.8 per level | comparing-solutions.md | 6.08e-5; factors 3.55 and 3.75 |
| largest relative difference 6.3e-5 at m = 0.01 on ℘ = 0.00005 | comparing-solutions.md | the rule is 6.29e-5 below the closed form there |
| own-laws residual 6.9e-3, falling to 2.3e-3 across the method-only step | comparing-solutions.md | 6.90e-3, then 2.32e-3 on the level-four grids at 31 nodes |
| the method-only step moves dolo's rule by 8.1e-6 to 1.8e-5 across the four members | comparing-solutions.md | 8.11e-6 (restrained) to 1.80e-5 (℘ = 0.00005) |
| restrained residual under the stated laws at the finest level about 2.1e-4, under its own laws below 1e-6 | for-toolkit-authors.md, participation.md | 2.06e-4; 9.6e-7 |
| rules move by about 3.3e-3 to 3.5e-3 between `medium` and `high`, m up to 20 | comparing-solutions.md | 3.29e-3 to 3.45e-3 |
| m at 0.999, a at 0.999, a at 0.99 and the median of m for the four members | reference-solution.md | equal in every digit given |
| target near 1.041, mean MPC near 0.456 for the restrained member at the finest level | for-toolkit-authors.md | 1.0414, 0.4556 |

Three of these (6.1e-5, 6.3e-5 and 2.3e-3) fail with my first choice of the natural grid's start; that is how its
value was found. None of them tests the MPC's convention at a node, the tolerance, or the first rule, which stay undetermined.

## A. Lookups: facts the stone, its cards and the hub did not give

**What the level's `nest` means, the savings grid's spacing.**
Needed: the rule that places the savings points. Found: nowhere in the sandbox. `common.py`'s `LEVELS` row gives the
numbers (`solve_points=300, solve_top=100.0, nest=3` at `low`) and says they "are read by an adapter that states no
settings of its toolkit's own"; reference-solution.md speaks of "the nested grid of the levels"; nothing defines
nesting. I wrote it from my own memory of HARK's `make_grid_exp_mult`: points evenly spaced after `nest`
applications of log(1 + x), mapped back. That is knowledge from outside the clean room, and unchecked: HARK is not
installed in dolo's environment. The stone's nearest: "The savings grid is `egm`'s `a_grid`"; the cards':
"savings_grid: a_grid". Count, top and spacing: absent.

**Where the nested grid begins.**
Needed: whether the nesting runs from HARK's 0.001 above the start (with the start added in front) or from the
start itself. Found by trial against the hub's numbers. With HARK's form the slope at the natural limit is short of
the closed form by 7.46e-5, 7.49e-5 and 7.50e-5 at `low`, `medium` and `high` on ℘ = 0.00005: constant, where
comparing-solutions.md reports a fall of "3.5 to 3.8 per level" to 6.1e-5. Nested from zero above the start it is
8.11e-4, 2.28e-4 and 6.08e-5. The stone's nearest: "it starts at a_min = `a_Art`, so that the kink's point is
solved"; "on the same nodes and savings grids" (as HARK's adapter, whose grid is not in the sandbox).

**How far "just above the limit" is.**
Needed: the first savings point of a natural member. Found by trial: 1e-6 reproduces three numbers of
comparing-solutions.md (6.1e-5, 6.3e-5, 2.3e-3); 1e-9 gives 6.4e-5, 6.4e-5 and 2.4e-3; 1e-7, 2e-6 and 1e-5 also
miss. Seven extra solves at `high` and on the level-four grids. 1e-6 is also where `common.make_agrid` puts the
population grid's first node, which is a hint, not a statement. The stone's nearest: "For a natural member it starts
just above the limit." The value: absent.

**`maxit`'s value.**
Needed: the most iterations. Found: dolo's default is 1000 (`algos/egm.py`, line 16; reference-solution.md says the
same of dolo's defaults). By trial 1000 is too few: the toy's type with β = 0.99 needs 1525 iterations at `low`,
and the stone says the toy verifies in the adapter's tests. The stone's nearest: "iterated to convergence (`η_tol`,
`maxit`)"; the cards': "maxit: {semantics: \"the most iterations\"}". The value: absent.

**`η_tol`'s value.**
Needed: the stopping tolerance. Found: `LEVELS` has `tol` (1e-8 at `low`), which its comment gives to an adapter
with no settings of its own; whether dolo's adapter uses it is not said. `egm` compares it with the sum of the
largest change in c and the largest change in m at the savings points (`algos/egm.py`, lines 116 to 124). The
stone's nearest: "`egm(model, grid=grid, dp=dp, a_grid=a_grid, η_tol=tol, maxit=maxit)`". The value: absent.

**What the placeholder must be.**
Needed: an `exogenous` block that lets the model be discretized and solved. Found in `algos/egm.py` line 31
(`iid_process = isinstance(model.exogenous, IIDProcess)`), `compiler/model.py` lines 388 to 424 and 591 to 603, and
`numeric/processes.py`; settled by trial. With no block, `model.discretize()` fails ("'dict' object has no attribute
'discretize'"). dolo's current syntax, a block keyed by the shocks' names (`psi, xi: !Normal …`), imports and
discretizes, and `egm` then fails at its second iteration with an IndexError, since the block becomes a
`ProductProcess`, which is not an `IIDProcess`. `!ConstantProcess` fails with "Not implemented". A bare tag for
the whole block works: `!UNormal {sigma: …}`, as dolo's own example has it, or a two-dimensional `!Normal`. The
stone's nearest: "The block `exogenous:` holds only a placeholder."

**The calibration block.**
Needed: what the model file must calibrate. Found: `compiler/model.py` lines 281 to 341 (an uncalibrated parameter
or control is NaN) and `algos/egm.py` lines 52 to 54 (with no `dr0`, `egm`'s first rule is the calibrated `c`,
constant in m). By trial, with no calibrated `c` the rule is NaN and `egm` returns `a_converged` False. So the file
needs the seven parameters and `c`. The stone's nearest: its recast model lists "parameters: [beta, L, rho, R, G,
a_min, cbar]" and no calibration; the values of `cbar` and of the first `c`: absent.

**How to read the node values.**
Needed: "sol.dr's values at its uniform grid's nodes" (the cards' words). Found: `numeric/decision_rule.py` lines 116
to 119 and 408 to 436: the `DecisionRule` keeps only its cubic coefficients, so the values come back by evaluating it
at its own nodes, `sol.dr(sol.dr.endo_grid.nodes)`, both N × 1 (`numeric/grids.py`, lines 24 to 26 and 104 to 121).
By trial they equal m below the kink to 1.1e-16. The stone names neither the attribute nor the call.

**How `egm`'s rule continues outside its endogenous points.**
Needed: what the rule is below the first endogenous point, to place the savings grid's start. Found by trial:
`interpolation.splines.eval_linear`, which `egm` uses, continues the end segments linearly; `egm` then clips to the
bounds (`algos/egm.py`, lines 91 to 100). So below the kink the line is cut to c = m − a_min, and a natural member's
grid cannot begin at HARK's 0.001: that run gave a residual of 8.9e-2 under its own laws. The stone's nearest: "It
then evaluates that rule, clipped to the bounds"; the continuation: absent.

**The request points are nodes of the uniform grid.**
Needed: which segment's slope is the MPC at a request point. Found by trial: 36 of the experiment's 39 request points
equal a node of the 0.005 grid exactly (as numpy's `linspace` builds it, `numeric/misc.py` lines 55 to 66), and 3
(0.7, 0.94, 0.95) lie one unit in the last place below theirs. So the reported MPC is a one-sided slope chosen by a
convention, at every point the experiment asks for. The stone's nearest: "The MPC is the slope of the segment."
Which segment at a node: absent.

**dolo's version at run time.**
Needed: `version()` and `commit()`. Found: dolo has no `__version__`; `importlib.metadata.version("dolo")` gives
0.4.9.20. The installed release carries no commit. (`dolang.__version__` says 0.0.18 while the installed
distribution is 0.0.20: its attribute is stale.) The stone's nearest: "It is read in its release 0.4.9.20, tag
`v0.4.9.20` at `d782336b`".

**What importing dolo does.**
Found in `config.py`, lines 27 and 33 to 34, and by trial: the import sets numpy's error state to ignore everything,
for the whole process, the shared code after it included; and it makes an empty directory `dolo_*` in the system's
temporary folder that it never removes. The stone: absent.

**`yaml_import` takes a path, and reads any path holding "http" as a URL.**
Found in `misc/display.py`, lines 6 to 23. So the model must be written to a file, and where is the adapter's
choice. The cards' nearest: "dolo.yaml_import(path) of the recast model file".

**What `egm` returns, exactly.**
Found in `algos/egm.py` lines 84 to 138 and `algos/results.py` lines 21 to 28: `err` is the sum of the two largest
changes; the returned rule is the one before the last step (the last iteration's points are not copied on the
breaking pass); `iterations` is the last iteration's index from zero. The stone's nearest: "`err`, the largest
change in the rule and the state between its last two iterations".

**Given by the hub's code, not by its protocol text.** The layout of `nodes` in `solve(member, beta, nodes, own)`,
(p_psi, psi, p_th, th), and that `joint_shocks(member, *nodes)` gives the joint nodes; the window the hub asserts on
`mNrmMin`; that `cFunc` is called with scalars and with arrays and `derivative` with arrays. All read from `run()`.

## B. Open decisions: what the documents left to me, and what I chose

Measured effects are at `low` on the two required members, against the adapter as it stands.

**The savings grid.** `solve_points` points, the first at the start, the last `solve_top` above it, evenly spaced
after `nest` applications of log(1 + x). Had I built HARK's grid from 0.001 with the start in front: c moves by up
to 3.0e-6 (restrained) and 1.9e-5 (natural), the reported MPC by 1.3e-3 and 6.5e-3. A geometric grid: 1e-3 in c.

**The natural grid's start.** 1e-6 above the limit; my first choice was 1e-9. Between the two: c moves by 9e-8
and the MPC by 5.8e-6 on ℘ = 0.005; nothing on the restrained member.

**The MPC at a node.** The segment to the right. The other choice changes `rule.mpc` at 28 (restrained) and 32
(natural) of the 39 request points, by up to 5.3e-3 (restrained, at m = 1) and 1.3e-2 (natural, at m = 0.975), and
changes nothing else in the file. Nothing in the sandbox decides it. This is the largest undetermined number.

**`η_tol`.** The level's `tol`, 1e-8 at `low`. With dolo's default 1e-6 instead: 1.3e-7 in c.

**`maxit`.** 20000, so that it never binds.

**The first rule and `cbar`.** `c: 1.0` and `cbar: 1.0`; no `dr0` passed. With c 0.5 or 2.0: below 1e-10. With
`cbar` 0.9: 1e-15.

**The placeholder.** `exogenous: !Normal` with `Sigma: [[0.01, 0.0], [0.0, 0.01]]`, two-dimensional as the model's
two shocks. With dolo's `!UNormal {sigma: 0.1}` the results file is the same to the last bit.

**The kink's point.** One evaluation of the Euler equation at a = a_min, with the rule read through the node values,
then inserted; not repeated with the point in. At `low` repeating changes nothing. At `high` a shock's node falls in
the kink's cell and the repeated value is 1.5e-6 higher; the stone's 0.974402 is the single evaluation's (0.9744021),
not the repeated one's (0.9744035).

**The uniform grid.** From a_min to a_min + `solve_top`, with `solve_top`/0.005 + 1 points: the stone's 20,001 to
100 when a_min is 0. For a_min below zero the stone says nothing; the variant with −0.5 verifies.

**a_min, and which members get the kink.** a_min is the constraint in force of the effective member, by the
arithmetic of `common.effective_member_block`. The grid's start and the kink's point go by the family
(`member.natural`).

**What `solve` returns beside the rule.** `mNrmMin` = a_min, the uniform grid's first node; `vFunc` = None.

**The rule's details.** Node values as `sol.dr(nodes)`, not clipped again. Beyond the grid's ends the end segments
continue (never reached in these runs).

**Where the model file goes.** `<out>/model-beta-<beta>.yaml`, one per type, beside the results; the adapter reads
`--out` from its arguments before calling `run`, and falls back to a temporary directory.

**The settings file.** Keys: `level`, `nodes_per_shock`, `transition_nodes_per_shock`, `savings_points`,
`savings_top`, `savings_nesting`, `savings_start_above_natural_limit`, `solution_tolerance`, `max_iterations`,
`grid_points`, `grid_max`, `grid_step`, `histogram_points`, `histogram_top`, `diagnostics_nodes_per_piece`. The cards
name seven (`solution_tolerance`, `max_iterations`, `savings_grid`, `grid_max`, `grid_points`, `nodes_per_shock`,
`histogram_points`); `savings_grid` has no plain value, so I wrote the three numbers that make it.

**The method file.** The cards' seven entries in numerics.md's form: the tag as the method where there is one, the
cards' words where there is none, the cards' handler. for-toolkit-authors.md says to copy a committed
`methods.yaml`, which the sandbox does not hold. So both hashes will differ from the existing files'.

**The identity strings.** `name` "dolo"; `driver` "harness/adapters/dolo/adapter.py"; `commit()` None, a release
being named by its version; `representation` and `diagnostics_method` in my words; `provenance.solver` holds, for
each type, `beta`, `iterations`, `a_converged`, `a_tol` and `err` (the stone says the adapter records the last two
and not where).

**No ladder file.** No `level_settings` and no `prepare`: `solve` reads the level's row, as for-toolkit-authors.md
describes it, and the 0.005 is a constant of the adapter.

**Housekeeping.** Standard output goes to a discarded buffer around `egm`. A solve that does not converge is
recorded and then raises. The adapter removes dolo's empty temporary directory when it ends and leaves numpy's
error state as dolo sets it.

## C. Errors: statements found wrong, stale or contradictory

**harness.md, "What exists to build on":** the two adapters "solve on the same nodes and savings grids, which
`common.py` supplies to both". `common.py` supplies the nodes and no savings grid: only the row's three numbers;
`make_agrid` is the population's grid.

**The stone, evidence: "on the same nodes and savings grids"** as HARK's adapter. The hub describes HARK's grid as
starting 0.001 above the constraint (reference-solution.md: "48 grid points to 20 above 0.001 with nesting 3";
`common.kink_point`: "HARK's first endogenous gridpoint sits at a = aXtraMin above it"), while the stone starts
dolo's at a_min or just above it. A grid built as HARK's with the start in front contradicts the hub's own numbers
(the trial under A). I cannot say what HARK's adapter does; the phrase misleads on the one setting the stone omits.

**The stone, capabilities table: "survival ℒ | β ℒ | — | ℒ = 1 only".** The same table gives "`toy`'s types" as
tested and the evidence says toy's file verifies; `toy.yaml` has `survival: 0.99375`. Here toy runs and verifies.

**The stone, link texts.** "[`../adapters/dolo/adapter.py`]" and "[`../adapters/common.py`]" show paths from
before the layout's move; their targets are under `../harness/adapters/`.

**The stone and the cards on `err` and `η_tol`:** "the largest change in the rule and the state". It is the sum of
the two largest changes (`algos/egm.py`, line 117). Imprecise, not wrong.

**The stone's recast model cannot be solved as printed.** "The recasting" gives symbols, equations, domain and
options; with no calibration and no exogenous block it imports, with NaN parameters, and cannot be discretized.

**results.md against its validator.** It marks the distributions of permanent income and of wealth in levels
"(required)" and sketches `permanent_income`, `a_levels` and `joint` in a type. `results.schema.json` has none of
them and forbids other keys in a type, and `common.py` writes none; a file that followed the document would be
refused. The document says its validator "follows"; stale by its own account.

**Where a job's files go.** harness/README.md: `<run folder>/<toolkit>/<member>/<level>/`, "named for the level";
harness.md, registry.md's example and `compare.py`: `level-<n>`. No bearing on the adapter.

**for-toolkit-authors.md on the protocol.** It lists `methods` and `solver` among "the strings"; they are a list and
a dict (`common.py`'s header has it right). It calls `settings.yaml` "a flat map … with a `level` key", while
numerics.md says a settings file gives a value to the methods' declared settings "and to nothing else", under
`settings:`.

**results.md asks for the MPC "as a derivative, not a finite difference".** The stone's MPC is the slope between
nodes 0.005 apart. The stone says so and gives its size; the two documents are in tension, not in conflict.

**Checked and found right in the stone:** the leftover print at `egm.py` line 110; `!LogNormal`'s default μ of 1;
`Truncation` needing a `cdf` that `LogNormal` lacks; `FiniteDistribution` having no tag; equiprobable nodes at bin
medians; the cubic `DecisionRule` with no derivative; 20,001 points to 100 at the low level; 0.166 against 0.231.

## What was read and run

- **Documents, all in the sandbox:** the three files in `rosetta/`; `harness/README.md` and
  `harness/adapters/common.py`; in `schemas/`: numerics.md, effective-member.md, harness.md, for-toolkit-authors.md,
  reference-solution.md, conventions.md, the parts of comparing-solutions.md, experiments.md, participation.md and
  registry.md that mention dolo, the grids or the container; in `schemas/bst/`: model.md, results.md, the results
  schema, the members, the request files, the experiment's folder; in `schemas/checker/`: check.py, bst1.py, the
  README and test_rosetta.py.
- **dolo's source, in the pinned environment:** `algos/egm.py`, `algos/results.py`, `tests/test_egm.py`,
  `compiler/recipes.yaml`, `compiler/model.py`, `compiler/model_import.py`, `compiler/misc.py`,
  `compiler/objects.py`, `numeric/distribution.py`, `numeric/processes.py` (to line 330),
  `numeric/decision_rule.py`, `numeric/grids.py`, `numeric/misc.py`, `misc/display.py`, `config.py`, `__init__.py`.
  No other package's source was read; `interpolation`'s `eval_linear` was tried, not read.
- **Not read:** anything under /home/shared/github/ or /home/econ-ark/github/ but the environment's packages; no git
  history; nothing on the web. That includes `schemas/records/MEMORY.md`, which the repository's CLAUDE.md asks
  every session to read first: the clean room's rule was followed instead.
- **Runs,** all under `out/`: the two required ones; under `out/_probe/`, the checks listed above, kept with their
  scripts (`variant.py`, `eps_probe.py`, `grid_probe.py`, `spline_variant.py`, `sens.py`).

## What could not be done

- **Compare with HARK's adapter or the existing dolo adapter.** Every agreement the stone claims with HARK is
  unchecked here.
- **Settle from the documents:** the MPC's segment at a node; `η_tol`; `maxit`; the first rule and `cbar`; the text
  of the method and settings files. None prevents a run; the first changes reported numbers.
- **Repeat the stone's test of dolo's own example** ("475 iterations", "c(4) = 1.149"): the example file is not in
  the installed package, and the stone's listing of it has no calibration.
- **Leave /tmp untouched.** Before I found that importing dolo makes a directory, 28 of my processes each left an
  empty `dolo_*` in /tmp. I did not delete them, since they are outside the sandbox. Later runs leave none.
