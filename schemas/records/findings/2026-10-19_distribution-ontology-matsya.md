# Matsya on an ontology of probability distributions

**What ran.** On 2026-10-19, on the owner's word typed in the bellman session, that session put four questions-only
sessions to Matsya (asks, no job) on the material this session had gathered at the candidates' official sources: a digest
of the requirements and the gaps no source fills, and a digest of fourteen candidates (five ontologies and vocabularies,
nine algebras of distributions in code) against a twelve-item checklist, with the working group's own precedent, SBML and
the Systems Biology Ontology, for the first session. Sessions 1 and 2 ran in the afternoon, three turns each, every answer
citing between 2 and 13 passages, about 790 thousand input tokens on the service's key. Sessions 3 and 4 were started in
the evening. The answers are kept outside this repository; this record holds what they say and how they were weighed.

## Session 1: the candidate ontologies

- **No candidate serves as it stands, and one is worth extending.** ProbOnto is the only candidate whose content has the
  shape the requirements ask for: families with several named parameterizations and conversion formulas between them
  (seven of the lognormal, `LogNormal1` to `LogNormal7`; 107 reparameterization records). It gives nothing for a law as a
  measure, nothing composable for the operators, and only strings for the properties; it has been dormant since 2017, its
  OWL file covers the knowledge base only in part, and 16 of the 42 ordered pairs of lognormal charts have no conversion
  there. UncertML is archived; the SBML distributions package is a written form that cites ProbOnto, not an ontology;
  STATO and OBCS name families without parameterizations.
- **The recommended base:** an ontology of the project's own, with its own namespace and canonical labels, that copies
  ProbOnto's families, parameterizations and conversion formulas under its CC BY 4.0 license, audits and completes the
  conversions, and links each family and chart to its `PROB_k` identifier as a cross-reference; the measure layer written
  in Bellman-SYM's form; the operators, the structured properties and a normal form for identity as new work; the parameter
  files and the stage files citing the one ontology, as SBML's distributions package cites ProbOnto.
- **The conventions, in the candidates' terms:** the standard deviation of the log after truncation and bounds in standard
  deviations are charts of the truncated law; mean one after truncation and relative means with a common shift are
  constraints that pin parameters; the quantile table is a law of its own, the pushforward of the uniform on [0, 1] under
  its quantile function; an omitted bound meaning three is no part of an ontology but a default of the written form,
  resolved before the law is formed and before the hash. No candidate has a place for any of the six as the schemas state
  them.
- **A correction it made to the material:** Bellman-SYM's laws page gives a measure-valued definition for `N`, `LogNormal`
  and `Mixture` only, the four discrete families holding none; the plan had said "each". Corrected in
  [`existing-syntax.md`](../../existing-syntax.md).

## Session 2: the operator layer

- **What the algebras offer.** Five truncate an arbitrary law (R's distr, Distributions.jl, scipy's new random variables,
  Wolfram, OpenTURNS); TensorFlow Probability and EnvStats have truncation only as named families; every one takes the
  bounds in the variable's own units and reads an omitted bound as infinite. Censoring appears as the pushforward under the
  clamp (Wolfram, distr, Distributions.jl). Mixture weights come in four conventions: a probability vector, a categorical
  mixing law, nonnegative numbers renormalized, and unnormalized superposition. "Product" means the joint law of independent
  components in most, the law of a product of variables in distr. Only Wolfram, and scipy within a single-use limit, show
  truncation composed before a pushforward on a page read.
- **Three operators suffice:** the pushforward of a measure under a measurable map, conditioning on a set, and the product
  of a measure with a kernel. The affine map, the exponential, the clamp of censoring and the projection to a marginal are
  pushforwards; the independent product is the kernel product with a constant kernel; the finite mixture is the kernel
  product of a law on labels with the kernel sending each label to its component, followed by the projection; a Markov chain
  iterates the kernel product. Bellman-SYM's own definitions already have this shape: `N` and `LogNormal` integrate the
  standard normal density over the preimage of a set under z ↦ m + √v z and z ↦ exp(m + s z), and `Mixture` is a kernel
  product with counting measure.
- **Where the schemas' laws sit:** the truncated lognormal is exp∗ affine_{μ,s}∗ cond_{[bot, top]} N(0, 1), so bounds in
  standard deviations are bounds on the base normal, applied before the affine map, which is why the schemas' units fit the
  algebra although almost no package uses them; and since conditioning commutes with an injective pushforward, the two
  units convert exactly. The mixture in logs with a common shift is exp∗ shift_c∗ of a mixture of conditioned normals, by
  linearity also a mixture of truncated lognormals. The quantile table is Q∗ of Lebesgue measure on [0, 1].
- **The fit with Bellman-SYM's forward builder:** a law it can extend a measure by is a named family in its table, so a
  truncation and an exponential are absorbed into a family's definition, as `LogNormal`'s already absorbs the exponential;
  weights are a probability vector, refused otherwise, matching the schemas' rule against silent normalization; a point mass
  is a number inside a `Mixture`; and a bound has to live in a family's parameters, since a declared set does not truncate.

## The weighing

Checked here against the schemas' definitions and rulings; the math of every operator identity above was verified
(conditioning commutes with an injective pushforward since f⁻¹(f(A)) = A; a mixture is a kernel product marginalized; a
pushforward is linear in the measure).

- **Agreed:** ProbOnto as a copied vocabulary layer, with cross-references rather than dependence; the measure layer in
  Bellman's form; the three operators; the places of the truncated lognormal, the mixture in logs and the quantile table;
  the omitted bound as a default of the written form, which is how the owner's rulings on the default of three and on the
  hash over the filled form already treat it. The owner's request of the same morning, a truncated lognormal mixture built
  from a truncated normal mixture, is the algebra's exp∗ shift_c∗ M.
- **Pushed back, by a note added to the material for sessions 3 and 4:** the owner's rulings, which the material lacked (an
  omitted bound means three, which settles the conflict the answers leave open; one-sided truncation must stay expressible;
  the hash over the filled form; the mixtures he asked for); the units of a mixture component's bounds, which session 2
  wrote ambiguously (they apply to the standard normal before the component's affine map); and three questions for the
  design to settle one way: a pinned mean as a constraint or a chart, relative means as a restriction of the chart's domain
  or a property of the law, and Bellman's σ = 0 against the schemas' separate point mass.

## Session 3: the design

Five turns, ended at 19:47, with 20, 20, 20, 15 and 7 citations. The third was asked seventeen seconds before the note of
rulings and corrections was added, so it does not apply them; the fourth and fifth do.

- **The kinds.** A measure is the object; a family is a named map from a parameter space into measures, a kernel being a
  family one of whose arguments is a state or another shock; a chart re-coordinates a family's parameters and changes no
  measure; an operator maps measures to measures; a property maps a measure to a value; a constraint is a property set
  equal to or bounded by a value. A written law, in either file, is a point of one chart of one family-and-operator
  expression.
- **The catalog.** Nine base families (normal, lognormal, point mass, uniform, finite discrete law on real points,
  categorical, Bernoulli, finite Markov kernel, truncated normal) and three named compositions (truncated lognormal,
  finite mixture with the schemas' mixture in logs as its constrained case, quantile table), each with its set, its measure,
  one canonical chart and its named charts with conversions; aligned to ProbOnto for the normal, the lognormal, the
  truncated normal and the mixture, and "defined here" for the rest.
- **The operators.** Pushforward, conditioning, kernel product, with the affine map, the mixture, the independent product
  and the Markov kernel as named cases; censoring recorded as a derived map, since no schema law uses it.
- **The three questions put to it, settled one way:** a pinned mean is a constraint that defines a subfamily, and the
  reduced parameterization it induces is that subfamily's chart (the mean-one lognormal's σ ↦ (−σ²/2, σ) being one the
  language already writes); the relative means of a mixture restrict the chart's domain so that each law has one spelling,
  since shifting every mean and the common shift oppositely changes no measure; and the point mass is a family of its own,
  with `N(x, 0)`, `LogNormal(ln x, 0)` and a number inside a `Mixture` as its boundary charts, `Degenerate` as its
  constrained chart at one, and the schemas' positive-spread rule a restriction of the lognormal chart's domain that keeps
  one written form per law.
- **Properties and identity.** Every law has its support (infimum, supremum, mass at the infimum), its moments and
  log-moments with their orders of existence, its domain and its pinning constraints, each transformed by rule under the
  operators. Two spellings are one law when, after filling the defaults, reducing the operator expression to its normal
  form and converting to the canonical chart, their canonical parameters agree; the hash stays exact over the filled written
  form, and a tolerance enters only where a package's chart is converted in the evaluation.
- **Form and home.** One structured source file per family, from which OWL 2 in Turtle and flat tables for the two
  consumers are generated; opaque permanent identifiers in a namespace the project controls, ProbOnto's codes as
  cross-references (`skos:closeMatch` unless provably the same chart); versioned releases with a changelog saying whether a
  change alters a measure; a public home apart from both written forms, as SBML keeps its ontology apart; Bellman's private
  tables checked against or generated from the public release. It leaves nine decisions to the owner.

**Weighed.** The kinds, the catalog, the operators, the three settlements and the identity rule are agreed; the
settlements answer the three questions as this session would have. Four points are pushed back on or closed here:

1. **The location formula** the answers mark unresolved was a defect in the bellman session's description of its branch,
   which subtracted s²/2 twice; the schemas' μ = −ln E[exp(sZ) | bot ≤ Z ≤ top], with ln m added for a stated mean, is
   right, and the branch's symbolic definition, which had copied the error, was corrected the same evening (its numerical
   code had been right throughout).
2. **The hash and the ontology's version.** The fifth answer says the defaults that fill a written form belong to the
   ontology, and so has the hash bind an ontology release; its own third and fourth answers, and its reading of the SBML
   precedent, put the defaults in the written form. The latter is right: the hash is taken over the filled form in the
   schemas' one chart, which no conversion formula touches, so it binds the schema's version alone, which every parameter
   file already names. A revised conversion formula can then change no hash.
3. **The serialization.** The working group's own deck on semantic ontologies presents OWL 2 as the language ontologies
   are written in, with RDF graphs and SKOS vocabularies beside it, which answers the fifth answer's open question on what
   the group's other ontologies need.
4. **The mixture's components** in the third answer still apply the bounds to N(m_j, s_j²); the note's correction stands,
   and session 4 was asked to revise that answer.

## Session 4: the mapping and the spellings

Five turns, 19:51 to 20:03, with 12, 10, 18, 14 and 16 citations; the design, the note of rulings, the current spellings,
the shock-law document, the corrected description of the branch and the digests as its entries.

- **The mapping.** Every package instantiates the normal with at least one chart; eight condition (truncate), all in the
  variate's units with an omitted bound infinite; seven push forward, three of them by the affine map only; nine mix,
  three with unnormalized weights the design forbids. No package has the constrained charts, the standard deviation of the
  log after truncation, the default of three, the relative means or the quantile table; their families outside the catalog
  (gamma, Weibull, beta and others) cannot be mapped until the catalog extends to them.
- **The revision under the rulings.** An omitted bound fills to three and an explicit token, `null` as proposed, fills to
  infinity, both before the conditioning; not both `null`, that law being `LogNormal`; the hash over the filled form with
  the token kept; the mixture components corrected; the location settled; the three questions settled as session 3 had.
  On the chart: a lone truncated law is written by the mean of the draw (the schemas' mean one being its constrained case),
  a mixture component by the mean of its logarithm after truncation, relative, because the common shift pins the mixture's
  mean once and moves every component's draw mean, so a draw-mean coordinate of a component would be overwritten.
- **The written forms.** In a parameter file, one key naming the composition and a mapping of the chart's coordinates, no
  operator written. In a stage file, one family call after `~`, the operators absorbed into the family's definition: the
  mean-one lognormal and an untruncated lognormal mixture with the shift folded into each location are admitted today; the
  branch's `TruncatedLogNormal(σ, bot, top, m)` is admitted as the author's own family and simulates once the family enters
  the package's tables; a mixture of truncated components needs that change and an unverified rule on nested components;
  the design's operator notation needs a grammar change. A stage file writes no bound as `inf`; `null` would be a name.
- **Registry and tests.** A row per chart: identifier, family and its measure, the operator expression in normal form, the
  coordinates with their domain and the conversion to the canonical chart, the defaults per written form, the pinning
  constraints with machine-readable names, the properties, the written-form labels per format, the cross-references. Tests
  in each repository: the ontology's rows complete, conversions round-tripping, means against quadrature, the generated
  files compared with the source; the schemas' validator, checker and hash agreeing with the rows; Bellman's family table
  and refusals agreeing with the rows' Bellman labels. The identity rule applied as resolve, fill, normalize, convert,
  compare, a vacuous conditioning reducing to none.
- **What it leaves undecided:** the stage-file grammar's treatment of keyword calls and nested coined families, unverified
  against its sources; and nine choices for the owner, folded into the list in [`existing-syntax.md`](../../existing-syntax.md).
  The bellman session settled the unverifiable items the same evening from its branch and by probing the elaborator: the
  branch's laws page lists eight families and names the support condition `law-support`; a keyword call is refused when
  the file is read, and `null` as a name the stage does not declare, so a stage file writes no bound as `inf` or `-inf`;
  a `Mixture` component outside the family table elaborates and its forward builder is constructed, whereas a declaration
  whose own family is outside the table gets none, an inconsistency for Bellman's maintainers; and two tests already read
  the family table, one of them comparing the laws page with it.

**Weighed.** Agreed throughout, with three additions. The `null` token is not a coinage: it is how Distributions.jl
(`nothing`), PyMC and NumPyro (`None`) spell "no bound", the difference here being only that an omitted key means three.
Cross-references to ProbOnto should use SKOS's mapping properties, `skos:exactMatch` for the same chart of the same family
and `skos:closeMatch` otherwise, not `owl:sameAs`, which merges every statement made about two identifiers. And the
"registry" asked about is the ontology's own table of rows, which the schemas' `conventions.md` cites, not the registry
block of Bellman's recipes.

## Since

The owner ruled on the decisions in [`existing-syntax.md`](../../existing-syntax.md) on the morning of 2026-10-20 (see
that day's rulings), as recommended except in three places:
- Bellman-SYM's truncated lognormal is aligned with the truncated normal its main had gained that morning. It is
  `TruncatedLogNormal(μ, σ, l, u)`, taking the location and spread of the logarithm with bounds on the draw, and σ > 0.
- The ontology's home is `ontologies/probability-distributions/`, under a top-level folder for the project's ontologies.
- The name of the w3id.org namespace is left for later.

The bellman session had raised one question for session 4: a mixture's component written by the mean of its logarithm,
against a lone law written by the mean of its draw. The alignment settles it. Bellman's family takes the location and
spread, which the converter computes from the parameter files' charts, as it computes each mixture component's.

The ontology is draft pull request #1, and the shock laws written on it are draft pull request #2. The ontology's tests and
the converter's check at Bellman's draft are in the findings of 2026-10-20.
