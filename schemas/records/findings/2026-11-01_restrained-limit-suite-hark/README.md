# The restrained-limit suite, solved with HARK's adapter

2026-11-01, 17:39–17:57 EST, on the owner's "start" of that evening (`../../../bst/model.md`, "The restrained-limit
suite"). The experiment is BST's "The Liquidity Constrained Solution as a Limit": the natural constraint, with a zero-income
event of falling probability ℘, against the restrained consumer, with ℘ = 0 and a ≥ 0.

## What was run

- **The members:** `bst-p-zero-0.005`, `-0.0005` and `-0.00005` in `bst-natural/1`, and `bst-restrained` in
  `bst-artificial/1`. All four have BST's calibration, with the laws truncated at three standard deviations.
- **The request files:** one per member, with the same 39 points in m, from 0.01 to 50 and dense around the restrained
  rule's kink near m = 0.98. They are written by `../../../bst/suites/restrained-limit/make_requests.py`.
- **The runs:** HARK's adapter at the precision levels 1, 2 and 3, four members times three levels, each run on two
  threads, with HARK pinned at llorracc/HARK `11852805`:

  ```sh
  PIN="econ-ark @ git+https://github.com/llorracc/HARK.git@1185280590b21fe2ddac80cadcfea66476e45380"
  uv run --python 3.12 --with "$PIN" --with sympy --with jsonschema --with pyyaml --with scipy --with referencing \
      python schemas/adapters/hark/adapter.py schemas/bst/<scenario>/members/<member>.yaml --out <dir> --level <n> \
      --request schemas/bst/suites/restrained-limit/<member>.request.yaml
  ```
- **The checks:** each results file was checked against its member, and all twelve validate and are consistent:

  ```sh
  python schemas/checker/check.py schemas/bst/<scenario>/members/<member>.yaml --verify-results <dir>/results.json
  ```
- **Since 2026-11-04** the results schema requires the quantiles, which these files carry, and the distribution function
  at the comparison points, which they predate: against the current schema they fail validation on that field alone.
  They stay as the record of this run.
- **The comparison:** written from the results files alone into `comparison.md` and `convergence.png`:

  ```sh
  uv run --with matplotlib --with numpy python schemas/bst/suites/restrained-limit/compare.py results .
  ```

The results files, with the method and settings files each run wrote, are in `results/<member>/level-<n>/`.

## The numbers

The largest gap between the restrained rule and a natural member's, over the common points:

| ℘ | level 1 | level 2 | level 3 |
|---|---|---|---|
| 0.005 | 0.1373 | 0.1376 | 0.1374 |
| 0.0005 | 0.0606 | 0.06113 | 0.06096 |
| 0.00005 | 0.02636 | 0.02685 | 0.02666 |

- **Where the gap is largest:** at m = 0.975, the restrained rule's kink, in every row.
- **How fast it falls:** at level 3, by a factor of 2.25 and then 2.29 for each tenfold fall in ℘.
- **The stationary population** at level 3:

  | | mean MPC | mass at a = 0 | bottom 10%'s share of a |
  |---|---|---|---|
  | ℘ = 0.005 | 0.270 | 0 | 0.052 |
  | ℘ = 0.0005 | 0.360 | 0 | 0.032 |
  | ℘ = 0.00005 | 0.423 | 0 | 0.014 |
  | restrained | 0.456 | 0.213 | 0 |

  The natural members never reach their limit, so they have no mass at a = 0. Their mass piles up near zero as ℘ falls,
  and their mean MPC rises toward the restrained consumer's.

## The picture

The owner asked for the result to be shown graphically, since the numbers are far less striking than the picture. The
page "The Restrained Limit", published on 2026-11-01 as a private claude.ai page, draws from the level-3 results files:
- the four consumption rules, with a zoom on the kink;
- each natural rule's gap to the restrained one;
- the MPCs;
- the largest gap against ℘ on log scales, at the three levels;
- a table of the stationary populations.

Its source is in `page/`. `extract.py` reads the results files and writes `data.json` and `restrained-limit.html`, the
page as published, from `template.html`:

```sh
uv run --with numpy python page/extract.py
```

The MPC curves are differences of each rule's dense points. At the common points they are within 0.004 of the MPCs HARK reports
for ℘ = 0.005 and the restrained rule, 0.008 for ℘ = 0.0005, and 0.027 for ℘ = 0.00005, whose rule bends most sharply;
the page's caption says so. The restrained rule's dense points begin at its lowest income, m ≈ 0.80. Below its kink the page draws
it from the results file's kink record, slope 1, and its common points. The gap is drawn to m = 2.94, the end of the
shortest rule's points.

## What it establishes, and what it does not

- **The limit holds in HARK's solution, at every level.** The natural rules converge to the restrained rule as ℘ falls,
  as BST's proposition states. The gap is largest at the kink the natural rules smooth.
- **The gap is a property of the model, not of the numerics.** It changes by about 10⁻³ of itself across the three
  levels.
- **The convergence is slow:** a factor of about 2.3 per decade of ℘. At ℘ = 0.00005 the rule is still 0.027 below the
  restrained one at the kink.
- **What it is not:** one toolkit. It is the suite's first record, not yet a comparison across toolkits.

## Pending

- The other toolkits' runs on the same request files. dolo's followed the same evening and agrees with this one
  (`../2026-11-01_restrained-limit-suite-dolo/README.md`), where the page's version 2, with both toolkits, is built.
- A smaller fourth rung, if the owner wants the last gap smaller (deferred follow-ups).
