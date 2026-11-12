# The core's two changes, tried on real runs

What was measured on 2026-11-11 and 2026-11-12 to show that two changes to the core leave an earlier experiment's
comparison as it was: the reference as its own kind of object (the fork's pull request #16, merged) and the metrics
an experiment defines (the branch `experiment-metrics`, unmerged). The runs are the two model repositories', which
are private; no number of theirs is repeated here.

## How

For each run folder: the folder is copied twice into a scratch directory, and the model repository is cloned into
the scratch directory at the commit the run's manifest names, so that the experiment's hash is the run's. Then, from
the clone,

    <old core's python> -m wg1core.runner compare <copy one>
    <new core's python> -m wg1core.runner compare <copy two>

and the two copies are compared: `comparison.json` after the new core's new keys are set aside (the entries' kinds,
the part on the references, each job's kind, each distance's `at`, the defined metrics), and every job's
`record.json` byte for byte. Nothing is solved again: a comparison reads the results files a run left.

## What was tried

| change | old core | new core | runs |
|---|---|---|---|
| the reference as its own kind | the fork's main before it | the branch at its first commit and again at its second | the buffer-stock repository's run of all three toolkits at all levels, 36 jobs; the perfect-foresight repository's first run, 6 jobs |
| the metrics an experiment defines | the fork's main with #16 | the branch | the same buffer-stock run; the perfect-foresight repository's three runs, 6 jobs each |

## What it found

- In every case the checks' verdicts and values, every distance from the reference, and every record are the same
  under the old core and the new. The reports differ only by what the change adds: for the first change the new
  part and columns, for the second one reworded closing sentence.
- The core's own tests pass at each commit: 34 after the first change, the 20 earlier ones unchanged; 42 after the
  second, with one assertion on a draft's number loosened.
- An independent reader, given the first change's diff and its specification and not this session's reasoning,
  compared 2,500 random runs of the earlier form under both cores, checked every verdict of the new check on 2,278
  random runs of the new form against its own statement of the specification, and validated all 2,304 combinations
  of a check's keys; it found no defect in the main paths, and edge cases that the branch's second commit fixes.
- The perfect-foresight repository's session, as it reports, ran its first experiment's version under the first
  change with every results, methods and settings file byte for byte that of its run of record, and its second
  version with all five checks passing.

## What it establishes, and what it does not

It establishes that an experiment and a registry file of the earlier form compare the same under the changed core,
on the runs both model repositories hold. It does not establish:
- that a run made afresh writes the same records: it does not, since a record names the schema's draft and now
  carries the entry's kind;
- anything about the runner's container path or the verifier, which a comparison does not exercise;
- that the second change was read by anyone but its author: no independent review was run on it.

## Pending

- The second change's push and merge, on the owner's word.
- A largest distance still passes over a value that is not a number outside a check against the reference
  ([the defects](../defects.md)).
