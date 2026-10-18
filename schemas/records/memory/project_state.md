---
name: project_state
description: "What the schema project holds, what is settled and what is open, as of 2026-10-18 18:38 EDT"
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
  calibrations of the dropout group's middle type, one per value; its prose is not written.
- `checker/`: the strict loader and hash, the laws' closed-form moments in log space, the member checker with the four
  lower-tail cases, the converter to Bellman's calibration, the results validator's tests; 54 tests.

**Settled** (see the rulings): BST's notation; ρ > 1; a newborn born employed at P = 1 with no assets; the bounds a̲_Art and
a̲_Nat with a̲ = max of the two; truncated lognormal as the usual law, with the stated standard deviation kept after truncation
and bounds at ±3; one written form and the hash over the parsed numbers; welfare in utils with W, F and M reported and no
consumption-equivalent; the restructuring on the stage file; the precision levels as settings, with measured convergence the
only source of tolerances; the switch's three values with `continues` the standard; ξ_U and ξ_X for the replacement incomes
and named groups; the borrowing limit in the household's units; the benchmark's toy following bst/1's newborn.

**Open with the owner:** the Markov family's newborn convention; whether the zero hazard of a recession's onset is a fixed
feature of the family or a key of the parameter file; the one Matsya job on the finished `bst/1` document. See
[`../deferred.md`](../deferred.md).

**Elsewhere:** the HAFiscal-Latest session changes the benchmark's toy specification to bst/1's newborn, runs the emitter's
ladder, and owes two answers (which world produced the published numbers; what the paper's text says of a newborn's state);
the HARK session holds the bounds-fix branch and the newborn flag, unpushed; the bellman session has filed the seven
requests in its repository, uncommitted; the BufferStockTheory session recorded the lower-tail finding on two branches,
unpushed. The owner asked at 18:28 on 2026-10-18 for this branch to be pushed to the fork after the second memorial.

**How to apply:** start from this file and the rulings; change a schema document only after a proposal to the owner; keep
private material out of this repository.
