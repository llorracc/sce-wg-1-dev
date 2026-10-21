---
name: project_state
description: "What the schema project holds, what is settled and what is open, as of the memorial of 2026-10-21"
metadata:
  type: project
---

**On the schemas' branch** (`buffer-stock-schema-work_CDC`, pushed with the memorial of 2026-10-21). All of it is draft, and none has been
proposed to the working group yet.
- **Shared:**
  - `shock-laws.md` with its validator;
  - `numerics.md` (method, settings and suite files, with the stage file's targets as a method file's addresses);
  - `foundation.md` (the stage file as the foundation of a family's statement);
  - the design note `hafiscal-models-and-test-suite.md`;
  - the plan `existing-syntax.md`, executed for the distribution class.
- **`bst/1`:**
  - `model.md`, read from the stage file in BST's notation;
  - `conditions.md`;
  - `results.md` and `results.schema.json`, with the effective member and the optional population block;
  - `parameters.schema.json`;
  - the members `library`, `toy` and `toy-untruncated`;
  - `bellman/buffer_stock.bl`, with the community library's calibration.
- **`bst-markov_ui-and-agg/1`:** its stage file, and its model and conditions documents. Its results, validator and members
  are not written.
- **`checker/`:** 73 tests. It holds:
  - the strict loader and the hash;
  - the laws' closed forms in log space;
  - the member checker, with the four lower-tail cases;
  - the converter to Bellman's calibration;
  - the results validator's tests;
  - the verification of a results file's report on the effective member.

**Draft pull requests in the fork** (llorracc/sce-wg-1-dev), none merged:

| # | branch | head | into | what it holds |
|---|---|---|---|---|
| 1 | `probability-distributions-ontology` | `44d10cc` | `main` | the ontology of probability distributions, `ontologies/probability-distributions/`, version 0.1.0-draft.1, rows `PD_0000001` to `PD_0000063`; 12 tests |
| 2 | `shock-laws-on-the-ontology` | `0583a60` | the schemas' branch | the shock laws written on the ontology: an omitted bound three standard deviations and `null` none; the hash over the filled form; `LogNormalMixture` and `TruncatedLogNormalMixture` in place of `NormalMixture`; each law's row; the converter to Bellman-SYM calls; the cross-test on a vendored copy of the ontology's table; `conventions.md` with its standing check; 123 tests, the members' hashes unchanged |
| 3 | `drop-the-quantile-at-one` | `141d17e` | the schemas' branch | the quantile maps without Q(1), at the fourteen probabilities 0.01 to 0.999, the Lorenz maps keeping 1; 76 tests |
| 4 | `coverage-of-the-representation` | `029a73f` | the schemas' branch | an optional `coverage` element in the population and income-measure blocks, with the toolkits' final wording; 82 tests |

**Merge order.**
- #1 merges into `main` first. The schemas' branch then takes `main`, and #2 merges after that.
- #3 and #4 merge in either order: a trial merge of the two is clean, and neither shares a file with #2.
- Every merge, and taking a draft out of draft, is the owner's word.
- The main checkout no longer needs to stay at `4f99d01`, since the emitter's rerun reads its own copy of the schemas.

**Settled** (see the rulings):
- **Notation and the model:**
  - BST's notation;
  - ρ > 1;
  - a newborn born employed at P = 1 with no assets;
  - the bounds a̲_Art and a̲_Nat, with a̲ the larger of the two;
  - welfare in utils, with W, F and M reported and no consumption-equivalent.
- **The written form:**
  - one written form, with the hash over the parsed numbers, and since 2026-10-20 over the filled form;
  - the restructuring on the stage file;
  - the precision levels as settings, with measured convergence the only source of tolerances;
  - the switch's three values, with `continues` the standard;
  - ξ_U and ξ_X for the replacement incomes, and named groups;
  - the borrowing limit in the household's units;
  - the benchmark's toy following bst/1's newborn.
- **The truncated lognormal** as the usual law, with the stated standard deviation kept after truncation. An omitted
  bound is three standard deviations (2026-10-19), and `null` is none (2026-10-20).
- **The Markov family** (ruled at 19:17 on 2026-10-18):
  - the newborn follows bst/1's convention;
  - the normal regime is absorbing, with no hazard key;
  - "agg" in the family's name means the aggregate regime alone.
- **The effective member** (`effective-member.md`, 2026-10-18):
  - A toolkit solves its own effective member and reports the expectations, every condition's factor and verdict, the
    lowest values of its representation and the derived parameters it used.
  - The checker verifies what needs no representation, and marks a verdict `undecided` within the closed forms'
    precision.
  - Since 2026-10-19, a population pushed forward under another representation is reported in an optional block that
    decides the population's conditions.
- **Fixed on 2026-10-19:**
  - levels written bold;
  - the Markov family's constraint in force as the per-state fixed point with the artificial limit inside;
  - both stage files' limits declared on (−∞, 0];
  - the community-library and law-family sentences.
- **The ontology** (2026-10-20):
  - **Design:** the six kinds, three operators and the identity rule, with Matsya's three settlements; ProbOnto
    cross-referenced by SKOS's mapping properties; one YAML source generating OWL 2 and a JSON table; CC BY 4.0;
    versioned releases.
  - **Home and tolerance:** `ontologies/probability-distributions/` in this repository; a tolerance of 10⁻¹² for
    irrational conversions.
  - **Bellman's side:** its `TruncatedLogNormal(μ, σ, l, u)`, aligned with its truncated normal, with σ > 0; the mixtures
    carried into stage files by the converter's numbers now, and by a Bellman family later.
- **Q(1) leaves the quantile maps** (2026-10-20), and nothing replaces it above 0.999 (2026-10-21). The toolkits' sessions
  are consulted before any change to what a results file carries.
- **The coverage points are each toolkit's** (2026-10-21); a statistic comparable across toolkits is deferred.

**The emitter** (the HAFiscal-Latest session).
- Its ladder of 2026-10-20 wrote and verified the three members' first two levels and the toy's third, against both the
  branch's checker and #2's.
- The toy's fourth level ran out of the run's memory after solving all seven types.
- It reruns under the emitter's version 0.5, after a kernel comparison, in about seven hours. Its checker line comes when
  it ends.

**Open with the owner:**
- every merge;
- the name of the w3id.org namespace;
- in the bellman session, the uniform for Bellman's comparator and Bellman's draft for the truncated lognormal;
- filing Bellman's parameter-condition defect.

**Next work:**
- the merges, on his word;
- a line in #2's description saying the toy's third and fourth levels verify too, once the fourth exists;
- the survey's other classes;
- the rest of the prose of `bst-markov_ui-and-agg/1`.

See [`../deferred.md`](../deferred.md).

**Elsewhere:**
- **The bellman session** holds Bellman's draft pull request for the truncated lognormal, and the uniform request.
- **The HAFiscal-Latest session** runs the emitter. Its version 0.4 reads the quantile probabilities from the schema it
  validates against.
- **As recorded on 2026-10-19:**
  - the HARK session holds the bounds-fix branch and the newborn flag;
  - the BufferStockTheory session recorded the lower-tail finding on two branches.

**How to apply:** start from this file and the rulings. Change a schema document only after a proposal to the owner, put
anything a results file carries to the toolkits' sessions first, and keep private material out of this repository.
