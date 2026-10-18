# Schemas for dynamic economic models

Draft. This directory is an experiment in the `llorracc/sce-wg-1-dev` fork. None of it has been proposed to the working
group yet, and every part of it may change.

The aim is to state a model so completely that any bug-free toolkit, given enough computation, converges to the same
solution as every other. The schemas say what the model is. They prescribe no numerical method: grids, quadrature,
tolerances and simulation sizes stay each toolkit's own choice.

## Vocabulary

- **Family:** a versioned template of models with named parameters, such as `bst/1` ("buffer-stock theory, version 1").
- **Member:** one complete parameterization of a family.
- **Model schema:** the document that states a family's math.
- **Parameter file:** a member written down, in YAML, to the parameter schema. Its hash, taken over a canonical
  serialization, identifies the model.
- **Results file:** what a toolkit returns, in JSON, to the results schema.
- **Shock law:** the probability distribution of one shock in a parameter file.
- **Validator:** a JSON Schema file that checks a parameter or results file's form.
- **Checker:** a program that checks what a validator cannot express, such as a law's mean or a regularity condition.
- **Addressable part:** a part of a family's model that a method can be attached to, such as the expectation over one shock.
  The model schema publishes the list.
- **Method file:** the algorithm chosen for each part of the model, with no numerical values.
- **Method registry:** the definitions of the methods, each with its contract and the settings it reads.
- **Settings file:** plain values for the settings that a method file's methods read.
- **Suite:** one method file run under many settings elements, so that results show how each quantity converges.
- **Request file:** the comparison points at which a results file reports, kept apart from the parameter file so that the
  model's hash does not change.
- **Validity condition:** a condition on the parameters that a member must meet to be accepted at all.
- **Domain rule:** a condition that decides whether a member defines one reported quantity. A quantity it does not define is
  reported as `undefined`.

## Contents

Shared by every family:
- [`shock-laws.md`](shock-laws.md): the shock laws a parameter file can use, and the two reserved for later.
- [`shock-laws.schema.json`](shock-laws.schema.json): their validator.
- [`numerics.md`](numerics.md): method files, settings files and suites.

The family `bst/1`:
- [`bst-1/model.md`](bst-1/model.md): the model schema, with its addressable parts and its parameter file.
- [`bst-1/regularity.md`](bst-1/regularity.md): the regularity conditions, the validity conditions and the domain rules.
- [`bst-1/results.md`](bst-1/results.md): the results schema, with the stationary population and the diagnostics.

Not yet written: the validators for the parameter, method, settings, suite and results files; the method registry; and the
checker.
