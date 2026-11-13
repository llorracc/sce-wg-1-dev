# The borrowing-constraint scenarios, applied

2026-11-01, from 12:51 EST, on the owner's rulings of 12:50:56 ([`constraint-scenarios.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/constraint-scenarios.md)).

Since 13:43 the natural scenario without a point mass and the zero-infima scenario are in `other/` in both families
(the owner's ruling of 13:38:32). The paths below are as they were when this was written.

## What was built

- **Six families, each with its own stage file:**
  - `bst-natural/1`, `bst-natural-no-point-mass/1`, `bst-artificial/1` and `bst-zero-infima/1`, in `bst/`, with what they
    share there: the model, the conditions, the results schema and the common parameter definitions;
  - the Markov family's `bst-markov_ui-and-agg-artificial/1` and `bst-markov_ui-and-agg-zero-infima/1`.
- **No stage file carries the natural limit as a parameter.** Bellman-SYM refuses a derived scalar (`h_min := …`: "no
  construction rule for the definition"). So `natural-no-point-mass.bl` writes the limit out inline from the laws'
  bounds, with `min` for the worst transitory income, and the other files need none.
- **The truncated stage files write TruncatedLogNormal(μ, s, ψ_min, ψ_max).** The bounds are in the draw's units and the
  location makes the mean one after truncation, as the checker's converter computes.
- **The Markov artificial version selects ψ's law by name.** In a quarter of unemployment under `grows` or `frozen`, ψ is
  a point mass, which a truncated lognormal cannot write, since it needs σ > 0. The file selects the law by `P_u`, then
  by `j`, two selections by declared names; Bellman refuses a selection by a computed index.
- **Every stage file elaborates on Bellman-SYM's current main**, all six, checked again at 13:23.
- **The checker:**
  - it validates each file against its family's schema, each schema read with its own URI so that its references to
    the shared definitions resolve;
  - it checks the scenario's requirements from the laws' true bounds and masses;
  - it writes each family's calibration.

  The binding case is named "the constraint binds", since the zero-infima scenario has no artificial constraint, and
  PF-FVAC is FVAC-PF.
- **The members:**
  - `library` truncated at ±3σ, in `bst-natural/1`;
  - `toy` in `bst-artificial/1`;
  - a new `toy-natural`, the toy's laws with no artificial constraint, in `bst-natural-no-point-mass/1`;
  - `toy-untruncated` in `bst-zero-infima/1`, with no `borrowing_constraint` key;
  - in the Markov family, `toy-as-hafiscal` in the artificial version, and `paper-published` and `paper-one-group` in
    the zero-infima version, also without the key.

  Every member's family key, and so its hash, changed.

## What the tests establish

- The checker's 194 tests pass. Among them, each scenario's requirements refuse eleven deliberate breaks, and each
  member's calibration names exactly its stage file's parameters.
- The adapter's 7 tests pass at its pinned HARK. They solve and verify `toy` and `library`, and solve `toy-natural`
  under the stated laws' natural limit.
- The ontology's 52 tests pass. A new test puts each of the four members in exactly the scenario class its family
  writes, by the classes' axioms.

None of these solves the model beyond the adapter's own runs. What the scenarios say about reaching the limit is
recorded with its source, and is not tested.

## What does not hold yet

- **No stage file for a natural member with a positive benefit.** Its point mass needs a discrete ψ, and the stage
  files write truncated lognormals.
- **The Markov family has no natural version.**
- **Existence is not stated** in the natural scenario without a point mass, nor in the artificial scenario with
  `a_Art` < 0 (`bst/conditions.md`).
- **Results files written for the old hashes are stale.** That is the emitter's ladder and the adapter's gate files,
  which are to be rerun.
