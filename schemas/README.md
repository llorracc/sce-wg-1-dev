# Schemas for dynamic economic models

Draft. This directory is an experiment in the `llorracc/sce-wg-1-dev` fork. None of it has been proposed to the working
group yet, and every part of it may change.

The aim is to state a model so completely that any bug-free toolkit, given enough computation, converges to the same
solution as every other. The schemas say what the model is. They prescribe no numerical method: grids, quadrature,
tolerances and simulation sizes stay each toolkit's own choice.

## Vocabulary

The names the validators fix, and the conventions they follow, are registered in [`conventions.md`](conventions.md).

- **Family:** a versioned template of models with named parameters, such as `bst/1` ("buffer-stock theory, version 1").
- **Member:** one complete parameterization of a family.
- **Stated member:** the member a parameter file names, with its laws as stated. In general what can be computed about it
  is a limit, approached numerically; for the laws the schemas admit, whose moments have closed forms, the checker computes
  it exactly.
- **Effective member:** the member a toolkit actually solves, with its own approximation of the laws in its own
  representation, which the schemas never see. They know it through the expectations the family names, the conditions
  decided on it, and the derived parameters it used, all reported in the results file ([`effective-member.md`](effective-member.md)).
- **Derived parameter:** a quantity the parameters determine that enters the model's statement, such as the natural
  borrowing limit or the employed-income scale; a toolkit uses its effective member's own and reports it.
- **Model-changing and method-only settings:** descriptions of a toolkit's settings, not requirements on them: the first
  alter its effective member, such as a shock's nodes or a truncation; the second alter only how the solution is
  approximated, such as a grid or a tolerance. The two converge in different things and are read separately.
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
- **Implication:** an exact consequence of a member's parameters that tests a solution, such as the limiting MPC or a tail
  exponent, computed for the stated member by the checker.
- **Method target:** the stage file's own name for a part a method attaches to: a block, a line, or an operator's name
  covering every occurrence. An expectation's method goes on its operator
  ([`bst-1/model.md`](bst-1/model.md#method-targets)).
- **Handler:** the routine a method entry names, which carries out what the entry's method tag leaves open, or a part
  no tag names.
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
- [`conventions.md`](conventions.md): the registry of the names the validators fix, with the ontology chart each writes
  and the convention it follows or the reason it departs; the laws are charts of the
  [ontology of probability distributions](../ontologies/probability-distributions/).
- [`numerics.md`](numerics.md): method files, settings files and suites.
- [`rosetta/`](rosetta/README.md): the Rosetta Stones, one for each toolkit, which say how the toolkit solves a family's
  members as the stage file states them; begun for `bst/1` with HARK and QuantEcon's JAX code.
- [`adapters/`](adapters/README.md): the adapters, one for each toolkit, which read a parameter file, solve the member with
  the toolkit and write its results file; HARK's for `bst/1` first.

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
  permanent income while unemployed (`continues`, the family's standard; `grows`; `frozen`).
- [`bst-markov_ui-and-agg/model.md`](bst-markov_ui-and-agg/model.md): the model schema, read from the stage file, with the
  groups, the newborn's level law, the splurge as an observation map, the regime, the parameter file and the reduction to
  `bst/1`.
- [`bst-markov_ui-and-agg/conditions.md`](bst-markov_ui-and-agg/conditions.md): `bst/1`'s conditions carried over to the
  chain, each as a condition on a matrix over the states that reduces to `bst/1`'s under `continues`; the natural borrowing
  constraint by state; the levels' tail exponent; the employment marginal that born-employed newborns imply.
- [`bst-markov_ui-and-agg/parameters.schema.json`](bst-markov_ui-and-agg/parameters.schema.json): the parameter file's
  validator, with the members under [`bst-markov_ui-and-agg/members/`](bst-markov_ui-and-agg/members/): `bst/1`'s toy
  written in the family, the paper's high-school group alone, and the paper's published calibration. The checker's
  module for the family, `checker/markov.py`, computes the stated member's conditions, limits and implications, and
  verifies a results file.
- [`bst-markov_ui-and-agg/results.md`](bst-markov_ui-and-agg/results.md): the results schema's first version, with what
  the paper uses: the rule and the constraint in force by state, the employment shares, household wealth by group and
  pooled, in ratios and in levels, and the paper's MPC;
  [`results.schema.json`](bst-markov_ui-and-agg/results.schema.json) is its validator.

Design notes:
- [`foundation.md`](foundation.md): the plan for making the Bellman-SYM stage file the foundation of a family's statement,
  with the requests it implies for the language.
- [`effective-member.md`](effective-member.md): approved and executed on 2026-10-18: the schemas state the problem without
  specifying methods or forms; a toolkit approximates the laws as it sees fit, solves its own effective member, and reports
  the expectations the family names, every condition's factor and verdict decided on it, and the derived parameters it
  used, trusted to compute them in its own representation; the checker verifies what needs no representation and keeps
  the stated member's closed-form limits where the law admits them.
- [`hafiscal-models-and-test-suite.md`](hafiscal-models-and-test-suite.md): how the schemas describe HAFiscal's household
  models, the family `bst-markov_ui-and-agg/1` they need, and the test suite over members, methods and settings.

Not yet written: the validators for the method, settings, suite and request files; the method registry; and the checker's
reading of a results file's values against the request file's points. Its reading of a results file's report on the
effective member, the expectations, the factors, the verdicts, the statuses and the derived parameters, is written.
