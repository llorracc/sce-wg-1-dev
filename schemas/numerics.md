# Numerical methods: methods, settings and suites

Draft; see the [README](README.md).

A parameter file states a model and holds nothing numerical. A toolkit's numerics go in three other kinds of file, each
with its own schema. The split exists so that one method can be fixed and run under many settings. For instance, a whole
set of grid sizes and grid placements can run in parallel, and the suite of results then shows how each reported
quantity depends on each numerical choice.

## What the schemas prescribe, and what they do not

The schemas state the problem and nothing about how it is solved. A method file and a settings file are a toolkit's own
record of what it did, stated so that a results file can be identified and so that a suite can show how each quantity
converges; nothing in them is prescribed by the schemas, neither a discretization of a law, nor a grid, nor a
quadrature, nor a form for any of them. What a toolkit must do is solve the problem it is handed and report, in the
results file, what it solved: the expectations the family names, evaluated under its own approximation of the laws;
every condition of the family's table, decided on that approximation; and the derived parameters it used. That
approximation is the toolkit's **effective member** ([`effective-member.md`](effective-member.md)); the schemas never
see its representation.

Two kinds of setting, as descriptions and not as requirements. A **model-changing** setting alters the effective member:
the number and placement of a shock's nodes, a truncation, the discretization of a level law. A **method-only** setting
alters only how the effective member's solution is approximated: the asset grid, the interpolation, the solver's
tolerance, the histogram of the stationary population, a simulation's sample size. Along a ladder the first kind
converges in the reported expectations and the second in the solution, and a suite's report reads the two separately.
The method on `diagnostics.expectation` states its own precision in the results file, since the diagnostics are computed
against the stated member's law.

## Method file

A method file chooses, for each part of the model, the algorithm that computes it. A part is named by the family's stage
file's own target, as Bellman's methods files name it: a block's id such as `policy`, a line's id such as
`cntn_to_dcsn.value`, or an operator's name such as `E_ψ_θ_j`, which covers every occurrence. A method attaches only
where the stage gives the computation a place of its own: an expectation's method goes on its operator, not on the block
or the line that holds it. Each target takes one method, and two entries on one target are an error. The family's model
schema lists its targets with a comment on each ([`bst/1`](bst-1/model.md#method-targets)); two parts the stage cannot
name, the stationary population and the diagnostics' expectation, keep names of the schema's own.

The file holds **no values**. Each method it names is defined in a **method registry**. The registry declares the
method's contract and **the settings it reads**: each setting's name, type, allowed range and meaning.

```yaml
methods:
  - on: policy.euler.solve        # the choice of c: the root of the Euler line
    method: "!time-iteration"
    handler: endogenous-grid      # the step that solves it, which the stage does not write
  - on: policy                    # the rule between the points where it was computed
    method: "!Linear"
  - on: E_ψ_θ_j                   # the joint expectation over the shocks and the unemployment event, in both lines
    method: "!quadrature"
    handler: equiprobable-quantile-nodes   # where the nodes go, which the tag leaves open
  - on: cntn_to_dcsn.value        # the value, kept for population welfare
    method: value-function
  - on: population.distribution   # the stationary population; no stage target
    method: histogram
  - on: diagnostics.expectation   # the Euler residuals' expectation; no stage target
    method: gauss-legendre-on-support
```

**The value and welfare.** Population welfare needs the value function v, which a method such as the endogenous grid
method does not produce by itself. The target `cntn_to_dcsn.value` names how it is obtained: `value-function`, the
solver's own v, which the family's recursion defines; or `simulated-utility`, the discounted sum of
utility along simulated paths, which reads the simulation's agent count, periods and seed and carries a standard error.

**Covering several parts.** A method that does several parts at once, such as one that fuses the quadrature of a shock
with the expectation step, is one method. Its contract lists the parts it covers. The method file names it once and the
registry declares every setting those parts read.

**Shared and toolkit-specific names.** The registry has two parts:
- a shared part, whose names mean the same in every toolkit;
- names under a toolkit's prefix, such as `hark:`, which identify a method but promise no comparability.

**Tags and handlers.** Where a computation has a method tag, as Project Bellman's methods files write them, the method
of an entry on a stage target is that tag, quoted so that YAML does not read it as a tag of its own:
`"!time-iteration"`, `"!Linear"`, `"!quadrature"`, `"!monte-carlo"`, `"!histogram"`. A registry's name then goes in the
entry's `handler`, where it says what the tag leaves open: the endogenous grid step under time iteration, or the
placement of the nodes under a quadrature. A setting that the tag does not name is read through the handler. Where no
tag fits, as for keeping the value function and for the two parts with no stage target, the registry's name is the
method.

## Settings file

A settings file gives a value to every setting that the method file's methods declare, and to nothing else. Examples are
the number and placement of grid points, the nodes per shock, the tolerances, the number of simulated agents and
periods, the seed, and the histogram grid. A validator built from the method file and the registry checks it.

**Every setting is a plain number, string or list of them.** No setting is an expression in a parameter or in another
setting. Then the hash of a settings element identifies it completely. A value that a toolkit derives from the model is
recorded in the results file with its derivation; an example is a grid's upper bound stated as a multiple of the target.

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

A suite file names one method file and a set of settings elements, as an explicit list or as the product of value lists
over named settings. The other settings take one shared value.

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

Results from one suite share the first two hashes and differ in the third. Gathering them shows how each quantity
converges with each setting. A comparison of two toolkits takes its tolerances from that measured convergence, not from
fixed numbers.

Each hash is the SHA-256 of a canonical JSON serialization of the parsed file: keys sorted, no white space, and every
number written as the shortest decimal that reads back to the same double. So `0.10` and `0.1` hash alike, as do `1` and
`1.0`, while any change of value changes the hash. The files are written in a strict YAML subset, with no anchors,
aliases, tags, merge keys, repeated keys, booleans or infinities, so that the parsed values are unambiguous.

## Open points

- **The registry.** The shared registry is not written: which methods it holds, their contracts and their declared
  settings.
