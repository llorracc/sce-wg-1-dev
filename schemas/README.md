# Schemas for dynamic economic models

Draft. This directory is an experiment in the `llorracc/sce-wg-1-dev` fork. None of it has been proposed to the working
group yet, and every part of it may change.

The aim is to state a model so completely that any bug-free toolkit, given enough computation, converges to the same
solution as every other. The schemas say what the model is. They prescribe no numerical method: grids, quadrature,
tolerances and simulation sizes stay each toolkit's own choice.

## Vocabulary

The names the validators fix, and the conventions they follow, are registered in [`conventions.md`](conventions.md).

- **Family:** a versioned template of models with named parameters and one stage file, such as `bst-artificial/1`
  ("buffer-stock theory with an artificial borrowing constraint, version 1"). The buffer-stock families are one for each
  borrowing-constraint scenario ([`constraint-scenarios.md`](constraint-scenarios.md)).
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
  ([`bst/model.md`](bst/model.md#method-targets)).
- **Handler:** the routine a method entry names, which carries out what the entry's method tag leaves open, or a part
  no tag names.
- **Observation map:** a stated transformation from the standard rule to what a household does, such as HAFiscal's splurge,
  kept outside the household's problem.
- **Level law:** a law of a quantity in levels, such as a newborn's permanent income, as against a mean-one shock law.
- **Regime:** an aggregate Markov state of the household's chain, such as normal times or a recession.
- **The floor of a law:** how a law behaves at the lowest value of its support, an atom, a positive density or a thin density,
  which decides the lower tail of the stationary distribution and whether welfare means are finite.
- **Semantic ontology:** in the working group's Project A, a model's meaning stated apart from any code: what exists
  (the ontology), what stands for what (the denotation), and what is written down (the syntax), with when the reading
  holds. The schemas are the syntax of the [ontology of buffer-stock models](../ontologies/buffer-stock-models/), which
  states the model class the families write.
- **Model class:** a class of models defined by membership axioms, such as `buffer-stock-model`; a family writes members
  of one or more classes.
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
  members as the stage file states them; begun for the buffer-stock families with HARK and QuantEcon's JAX code.
- [`adapters/`](adapters/README.md): the adapters, one for each toolkit, which read a parameter file, solve the member with
  the toolkit and write its results file; HARK's for the buffer-stock families first.

The four buffer-stock families, which replaced `bst/1` on 2026-11-01, one for each borrowing-constraint scenario
([`constraint-scenarios.md`](constraint-scenarios.md)), in [`bst/`](bst/):
- [`bst/model.md`](bst/model.md): the model schema the four share, read from their stage files, with the table of the
  families, their method targets and their parameter files.
- [`bst/conditions.md`](bst/conditions.md): the validity conditions, each scenario's among them, the domain rules, the
  implications a results file is tested against, and the conditions of the simulation phase, population welfare's among
  them.
- [`bst/results.md`](bst/results.md): the results schema the four share, with the stationary population, welfare and
  marginal welfare, and the diagnostics; [`bst/results.schema.json`](bst/results.schema.json) is its validator.
- [`bst/parameters.common.schema.json`](bst/parameters.common.schema.json): the parameter definitions the four share.
- One folder for each family, each with its parameter file's validator (`parameters.schema.json`), its stage file in
  Bellman-SYM under `bellman/`, and its members under `members/`:
  - [`bst/natural/`](bst/natural/), `bst-natural/1`: the natural scenario with a point mass, BST's own model, with the
    community library's member and its calibration;
  - [`bst/natural-no-point-mass/`](bst/natural-no-point-mass/), `bst-natural-no-point-mass/1`;
  - [`bst/artificial/`](bst/artificial/), `bst-artificial/1`, with the benchmark's toy;
  - [`bst/zero-infima/`](bst/zero-infima/), `bst-zero-infima/1`, with the untruncated toy.
- [`checker/`](checker/README.md): the checker, which validates and hashes a parameter file, checks its scenario's
  requirements, and evaluates the family's conditions, domain rules and implications.

The Markov family, HAFiscal's household problem, begun stage-file first, in two versions since 2026-11-01:
`bst-markov_ui-and-agg-artificial/1` and `bst-markov_ui-and-agg-zero-infima/1`, in
[`bst-markov_ui-and-agg/`](bst-markov_ui-and-agg/):
- each version's folder, [`artificial/`](bst-markov_ui-and-agg/artificial/) and
  [`zero-infima/`](bst-markov_ui-and-agg/zero-infima/), holds its parameter file's validator, its stage file and its
  members. The zero-infima version's stage file has three calibration files for the dropout group's middle type, one per
  value of the switch for permanent income while unemployed (`continues`, the family's standard; `grows`; `frozen`);
- [`bst-markov_ui-and-agg/model.md`](bst-markov_ui-and-agg/model.md): the model schema, read from the stage files, with the
  groups, the newborn's level law, the splurge as an observation map, the regime, the parameter file and the reduction to
  the buffer-stock families;
- [`bst-markov_ui-and-agg/conditions.md`](bst-markov_ui-and-agg/conditions.md): the buffer-stock families' conditions
  carried over to the chain, each as a condition on a matrix over the states that reduces to theirs under `continues`;
  the natural borrowing constraint by state; the levels' tail exponent; the employment marginal that born-employed
  newborns imply;
- [`bst-markov_ui-and-agg/parameters.common.schema.json`](bst-markov_ui-and-agg/parameters.common.schema.json): the
  definitions the two versions share. The members are the benchmark's toy written in the family (artificial), and the
  paper's high-school group alone and its published calibration (zero-infima, by their stated lognormal laws). The
  checker's module for the family, `checker/markov.py`, computes the stated member's conditions, limits and
  implications. Its results schema is not yet written; the design is in the note below.

Design notes:
- [`constraint-scenarios.md`](constraint-scenarios.md): approved on 2026-11-01: the four borrowing-constraint scenarios,
  each a family with its own stage file.
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
