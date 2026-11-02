# The first experiment's checks, on the committed runs

2026-11-02, with the experiment schema drafted that morning on the owner's request (`../../../experiments.md`).

## What was run

`eval_checks.py`, a prototype of the harness's comparator (`../../../harness.md`), evaluated the three checks of
`bst/suites/restrained-limit/experiment.yaml` on the results files committed on 2026-11-01. It used HARK's run and
dolo's, at the levels `low`, `medium` and `high` (the adapters' levels 1 to 3). It reads the results files and solves
nothing:

```sh
cd schemas && uv run --with pyyaml python records/findings/2026-11-02_experiment-checks/eval_checks.py \
    bst/suites/restrained-limit/experiment.yaml \
    HARK records/findings/2026-11-01_restrained-limit-suite-hark/results \
    dolo records/findings/2026-11-01_restrained-limit-suite-dolo/results
```

Its output is `verdicts.txt`.

## The numbers

| check | what it compares | result |
|---|---|---|
| `rungs_approach_the_limit` | each natural rule against the restrained one, within a toolkit and level | passes for both toolkits at every level: at `high`, 0.137, 0.061 and 0.0267 in both |
| `same_effective_member` | the two toolkits' `effective_member` blocks, member by member and level by level | passes: the largest relative difference is 3.3 · 10⁻¹⁶ |
| `toolkits_agree` | the two toolkits' rules at the common points, level by level | passes: for each member the difference falls, from about 4.4 · 10⁻⁴ to 1.4 · 10⁻⁴ to 3.8 · 10⁻⁵ |

**A measurement that shaped the checks.** For m up to 20, each toolkit's own rule moves by 3.3 · 10⁻³ between `medium`
and `high`, against a difference between the two toolkits at `high` of 1.1 to 2.4 · 10⁻⁵. A level changes the nodes per
shock as well as the grid, and the nodes move both toolkits' rules alike (`../2026-11-01_dolo-probe/README.md`). So a
tolerance for comparing toolkits cannot be taken from the levels: it would pass almost anything. The checks require the
same effective member and a difference that falls with the level instead.

## What it establishes, and what it does not

- **The experiment's checks can be evaluated from results files alone,** and both toolkits pass them.
- **The prototype is not the harness.** It reads two runs laid out by hand. It has no verification step, no report of
  missing quantities, and no `compare: levels` check, which the first experiment does not use.
- **The sharper test,** a tolerance from a ladder of method-only settings at fixed nodes, was deferred by the owner.
