# The reference solution: the standard every solution is compared to

Proposed on 2026-11-04, on the owner's ruling of 06:23:39 that morning
([the ruling](records/rulings/2026-11-04_reference-solution.md)), which answered the two questions of
[`comparing-solutions.md`](comparing-solutions.md). **Status: PROPOSED**; nothing below is applied, and nothing is built
until the owner has read it. Where it differs from [`comparing-solutions.md`](comparing-solutions.md),
[`participation.md`](participation.md), [`for-toolkit-authors.md`](for-toolkit-authors.md),
[`experiments.md`](experiments.md), [`harness.md`](harness.md), [`bst/results.md`](bst/results.md),
[`numerics.md`](numerics.md) and [`../rosetta/README.md`](../rosetta/README.md), this note is the revision, and the
section "What changes in each proposal" says what changes in each. Paths are relative to the repository's root; links
resolve from this directory.

## The ruling, in substance

Four requirements. The owner marked the first two as closed; the other two say what the reference's grids are.

1. A reference solution of each member, solved to very high precision, is what every actual solution, at its toolkit's
   default settings, is compared to.
2. The reference is solved by the continuous solution methods developed in the HAFiscal and HARK contexts.
3. Its solution grid is wide and dense.
4. Its ergodic distribution is constructed on a dense grid that extends up to the 99.9th percentile of the wealth
   distribution.

What this settles. The design of 2026-11-03 asked two questions, fidelity and agreement, and could answer the second only
with a tolerance it could not defend. With a reference there is one question, how far a solution is from the reference,
and the reference's own error is the resolution of the answer. The ladders of levels, which the first experiment held
every toolkit to, become the reference's convergence study; a toolkit's ladder stays optional, as ruled on 2026-10-17.
Agreement between two toolkits is no longer a check: it is what their two distances from the reference imply.

## What the reference is

One results file per member, in the results schema as it stands, with these properties:
- it solves the stated member: the laws are integrated, not discretized, so its effective member is the stated member
  and its named expectations are the checker's closed forms; its representation string says so;
- its toolkit field names the reference solver and its commit, whichever code the owner assigns below, and its method
  and settings files state every count, bound and tolerance;
- its error is stated beside its numbers: the movement of each reported quantity across the reference's own
  convergence study (the grid doubled, the quadrature's nodes a piece doubled, the tolerance tightened), carried as the
  optional ladder the results schema already has, with the finest rung the reference and the movement between the two
  finest rungs its error;
- it is certified before it is used, as the section "Certification" says.

## The continuous methods, named

Five pieces, each with its source. The public sources are what a reader can check; the private ones are named by file
and never quoted.

**The kink-split expectation.** Next period's marginal value is integrated against the shocks' continuous laws, not
summed over atoms: Gauss-Legendre in each law's standard-normal coordinate, the integral cut at the preimage of next
period's kink (and, in HARK's solver, at every knot of next period's rule and at each unit step of the coordinate), so
that no node ever crosses a kink and the expectation is as smooth in assets as the true one; the zero-income event is a
point and enters exactly. Sources: the Kink-Split Quadrature page,
https://econ-ark.github.io/HARK-dev/kink-split-quadrature/, public, with its finding that the rule converges
geometrically from about seven nodes a side; HARK's continuous solver, on the HARK session's unposted local branches,
so not yet citable, its public parts being the proposal issue econ-ark/HARK#1869, the drafts econ-ark/HARK#1861, #1862
and #1863 at their GitHub heads, and the status page https://econ-ark.github.io/HARK-dev/pr-status/; two cautions on
the page, from the HARK-dev session: its measurements are of one shock solved back from a terminal period, not an
infinite-horizon solve with two shocks, and the solver's split at every knot of next period's rule is on no public page
yet; HAFiscal's
`Code/HA-Models/kink_split_expectation.py` in HAFiscal-Latest, private, whose mode SM2 takes the same integral in closed
form as a precomputed operator on cubic Hermite pieces; and the bench's own `exact_expected_marginal_value` in
`harness/adapters/common.py`, the same rule, which has computed every Euler residual under the stated laws since the
first runs.

**The endogenous grid method with a cubic Hermite carrying the EGM slopes.** The same nodes give E[v′] and E[v″], so
the rule's slope at each endogenous point is exact, and the interpolant is a cubic Hermite through the points and the
slopes. The pairing rule, from HAFiscal: a Hermite is legal only with the continuous expectation, since a sum over atoms
puts a kink at every image of next period's kink and a cubic cannot carry a kink inside a segment. HARK's solver builds
a shape-preserving cubic, the subject of its concavity page, https://econ-ark.github.io/HARK-dev/concavity-violations/;
HAFiscal's `continuous_expectation_solver.py` the plain Hermite with the exact slopes, on HARK 0.17.2's one-period
solver. HAFiscal's continuous expectation is moving into HARK as its single source, the HAFiscal session says, with
HAFiscal importing it and adding no capability to its own copy; so HARK's solver is the version of record of the method,
and HAFiscal's serves as a check.

**The natural borrowing constraint from the laws' infima** (the draft econ-ark/HARK#1862), where it lies under the laws
and not where the atoms put it. For the three natural members, with the zero-income event at probability ℘ and
ξ_u = 0, the limit is a = 0, c(0) = 0, and the MPC at the limit is 1 − ℘^(1/ϱ) Þ̊_R, which HARK's rule at level 3
carries to one part in 10¹⁴ ([the record of 2026-11-03](records/findings/2026-11-03_two-questions-on-the-committed-runs/README.md)).
HARK's solver takes the worst income to have no mass under continuous laws, so that the MPC at the natural constraint is
one: true for a positive benefit, not for the zero-income event, whose mass is ℘. The HARK-dev and HARK sessions
confirmed the same morning that the solver's rule is unaffected and only its recorded bound is wrong, a defect whose
fix waits for the owner's word in the HARK session; HAFiscal's solver has the same line. So the reference reports the
MPC at the limit from its rule and checks it against the closed form, never from a solver's recorded bound.

**The kink as the constraint's own endogenous point.** Where an artificial constraint binds, as for the restrained
member, the asset grid holds the constraint itself; the Euler equation gives consumption there directly, the rule has a
knot exactly at the kink, c = m below it, and next period's expectation splits at it. HARK's solver and HAFiscal's both
do this; HAFiscal's solves the restrained member today as stated, the HAFiscal session confirmed, and not the natural
members, whose limit its solver refuses.

**The ergodic distribution.** HAFiscal's and HARK's distributions today are transition matrices on an asset grid with a
lottery between the bracketing nodes, Young's method, the transition's expectation over the shocks' atoms. HAFiscal
developed beside it the kernel-and-curvature spacing of the distribution grid (`tm_grid_spacing.py`: nodes
equidistributed by the larger of the one-step kernel's width and the rule's curvature) and the quantiles of a gridded
distribution by its interpolated weighted CDF, with half of a node's mass below the node (`dist_quantile.py`). A
continuous landing operator, the transition's expectation against the laws themselves, was planned there and not built,
as the HAFiscal session confirmed; only its building blocks exist, the closed-form weights of hat functions and the
truncated law's partial moments. HARK's grid machinery, the simulator's grid specifications and Young's lottery, draws the
shocks from the atoms, so its resolution is the node count, as the HARK-dev session confirmed; the reference's
distribution is therefore the bench's, under the decision R6, whatever code solves the rule. The bench's `Population` is
the same lottery on an a-grid, with the transition over quadrature nodes of the laws.

## The grids

**The solution grid.** Wide: the rule is needed wherever the distribution puts mass and wherever a comparison point
lies; the committed request points reach m = 50, and the committed solve grids 100 to 800. Dense: the nested grid of the
levels with many more points, the kink inserted, and for a natural member the points near the limit that HARK's solver
places where the MPC falls from its limit. The interpolant is the cubic Hermite, never the linear one, whose error on
a coarse grid is of the order of what the comparison measures. Proposed: a top of 1,000 with nesting 3, and the count
set by the convergence study, begun at 4,000 points and doubled until the rule at the request points moves by less
than the target. The HAFiscal session's probe of the restrained member this morning used 1,000 points nested 3 times
from 0.001 above the constraint to 200, the kink inserted, a tolerance of 10⁻¹¹ and 32 nodes a piece, and it would add
one refinement, 2,000 points to 400, before claiming an error. The HARK-dev session's convergence runs on HARK's solver
the same morning recommend, for that code, the cubic with 8 nodes a piece, at least 384 asset points with the top at
or beyond the distribution grid's, a tolerance of 10⁻¹⁰ or tighter, and a check by halving the points; the cost of
its split at every knot rises with the grid, so the restrained member's finer solves are the thing to plan for there.
Its numbers are its own until something public reports them.

**The distribution grid.** Dense, from the constraint to the 99.9th percentile of wealth. The committed level-3 files
already carry that percentile, the schema's `0.999` quantile, and HARK's and dolo's files agree on it to four digits:

| member | m at 0.999 | a at 0.999 | a at 0.99 | median m |
|---|---|---|---|---|
| ℘ = 0.005 | 2.10 | 0.96 | 0.79 | 1.42 |
| ℘ = 0.0005 | 1.72 | 0.60 | 0.47 | 1.18 |
| ℘ = 0.00005 | 1.60 | 0.49 | 0.37 | 1.10 |
| restrained | 1.56 | 0.44 | 0.33 | 1.07 |

So the dense grid covers an interval of length about one, where the committed grids, with tops of 60 to 480, spend most
of their points beyond any mass. Two passes: a first solve and distribution on the ladder's grid give the percentile;
the dense grid is built to it, uniform in a with the constraint and the kink as nodes, at a count the convergence study
sets, begun at 32,000 points, a spacing of 3 · 10⁻⁵, and doubled until no reported statistic moves by more than the
target. Beyond the percentile there are two readings of the ruling, a decision below: the grid ends there and the
lottery puts the mass above on the last node, the literal reading, under which the mean of a and the top Lorenz
ordinates carry a bias of the order of that mass times its excess over the node; or a coarse geometric continuation
carries that mass up to a top beyond which less than the target remains, with the last node's mass reported. The tail
is not bounded under these laws: along the path of the lowest permanent and highest transitory draws, normalized assets
grow by the factor R(1 − κ)/(𝒢ψ_min), above one here, so the stationary distribution reaches every level of wealth
with a tail that falls as a power, whose exponent the family's conditions give; the committed grids' tops of 60 to 480
are where that tail is already below round-off. The transition's expectation: proposed in closed form for the transitory law, as cell probabilities
from its CDF at the cells' preimages, with Gauss-Legendre over the permanent law, so that the distribution's error is
the lottery's alone; checked against the bench's nodes doubled. Quantiles by the interpolated CDF with the half-mass
convention; the bench's `quantiles` is checked against it.

## Certification

The reference is used only once it has passed, with the numbers printed:
1. its named expectations are the closed forms; there is no representation, and the floor of 10⁻¹² of the design of
   2026-11-03 covers round-off alone;
2. the Euler residual under the stated laws, by the bench's diagnostics expectation, independent code, is below the
   target at every request point, and that expectation's own precision, from doubling its nodes, is below it too;
3. the rule's closed forms hold to the target: the MPC at the natural constraint, the limiting MPC, and c = m below the
   kink;
4. two independent continuous solves agree within their stated errors: HARK's continuous solver, and a second solve of
   the same method in independent code, the bench's own continuous EGM built from `exact_expected_marginal_value` and
   a cubic Hermite, with HAFiscal's solver as a third on the restrained member, which its session can run today. This is
   the SBML test suite's standard from [the precedents](records/findings/2026-11-03_precedents-for-the-apparatus.md),
   expected values from closed forms or two independent tools;
5. the distribution: the stationarity residual at round-off, and no reported statistic moving by more than the target
   when the dense grid and the transition's nodes are doubled;
6. the solver's convergence error bounded, not assumed: a tolerance on the loop bounds the last step, not the distance
   to the fixed point, as the HARK session notes of HARK's own loop, so the reference stops when the last step times
   λ/(1 − λ), with λ the contraction factor measured from successive steps, is below the target.

The target is a decision below; proposed at 10⁻¹⁰ for the Euler residual and 10⁻⁹ for the rule's movement at the
request points. The committed level-3 runs reach 10⁻⁵ to 10⁻⁴ under the stated laws, and HARK 10⁻⁷ under its own.

## Default settings

"Default settings" is what a user gets who states the member in the toolkit's own terms and changes nothing else. It is
defined per toolkit, in its stone, and reported in full in the run's settings file:
- HARK 0.17.2, `init_idiosyncratic_shocks`: 48 grid points to 20 above 0.001 with nesting 3, 7 nodes per shock,
  equiprobable with each node its bin's conditional mean, linear interpolation, no value function, the solver's
  tolerance of 10⁻⁶, which bounds the last step of the loop and not the distance to the fixed point. Three things the
  HARK and HAFiscal sessions point out are the member's, not the toolkit's: the infinite horizon (HARK's default is one
  period before a terminal one), the constraint, and the laws. Released HARK has no truncated lognormal, and its own
  default discretizes the untruncated law, a different member; so the laws' nodes are the adapter's, HARK's own
  construction applied to the member's law at HARK's own count, 7 per shock as the ladder's first rung has them. The
  member and the request file are the harness's.
- dolo 0.4.9.20, `egm`: a tolerance of 10⁻⁶ and at most 1,000 iterations; the grid is the model file's, which the
  adapter writes. dolo's own example model for this class, `examples/models/consumption_savings_iid.yaml` in
  EconForge/dolo.py, puts a uniform grid of 100 points on cash-on-hand from 0.01 to 4 and leaves the shock's node
  count to dolo's default discretization; the stone states what the adapter's level `default` takes from it.

The adapters gain a level named `default` beside `low`, `medium` and `high`; the ladder stays optional, as ruled on
2026-10-17, and the committed runs at levels 1 to 3 stay as the two toolkits' ladders.

## The comparison

For each member, each default-settings file against the reference file, every distance printed with the reference's
error beside it:
- the rule at the request points on the relative scale, the largest distance and where it sits, and the MPC;
- the kink and the target, absolute;
- the distribution of m and of a: the quantiles at the schema's probabilities, the 0.999 among them, the generalized
  Lorenz ordinates, the mass at the constraint, the mean of a, the mean MPC and the MPC by quartile;
- the welfare numbers where defined;
- the Euler residual under the stated laws, the toolkit's own beside the reference's.

Reported, not passed or failed: the distance is what a user of the default settings gets, which is the point of the
measurement. A tolerance per quantity, above which a default-settings solution is called wrong rather than coarse, is a
decision below. The experiment schema gains `compare: reference`, whose metric is the distance from the reference file,
and the restrained-limit experiment's second version runs it.

## Who solves the reference, and where the code lives

Three options, a decision below; what the three sessions said on the morning of 2026-11-04 sets their timing:
- **HARK's continuous solver**, the version of record of the method, run by the harness's HARK adapter in a second
  locked environment pinned to a public commit: the fullest implementation (the natural limit from the infima, the
  split at every knot, the shape-preserving cubic, the value function), and HARK's own, so the HARK session's to run
  or to hand over. It is on unposted local branches built on HARK's main after 0.17.2, and the owner's rule there is to
  perfect a pull request locally before posting it; so a locked environment can hold it only once he has it posted,
  and until then an archive of the local commit, which both HARK sessions ran this morning, serves a probe whose
  numbers stay theirs, not a reference file. HARK is also one of the toolkits compared, so its certification needs a
  second solve.
- **HAFiscal's solver**, run by the HAFiscal session: it solves the restrained member today as stated, and not the
  natural members. Its emitter would need a new method, a change to HAFiscal-Latest on the owner's word typed there,
  and under the single-source rule that method would call HARK's solver from an export of the same unposted commit.
  Private, so a run of record there is what this repository could cite.
- **The bench's own continuous EGM**, in this repository: the same method in independent code, from pieces the bench
  has, the kink-split expectation, the quadrature of the laws and the population; public and this session's to build;
  developed in the HAFiscal and HARK contexts by its method, not by its code.

Recommended: the bench's solve now, as the provisional reference, certified against HARK's solver run from the archive
and against HAFiscal's on the restrained member, with those two solves' numbers recorded as their sessions' until they
are of record; HARK's solver becomes the reference of record, in a locked environment, once the owner has it posted,
and the bench's solve then certifies it. If the owner would rather wait for the posting than publish a provisional
reference, the bench's solve is still the certification and the first measurement.

## What the probe found

On the morning of the ruling, step 2 of the order of work was run in the scratchpad and recorded as
[the reference probe](records/findings/2026-11-04_reference-probe/README.md): the bench's continuous EGM, the
kink-split expectation with a cubic Hermite carrying the EGM slopes, on the four members, with a convergence study,
HARK at its default settings, and the ergodic distribution on the dense grid. What it found, against the decisions:
- The method reaches a rule whose error is between 10⁻¹² and a few 10⁻¹⁰ relative at the request points, member by
  member, with the closed forms at the limits carried to round-off: the MPC at a natural limit to 10⁻¹², and the restrained kink
  agreeing with the HAFiscal session's independent solve to 2 · 10⁻¹¹. Where the error sits is known: the points just
  above a natural limit for small ℘, and the quadrature at the split for an artificial kink. R3's targets for the
  rule are reachable, and R1's certification by two independent solves has its first instance.
- The committed ladder's finest level is 8 · 10⁻⁴ from the solution of the stated member on every member, while its
  two toolkits agree with each other to 10⁻⁵: the representation's error, which the design of 2026-11-03 could not
  see and the reference does.
- HARK at its default settings is 5 · 10⁻³ to 10⁻² from the reference within its grid and 2 · 10⁻² beyond it, with
  an Euler residual of the order of 10⁻² under the stated laws on the natural members: the kind of distance the
  comparison of R5 reports.
- On the dense grid the distribution's error is the transition's, not the grid's: refining the grid moves the
  statistics by 10⁻⁶ to 10⁻⁴, while doubling the transition's nodes moves the restrained member's quantiles by 10⁻²
  and the mass at the constraint by 10⁻³. So R6's continuous landing is a requirement, and R3's target for the
  distribution holds only once it exists; until then a reference distribution's error is 10⁻³ to 10⁻².

## What changes in each proposal

- [`comparing-solutions.md`](comparing-solutions.md): the agreement question and its decisions 2a to 2c are withdrawn:
  no classed agreement, no method-only step in every ladder as the tolerance's source (the step stays as a tool of the
  reference's convergence study), the relative scale kept. Of the fidelity decisions, 1a's criterion becomes the
  reference's certification, 1b (the residual under the toolkit's own laws required) is withdrawn as a requirement and
  stays optional, and 1c (the rule's closed forms) stays, as certification. Of the design's six decisions, the split (1)
  stands, agreement as a report (2) is replaced by the distance from the reference, and the rest stand.
- [`experiments.md`](experiments.md): `compare: reference` and its metric; the reference file named in the experiment.
- [`harness.md`](harness.md): the level `default`; the reference's environment and runner; the convergence study as the
  reference's ladder.
- [`participation.md`](participation.md), [`for-toolkit-authors.md`](for-toolkit-authors.md): a participant submits at
  default settings, and a ladder if it wishes; the reference file and its error are what it receives; the two-solve
  certification is the organizer's.
- [`bst/results.md`](bst/results.md) and the results schema: no change in what a file carries; a reference file is a
  results file whose toolkit names the reference solver, and the optional ladder carries its convergence study.
- [`../rosetta/README.md`](../rosetta/README.md): each stone states its toolkit's default settings.
- [`numerics.md`](numerics.md): the level `default` named.

## The decisions

Each with a recommendation.

- **R1, which code solves the reference.** The bench's solve now, as a provisional reference certified against HARK's
  solver run from its archive and HAFiscal's on the restrained member; HARK's solver as the reference of record once
  the owner has it posted, the bench's solve then its certification. Recommended. The alternative is to publish
  nothing until the posting.
- **R2, the distribution grid beyond the percentile.** Dense to the 99.9th percentile as ruled, then a coarse geometric
  continuation to a top beyond which less than the target remains, the last node's mass reported, so that no mass that
  matters is lumped on the last node. Recommended; the literal reading is the alternative.
- **R3, the targets.** 10⁻¹⁰ for the Euler residual under the stated laws, 10⁻⁹ for the rule's movement at the request
  points across the convergence study, 10⁻⁸ for the distribution's statistics. Recommended as a start, to be tightened
  if the solves reach further.
- **R4, default settings.** As defined above, per toolkit in its stone, with the horizon, the constraint and the laws
  the member's and the discretization's count and construction the toolkit's; a level `default` in each adapter; the
  ladder optional. Recommended. The alternative the HARK session names, HARK's own untruncated atoms, changes the law
  as well as the numerics, and the HAFiscal session's probe finds both at a few parts in a thousand from a continuous
  solve of the restrained member.
- **R5, the comparison's form.** Reported with the reference's error beside each distance, no verdict; a tolerance per
  quantity only if the owner wants one. Recommended.
- **R6, the distribution's method.** The transition's expectation in closed form for the transitory law and by
  Gauss-Legendre for the permanent one; quantiles by the interpolated CDF with the half-mass convention. Recommended.
- **R7, the experiment.** The restrained-limit experiment's second version carries `compare: reference` and the
  default-settings runs; the committed ladders stay. Recommended.

## The order of work

1. The three sessions' answers, asked at 06:28 and received between 06:48 and 06:52: the methods confirmed, the
   pointer 1869 corrected to the proposal issue, the unposted branches kept out of public text; the HARK-dev session's
   grid recommendation to follow.
2. The bench's continuous EGM in the scratchpad, on the four members, with its convergence study: the first measurement
   of what the method reaches here; nothing committed.
3. HARK's solver from an archive of the HARK session's local commit, as both HARK sessions ran it this morning, and
   HAFiscal's solver on the restrained member, run by its session; the solves compared, those two sessions' numbers
   recorded as theirs until they are of record.
4. The reference files for the four members, certified, in a findings record, marked provisional until HARK's solver is
   posted and takes over as the reference of record.
5. The level `default` in both adapters, the default-settings runs, `compare: reference` in the experiment schema.
6. The comparison, its record, and the page.
