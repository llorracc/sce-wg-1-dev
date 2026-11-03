# Experiments: what every toolkit is asked to do

Drafted on 2026-11-02 on the owner's request of that day, and approved with the harness plan the same morning; see the
[README](README.md). **Status: APPROVED; revised on 2026-11-02 and 2026-11-03** by the owner's rulings on what the
harness gives a toolkit and asks of it; the revision is a proposal until the owner has read it. The harness's runner
reads the file ([`harness.md`](harness.md)); its comparator is next.

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

## What the harness gives a toolkit, and what it asks of it

The owner's rulings of 2026-11-02 (18:28 and 19:09) and of 2026-11-03 (04:37):
- **It gives parameters, never methods or settings.** An adapter receives the member's parameter file, the request
  file, the name of a precision level, and a folder to write into; nothing else. What a level means is the
  toolkit's own ladder's business ([`numerics.md`](numerics.md)); the harness only maps the names.
- **The true model has truncated lognormal laws, and each toolkit represents them as it likes:** by discretizing, by a
  continuous representation, or otherwise. No experiment and no code the adapters share prescribes nodes, grids or a
  population method. What a toolkit chose is read from its method file, its stone and its reported effective member.
- **It asks every toolkit for,** through the results schema ([`bst/results.md`](bst/results.md)): the rule and its
  special points, the buffer-stock target among them; the stationary distributions of m, a and c under both measures,
  which carry the population's means of m, a and c, and marginal welfare, E[u′(c)]; the stationary distribution of
  permanent income, for its Lorenz curve, which is all that is asked of it; and, where an experiment asks for it, the
  joint distribution of (m, 𝐩, c, a) the economy generates.

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
  - `levels`: one toolkit's files for one member, at successive levels;
  - `stated`: one toolkit's files for one member at successive levels, against the checker's report of the stated
    member: the quantity's distance from its closed form, such as the effective member's expectations from the laws'.
- **`quantity`,** a path into the results file. Every number it holds is compared: a rule's values at the request's
  points, or the whole `effective_member` block.
- **`metric`,** `max_abs_difference`, or `max_relative_difference` (divided by the larger of one and the first value's
  magnitude).
- **`expect`:**
  - `decreasing`: each pair's metric smaller than the pair before it, at every level (for `members`);
  - `falls_with_level`: the metric smaller at each finer level (for `toolkits` and `levels`);
  - `{at_most: x}`: the metric no larger than x, at every level;
  - `within_own_convergence`: at the finest level, the metric no larger than the sum of the two toolkits' own movements
    of the same quantity between their two finest levels (for `toolkits`).

**How two toolkits are compared.** `numerics.md` asks that a comparison of two toolkits take its tolerance from
measured convergence. Since each toolkit represents the laws its own way (the ruling of 2026-11-02), the two solve
different effective members, each an approximation of the stated one, and their rules differ by about their
representation errors; so the first experiment asks three things:
- **Each approaches the stated member.** The distance between a toolkit's effective member, the expectations it
  reports, and the checker's closed forms for the stated laws falls at each finer level (`compare: stated`).
- **Each converges, and the two agree within their own convergence.** At the finest level the two rules differ by no
  more than the sum of each toolkit's own movement between its two finest levels (`within_own_convergence`): a toolkit
  converged to 10⁻⁵ and one to 10⁻³ must agree to about 10⁻³, and a toolkit that converges to the wrong rule is
  caught by the next check.
- **Each solves the stated model.** The Euler residuals under the stated laws, which the results schema requires,
  fall with the level. That trusts no toolkit's representation.

The first version of this experiment, run on 2026-11-01, compared two adapters that shared their nodes and grids
through common code; they differed by 1.2 · 10⁻⁵ where each moved by 3.3 · 10⁻³ between levels
([the probe](records/findings/2026-11-01_dolo-probe/README.md)), and its check `same_effective_member` required the
two effective members to agree to 10⁻¹². That shared code is a departure from the ruling and is being undone
([`harness.md`](harness.md)); the check goes with it. A tolerance from a ladder of method-only settings at fixed nodes
would be a sharper test of a single toolkit; the owner deferred it.

## The first experiment: restrained-limit

[`bst/experiments/restrained-limit/experiment.yaml`](bst/experiments/restrained-limit/experiment.yaml) states BST's "The
Liquidity Constrained Solution as a Limit" as [`bst/model.md`](bst/model.md) describes it. Its second version, to be
written from this revision, has the first version's four members and request files, BST's calibration with ℒ = 1, and
the levels `low`, `medium` and `high`, each toolkit's own. It asks for:
- the rule and its MPCs, the kink and the target;
- the stationary populations: the mean MPC and the mass at the constraint.

It asks for no distribution of permanent income and no joint: its members have no mortality, so the first is
`undefined` for them, and the second would add nothing to the populations' ordinates.

It makes three checks:
- `rungs_approach_the_limit`: each natural rule is closer to the restrained one than the rung before, at every level;
- `approaches_stated_member`: each toolkit's effective member approaches the stated one with the level;
- `toolkits_agree`: the rules agree within the toolkits' own convergence.

**Its first version**, with the check `same_effective_member`, was **evaluated on the committed results** of
HARK's and dolo's runs of 2026-11-01, by a prototype of the harness's comparator, and all three of its checks passed:

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
- reports: the types' rules and populations, the pooled population, the distributions of permanent income and of
  wealth in levels, the joint, and `jacobians`.

The toy, HAFiscal's calibration with ℒ = 0.99375 and 𝒢 = 1.0019 a quarter, has a stationary distribution of permanent
income with a finite mean, ℒ𝒢 = 0.9956 < 1, so its Lorenz curve of permanent income is defined, the same for every
type.

**One gap in the results schema.** The targets' Lorenz shares of liquid wealth are shares of end-of-period assets in
levels, a𝐩, across households ranked by them, at p = 0.2, 0.4, 0.6 and 0.8: the owner's ruling of 2026-11-03, which
HAFiscal's code confirmed ([the finding](records/findings/2026-11-03_hafiscal-lorenz-in-levels.md)). GL(p)/GL(1) of a
under the population measure is the Lorenz curve of normalized wealth, a different curve whenever permanent income
varies across households. So the results schema now carries the distribution of wealth in levels beside the
distribution of permanent income, and the targets are read off it; K/Y is its mean over the economy's mean income. The
iMPC profile after a lottery prize is not in a results file.
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
