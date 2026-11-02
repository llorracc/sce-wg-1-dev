# The harness's runner, accepted on the restrained-limit experiment

2026-11-02, on the owner's go-ahead of 11:23:59 for the runner, the second stage of the harness plan
(`../../../harness.md`). The plan's test of acceptance: at `low`, each real toolkit's files are those its adapter
wrote on 2026-11-01.

## What was run

The runner (`harness/runner.py`) ran HARK and dolo on the experiment's four members at `low`, eight jobs, each in its
toolkit's environment locked in `harness/envs/<toolkit>/uv.lock`. It then verified every results file:

```sh
uv run --project harness --frozen python harness/runner.py run schemas/bst/experiments/restrained-limit/experiment.yaml \
    --toolkits hark,dolo --levels low --jobs 8
uv run --project harness --frozen python harness/runner.py verify harness/runs/restrained-limit-1
```

The run folder is ignored by git; its `manifest.json` and `verification.json` are kept here. The environments pin the
interpreter and the numpy, scipy and numba that the runs of 2026-11-01 recorded (`harness/README.md`).

## What happened

- **The first run, started at 11:27:54:**
  - HARK's four jobs succeeded;
  - dolo's first succeeded and its other three failed with `LLVM ERROR: Symbol not found: __gufunc__...dolo.algos.invert...`.

  dolo's numba functions cache their compiled code inside the environment. The environment had just been built, so the
  cache was empty, and four jobs started together raced to write it. The hand run of 2026-11-01 had used an
  environment whose cache was already filled.
- **The fix:** the runner now runs each toolkit's first job alone, then the rest in parallel, so that one process
  writes the cache.
- **The second run, started at 11:29:08:**
  - dolo's built environment, with its cache, and dolo's run folder were deleted first, so the fix was tested from
    cold;
  - HARK's four jobs were skipped, their fingerprints unchanged: the runner's resumption, with real toolkits;
  - dolo's four succeeded;
  - all eight results files verified.

## The numbers

Each of the eight jobs against the committed file for its toolkit, member and level 1, in
`../2026-11-01_restrained-limit-suite-hark/results/` and `../2026-11-01_restrained-limit-suite-dolo/results/`:

| | method file | settings file | results file |
|---|---|---|---|
| HARK, four members | identical | identical | identical but for one line |
| dolo, four members | identical | identical | identical but for one line |

The one line is `toolkit.driver`, the adapter's own path. It reads `harness/adapters/<toolkit>/adapter.py` since the
layout's move (commit `9675109`) and `schemas/adapters/...` in the committed files.

## What it establishes, and what it does not

- **The runner reproduces the hand runs.** From the lock files alone it builds environments in which both adapters
  write the same numbers as on 2026-11-01, so the lock files capture what the runs depended on, on this machine.
- **Resumption, failure and verification work** with the real toolkits as well as in the runner's tests on a stand-in.
- **Not shown:**
  - the levels `medium` and `high`;
  - another machine: the interpreter, the BLAS and the CPU may change the last digits elsewhere;
  - the comparator, which is the next stage.
