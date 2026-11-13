---
name: project_state
description: "What the schema project holds, what is settled and what is open, as of 13:15 on 2026-11-13: main at 8b34952 with the three live branches merged, the records branch renamed `records`, slimmed and pushed, the hold released, two worktrees and two branches; and as of the memorial of 11:46 on 2026-11-12 (earlier memorials' blocks kept below it): the fork's main with the reference as its own kind, three branches of live work unmerged, a plan for the branches; and as of the memorial of 19:12:50 on 2026-11-04 (the state of the evening's commit and of the memorial of 08:07 on 2026-11-03 kept below the later changes): the fork's thirteen pull requests merged, #15 open, the ontology's branch unpushed; two buffer-stock families, the other two abolished on 2026-11-03; the Markov family retired; two experiments; the Jacobian interface approved, in the results schema and verified by the checker; the restrained-limit experiment run with HARK and with dolo, whose adapter shares its toolkit-neutral code with HARK's; the experiment schema and the harness plan approved, with the words experiment and ladder; the layout of ontologies/, schemas/, rosetta/ and harness/; the harness's runner built and accepted; the rulings of 2026-11-02 that the harness gives parameters only and leaves the representation to each toolkit, and the revised proposal of 2026-11-03 that followed, the distributions of permanent income and of wealth in levels and the joint, with the adapters' independence planned, all awaiting the owner's reading; the toy-hafiscal estimation built in the HAFiscal session on his request; the ontology at draft.2, naming no toolkit; the ruling of 2026-11-04 that a reference solution is the standard, his answers to its decisions later that morning, and the results-schema ruling of the same morning, the quantiles required and the distribution function at the comparison points added"
metadata:
  type: project
---

**As of 13:15 on 2026-11-13**, what has changed since the blocks below:
- **The fork's main is at 8b34952,** pushed. It gained three merges that day, each by pull request with a merge
  commit and the core's tests run on it first: #17, the stone convention amended for the method files; #18, the
  core's reader for REMARK's status table, kind `canonical-model`; #19, the metrics an experiment defines, with the
  registry schema's eighth draft. 50 tests pass on main.
- **The records branch is `records`,** renamed from `buffer-stock-ontology` on GitHub and locally, pushed, the hold on
  its push released by the owner at 12:58:10. It holds the records, the instructions file and two documents found
  nowhere else, the model's stale files removed; 16 files it shares with main in older versions remain, for his
  decision.
- **The fork has two worktrees and two local branches,** the records branch and main; nine branches on GitHub, main,
  `records` and the heads of the working group's seven open pull requests; two archive tags; no open pull requests
  ([the plan](../plans/2026-11-12_branches-and-worktrees.md), its steps in the fork done).
- **What is open with the owner** is in [the deferred items](../deferred.md): whether the working group's seven pull
  requests are merged by him or put to the group first; the 16 older shared files; the fork's deploy job, failing
  for want of GitHub Pages; the status reader's reading of records of earlier drafts, due since the merges; four
  further points on metrics; the rule on a failed build's image and three small fixes to the core; the ontology's
  statement on Bellman's documentation.

**As of the memorial of 11:46 on 2026-11-12**, what has changed since the blocks below:
- **The fork's main is at f557ef4,** pushed. It gained, by pull request #16, the reference as an object of its own:
  a solution's kind, exact or numerical, and its role, the reference or an entry; checks that hold the entries of
  one kind to a member's reference; a metric relative to the reference; the registry schema's seventh draft.
- **Three branches of live work wait on the owner,** each local, unpushed and unmerged, and all three merging
  together without conflict: `stone-method-files` (2700da6), the stone convention's amendment for Bellman's methods
  file; `status-reader` (74312f9), the core's reader for the status table of REMARK's catalog, kind
  `canonical-model`; `experiment-metrics` (09a4548), the metrics an experiment defines, with the registry schema's
  eighth draft.
- **Bellman is read in `bellman-dev`** and consulted through its session, since 2026-11-09; its documentation is
  public at bellman.io.
- **REMARK's main holds the working group's six updates,** the execution records, the private mark and the status
  table among them, with no release tagged; the core's use of REMARK's records and schema waits on a tag.
- **Two model repositories pin the core:** the buffer-stock model's and the perfect-foresight model's, the second
  at the commit #16 merged.
- **The fork has six worktrees and six local branches** since 17:02 on 2026-11-12, when the plan's first step
  cleared away twelve merged branches and five worktrees on his word; the plan's other steps, which bring them to two
  each, wait on his decisions ([the plan](../plans/2026-11-12_branches-and-worktrees.md)).
- **What is open with the owner** is in [the deferred items](../deferred.md): the three branches; four further
  points on metrics from the buffer-stock session; the plan's five decisions; the rule on a failed build's image and
  three small fixes to the core; the ontology's statement on Bellman's documentation; and the records branch's
  push, held.

**As of the memorial of 19:12:50 on 2026-11-04**, the evening's additions to the block below:
- **The series to upstream.** Seven pull requests open on econ-ark/sce-wg-1, #14 to #20: the purpose; the
  apparatus with the vocabulary and the conventions; the ontology of probability distributions; the ontology of
  buffer-stock models, on #15's branch; the shock laws and the stone convention; the experiment and execution-record
  schemas; the core as the package `wg1core`, on #19's branch, under the Apache License 2.0, on Python 3.11 or later,
  naming its own commit. Each cut from upstream's main on its own branch of the fork with its documents in settled
  form; the two stacked ones say which merges first. The plan is [`upstreaming.md`](../../upstreaming.md), adopted.
- **The fork's trunk.** The owner builds the remaining framework in the fork before it goes upstream: the seven
  branches are merged into the fork's `main`, from which the framework branches are cut and merged back;
  wg1-buffer-stock runs on the core from `main` at a commit, 7679b48 since 21:17:53 on 2026-11-04, and changes the
  pin to upstream at a tag when the series merges. This branch, `buffer-stock-ontology`, is frozen as history, except for these records.
- **The comparator**, in the core: the experiment's checks evaluated as written, between members, toolkits or
  successive levels in the experiment's order, with verdicts of pass, fail, not applicable or error; every job's
  distances from its member's reference reported with the reference's error and no verdict, as the fifth reference
  decision has it; an uncomputable comparison an error that fails the command; the reference required to answer the
  same question by the identity keys the model names; the `compare` command; the registry entry's comparison block
  without a verdict (draft.6) and the experiment's pinned references with `reference_quantities`, both ruled.
- **The model repository's side.** The switch to the package is made, on the owner's word in that session at
  19:20:13 on 2026-11-04: its harness and both adapters pin `wg1-core` at a4a52bbd, the vendored runner, records,
  schemas and the checker's generic modules are gone, every suite passes, and the coarse-level reproduction through
  containers gives the eight jobs' results, methods and settings byte-identical to the vendored runner's, with ten
  records registered at the sixth draft. Repinned at 7679b48 and pushed on his word there at 21:17:53; its first
  continuous-integration run passed, every record naming the run. A results file need not be byte-identical across
  machines, so a reference's hash identifies its file, not a reproduction; by 2026-11-05 three two-core runners had
  given two sets of HARK files, so identity does not follow the core count, and its cause is not examined. Still that session's, on the owner's word there:
  the workflow, the levels in both adapters, restrained-limit's second version with pinned references, the
  reference solvers as toolkits named for their code (`bench-continuous`, later `hark-continuous`), the second HARK
  mode, the license push, going public and the REMARK catalog entry. The REMARK session's first update is committed
  locally in its clone, unpushed. The sixth reference decision, the distribution's method, is still open, so only the
  rule is certifiable.
- **The Markov route reassessed, 2026-11-05.** The owner now holds that solving the model through HARK's Markov consumer
  with a nonpersistent unemployment state was not the best approach and means to prepare a specialized
  `ConsBufferStockModel` class in HARK; the survey of the route is [the finding](../findings/2026-11-05_hark-markov-route-survey.md).
  The second HARK mode of the ruling of 2026-11-04 is superseded in prospect; what the class is to do and where its
  work lives are his to say.
- **The redesign of HARK's expectation machinery, 2026-11-05.** Asked for at 13:46:09, proposed here with the HARK,
  HARK-dev and HAFiscal sessions consulted, and ruled at 15:09:32 to be HARK-dev's work. Handed off with the whole
  afternoon's thread on his choices of 15:32:48 ([the handoff plan](../plans/2026-11-05_handoff-to-hark-dev.md),
  EXECUTED): filed in econ-ark/HARK-dev and confirmed at 15:54:22, the redesign and the point-mass plan now plans
  there with their decisions; the two files here keep the harness's part with a pointer. One hold is open: the
  HAFiscal session holds a fact about HARK's grid at a binding artificial constraint on his word in its session and
  is asking him whether that reaches the HARK session's independent measurement, which the survey's committed bullet
  carries; until his answer this branch is not pushed ([the deferred items](../deferred.md)).
- **The Rosetta Stones as data, 2026-11-06.** Asked at 10:46:02 whether the stones hold what builds the adapters and
  answered no; he agreed at 16:01:18 and asked for proposals. [The proposals](../plans/2026-11-06_stones-as-data.md),
  revised at 18:45 to his direction that capable AI sessions operate the system, are ACCEPTED (18:46:34, all nine
  decisions): a stone states desiderata for a competent reader and records each realization, with acceptance by
  outcome. The convention's text, `rosetta/README.md`, was drafted on `stone-convention`, merged to the fork's main
  (7a4889f) and pushed on his word on 2026-11-07; its revision reaches upstream through the open #18 or a follow-up.
  An amendment for the method files, after Bellman's specification 0.7 and his rulings of 2026-11-11 in the model
  repository's session, is drafted on the local branch `stone-method-files` (2700da6), and the core's reader for
  REMARK's status table, kind `canonical-model`, is written on the local branch `status-reader` (74312f9): both on
  his word of that night, unpushed and unmerged, for him to read. The same night the core gained, on a third local
  branch, `reference-as-its-own-kind` (6c12de1), the distinction he asked for in the perfect-foresight repository's
  session between a reference solution and a numerical one: a solution's kind, exact or numerical, and its role, the
  reference or an entry, with checks that hold entries to the reference; pushed and merged into the fork's main
  on his word on 2026-11-12, by pull request #16 (main at f557ef4). On his word of the same morning an experiment may define its own metrics, a
  pointwise distance with an aggregate or a function of the model's repository: built on the local branch
  `experiment-metrics` (09a4548), unpushed and unmerged.
  The stones and adapters are the model repository's session's to change, on his word there, with the prototype and
  the clean-room regeneration test as its evidence.
- **Open for the owner:** the level names (coarse, default, fine proposed); whether a record's `ci` block should
  carry fields for the attempt, the repository and the workflow's name beyond the provider, the identifier and the
  attempt's address, recommended not; the comparator's pull request upstream;
  participation's rewrite, after his twenty decisions; the model pointer upstream once wg1-buffer-stock is public and
  cataloged; the pushes of the model repository's commits and the REMARK session's branches, in their sessions; and
  the earlier items, R6 among them.

**As of the commit of the evening of 2026-11-04** (the day's rulings: [the purpose](../rulings/2026-11-04_purpose.md),
[the architecture](../rulings/2026-11-04_architecture.md), [the reference solution](../rulings/2026-11-04_reference-solution.md);
[the journal](../journal/2026-11-04_session-record.md)):
- **The purpose made exact.** The owner confirmed the reading that the project is its own test of Project A's thesis,
  and the exact-definition criterion, every valid solution method converging, given unbounded computation, to the same
  solution as every other, with a canonical definition fixed for each model the group takes up, was proposed, approved
  and opened as econ-ark/sce-wg-1 pull request #14 from the fork's branch `exact-definition`
  ([`project-a/exact-definition.md`](../../../project-a/exact-definition.md)); the fork's own documents say "valid
  solution method" for "bug-free toolkit", and the vocabulary gained the three terms.
- **The architecture.** The buffer-stock model is the canonical model, its scenarios its families; one repository per
  canonical model, not split yet; the adapters define and pin their environments; the images live in the model
  repository until a second model; ConsIndShock and the Markov version with nonpersistent unemployment are two modes of
  solution, a `mode` string proposed for the results schema; the no-timings rule is revoked
  ([[feedback_no-timings]], superseded); Docker, its buildx plugin and repo2docker are installed on jhu-dell.
- **The toy-hafiscal work moved to HAFiscal-Latest** until it is ready: the bundle verified there row by row; the member
  `iid-ui-artificial`, the HAFiscal design note, the Lorenz-in-levels finding and the model document's section removed
  here, the Jacobian interface kept and made general. It returns as one piece on three decisions typed in that session.
- **The run registry on REMARK's machinery, adopted** ([`registry.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/registry.md)): the model repository as a
  REMARK whose `reproduce.sh` is the comparison and whose exit is the verdicts, `binder/` defining the organizer's
  image; a registry entry as a REMARK execution record, the core
  [`harness/execution-record.schema.json`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/harness/execution-record.schema.json) at 0.1.0-draft.4 after three
  readings by the REMARK session, the fork's entry [`harness/runs.registry.schema.json`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/harness/runs.registry.schema.json);
  five updates to REMARK begun in the session `jd_REMARK_integrate-with-WG1` on the owner's word, its first, execution
  without a terminal, committed locally there, the push and the pull requests on his word in that session.
- **Built here.** `harness/adapters/<toolkit>/env/` with a Dockerfile beside each lock file, both images built; the
  runner's `--runtime docker` under the container contract, build and execution records (`harness/records.py`),
  `verify` filling the verdicts, `register` into `harness/runs.registry/`; one HARK and one dolo job through
  containers, verified. Tests: runner 9, checker 199, HARK 9, dolo 4, the ontologies 58 and 12.
- **Open for the owner:** the registry entries' location; the `mode` string; the license; the level names (coarse,
  default and fine proposed); the HAFiscal session's three decisions; the REMARK session's push and pull requests; the
  push of this branch; and the morning's items on the reference solution and the results schema, recorded below.

**The ruling of 2026-11-04, 06:23:39** ([the ruling](../rulings/2026-11-04_reference-solution.md)): a reference
solution of each member, solved to very high precision by the continuous methods developed in the HAFiscal and HARK
contexts, with a wide and dense grid and an ergodic distribution on a dense grid to the 99.9th percentile of wealth, is
the standard, and actual solutions at default settings are compared to it. It answers the two questions of
`schemas/comparing-solutions.md` put to him the evening before, and supersedes that design's agreement question. The
proposal is `schemas/reference-solution.md`, PROPOSED, nothing built; the HAFiscal-Latest, HARK-dev and HARK sessions
were asked the same morning which code solves the members as stated and what their defaults are. The continuous
methods: HAFiscal's kink-split expectation in its SM2 form with the Hermite EGM, private and moving into HARK as its
single source; HARK's continuous solver on the HARK session's unposted local branches, whose names stay out of public
text, with the issue #1869 and the drafts #1861 to #1863 as its public parts; the bench's diagnostics expectation, the
same rule. The three sessions answered the same morning; the proposal carries what they settled. The probe of the same
morning, `records/findings/2026-11-04_reference-probe/`, ran the bench's continuous EGM on the four restrained-limit
members: the rule to 10⁻¹² to 10⁻¹⁰ with the closed forms at round-off, the committed ladder's finest level 8 · 10⁻⁴
from the stated member's solution, HARK's defaults 5 · 10⁻³ to 10⁻² off, and on a dense distribution grid the
transition's nodes the binding error, so that a continuous landing is required; the proposal's section "What the probe
found" carries it.

**The owner's answers later that morning** ([the rulings](../rulings/2026-11-04_reference-solution.md)): R1 and R5
accepted; R4 ruled in part, the harness without default settings and each stone stating three precision levels, the
names coarse, default and fine proposed; R3 answered, awaiting his word; R6 to be discussed in detail; a registry of
every run requested, in tension with the rule against timings, put to him. On R2 he ruled that the results schema
require the quantiles and carry the distribution function at the comparison points; applied the same morning to the
schema, the results document, the checker's verifier and the shared emitter, with the consequence that the committed
results files of 2026-11-01 no longer validate until superseded or regenerated. On the HAFiscal session's measurements
of the field, two defects, he ruled before 11:31:06 that request points move off genuine atoms and that a get
comparison points of its own: the request rule, the request file's `a_points`, the results file's
`a_comparison_points` and the checker's flags, applied the same hour; the field required for m alone.

**On branch `buffer-stock-ontology`** (from the schemas' branch; committed, not pushed, no pull request):
`ontologies/buffer-stock-models/`, the semantic ontology of buffer-stock models, version 0.1.0-draft.2, rows
`BSM_0000001` to `BSM_0000231`, 209 in force and 19 retired; 61 tests, none of which solves a model
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
stage file ([`constraint-scenarios.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/constraint-scenarios.md),
[the findings](../findings/2026-11-01_constraint-scenarios-applied.md)). Since 13:38 two are principal, `bst-natural/1`
and `bst-artificial/1`, in `bst/`; `bst-natural-no-point-mass/1` and `bst-zero-infima/1` were in `bst/other/` until
the owner abolished both on 2026-11-03 as uninteresting cases ([the rulings of 2026-11-03](../rulings/2026-11-03_harness-decisions.md)):
two families remain, and the two scenarios stay described in `constraint-scenarios.md` with no family writing them.

**The Markov family is retired** (16:10:29 on 2026-11-01), after its zero-infima version went at 13:51:57 since
HAFiscal's code never solved that scenario ([[feedback_classify-by-what-the-code-solves]]). Its one-state unemployment
model is a calibration of the buffer-stock families, and a Markov state only a way to solve it
([[feedback_markov-family-is-a-device]]): `iid-ui-artificial`, the toy with ℘ = 0.05 and ξ_u = 0.5, is a
`bst-artificial/1` member. The four-state family and the paper's members are in the history
([the findings](../findings/2026-11-01_markov-family-as-the-code-solves.md)).

**One experiment for every toolkit's solution** (`bst/model.md`; called a test suite until 2026-11-02): the
restrained-limit experiment, BST's "The Liquidity Constrained Solution as a Limit": `bst-p-zero-0.005`, `-0.0005` and
`-0.00005` in `bst-natural/1` and `bst-restrained` in `bst-artificial/1`, solved with HARK and dolo
([the findings](../findings/2026-11-01_restrained-limit-suite.md)). The second, on an estimated member with three
types, is with the HAFiscal-Latest repository since 2026-11-04 until it is ready.

**The Jacobian interface** (`jacobians.md`), kept as buffer-stock infrastructure when the toy-hafiscal work moved:
designed with the HARK, HARK-dev, HAFiscal-Latest and QuantEcon sessions and DolARK's design, and approved at 17:05:24
on 2026-11-01. The Jacobians with their metadata are optional in a results file, an experiment may require them, as
`.npy` matrices; the fake-news ingredients are optional, as data. The
inputs are the return, a scale on all non-capital income and a transfer proportional to permanent income; the outputs
C, A and Y_hh; one distribution grid for every toolkit; a steady state to 10⁻¹⁰. The block is the key `jacobians` of
`bst/results.schema.json` (approved 17:26:21), and `checker/jacobians.py` verifies it.

**The restrained-limit experiment's first run** (`schemas/bst/experiments/restrained-limit/`, in `bst/suites/` until
2026-11-02): common request files for its four members,
and a comparison from results files alone. HARK's adapter at levels 1 to 3 shows the natural rules converging to the
restrained one, the largest gap 0.137, 0.061 and 0.027 at the kink
([the findings](../findings/2026-11-01_restrained-limit-suite-hark/README.md)), drawn on the private page "The
Restrained Limit", whose source is in the findings' `page/`.

Its experiment file, `experiment.yaml`, is the first under `experiment.schema.json` (`experiments.md`). dolo's adapter
ran it too on 2026-11-01 and agrees with HARK's (the findings of that run). On 2026-11-02 the harness's runner
reproduced both toolkits' files at `low` from lock files ([the findings](../findings/2026-11-02_harness-acceptance/README.md)).

On 2026-11-03, after the two families' abolition, the checker's 191 tests, the runner's 7, the buffer-stock ontology's 61
and the distributions' 12 pass, and HARK's adapter's 8 and dolo's 4 in their locked environments.

**Open pull request #15** (`stage-derivative-terms`, pushed, against the schemas' branch, opened 22:24:43 on
2026-10-31): both families' stage files rewritten with Bellman-SYM's derivative terms, as the owner approved at 22:17:58.
Both elaborate on Bellman-SYM's current main; the checker's 175 tests pass. Unmerged; what follows its merge is in the
deferred follow-ups.

**On the schemas' branch** (`buffer-stock-schema-work_CDC`, pushed). It holds the merged work of the fork's thirteen
pull requests and `main`'s ontology. Nothing has been proposed to the working group's repository yet.
- **Shared:**
  - `shock-laws.md` with its validator;
  - `numerics.md` (method, settings and ladder files, with the stage file's targets as a method file's addresses, under
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
  `schemas/adapters/`, in `harness/adapters/` since 2026-11-02. HARK's comes first, then dolo's; no QuantEcon module is published. HARK's is built on its Markov
  consumer with `bst/1` as the nonpersistent chain, starts from the benchmark's emitter with its private material taken
  out, and records neither the machine's name nor its operating system. Merged as #8 after passing its gate (the
  findings on HARK's Markov consumer), pinned to #1858's commit; since #12 it pins #1862's, stacked on it, whose solvers
  compute a `natural` member's limit from the laws' infima, the stated `a_Nat`. dolo's adapter followed on 2026-11-01,
  on dolo's release 0.4.9.20 and its `egm`, with the toolkit-neutral code of both in `adapters/common.py`; it has run
  the restrained-limit experiment and agrees with HARK's (the findings of that run).

**The emitter** (the HAFiscal-Latest session).
- Its ladder of 2026-10-20 and the rerun of the toy's fourth level on 2026-10-21 wrote eight results files. All of them
  verify against both the branch's checker and #2's.
- Each level's changes fall by a factor of about three, the first measured error estimates for comparing toolkits.
- Its version 0.7 writes the run time only where the schema it validates against has the field.

**The Rosetta Stones** (#6, revised in #11).
- HARK's stone describes `MarkovConsumerType` at the adapter's pin, with the standard consumer in a section of its own.
- Matsya's third session, on HARK's source, ran on 2026-10-22 and agrees with the stone (the findings of that day).

**The harness's rulings of 2026-11-02 and the revised proposal of 2026-11-03**
([the rulings of 2026-11-02](../rulings/2026-11-02_harness-decisions.md), [of 2026-11-03](../rulings/2026-11-03_harness-decisions.md);
[`harness.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/harness.md), [`experiments.md`](../../experiments.md), [`bst/results.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/bst/results.md)), in
no validator, checker, member or adapter:
- The harness gives each toolkit parameters, never methods or settings (18:28:43 on 2026-11-02); the laws' representation
  is each toolkit's own, the true model the one with truncated lognormals (19:09:13). The experiment's checks
  `approaches_stated_member` and `toolkits_agree` replace `same_effective_member`. The adapters' independence is planned
  as the harness's stage 4, status PROPOSED, with three decisions for the owner; today the grid counts and the
  quadrature live in the adapters' shared module.
- The results document proposes three blocks: the distribution of permanent income, required, behind a status, its
  Lorenz curve defined when ℒ < 1 and ℒ𝒢 < 1; the distribution of wealth in levels a𝐩, required, behind a status, whose
  Lorenz shares at 0.2, 0.4, 0.6 and 0.8 are HAFiscal's targets and whose mean over mean income is K/Y
  (the finding, with the HAFiscal-Latest repository since 2026-11-04); and the joint of (m, 𝐩, c, a) as weighted
  points out of git, optional. No member or hash changes.
- The stationary permanent income condition proposed on the evening of 2026-11-02 was withdrawn at 04:37:53 on
  2026-11-03 with everything that served it; the notation registry's branch `notation-v8.1-spic` in the econ-ark-tools
  clone is superseded, to delete.
- The toy-hafiscal member's estimation was requested of the HAFiscal-Latest session at 05:23 on 2026-11-03 and built
  there for the member as stated, 𝒢 = 1.0019026 for every household with newborns at 1; it waits on the owner's word in
  that session. The published first step's economy differs, growing through its newborns, and whether the member should
  mirror it is the owner's.

**Open with the owner:**
- the revised proposal of 2026-11-03: the three results blocks and the checker's statuses for them, the restrained-limit
  experiment's second version, the stage-4 plan's three decisions (dolo's population with mortality, HARK's population
  method, the diagnostics' quadrature), the joint as weighted points, and the closed forms E[𝐩] and var(log 𝐩) offered;
- the notation registry's branch `notation-v8.1-spic`, superseded, to delete;
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
- the toy-hafiscal work, with the HAFiscal-Latest session since 2026-11-04: the estimation's go, the emitter's move to
  the new schema and the continuous method for the reference, typed there; the return as one piece, or the member
  alone first;
- HARK's cyclical index: ruled on 2026-10-31 that solver and simulation be consistent, the simulation side to be fixed,
  made clear on 2026-11-01 not to find the solver right; the fix is the HARK-dev session's;
- #15, to merge;
- in the HARK session: #1858 and #1862, which stay drafts; the tags on HARK's fork at the adapter's two pins,
  `sce-adapter/2026-10-22` and `sce-adapter/2026-10-22.2`, were made on 2026-10-22;
- what goes to the working group's repository, and when;
- in the bellman-dev session, the bellman session's successor since 2026-11-09: nothing pending from the owner; Bellman's
  truncated lognormal and the uniform comparator merged on 2026-10-22, and the parameter-condition defect is filed;
- in the bellman-ark session: the three changes asked of Bellman on 2026-10-31, drafted on 2026-11-03 (a message to its
  maintainer on the Matsya service's lag behind the language, a pull request on the typography of fields and
  functions, an issue on Γ in two senses), each waiting on his approval there and his word on who sends or posts it;

Registering `w3id.org/sce` is not raised before a pull request from this fork is merged into econ-ark/sce-wg-1
([[feedback_w3id-not-yet]]).

**Next work:**
- the model repository as a REMARK: `binder/Dockerfile` for the organizer's image with the root Dockerfile kept
  identical by a test, `reproduce.sh` and `reproduce_min.sh`, the catalog entry on the owner's word; the two HARK modes
  and the `mode` string; the runner calling REMARK's package once its signatures are final;
- HARK's adapter writing the Jacobians block, from a branch carrying #1863, once an estimated member returns;
- the harness, approved on 2026-11-02 ([`../../harness.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/harness.md)): the layout's move done in `9675109`
  (`rosetta/`, `harness/adapters/`, `schemas/bst/experiments/`); the registry, lock files and runner built and accepted
  (`harness/`; the findings of 2026-11-02 on its acceptance); next, on the owner's reading of the revised proposal, the
  three results blocks with the checker's statuses, the restrained-limit experiment's second version, the adapters'
  independence (stage 4, planned) and the comparator (stage 5). The experiment schema and its first experiment are
  drafted and approved ([`../../experiments.md`](../../experiments.md));
- the estimated member, once the HAFiscal session returns it ready: validated and hashed by the checker, solved by
  HARK's adapter, the fit evaluated again with the family's newborn; then its experiment file and request file;
- the proposal to the working group's repository, whose trigger, dolo's adapter and the first comparison of two
  toolkits' results files, is met as of 2026-11-01 (deferred follow-ups); the owner's to start;
- the validators for the method, settings and request files; the survey's other classes;
- the toy's level-4 gate run for the adapter.

See [`../deferred.md`](../deferred.md).

**Elsewhere:**
- **The econ-ark-tools session** keeps econ-ark's notation registry (version 8.0.0 on its master since 2026-10-22); no
  session lives in its clone on this machine, whose branch `notation-v8.1-spic` is superseded, to delete. **The NARK
  session** keeps econ-ark's naming conventions.
- **The bellman-dev session**, in the clone of `bellman-dev`, the development repository, is since 2026-11-09 the
  session Bellman is read in and consulted through, on the owner's word; the bellman session before it held Bellman's
  draft pull requests for the truncated lognormal and the uniform and ran Matsya, and its consultation of 2026-10-31
  on the ontology is in its on-box record. Bellman's changes to 2026-11-09 are reviewed in
  [the journal](../journal/2026-11-09_session-record.md): the stage files, the laws and the concepts stand; the
  methods file and the public site are with the owner.
- **The bellman-ark session** on this machine, since 2026-11-03 the only writer of Bellman's records, holds the three
  drafted changes.
- **The community-library session** stopped the QuantEcon module on the evening of 2026-10-21; its branches stay local.
- **The HAFiscal-Latest session** runs the emitter (version 0.8, unpushed on 2026-10-22), the basis of HARK's adapter;
  since 2026-11-04 it holds the toy-hafiscal work, the estimation built there on 2026-11-03 and the material moved
  from this fork, waiting on the owner's three decisions there.
- **The REMARK session**, `jd_REMARK_integrate-with-WG1`, in the local clone of econ-ark/REMARK since 2026-11-04,
  makes the five updates to REMARK; its first is committed locally; nothing pushed without the owner's word there.
- **As recorded on 2026-10-19:**
  - the HARK session holds the bounds-fix branch and the newborn flag;
  - the BufferStockTheory session recorded the lower-tail finding on two branches.

**How to apply:** start from this file and the rulings. Change a schema document only after a proposal to the owner, put
anything a results file carries to the toolkits' sessions first, and keep private material out of this repository.
