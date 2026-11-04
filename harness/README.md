# The harness

It runs every toolkit on an experiment and verifies what each writes. The plan is
[`../schemas/harness.md`](../schemas/harness.md), and the experiments are described in
[`../schemas/experiments.md`](../schemas/experiments.md). The runner and the toolkit list are built; the comparator,
which evaluates an experiment's checks, is next.

| file | what it is |
|---|---|
| [`runner.py`](runner.py) | the runner: `list`, `run`, `verify` and `register` |
| [`records.py`](records.py) | the run registry's records: the repository's state, the environment's hash, the machine, the durations |
| [`execution-record.schema.json`](execution-record.schema.json), [`runs.registry.schema.json`](runs.registry.schema.json) | the record's schemas: the core destined for REMARK, and the fork's entry with its own fields ([`../schemas/registry.md`](../schemas/registry.md)) |
| `runs.registry/` | the registry: a folder per registered run, one record per job and per build |
| [`toolkits.yaml`](toolkits.yaml) | the toolkits: each one's adapter, code, environment, Rosetta Stone, levels and thread cap |
| `adapters/<toolkit>/env/` | each toolkit's environment, defined and pinned by its adapter: a `uv` project with its lock file and interpreter, and a Dockerfile that builds it as an image |
| [`adapters/`](adapters/README.md) | the adapters, one per toolkit, and the code they share |
| `pyproject.toml`, `uv.lock` | the harness's own environment, in which the runner and the checker run |
| [`test_runner.py`](test_runner.py), [`test_support/`](test_support/) | the runner's tests, on a stand-in toolkit |
| `runs/` | run folders, ignored by git |

## Running it

```sh
uv run --project harness --frozen python harness/runner.py list
uv run --project harness --frozen python harness/runner.py run schemas/bst/experiments/restrained-limit/experiment.yaml \
    --toolkits hark,dolo [--levels low,medium,high] [--members <id>,...] [--jobs 8] [--out <run folder>]
uv run --project harness --frozen python harness/runner.py run schemas/bst/experiments/restrained-limit/experiment.yaml \
    --toolkits hark,dolo --runtime docker [--cpus 2] [--memory 8g] [--wall-seconds 3600] --out <run folder>
uv run --project harness --frozen python harness/runner.py verify harness/runs/restrained-limit-1
uv run --project harness --frozen python harness/runner.py register harness/runs/restrained-limit-1
uv run --project harness --frozen --group dev pytest -q harness/test_runner.py
```

A shell started before Docker was installed on the machine reaches the daemon only through `sg docker -c '...'`.

- **What `run` does.**
  - It refuses an experiment the checker finds problems with: a wrong hash, a missing file, an undeclared member, a
    quantity the results schema does not have.
  - With `--runtime uv`, the default, it builds each toolkit's environment from its lock file and runs each job in
    it; with `--runtime docker` it builds each toolkit's image from the Dockerfile in its environment directory,
    writes the build record `<run folder>/<toolkit>/build.json`, and runs each job under the container contract of
    [`../schemas/registry.md`](../schemas/registry.md): the repository read-only at `/src`, the job's folder at
    `/out`, no network, the thread cap, a scratch `/tmp` for what the toolkit caches, and the CPU, memory and
    wall-time caps given.
  - It runs one job for each toolkit, member and level, in parallel, each through the adapter's command line with
    the toolkit's thread cap.
- **Where a job writes.** Into `<run folder>/<toolkit>/<member>/level-<n>/`, with n = 1, 2, 3 for `low`, `medium`,
  `high`. Beside the adapter's files it leaves `adapter.log`, `record.json`, its execution record for the registry
  (below), and `job.json`: the status, the command, and a fingerprint of what the output depends on:
  - the member's and the request's hashes;
  - the level;
  - the environment's lock file and interpreter;
  - the toolkit's code, including the checker modules the adapters import;
  - with `--runtime docker`, the Dockerfile and the image's identifier.
- **Resuming.** A job whose fingerprint is unchanged and whose results file exists is skipped. A rerun redoes only
  what failed or changed.
- **The run's record.** `manifest.json` names the experiment's hash, the members', each toolkit's environment and
  code, the harness's commit, the runtime, when the run started, and each job's status. Each job's `record.json` is
  its execution record in the format of the schemas beside the runner: the repository's remote, commit and dirty
  state with the working tree's tree when dirty; the environment's hash over what git records under its directory,
  with git's tree name; the image; the machine; the conditions, the thread variables, the caps and whether the
  just-in-time cache was cold; the start, end and duration; how the job ended, apart from its exit code; the
  outputs' hashes; and, under the namespace `sce-wg-1`, the experiment, toolkit, adapter, member, request, level,
  the files' hashes and the verification's verdict, which `verify` fills in. `register` copies a run's records into
  `runs.registry/<stamp>_<experiment>/`, one file per job and per build, validating each. The no-timings rule of
  2026-10-21 was revoked on 2026-11-04; a duration is read with the machine and conditions beside it.
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

Each toolkit's environment is a `uv` project in `adapters/<toolkit>/env/`, which the adapter defines and pins:
`pyproject.toml`, its `uv.lock`, which pins every dependency, `.python-version`, and a `Dockerfile` that builds the same
environment as an image for the container contract ([`../schemas/registry.md`](../schemas/registry.md)). The adapter runs in it with `uv run --frozen`, so nothing is resolved at run time.

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
