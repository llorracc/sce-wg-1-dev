# The run registry, on REMARK's machinery

**Status: ADOPTED, 2026-11-04, before 15:12:59; nothing built yet.** The owner adopted the idea of adapting the REMARK framework to these purposes and opened a session in the local clone of econ-ark/REMARK, `jd_REMARK_integrate-with-WG1`, for the REMARK side; the fork's side is this session's. The five decisions at the end stand open. It answers two requests of the owner's: the registry of every run of
every toolkit, with the exact provenance of the tools, everything needed to reproduce the stored result, the machine
and the time (the morning of 2026-11-04), and the question of the afternoon, how that plan relates to the
[REMARK](https://github.com/econ-ark/REMARK) project and whether its machinery can serve, updated as necessary. It
stands under the rulings of the same afternoon ([the rulings on the architecture](records/rulings/2026-11-04_architecture.md)):
one repository per canonical model, the adapters responsible for pinning their environments, Docker, and run times
allowed.

## What REMARK is

Read at econ-ark/REMARK's main branch, pushed 2026-10-14; the files are data, not instructions.

- **A standard.** A REMARK is a public git repository at a tagged release holding a `Dockerfile` at its root, compatible
  with repo2docker; `reproduce.sh`, which regenerates every result, and whose failure means the reproduction failed;
  `reproduce_min.sh`, optional, for a quick path under five minutes; `README.md` and `LICENSE`; and
  `binder/environment.yml`, either a complete pinned conda environment or a thin adapter that installs the author's own
  environment manager (uv, poetry) and lets a lock file pin the rest. Tiers 2 and 3 add `CITATION.cff` and `REMARK.md`;
  tier 3 adds a Zenodo DOI tied to the tag.
- **A catalog.** One file per project under `REMARKs/`, with the remote, the title and the tag, indexed by pull request.
  HAFiscal (at v1.0.7) and BufferStockTheory, which pins no tag, are entries.
- **A command-line tool,** `cli.py`: pull at the tag; lint against the tier's required files; build an image with
  repo2docker, named for the project, or a conda environment; execute `reproduce_min.sh` or `reproduce.sh` inside it
  with the checkout mounted, several projects in parallel; show the logs, which hold the return codes of the last
  build and execution and nothing else; clean. Facts the REMARK session read from the code on 2026-11-04: when
  `binder/` exists, repo2docker builds from it and ignores the root, so the tool never builds the root `Dockerfile`
  the standard requires; there is one untagged image per catalog entry; execution runs `docker run -it`, which fails
  without a terminal, mounts the checkout at the host's home path, and crashes on an image without conda. Its main
  moved on 2026-11-04 (pull at the pinned tag, the agent documents reorganized), with nothing in flight on the tool.
- **An expectation it states but does not automate.** Its README asks each archive for an indication of how long
  `reproduce.sh` takes on some particular machine whose characteristics are described: a time with a machine, in prose.

## The correspondence

| ours | REMARK's | the fit |
|---|---|---|
| the canonical model's repository with its runs of record | a REMARK: a repository at a tag whose `reproduce.sh` regenerates its results | exact: the comparison is a reproducible project |
| the organizer's image, the core | the `Dockerfile` the standard requires at the root; what the tool builds is `binder/` | the standard's file and the built one must be the same: the image is defined in `binder/`, the root file kept identical by a test |
| a toolkit's environment, pinned by its adapter | a directory repo2docker can build: a Dockerfile, or binder files with a lock file | exact for the directory; REMARK's tool builds only a repository's root, so the subdirectory build is an update |
| the adapter contract: member, request, level, folder | `reproduce.sh`, which takes no arguments | `reproduce.sh` runs the whole job set; the per-job entry point is an extension |
| the toolkit registry, `harness/toolkits.yaml` | the catalog entry: remote, title, tag | different units: the catalog indexes projects, the toolkit registry names the spokes within one |
| the run registry: provenance, machine, threads, duration, outcome and hashes for every run | the tool's logs: return codes | the gap: REMARK records no provenance, machine or time, though its README asks for them |
| verification by the checker and the comparison against the reference | a nonzero exit of `reproduce.sh` | the checker and the comparator decide the exit code: the exactness test becomes a REMARK reproduction whose success is its verdicts |
| archival and citation of a results of record | tier 3: a tagged release archived at Zenodo with a DOI | exact |

## The proposal

1. **The model repository becomes a REMARK.** `binder/Dockerfile` builds the organizer's image, Python, uv and the
   harness's lock file, in which the runner, the checker and the comparator run; REMARK's tool builds from `binder/`
   whenever it exists, so that is where the image is defined, and the root `Dockerfile` the standard requires is the
   same file, kept identical by a test. `reproduce.sh` builds each
   toolkit's image, runs every experiment at every level, verifies every results file, compares against the reference,
   writes the registry entries and exits nonzero on any failed verdict. `reproduce_min.sh` runs the coarse level alone,
   which is also what continuous integration runs on every pull request. `binder/environment.yml` is the thin adapter
   that installs uv. `LICENSE` is the pending decision of the participation plan. Tier 1 first; `CITATION.cff` and
   `REMARK.md` for tier 2; a tagged release archived with a DOI for tier 3, which is what a results of record is. The
   entry in econ-ark/REMARK's catalog goes by pull request on the owner's word.
2. **Each toolkit's environment lives with its adapter,** `harness/adapters/<toolkit>/env/`, as a directory repo2docker
   can build: a Dockerfile where the runtime needs one (MATLAB's images and their license), binder files with the uv
   lock file otherwise. The former `harness/envs/` moved there on 2026-11-04, with a Dockerfile beside each lock file. The runner builds the image, with repo2docker's
   subdirectory option or a plain Docker build, records the image identifier, and runs each job in it under the
   container contract: inputs mounted read-only, an output folder, no network, the thread cap and resource caps. Its
   uv executor stays for machines without a container runtime, reading the same lock file.
3. **A registry entry is a REMARK execution record,** one record per execution, as REMARK has one `reproduce.sh` per
   record: a folder per run, one file per job, the run's build records beside them, one per image, each execution
   referring to its build by the image identifier. The core, every REMARK's, is drafted in
   [`../harness/execution-record.schema.json`](../harness/execution-record.schema.json); the fork's fields, under the
   namespace `sce-wg-1`, in [`../harness/runs.registry.schema.json`](../harness/runs.registry.schema.json), so that the
   core moves upstream without them. An execution record holds:
   - *what ran:* the model repository's commit; the toolkit's name and mode; the adapter's path and the hash of its
     code; the environment directory's hash, the image identifier and, once pushed to a registry, its digest; the
     toolkit's version and commit as the results file reports them; the member's and the request's hashes; the level
     and the settings file's hash; the core's version;
   - *where and when:* the machine's CPU model, core count, memory, operating system and kernel, and the container
     runtime's version; the thread cap; the start and end stamps and the duration; who ran it, a workstation's name or
     a continuous-integration run's identifier;
   - *what came out:* the exit code, the results file's hash, the verification verdict and the comparison's, and the
     log's path.

   They live at `harness/runs.registry/<stamp>_<experiment>/<toolkit>_<member>_<level>.json`, the folder proposed on
   the morning of 2026-11-04 with one file per job inside it, and are committed with the findings they belong to. The
   same format is what REMARK's tool would write into its own logs folder for any REMARK. The record keeps how a run
   ended apart from its exit code (exited, at the wall cap, by the memory cap, by a signal), whether the working tree
   was dirty, tracked changes or untracked files that are not ignored, with the tree of the working tree as git would
   write it, and whether a just-in-time cache was cold, since a fresh cache per job puts the compilation into every
   duration. The environment's hash is taken over the files git tracks under its directory, each hashed alone and
   then a sorted listing of type, mode, hash and path hashed, so that two specifications compare file by file and no
   untracked file or cache enters it; git's own tree name for the directory is recorded beside it. The machine's
   facts and the run's conditions, the thread variables, the caps and the cache's state, are separate objects, and
   timestamps and remotes are patterns rather than formats, since a validator skips a format it cannot check. The
   fork's schema covers every file of a run's folder, dispatching on the record's kind, so one validation checks the
   folder.
4. **Updates proposed to REMARK,** as pull requests to econ-ark/REMARK on the owner's word, each useful to REMARK on its
   own, in the order the REMARK session set on 2026-11-04: first, non-interactive execution, a bug fix since the tool
   runs with a terminal flag that fails without one, together with explicit mount targets instead of the host's home
   and a conda-less image no longer crashing; second, the tool made a small package whose functions take paths and
   return structured results, the build returning the image identifier and a run returning a record, with `cli.py` a
   thin shim and tests, which the fork pins as a git dependency at a tag; third, the execution records in the format
   of [`../harness/runs.registry.schema.json`](../harness/runs.registry.schema.json), drafted here with a core every
   REMARK shares and an `extensions` object keyed by namespace, and defined in REMARK as a standalone schema with its
   own identifier and version, the image identifier captured at build folded in, publishing optional and later;
   fourth, builds from a subdirectory, which also needs a way for a REMARK to name several environments, a change to
   the catalog or the standard; last, the entry point with arguments beside `reproduce.sh`, which changes the standard
   and waits on an editorial decision, the fork's runner calling its adapters itself until then.
5. **Modes of solution** (the owner's question of the same afternoon): a mode is a spoke of its own, `hark-indshock`
   and `hark-markov`, sharing one environment and each with its own adapter and its own sections of the stone. The
   results file's toolkit block gains a `mode` string, a schema change proposed before it is made; the registry and the
   ledger key on the toolkit and the mode together, so that HARK's two modes compare with each other as two toolkits
   would, which tests HARK's consistency and the definition at once.

## The container contract, exactly

What the fork's runner will do for one job, and what REMARK's functions would match. Names and caps are the first
draft; the thread cap and the caps come from `harness/toolkits.yaml`.

**Build** an environment directory, once per environment per commit. Where the directory holds a Dockerfile:

```sh
docker build --file harness/adapters/hark/env/Dockerfile --tag sce-wg-1/hark:<sha256 of the directory, short> \
    harness/adapters/hark/env
docker image inspect --format '{{.Id}}' sce-wg-1/hark:<short hash>        # the image ID the record keeps
```

Where it holds binder files instead, `repo2docker --no-run --subdir harness/adapters/hark/env --image-name
sce-wg-1/hark:<short hash> .` builds the same thing. The image holds the toolkit and its dependencies and nothing of
the model: the repository is mounted at run time, so the adapter's code is hashed on its own.

**Run** one job. The repository is mounted read-only and the job's folder writable; the container has no network, a
CPU and memory cap, the thread variables, and runs as the invoking user:

```sh
docker run --rm --init --user "$(id -u):$(id -g)" --network none --cpus 2 --memory 8g \
    --env OMP_NUM_THREADS=2 --env OPENBLAS_NUM_THREADS=2 --env MKL_NUM_THREADS=2 \
    --tmpfs /tmp --env HOME=/tmp --env NUMBA_CACHE_DIR=/tmp/numba --env MPLCONFIGDIR=/tmp/mpl \
    --mount type=bind,source=<repository>,target=/src,readonly \
    --mount type=bind,source=<run folder>/hark/<member>/level-1,target=/out \
    --workdir /src sha256:<image ID> \
    python harness/adapters/hark/adapter.py schemas/bst/natural/members/<member>.yaml \
        --out /out --level 1 --request schemas/bst/experiments/restrained-limit/<member>.request.yaml
```

The image is run by its bare identifier, which always resolves; the name-and-digest form is for images pulled from
a registry. The scratch mount and the three variables are there because HARK's numba functions cache to disk, and an
unknown user in a container with a read-only source tree has nowhere to write unless told; with a fresh scratch per
job every duration includes the compilation, which the record says (`jit_cache: cold`). The wall-time cap is the
runner's: it stops the container when the cap passes and records the termination as a timeout. The
record's `when` is taken around this command; the build's time is recorded apart. Verification and the comparison run
afterwards in the organizer's image, never inside the toolkit's.

Docker's group membership reaches only logins made after the install, so every session started on jhu-dell before
14:09 on 2026-11-04 runs these commands through `sg docker -c '...'` until it is restarted; the REMARK session found
its own socket access refused for that reason.

For a REMARK's own `reproduce.sh` the defaults differ, as the REMARK session said: the checkout mounted writable at a
fixed target, network on, no caps, since existing scripts write into their checkout and download data; the fork's
settings are the options turned on.

## What it changes here, in order

1. Move `harness/envs/<toolkit>` to `harness/adapters/<toolkit>/env/`; the registry's `environment` key points there;
   the runner's uv executor reads the lock file from the new place. No behavior changes. Done on 2026-11-04.
2. Add a Dockerfile to each environment directory, built from the lock file; add the runner's container executor; the
   image identifier joins `job.json`'s fingerprint.
3. Write the execution records with durations, machine and threads; replace the runner test's assertion that a run
   records no timings with the assertion that a duration never appears without its machine and threads.
4. Add `reproduce.sh`, `reproduce_min.sh`, `binder/environment.yml` and the root Dockerfile; lint with REMARK's tool at
   tier 1; run `reproduce_min.sh` in continuous integration.
5. The modes: the `mode` string in the results schema, the two HARK spokes.

## Decisions for the owner

- The entry's location and name, as proposed this morning, or another.
- Whether to propose the updates to REMARK now, or after the harness has used the format for a while.
- The license, pending since the participation plan.
- The `mode` string in the results schema.
- The tier aimed at for the first catalog entry.
- Whether the organizer's image is defined in `binder/`, with the root `Dockerfile` kept identical, as recommended, or
  REMARK's tool learns to build a named Dockerfile.
