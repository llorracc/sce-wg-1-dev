# The restrained-limit suite, solved with HARK

2026-11-01, 15:02–15:06 EST, on the owner's rulings of 14:59:32 and 15:01:21 (`bst/model.md`, "The restrained-limit
suite").

## What was run

The suite's four members, BST's calibration with ℘ = 0.005, 0.0005 and 0.00005 in `bst-natural/1` and the restrained
consumer, ℘ = 0 with a ≥ 0, in `bst-artificial/1`, were solved with the HARK adapter's own route at precision level 1:
`adapter.solve_type` on `adapter.shocks(member, 7)`, at the adapter's pinned HARK (llorracc/HARK at `11852805`). Each
rule was evaluated on one grid, 400 points on (0, 1] and 399 on (1, 10], and compared with the restrained rule:

```python
for name, f in files.items():
    member = bst1.load_member(f)
    nodes = adapter.shocks(member, lev["nodes"])[0]
    rules[name] = adapter.solve_type(member, member.types[0]["beta"], nodes, lev).solution[0].cFunc(m)
gap = max |rules[p] - rules["restrained"]|
```

The adapter's test `test_the_restrained_limit_suite_converges` runs the same comparison.

## The numbers

| ℘ | c(0.1) | c(1) | largest gap to the restrained rule on (0, 10] | where |
|---|---|---|---|---|
| 0 (restrained) | 0.100000 | 0.986546 | — | — |
| 0.005 | 0.093169 | 0.852707 | 0.138 | m ≈ 0.977 |
| 0.0005 | 0.097840 | 0.930701 | 0.061 | m ≈ 0.977 |
| 0.00005 | 0.099322 | 0.965593 | 0.027 | m ≈ 0.977 |

Every natural rule's lowest m is 0, the natural limit, and the restrained rule's is 0, its constraint.

## What it establishes, and what it does not

- The rules converge to the restrained rule as ℘ falls, as BST's proposition states, and the gap is largest at the
  restrained rule's kink, which the natural rules smooth. The gap falls by a factor of about 2.3 for each tenfold fall
  in ℘.
- It is one toolkit at one precision level. It does not measure the gap's convergence in the node count or the grid,
  and it does not test any other toolkit; the suite is for every toolkit's solution.
- The route is HARK's Markov consumer with the two-state chain that does not persist, which the adapter's existing test
  checks against HARK's standard consumer.

## Pending

- Other toolkits' solutions of the four.
- Whether the last rung should be smaller (deferred follow-ups).
