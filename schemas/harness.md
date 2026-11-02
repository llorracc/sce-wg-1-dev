# The harness: every toolkit on every experiment

Plan, 2026-11-02, drafted on the owner's request of that day and approved by him with six decisions the same morning;
see the [README](README.md). **Status: APPROVED, in progress:** the experiment schema
([`experiments.md`](experiments.md)), the layout and the runner ([`../harness/`](../harness/README.md)) are done; the
comparator is next.

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
  savings grids.
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
3. **The comparator.** Accepted when its verdicts and numbers on the committed HARK and dolo runs match the prototype's
   and `compare_toolkits.py`'s.
4. **A full run of restrained-limit** for both toolkits at all three levels, through the harness, recorded as a
   findings record that should repeat the hand run of 2026-11-01.
5. **The toy-hafiscal experiment,** once its member is delivered and the results schema carries the iMPC.
6. **The layout:** done on 2026-11-02, before the runner, in commit `9675109`.
7. **Continuous runs,** later: the harness at `low` for every toolkit on every pull request.

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

## Risks

- **The toolkits move.** dolo's master has moved to Python 3.12, numpy 2 and JAX, untagged. HARK's pin is a commit on
  a fork's branch, kept reachable by the fork's tags. The registry pins both, and a re-pin is a recorded change.
- **Two Pythons on one machine,** for as long as dolo's release needs 3.11; `uv` handles it, as it did on 2026-11-01.
- **An adapter's errors look like a toolkit's.** The verdicts say which adapter and which commit produced each file, so
  that a failure is traced to the adapter or to the toolkit before it is reported.
