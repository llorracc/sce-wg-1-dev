# dolo's recasting of the household, probed against HARK

2026-11-01, on the owner's request to see whether a second toolkit reproduces the restrained-limit suite, and his
instruction to write dolo's Rosetta Stone first (`../../../rosetta/dolo.md`).

## What was run

- **The environment:** dolo's release 0.4.9.20, with dolang 0.0.20, on CPython 3.11.14 and numpy 1.26.4:

  ```sh
  uv run --python 3.11 --with dolo==0.4.9.20 --with jsonschema --with referencing --with pyyaml python probe3.py
  ```
- **The smoke test:** dolo's own `examples/models/consumption_savings_iid.yaml`, solved by `dolo.algos.egm.egm` as its
  `test_egm_iid` does. It converges in 475 iterations, and its rule spends everything below its kink.
- **The probe:** `probe.py` writes the household, normalized by permanent income, as a dolo model file (the stone's "The
  recasting"). It solves the model with `egm` on the schemas' own joint nodes of (ψ, ξ), which it gets from HARK's
  adapter's `shocks` and passes as a `FiniteDistribution`. The model's uniform grid has 40,001 points up to m = 200.
  The savings grid is 300 or 1200 points, geometric from 10⁻⁶ up to 400, with a = 0 added for the artificial member.
- **The comparison:** `probe3.py` compares the rule at the restrained-limit suite's common points with HARK's results
  files at levels 1 and 3, in `../2026-11-01_restrained-limit-suite-hark/results/`.

## The numbers

The largest |c_dolo − c_HARK| at the common points with m ≤ 20:

| member | dolo's nodes and savings points | against HARK's level 1 (7 nodes) | against HARK's level 3 (31 nodes) |
|---|---|---|---|
| `bst-restrained` | 7 nodes, 300 points | 8.7 · 10⁻⁴ | 1.3 · 10⁻² |
| `bst-restrained` | 7 nodes, 1200 points | 5.2 · 10⁻⁵ | 1.4 · 10⁻² |
| `bst-restrained` | 31 nodes, 1200 points | 1.4 · 10⁻² | 5.2 · 10⁻⁵ |
| `bst-p-zero-0.005` | 7 nodes, 300 points | 9.9 · 10⁻⁴ | 1.2 · 10⁻² |
| `bst-p-zero-0.005` | 7 nodes, 1200 points | 6.0 · 10⁻⁵ | 1.3 · 10⁻² |
| `bst-p-zero-0.005` | 31 nodes, 1200 points | 1.3 · 10⁻² | 5.9 · 10⁻⁵ |

- **Convergence:** every solve converged, `a_converged` true, to an error near 10⁻¹⁰.
- **Reproduced:** the probe was run again from this folder the same evening, and gave the same numbers to the
  digits shown.
- **Below the kink,** the restrained rule is c = m to within 10⁻¹⁶ of HARK's.

## What it establishes, and what it does not

- **The recasting is right.** On the same nodes and comparable grids, dolo's rule agrees with HARK's to about 5 · 10⁻⁵
  at both node counts. The 300-point savings grid's error, growing with m, is dolo's grid, not a difference of models.
- **The node count shifts both toolkits' rules alike,** by about 10⁻² at m = 10, so the comparison must match nodes.
- **What it is not:** an adapter. There are no results files, no population and no checker run, so nothing about dolo
  is yet established beyond these two members' rules at one setting each.

## Pending

- dolo's adapter, its results files for the suite, the checker's verification, and the comparison across toolkits.
