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
- **Implication:** an exact consequence of a member's parameters, such as the limiting MPC or the natural borrowing
  constraint, that a results file is tested against.
- **Method target:** the stage file's own name for a part a method attaches to: a block, a block's line, or an operator's
  name covering every occurrence.
- **Observation map:** a stated transformation from the standard rule to what a household does, such as HAFiscal's splurge,
  kept outside the household's problem.
- **Level law:** a law of a quantity in levels, such as a newborn's permanent income, as against a mean-one shock law.
- **Regime:** an aggregate Markov state of the household's chain, such as normal times or a recession.
- **The floor of a law:** how a law behaves at the lowest value of its support, an atom, a positive density or a thin density,
  which decides the lower tail of the stationary distribution and whether welfare means are finite.
- **Records:** the project's own memory, rulings, journal, findings, deferred follow-ups and defects, under
  [`records/`](records/MEMORY.md), written for publication.

## Contents

Shared by every family:
- [`shock-laws.md`](shock-laws.md): the shock laws a parameter file can use, and the two reserved for later.
- [`shock-laws.schema.json`](shock-laws.schema.json): their validator.
- [`numerics.md`](numerics.md): method files, settings files and suites.

The family `bst/1`:
- [`bst-1/model.md`](bst-1/model.md): the model schema, read from the stage file, with its method targets and its parameter
  file.
- [`bst-1/conditions.md`](bst-1/conditions.md): the validity conditions, the domain rules, the implications a results file
  is tested against, and the conditions of the simulation phase, population welfare's among them.
- [`bst-1/bellman/buffer_stock.bl`](bst-1/bellman/buffer_stock.bl): the household's problem in Bellman-SYM, the foundation
  of the family's statement, with a calibration file for the community library's member.
- [`bst-1/results.md`](bst-1/results.md): the results schema, with the stationary population, welfare and marginal welfare,
  and the diagnostics; [`bst-1/results.schema.json`](bst-1/results.schema.json) is its validator.
- [`bst-1/parameters.schema.json`](bst-1/parameters.schema.json): the parameter file's validator, with the members under
  [`bst-1/members/`](bst-1/members/).
- [`checker/`](checker/README.md): the checker, which validates and hashes a parameter file and evaluates the family's
  conditions, domain rules and implications.

The family `bst-markov_ui-and-agg/1`, HAFiscal's household problem, begun stage-file first:
- [`bst-markov_ui-and-agg/bellman/bst_markov_ui.bl`](bst-markov_ui-and-agg/bellman/bst_markov_ui.bl): the household's
  problem in Bellman-SYM, with three calibration files for the dropout group's middle type, one per value of the switch for
  permanent income while unemployed (`continues`, the family's standard; `grows`; `frozen`). Its prose documents are not yet
  written; the design is in the note below.

Design notes:
- [`foundation.md`](foundation.md): the plan for making the Bellman-SYM stage file the foundation of a family's statement,
  with the requests it implies for the language.
- [`hafiscal-models-and-test-suite.md`](hafiscal-models-and-test-suite.md): how the schemas describe HAFiscal's household
  models, the family `bst-markov_ui-and-agg/1` they need, and the test suite over members, methods and settings.

Not yet written: the validators for the method, settings, suite and request files; the method registry; and the checker's
reading of a results file against a member's domain rules.
