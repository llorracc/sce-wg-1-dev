---
name: project_state
description: "What the schema project holds, what is settled and what is open, as of the fourth memorial of 2026-10-21, after the fork's seven pull requests merged"
metadata:
  type: project
---

**On the schemas' branch** (`buffer-stock-schema-work_CDC`, pushed). It holds the merged work of the fork's seven pull
requests and `main`'s ontology. Nothing has been proposed to the working group's repository yet.
- **Shared:**
  - `shock-laws.md` with its validator;
  - `numerics.md` (method, settings and suite files, with the stage file's targets as a method file's addresses);
  - `foundation.md` (the stage file as the foundation of a family's statement);
  - the design note `hafiscal-models-and-test-suite.md`;
  - the plan `existing-syntax.md`, executed for the distribution class;
  - `conventions.md`, with its standing check;
  - `rosetta/`: the Rosetta Stones for HARK and QuantEcon's JAX code, with their cards.
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

**The fork's pull requests, all merged on 2026-10-21** (llorracc/sce-wg-1-dev), each with a merge commit:

| # | what it held | merged |
|---|---|---|
| 7 | the notation in two spellings, reconciled with econ-ark's registry | 23:04, `5b4207f`, into the schemas' branch |
| 1 | the ontology of probability distributions | 23:07, `e07a574`, into `main`; the schemas' branch took `main` |
| 2 | the shock laws on the ontology | 23:08, `e43c566` |
| 3 | the quantile maps without Q(1) | 23:09, `5cff244` |
| 4 | how far the stationary distribution's representation reaches | 23:09, `c389b73` |
| 5 | no run time in a results file | 23:09, `36f8071` |
| 6 | the Rosetta Stones for HARK and QuantEcon's JAX code | 23:10, `a955677` |

The branches are kept. With everything merged, the checker's 150 tests and the ontology's 12 pass.

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
  sources. The plan of 11:59 for a QuantEcon adapter is superseded by the adapters of 20:41.
- **Notation** (2026-10-21): the BST paper is the authority.
  - Typeset, an underline marks a minimum (`\underline{\xi}`), and a word subscript is upright.
  - In plain text, names are in code font: `ξ_min`, `ψ_min`, `θ_min`, `a_Art`, `a_Nat`, `a_min`, `m_min`, `p_worst`.
  - ξ_U is the income while unemployed (19:25), after μ was withdrawn for its competing uses. `bst/1` allows the lowest
    employed income below it.
  - Econ-ark's notation registry, version 1.0.0 in econ-ark-tools, is in force beside BST: the target `\hat{m}`, the
    pseudo-target `\check{m}`, 𝒢 for the growth factor (so 𝒢_t for the Markov family's factor in a quarter), and a bold
    thorn for the patience factors.
  - The batch of 20:43: the natural limit −`ξ_min` `ψ_min`/(ℛ − `ψ_min`) without κ; R(1 − `κ_min`) for the old
    min(Þ, R); `sep`, `find`, `p_exit`, `reg` and ℷ in the Markov family, Ω in the HAFiscal design note; plain-text names
    for minima and word subscripts only, marks above a letter kept.
  - All of it merged with #7; the registry's version 2.1.0 carries rows for the schemas' own symbols.
- **Adapters** (20:41): a toolkit's adapter reads a parameter file, solves, and writes a results file; adapters live in
  `schemas/adapters/`. HARK's comes first, then dolo's; no QuantEcon module is published. HARK's is built on its Markov
  consumer with `bst/1` as the nonpersistent chain, starts from the benchmark's emitter with its private material taken
  out, pins HARK pull request #1858's commit, and writes no operating-system string in a results file's provenance.

**The emitter** (the HAFiscal-Latest session).
- Its ladder of 2026-10-20 and the rerun of the toy's fourth level on 2026-10-21 wrote eight results files. All of them
  verify against both the branch's checker and #2's.
- Each level's changes fall by a factor of about three, the first measured error estimates for comparing toolkits.
- Its version 0.7 writes the run time only where the schema it validates against has the field.

**The Rosetta Stones** (#6, merged).
- HARK's stone describes the standard consumer; it is to be revised for the Markov adapter.
- Matsya's third session, on HARK's source, waits for the owner's word in the bellman session.

**Open with the owner:**
- registering `w3id.org/sce`, a pull request to w3id.org's public repository, and then the ontology's namespace with a new
  version and the checker's copy of its table;
- making the dolo dry runs' model files, which are the benchmark's and private, the public basis of dolo's adapter;
- what goes to the working group's repository, and when;
- in the bellman session: the uniform for Bellman's comparator, Bellman's draft for the truncated lognormal, and Matsya's
  third session;
- filing Bellman's parameter-condition defect;
- in the HARK session: #1858, which stays a draft for now.

**Next work:**
- HARK's adapter in `schemas/adapters/hark/`, with the gate in the findings of 2026-10-21 on HARK's Markov consumer; then
  HARK's stone revised for it;
- dolo's adapter;
- the comparison of results files, and the validators for the method, settings and request files;
- the remaining notation differences, as econ-ark-tools' reconciliation reaches them;
- the survey's other classes;
- the rest of the prose of `bst-markov_ui-and-agg/1`.

See [`../deferred.md`](../deferred.md).

**Elsewhere:**
- **The econ-ark-tools session** keeps econ-ark's notation registry (version 3.0.0 on its master, which frees ζ for the
  Pareto exponent; 4.0.0 waits as its #48). **The NARK session** keeps econ-ark's naming conventions.
- **The bellman session** holds Bellman's draft pull requests for the truncated lognormal and the uniform, and runs
  Matsya.
- **The community-library session** stopped the QuantEcon module on the evening of 2026-10-21; its branches stay local.
- **The HAFiscal-Latest session** runs the emitter, version 0.7, the basis of HARK's adapter.
- **As recorded on 2026-10-19:**
  - the HARK session holds the bounds-fix branch and the newborn flag;
  - the BufferStockTheory session recorded the lower-tail finding on two branches.

**How to apply:** start from this file and the rulings. Change a schema document only after a proposal to the owner, put
anything a results file carries to the toolkits' sessions first, and keep private material out of this repository.
