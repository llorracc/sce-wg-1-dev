# Bringing the work to the working group's repository: the pull requests in order

**Status: ADOPTED, 2026-11-04, in the evening, with the recommendations taken on every decision below: the framework upstream and the model in its repository; the records kept out of upstream; the apparatus document at the repository's root; the order as listed, the first new pull requests cut at once.** The owner asked, in the evening, how thoroughly the new way of doing things is
documented and where, and whether the work since the fork left econ-ark/sce-wg-1 should be organized into a set of
coherent pull requests to upstream that merge in order and build the new way systematically. This document answers
both. Nothing is cut or opened until he says.

## Where the documentation is, and how thorough it is

The new way of doing things is documented in four places, each thorough for what it is and none of them the single
statement a working-group member could read first.

| what | where | state |
|---|---|---|
| the purpose and the exactness criterion | econ-ark/sce-wg-1 pull request #14; [`../project-a/exact-definition.md`](../project-a/exact-definition.md) | settled; open upstream |
| the architecture: one repository per canonical model as a REMARK, the core, the images, the container contract, the registry's execution records, the updates to REMARK | [`registry.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/registry.md), ADOPTED; the record schemas [`../harness/execution-record.schema.json`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/harness/execution-record.schema.json) and [`../harness/runs.registry.schema.json`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/harness/runs.registry.schema.json) | settled in substance; written as a proposal with its history |
| the decisions and their reasons | [`records/rulings/2026-11-04_architecture.md`](records/rulings/2026-11-04_architecture.md), [`records/rulings/2026-11-04_purpose.md`](records/rulings/2026-11-04_purpose.md), the journal | complete; a record, not an exposition |
| how the harness runs today | [`../harness/README.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/harness/README.md), the runner's docstring, the adapters' READMEs | current |
| the earlier designs the architecture builds on or supersedes | [`harness.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/harness.md) (approved, its design section predating the container runtime), [`participation.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/participation.md) (proposed, its kit and ingest path overtaken by REMARK's machinery), [`comparing-solutions.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/comparing-solutions.md), [`reference-solution.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/reference-solution.md), [`experiments.md`](https://github.com/llorracc/sce-wg-1-dev/blob/72ee2eef21c1c75f60c109a851118f9b4f025ad8/schemas/experiments.md), [`for-toolkit-authors.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/for-toolkit-authors.md) | mixed: approved, proposed, partly superseded, each saying so in its own status line |
| what lives where since this afternoon: the fork, wg1-buffer-stock, the REMARK session's clone, upstream | the handoff to the wg1-buffer-stock session (on-box) and the journal | not in any public document |

So: every decision is recorded with its reasons, and every built piece has a README, but the whole is spread over
sixteen design documents written for the owner and the sessions, with status lines, stamps and the sessions'
names, and no document says in one place what the working group builds, where each part lives and how a member takes
part. That document is the first thing the series below adds, and each later pull request carries its documents in
settled form, the history pointed to rather than restated.

## What the fork holds against upstream

The branch `buffer-stock-ontology` left upstream at its merge of 2026-10-01 and has 95 commits of its own; upstream
has 34 since, the primer and the site. The branch adds 406 files, in round numbers: the two ontologies (24 files),
the schemas (323 files, of which 262 are the records), the stones (7), the harness (27), and the purpose proposal.
The earlier work branch and the open pull request #15 are wholly inside it; #14's Markov family is retired, so both
fork pull requests close. The same content is in wg1-buffer-stock at the branch's commit 5c6961b, with its own
session since this afternoon.

## The one decision the series depends on

The architecture adopted this afternoon separates the core, what every canonical model shares, from a model's
repository, which is a REMARK. Upstream is the working group's repository. Two ways to read the request:

- **Everything upstream.** The branch's whole content goes to econ-ark/sce-wg-1 in ordered pull requests, the
  buffer-stock model included as the worked example, and wg1-buffer-stock becomes a thin REMARK that depends on
  upstream at a tag, or is retired. One home, no packaging first; but the working group's repository then holds one
  model's adapters, runs and records, and the split into a core comes later by extraction.
- **The framework upstream, the model in its repository.** Upstream takes what every model shares: the statement of
  the apparatus, the vocabulary and conventions, the two ontologies (Project A's deliverables, which the proposal says
  the group's repository keeps), the stone convention, the experiment schema, the harness's generic parts and the
  record schemas, and the participation rules. wg1-buffer-stock keeps the families, their validators and checker, the
  stones, the adapters, the experiments, the findings and the records, and depends on upstream's core. This is the
  adopted architecture; it costs making the core a package before the model repository can stop vendoring it, which
  the owner deferred this afternoon, and separating the checker's generic modules from the family's.

**Recommended:** the second, staged: the framework goes upstream now in the order below, wg1-buffer-stock keeps
vendoring the core until the packaging lands (its copy is the fork's at 5c6961b), and nothing of the model is
duplicated upstream. The fork's buffer-stock content is then superseded by wg1-buffer-stock, and the fork keeps only
the staging of upstream pull requests and its history.

## The pull requests, in order

Each is cut from upstream's main, self-contained, with its documents in settled form and its tests passing in
upstream's continuous integration, which today builds only the site and the primer and is not touched by new
folders. Each depends on the ones before it.

1. **The purpose made exact.** Pull request #14, already open: the README, the landing page and the special-issue
   proposal. Merge first; everything after it uses its words.
2. **The apparatus.** One document, `apparatus.md` at the root or a page of the site, stating what the working group
   builds and where: a canonical model's repository as a REMARK whose reproduction is the comparison; the core this
   repository holds; the toolkits' Rosetta Stones and adapters; the execution records and the registry; REMARK's
   tool; how a toolkit's author takes part; and the exactness test as the whole's purpose. With it the vocabulary
   (today the glossary of `schemas/README.md`) and `conventions.md`. This is the document that does not exist yet.
3. **The ontology of probability distributions.** `ontologies/probability-distributions/`, standalone: the catalog of
   families and charts, the formulas, the tests, the README. Version 0.1.0 at merge.
4. **The ontology of buffer-stock models.** `ontologies/buffer-stock-models/`: the classes, axioms, conditions and
   results in BST's terms, with the Bellman-SYM statement, the generated JSON and Turtle, the tests. Its references to
   the families' schemas point at wg1-buffer-stock.
5. **The shock laws and the stone convention.** `shock-laws.md`, written on the probability ontology, and
   `rosetta/README.md`, what a Rosetta Stone holds and how a toolkit's cards are kept; the stone tests' generic part.
   The stones themselves stay with the model.
6. **The experiment schema and the record schemas.** `experiment.schema.json` with `experiments.md` in settled form;
   `execution-record.schema.json`, the core, until REMARK takes it; `runs.registry.schema.json` as the pattern for a
   model repository's entry.
7. **The harness's core.** The runner, `records.py`, the adapter contract, the container contract, the toolkit
   registry's form, the checker's generic modules (the canonical serialization and hash, the laws, the experiment
   checks) and their tests, as a package the model repository can pin; `harness.md` and `registry.md` in settled form.
   This is the pull request that lets wg1-buffer-stock stop vendoring.
8. **Participation.** `for-toolkit-authors.md`, `participation.md`, `comparing-solutions.md` and
   `reference-solution.md` in settled form: what an author provides, what the organizer does, how solutions are
   compared and what the reference is; the ledger's rules; the license for submitted results.
9. **The first canonical model.** No content: the README's project list and the apparatus document point at
   wg1-buffer-stock as the first canonical model, once it is public and cataloged in REMARK, and at the REMARK
   updates that carry the execution records.

Under the first reading instead, items 5 to 9 widen: the families, the checker, the stones, the adapters, the
experiments and the findings go in as three or four further pull requests after the harness, and the records stay
in the fork and the model repository in either reading.

## The series as it stands

| pull request | branch of the fork | state on 2026-11-04 in the evening |
|---|---|---|
| #14, the purpose | `exact-definition` | open |
| #16, the apparatus, the vocabulary, the conventions | `apparatus` | open |
| #15, the ontology of probability distributions | `ontology-probability-distributions` | open; the compiled files it first carried removed and ignored |
| #17, the ontology of buffer-stock models | `ontology-buffer-stock-models`, on #15's branch | open; a family row may name the repository that holds its schema; the six tests that need the model's files stay with the model |
| #18, the shock laws and the stone convention | `shock-laws-and-stones` | open |
| #19, the experiment schema and the execution-record schemas | `experiment-and-record-schemas` | open; the schemas identified by upstream's paths |
| #20, the core as a package, `wg1core` | `harness-core`, on #19's branch | open; the design taken: the runner, records, canonical, laws and the experiment checker in `core/`, the three validators as its data, a `model` section in the registry file, its tests on a model repository of their own; since, the Apache License 2.0, Python 3.11 or later, the core naming its commit; the verifier's command run from the repository's root, its example corrected and the rule tested; a record naming the continuous-integration run that made it; a clone without a nameable remote refused before running |
| the comparator | `comparator`, merged into the fork's main; not yet a pull request | built on 2026-11-04 in the evening with the two schema changes it rests on |
| participation | | not cut: a rewrite of four documents whose decisions are still the owner's |
| the first canonical model | | after wg1-buffer-stock is public and cataloged |

**The harness's core, cut as #20 with the design below taken.** Today the runner imports the checker's modules by path and the
experiment checker reads the family's results schema and the model's experiments folder; the runner's tests use the
model's experiment and its committed results through the stand-in adapter. A package that a model repository pins
needs: a name; the modules that move (the runner, the records, the canonical serialization and hash, the laws, the
experiment checker with the results schema given to it rather than found); the command line; a stand-in family and
experiment for its own tests; and the model repository's imports changed to it, which is the wg1-buffer-stock
session's work. That design is put to the owner before anything is cut.

**Participation needs the owner's decisions.** `participation.md` lists twenty decisions for him; the settled form
upstream states rules, not decisions, so the rewrite follows the rulings.

## The fork's trunk, since the evening of 2026-11-04

The owner decided to build the remaining framework pieces in the fork before they go upstream: the seven branches
of the series were merged in order into the fork's `main`, which tracks upstream and now stands 29 commits beyond it
at 0652b49, with the core's tests and both ontologies' passing there. The remaining framework branches are cut from `main` and merged back into it, the comparator the first of them, built
the same evening, the core's continuous integration next; each later
goes upstream as a pull request from its branch. wg1-buffer-stock pins the core from the fork's `main` at a commit
until upstream merges and tags. `buffer-stock-ontology`, the old working branch, is frozen as history, except that this
session's journal and records continue on it until the owner moves them. The core package is under the Apache
License 2.0, as HARK is.

## What each pull request costs

The code moves are mechanical. The cost is the writing: every document goes upstream in its settled form, stating
what the thing is, with its history as a pointer to the records rather than as the proposal's own text, and with
no session's name, no stamp and none of the owner's words in it. The sixteen design documents hold about 3,800
lines; the settled forms are shorter. The apparatus document is new.

## What happens to the fork and its branches

After the series, the fork keeps `main` tracking upstream and a branch per pull request; `buffer-stock-ontology`
is kept as the history up to 5c6961b and the journal after it, and the work branch `buffer-stock-schema-work_CDC`
and the two open pull requests close as superseded. The records continue in wg1-buffer-stock for the model and here
for the staging.

## Decisions for the owner

- The reading: the framework upstream and the model in its repository, as recommended, or everything upstream.
- Whether the records, the project's memory, go upstream at all; recommended not: they stay with the model and the fork.
- The apparatus document's place: the repository's root, or a page of the site beside Project A's.
- The order above, or another; and whether the first three pull requests are cut now, since they depend on nothing
  that is still moving.
