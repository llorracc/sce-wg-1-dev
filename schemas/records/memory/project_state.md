---
name: project_state
description: "What the schema project holds, what is settled and what is open, as of the second memorial of 2026-10-21"
metadata:
  type: project
---

**On the schemas' branch** (`buffer-stock-schema-work_CDC`, pushed with the memorials of 2026-10-21). All of it is draft, and none has been
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
| 5 | `drop-the-wall-time` | `c1362d9` | the schemas' branch | no run time in a results file: the provenance keeps hardware and threads; 74 tests, 86 with #3 and #4 |
| 6 | `rosetta-stones` | `a9e9043` | the schemas' branch | the Rosetta Stones for HARK and QuantEcon's JAX code, with their cards and a standing check, and `model.md`'s sentence on Bellman-SYM's families; 80 tests, 130 with #2. `329d78c` sits on the branch unpushed, waiting for the notation pull request |

**Merge order.**
- #1 merges into `main` first. The schemas' branch then takes `main`, and #2 merges after that.
- #3, #4 and #5 merge in any order: trial merges of each pair, and of all three, are clean. #3 and #4 share no file with
  #2; #5 shares the HAFiscal design note with it, in other places, and a trial merge of the two is clean.
- #6 merges cleanly with #2 to #5. It takes the notation pull request's spelling before it merges.
- Every merge, and taking a draft out of draft, is the owner's word.
- The main checkout no longer needs to stay at `4f99d01`, since the emitter's rerun reads its own copy of the schemas.

**Settled** (see the rulings):
- **Notation and the model:**
  - BST's notation;
  - ρ > 1;
  - a newborn born employed at P = 1 with no assets;
  - the bounds `a_Art` and `a_Nat`, with `a_min` the larger of the two;
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
- **No timings in public** (2026-10-21): no run time in the records or a results file (#5).
- **The Rosetta Stones** (2026-10-21) live in this repository's schemas, in Bellman's card fields, and cite only checkable
  sources. QuantEcon's adapter will import the community library's solver at a pinned commit.
- **Notation** (2026-10-21): the BST paper is the authority.
  - Typeset, an underline marks a minimum (`\underline{\xi}`), and a word subscript is upright.
  - In plain text, names are in code font: `ξ_min`, `ψ_min`, `θ_min`, `a_Art`, `a_Nat`, `a_min`, `m_min`, `p_worst`.
  - μ is the income while unemployed.
  - Approved, and committed locally on branch `notation-bst` (`cbcc0c9`), unpushed: the two spellings, the notation
    tables, μ for the income while unemployed, and the standing check. #6's stones take the new notation before both merge.

**The emitter** (the HAFiscal-Latest session).
- Its ladder of 2026-10-20 and the rerun of the toy's fourth level on 2026-10-21 wrote eight results files. All of them
  verify against both the branch's checker and #2's.
- Each level's changes fall by a factor of about three, the first measured error estimates for comparing toolkits.
- Its version 0.7 writes the run time only where the schema it validates against has the field.

**The Rosetta Stones** (#6).
- HARK's adapter in use is the benchmark's emitter, not yet public.
- QuantEcon's solver is a module in the owner's fork of the community library, local and unpublished, which solves
  `bst/1`'s members directly and agrees with HARK.
- Matsya's third session, on HARK's source, waits for the owner's word in the bellman session.

**Open with the owner:**
- every merge;
- whether `bst/1` requires the lowest employed income to be at least the income while unemployed;
- publishing the QuantEcon module;
- the name of the w3id.org namespace;
- in the bellman session: the uniform for Bellman's comparator, Bellman's draft for the truncated lognormal, and Matsya's
  third session;
- filing Bellman's parameter-condition defect.

**Next work:**
- the notation pull request, then #6 in its spelling with `329d78c`;
- the merges, on his word;
- a line in #2's description saying the toy's third and fourth levels verify too;
- the adapters, the comparison of results files, and the validators for the method, settings and request files;
- the survey's other classes;
- the rest of the prose of `bst-markov_ui-and-agg/1`.

See [`../deferred.md`](../deferred.md).

**Elsewhere:**
- **The bellman session** holds Bellman's draft pull requests for the truncated lognormal and the uniform, and runs
  Matsya.
- **The community-library session** builds the QuantEcon module in the owner's fork of the community library.
- **The HAFiscal-Latest session** runs the emitter. Its version 0.4 reads the quantile probabilities from the schema it
  validates against.
- **As recorded on 2026-10-19:**
  - the HARK session holds the bounds-fix branch and the newborn flag;
  - the BufferStockTheory session recorded the lower-tail finding on two branches.

**How to apply:** start from this file and the rulings. Change a schema document only after a proposal to the owner, put
anything a results file carries to the toolkits' sessions first, and keep private material out of this repository.
