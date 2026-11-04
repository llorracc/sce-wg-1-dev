# The restrained-limit suite, solved with dolo's adapter, and compared with HARK's

2026-11-01, 19:48–19:54 EST for the runs, on the owner's "go ahead with the dolo adapter" that evening. The suite and
its request files are HARK's run's (`../2026-11-01_restrained-limit-suite-hark/README.md`): BST's "The Liquidity
Constrained Solution as a Limit", three `bst-natural/1` members with ℘ = 0.005, 0.0005 and 0.00005, and
`bst-restrained` in `bst-artificial/1`, at the same 39 common points in m.

## What was run

- **The adapter:** `../../../adapters/dolo/adapter.py`, with dolo's release 0.4.9.20 (dolang 0.0.20) on CPython 3.11,
  at the precision levels 1, 2 and 3, four members times three levels, each on two threads. At each level it uses the
  same nodes and savings grid as HARK's adapter, and the same code for everything but the solve (`../../../adapters/common.py`):

  ```sh
  uv run --python 3.11 --with dolo==0.4.9.20 --with jsonschema --with pyyaml --with referencing \
      python schemas/adapters/dolo/adapter.py schemas/bst/<scenario>/members/<member>.yaml --out <dir> --level <n> \
      --request schemas/bst/suites/restrained-limit/<member>.request.yaml
  ```
- **The checks:** all twelve results files validate and are consistent with their members, checked at 19:53 and again,
  from this folder, at 20:00:

  ```sh
  python schemas/checker/check.py schemas/bst/<scenario>/members/<member>.yaml --verify-results <dir>/results.json
  ```
- **Since 2026-11-04** the results schema requires the quantiles, which these files carry, and the distribution function
  at the comparison points, which they predate: against the current schema they fail validation on that field alone.
  They stay as the record of this run.
- **dolo's own comparison,** the same script as HARK's run, into `comparison.md` and `convergence.png`:

  ```sh
  uv run --with matplotlib --with numpy python schemas/bst/suites/restrained-limit/compare.py results .
  ```
- **The comparison across toolkits,** from both runs' results files alone, into `toolkits.md` and `toolkits.png`:

  ```sh
  uv run --with matplotlib --with numpy python schemas/bst/suites/restrained-limit/compare_toolkits.py \
      HARK ../2026-11-01_restrained-limit-suite-hark/results dolo results .
  ```

The results files, with the method and settings files each run wrote, are in `results/<member>/level-<n>/`.

## How dolo's rule is read

`egm` returns its rule as a cubic spline on the model's uniform grid of m, a point every 0.005 at every level. The
spline rounds the restrained rule's kink and ripples just below it. Read as the spline, the restrained member's mass at
the constraint came out 0.166 against HARK's 0.231 at level 1, with the kink's slopes wrong. The adapter therefore reads
the rule as `egm`'s own iteration holds it: linear between the spline's node values, with the kink's point added from
the Euler equation at a = a_min. The Rosetta Stone, `../../../rosetta/dolo.md`, records this as its second departure.

## The numbers

**The two toolkits' rules,** the largest |c_HARK − c_dolo| at the common points:

| member | level 1, m ≤ 20 | level 2, m ≤ 20 | level 3, m ≤ 20 | level 3, all |
|---|---|---|---|---|
| ℘ = 0.005 | 1.65 · 10⁻⁴ | 4.78 · 10⁻⁵ | 1.24 · 10⁻⁵ | 3.87 · 10⁻⁵ |
| ℘ = 0.0005 | 1.52 · 10⁻⁴ | 4.47 · 10⁻⁵ | 1.15 · 10⁻⁵ | 3.77 · 10⁻⁵ |
| ℘ = 0.00005 | 3.26 · 10⁻⁴ | 7.64 · 10⁻⁵ | 2.38 · 10⁻⁵ | 3.74 · 10⁻⁵ |
| restrained | 1.46 · 10⁻⁴ | 4.32 · 10⁻⁵ | 1.10 · 10⁻⁵ | 3.72 · 10⁻⁵ |

- **The difference falls with the level,** by a factor of 3 to 4 per level, so it comes from the grids. Below its kink
  the restrained rule is the same in both, to machine precision.
- **The MPCs** at the common points differ by up to 0.012 at level 3, for ℘ = 0.00005, whose rule bends most sharply.
  dolo's MPC is the slope of a segment 0.005 wide.
- **The restrained kink** at level 3: m = 0.974402 with slopes 1 and 0.4206 in dolo; m = 0.974405 with slopes 1 and 0.4185
  in HARK.
- **The stationary populations** at level 3: the mean MPCs equal to five digits (0.27011, 0.35952, 0.42284 and
  0.45559); the restrained member's mass at the constraint 0.21273 against 0.21274; mean assets within 2 · 10⁻⁵.
- **The convergence to the restrained rule:**

  | ℘ | HARK, level 3 | dolo, level 3 |
  |---|---|---|
  | 0.005 | 0.13742 | 0.13742 |
  | 0.0005 | 0.06096 | 0.06096 |
  | 0.00005 | 0.02666 | 0.02667 |

  In both, the gap falls by a factor of 2.254 and then 2.286 for each tenfold fall in ℘.

## The picture

The page "The Restrained Limit", republished as version 2 at 19:59:55 to the same private claude.ai link,
now draws both toolkits:
- a switch shows HARK, dolo, or both, with dolo dashed over HARK, on the rules, the gaps, the MPCs and the convergence;
- a new panel draws |c_HARK − c_dolo| at the common points on log scales;
- the table gives each number from both toolkits, HARK first.

Its source is in `page/`, and supersedes the one in HARK's run, which is version 1 as published. `extract.py` reads the
level-3 results files of both runs and writes `data.json` and `restrained-limit.html`, the page as published:

```sh
uv run --with numpy python page/extract.py
```

Version 2 also carries three fixes that version 1 should have had: the levels-1-and-2 markers of the convergence chart
are no longer joined into lines, the y-axis title is placed without a workaround, and a line that did nothing is gone
(`../../defects.md`).

## What it establishes, and what it does not

- **dolo reproduces HARK's restrained-limit suite.** On the same effective members, nodes and savings grids, the two
  toolkits' rules agree to about 10⁻⁵ at level 3, and their kinks, populations and convergence agree to the digits
  that matter. BST's limit holds in both, at the same slow rate.
- **The agreement is between two solutions of the same discretized household.** Both use the schemas' nodes and the
  shared population code, so it tests the two solvers, not the discretization or the population, which the adapters
  share.
- **What it is not:** a proof that either is right, a test of dolo's own laws or its `ergodic_distribution`, or of the
  two families in `bst/other/`. Welfare is not compared: dolo's adapter reports it as not computed.

## Pending

- The toy-hafiscal estimation, which waits on HAFiscal's session.
- A smaller fourth rung of ℘, if the owner wants the last gap smaller (deferred follow-ups).
- Policy evaluation in dolo's adapter, for welfare.
