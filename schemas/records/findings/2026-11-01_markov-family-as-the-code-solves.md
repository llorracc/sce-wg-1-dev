# The Markov family as HAFiscal's code solves it

2026-11-01, 13:51–14:57 EST, on the owner's rulings of 13:51:57, 14:50:39 and 14:55:52.

## What was built

- **One version.** `bst-markov_ui-and-agg-zero-infima/1`, its stage file, parameter schema and three calibrations are
  retired. The family is `bst-markov_ui-and-agg-artificial/1`, and the checker refuses a law with a zero floor and the
  retired key.
- **The published package's members** (from the HAFiscal-Latest session's reading of llorracc/HAFiscal-QE).
  `paper-published` and `paper-one-group` state the laws the code solves on: HARK's
  `construct_lognormal_income_process_unemployment` with 7 equiprobable atoms of each mean-one lognormal (log variances
  0.003 and 0.12), no unemployment atom, at HARK 0.14.1, under which the estimates of record were made, and
  `BoroCnstArt = 0.0`. Their other values are unchanged, so they reproduce the published numbers and nothing is redone.
  The published simulations' age cap of 200 quarters and the newborn's assets of 1e-5 are in the headers, not the
  files.
- **ξ_x = 0 allowed,** so that the exhaustion state can be a zero-income disaster.
- **`iid-ui-artificial`,** formerly `toy-as-hafiscal`: unemployment with probability 0.05 every quarter, paying 0.5, and
  a ≥ 0, with the toy's other values; its counterpart is the toy with ℘ = 0.05 and ξ_u = 0.5.

## What the tests establish

- The checker validates both paper members: every condition holds for the 21 types, and the constraint in force is 0
  in every state.
- With ξ_x = 0 in `iid-ui-artificial`, the states from which the disaster can follow get natural limit 0, with chance
  1 − find, and the others stay below zero, so a ≥ 0 is valid and has a kink only in them.
- `iid-ui-artificial` is exactly its buffer-stock counterpart written in the family, and the reduction gives the
  counterpart's conditions, limits and tail exponent.
- None of this solves a Markov member; the published atoms have no stage file.

## What it found

- The Markov checker's tail-exponent search failed on the atoms for impatient types, and its chance of a zero-income
  state counted ψ's mass (the defects of 2026-11-01).
- The owner's device for a disaster state is one unemployment state that does not persist. HARK's adapter already
  solves every buffer-stock member that way, on HARK's Markov consumer. The four-state family as built is not that
  device; what becomes of it is with the owner.
