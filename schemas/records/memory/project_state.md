---
name: project_state
description: "What the schema project holds, what is settled and what is open, as of the fourth memorial of 2026-10-22, after the fork's twelve pull requests merged"
metadata:
  type: project
---

**On the schemas' branch** (`buffer-stock-schema-work_CDC`, pushed). It holds the merged work of the fork's twelve pull
requests and `main`'s ontology. Nothing has been proposed to the working group's repository yet.
- **Shared:**
  - `shock-laws.md` with its validator;
  - `numerics.md` (method, settings and suite files, with the stage file's targets as a method file's addresses, under
    the rules of attachment of #11);
  - `foundation.md` (the stage file as the foundation of a family's statement);
  - the design note `hafiscal-models-and-test-suite.md`;
  - the plan `existing-syntax.md`, executed for the distribution class;
  - `conventions.md`, with its standing check;
  - `rosetta/`: the Rosetta Stones for HARK and QuantEcon's JAX code, with their cards, HARK's describing its Markov
    adapter since #11;
  - `adapters/`: HARK's adapter for `bst/1` (`adapters/hark/`), with its tests (6) and its gate.
- **`ontologies/probability-distributions/`:** the ontology of probability distributions, version 0.1.0-draft.1, rows
  `PD_0000001` to `PD_0000063`, its namespace provisional until `w3id.org/sce` is registered; 12 tests. The checker holds
  a pinned copy of its table.
- **`bst/1`:**
  - `model.md`, read from the stage file in BST's notation;
  - `conditions.md`;
  - `results.md` and `results.schema.json`, with the effective member and the optional population block;
  - `parameters.schema.json`;
  - the members `library`, `toy` and `toy-untruncated`;
  - `bellman/buffer_stock.bl`, with the community library's calibration.
- **`bst-markov_ui-and-agg/1`:** its stage file, and its model and conditions documents. Its results, validator and members
  are not written.
- **`checker/`:** 150 tests. It holds:
  - the strict loader and the hash;
  - the laws' closed forms in log space;
  - the member checker, with the four lower-tail cases;
  - the converter to Bellman's calibration;
  - the results validator's tests;
  - the verification of a results file's report on the effective member;
  - the shock laws' cross-test against the ontology, the notation check, and the Rosetta Stones' check.

**The fork's pull requests, all merged** (llorracc/sce-wg-1-dev), each with a merge commit:

| # | what it held | merged |
|---|---|---|
| 7 | the notation in two spellings, reconciled with econ-ark's registry | 23:04, `5b4207f`, into the schemas' branch |
| 1 | the ontology of probability distributions | 23:07, `e07a574`, into `main`; the schemas' branch took `main` |
| 2 | the shock laws on the ontology | 23:08, `e43c566` |
| 3 | the quantile maps without Q(1) | 23:09, `5cff244` |
| 4 | how far the stationary distribution's representation reaches | 23:09, `c389b73` |
| 5 | no run time in a results file | 23:09, `36f8071` |
| 6 | the Rosetta Stones for HARK and QuantEcon's JAX code | 23:10, `a955677` |
| 8 | HARK's adapter for `bst/1`, on HARK's Markov consumer | 2026-10-22 12:56, `0cfe05c`, by the owner |
| 9 | econ-ark's notation registry v5.0.0 and v6.0.0, and the HAFiscal design note's symbols | 2026-10-22 12:58, `673405f` |
| 10 | registry v8.0.0: ξ_u and ξ_x, j for the employment state, ℘'s gloss, the design note's replacement rates | 2026-10-22 16:02:08, `613a9fb` |
| 11 | each method where the stage gives it a place; HARK's Rosetta Stone for its Markov adapter | 2026-10-22 16:02:43, `a3f897a` |
| 12 | HARK's adapter under `natural`, pinned to HARK's draft #1862 | 2026-10-22 21:32:14, `d240a48` |

The merged branches and their worktrees were deleted at 18:07 on 2026-10-22. With everything merged, the checker's
150 tests and the ontology's 12 pass.

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
  - ξ_u and ξ_x for the incomes while unemployed (ξ_U and ξ_X until #10), and named groups;
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
  sources. The plan of 11:59 for a QuantEcon adapter is superseded by the adapters of 20:41.
- **Notation**: the BST paper and econ-ark's registry; the symbols in force are listed in
  [the notation memory](feedback_notation-and-foundation.md). Merged with #7 (2026-10-21) and #9 (2026-10-22). The
  registry's v8.0.0 rulings of 2026-10-22 (ξ_u and ξ_x, j for the employment state, ℘'s gloss, the design note's
  replacement rates) are merged with #10.
- **Method targets** (2026-10-22, #11): see [the memory on method attachment](feedback_method-attachment.md).
  `bst/1`'s stage file stays free of any method's lines (15:11:02).
- **Adapters** (20:41): a toolkit's adapter reads a parameter file, solves, and writes a results file; adapters live in
  `schemas/adapters/`. HARK's comes first, then dolo's; no QuantEcon module is published. HARK's is built on its Markov
  consumer with `bst/1` as the nonpersistent chain, starts from the benchmark's emitter with its private material taken
  out, and records neither the machine's name nor its operating system. Merged as #8 after passing its gate (the
  findings on HARK's Markov consumer), pinned to #1858's commit; since #12 it pins #1862's, stacked on it, whose solvers
  compute a `natural` member's limit from the laws' infima, the stated `a_Nat`.

**The emitter** (the HAFiscal-Latest session).
- Its ladder of 2026-10-20 and the rerun of the toy's fourth level on 2026-10-21 wrote eight results files. All of them
  verify against both the branch's checker and #2's.
- Each level's changes fall by a factor of about three, the first measured error estimates for comparing toolkits.
- Its version 0.7 writes the run time only where the schema it validates against has the field.

**The Rosetta Stones** (#6, revised in #11).
- HARK's stone describes `MarkovConsumerType` at the adapter's pin, with the standard consumer in a section of its own.
- Matsya's third session, on HARK's source, ran on 2026-10-22 and agrees with the stone (the findings of that day).

**Open with the owner:**
- in the HARK session: #1858 and #1862, which stay drafts; the tags on HARK's fork at the adapter's two pins,
  `sce-adapter/2026-10-22` and `sce-adapter/2026-10-22.2`, were made on 2026-10-22;
- what goes to the working group's repository, and when;
- in the bellman session: nothing pending from the owner; Bellman's truncated lognormal and the uniform comparator merged
  on 2026-10-22, and the parameter-condition defect is filed;

Registering `w3id.org/sce` is not raised before a pull request from this fork is merged into econ-ark/sce-wg-1
([[feedback_w3id-not-yet]]).

**Next work:**
- the Markov family (ruled 21:42:05 on 2026-10-22), in collaboration with the HARK and HAFiscal sessions: its parameter
  validator, members and checker first (begun on branch `markov-family`: the calibrations' keys and `markov.py`), then
  its results document, validator and verification, then HARK's adapter for its chains;
- dolo's adapter, written from the schemas, and the first comparison of two toolkits' results files;
- the validators for the method, settings and request files; the survey's other classes;
- the toy's level-4 gate run for the adapter.

See [`../deferred.md`](../deferred.md).

**Elsewhere:**
- **The econ-ark-tools session** keeps econ-ark's notation registry (version 8.0.0 on its master since 2026-10-22). **The NARK session** keeps econ-ark's naming conventions.
- **The bellman session** holds Bellman's draft pull requests for the truncated lognormal and the uniform, and runs
  Matsya.
- **The community-library session** stopped the QuantEcon module on the evening of 2026-10-21; its branches stay local.
- **The HAFiscal-Latest session** runs the emitter (version 0.8, unpushed on 2026-10-22), the basis of HARK's adapter.
- **As recorded on 2026-10-19:**
  - the HARK session holds the bounds-fix branch and the newborn flag;
  - the BufferStockTheory session recorded the lower-tail finding on two branches.

**How to apply:** start from this file and the rulings. Change a schema document only after a proposal to the owner, put
anything a results file carries to the toolkits' sessions first, and keep private material out of this repository.
