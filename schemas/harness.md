# The harness: every toolkit on every experiment

Plan, 2026-11-02, drafted on the owner's request of that day and approved by him with six decisions the same morning;
see the [README](README.md). **Status: APPROVED, in progress:** the experiment schema
([`experiments.md`](experiments.md)), the layout and the runner ([`../harness/`](../harness/README.md)) are done. Revised
on the evening of 2026-11-02 and on 2026-11-03 by the owner's rulings, below: the schemas' revision and the adapters'
independence come before the comparator.

## The four pieces

The owner set out the project as four pieces on 2026-11-02:
1. **An ontology** of buffer-stock models, consistent with Bellman's ontologies: what the terms mean, naming no toolkit
   ([`../ontologies/buffer-stock-models/`](../ontologies/buffer-stock-models/), at draft.2 on its own branch).
2. **Schemas** of the models and of the experiments every toolkit is to perform: the families, their parameter, request
   and results files, and now the experiment files.
3. **A Rosetta Stone for each toolkit**: how its names and methods map onto the ontology and the schemas, and where it
   departs from them ([`rosetta/`](../rosetta/README.md): HARK, dolo and QuantEcon's JAX code).
4. **A harness** that runs every toolkit on every experiment, checks the results and compares them.

The **adapters** join the third piece to the fourth. A stone states a toolkit's mapping in words and cards; its adapter
is that mapping as code, and the harness's plug-in for the toolkit.

"Harness" is the usual word: a test harness runs a suite against an implementation, and a benchmark or evaluation
harness does it for many implementations at once, as EleutherAI's `lm-evaluation-harness` does for language models. The
whole arrangement is what other fields call a model intercomparison:
- **CMIP** in climate science: the CF conventions' standard names (an ontology), the experiment protocols and data
  request (what every model runs and reports), and CMOR, which rewrites each model's output into the common form, as an
  adapter's decode does;
- **YCSB** for databases: workloads, run against each database through its own "binding";
- in economics, the 2010 comparison of solution methods for Krusell and Smith's model in the *Journal of Economic
  Dynamics and Control*, and the Macroeconomic Model Data Base.

## What exists to build on

- **Two adapters** with the same command line, HARK's and dolo's, sharing their toolkit-neutral code in
  [`adapters/common.py`](../harness/adapters/common.py). On the same member, level and request they solve on the same nodes and
  savings grids, which `common.py` supplies to both: a departure from the ruling of 2026-11-02 that each toolkit
  represents the laws its own way, to be undone (stage 4 below).
- **The checker:** `check.py <member> --verify-results <results.json>`.
- **The restrained-limit experiment's** request files, comparison scripts, and an experiment file.
- **A run made by hand,** on 2026-11-01:
  - a shell script started each adapter on each member and level, two threads apiece;
  - the checker verified each file;
  - the comparison scripts wrote the tables and figures;
  - the files were copied into the findings.

  The harness is that run, made a program.

## The design

**The adapter contract.** The harness talks to an adapter only through a command line and files:

```sh
<adapter> <parameter file> --out <dir> --level <n> --request <request file>
```

It writes `results.json`, `methods.yaml` and `settings.yaml` into `<dir>` and exits with 0, or with another code and a
message on standard error. An adapter in any language can plug in, Julia's or MATLAB's as well as Python's. Python
adapters keep sharing `common.py`'s toolkit interface, which is a convenience and not part of the contract.

**What the harness gives a toolkit** (the owner's ruling of 2026-11-02, 18:28): the parameter file, which is the
model; the request file, which says where to report; the name of a precision level; and the folder. Nothing of
methods or settings, and no representation of the laws: the true model's laws are the truncated lognormals, and each
toolkit represents them as it likes. `common.py` reads the files, checks the member and writes the results; it
chooses nothing numerical.

**The toolkit registry**, `harness/toolkits.yaml`, one entry per toolkit:

```yaml
hark:
  adapter: harness/adapters/hark/adapter.py
  stone: rosetta/hark.md
  environment: harness/envs/hark      # pyproject.toml and uv.lock: Python 3.12, HARK at 11852805, and the rest
  levels: {low: 1, medium: 2, high: 3}
dolo:
  adapter: harness/adapters/dolo/adapter.py
  stone: rosetta/dolo.md
  environment: harness/envs/dolo      # Python 3.11, dolo 0.4.9.20 with dolang 0.0.20, and the rest
  levels: {low: 1, medium: 2, high: 3}
```

Each toolkit runs in its own environment: a `uv` project with a lock file that pins every dependency, not only the
toolkit, and the harness runs the adapter in it with `uv run --frozen`. HARK's needs Python 3.12 and dolo's release needs
Python below 3.12, so one environment cannot hold both. The lock files pin, to begin with, the versions the runs of
2026-11-01 recorded (numpy 2.5.4 with HARK, 1.26.4 with dolo), so that the harness can reproduce those files.

**The runner.**
- **Jobs.** `harness run <experiment> --toolkits hark,dolo` expands the experiment into one job for each member, level
  and toolkit: twelve for each toolkit on restrained-limit.
- **Execution.** It runs the jobs in parallel, each with its thread count capped (`OMP_NUM_THREADS` and its kin), and
  keeps each job's log and exit code.
- **Resuming.** A job whose results file exists is skipped if the file names the same parameter, request, method and
  settings hashes and the same toolkit version and commit. A rerun after a failure redoes only what failed.

**Verification.** Every results file goes through `check.py --verify-results`. The harness also checks that it carries
the experiment's `reports`. A file that fails either is reported, and the experiment's checks that need it are not
evaluated.

**The comparator** evaluates the experiment's `checks` (the prototype of 2026-11-02 did this for restrained-limit):
- for `members`, within each toolkit and level;
- for `toolkits`, for every pair of toolkits run;
- for `levels`, within each toolkit.

It writes a verdict for each check, with the numbers behind it, as a table and as JSON. Then it runs the experiment's
`report_scripts` for the tables and figures particular to the experiment.

Since the revision of 2026-11-02 and 03 it also computes, from a results file's joint distribution where an experiment
asks for one, the Lorenz curves of permanent income and of wealth in levels with one code for every toolkit, and tests
the toolkit's own numbers against them; and it evaluates the checks against the stated member, the expectations'
distance from the closed forms and the agreement within the toolkits' own convergence (`experiments.md`).

**The run's record.** Each run writes a folder holding:
- the results, method and settings files, laid out `<toolkit>/<member>/level-<n>/`;
- the logs;
- the verdicts and the reports;
- a manifest naming every hash: the experiment's, the members', the requests', each toolkit's version and commit and
  its environment's, and the harness's own commit.

The manifest records when a run was made, but no run times or speeds (the memory on timings). A findings record stays
hand-written: the harness gives the numbers, and a person says what they establish.

**The command line, sketched:**

```sh
harness run     <experiment> --toolkits hark,dolo [--levels low,medium] [--jobs 8] --out <run folder>
harness verify  <run folder>          # the checker on every results file
harness compare <run folder>          # the checks, the verdicts, the report scripts
harness list                          # the experiments and the toolkits
```

**What it does not do.**
- It estimates nothing. toy-hafiscal's estimation is HARK's and HAFiscal's alone, and its member enters the harness
  delivered.
- It judges nothing beyond the experiment's checks. A toolkit that passes them is consistent with the others, not
  proved right.
- It never edits an adapter's output.

## In order

Each stage is checked before the next starts.
1. **The experiment schema.** Drafted, with restrained-limit as its first instance and 17 tests
   ([`experiments.md`](experiments.md)), and approved.
2. **The registry and the runner**, with `harness/toolkits.yaml` for HARK and dolo. Done and accepted on 2026-11-02
   ([the findings](records/findings/2026-11-02_harness-acceptance/README.md)); see [`../harness/`](../harness/README.md).
   - Tested on a stub toolkit, whose adapter copies a canned results file, so that the tests need neither HARK nor dolo.
   - Accepted when, at `low`, each real toolkit's results files are identical byte for byte to the committed ones.
     HARK's adapter was known to reproduce its files exactly: its refactor did on 2026-11-01. dolo's was checked by
     this stage, and does, but for the adapter's own path, which the layout changed.
3. **The schemas' revision of 2026-11-02 and 03:** the representation left to each toolkit, and the distribution of
   permanent income with the joint ([`bst/results.md`](bst/results.md), [`bst/conditions.md`](bst/conditions.md),
   [`experiments.md`](experiments.md)). First the documents, as a proposal to the owner; then the results schema's
   `permanent_income`, `a_levels` and `joint` blocks, the checker's reading of their statuses, and the experiment's second
   version, with the first's members. No validator, member or hash changes. Accepted when the checker's tests pass
   with the new blocks' breaks caught.
4. **The adapters' independence:** `common.py` keeps reading, checking and writing, and each adapter takes its own
   representation of the laws, its own grids, and its own population method, with mortality where the member has it
   and the joint of (m, 𝐩, c, a) where an experiment asks for it; dolo's needs a population method with newborns,
   which its release lacks. Accepted when each adapter's files verify and its Euler residuals against the stated laws
   fall with its level.
5. **The comparator.** Accepted when, on the first version's committed runs, its verdicts and numbers for the checks
   that survive match the prototype's and `compare_toolkits.py`'s, and on a run that carries joints it computes the
   Lorenz curves from them.
6. **A full run of restrained-limit's second version** for both toolkits at all three levels, through the harness,
   recorded as a findings record; the hand run of 2026-11-01 remains the record of the first version.
7. **The toy-hafiscal experiment,** once its member is delivered and the results schema carries the iMPC.
8. **The layout:** done on 2026-11-02, before the runner, in commit `9675109`.
9. **Continuous runs,** later: the harness at `low` for every toolkit on every pull request.

## The adapters' independence: the plan for the goals of 18:28 (stage 4)

Drafted on 2026-11-03 on the owner's request; **status: PROPOSED**, no code changed. The goals, from the rulings of
18:28:43 and 19:09:13 on 2026-11-02: the harness gives each toolkit parameters, never methods or settings; the true
model's laws are the truncated lognormals, and each toolkit represents them, solves, and builds its population as it
chooses; what it chose is read from what it reports, never prescribed.

**What the harness gives, unchanged:** the parameter file, the request file, a level's name and the folder. The name
is the one input that is not a parameter: it names an element of the toolkit's own ladder
([`numerics.md`](numerics.md)), and `toolkits.yaml` records which element each toolkit means by `low`, `medium` and
`high`. The runner does not change.

**What moves out of the shared module.** `harness/adapters/common.py` keeps reading the member and the request,
checking the member, computing the reports from what an adapter hands it (the effective-member block from the
adapter's own representation, the GL ordinates and quantiles from the adapter's own distribution, the Euler residuals
under the stated laws) and writing the three files. It loses every numerical choice:
- the `LEVELS` table and `NAMED_LEVELS`;
- the representation of the laws: `law_nodes`, `law_quadrature`, `state_shocks`, `joint_shocks`, `shocks`;
- the grids and the population: `make_agrid`, `Population`, `newborn_dist`, `stationary`;
- the `--nodes` option.

One numerical setting stays, documented as the verifier's and not the toolkit's: the quadrature of the diagnostics'
Euler residual under the stated laws, 32 Gauss-Legendre nodes per piece, which tests a solution against the model and
must not depend on the toolkit's representation. It is written into `settings.yaml` under `diagnostics`.

**What each toolkit owns.** Beside each adapter, its ladder, `harness/adapters/<toolkit>/ladder.yaml`, naming its
method file and the elements `low`, `medium` and `high`, and any more, in the toolkit's own names; the adapter reads
the element the level names and writes it out as the run's `settings.yaml`, as now. A validator for ladder and
settings files, the first of those `numerics.md` calls for, checks the shape: named elements, plain values, no
parameter of the model among them.
- **HARK's adapter.** The representation of the laws becomes its own choice: the equiprobable nodes with exact
  conditional means of the truncated laws that `law_nodes` computes today move into the adapter, recorded in its stone
  as the adapter's and not HARK's, since HARK's own `discretize` does not truncate; or HARK's own discretization, if
  the stone can state it. The solution grid stays HARK's, `aXtraCount`, `aXtraMax`, `aXtraNestFac` and `tolerance`,
  set from the ladder. The population becomes HARK's: its transition-matrix histogram on HARK's own distribution grid,
  which its Jacobians already use, with mortality and the family's newborn through `MrkvPrbsInit`, `NewbornTransShk`
  and the newborn permanent-shock switch of draft HARK#1860; or HARK's simulator, with standard errors. The adapter's
  gate: at `low`, its new populations against the committed ones, the difference recorded as a finding, not a defect.
- **dolo's adapter.** Its own nodes: dolo's native discretization of a lognormal, equiprobable at bin medians and
  untruncated, is one choice, whose effective member differs from the stated one in E[ψ] and E[θ] by an amount the
  check `approaches_stated_member` measures; a quadrature of the truncated laws written by the adapter is the other.
  Its own `a_grid`. Its population: dolo's `ergodic_distribution` has no deaths and no newborns, so a member with
  ℒ < 1 needs a population method of the adapter's own, a lottery or a simulation with mortality written in numpy for
  dolo, a departure its stone states; until then dolo reports the population of a member with mortality as
  `not_computed`. The owner decides which.
- **Every adapter:** the joint of (m, 𝐩, c, a) where an experiment asks for it, and the distributions of permanent
  income and of wealth in levels ([`bst/results.md`](bst/results.md)).

**What the checks then mean.** The two toolkits no longer share a representation, so `same_effective_member` is gone,
and the experiment's second version asks what [`experiments.md`](experiments.md) states: each toolkit's effective
member approaches the stated member with its level, the Euler residuals under the stated laws fall, and the rules
agree within the two toolkits' own convergence. A difference between the two is then a difference of representation
and method, which is what a comparison of toolkits is for.

**Accepted when:**
1. `common.py` holds no numerical constant but the diagnostics' quadrature, and no function that chooses nodes,
   grids or a population;
2. each adapter runs `low`, `medium` and `high` through the runner on restrained-limit's members, every results file
   verifies, and its `methods.yaml` and `settings.yaml` are its own ladder's;
3. the two effective members differ, and each approaches the stated member with the level;
4. HARK's rules at `high` agree with the committed ones within its own convergence, and its populations' difference
   from the committed lottery is recorded;
5. the stones say what each adapter chooses, and dolo's says what its adapter wrote for it;
6. a findings record holds the numbers.

**In order:** the ladder files and their validator; HARK's adapter; dolo's adapter; `common.py` stripped and the
`--nodes` flag removed; the runs; the stones; the record. The comparator, stage 5, follows on the runs.

**The owner's decisions:** dolo's population with mortality, adapter-written or `not_computed`; HARK's population by
transition matrix, recommended as deterministic and the Jacobians' own, or by simulation; the diagnostics' quadrature
staying in the shared module as the verifier's.

## The owner's decisions (2026-11-02, 10:33:47)

1. **Words:** approved. The restrained-limit and toy-hafiscal test suites are experiments, and `numerics.md`'s suite of
   settings elements is a ladder; applied to the live documents the same morning.
2. **When two toolkits agree:** the first experiment's two checks stand: the same effective member, to 10⁻¹², and a
   difference between the rules that falls at each finer level. A fixed tolerance is not used, because the levels mix
   the nodes into the grid (`experiments.md`). The sharper test, a tolerance from a ladder of method-only settings at
   fixed nodes, is deferred until later.
3. **The layout:** approved. The four pieces become:
   - `ontologies/` (as now);
   - `schemas/`, the families, the experiments and the checker;
   - `rosetta/`;
   - `harness/`, with the adapters and the registry.

   The move is one commit with nothing else in it.
4. **The environments:** lock files from the start. Each toolkit's environment is a `uv` project,
   `harness/envs/<toolkit>/pyproject.toml` with its `uv.lock`, and the harness runs each adapter with `uv run --frozen`
   in it. The registry names the project in place of a requirement list.
5. **Large outputs:** the Jacobians' matrices are kept out of git for now. A run folder's `.npy` files are ignored by git,
   and the results file's hashes of them are the record.
6. **The spelling of names:** the experiment file's underscores, following the schemas' keys, approved. Whether the
   ontology's names keep their hyphens is still open.

## The owner's rulings (2026-11-02, evening, and 2026-11-03)

- **18:28:43.** The harness gives each toolkit parameters, not methods or settings. The runner as built passes a level
  number that the adapters' shared code turns into grids, nodes and tolerances, and the shared code hands both
  toolkits the same nodes, grids and population method; that is the departure stage 4 undoes.
- **19:09:13.** The harness also asks for the model's estimate of the buffer-stock target; the ergodic distributions
  of m or a and of permanent income, and the joint distributions an economy of these consumers generates, from which
  population-wide E[c], E[u′(c)], E[a] and E[m] and perhaps their log variances are computed; and the shared code
  must not insist on one representation of the shocks: the true model has truncated lognormals, which each toolkit
  may discretize, represent continuously, or otherwise, as it chooses.
- **19:17:06 and 21:00:56,** superseded on 2026-11-03, below. The framework requires a mortality probability sufficient for a stationary distribution
  of permanent income; and, on the four questions put to him, the owner accepted: a member-level choice of the
  newborn's permanent income, `one` or `trend`, the toy at `one` and the restrained-limit members at the trend; as
  validity conditions ℒ < 1 and, at `one`, ℒ𝒢 < 1, the variance and marginal-utility conditions staying domain rules
  with statuses; the restrained-limit members' ℒ chosen for a tail exponent of at least 2, with 𝒢 = 1.03 kept; and
  the name: the stationary income condition at 21:00:56, and at 21:24:16 the owner's own choice, the stationary
  permanent income condition, SPIC. The reasoning and the numbers are in the rulings of the day.
- **2026-11-03, 04:37:53.** The SPIC requirement is removed: all that is needed is a way to calculate permanent
  income inequality, and Lorenz curves give it. The ruling of 19:17:06 and the decisions of 21:00:56 that served it
  are superseded: no validity condition on ℒ, no moment conditions, no `newborn` key, the restrained-limit members
  at BST's ℒ = 1 as before, `library` kept, no means in levels, and no hash changed. What remains is the
  distribution of permanent income, reported behind a status, its Lorenz curve defined when ℒ < 1 and ℒ𝒢 < 1, and
  the joint, optional ([the rulings of 2026-11-03](records/rulings/2026-11-03_harness-decisions.md)).

## Risks

- **The toolkits move.** dolo's master has moved to Python 3.12, numpy 2 and JAX, untagged. HARK's pin is a commit on
  a fork's branch, kept reachable by the fork's tags. The registry pins both, and a re-pin is a recorded change.
- **Two Pythons on one machine,** for as long as dolo's release needs 3.11; `uv` handles it, as it did on 2026-11-01.
- **An adapter's errors look like a toolkit's.** The verdicts say which adapter and which commit produced each file, so
  that a failure is traced to the adapter or to the toolkit before it is reported.
