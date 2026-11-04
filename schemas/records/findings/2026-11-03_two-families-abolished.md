# Two families abolished: `bst-natural-no-point-mass/1` and `bst-zero-infima/1`

The owner's rulings of 17:59:50 and 18:01:14 on 2026-11-03 ([the rulings](../rulings/2026-11-03_harness-decisions.md)):
both families are uninteresting cases. Applied the same evening, as the Markov family's retirement was on 2026-11-01.
The last commit holding them is `2ae4c35`. Two families remain, `bst-natural/1` and `bst-artificial/1`.

## What went

- `schemas/bst/other/`: the stage files `natural-no-point-mass.bl` and `zero-infima.bl`, the two validators, and the
  members `toy-natural`, the toy's laws with no artificial constraint, and `toy-untruncated`, the toy with untruncated
  lognormals.
- The checker, `bst1.py`: the two scenarios' checks, the zero-infima rules for the kink and the binding case, the
  untruncated laws' calibration path and the never-paid benefit's floor, and the moment helper only the zero-infima
  check used. A natural member whose joint worst income has probability zero is now refused, with no family to send it
  to, as is an artificial member with a zero floor.
- The results validator's list of families; the notation, stone and checker tests' lists of scenarios and members;
  HARK's adapter tests' members, its natural-limit test now on `library`, whose limit is zero.
- The ontology: the family rows `BSM_0000225` and `BSM_0000227` retired; the tests' members and family map; the README
  and the changelog; the generated files.
- The documents: `bst/model.md`, `bst/conditions.md`, `constraint-scenarios.md`, the README of the schemas, the
  checker's README, the adapters' README, HARK's adapter README, the stones for HARK, dolo and QuantEcon's JAX code,
  and `for-toolkit-authors.md`.

## What stays

- The scenarios' analysis in `constraint-scenarios.md`, which is why the natural family requires a point mass at the
  joint worst income and the artificial family positive floors.
- The ontology's classes `natural-without-point-mass` and `zero-infima`, with their axioms and results, written by no
  family: the ontology says what exists, and the owner spoke of the families. Whether the classes should go is put to
  him.
- The floor cases in `bst/conditions.md` that only the abolished families reached, kept as derivations with no family
  named.
- HARK's stone's evidence of its gate's run on the untruncated toy, from 2026-10-21 and 22, the record of a past run.
- The records of 2026-11-01, which say how the four families were made.

## What the tests establish

| suite | on 2026-11-02 | after the abolition |
|---|---|---|
| the checker | 200 | 191 |
| the buffer-stock ontology | 67 | 61 |
| the distributions' ontology | 12 | 12 |
| the harness's runner | 7 | 7 |
| HARK's adapter, in its locked environment | 8 | 8 |
| dolo's adapter, in its locked environment | 4 | 4 |

The tests that went were the abolished members' and folders' parametrized cases and the lower-tail test that used
them; the rejection of a member filed under the retired `bst/1` is now tested on the toy. No remaining member's hash
changed, and no results file changed. The adapters' suites still solve and verify `toy` and `library`; HARK's
natural-limit test runs on `library` now, whose limit is zero.
