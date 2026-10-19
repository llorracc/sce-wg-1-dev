# Rulings of 2026-10-18

The owner's decisions, in substance and by time (EDT); times without a stamp are placed from file modification times and
are approximate to about ten minutes. His words are kept outside this public repository.

- **Morning.** The schema's Matsya review proceeds by questions in a session; a job runs only on the owner's word. Of the
  review's suggestions: HARK's
  missing laws are to be raised with the HARK session; the regularity conditions are to cover every variant that uncertainty
  modifies (Szeidl, Harmenberg, the risk-modified and mortality-adjusted forms); the existence question for unbounded laws is
  set aside; methods and their settings are separate schemas, so that one method runs under a suite of settings; the results
  always include a measure of the numerical ergodic distribution and the target buffer stock where one exists.
- **10:35.** Three things approved: the variance-matching convention for the truncated lognormal (the stated standard
  deviation is that of the log after truncation; bounds at ±3), folding the review's suggestions into the documents with Euler
  and stationarity residuals required, and the HARK session's bounds-fix pull request.
- **About 11:00.** A draft is to be made, with the matsya, HARK and HAFiscal sessions, of how the schemas describe HAFiscal's
  household models and of a test suite over parameterizations and methods.
- **14:21** (clock). Five decisions: the paper's family is named `bst-markov_ui-and-agg`; the toy's true model is truncated at
  ±3, with an untruncated member kept in the suite; the draft goes into the fork without the benchmark's atoms and dry-run
  results; the emitter and the HARK newborn flag go ahead iteratively, any schema improvement the work suggests being put to
  the owner with its consequences first; the bellman session writes the bst/1 stage file by hand, one Matsya question checks
  it, and a Matsya job follows once, later, as a completeness test.
- **About 15:00.** The schemas use BST's notation and SolvingMicroDSOPs' where BST is silent; the baseline is BST's version;
  all parameter domains are stated, which the `.bl` file requires, since the Bellman-SYM machinery is the foundation of the
  true-model descriptions; the newborn must not draw from a law that admits zero income; the natural borrowing limit and the
  worst-income probability are implications, not conditions, and the conditions document is to explain its three kinds of
  statement; the hash over parsed numbers and the tabulated law's collinearity rule on parsed numbers are accepted. ρ ≥ 1
  with the log amendment was chosen here and superseded at 17:30.
- **About 15:15.** A newborn is born employed: its first transitory draw is the employed branch of ξ. The requirement that no
  newborn arrive where zero consumption is forced belongs in the conditions document as a condition of the simulation phase.
- **About 15:30.** Bounds carry marks: a̲_Art for the artificial constraint, a̲_Nat for the natural one, a̲ = max of the two,
  the budget a ≥ a̲. The condition that the population mean of the value be finite is a legitimate regularity condition for
  every bst-class problem, so that population welfare can be computed as in HAFiscal.
- **About 16:20.** The consumption-equivalent is dropped from the results; welfare and marginal welfare statistics are to be
  required or allowed, specified from a close reading of HAFiscal's welfare measure.
- **About 16:50.** The revised welfare block, W = E[v(m)], F = E[u(c(m))] and M = E[u′(c(m))] with its quartile breakdown, in
  utils, with its domain rules, is approved.
- **17:30:27** (the relay checker's stamp). Four decisions on the stage-file foundation: the restructuring is approved in the
  order proposed; a method file names the stage file's own targets, each with a comment; the seven requests go to the Bellman
  maintainer through the bellman session under the owner's name; ρ = 1 is dropped from the family for now, which requires
  ρ > 1 as BST does.
- **18:28:39** (the transcript's stamp). Answers to the evening's walkthrough of what was open. The Markov family's switch
  for permanent income while unemployed gets a third value, `grows` (growth applies, ψ = 1), and `continues` is to be the
  family's standard world; the owner's question of what the code does now is answered by the HAFiscal session's reading:
  the code's default world is `continues`. The precision levels are settings, not error targets. The three optional
  results-file keys are accepted. Of the Markov stage file's open points: the replacement incomes are ξ_U and ξ_X and groups
  are named rather than indexed; the borrowing limit is stated in the household's units, which the owner reads as making
  explicit what the code did implicitly. The benchmark's own toy specification follows bst/1's newborn. The commit of
  unknown origin is the owner's own. He asked for a fuller account of the Markov family's newborn before ruling, and asked
  whether the zero hazard of a recession's onset means HAFiscal treats the onset as an unanticipated shock; both wait. He
  asked for a memorial followed by a push.
- **By 19:12.** After a reading of HAFiscal's history for the computational reason behind the published code's frozen
  permanent income (fewer income atoms in the unemployed states; less simulation noise from the few unemployed), set against
  the reason for the revision's convention (permanent income independent of the employment state, which the
  transition-matrix method's factorization needs), the owner confirms `continues` as the switch's standard value.
- **19:17:31** (the transcript's stamp). The Markov family's newborn follows bst/1's convention: born employed, no ψ in its
  first quarter, its first transitory draw the employed branch, its permanent income from the group's level law. The normal
  regime is absorbing in the household's problem, and the parameter file drops the hazard of entering a recession; the
  exit hazard stays a parameter. "agg" in the family's name is the aggregate regime alone; the aggregate-demand feedback
  is a later family or version. The Matsya completeness job on the finished bst/1 document is to be pursued.
- **21:08:56** (the transcript's stamp). Both stage files are to declare the artificial borrowing limit on (−∞, 0] and no
  lower than the natural one, as the model document states. On the per-state natural constraint the owner asked whether
  it reflects his reasons for choosing truncated laws; it does, a natural constraint being meaningful only under bounded
  support, and the answer narrowed the claim: the constraint differs by state only under some calibrations. The prose-only
  completeness job waits for further clarity.
- **21:29–21:33.** Matsya is to be asked for the right solution to the parameter-condition defect in Bellman's own terms;
  its answers are to be weighed against this project's needs and pushed back on where they do not fit; the question is to
  recognize that the natural limit is itself determined by the other parameters; and the schema is to accommodate such
  quantities.
- **21:54:41** (the transcript's stamp). The derived-parameter proposal is approved: derived parameters distinguished from
  implications, a table in each model document, the values a toolkit used reported in the results file, the checker as
  their reference. The owner names the problem exactly: a toolkit taking its natural limit from the discretized shock's
  minimum rather than the law's infimum. He adds that conditions defined by expectations, the GIC-Mod, Szeidl's and
  Harmenberg's among them, depend on the numerical approximation of the integrals and can only be decided once the
  parameters, the method and the settings are all fixed, which may need a fundamental restructuring; and that BST defines
  its conditions by expectations over laws with no analytical form. The restructuring is proposed in `effective-member.md`
  and awaits his ruling.
- **22:08:10** (the transcript's stamp). The proposal's premise is corrected by the owner: there is in general no member
  computable from a parameter file's continuous laws; what can be computed about such a member is a limit, reached only
  numerically; apart from rare cases, only the effective member is well defined. The note is rewritten on that basis.
- **22:18:57** (the transcript's stamp). The discretization is not the schemas' to prescribe: it is up to the toolkit. The
  goal is to set up a problem in a rigorous mathematical way without specifying methods; a toolkit, fed the fully
  parameterized, methodized and settingized problem, must do the calculation and report whether each requirement is
  satisfied. The note is rewritten again on that basis.
- **22:27:22** (the transcript's stamp). A toolkit is not to be required to report its discretization in a form of the
  schemas' choosing: that would need a protocol for the form, would disallow toolkits with other representations of a
  discrete approximation, and is not necessary. What is necessary is to specify the conditions the distribution must
  satisfy, the GIC-Mod among them, and to trust the toolkit to calculate them whatever its internal representation. The
  note's fourth version follows.
- **22:29:24** (the transcript's stamp). The interface pins down expectations rather than moments: the family names the
  expectations its conditions are defined by, and the toolkit reports their values.
- **22:38:58** (the transcript's stamp). The infimum of a shock is defined as the limiting value of a
  representation's bottommost point as the number of points goes to infinity; this is why the truncated lognormal is the
  preferred specification of the law. Recorded in the proposal with the reasoning the owner asked to be thought through:
  the limit is a property of the law and not of a representation, and under truncation it is positive and finite, so the
  effective members share the stated member's regime and differ from it in value only.
- **22:41:43** (the transcript's stamp). The effective-member proposal, in its form after the four corrections, is
  approved for execution: the schema is to be revised accordingly. Executed by 22:51 (see the journal); the choices on
  the note's open questions were taken as recommended and are recorded at the note's end for the owner to reverse.
- **17:44.** The memorial is asked for: the records brought current and committed in this repository, without a push.
