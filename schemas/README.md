# Schemas for dynamic economic models

Draft. This directory is an experiment in the `llorracc/sce-wg-1-dev` fork. None of it has been proposed to the working
group yet, and every part of it may change.

The aim is a canonical, exact definition of each model: a statement so complete that every valid solution method, given
unbounded computation, converges to the same solution as every other. The schemas say what the model is. They prescribe
no numerical method: grids, quadrature, tolerances and simulation sizes stay each toolkit's own choice, on one condition,
that the choice vanishes in the limit. A choice that survives it, such as a fixed set of nodes standing for a continuous
shock, changes the model; the schemas read it as a model-changing setting, and the results file reports the effective
member it produces. The schemas are tested by use: the adapters for HARK and dolo were written from the schemas and the
toolkits' documentation alone, and the harness checks whether what they compute converges to the stated member's
solution. The criterion is proposed to the working group's purpose documents in
[`../project-a/exact-definition.md`](../project-a/exact-definition.md).

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
- **Valid solution method:** a procedure that approximates a member's problem as stated and nothing else, every choice
  of its own refinable without bound. A toolkit at fixed settings is an approximation, not a method in this sense; its
  ladder, with its model-changing settings refined as well, is.
- **Exact definition:** a definition under which every valid solution method, given unbounded computation, converges to
  the same solution as every other. The families aim to be exact definitions of their members. A disagreement between
  two toolkits in the limit is a gap in the definition or a departure in one toolkit, and the toolkit's stone, read
  against the definition, says which.
- **Canonical definition:** the exact definition the working group fixes for a model: the hub to which every stone maps
  its toolkit.
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
- **Ladder:** one method file run under many settings elements, so that results show how each quantity converges.
  Called a suite until 2026-11-02.
- **Experiment:** what every toolkit is to do with some members, and what the results must show, stated in an
  experiment file ([`experiments.md`](experiments.md)). The restrained-limit experiment was
  called a test suite until 2026-11-02.
- **Harness:** the program that runs every toolkit on an experiment through its adapter, verifies the results files and
  evaluates the experiment's checks ([`harness.md`](harness.md), approved 2026-11-02; its runner is built in
  [`../harness/`](../harness/README.md), its comparator not yet).
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

The apparatus around the schemas, gathered on 2026-11-04 at the owner's request:

- **Toolkit:** a solution library that a stone and an adapter serve: HARK, dolo, QuantEcon's JAX code.
- **Rosetta Stone,** or **stone:** the document, one per toolkit, that says how the toolkit solves a family's members as
  the stage file states them: its lexicon, its handlers, its adapter's two legs, its departures
  ([`../rosetta/`](../rosetta/README.md)). Its **cards** are the lexicon's rows in a YAML file beside it, in the field names
  of Bellman's Rosetta registry. The family's statement is the **hub** and each toolkit a **spoke** mapped to the hub
  alone; no stone translates one toolkit into another.
- **Adapter:** the program, one per toolkit, that takes a parameter file, a request file, a level's name and a folder,
  and writes a results file with its method and settings files; the stone's mapping as code, and the harness's plug-in
  for the toolkit ([`../harness/adapters/`](../harness/adapters/README.md)). Its **encode** leg turns the member into the
  toolkit's arguments and its **decode** leg turns the toolkit's output into the results file.
- **The shared module:** the toolkit-neutral code the Python adapters share, `common.py`: it reads the member and the
  request, computes the reports from what an adapter hands it, and writes the files.
- **Scenario:** a family's borrowing-constraint case, natural or artificial, each with its own stage file.
- **Types:** a member's discount-factor types, each a β with a population share; **pooled** blocks are the types pooled
  by share.
- **Representation:** a toolkit's own approximation of the laws, as nodes or atoms, and of the stationary distribution,
  as a grid, a lottery, a sample or a density; what the effective member is solved on.
- **Population measure and income measure:** the stationary cross-section weighted by households, and weighted by
  permanent income, under which aggregate responses are means.
- **Comparison points:** the values of m in a request file at which the rule, its derivative, the Euler residuals and
  the distribution function are reported, and, since the ruling of 2026-11-04, a's own points for its distribution
  function; the **request rule** generates both from a **quick solution** of the member, a solve at the lowest level,
  and moves a point off a **genuine atom**, an atom of the stated member's distribution whose location the parameters
  fix.
- **Exported rule:** the rule at dense points of the toolkit's choosing, with the kink and the range, for a reader who
  computes what the results file does not report.
- **Coverage:** the results-file block that says how far a representation of the distribution reaches: a stated point,
  the mass at or above it, and what became of the mass sent beyond it, clipped, dropped or kept.
- **Level:** a named rung of a toolkit's ladder, the one input the harness passes that is not a parameter; `low`,
  `medium` and `high` today, with `coarse`, `default` and `fine` proposed on 2026-11-04 so that the middle rung is the
  toolkit's own default.
- **Toolkit registry:** `harness/toolkits.yaml`, one entry per toolkit naming its adapter, its stone and its
  environment.
- **Locked environment:** a `uv` project per toolkit whose lock file pins every dependency; the harness runs the adapter
  in it with `uv run --frozen`.
- **Runner:** the harness's program that expands an experiment into **jobs**, one per toolkit, member and level, runs
  them, verifies every results file and writes the **run folder** with its **manifest**, the record of every hash, the
  start stamp and each job's status.
- **Comparator:** the harness's program that evaluates an experiment's **checks**, each a comparison across members,
  toolkits or levels of one **quantity**, a path into the results file, under a metric and an expectation, and runs the
  experiment's report scripts. Planned, not built.
- **Reports:** the results-file quantities every run of an experiment must carry beyond what the schema requires.
- **Reference solution,** or **the reference:** the organizer's solve of a member to very high precision by the
  continuous methods, the standard every solution at default settings is compared to, by the ruling of 2026-11-04
  ([`reference-solution.md`](reference-solution.md)).
- **The continuous methods:** the **kink-split expectation**, next period's marginal value integrated against the
  shocks' continuous laws with the integral cut at the preimage of the kink; the cubic Hermite interpolation that
  expectation makes legal; the natural limit from the laws' infima; and the **continuous landing**, the transition's mass
  assigned to the distribution grid's cells by the laws' distribution functions rather than carried by atoms.
- **The bench:** the organizer's own numerical code, which is no toolkit: the diagnostics' quadrature for the Euler
  residual under the stated laws, the comparator, and the probe's reference solver. The word is borrowed from HAFiscal's
  benchmark package and means the working group's bench here.
- **Probe:** a measurement made in a scratch folder and recorded as a finding, for planning; not a run of record.
- **Run of record:** a run whose files are kept and cited as the measurement: made through the harness, or by a toolkit's
  session on the owner's word.
- **Finding:** the record of a measurement with its artifacts, a README with the commands and the numbers, what it
  establishes and what it does not, and its pending list.
- **Emitter:** HAFiscal's word for the program that assembles its results files; the results schema's `driver` field
  names it when a toolkit has more than one. The shared module is the emitter of this repository's adapters.
- **Gate:** HARK's adapter's acceptance check for a new HARK version, one member at one level against the committed
  results. **Stub adapter:** the harness tests' stand-in toolkit, which copies committed files and solves nothing.
- **Organizer and participant:** the organizer runs the comparison and holds the reference; a participant is a
  toolkit's author who submits a results file ([`participation.md`](participation.md)).
- **Registry:** three things, to be read by context: the toolkit registry above, the **method registry** of
  [`numerics.md`](numerics.md), and the **run registry** the owner asked for on 2026-11-04, every run of every toolkit
  with its provenance, its machine and its times, not yet designed.

## Contents

Shared by every family:
- [`shock-laws.md`](shock-laws.md): the shock laws a parameter file can use, and the two reserved for later.
- [`shock-laws.schema.json`](shock-laws.schema.json): their validator.
- [`conventions.md`](conventions.md): the registry of the names the validators fix, with the ontology chart each writes
  and the convention it follows or the reason it departs; the laws are charts of the
  [ontology of probability distributions](../ontologies/probability-distributions/).
- [`numerics.md`](numerics.md): method files, settings files and ladders.
- [`experiments.md`](experiments.md): the experiment file, which states what every toolkit is to do with some
  members and what the results must show; [`experiment.schema.json`](experiment.schema.json) is its validator, and
  restrained-limit is the first experiment.
- [`harness.md`](harness.md), a plan approved on 2026-11-02: the harness that runs every toolkit on every experiment, verifies the
  results files and evaluates the experiment's checks.
- [`../harness/`](../harness/README.md): the harness as built so far: the toolkit list, a locked environment for each
  toolkit, and the runner, which runs and verifies; the comparator is next.
- [`jacobians.md`](jacobians.md): the interface every toolkit follows for its sequence-space Jacobians when an
  experiment asks for them, approved on 2026-11-01: the results schema's key `jacobians`, which `checker/jacobians.py`
  verifies.
- [`../rosetta/`](../rosetta/README.md): the Rosetta Stones, one for each toolkit, which say how the toolkit solves a family's
  members as the stage file states them; begun for the buffer-stock families with HARK and QuantEcon's JAX code.
- [`../harness/adapters/`](../harness/adapters/README.md): the adapters, one for each toolkit, which read a parameter file, solve the member with
  the toolkit and write its results file; HARK's for the buffer-stock families first.
- [`for-toolkit-authors.md`](for-toolkit-authors.md), proposed on 2026-11-03 and sent to no one: the page a toolkit's
  author would receive: what the comparison is, what they receive and provide first, how a file is verified and reported,
  and what the later stages add.

The two buffer-stock families, one for each borrowing-constraint scenario that has a family
([`constraint-scenarios.md`](constraint-scenarios.md)), in [`bst/`](bst/). They replaced `bst/1` on 2026-11-01 together
with two more, which the owner abolished on 2026-11-03 as uninteresting cases.
- [`bst/model.md`](bst/model.md): the model schema the two share, read from their stage files, with the table of the
  families, their method targets and their parameter files.
- [`bst/conditions.md`](bst/conditions.md): the validity conditions, each scenario's among them, the domain rules, the
  implications a results file is tested against, and the conditions of the simulation phase, population welfare's among
  them.
- [`bst/results.md`](bst/results.md): the results schema the two share, with the stationary population, welfare and
  marginal welfare, and the diagnostics; [`bst/results.schema.json`](bst/results.schema.json) is its validator.
- [`bst/parameters.common.schema.json`](bst/parameters.common.schema.json): the parameter definitions the two share.
- One experiment for every toolkit's solution ([`bst/model.md`](bst/model.md)): the restrained-limit experiment, BST's
  liquidity-constrained solution as a limit, with three `bst-natural/1` members with BST's calibration and ℘ falling
  and the restrained consumer in `bst-artificial/1`. A second, on an estimated member, is with the HAFiscal-Latest
  repository since 2026-11-04 until it is ready.
- One folder for each family, each with its parameter file's validator (`parameters.schema.json`), its stage file in
  Bellman-SYM under `bellman/`, and its members under `members/`:
  - [`bst/natural/`](bst/natural/), `bst-natural/1`: the natural scenario with a point mass, BST's own model, with the
    community library's member and its calibration;
  - [`bst/artificial/`](bst/artificial/), `bst-artificial/1`, with the benchmark's toy.

  `bst-natural-no-point-mass/1` and `bst-zero-infima/1` stood in `bst/other/` from 2026-11-01 until 2026-11-03; their
  stage files, validators and members are in the repository's history.
- [`checker/`](checker/README.md): the checker, which validates and hashes a parameter file, checks its scenario's
  requirements, and evaluates the family's conditions, domain rules and implications.

The Markov family, `bst-markov_ui-and-agg`, is retired (2026-11-01). Its one-state unemployment model is a calibration
of the buffer-stock families, such as [`bst/artificial/members/toy.yaml`](bst/artificial/members/toy.yaml) with its
unemployment, and writing unemployment as a Markov state is a way to solve it, as HARK's adapter does. Its four-state version, with
HAFiscal's benefit countdown, regime, groups and splurge, and the paper's members written in it, are in the
repository's history.

Design notes:
- [`participation.md`](participation.md), proposed on 2026-11-03: how a toolkit takes part, measured against six families
  of intercomparison and interchange that lasted ([the precedents](records/findings/2026-11-03_precedents-for-the-apparatus.md)):
  the stages by name, what the organizer generates, what each component becomes, and the decisions it puts to the owner.
- [`comparing-solutions.md`](comparing-solutions.md), proposed on 2026-11-03: the lessons of the precedents, of Bellman
  and of the Matsya consultations for comparing alternative solutions of one member, and the design that follows:
  fidelity checked against the model, agreement reported and classed, the bench computing the diagnostics from each
  toolkit's exports, the method-only step as the tolerance's source; what it changes in each proposal. Superseded in
  part on 2026-11-04 by the note below.
- [`reference-solution.md`](reference-solution.md), proposed on 2026-11-04 on the owner's ruling of that morning: a
  reference solution of each member, solved to very high precision by the continuous methods of HAFiscal and HARK, with
  a wide dense grid and an ergodic distribution on a dense grid to the 99.9th percentile of wealth, is the standard;
  actual solutions at default settings are compared to it; the methods named with their sources, the grids, the
  certification, default settings per toolkit, the comparison as a report, who solves it, what changes in each
  proposal, and seven decisions.
- [`constraint-scenarios.md`](constraint-scenarios.md): approved on 2026-11-01: the four borrowing-constraint scenarios,
  each a family with its own stage file.
- [`foundation.md`](foundation.md): the plan for making the Bellman-SYM stage file the foundation of a family's statement,
  with the requests it implies for the language.
- [`effective-member.md`](effective-member.md): approved and executed on 2026-10-18: the schemas state the problem without
  specifying methods or forms; a toolkit approximates the laws as it sees fit, solves its own effective member, and reports
  the expectations the family names, every condition's factor and verdict decided on it, and the derived parameters it
  used, trusted to compute them in its own representation; the checker verifies what needs no representation and keeps
  the stated member's closed-form limits where the law admits them.
- The design note on HAFiscal's household models and the test suite over members moved to the HAFiscal-Latest
  repository on 2026-11-04 with the toy-hafiscal work ([the rulings](records/rulings/2026-11-04_architecture.md)).

Not yet written: the validators for the method, settings, ladder and request files; the method registry; and the checker's
reading of a results file's values against the request file's points. Its reading of a results file's report on the
effective member, the expectations, the factors, the verdicts, the statuses and the derived parameters, is written.
