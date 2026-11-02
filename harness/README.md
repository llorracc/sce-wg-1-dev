# The harness

It runs every toolkit on an experiment and verifies what each writes. The plan is
[`../schemas/harness.md`](../schemas/harness.md), and the experiments are described in
[`../schemas/experiments.md`](../schemas/experiments.md). The runner and the toolkit list are built; the comparator,
which evaluates an experiment's checks, is next.

| file | what it is |
|---|---|
| [`runner.py`](runner.py) | the runner: `list`, `run` and `verify` |
| [`toolkits.yaml`](toolkits.yaml) | the toolkits: each one's adapter, code, environment, Rosetta Stone, levels and thread cap |
| [`envs/`](envs/) | one `uv` project per toolkit, with its lock file and interpreter |
| [`adapters/`](adapters/README.md) | the adapters, one per toolkit, and the code they share |
| `pyproject.toml`, `uv.lock` | the harness's own environment, in which the runner and the checker run |
| [`test_runner.py`](test_runner.py), [`test_support/`](test_support/) | the runner's tests, on a stand-in toolkit |
| `runs/` | run folders, ignored by git |

## Running it

```sh
uv run --project harness --frozen python harness/runner.py list
uv run --project harness --frozen python harness/runner.py run schemas/bst/experiments/restrained-limit/experiment.yaml \
    --toolkits hark,dolo [--levels low,medium,high] [--members <id>,...] [--jobs 8] [--out <run folder>]
uv run --project harness --frozen python harness/runner.py verify harness/runs/restrained-limit-1
uv run --project harness --frozen --group dev pytest -q harness/test_runner.py
```

- **What `run` does.**
  - It refuses an experiment the checker finds problems with: a wrong hash, a missing file, an undeclared member, a
    quantity the results schema does not have.
  - It builds each toolkit's environment from its lock file.
  - It runs one job for each toolkit, member and level, in parallel, each through the adapter's command line with
    the toolkit's thread cap.
- **Where a job writes.** Into `<run folder>/<toolkit>/<member>/level-<n>/`, with n = 1, 2, 3 for `low`, `medium`,
  `high`. Beside the adapter's files it leaves `adapter.log` and `job.json`: the status, the command, and a fingerprint
  of what the output depends on:
  - the member's and the request's hashes;
  - the level;
  - the environment's lock file and interpreter;
  - the toolkit's code, including the checker modules the adapters import.
- **Resuming.** A job whose fingerprint is unchanged and whose results file exists is skipped. A rerun redoes only
  what failed or changed.
- **The run's record.** `manifest.json` names the experiment's hash, the members', each toolkit's environment and
  code, the harness's commit, when the run started, and each job's status. Nothing records how long anything took.
- **What `verify` does.** It runs `check.py --verify-results` on every results file, and checks that each carries
  the quantities the experiment's `reports` names. It writes `verification.json`.

## The adapter contract

```sh
<adapter> <parameter file> --out <dir> --level <n> --request <request file>
```

The adapter writes `results.json`, `methods.yaml` and `settings.yaml` into `<dir>` and exits with 0. It runs from the
repository's root. Any language will do; the harness reads only the files and the exit code. A toolkit with no
`environment` in `toolkits.yaml` runs in the harness's own Python, as the tests' stand-in does.

## The environments

Each toolkit's environment is a `uv` project in `envs/<toolkit>/`: `pyproject.toml`, its `uv.lock`, which pins every
dependency, and `.python-version`. The adapter runs in it with `uv run --frozen`, so nothing is resolved at run time.

To begin with, the projects pin the interpreter and the numpy, scipy and numba that the adapters' runs of 2026-11-01
recorded, so that the harness reproduces those runs' files:

| toolkit | Python | numpy | scipy | numba | the toolkit |
|---|---|---|---|---|---|
| HARK | 3.12.3 | 2.5.4 | 1.18.1 | 0.68.1 | llorracc/HARK at `11852805` |
| dolo | 3.11.14 | 1.26.4 | 1.17.1 | 0.68.1 | 0.4.9.20 |

A change of pin is a change to the project and its lock file (`uv lock` in the project's folder), recorded in a commit.

## Large outputs

Run folders are ignored by git. A run kept as a record goes into the findings, but without the Jacobians' matrices,
which stay out of git for now; the results file's hashes of them are the record.
