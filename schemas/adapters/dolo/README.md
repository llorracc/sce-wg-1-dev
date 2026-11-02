# dolo's adapter

It solves a member of a buffer-stock family with dolo's endogenous grid method and writes the results file. The Rosetta
Stone [`../../rosetta/dolo.md`](../../rosetta/dolo.md) sets out how the household is written for dolo and how dolo's
output is read back.

## Running it

dolo's release 0.4.9.20 needs Python below 3.12:

```sh
uv run --python 3.11 --with dolo==0.4.9.20 --with jsonschema --with pyyaml --with referencing \
    python schemas/adapters/dolo/adapter.py schemas/bst/artificial/members/toy.yaml --out out --level 1
uv run --with jsonschema --with pyyaml --with scipy --with referencing \
    python schemas/checker/check.py schemas/bst/artificial/members/toy.yaml --verify-results out/results.json
```

`--level` is one of the precision levels 1 to 4 (`low`, `medium` and `high` for 1 to 3). They are the same node counts
and savings grids as HARK's adapter's, so that the two toolkits solve the same effective member on the same grid.
`--request` uses a given request file of comparison points.

## How it solves a member

- **The model file.** For each type, the household normalized by permanent income is written as a dolo model, with
  EGM's four blocks and the complementarity 0 ≤ c ≤ m − a_min.
- **The nodes.** The laws' nodes are the adapters' own: equiprobable bins, each node its bin's exact conditional mean,
  with the unemployment atom. They are passed to `egm` as a `FiniteDistribution`, since dolo's model files cannot state
  a truncated law.
- **The savings grid** is HARK's multi-exponential grid at the level. It starts at a_min wherever the constraint can
  bind, and 10⁻⁶ above it under `bst-natural/1`, whose zero-income atom would make next period's consumption zero there.
- **The rule.** `egm` returns its rule as a cubic spline on the model's uniform grid of m, a point every 0.005. The
  spline rounds the kink and ripples just below it. The adapter reads the rule back as `egm`'s own iteration holds it:
  linear between the spline's node values, which are `egm`'s endogenous rule there, with the kink's point added from
  the Euler equation at a = a_min. The MPC is the slope of the segment.
- **The rest** comes from the code the adapters share ([`../common.py`](../common.py)), as for HARK: the population,
  the effective member, the conditions and statuses, the statistics and the residuals.
- **Welfare** is reported as not computed, since `egm` gives no value function.

## Tests

`test_adapter.py`, in the same environment with `--with pytest`:
- the restrained member at level 1 against HARK's committed results file: the rule within 5 · 10⁻⁴ for m ≤ 20, and the
  same kink and mass at the constraint;
- the toy and the library solved and verified by the checker;
- the restrained-limit experiment's convergence: each rung's largest gap to the restrained rule smaller than the last.
