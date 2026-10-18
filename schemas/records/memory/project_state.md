---
name: project_state
description: "What the schema project holds, what is settled and what is open, as of 2026-10-18 17:45 EDT"
metadata:
  type: project
---

**What exists in `schemas/`** (all drafts; none proposed to the working group yet):
- Shared: `shock-laws.md` with its validator; `numerics.md` (method, settings and suite files, with the stage file's targets
  as a method file's addresses); `foundation.md` (the stage file as the foundation of a family's statement); the design note
  `hafiscal-models-and-test-suite.md`.
- `bst/1`: `model.md` (read from the stage file, in BST's notation), `conditions.md` (validity conditions, domain rules,
  implications, the simulation phase), `results.md` and `results.schema.json`, `parameters.schema.json`, the members
  `library`, `toy` and `toy-untruncated`, and `bellman/buffer_stock.bl` with the community library's calibration.
- `bst-markov_ui-and-agg/1`: only its stage file and two calibrations; its prose is not written.
- `checker/`: the strict loader and hash, the laws' closed-form moments in log space, the member checker with the four
  lower-tail cases, the converter to Bellman's calibration, the results validator's test; 51 tests.

**Settled** (see the rulings): BST's notation; ρ > 1; a newborn born employed at P = 1 with no assets; the bounds a̲_Art and
a̲_Nat with a̲ = max of the two; truncated lognormal as the usual law, with the stated standard deviation kept after truncation
and bounds at ±3; one written form and the hash over the parsed numbers; welfare in utils with W, F and M reported and no
consumption-equivalent; the restructuring on the stage file, four of six steps done.

**Open with the owner:** the toy's specification following bst/1's newborn; whether the precision levels are settings rather
than error targets; three small results-file keys the emitter proposed; the eight points the Markov family's stage file left
for decision, with the code's conventions now known; a third value of that family's permanent-income switch for the paper's
corrected world; the one Matsya job on the finished `bst/1` document. See [`../deferred.md`](../deferred.md).

**Elsewhere:** the HAFiscal-Latest session's emitter writes results files for the toy (its first validates); the HARK session
holds the bounds-fix branch and the newborn flag, unpushed; the bellman session is filing the seven requests to the Bellman
maintainer; the BufferStockTheory session recorded the lower-tail finding on two branches, unpushed.

**How to apply:** start from this file and the rulings; change a schema document only after a proposal to the owner; keep
private material out of this repository.
