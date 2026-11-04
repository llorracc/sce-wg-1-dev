# Comparing alternative solutions of a BST-class model: the lessons, and the proposals revised

Proposed on 2026-11-03, in the evening, on the owner's request to draw the lessons of the precedents read that day, of
the work with Bellman, and of the consultations with Matsya, and to revise the proposals for comparing alternative
solutions of models of Buffer Stock Theory's class. **Status: PROPOSED**; nothing below is applied. Where it differs from
[`participation.md`](participation.md), [`experiments.md`](experiments.md), [`harness.md`](harness.md),
[`bst/results.md`](bst/results.md), [`numerics.md`](numerics.md) and [`../rosetta/README.md`](../rosetta/README.md), this
note is the revision and the last section says what changes in each. Paths are relative to the repository's root; links
resolve from this directory. The sources are the records: [the precedents](records/findings/2026-11-03_precedents-for-the-apparatus.md),
[the completeness job](records/findings/2026-10-18_matsya-completeness-job.md),
[Matsya on the distributions](records/findings/2026-10-19_distribution-ontology-matsya.md),
[the stage file as the foundation](foundation.md), [where a method attaches](records/findings/2026-10-22_method-attachment.md),
[the effective member](effective-member.md), [the first experiment's checks](records/findings/2026-11-02_experiment-checks/README.md)
and [dolo's probe](records/findings/2026-11-01_dolo-probe/README.md).

**Superseded in part on 2026-11-04.** The owner's ruling of that morning
([the ruling](records/rulings/2026-11-04_reference-solution.md)) makes a reference solution of each member the standard
and compares actual solutions at default settings to it. [`reference-solution.md`](reference-solution.md) is the
proposal that follows; its section "What changes in each proposal" says which of this note's decisions stand, which are
withdrawn, and which become the reference's certification.

## The question, stated once

A model of the class has no closed-form solution. To compare alternative solutions of one member is to answer two
different questions, and the apparatus so far has run them together:

- **Fidelity.** Did this toolkit solve the stated member? That is a question about one toolkit and the model, and it can
  be answered without any other toolkit: by the distance of the model the toolkit actually solved from the stated one,
  and by the Euler residual of its rule under the stated laws.
- **Agreement.** Do two toolkits' solutions of the stated member coincide? That is a question about a pair, and it has
  no answer without a tolerance; the apparatus has none it can defend, because its levels move the representation of the
  laws along with the method, and the first experiment's check that two toolkits share one effective member holds only
  while both use one shared code for the laws.

The precedents answer the first question against values the organizer owns and report the second with its limits
stated, never as a score. The lessons below say why, and the design that follows keeps every ruling and changes what is
computed by whom, what counts as a pass, and what is only reported.

## The lessons

### From the precedents

- **The organizer ships the writer and the validator; the participant brings what only it has.** Every scheme that
  lasted asks the participant for one artifact it already has plus a short self-description, and runs the rest itself:
  CMOR and PrePARE for the climate archive, the reference libraries and the one-command container of the systems-biology
  suites, Bowtie's thin wrapper. Here the author brings its solution and a card; the organizer's program makes the file.
- **One bench computes every diagnostic from the reported rule at fixed points.** The multi-country comparison of 2011
  fed each team's policy function to one test bench with its own shocks, points and integration rule, so that every
  difference was the policy function's and none the diagnostics'; the unit-free Euler residual was the shared currency.
  Here two reference adapters compute the residual through one shared quadrature today, which no outside author has.
- **Verification is against values the organizer owns; comparison is downstream, with its limits named.** The SBML
  suite's expected results come from closed forms or two independent tools; NIST certifies by two methods; the web
  platform's dashboard belongs to the organizer. Here the stated member's closed forms are the certified values, and two
  implementations already agree on them: the checker and the buffer-stock ontology, whose formulas reproduce the checker's
  factors to one part in a trillion.
- **A comparison run or reported by the participants hollows out, and timings do not compare.** FMI's cross-check was
  archived; the SBML results database shows passes and not discrepancies; the 1990 comparison could not say who won. The
  harness runs every toolkit, the ledger shows discrepancies, and a run time, recorded since the ruling of 2026-11-04 that revoked the no-timings rule, is shown with the machine and
  settings it came from and never as a score.
- **A normative statement nobody outside can read is recorded as a failure.** The climate archive's attributes document
  sat behind a sign-in; the stage files are written in a language whose documentation is not public.
- **Curated files rot until a machine reads them.** Almost every curated experiment file in BioModels carried a mistake
  that a validator later found. Every member, request and experiment file here is to be read by a test on every change.

### From Bellman

- **Statement, method and settings are three files, and the statement carries no method.** Bellman's stage file states
  the problem, its methods file attaches a method to a target the stage names, by tag with a handler for the routine,
  and its settings stay apart; the owner ruled on 2026-10-22 that the stage files stay free of any method's lines. The
  COMBINE community reached the same split on its own: the model, the experiment and the algorithm are three documents
  with three vocabularies. The trio stays the hub, and the cards are generated from the method file, never written twice.
- **The stage file cannot state everything, and the comparison lives largely in what it cannot state.** Types and
  shares, mortality as an event with replacement, the newborn, the stationary population and its two measures, the laws
  outside the language's families, a parameter the laws determine: all of these are the schemas' own layers. The
  stationary population is where toolkits differ most, by a lottery, a simulation or an eigenvector, so the population
  layer needs the care the stage file gets: one definition of each statistic, written out, and one estimator.
- **A parameter the laws determine is asked for, never assumed.** Bellman accepts a condition that names another
  parameter without evaluating it, and takes the natural limit as a calibration entry; HARK took it from its lowest atom.
  The owner's rulings of 2026-10-18 made the effective member the toolkit's own report: the expectations the family
  names, the lowest values, the derived parameters it used, every condition's factor and verdict. Nothing in that block
  is generated by the organizer, because only the toolkit knows what it solved.
- **A spelling is adopted; a convention is stated in the adopted spelling; both get a registry row and a test.** The
  schemas write a truncated lognormal by the standard deviation of the log after truncation and bounds in standard
  deviations; Bellman's family takes the location and scale before truncation with bounds on the draw; the converter
  does the arithmetic and Bellman's closed forms gave every converted law its mean of one. A toolkit's representation of
  the laws is one more chart, and the closed-form moments the checker prints are its self-test.
- **The language binds; the toolkits solve; and the language moves.** Bellman elaborates a stage file and binds methods
  to its targets, in a private repository whose main dropped the marginal-value fields the stage files used, so that
  both had to be rewritten. The day-to-day comparison must depend on no elaboration: the checker's tests pin the stage
  files' names; Bellman's elaboration and a Matsya round trip are checks of the statement, run once per family version.
- **Two toolkits meet at common points privileged by neither grid.** The request file's points are that rule here;
  Bellman's registry design, which is not public, holds the same one. The points are read through each toolkit's own
  interpolant, never through a resampled export.

### From the consultations with Matsya

- **A round trip finds what agreement between neighbors hides.** The completeness job converged on a flipped law: its
  convergence compared adjacent cycles, and a change made in the first cycle went unremarked. A ladder that compares
  each level with the one before has the same blind spot; the stated member's closed forms are the origin every level is
  compared with, and the effective member's movement between two levels says whether a step changed the model or only
  the method.
- **An independent reader, given material and a pinned source, produces the hard part of a stone.** Matsya's reading
  of HARK's source at one commit, in sixty-seven excerpts each checked against the file, found the order of the atoms,
  the reweighting of one shock, the limit taken from the atoms and the newborn's draws. That is how a stone's departures
  are made: by reading the toolkit's public source against the stage file, every row citing a line, before any run.
- **An answer is weighed, and cites what it rests on; what it cannot cite is deduction.** The standing rule for Matsya
  is the rule for a ledger: every number says whether it is the toolkit's report, the organizer's computation or a closed
  form, and a reader can trace each to its source.
- **Identity is decided in a canonical chart.** Two spellings are one law when, after filling the defaults and
  converting to the canonical chart, their parameters agree. Two solutions are compared in canonical coordinates in the
  same way: the named expectations of the effective member, the rule at the request points, the residual under the
  stated laws at those points, and the generalized Lorenz ordinates at the fixed probabilities. Nothing else is compared.

### From the committed runs

- **Agreement between two solvers on one representation certifies the solvers, not the solution.** HARK's and dolo's
  committed rules agree to a few parts in a hundred thousand at the finest level, while each moves by about 3.5e-3 at
  the request points below m = 20 when the nodes change between the medium and high levels. Every step of both committed
  ladders moves the named expectations, by 1.6e-2 and then 3.4e-3, so no step of either measures the solver alone.
- **An export is not the rule.** Linear interpolation of the 401-point export differs from the reported rule at the
  request points by about 3e-5, above both toolkits' residual under their own laws, which is below 1e-6.
- **A residual of one's own transition tests nothing.** Every committed stationarity residual is one forward step of
  the adapter's own lottery on the reported distribution, between 1e-14 and 3e-10, as the results document itself says of
  a linear solve.

## The revised design

### Two kinds of check

A check that can fail is a check of one toolkit against the model, or of one toolkit against itself across members and
levels. A comparison of two toolkits is reported, classed and never failed.

- **Fidelity, against the model.** Each named expectation of the effective member approaches the stated member's closed
  form along the toolkit's ladder, or sits at a stated round-off floor, which passes at any level. The Euler residual
  under the stated laws, computed by the bench, falls along the ladder or sits at its floor. A representation that
  reproduces the closed forms is never failed for a distance that cannot fall.
- **Within one toolkit.** The experiment's own member-against-member checks, such as each natural rule lying closer to
  the restrained rule than the rung before.
- **Agreement, reported.** The difference of two toolkits' rules at the request points, beside each toolkit's own
  movement between its two finest levels and the kind of each step, classed as within the solvers' convergence where a
  method-only step exists for both, a difference of regime where their effective members sit on opposite sides of a
  condition, a difference of method where the stones name one, and otherwise a difference to trace. No class is a verdict.

### What a toolkit reports

Unchanged in principle, and smaller in practice:

- the effective member it solved: the named expectations, the lowest values, the derived parameters it used, every
  condition's factor and verdict, the statuses that follow;
- the rule: c and its own MPC at any point the bench asks, through `evaluate`, and the exported rule for the record;
- the value where it keeps one;
- its stationary population as weighted points, never published: a grid method's nodes and masses, a simulation's agents
  with equal weights, with the agents, periods, burn-in and seed. A toolkit that declines reports the population block
  itself, as today;
- its own Euler residual under its own representation of the laws, optional today and recommended, since it is the one
  residual that measures the solver apart from the representation and only the toolkit can compute it.

### What the bench computes

One program of the organizer's, the bench, named for the test bench of the 2011 comparison, replaces the kit of
[`participation.md`](participation.md) and is carved from the toolkit-neutral functions of `harness/adapters/common.py`
before the adapters' independence strips that module. From the toolkit's exports it computes, by one code for every
toolkit:

- the Euler residual under the stated laws at the request points, by its own Gauss-Legendre quadrature of the stated
  laws, evaluating the toolkit's interpolant through `evaluate`, with the quadrature's precision stated;
- the special points, the kink, the target and the pseudo-target, as roots on the rule through `evaluate`, their
  statuses from the toolkit's verdicts;
- from the weighted points, the generalized Lorenz ordinates and quantiles, the mass at the constraint, the mean MPC and
  its quartiles under both measures, by the one estimator written into `bst/results.md`;
- the stationarity residual as one forward step of the weighted points under the stated laws and the toolkit's rule
  through `evaluate`, which tests stationarity where the adapter's own step did not;
- the pooled blocks, the hashes, the provenance, and the results file.

Where the toolkit also reports a value the bench computes, both are recorded and the discrepancy shown. The checker
stays the only gate and verifies the assembled file as it verifies any other; the bench adds nothing to what it checks,
so the writer and the gate stay two programs. Acceptance: the bench assembles HARK's and dolo's committed files at the
low level from their exports, and the assembled files verify and agree with the committed ones to the estimator's own
difference, which is recorded.

### The ladder, and the method-only step

A settings element may change the representation of the laws, the method's own settings, or both. Nothing new is
declared: the bench reads the kind of a step from the effective member, which moves across a step that changes the
representation and is identical across one that does not. A toolkit's ladder is asked to hold at least one method-only
step at its finest representation, so that its movement there measures the solver alone and gives the agreement report
its tolerance. The committed ladders hold none; each reference adapter can add one at the cost of one more run, the
finest nodes with a finer grid. This brings forward the sharper test the owner deferred on 2026-11-02, in the form the
effective member makes free.

### The statement a participant is held to

The stage file stays the normative statement, as ruled on 2026-10-18. A participant reads it once beside
`bst/model.md`, which reads it block by block, and is held to the model document with the parameter and results
validators, since the language's documentation is not public. Three checks keep the two in step: the notation test that
every name the document uses is the stage file's; Bellman's elaboration of the stage file at a named commit, through the
session that makes Bellman's changes; and a Matsya round trip of the document, once per family version, as the
completeness job was run once. A request goes to Bellman, through that session, for a public rendering of the subset of
the language the two stage files use, and until it exists the schemas carry a one-page reading guide stated as their
own.

### The stone, in two stages

The card first, as the plan has it: the toolkit's capabilities against the families, in the author's words, answered by
the organizer before any code, which keeps the pause the owner asked for after a stone. The rest generated after the
first verified run: the lexicon's rows from the card and the writer, the methods table from the method file, the
evidence from the verification, and the departures from a reading of the toolkit's public source at a pinned commit
against the stage file, every row citing a line, as Matsya's reading of HARK was done. The author corrects the rows only
the author knows. The cards in the stone registry's fields are the organizer's export from the same source.

### The certified values

The stated member's closed forms, agreed by the checker and the ontology, are written by command into an expected file
per member: the expectations, the factors, the verdicts, the natural limit and the worst income, with a changelog. For
the solution no closed form exists, so no expected value is certified; the reference runs' agreement bands are
informative only, labeled as shared-node runs until the adapters' independence has run and as two independent
representations after it. The ledger prints beside every number its provenance: the toolkit's report, the bench's
computation, or a closed form.

### Everything else

The stages of participation, the probe through the private channel, the ledger's form, the governance entry, the
license, the refusals, the disputes, the versioning of the model statement and of the results schema, the execution
envelope, the registration, the lifecycle and the attribution stay as [`participation.md`](participation.md) proposes
them. A second experiment's terms wait for its member, with the HAFiscal-Latest repository since 2026-11-04.

## The two questions, put to the committed runs

On the owner's request of the same evening, the design above was put to the restrained-limit suite's committed runs
and to one more run per toolkit and member, the method-only step, in
[the record of 2026-11-03](records/findings/2026-11-03_two-questions-on-the-committed-runs/README.md). What the files
showed sharpens each question into the decisions below.

**Question 1. What must a toolkit show, against the model, for its solution to count as a solution of the stated
member?** Both toolkits pass both of the design's checks on every member. Beside the pass, four facts:
- the floor is necessary: the distance of E[ψ] from its closed form rises from 0 to 2.2 · 10⁻¹⁶ along the ladder,
  so a check that only asks for a fall fails the one name the representation gets exactly;
- the metric is absolute where the closed form is zero, as the experiment schema's definition already has it, since
  the restrained member's worst income has mass zero and a finite representation puts 1/N² there;
- "falls along the ladder" passed dolo's residual on ℘ = 0.00005 at 1.17 per level while that residual was pinned at
  the cap the definition gives it; the number that told the solver's error from the representation's was the residual
  under the toolkit's own laws, which the schema makes optional, and across the method-only step it fell from
  6.9 · 10⁻³ to 2.3 · 10⁻³ for dolo while the residual under the stated laws on the restrained member stayed at
  2.1 · 10⁻⁴, the representation's;
- the model has closed forms for the rule itself that no check uses: the MPC at the natural constraint,
  1 − ℘^(1/ϱ) Þ̊_R, which HARK's rule carries to one part in 10¹⁴ at every level and dolo's approaches by 3.5 to 3.8
  per level, 6.1 · 10⁻⁵ short at level 3 on ℘ = 0.00005; the limiting MPC 1 − Þ̊_R, which the checker already prints;
  and c = m below the restrained kink, which both carry to round-off.

**Question 2. When two toolkits' solutions differ, what is the apparatus to say?** At the finest level the two rules
differ by 1.1 · 10⁻⁵ to 2.4 · 10⁻⁵ at the request points up to m = 20, and each toolkit's own rule moves by
3.3 · 10⁻³ to 3.5 · 10⁻³ across the step from level 2 to level 3, which moves the effective member and so changes
the representation; the second version's check, the sum of the two movements, would accept a difference three hundred
times the one observed. Across the method-only step, which the report reads as such from the effective member's
identity, HARK moves by 7.4 · 10⁻¹¹ to 4.1 · 10⁻⁷ and dolo by 8.1 · 10⁻⁶ to 1.8 · 10⁻⁵ across the four members, the size
of the difference itself; at that step the two differ by 2.9 · 10⁻⁶ to 6.1 · 10⁻⁶. On the relative scale, which the
stone guide asks for the rule, the largest difference at level 3 is 1.0 · 10⁻⁵ at m = 50 for the restrained member and
6.3 · 10⁻⁵ at m = 0.01 for ℘ = 0.00005, where dolo's residual sits and where the absolute scale, with c ≈ 0.01,
sees nothing.

## What changes in each proposal

| document | what this note changes |
|---|---|
| [`participation.md`](participation.md) | the kit becomes the bench, with the split above; its decisions on the kit, on the block-level status and on the weighted points fold into the first and third decisions below; the agreement check is a report |
| [`experiments.md`](experiments.md), the restrained-limit experiment's second version | `toolkits_agree` becomes the agreement report with its classes; `approaches_stated_member` gains the round-off floor; a third check, the bench's residual under the stated laws falling along the ladder, is added; the validator's enumerations gain what the three need, a schema change |
| [`harness.md`](harness.md), the adapters' independence | the bench is carved from `common.py` before the module is stripped; the diagnostics' quadrature moves to the bench; each adapter's ladder gains a method-only step; the acceptance adds the bench's reproduction of the committed files |
| [`bst/results.md`](bst/results.md) | the comparison section rewritten as above; the estimator of the ordinates and quantiles written out with its own difference as a tolerance; the residual under the toolkit's own laws recommended; the weighted points named as the population's export, as the exported rule is the policy's |
| [`numerics.md`](numerics.md) | the ladder's kinds of step, detected from the effective member and not declared; the method-only step asked for |
| [`../rosetta/README.md`](../rosetta/README.md) | the section on comparing two toolkits replaced by the classes above; the stone's second stage generated, with the departures from a cited reading |
| the checker, the ontology, the parameter files, the hashes | unchanged; the committed results files stay valid |

## The decisions

The two questions first, each with the decisions the committed runs made concrete; then the six of the design, in
order, each with what it blocks and who is consulted first.

**On the first question, fidelity:**
- **1a.** The pass criterion stays as the design has it: each named expectation approaches its closed form or sits at
  the floor of 10⁻¹², on the absolute metric where the closed form is zero; the residual under the stated laws falls
  along the ladder; the numbers printed beside every pass. Recommended.
- **1b.** The residual under the toolkit's own representation of the laws becomes required, since it is the one number
  that tells a solver's error from a representation's and only the toolkit can compute it. A schema change, so put to
  the HARK and HAFiscal sessions first. Recommended.
- **1c.** The rule's closed forms join the certified values and the fidelity checks: the MPC at the natural
  constraint, the limiting MPC, and c = m below an artificial kink, each with the floor. Checks of one toolkit against
  the model that need no other toolkit, and no change to what a results file carries, since the rule's slope at the
  request points nearest the constraint is already reported. Recommended.

**On the second question, agreement:**
- **2a.** Agreement is reported and classed, never failed, as the design has it. Recommended.
- **2b.** Each ladder holds a method-only step at its finest representation, one run more per member and toolkit,
  and the class "within the solvers' convergence" takes its tolerance from it; this brings forward the deferral of
  2026-11-02, and the record shows what it buys. Recommended.
- **2c.** The rule is compared on the relative scale, as the stone guide says; the experiment's first version, which
  compares it on the absolute scale, is corrected in its second. Recommended.

1. **The split.** The bench computes the Euler residual under the stated laws, the special points, the population
   statistics from weighted points and the stationarity residual, by one code; the effective member and the conditions
   stay the toolkit's own report; the toolkit's residual under its own laws is recommended beside. A change to what a
   toolkit computes, so put to the HARK and HAFiscal sessions before any validator changes. Blocks the bench.
2. **Agreement as a report.** Pass and fail only against the model and within a toolkit; the pairwise difference
   reported with its classes and the movements beside it; the method-only step as the tolerance's source, which brings
   forward the deferral of 2026-11-02. Blocks the experiment's second version.
3. **Weighted points as the population's export,** declinable, never published, from which the bench computes the
   block for every toolkit alike. Blocks the bench's population path; without it the block stays the toolkit's own and
   the stationarity residual stays what it is today.
4. **The statement a participant is held to** while the language's documentation is not public, and the request to
   Bellman for a public rendering of the subset the stage files use. Blocks the reading guide and the page.
5. **The stone in two stages,** the card first and the departures from a cited reading of the source, as a reading of
   the stone-first order of 2026-11-01. Blocks the stone stage.
6. **The order of work:** the bench carved from `common.py`; the adapters' independence run with a method-only step in
   each ladder; the experiment's second version; then the page, after the governance entry and the license that
   [`participation.md`](participation.md) asks for first. Blocks sending anything.
