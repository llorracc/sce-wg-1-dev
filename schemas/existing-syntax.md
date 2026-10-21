# Adopting existing syntax: a survey through Matsya, proposals, and standing checks

**Status: EXECUTED for the distribution class; ACTIVE for the other classes** (proposed and approved 2026-10-19).
- **How it ran.** This session gathered the material by 11:43 on 2026-10-19. Matsya's four sessions on the distribution
  ontology ran in the bellman session that afternoon and evening ([the findings](records/findings/2026-10-19_distribution-ontology-matsya.md)).
- **The rulings.** The owner ruled on the ontology's decisions below on the morning of 2026-10-20
  ([the rulings](records/rulings/2026-10-20_schema-decisions.md)). All were as recommended, with three exceptions:
  - Bellman-SYM's truncated lognormal is aligned with its truncated normal: `TruncatedLogNormal(μ, σ, l, u)`, with σ > 0.
  - The home is `ontologies/probability-distributions/`, under a top-level folder for the project's ontologies.
  - The name of the w3id.org namespace is left for later.

  The decision on Bellman's comparator is not among his answers.
- **What it produced.**
  - The ontology: draft pull request #1, into the fork's `main`.
  - The shock laws written on it, with the registry [`conventions.md`](conventions.md) and its standing check: draft pull
    request #2, into the schemas' branch. Its `conventions.md` links back here.
  - Bellman-SYM's side, the bellman session's, in Bellman's own repository.
- **What remains:** the survey's other classes, later: method names, settings, parameter-file keys and results-file names.

Draft; see the [README](README.md).

## Why

The schemas and the stage files have been coining names and spellings for objects that other packages already describe: a
truncated lognormal and how its bounds are written, a mixture and its components, a discrete law, an interpolation, a grid,
a quadrature rule, a solver's settings. Each coinage was made for a local reason, and each is one more thing a toolkit author
must learn and one more place where the schemas can disagree with the package the author already uses. The owner's direction
on 2026-10-19: wherever an existing syntax or approach describes the object, adopt it; and check every decision of this kind
against the existing ones, now and as a standing rule, for distributions, interpolation and the rest alike.

Two things are separated throughout. A **spelling** is a name or a parameterization: `TruncatedLogNormal`, `sd_log`, bounds
in standard deviations. A **convention** is a choice of meaning that a package may not offer at all: mean one after
truncation with the stated standard deviation of the log kept, one written form per law, no infinities in a file. A spelling
is adopted from the package that has it; a convention is kept where the schemas need it, and is then stated in the adopted
package's terms, so that a reader who knows the package can see what was added.

Two principles from the owner (2026-10-19). **Few sources:** the spellings are adopted from a small number of sources, chosen
by the survey, rather than gathered one object at a time from wherever each happens to be spelled; a proposal names its one
or two anchors, and a class whose anchor cannot express an object says so rather than borrowing from a third. **Two
coordinated pull requests:** what is adopted goes to Bellman and to this repository together, as two pull requests written
against one registry, so that every name, argument order and unit agrees and the converter copies numbers through; each
names its counterpart and neither merges without the other ready.

## The inventory of decisions under review

One row per class of decision. The last column names the existing syntaxes the survey compares with; the list is a starting
point, and the survey's first task is to complete it.

| class | where fixed | our spelling today | compared with |
|---|---|---|---|
| Continuous laws, their names and parameters | [`shock-laws.md`](shock-laws.md), its validator | `LogNormal{sd_log}`, `TruncatedLogNormal{sd_log, bot, top}`, `Uniform{half_width}`, `Degenerate{}` | scipy.stats (`lognorm(s, scale)`, `truncnorm(a, b, loc, scale)`, no truncated lognormal); R (`dlnorm(meanlog, sdlog)`, the `truncnorm` and `truncdist` packages); Stan (`lognormal(mu, sigma) T[L, U]`); PyMC (`LogNormal(mu, sigma)`, `Truncated(dist, lower, upper)`); TensorFlow Probability (`TruncatedNormal(loc, scale, low, high)`); Distributions.jl (`truncated(LogNormal(μ, σ), lower, upper)`); the SBML distributions package, UncertML and ProbOnto, which name distributions and their parameters as an ontology; BUGS and JAGS (`dlnorm(mu, tau)` with a precision); dolo's model files (`!Normal`, `!AR1`, `!MarkovChain`); Dynare's shocks block |
| Truncation: where the bounds are written and in what units | the same | `bot`, `top` in standard deviations of the normal before truncation; an omitted bound is three (ruled 2026-10-19); no infinity in a file | scipy's standardized `a, b`; Stan's `T[L, U]`, BUGS's `T(L, U)`, PyMC's and Distributions.jl's wrapper with bounds in the variable's own units; TensorFlow Probability's `low, high`; the SBML distributions package's trailing lower and upper bounds; Bellman-SYM's `inf` |
| Mixtures | the same | `NormalMixture{components: [{weight, mean_log, sd_log, bot, top}]}`, relative means with a common shift for mean one | PyMC (`Mixture(w, comp_dists)`), Distributions.jl (`MixtureModel`), Stan (`log_mix`), scipy (none), Bellman-SYM (`Mixture((f₁, J₁), …)`) |
| Discrete and tabulated laws | the same | `Discrete{values, probs}`; `Tabulated{points}` as a quantile table | scipy (`rv_discrete(values=(xk, pk))`, `rv_histogram`), Bellman-SYM (`Categorical`, point masses in `Mixture`), numpy (`choice(a, p)`), R (`sample(x, prob)`) |
| Bellman-SYM's families | Bellman's laws page | `N(μ, v)` with the variance; `LogNormal(μ, σ)`; `Mixture`, `Categorical`, `Bernoulli`, `DiscreteMarkov`, `MarkovChain`; positional arguments | the same packages; note that nearly every package takes a normal's standard deviation, not its variance |
| Methods | [`numerics.md`](numerics.md) | `endogenous-grid`, `linear-interpolation`, `equiprobable-quantile-nodes`, `value-function`, `histogram`, `gauss-legendre-on-support` | SED-ML and KiSAO, the COMBINE community's description of a simulation experiment and its ontology of algorithms and their parameters; dolo (its documentation names `Equiprobable` and `Gauss-Hermite Nodes` for the discretization of a law; `egm`, `time_iteration`, `value_iteration`, `tauchen`, `rouwenhorst` and `gauss_hermite_nodes` are in its source, not its pages, as the survey found on 2026-10-19); QuantEcon (`tauchen`, `rouwenhorst`, and the CompEcon quadrature names `qnwnorm`, `qnwlogn`, `qnwequi`); scipy's interpolators (`interp1d(kind=…)`, `CubicSpline`, `PchipInterpolator`, `Akima1DInterpolator`); EconForge's interpolation.py (`multilinear`, cubic splines) |
| Settings | the same | `grid_points`, `grid_max`, `grid_nesting`, `nodes_per_shock`, `euler_tolerance`, `histogram_points`; precision levels `low`, `medium`, `high` | dolo (`grid: {n, min, max}`); KiSAO's algorithm parameters; Dynare's `options_` |
| Parameter-file keys | [`bst/1`](bst-1/model.md)'s validator | `crra`, `return`, `survival`, `borrowing_constraint`, `income.growth`, `permanent_shock`, `employed_shock`, `unemployment.prob` | dolo's and Dynare's parameter blocks, SBML's parameter element, Bellman's stage-file names |
| Results-file names | [`bst/1`](bst-1/results.md)'s validator | the statistics (`gl`, `quantiles`, `mean_mpc`, `mpc_by_a_quartile`, …), the residuals, the statuses | SED-ML's outputs; the conditions keep BST's own names |

Out of the review: the math of the model, BST's notation in prose, and the conditions' names, which BST fixes. HARK is
excluded as a source, on the owner's ruling of 2026-10-19: it is a toolkit the schemas serve, not a standard they adopt;
where its spellings matter, they matter to its adapter.

## What Matsya is for, and what it is not

Matsya answers from the material a session supplies and from its own collections, and cites what it uses; what it cannot cite
it marks as deduction. That shape fits the survey: it can hold Bellman's own pages, which say what the grammar admits
today, and it can hold excerpts of the other packages' documentation if they are supplied. It cannot be the authority on
another package's syntax, since it has not read that package unless given the page. So the division of work is:

- **This session gathers the material**: for each package in the inventory, the official page that defines the syntax, read
  at its source, cut to the defining passage, with its address and the date read. The excerpts are kept outside the
  repository; the repository records the addresses. The gathering is checkable work and precedes every ask.
- **Matsya builds the overview and the proposals from that material**, in questions-only sessions, one per class, citing the
  excerpt for every claim about a package and Bellman's pages for every claim about the grammar.
- **This session weighs the answers** against the schemas' needs, as the standing rule requires, and drafts what goes to the
  owner; every cited syntax is checked once more against the package's page before it is adopted.
- **The owner rules**, class by class.

The practical limits, from the installed guide: a session's text stays under about eighty to a hundred thousand characters,
because every turn resends it, so each class gets its own session and the excerpts are cut short; a question is asked with
`ask`, one topic per turn, and never worded as "build" or "submit", which would start a job that writes files and needs the
owner's word; the service is plain HTTP and its sessions are exportable by its administrator, so only material fit to be
public is sent, which the inventory's material is. The collections can be searched without a language model and at no cost:
the literature and articles collections for how papers state truncated shocks and mixtures, the hark collection for HARK's
spellings, the repository collection for Bellman's.

The client and its token are the owner's, and the asks run on his word; a relayed word does not count for Matsya. The
bellman session runs the asks (ruled 2026-10-19), in the multi-agent mode the owner asked for, once the material is
gathered; it is on the truncated-lognormal branch today, whose family name, argument order and bound spelling now wait for
the distribution class.

## The sessions and their questions

Each session is given: the inventory row, our document for the class, Bellman's page for the class where there is one, and
the excerpts. The questions, in order, one per turn:

1. **The overview.** For this class, list every object our spelling names, and for each package in the material, the
   package's spelling of the same object: the name, the parameters and their order, the units of each, the defaults, how an
   absent bound or an infinite one is written, and what the package cannot express. Mark what the material does not say.
2. **The conventions.** Which of our conventions (mean one after truncation, the standard deviation of the log kept, one
   written form, no infinities, relative means in a mixture) does any package offer as such; which must be added on top of
   an adopted spelling; and how each would be stated in that package's terms.
3. **Three proposals**, each named for the standard it follows, each a complete spelling for the class in the parameter files
   and in Bellman-SYM, with what changes in the validator, the checker, the stage files, the converter and Bellman's package;
   what each one gains and loses against the constraints; and which of them Bellman's grammar admits today, which after the
   freeze, and which never without a grammar change.
4. **The check.** How a toolkit author or a test could tell, from the files alone, which standard a spelling follows: what a
   registry row needs, and what Bellman's laws page or methods page would need to carry.

Two further asks, once per survey rather than per class: whether SED-ML's split of model, algorithm, algorithm parameters and
outputs maps onto the schemas' parameter, method, settings, suite and results files, and what its vocabulary offers the
numerics document; and whether an ontology of distributions (ProbOnto, UncertML) gives names and parameterizations that the
shock-law document could adopt wholesale, with the mean-one laws as named variants.

The classes run in the inventory's order, since the first one is already under construction in Bellman: the truncated
lognormal's family name, argument order and bound spelling are decisions this survey may change, so the distribution class
runs first and quickly. For the distribution classes the session is the ontology session described next, and its questions
replace the four above: the adequacy of each candidate ontology, with citations; the gaps; what fills them, written with
the semantics in Bellman's own measure-theoretic form; the mapping of each package's constructors, from the gathered
material, onto the result; and the spellings for the parameter files and the stage files that follow from it, with the
check that any spelling can be traced to the ontology.

## The ontology

At 10:54 on 2026-10-19 the owner directed a different center for the distribution classes: rather than choose among the
packages' spellings, ask Matsya to find online, or failing that to develop, a semantic ontology for the rigorous
description of probability distributions, with respect to which every package's distributions, and ours, are evaluated.
It is the probability-law part of the working group's own program: Project A's semantic ontologies have a written form, a
domain of meaning and the map between them, with SBML and the Systems Biology Ontology as the closest precedent
([`../project-a/semantic-ontology-precedents.md`](../project-a/semantic-ontology-precedents.md)), and SBML's distributions
package points to ProbOnto for the meaning of its laws. Here the parameter files and the stage files are the written form,
the ontology is the domain of meaning for laws, and Bellman's primitive definitions are the map for the stage files.
That makes the ontology the one source the few-sources principle asked for, and turns the package survey into the
ontology's evaluation set: each package's constructor is an instance to be mapped onto it, and a constructor that cannot
be mapped shows where the ontology, or the package, falls short.

What the ontology must give, in the schemas' and Bellman's terms:

- a distribution as a probability measure on a stated space, which is how Bellman's primitive definitions already define
  three of its families, `N`, `LogNormal` and `Mixture`: a map from the parameters to a measure, written as an integral
  (the four discrete families have no such definition yet, as Matsya's first session pointed out);
- a family as a named map from a parameter space to measures, with one canonical parameterization, and every other chart
  named, with its conversion formulas to the canonical one; this is what ProbOnto provides for the families it lists;
- the operators that build one law from another: truncation as conditioning on a set, censoring, the pushforward under a
  map such as the exponential or an affine shift, the finite mixture, the product of independent laws, the Markov kernel;
  so that a truncated lognormal is the pushforward under the exponential of a truncated normal, and a mixture in logs is
  the pushforward of a mixture, without a family coined for each composition;
- the properties a condition or a checker asks of a law: the support with its infimum, its supremum and the mass at the
  infimum; moments and log-moments; the domain conditions on the parameters; and the constraints that pin a parameter,
  mean one among them;
- the identity of two spellings as one measure, decided by conversion to the canonical chart, which is what one written
  form, the hash and Bellman's comparator need;
- a written form, in a parameter file and in a stage file, that names the ontology's family, chart and operators.

Candidates to find before anything is developed: ProbOnto, the ontology and knowledge base of probability distributions
with named parameterizations and re-parameterization formulas; UncertML's distribution dictionary; the SBML distributions
package's function list; the statistics ontologies STATO and OBCS; and, as de facto ontologies in code, the algebras of
distributions in R's distr family, MeasureTheory.jl and Distributions.jl's wrappers, TensorFlow Probability's transformed
distributions and bijectors, and the Leemis–McQueston chart of univariate distribution relationships.

**Where it stands.** Matsya reads no web page: it answers from its retrieval index (Bellman's documentation and stage files,
HARK, Buffer Stock Theory, a literature on dynamic programming and journal articles), from the session's text and from its
jobs' outputs. So the candidates were found from this session, at their official sources, and quoted verbatim, with a
second reader verifying every package record, a critic naming what was missing, and two digests cut to a Matsya session's
size: the requirements with the gaps no source fills, and the fourteen candidates against a twelve-item checklist. That is
material only. The evaluation and the design are Matsya's, in four questions-only sessions run by the bellman session on
the owner's word there: the adequacy of the ontologies; the operator layer; the design, aligned to ProbOnto's identifiers
where ProbOnto has the family; the mapping of each package's constructors and the written forms. The first two ran on the
afternoon of 2026-10-19. That evening the owner dropped the planned multi-agent checking of the answers, the material
having been verified against its sources here and the service accepting no citation it cannot find in a session's
material; the last two sessions run from the bellman session through the client, and the weighing of all four is this
session's ([the findings](records/findings/2026-10-19_distribution-ontology-matsya.md)). The substitution of this session's gathering for Matsya's "find
online" was not put to the owner first, and should have been.

**The pull requests.** After the owner's rulings on the design, two pull requests written against it, each naming the
other: to Bellman, the law families aligned to the ontology, their terms and charts on the laws page, the operators, the
comparator deciding identity by the canonical chart, and the truncated-lognormal branch re-spelled; to this repository,
the ontology's files and document, the shock-law document and validator written on it, the checker's laws as its
operators, the converter to Bellman's spelling, the registry and its standing check. A shared test holds them together:
every law of every member converts to a Bellman call that elaborates at the Bellman pull request's head and resolves to
the same ontology term and the same canonical parameters. Where the ontology lives is a decision for the owner; Bellman's
repository is private and this one is public, so a public home lets the working group's other ontologies, and ProbOnto,
cite it.

## The ontology: decisions for the owner

From Matsya's four sessions and their weighing ([the findings](records/findings/2026-10-19_distribution-ontology-matsya.md)),
put to the owner on the evening of 2026-10-19, each with a recommendation.

1. **The core of the design.** The six kinds (measure, family, chart, operator, property, constraint); three operators
   (pushforward, conditioning on a set, product with a kernel), with the affine map, the mixture, the independent product
   and the Markov kernel as their cases; a catalog of nine base families and three named compositions; the identity rule
   (fill the defaults, normalize the composition, convert to the canonical chart, compare); and the three settlements: a
   pinned mean is a constraint defining a subfamily whose reduced parameterization is its chart, the relative means of a
   mixture restrict the chart so that each law has one spelling, and the point mass is a family of its own whose
   boundary spellings (`LogNormal(μ, 0)`, `Degenerate`) are its charts. *Recommended: adopt.*
2. **No bound on one side, in a parameter file.** `null`, the spelling Distributions.jl, PyMC and NumPyro use for no bound;
   an omitted key keeps meaning three; both `null` refused, that law being `LogNormal`; the hash over the filled form with
   `null` kept. A stage file writes `inf`. *Recommended: `null`.*
3. **The mixtures.** Two shock laws, as the owner asked: `LogNormalMixture`, with untruncated components, and
   `TruncatedLogNormalMixture`, whose components are truncated (omitted bound three, `null` none); each defined in the
   ontology as the exponential of a shifted `NormalMixture` or `TruncatedNormalMixture` in logs. Components are written by
   the mean of their logarithm, relative, with mean one pinned once on the whole mixture; a lone truncated law by the mean
   of its draw. The schemas' present `NormalMixture` key is renamed, since elsewhere that name means a mixture of normals.
   *Recommended: adopt.*
4. **The stage file's truncated lognormal.** The branch's family `TruncatedLogNormal(σ, bot, top, m)`, the operators
   absorbed into its definition (the only form the grammar admits), registered in the ontology as a named composition with
   its own identifier; truncated mixture components in Bellman stay later, as ruled that morning. *Recommended: keep the
   name and order: ProbOnto's naming (`TruncatedNormal`, `LogNormal`) and the parameter file's chart with the mean
   appended.*
5. **The ontology's home.** Matsya recommends a public repository of its own. *Recommended instead: a top-level
   `ontology/` directory in this repository, with its own version, changelog and tags, apart from `schemas/`, split into a
   repository of its own, history kept, once it has consumers beyond these two.*
6. **Its form.** One YAML source file per family and operator, generating OWL 2 in Turtle (the language the working
   group's own deck takes for ontologies) and JSON tables for the validator and Bellman; opaque permanent identifiers under
   a w3id.org namespace, whose registration is a request to that public project; CC BY 4.0, with ProbOnto attributed for
   what is copied. *Recommended: adopt; the namespace's name is the owner's.*
7. **Cross-references to ProbOnto.** `skos:exactMatch` for the same chart of the same family, `skos:closeMatch` otherwise,
   not `owl:sameAs`. *Recommended: adopt.*
8. **The hash.** It binds the schema's version only: defaults belong to the written form and no conversion formula
   touches the hash. *Recommended: adopt.*
9. **Bellman's family table.** Checked against the ontology's JSON table at a pinned release by a test in Bellman, beside
   the two tests that already read that table, rather than generated from it. *Recommended: checked.*
10. **The catalog's scope.** What the schemas and Bellman need now; the packages' other families (gamma, Weibull, beta and
    the rest) recorded as outside the catalog in the evaluation, and added when a model needs them. *Recommended: adopt.*
11. **The tolerance for irrational conversions.** One relative tolerance, 10⁻¹², the checker's precision for closed forms;
    never applied to the hash. *Recommended: adopt.*
12. **The pull requests, after the rulings.**
    - To this repository's `main`: the `ontology/` directory, self-contained, since `main` has no `schemas/`: the sources,
      the generator, the OWL and JSON files, the tests (rows complete, conversions round-tripping, means against
      quadrature, generated files matching the source), a README holding the design, a changelog and a license.
    - Into the schemas' branch: the shock-law document and validator rewritten on the ontology (identifiers, charts,
      `null`, the default of three, the two mixture keys), the checker's laws as compositions, the converter, the registry
      `conventions.md` with its standing check, and the hash test over the filled form.
    - To Bellman, by the bellman session, through Bellman's amendment process and its maintainer's review: the
      truncated-lognormal branch with the rulings applied; each family's ontology identifier and chart recorded in the
      package's family table, which the laws page's generated table then prints (a hand edit of that table would be
      overwritten); a test of the family table against the ontology's; and optionally the measure definitions of the four
      discrete families, which the ontology supplies in any case. Deciding the support condition for the other families
      could ride in the same amendment.
    - Holding them together: every law of every member converts to a Bellman call that elaborates at the Bellman pull
      request's head and resolves to the same ontology identifier and canonical parameters.

Four more, raised by the bellman session from Bellman's side:

13. **How a stage file carries the mixtures.** Bellman's `Mixture` has no common shift, no relative-means normalization and
    no truncated normal, and its grammar writes no Φ, so the parameter file's mixtures reach a stage file only as numbers
    computed outside it: each component's draw mean, or each location with the shift folded in. Either the converter
    writes those numbers into the calibration, as it already writes the natural borrowing limit, or Bellman gains a family
    for a mixture in logs with a common shift. *Recommended: the converter now; the family later, with the derived
    parameters already requested of Bellman.* No member uses a mixture yet.
14. **Where an ontology release enters Bellman.** Bellman's tests read no network, so the test of item 9 needs a copy of
    the ontology's JSON table in Bellman's repository, with the release's version and digest; and the version can enter
    each stage's encoding, changing every recorded encoding at each release, or stay a constant of the test.
    *Recommended: a vendored copy, the version a constant of the test.*
15. **A zero spread in Bellman's truncated lognormal.** The branch admits `TruncatedLogNormal(0, bot, top, m)` as the point
    mass at m, as `LogNormal(μ, 0)` is admitted; Bellman has no rule of one spelling per law, and the identity rule maps
    both to the point mass, while the schemas keep a positive spread. *Recommended: keep admitting it.*
16. **Bellman's comparator.** It identifies two laws numerically today, at quadrature nodes per family. *Recommended: the
    identity rule of item 1, with the tolerance of item 11, wherever both laws resolve to rows of the ontology; the numerical
    comparison for laws outside it.*

## What comes out

1. **The overview**, as a findings record in [`records/findings/`](records/findings/): the matrix by class and package, with
   the address of every page cited, and what no package offers.
2. **The proposals**, as a section of this plan per class, three each, with the weighing and a recommendation, for the owner's
   ruling; a ruling is recorded in that day's rulings record and the spelling it chooses is applied to the documents, the
   validators, the checker, the stage files and, through the bellman session, to Bellman's package.
3. **The registry**, `conventions.md` in this directory: one row per spelling in the validators, the numerics document and
   the stage files, naming the package and object it follows, or the reason it departs, with the page cited. It is the
   standing check's data.
4. **The standing checks.**
   - In the checker: a test that every family name, law parameter, method name, setting name and parameter-file key the
     validators and the numerics document fix has a registry row, so that a coinage cannot enter without a row saying what
     it follows.
   - In the process: a proposal for any new name carries its registry row, and the rulings record says which standard was
     adopted or why none was; the README's vocabulary section points to the registry.
   - In Bellman-SYM, as a request to its maintainer through the bellman session: each family's row on the laws page and each
     method's on the methods page names the convention it follows and the packages that share it, the variance of `N` being
     the first thing to say; and the amendment that adds a family or a method asks the question before the signature is
     fixed. Matsya's own configuration gains a page saying the same, so that a job's writer prefers the adopted spellings.

## What this holds back

- The three sub-decisions on truncation put to the owner on 2026-10-19 (one-sided bounds as `null`, the hash over the filled
  form, the mixture's components as building blocks in logs) are not applied; the distribution class's survey subsumes them,
  and its first proposal should include them as the local alternative. The owner's ruling that an omitted bound means three
  standard deviations stands as a convention, and is stated in whatever spelling is adopted.
- The truncated-lognormal pull request to Bellman continues on its branch for everything that no spelling changes: the
  closed forms, the mean-one location, the support, the conditions, the tests and the dossier. Its family name, argument
  order and bound spelling wait for the distribution class's ruling, which is why that class runs first.

## Decisions taken (the owner, 2026-10-19)

1. The inventory is the scope, with HARK excluded as a source.
2. The pull request's signature waits for the distribution class.
3. The bellman session runs the asks, and uses the multi-agent mode for its part.
4. The material gathering starts at once, from this session, in the multi-agent mode: one agent per group of sources reads
   the official pages and writes the excerpts verbatim with their addresses, a second re-reads every page to refute or
   confirm each claim, and a last one says what is missing and which few sources could anchor each class.
