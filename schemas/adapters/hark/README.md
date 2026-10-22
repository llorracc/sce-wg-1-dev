# HARK's adapter for `bst/1`

[`adapter.py`](adapter.py) solves a `bst/1` member with HARK and writes its results file. [`test_adapter.py`](test_adapter.py)
is its standing check and [`gate.py`](gate.py) the check a version passes before it is published.

## Running it

HARK is pinned to the commit of HARK's pull request #1858, from the fork that opened it:

```sh
PIN="econ-ark @ git+https://github.com/llorracc/HARK.git@03a2c7a11ebd430e0c54eaa2da7f0eb5ab3d7483"
uv run --with "$PIN" --with sympy --with jsonschema --with pyyaml --with scipy --with referencing \
    python schemas/adapters/hark/adapter.py schemas/bst-1/members/toy.yaml --out out --level 1
uv run --with jsonschema --with pyyaml --with scipy --with referencing \
    python schemas/checker/check.py schemas/bst-1/members/toy.yaml --verify-results out/results.json
```

`--level` is one of the precision levels 1 to 4 (`low`, `medium`, `high` for 1 to 3). `--request` uses a given request
file in place of the one the adapter generates from a level-1 solution. `--nodes` overrides the level's nodes per shock.
HARK's release 0.17.2 does not declare its dependency on sympy, hence `--with sympy`.

## How it solves a member

HARK solves a `bst/1` household with its `MarkovConsumerType` on the nonpersistent chain, which is how the
[Markov family](../../bst-markov_ui-and-agg/model.md) writes a `bst/1` member. The chain has two employment states,
employed and unemployed, and both rows of its matrix are (1 − ℘, ℘): unemployment with probability ℘ whatever the previous
state.
- **Income in each state.** Employed income is ψ times the employed draw scaled by (1 − ℘ξ_U)/(1 − ℘). Unemployed income is ψ
  times ξ_U, since ψ is drawn in both states.
- **The rest is common.** Return, growth and survival are the same in both states, and newborns start employed.
- **The nodes.** The laws are discretized by the adapter: equiprobable bins, each node the bin's exact conditional mean.
- **The same rule in both states.** The end-of-period value does not depend on the current state, so the two states' rules
  and values are the same function of m.

The adapter asserts three things after each solve:
- HARK solved with the adapter's chain and income process. HARK's constructors for both are switched off, since HARK
  otherwise rebuilds them from its defaults: the chain at construction and the income process on any update.
- The two states' rules and values agree to 1e-12 relative.
- The two states' lower limits are equal, and equal to the effective member's constraint in force.

The same machinery then solves the Markov family, whose chains differ only in the matrix and the incomes.

**Why the pin.** Released HARK interpolates each next state's expected marginal value on a grid starting at that state's
own natural limit and evaluates it on the current state's grid. When the states' worst incomes differ, as here, that adds an
interpolation error to the rule and a larger one to the value function. Pull request #1858 evaluates each next state's
expectation at the current state's points, as HARK's standard solver does. With it, the Markov rule equals the standard
consumer's on the same nodes to about 1e-15. The adapter re-pins to the first HARK release that includes it.

**What the adapter computes itself:**
- the conditions and statuses, through the checker's arithmetic on the effective member's expectations. HARK has no
  condition checks or targets for its Markov consumer.
- the stationary population: a lottery onto an asset grid with mortality and newborn replacement, and Harmenberg's
  income-neutral measure. HARK has no Markov transition matrix. Since the next state does not depend on the current one,
  end-of-period assets are the whole state.
- the Euler residuals, against a Gauss–Legendre quadrature of the stated laws.

## The gate

`gate.py` runs one member at one level and reports:
1. for each type, the largest relative difference between the Markov rule and HARK's standard consumer's on the same nodes,
   and between the two employment states' rules;
2. given a reference results file, the largest difference from it, number by number. It uses relative differences for
   numbers of size one or more and absolute ones for smaller numbers, by part of the file;
3. the checker's verdict on the adapter's file.

A version is published once the gate passes on the benchmark's ladder of results files: levels 1 and 2 for the three
members, and the toy's level 3. The reference files are the buffer-stock benchmark's emitter's, which are not public.
Steps 1 and 3 need no reference.

## Provenance

A results file's provenance carries the hardware as the architecture and the number of logical cores, the thread count,
the files' names, and the numerical libraries' versions. It carries no machine name, no operating-system string and no run
time.
