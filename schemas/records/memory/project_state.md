---
name: project_state
description: "What the schema project holds, what is settled and what is open, as of 2026-10-19 08:10 EDT"
metadata:
  type: project
---

**What exists in `schemas/`** (all drafts; none proposed to the working group yet):
- Shared: `shock-laws.md` with its validator; `numerics.md` (method, settings and suite files, with the stage file's targets
  as a method file's addresses); `foundation.md` (the stage file as the foundation of a family's statement, five of its six
  steps done); the design note `hafiscal-models-and-test-suite.md`.
- `bst/1`: `model.md` (read from the stage file, in BST's notation), `conditions.md` (validity conditions, domain rules,
  implications, the simulation phase), `results.md` and `results.schema.json` (with the optional environment, driver and
  parameter-file keys), `parameters.schema.json`, the members `library`, `toy` and `toy-untruncated`, and
  `bellman/buffer_stock.bl` with the community library's calibration.
- `bst-markov_ui-and-agg/1`: its stage file, with the three-valued switch for permanent income while unemployed, and three
  calibrations of the dropout group's middle type, one per value; its model document, read from the stage file; its
  conditions document, with bst/1's conditions as matrix conditions over the chain; its results, validator and members are
  not written.
- `checker/`: the strict loader and hash, the laws' closed-form moments in log space, the member checker with the four
  lower-tail cases, the converter to Bellman's calibration, the results validator's tests, and the verification of a
  results file's report on the effective member; 72 tests.

**Settled** (see the rulings): BST's notation; ρ > 1; a newborn born employed at P = 1 with no assets; the bounds a̲_Art and
a̲_Nat with a̲ = max of the two; truncated lognormal as the usual law, with the stated standard deviation kept after truncation
and bounds at ±3; one written form and the hash over the parsed numbers; welfare in utils with W, F and M reported and no
consumption-equivalent; the restructuring on the stage file; the precision levels as settings, with measured convergence the
only source of tolerances; the switch's three values with `continues` the standard; ξ_U and ξ_X for the replacement incomes
and named groups; the borrowing limit in the household's units; the benchmark's toy following bst/1's newborn.

Ruled at 19:17 on 2026-10-18: the Markov family's newborn follows bst/1's convention; the normal regime is absorbing with
no hazard key in the parameter file; "agg" in the family's name is the aggregate regime alone; the Matsya completeness job
on bst/1 goes ahead through the bellman session.

The Matsya completeness job ran at 20:32 the same day (see the findings): the prose and the stage file contradict each other
nowhere; Matsya flipped the unemployment law in its own round trip; its output's domain for the borrowing limit matches the
model document where our stage file declares ℝ.

**The effective member** (`effective-member.md`, approved and executed on 2026-10-18 by 22:51): the schemas state the
problem without methods or forms; a toolkit solves its own effective member and reports the expectations the family
names, every condition's factor and verdict decided on it, the lowest values of its representation and the derived
parameters it used; the checker verifies what needs no representation, labels its own report as the stated member's,
the limit, and marks a verdict `undecided` within the closed forms' precision; a law's lowest value is defined as the limit
of a representation's bottommost point, which is why truncated laws keep every effective member in the stated member's
regime. The results validator, the checker (73 tests, with `--verify-results`), both model and conditions documents, the
results document, the numerics document and the README's vocabulary follow it. Since 2026-10-19 a toolkit that pushes
the population forward under another representation reports it in an optional block that decides the population's
conditions.

**Open with the owner:** the form of the
stage files' tightened domains, pending Matsya's answer on derived parameters in the language; whether the Markov stage
file's natural constraint becomes a per-state entry. **Next work:** the proposal's implementation on his approval, then
the rest of the prose of `bst-markov_ui-and-agg/1`: the results schema, the parameter validator and the members. See
[`../deferred.md`](../deferred.md).

**Elsewhere:** the HAFiscal-Latest session has changed the benchmark's toy specification to bst/1's newborn, is regenerating
its reference, emits the three optional keys, and has answered: the published numbers came from `frozen`, the paper's text
describes `continues`, and the text is silent on a newborn's state and first-quarter shocks; the HARK session holds the bounds-fix branch and the newborn flag, unpushed; the bellman session has filed the seven
requests in its repository, uncommitted; the BufferStockTheory session recorded the lower-tail finding on two branches,
unpushed. The owner asked at 18:28 on 2026-10-18 for this branch to be pushed to the fork after the second memorial.

**How to apply:** start from this file and the rulings; change a schema document only after a proposal to the owner; keep
private material out of this repository.
