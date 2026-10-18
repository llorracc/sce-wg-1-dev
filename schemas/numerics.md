# Numerical methods: methods, settings and suites

Draft; see the [README](README.md).

A parameter file states a model and holds nothing numerical. A toolkit's numerics go in three other kinds of file, each with
its own schema. The split exists so that one method can be fixed and run under many settings. For instance, a whole set of grid
sizes and grid placements can run in parallel, and the suite of results then shows how each reported quantity depends on each
numerical choice.

## Method file

A method file chooses, for each part of the model, the algorithm that computes it. A part is named:
- by an address that the family's model schema publishes, such as `household.expectation.permanent_shock` in
  [`bst/1`](bst-1/model.md#addressable-parts);
- or by a kind, such as `expectation`, which covers every part of that kind.

An entry for a named part overrides an entry for its kind.

The file holds **no values**. Each method it names is defined in a **method registry**. The registry declares the method's
contract and **the settings it reads**: each setting's name, type, allowed range and meaning.

```yaml
methods:
  - on: expectation
    method: equiprobable-quantile-nodes
  - on: household.expectation.transitory_shock
    method: gauss-hermite-with-unemployment-atom
  - on: household.choice
    method: endogenous-grid
  - on: household.rule
    method: linear-interpolation
  - on: population.distribution
    method: histogram
  - on: diagnostics.expectation
    method: gauss-legendre-on-support
```

**Covering several parts.** A method that does several parts at once, such as one that fuses the quadrature of a shock with
the expectation step, is one method. Its contract lists the parts it covers. The method file names it once and the registry
declares every setting those parts read.

**Shared and toolkit-specific names.** The registry has two parts:
- a shared part, whose names mean the same in every toolkit;
- names under a toolkit's prefix, such as `hark:`, which identify a method but promise no comparability.

## Settings file

A settings file gives a value to every setting that the method file's methods declare, and to nothing else. Examples are the
number and placement of grid points, the nodes per shock, the tolerances, the number of simulated agents and periods, the seed,
and the histogram grid. A validator built from the method file and the registry checks it.

**Every setting is a plain number, string or list of them.** No setting is an expression in a parameter or in another setting.
Then the hash of a settings element identifies it completely. A value that a toolkit derives from the model is recorded in the
results file with its derivation; an example is a grid's upper bound stated as a multiple of the target.

```yaml
settings:
  grid_points: 200
  grid_max: 40.0
  grid_nesting: 3
  nodes_per_shock: 7
  euler_tolerance: 1.0e-10
  histogram_points: 2000
```

## Suite file

A suite file names one method file and a set of settings elements, as an explicit list or as the product of value lists over
named settings. The other settings take one shared value.

```yaml
method_file: methods.yaml
fixed: {grid_max: 40.0, grid_nesting: 3, euler_tolerance: 1.0e-10, histogram_points: 2000}
product:
  grid_points: [50, 100, 200, 400]
  nodes_per_shock: [5, 7, 11]
named:
  low: {grid_points: 50, nodes_per_shock: 5}
  medium: {grid_points: 200, nodes_per_shock: 7}
  high: {grid_points: 400, nodes_per_shock: 11}
```

- Each element is one independent run, so a suite runs in parallel.
- The optional precision levels `low`, `medium` and `high` are named elements.
- The element's hash is taken over its resolved values, the fixed values merged with the element's own.

## How the pieces are identified

A results file records:
- the parameter file's hash (the model);
- the method file's hash;
- the settings element's hash;
- the request file's hash (the comparison points).

Results from one suite share the first two hashes and differ in the third. Gathering them shows how each quantity converges
with each setting. A comparison of two toolkits takes its tolerances from that measured convergence, not from fixed numbers.

## Open points

- **The registry.** The shared registry is not written: which methods it holds, their contracts and their declared settings.
- **The canonical form for hashing.** It has yet to be fixed. A strong candidate is canonical JSON over the parsed values, with
  each number in its exact binary form, so that `0.10` and `0.1` hash alike.
