# The effective member

Design note, 2026-10-18; see the [README](README.md). Proposed that evening, corrected by the owner four times, approved
at 22:41 EDT and EXECUTED the same evening: the documents, the results validator and the checker now follow it, and the
choices made on its open questions are at the end. It restructures how the schemas treat quantities the parameters
determine and conditions whose value depends on a toolkit's numerical choices. Three earlier versions the same evening were
corrected by the owner: the parameter file's member is in general a limit, not a computable thing; the discretization is the
toolkit's own, not the schemas' to prescribe; and a toolkit is not to be made to report its discretization in a form of the
schemas' choosing, which would be a protocol that shuts out other representations and is not needed. The owner then set the
interface: not moments, but the expectations the conditions are defined by.

## The principle

The schemas state a problem in a rigorous mathematical way and say nothing about how it is solved. A toolkit, handed the
problem with its own method and settings, solves it as it sees fit and reports back: the quantities asked for, and whether
each of the family's requirements is satisfied in what it solved. The requirements are stated as conditions on the
distribution, the GIC-Mod and its kin, each defined by expectations the family names, and the toolkit is trusted to
compute those expectations in whatever representation it keeps of the distribution. Nothing in the schemas prescribes a
discretization, a grid, a quadrature, or a form for any of them.

## The problem this addresses

Two observations of 2026-10-18 point at one gap.

- **Derived parameters.** The natural borrowing limit is not a free parameter: it is the capitalized worst income, a
  function of the laws' lowest values, of 𝒢 and of R, and in the Markov family a fixed point over the employment states.
  HARK takes its natural limit from the discretized shock's minimum, not from the law's infimum. Nothing in the schemas
  says what a toolkit is to do about that, or asks what it did.
- **Numerical conditions.** The GIC-Mod, the GIC-Szeidl and the GIC-Harmenberg compare a patience factor with an
  expectation, E[ψ^(−1)], E[log ψ] or E[ψ log ψ]. A toolkit evaluates those expectations under its own approximation of the
  law, so their values depend on the method and the settings, and a member near a boundary can satisfy a condition under
  one approximation and fail it under another. Such a condition can only be decided after the parameters, the method and
  the settings are all fixed. The checker today decides it from the parameter file's law alone, and the emitter copies
  those verdicts into the results file as the statuses of quantities the toolkit computed under a different law.

## What BST assumes

BST's assumption on the shocks is not parametric: ψ has mean one and bounded support in the strictly positive reals, and so
has the employed draw. The paper says that this excludes the lognormal and other unbounded laws, and that it is consistent
with every standard discretization of them onto a finite grid, Gauss–Hermite or equiprobable. Its conditions are
expectations under whatever law the shocks have: the FVAC's E[ψ^(1−ρ)], the GIC-Mod's E[1/ψ], Szeidl's E[log ψ],
Harmenberg's E[ψ log ψ], the rate condition's E[ψ²], and the killed root of the tail. None has an analytical form in
general; each is defined by the law, and is a number only once the law is a particular one.

## The two members

The member a parameter file names is the **stated member**. In general nothing about it is computable except as a limit,
approached numerically and never reached. For the seven laws the schemas admit today the moments have closed forms, so the
stated member's conditions and derived parameters can be evaluated to machine precision; that is a property of those laws,
and the architecture does not rest on it.

What a toolkit solves is the member whose laws are its own approximations of the stated ones: its **effective member**. In
the toolkit's own representation everything about it is computable, its conditions in particular; it is a member of the
same family and, for any finite representation, sits inside BST's assumption. The schemas never see its representation.
They know it through what the toolkit reports about it: the expectations the family names, evaluated under it; the
conditions it satisfies; and the derived parameters it has.

## What a toolkit reports

Given the parameter file, a method file and a settings file, a toolkit reports, in the results file:

- **The expectations the family names**, evaluated under its effective member. Each family's conditions document lists,
  for every condition and derived parameter, the expectations it rests on, as integrands: for `bst/1`, E[ψ^(1−ρ)], E[1/ψ],
  E[log ψ], E[ψ log ψ] and E[ψ²], with the mean E[ψ] and E[θ] as the representation's own; for the Markov family the same
  conditional on the next state, and the chain's rows. They are numbers free of any representation, which any toolkit that
  computes the conditions has in hand, and they are the interface: pinned down as expectations, not as moments, since
  E[log ψ] and E[ψ log ψ] are not moments and a later family's integrands need not be either.
- **The family's conditions, decided on its effective member:** for each condition in the family's table, the factor it
  computed and the verdict, holds or fails, required in full. Each factor is arithmetic on the reported expectations and the
  parameters, which the checker repeats.
- **The derived parameters it used**, the natural limit among them, per state where they vary: its effective member's own,
  which is what HARK computes when it takes its limit from the lowest value of its representation.
- **The statuses of the quantities**, from the domain rules applied to its own verdicts: a target exists for the toolkit
  when its effective member satisfies the GIC-Mod; a kink when the artificial constraint binds in its effective member; a
  welfare mean when its effective member's lower-tail case says so. The emitter stops copying the checker's verdicts on the
  stated member.
- **The diagnostics**, as now: the Euler and stationarity residuals against the stated member's law, by a method other
  than the toolkit's own and with that method's precision stated, since they measure the whole error of the toolkit's
  solution as an approximation to the stated problem.
- **The lowest values** of ψ and of income under its effective member, beside the derived parameters, since the natural
  limit is arithmetic on them; they are not expectations, but they are numbers free of any representation all the same.
- **The population's representation**, when the toolkit pushes the population forward under one other than the
  household's: the same expectations and lowest values, deciding the conditions that are about the stationary population,
  the GIC-Szeidl, the GIC-Harmenberg, the welfare conditions and the tail exponents, while the household's block decides
  the rest. Added on 2026-10-19 on the owner's approval, after the emitter's fourth level showed the need.
  The stated member's infimum is defined as the limit of the bottommost point of a representation as its number of points
  grows without bound (the owner's definition, 2026-10-18): it is then a property of the law and not of any
  representation, since every consistent scheme's lowest point tends to it, and the toolkit's reported lowest value is its
  approximation of that primitive, as its reported E[1/ψ] is of the law's. For a truncated law the limit is the truncation
  point, positive and finite, so the stated member has a finite natural limit and a positive worst income, and every
  effective member shares that regime, differing from the stated member in value only. For an untruncated law the limit is
  zero while every finite representation's lowest point is positive, so every effective member has a finite natural limit
  where the stated member has none and a kink under a zero artificial limit where the stated member has none: the regime
  never converges, only the value does. That is why the truncated lognormal is the recommended form of the law, and why the
  untruncated members of a suite are limit cases to be read as such.

## What the checker does

- Admits a stated member to a suite by the family's validity conditions, decided in closed form where the law admits it,
  which the seven laws do, and otherwise to a stated numerical precision, with `undecided` when the margin lies within it.
- Computes, where closed forms exist, the stated member's factors and derived parameters as the limit a toolkit's effective
  members approach along its own ladder, and reports each toolkit's distance from them against the toolkit's own measured
  convergence; where no closed form exists, says so.
- Verifies each results file for what needs no representation: each factor is the arithmetic of the reported expectations
  and the parameters, which catches a factor that leaves out a term, as HARK's released finite-value-of-autarky factor
  leaves out survival; each verdict agrees with its factor; the statuses follow the verdicts; each derived parameter is the
  arithmetic of the reported lowest values; the reported lowest values lie at or above the stated member's infima and
  approach them along the toolkit's own ladder; and the expectations obey what holds for every mean-one law,
  E[ψ^(1−ρ)] ≥ 1, E[1/ψ] ≥ 1, E[log ψ] ≤ 0 and E[ψ log ψ] ≥ 0, up to the reported mean's departure from one.
- Compares results files as approximations to the stated member's solution, with the differences of the toolkits' factors
  and verdicts reported beside the differences of their values.

## How the comparison changes

- Two toolkits' values are compared, as now, at a tolerance from each one's measured convergence, and a disagreement
  beyond it is read with their verdicts: a difference of regime, one toolkit's effective member satisfying a condition the
  other's fails, is reported as such, with both factors and the stated member's limit verdict where it is known.
- Along a toolkit's own ladder of settings, the settings that change its effective member, its nodes and truncations,
  converge in the factors, and the others, its grids and tolerances, converge in the solution; the two are read separately,
  which the vocabulary names model-changing and method-only settings, as descriptions of a toolkit's settings and not as
  requirements on them. The emitter's residual against the continuous law, falling as n^(−1.4) in its node count, is a
  measurement of the first kind.
- Near a boundary of a condition, toolkits may legitimately sit on opposite sides and report opposite verdicts; the stated
  member's verdict is then whatever the closed form says, or `undecided`.

## What changes in each document

1. [`README.md`](README.md): the vocabulary gains stated member, effective member, derived parameter, implication, and
   model-changing and method-only as descriptions of settings.
2. [`numerics.md`](numerics.md): a results file reports on the toolkit's effective member through its conditions; nothing
   in a method or settings file is prescribed by the schemas beyond being stated.
3. Each family's model document: a table of derived parameters with their formulas, and the rule that a toolkit solves its
   effective member on its own terms and reports what it used.
4. Each family's conditions document: for every condition and derived parameter, the expectations it rests on, named as
   integrands; the conditions decided by the toolkit on its effective member and reported; the stated member's verdicts as
   limits, decided in closed form only where the law admits it; a section on regimes differing between effective members
   and in the lower tail, where a finite representation puts an atom at its minimum.
5. [`bst-1/results.md`](bst-1/results.md) and its validator: the required block of the named expectations, the factors and
   verdicts, the used derived parameters with the lowest values, the statuses as the toolkit's own, the diagnostics'
   precision stated.
6. The checker: the representation-free verifications above; the closed-form evaluation of stated members kept as the
   limit reference; the member checker's verdicts labeled as the stated member's.
7. The emitter, in the HAFiscal-Latest session: report its factors and verdicts, its used derived parameters, and its own
   statuses.

No parameter file or hash of a stated member changes. The stage files are untouched.

## The choices made at execution

Taken as recommended on 2026-10-18; any of them the owner can reverse.
- The named expectations for `bst/1` are E[ψ], E[θ], E[ψ^(1−ρ)], E[ψ^(−1)], E[log ψ], E[ψ log ψ], E[ψ²], E[ψ^(ρ−1)],
  E[ψ^ρ] and p̲, the last three for the welfare conditions and the WRIC; the lowest values of ψ and of income are asked for
  beside them, the owner having asked for the arguments against and found them wanting.
- The diagnostics' primary form stays the residual against the stated member's law, with the method's precision stated; the
  residual under the toolkit's own representation is optional.
- The block of factors and verdicts is required in full; no `not computed` is admitted for a condition.
- `undecided` is kept in the checker's report of the stated member, for a margin within the closed form's precision.
- The population block, approved by the owner on 2026-10-19 at 08:05 EDT: optional, present only when the two
  representations differ, deciding the population's conditions when present.
