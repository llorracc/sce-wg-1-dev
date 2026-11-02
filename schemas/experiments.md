# Experiments: what every toolkit is asked to do

Drafted on 2026-11-02 on the owner's request of that day, and approved with the harness plan the same morning; see the
[README](README.md). **Status: APPROVED, not yet read by a harness.** The harness that reads it is planned in
[`harness.md`](harness.md).

A family's schemas say what a model is. An **experiment** says what every toolkit is to do with some of a family's
members, and what the results must show. An experiment file names:
- the members, with the request file each is solved with;
- the precision levels every toolkit runs;
- what every results file must carry;
- the checks the harness makes on the results files.

It names no toolkit and holds none of a toolkit's settings. Those stay in the toolkit's method and settings files
([`numerics.md`](numerics.md)), and its Rosetta Stone says how it maps onto the family. An experiment is to the
toolkits what CMIP's experiment protocols and data request are to climate models: one statement of what everyone runs
and reports, so that the results can be laid side by side.

- [`experiment.schema.json`](experiment.schema.json) is its validator.
- [`bst/experiments/restrained-limit/experiment.yaml`](bst/experiments/restrained-limit/experiment.yaml) is the first experiment.
- [`checker/test_experiment.py`](checker/test_experiment.py) tests both.

## What an experiment file holds

| key | what it holds |
|---|---|
| `experiment` | the name and version, as a family's: `restrained-limit/1`. A change to what it asks makes a new version |
| `title`, `statement` | what it shows, in words |
| `sources` | where it comes from, by anchor; BST's must be among the published page's (`bst-anchors.txt` in the ontology) |
| `members` | for each member: its `id` (the parameter file's name), the parameter file and the request file, each with its hash as the checker takes it. Pinning the hashes means an edited member makes the experiment fail its test, not silently change |
| `levels` | the named precision levels every toolkit runs: `low`, `medium` and `high`, as [`numerics.md`](numerics.md) names a ladder's elements. A toolkit may run more |
| `reports` | the results-file quantities every run must carry beyond what the results schema requires of every file, as paths into it: `types[].rule.c`, `types[].kink` |
| `checks` | what the results must show (below) |
| `report_scripts` | optional scripts of the experiment's own that write tables and figures from the results files alone, solving nothing |

The file is strict YAML, like a parameter file, so it has a hash, and its keys and values follow the schemas' own spelling,
with underscores. A quantity's path must resolve in [`bst/results.schema.json`](bst/results.schema.json); the test checks
it.

## The checks

Each check compares results files and says what the comparison must show. It has an `id`, a `statement` in words, and:
- **`compare`,** what is set side by side:
  - `members`: one toolkit's files at one level, between the named `pairs` of members;
  - `toolkits`: two toolkits' files for one member at one level, for every pair of toolkits run;
  - `levels`: one toolkit's files for one member, at successive levels.
- **`quantity`,** a path into the results file. Every number it holds is compared: a rule's values at the request's
  points, or the whole `effective_member` block.
- **`metric`,** `max_abs_difference`, or `max_relative_difference` (divided by the larger of one and the first value's
  magnitude).
- **`expect`:**
  - `decreasing`: each pair's metric smaller than the pair before it, at every level (for `members`);
  - `falls_with_level`: the metric smaller at each finer level (for `toolkits` and `levels`);
  - `{at_most: x}`: the metric no larger than x, at every level.

**Why a comparison of toolkits is not a fixed tolerance.** `numerics.md` asks that a comparison of two toolkits take its
tolerance from measured convergence. The levels cannot supply it on their own. A level changes model-changing and
method-only settings together: from `low` to `high` the nodes per shock go from 7 to 31 as well as the grid getting
finer. On the restrained-limit experiment, for m up to 20, each toolkit's own rule moves by 3.3 · 10⁻³ between `medium`
and `high`, mostly from the nodes, which dolo's probe found move both toolkits' rules alike
([the probe](records/findings/2026-11-01_dolo-probe/README.md)). The two toolkits differ by 1.2 · 10⁻⁵, because they
share the nodes. A tolerance taken from the levels would pass almost anything. So the first experiment checks two things instead:
- **The same effective member.** The two toolkits' `effective_member` blocks, the expectations of the member they
  actually solved, agree to 10⁻¹².
- **A difference that shrinks.** The difference between their rules falls at each finer level, as the solution error
  of each does on that one effective member.

A tolerance from a ladder of method-only settings at fixed nodes would be the sharper test; the owner deferred it.

## The first experiment: restrained-limit

[`bst/experiments/restrained-limit/experiment.yaml`](bst/experiments/restrained-limit/experiment.yaml) states BST's "The
Liquidity Constrained Solution as a Limit" as [`bst/model.md`](bst/model.md) describes it. It has the suite's four
members and request files and the levels `low`, `medium` and `high`. It asks for:
- the rule and its MPCs;
- the kink;
- the mean MPC and the mass at the constraint.

It makes three checks:
- `rungs_approach_the_limit`: each natural rule is closer to the restrained one than the rung before, at every level;
- `same_effective_member`: the toolkits solve the same effective member;
- `toolkits_agree`: their rules' difference falls with the level.

**Evaluated on the committed results** of HARK's and dolo's runs of 2026-11-01, by a prototype of the harness's
comparator, all three pass:

| check | HARK | dolo | HARK against dolo |
|---|---|---|---|
| `rungs_approach_the_limit`, `high` | 0.137, 0.061, 0.0267 | 0.137, 0.061, 0.0267 | |
| `same_effective_member`, largest at any level | | | 3.3 · 10⁻¹⁶ |
| `toolkits_agree`, `bst-restrained` | | | 4.4 · 10⁻⁴, 1.4 · 10⁻⁴, 3.7 · 10⁻⁵ |

## The toy-hafiscal experiment, sketched

Not written, since its member is not delivered: HARK's and HAFiscal's tools estimate its three types
([`bst/model.md`](bst/model.md)). Written to this schema it would have:
- one member, `toy-hafiscal`, with its request file, which states the Jacobians' horizon, inputs, outputs and shared
  grid ([`jacobians.md`](jacobians.md));
- one level, `high`, since the Jacobians ask for a steady state to 10⁻¹⁰;
- reports: the types' rules and populations, the pooled population, and `jacobians`.

**One gap in the results schema.** The targets' Lorenz shares of wealth are GL(p)/GL(1) of the pooled population, and
K/Y comes from the pooled means, so both are already in a results file. The iMPC profile after a lottery prize is not.
Adding it is a change to what results carry, to be drawn up with the toolkits and put to the owner before it is made.

## Names

The owner's "test suites" of 2026-11-01 are experiments in this document's sense. `numerics.md` used "suite" for
something else, one method file run under many settings elements, which is now a **ladder**, the word the records already
used for it (the owner's ruling of 2026-11-02). The records and the findings' folder names keep the old word, as they
were written; the folder `bst/suites/` became `bst/experiments/` with the layout's move of 2026-11-02 ([`harness.md`](harness.md)).

## What the tests establish

`checker/test_experiment.py`, 17 tests, checks that:
- the validator is a valid JSON Schema;
- the experiment file is strict YAML and validates;
- the members' and request files exist and hash as the file says, and each request file is for its member;
- the checks name declared members, and every quantity resolves in the results schema;
- the report scripts exist, and BST's anchor is one of the published page's;
- the restrained-limit members ask for the same points, as its member-against-member check needs;
- thirteen breaks are each caught, from a wrong hash to a toolkit's setting written into the file.

They solve nothing and say nothing about whether a toolkit passes. That is the harness's job, which the prototype above
only previews.

## Open points

- A **ladder of method-only settings** at fixed nodes, to give a comparison of toolkits a measured tolerance:
  deferred by the owner on 2026-11-02.
- **A region** for a check, such as m ≤ 20, where the rule is far from the grid's top. Not needed by the first
  experiment, which passes over all its points.
- **Checks on the levels' own convergence,** `compare: levels`, which the first experiment does not use.
- The **iMPC** in the results schema, for toy-hafiscal.
