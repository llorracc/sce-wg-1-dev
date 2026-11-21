# Plan: the bench outside the adapter, with settings as suggestions

**Status: ACTIVE.** Adopted 2026-11-20 at 18:19:48 and agreed in substance at 18:36:08 ([the rulings](../rulings/2026-11-20_the-bench-outside-the-adapter.md)).
The core's packages are done: the fork's #31 and #32, merged at 19:40. The first is open in the working group's
repository as #24. The model repositories' packages are under way in their own sessions.

This is the core's part, written for publication. The full plans, with what they say of the two model repositories'
code, are kept on the machine of the fork's session; those repositories are not public.

## The principle

An adapter translates the member into the toolkit's terms, calls the toolkit, and translates the answer back. It
supplies none of the toolkit's numerical choices. The harness gives parameters and suggests settings it never
imposes: a toolkit takes, adapts or declines each suggestion, or as an exact entry answers that none applies, and says
which. Only the outcome is judged. Where an adapter reads the toolkit's internals rather than what the toolkit returns,
the solution file declares it and the stone says why. The organizer's measuring code, the bench, runs once for every
toolkit, outside the toolkit's environment.

## The design, as built in the core

- **The adapter's command.** A registry entry may state the words that start its adapter, `{adapter}` once among
  them, so that an adapter may be in any language (#31).
- **The contract's second form** (#32):
  - **The solve.** An entry stating `contract: 2` has its adapter given the level's suggestions as a file in place of
    the level. It writes the toolkit's solution, method and settings files, the solution checked against the model's
    solution schema.
  - **The measure.** The model's bench then runs on the host, in the harness's environment, outside any container. It
    reads those files and its settings at the level and writes the results file.
  - **Records and reruns.** Each step has its own record and fingerprint, so a change to the bench measures again
    without solving again.
- **The experiment.** It names its levels, `out-of-box` among the names it may use. It gives each level optional
  suggestions in the model's own terms, checked against the model's suggestions schema, and states the bench's
  settings as it states its metrics.
- **The records.** Draft 9 of the registry schema carries the step, the contract, the suggestions' and solution's
  hashes, and a measure step's inputs and bench. All of it is in the project's namespace, so the execution-record
  schema REMARK carries is unchanged; draft 8 is held among the earlier drafts.

What a solution file holds is each model's to state, in its own schema: the toolkit's rules as the toolkit holds them,
in a form the bench can read exactly; the representation of the laws it solved on; what the toolkit computes itself;
the solve's provenance; and the toolkit's own evaluations at check points the adapter chooses, by which the bench
checks its reading.

## The packages

| package | owner | status |
|---|---|---|
| the adapter's command | the fork's session | merged, the fork's #31 (1b74c66); open in the working group's repository as #24 |
| solve and measure | the fork's session | merged, the fork's #32 (f56d46e); to the working group's repository after #24 |
| the core's text | the fork's session | merged with #32 |
| the perfect-foresight cut | that repository's session | built and accepted, 19:06 on 2026-11-20; its commit approved at 19:42:12 |
| the buffer-stock cut | that repository's session | under way |
| the pilot: perfect foresight on the contract's second form | that repository's session | approved at 19:42:12, after its repin to the merged core |
| the buffer-stock move: all three toolkits on the second form, in containers, one run | that repository's session | after its cut and the pilot |
| each toolkit's own representation of the laws, with the experiment's next version | that repository's session, with HARK-dev's | after the move and HARK's adapter moving to the standard consumer |

**Acceptance:**
- **The cuts:** every number of the run of record the same, read through the export, since the bench still runs on
  the toolkit's own numerical library.
- **The pilot and the move:** every number the same to a stated relative tolerance of about 1e-15, with the read-back
  check as the guard, since out of process the bench's library is the harness's.
- **The last package:** no reproduction. Every entry verifies; every outcome is shown beside the settings the toolkit
  used; every difference between toolkits at the finest level is within their convergence or traced to a stated
  convention, which is then a finding.

## What it settles

- the comparator survey's *bench outside the adapter* and *the adapter as a command*;
- in its last package, *the shared nodes against the rulings of 2026-11-02*;
- the buffer-stock repository's plan for other models, its "bench as a step";
- the first of the six decisions of 2026-11-03 on comparing solutions, the split between toolkit and bench.
