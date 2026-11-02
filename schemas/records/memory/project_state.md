---
name: project_state
description: "What the schema project holds, what is settled and what is open, as of the memorial of 10:37 on 2026-11-02: the fork's thirteen pull requests merged, #15 open, the ontology's branch unpushed; two principal buffer-stock families and two in other/; the Markov family retired; two test suites; the Jacobian interface approved, in the results schema and verified by the checker; the restrained-limit suite run with HARK and with dolo, whose adapter shares its toolkit-neutral code with HARK's; the experiment schema drafted and the harness plan approved, with the words experiment and ladder; the ontology at draft.2, naming no toolkit"
metadata:
  type: project
---

**On branch `buffer-stock-ontology`** (from the schemas' branch; committed, not pushed, no pull request):
`ontologies/buffer-stock-models/`, the semantic ontology of buffer-stock models, version 0.1.0-draft.2, rows
`BSM_0000001` to `BSM_0000205`, 193 in force and 12 retired; 47 tests, none of which solves a model
([[feedback_say-what-tests-establish]]).
- It states:
  - what makes a model a buffer-stock model: the membership axioms, the owner's atom rule of 2026-10-31 among them;
  - BST's hypotheses as a second tier, and the classes and extensions;
  - the objects in Bellman-SYM's terms;
  - the conditions with their implications, and the identities;
  - each term's written forms in four formats: three notations and the parameter file;
  - the divergences in other papers, a notation and the schemas.
- Draft.2 (2026-10-31 evening and 2026-11-01) adds:
  - Bellman-SYM's terms: perches, stage values, derivative terms, laws and connector, operators;
  - the natural and the artificial constraint told apart in behavior, conditions and limits;
  - Ma, Stachurski and Toda's conditions: the liquidity-constrained class and MST-βR;
  - the WRIC's necessity, treated as true until the paper proves it.
- It names no toolkit ([[feedback_ontology-names-no-toolkit]]): HARK's names and departures are in HARK's Rosetta Stone.
- The schemas are its syntax. It changes no schema. Its open questions are the owner's
  ([the rulings of 2026-10-31](../rulings/2026-10-31_ontology-decisions.md) and
  [of 2026-11-01](../rulings/2026-11-01_ontology-decisions.md);
  [the findings](../findings/2026-11-01_ontology-draft2.md)).

**The borrowing-constraint scenarios** (ruled 12:50:56 on 2026-11-01, applied that afternoon on `buffer-stock-ontology`,
committed and unpushed, for a draft pull request stacked on #15): `bst/1` gave way to four families, each with its own
stage file ([`constraint-scenarios.md`](../../constraint-scenarios.md),
[the findings](../findings/2026-11-01_constraint-scenarios-applied.md)). Since 13:38 two are principal, `bst-natural/1`
and `bst-artificial/1`, in `bst/`; `bst-natural-no-point-mass/1` and `bst-zero-infima/1` are in `bst/other/`.

**The Markov family is retired** (16:10:29 on 2026-11-01), after its zero-infima version went at 13:51:57 since
HAFiscal's code never solved that scenario ([[feedback_classify-by-what-the-code-solves]]). Its one-state unemployment
model is a calibration of the buffer-stock families, and a Markov state only a way to solve it
([[feedback_markov-family-is-a-device]]): `iid-ui-artificial`, the toy with ℘ = 0.05 and ξ_u = 0.5, is a
`bst-artificial/1` member. The four-state family and the paper's members are in the history
([the findings](../findings/2026-11-01_markov-family-as-the-code-solves.md)).

**Two test suites for every toolkit's solution** (`bst/model.md`):
- the restrained-limit suite, BST's experiment: `bst-p-zero-0.005`, `-0.0005` and `-0.00005` in `bst-natural/1` and
  `bst-restrained` in `bst-artificial/1`, solved with HARK
  ([the findings](../findings/2026-11-01_restrained-limit-suite.md));
- the toy-hafiscal suite, specified: three types, a center and a spread, estimated by HARK's and HAFiscal's tools to
  HAFiscal's Lorenz points, the iMPC profile and the wealth-to-income ratio, with one prize; every toolkit solves and
  simulates the steady state and exposes what its Jacobians need.

**The Jacobian interface** for the toy-hafiscal suite (`jacobians.md`): designed with the HARK, HARK-dev,
HAFiscal-Latest and QuantEcon sessions and DolARK's design, and approved at 17:05:24 on 2026-11-01. The Jacobians with
their metadata are required in a results file, as `.npy` matrices; the fake-news ingredients are optional, as data. The
inputs are the return, a scale on all non-capital income and a transfer proportional to permanent income; the outputs
C, A and Y_hh; one distribution grid for every toolkit; a steady state to 10⁻¹⁰. The block is the key `jacobians` of
`bst/results.schema.json` (approved 17:26:21), and `checker/jacobians.py` verifies it.

**The restrained-limit suite's first run** (`bst/suites/restrained-limit/`): common request files for its four members,
and a comparison from results files alone. HARK's adapter at levels 1 to 3 shows the natural rules converging to the
restrained one, the largest gap 0.137, 0.061 and 0.027 at the kink
([the findings](../findings/2026-11-01_restrained-limit-suite-hark/README.md)), drawn on the private page "The
Restrained Limit", whose source is in the findings' `page/`.

The checker's 180 tests, the adapter's 8 and the ontology's 67 pass.

**Open pull request #15** (`stage-derivative-terms`, pushed, against the schemas' branch, opened 22:24:43 on
2026-10-31): both families' stage files rewritten with Bellman-SYM's derivative terms, as the owner approved at 22:17:58.
Both elaborate on Bellman-SYM's current main; the checker's 175 tests pass. Unmerged; what follows its merge is in the
deferred follow-ups.

**On the schemas' branch** (`buffer-stock-schema-work_CDC`, pushed). It holds the merged work of the fork's thirteen
pull requests and `main`'s ontology. Nothing has been proposed to the working group's repository yet.
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
- **`bst-markov_ui-and-agg/1`:** its stage file with three calibrations, its model and conditions documents, its
  parameter validator, the members `toy-as-hafiscal`, `paper-one-group` and `paper-published` at the paper's published
  values, and the checker's module `markov.py` for its stated member (#13). Its results document is not written.
- **`checker/`:** 175 tests. It holds:
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
| 13 | the Markov family's parameter validator, first members and checker, at the paper's published values | 2026-10-22 22:44:03, `2910efe` |

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
  compute a `natural` member's limit from the laws' infima, the stated `a_Nat`. dolo's adapter followed on 2026-11-01,
  on dolo's release 0.4.9.20 and its `egm`, with the toolkit-neutral code of both in `adapters/common.py`; it has run
  the restrained-limit suite and agrees with HARK's (the findings of that run).

**The emitter** (the HAFiscal-Latest session).
- Its ladder of 2026-10-20 and the rerun of the toy's fourth level on 2026-10-21 wrote eight results files. All of them
  verify against both the branch's checker and #2's.
- Each level's changes fall by a factor of about three, the first measured error estimates for comparing toolkits.
- Its version 0.7 writes the run time only where the schema it validates against has the field.

**The Rosetta Stones** (#6, revised in #11).
- HARK's stone describes `MarkovConsumerType` at the adapter's pin, with the standard consumer in a section of its own.
- Matsya's third session, on HARK's source, ran on 2026-10-22 and agrees with the stone (the findings of that day).

**Open with the owner:**
- the ontology's open questions:
  - the two tiers, and what buffer-stock saving means;
  - the perfect-foresight and risky-asset classes;
  - the ontology's identifiers on the schemas' keys, and the atom axiom as a bst/1 validity condition;
  - what a Rosetta Stone holds, against which HARK's moved section is judged;
  - three points left by Ma, Stachurski and Toda;
- the push of `buffer-stock-ontology` and the scenarios' draft pull request, which this session's permission check
  refused as an external write;
- `library` against the community library's published v0.1, whose laws are untruncated: a v0.2 of the description
  (recommended), a renamed member, or a note;
- the estimation of the toy-hafiscal member, HAFiscal's to do on the owner's word in that session;
- HARK's cyclical index: ruled on 2026-10-31 that solver and simulation be consistent, the simulation side to be fixed,
  made clear on 2026-11-01 not to find the solver right; the fix is the HARK-dev session's;
- #15, to merge;
- in the HARK session: #1858 and #1862, which stay drafts; the tags on HARK's fork at the adapter's two pins,
  `sce-adapter/2026-10-22` and `sce-adapter/2026-10-22.2`, were made on 2026-10-22;
- what goes to the working group's repository, and when;
- in the bellman session: nothing pending from the owner; Bellman's truncated lognormal and the uniform comparator merged
  on 2026-10-22, and the parameter-condition defect is filed;

Registering `w3id.org/sce` is not raised before a pull request from this fork is merged into econ-ark/sce-wg-1
([[feedback_w3id-not-yet]]).

**Next work:**
- HARK's adapter writing the Jacobians block, from a branch carrying #1863, once the toy-hafiscal member exists;
- the harness, approved on 2026-11-02 ([`../../harness.md`](../../harness.md)): first the layout's move, as one commit
  with nothing else; then the registry with a lock file per toolkit, and the runner, accepted when it reproduces the
  committed results files at `low`; then the comparator. The experiment schema and its first experiment are drafted
  and approved ([`../../experiments.md`](../../experiments.md));
- the proposal to the working group's repository, whose trigger, dolo's adapter and the first comparison of two
  toolkits' results files, is met as of 2026-11-01 (deferred follow-ups); the owner's to start;
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
