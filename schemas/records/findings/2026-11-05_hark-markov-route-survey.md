# The Markov route to the buffer-stock model in HARK: a survey

Written on 2026-11-05 at the owner's request, in preparation for an alternative: a specialized `ConsBufferStockModel`
class in HARK, built to solve the buffer-stock model as the working group defines it, in place of solving it through
HARK's Markov consumer with a nonpersistent unemployment state. The survey gathers what was built on that route here
and in HARK's pull requests, why, what it established, what it cost, and what the harness asks of any route. It records
and does not decide. Its sources are the fork's records, the adapter and the stone at the fork's commit 5c6961b (the
copy that lives on in wg1-buffer-stock), HARK's solvers at the adapter's pin, and econ-ark/HARK's pull requests and
issues as GitHub showed them on 2026-11-05. The HARK and HAFiscal-Latest sessions were asked for their side the same
day; their answers, the HARK session's at 12:07 EST and the HAFiscal session's just after, are the two sections before
the last.

## Why the Markov route was taken

- **The ruling of 2026-10-21 (20:39:38 EDT).** HARK's adapter is to solve the model with HARK's Markov consumer, not its
  standard consumer: two employment states, employed and unemployed, every row of the chain (1 − ℘, ℘), so that
  unemployment comes with probability ℘ whatever the previous state. The model `bst/1` was then read as the nesting of the
  Markov family that was to carry HAFiscal's model, with one machinery for both
  ([the rulings](../rulings/2026-10-21_schema-decisions.md)).
- **The reason, as the owner gave it on 2026-11-01 (in substance).** The nonpersistent unemployment state is a device,
  not a model of its own: it gives the worst income event a parameter of its own, so that either the natural-constraint
  case or the artificial-constraint case can be solved on the toolkit's Markov machinery without rewriting its i.i.d.
  solver. The comparison he wanted it for is BST's own: a natural-constraint model whose limit is zero because of a very
  small point mass at zero income, against the artificial-constraint model, the experiment in BST that shows the first as
  a smoothed version of the second ([the memory](../memory/feedback_markov-family-is-a-device.md)). That experiment is
  the restrained-limit experiment, which has since been run with HARK and with dolo.
- **The reason HARK's own pull request gives** (#1859, below): in the standard consumer unemployment is one more atom
  of the transitory shock, so nothing can be conditioned on employment; a newborn cannot be born employed while still
  drawing the transitory shock, and with no income while unemployed some newborns start with no income. As a Markov
  state, unemployment can be conditioned on like any other state.
- **What the route was not for.** The natural limit from the laws' infima rather than the discretized atoms is a separate
  matter, which HARK's draft pull request #1862 changes in both the standard and the Markov solver; the route did not
  avoid it, and the gate below shows the two solvers giving the same rule to rounding.

## What was built here

- **The adapter** (`harness/adapters/hark/adapter.py`; begun 2026-10-21 at about 23:15, draft pull request #8 of the
  fork, merged 2026-10-22 at 12:56; since 2026-11-04 the live copy is wg1-buffer-stock's). One `MarkovConsumerType` per
  type, `cycles = 0`, two states with identical rows; each state's income its own nodes, employed ψ times the scaled
  employed draw, unemployed ψ times ξ_u; the same return, growth and survival in both states; HARK's constructors for the
  chain and the income process switched off, since HARK otherwise rebuilds the chain at construction from its defaults
  and the income process on any update; after the solve, assertions that HARK solved with the adapter's chain and
  nodes, that the two states' rules and values agree to 10⁻¹² relative, and that both states' lower limits equal the
  effective member's constraint in force. A member of the natural family passes no artificial constraint; the laws'
  infima are recorded on each distribution HARK is given (`limit`), and HARK at the pin takes the natural limit from
  them. The employed state's rule and value are read; the cubic rule is reported inside the grid only. The levels set the
  grid's top, points and nesting and the tolerance (10⁻⁸, 10⁻¹⁰, 10⁻¹²).
- **What the adapter computes outside HARK**, in the code it shares with dolo's adapter: the effective member's natural
  limit from the nodes, the conditions and statuses through the checker's arithmetic on the effective member's
  expectations, the kink and the targets as roots of the rule, the stationary population by a lottery on an asset grid
  with mortality and newborn replacement under both measures, welfare from the value function, and the Euler residuals
  by its own quadrature of the stated laws. HARK's Markov consumer has no condition checks, no targets and no
  Euler-error function; a transition matrix for it does exist on main through the model-file route, as the HARK
  session measured on 2026-11-05 (below), but the adapter built its own.
- **The gate** (`gate.py`, proposed by the HAFiscal-Latest session): at each level the Markov rule against HARK's standard
  consumer on the same joint nodes, the adapter's file against the benchmark emitter's number by number, and the
  checker's verdict. Over the benchmark's ladder the Markov rule agreed with the standard consumer's to 2.3·10⁻¹⁴
  relative or better, the two states' rules were identical, and every number agreed with the emitter's files to
  2.2·10⁻¹² relative ([the finding](2026-10-21_hark-markov-for-bst1.md)). The standing test
  `test_the_markov_rule_is_the_standard_consumers` keeps the first check.
- **The stone** (`rosetta/hark.md`, `hark.cards.yaml`): the lexicon of the Markov consumer's inputs, where each
  reported quantity comes from, the method and its settings, the standard consumer in a section of its own, and HARK's
  departures from the ontology's terms with their identifiers.
- **A natural member under the stated limit** (2026-10-22, evening; fork pull request #12): at the pin, the toy stated
  `natural` is solved under its stated limit at 5 and 9 nodes per shock, the same at every node count, and its file
  passes the checker; the limit binds in the effective member, whose nodes would allow a lower one
  ([the finding](2026-10-22_method-attachment.md), "A natural constraint in HARK"). The test
  `test_a_natural_member_is_solved_under_the_stated_limit` keeps it, on `library` since the family without a point mass
  was abolished.
- **The restrained-limit experiment**, the comparison the route was taken for: BST's calibration with ℘ = 0.005, 0.0005
  and 0.00005 under the natural constraint, against the restrained consumer with ℘ = 0 and a ≥ 0. With HARK at the first
  level the largest gaps to the restrained rule were 0.138, 0.061 and 0.027, at the restrained rule's kink, falling by
  about 2.3 for each tenfold fall in ℘ ([the finding](2026-11-01_restrained-limit-suite.md)); dolo agrees
  ([the two questions](2026-11-03_two-questions-on-the-committed-runs/README.md)); wg1-buffer-stock reproduces it through
  the harness's containers, and its experiment file carries the checks.
- **The Markov family**, HAFiscal's model with persistent unemployment states, which the route was first meant to
  nest: begun 2026-10-22 (fork pull request #13, the validator, first members and checker at the paper's published
  values), its constraint in force found to be a fixed point over the states rather than a maximum
  ([the finding](2026-10-19_markov-constraint-in-force.md)), HARK's Markov solver read on its chains
  ([the finding](2026-10-22_markov-family-scoping.md)), rebuilt on what HAFiscal's code solves and retired on 2026-11-01
  at 16:10 as a calibration of the two principal families ([the finding](2026-11-01_markov-family-as-the-code-solves.md)).
  Its results schema's first version is on the unmerged branch `markov-results`, and the stage files' derivative-term
  spelling on `stage-derivative-terms`; both are history.
- **The ruling of 2026-11-04** that HARK's standard consumer and its Markov consumer are to be tested as two separate
  modes of solution, each a spoke with its own adapter and sections of the stone, keyed with the toolkit in the registry
  ([the rulings](../rulings/2026-11-04_architecture.md); `schemas/registry.md`, "Modes of solution"). The second mode's
  adapter was not built, and the results file has no `mode` field yet; a fresh class supersedes the question.

## What the route established about HARK's solvers

Each item names its source. Line numbers are of HARK's `ConsIndShockModel.py` and `ConsMarkovModel.py` at the adapter's
pin, 11852805 on the fork llorracc/HARK (the first commit of draft #1862, on #1858), unless another commit is named.

**On the two constraints, the heart of the matter.**

- **The natural limit anchors the grid; a tighter limit is imposed as an artificial one.** The standard solver computes
  one period's natural limit from the discretized laws' lowest atoms, `BoroCnstNat` = (`mNrmMin`₊₁ − θ_min) 𝒢 ψ_min / R
  (`calc_boro_const_nat`), sets the constraint in force to the larger of it and `BoroCnstArt` (`calc_m_nrm_min`), and
  builds the asset grid above `BoroCnstNat`. At the pin, with `BoroCnstInfimum` on, the limit from the laws' recorded
  infima is imposed on top as a constraint, "as `BoroCnstArt` is", while the grid still starts at the atoms' limit
  (lines 703 to 716). So a natural-constraint member whose stated laws reach below their atoms is solved as an
  artificial-constraint member of the discretized problem: the top MPC is set to one (`MPCmaxNow = 1.0 if BoroCnstNat <
  mNrmMinNow`, line 726), the rule has a kink at the limit, the population can hold mass at it, and the Euler residuals
  against the stated laws are large near it, where those laws' worst draws leave nothing to consume
  ([the finding](2026-10-22_method-attachment.md); `rosetta/hark.md`, the row on `a_Nat`). The stated model has none of
  these: under the natural constraint consumption goes to zero at the limit with the MPC approaching
  1 − p_worst^(1/ϱ) Þ̊_R, and no agent ends a period at the limit (`schemas/constraint-scenarios.md`). The route did not
  remove this difference: it is in both solvers alike.
- **Where that difference bites, for the families as they stand** (this session's reading of the code, to be checked).
  It arises only when the laws' infimum carries no mass, as a truncated continuous law's bound does. In `bst-natural/1`
  every member has BST's zero-income event, so its limit is zero and the zero-income atom carries the point mass exactly;
  the atoms' limit and the laws' agree, and the standard consumer's arithmetic is that of the stated model. In
  `bst-artificial/1` the artificial constraint is tighter than both limits, so the infima enter only through the grid's
  anchor and the placement of the kink. The member that showed the difference, the toy stated `natural` with a positive
  benefit under truncated laws, belonged to the scenario without a point mass, abolished on 2026-11-03.
- **Released HARK's natural limit is the atoms'.** With HARK's default lognormal laws and no artificial constraint, the
  limit from the atoms lets households borrow about 1.5 times permanent income, which the true laws rule out (the HARK
  session, in `constraint-scenarios.md`); on the toy at seven nodes the atoms give −5.54 where the laws give −1.729, and
  the population then holds assets below the stated limit, so no valid results file can be written. Draft #1862 reads
  the recorded infima by default; HARK's defaults with both laws truncated at three standard deviations then give one
  limit, −0.782670, at 5, 7, 15, 40 and 200 nodes ([the finding](2026-10-22_method-attachment.md)).
- **Zero-probability atoms at the infima do not work**: a zero weight meets an infinite marginal value in HARK's
  expectation, the value is not finite at most points and the limit comes out wrong (the same finding).
- **The probability of the worst income is read from the atoms** (`calc_worst_inc_prob`, line 493): the mass of the
  smallest product of the atoms. It is ℘ when the unemployment event pays nothing, and with a positive benefit and a
  continuous permanent shock it is ℘ divided by the number of permanent-shock atoms, where the true law gives zero
  (departure BSM_0000156). `MPCmax` is built on it (`calc_mpc_max`, line 548), so the top MPC of the effective member
  is the discretization's, not the stated model's; the adapter therefore reports the limiting MPCs from the checker's
  closed forms and reads neither of HARK's.
- **The one-period relaxation and the lower envelope.** Every solver computes c(m) = min(c̃(m), m − `mNrmMin`), the
  lower envelope of the relaxed rule and the constraint line, always, with the comment that it "should only be used
  when BoroCnstArt is True" (line 788; the Markov solver, line 642). The min is exact for the problem; numerically the
  kink is exact only where a = `a_Art` is a grid point (`constraint-scenarios.md`, the HARK and HARK-dev sessions).
- **The Markov solver's limits are a fixed point over the states**, each state's natural limit the largest over its
  successors of (`mNrmMin`₊₁ − the floor) 𝒢 ψ_min / R with the artificial limit inside (lines 369 to 413), which is the
  schemas' recursion; under identical rows the two states' limits coincide, which the adapter asserts.

**On the rest of the standard consumer.**

- **Constructors rebuild what was passed.** HARK 0.17.2 and main replace a transition matrix passed to the Markov
  consumer's constructor with the defaults [[0.9, 0.1], [0.6, 0.4]] without a warning, and rebuild an income process
  assigned after construction on any update; an assigned `IncShkDstn` on the standard consumer must be followed by
  `construct("PermShkDstn", "TranShkDstn")`, since the condition report reads those ([the finding of
  2026-10-21](2026-10-21_hark-markov-for-bst1.md); `rosetta/hark.md`, "The standard consumer").
- **No truncated law, and nodes at bins' conditional means**; the tail options add bins and massless atoms and none
  truncates, so a truncated law needs the adapter's own nodes (Matsya's reading, in the finding of 2026-10-22). HARK's
  `neutral_measure` reweights only the permanent shock, so a solver given those weights integrates against the wrong
  law. The income process's recorded bounds are wrong in four places, among them the rescaling by the unemployment atom
  (draft #1861).
- **Human wealth lags the rule's convergence**; at HARK's default tolerance `hNrm` is 44.99 against its limit of
  50.50, and the rule above the grid is off by 0.0115 at m = 60 (`rosetta/hark.md`, "The tolerance"). HARK names two
  objects `hNrm`, one with this period's income and one without (BSM_0000157).
- **A cubic rule with its limiting line can diverge or jump above the top gridpoint**, which pull request #1848 fixes;
  the adapter reports the rule inside the grid only. A cubic can also lose concavity where an atom sends next period's
  kink back to one point of this period's rule, which no finer grid cures (issue #1869).
- **The newborn cannot be the families'** on main: a newborn draws ψ and gets a transitory shock of one unless
  `NewbornTransShk` draws from the whole mixture, unemployment included; permanent income of one needs the
  `NewbornPermShk` of draft #1860; assets of exactly zero cannot be set through the initial law (the default gives about
  6·10⁻⁶). The Markov consumer's `MrkvPrbsInit` lets a newborn start employed.
- **The targets and condition checks exist only for `IndShockConsumerType` exactly**, in an infinite horizon with one
  period per cycle (`calc_stable_points` in `post_solve`, which returns early for every subclass); the Markov consumer
  has neither, nor an Euler-error function: its four condition methods raise, and its `pre_solve` does not check
  conditions (`rosetta/hark.md`; the HARK session, below).
- **The condition factors depart from the paper's in places**: VAFac without survival (BSM_0000138, draft #1855),
  GPFacLivMod with survival twice (BSM_0000139), the WRIC's and FVAC-PF's messages (BSM_0000154, BSM_0000155), the
  message when the RIC fails (BSM_0000158), no log target (BSM_0000140), all at HARK's main of 2026-10-07.
- **The cyclical index**: the solver and the simulation read the time-varying lists one entry apart in a cyclical
  model, and the owner ruled on 2026-10-31 that they be made consistent, the simulation side to be fixed (BSM_0000159).

**On the Markov consumer in particular.**

- **The per-state interpolation gap.** Released HARK interpolates each next state's marginal value on a grid that starts
  at that state's own natural limit and evaluates it on the current state's grid; when the states' worst incomes differ,
  as they do here, the rule carries a gap of 2.3·10⁻⁴ relative on 200 points and the value is off by up to 30 percent
  near the limit on HARK's default grid. Draft #1858 evaluates each next state's expectation at the current state's
  points, as the standard solver does, and the gap falls to about 10⁻¹⁴ (the finding of 2026-10-21). The adapter has
  depended on that draft's commit since it was written.
- **Human wealth in the Markov solver omits a weight** that matters when the states' return or survival differ (issue
  #1852, pull request #1853, by a HARK maintainer); with identical rows and parameters the weight cancels, so the
  route's solutions are unaffected.
- **What the route costs in machinery.** Two states that solve one rule twice; a chain and an income process that must
  be forced past HARK's constructors and asserted afterwards; a pin on a fork's commit, since neither #1858 nor #1862
  is in a release; the whole diagnostic layer outside HARK; and a result that is the standard consumer's to rounding,
  so that the Markov consumer adds nothing to the solution of the one-state model beyond conditioning on employment,
  which the newborn uses, and the worst state's income as a parameter of its own, which the standard consumer's
  `UnempPrb` and `IncUnemp` also give.

## HARK's pull requests of this line of work

Read on 2026-11-05 from GitHub: every pull request and issue of econ-ark/HARK opened since 2026-10-01, their bodies,
comments, review threads, file lists and changelog entries, with copies kept in the session's scratch. None of the
line's pull requests is merged, and none has a formal review; all are drafts by the owner on `main`, in the two groups
they describe themselves as: the Markov solver and the employment model, and the natural limit with its laws.

| pull request | opened | what it does | stacked on | state on 2026-11-05 |
|---|---|---|---|---|
| #1858, make `MarkovConsumerType`'s solver exact at its gridpoints | 2026-10-21 | each next state's expectation evaluated at the current state's asset points, as the standard solver does; the unconstrained rule starts at the natural limit and the lower envelope applies the artificial one, where before a binding artificial constraint put the first points out of order; NaN below `mNrmMin`; the value built as the standard solver's. Its test holds the Markov consumer to the standard consumer within 10⁻¹² | `main` | draft; its third commit (NaN below the limit) is not in the branches stacked on it |
| #1859, add unemployment as a Markov state | 2026-10-21 | the adapter's construction in HARK itself: the employment income process (employed, the scaled mean-one draw; unemployed, the income while unemployed), the nonpersistent chain, and a parameter set with the standard consumer's defaults, `MrkvPrbsInit = [1, 0]` and `NewbornTransShk`; the rules agree with the standard consumer's to 8.9·10⁻¹⁶ | #1858 | draft; retirement parameters not read; persistent unemployment untested |
| #1860, `NewbornPermShk`, and Markov newborns at their own state's mean transitory income | 2026-10-21 | simulation only: `NewbornPermShk = False` pins the birth-period permanent shock to one, so a newborn starts at P = 1; a `TranShkMean` per state | #1859 | draft; `initialize_sym` refuses the flag |
| #1861, keep the true bounds in a discretized distribution's limit | 2026-10-21 | four places recorded a law's bounds wrongly, among them the rescaling by the unemployment atom; no solver read the bounds at the time | `main` | draft |
| #1863, a truncated lognormal distribution, with a mean-one variant | 2026-10-23 | `TruncatedLognormal` with closed forms and bounds in standard deviations of the log, `MeanOneTruncatedLogNormal`; the discretization records the law's bounds at every node count, and an option adds zero-probability atoms at them | `main` | draft |
| #1862, the natural borrowing constraint from the shock laws' infima | 2026-10-23 | `BoroCnstInfimum`, on by default: the infima's limit imposed as an artificial constraint on top of the atoms' limit, which still anchors the grid; the standard and the Markov solver; distinguished from HARK's earlier attempt of 2025, which made the infima's limit the grid's anchor and was turned off for bad behavior with the value function. The adapter's pin is its first commit | #1858 | draft; declared superseded by a revision, restacked on #1861, planned in issue #1869 and not yet written |
| issue #1869, a proposal marked draft | 2026-10-28 | a shape-preserving cubic under `CubicBool`; an opt-in continuous expectation over the income shocks by Gauss–Legendre quadrature split at the kink; truncation bounds on the standard consumer's income constructor; the revised #1862, with a halt when no point mass sits at the lowest reachable state and `BoroCnstNatCheck` to override it, and `BoroCnstInfimum = False` keeping the atoms' limit for comparisons with the kinked-return type; the Markov solver's rules last | | asks the maintainers not to read it yet; none of its new items is a pull request |

**The maintainers' positions on record.**

- On #1862, 2026-10-23, a maintainer who had tried the infimum approach before: it creates a mismatch between the
  numeric natural limit, from the income nodes, and the recorded one; anchoring the grid at the true limit leaves a gap
  between the lowest gridpoint with positive consumption and the bottom point, where a cubic rule misbehaves because
  the MPC at the lowest nonzero gridpoint is not near one; a tiny point mass at the infimum led to other issues; and
  the kinked-return type needs negative assets to be of use. Issue #1869 answers the three points.
- On 2026-11-05, on seven of the owner's drafts (#1855, #1858 to #1863), a maintainer leaves them unapproved while
  their commits carry `Claude-Session:` trailers, which he wants kept out of HARK's history; the line in the description
  can stay. Removing the trailers means rewriting the branches.

**Adjacent, not of the line:** #1848 (the cubic interpolators' extrapolation above the grid, by a maintainer, open),
#1855 (the FVAC factor discounted by survival, the condition report only, draft), #1853 with issue #1852 (the Markov
human-wealth weight, by a maintainer, open), #1846 (the kinked-return type's cubic segment, merged 2026-10-07), and
issue #1868 (the labeled type's distance infinite while the natural limit moves, no pull request).

**What the line leaves open:** nothing merged or reviewed; the trailer objection; the revised #1862 and the Markov
solver's natural-limit rules unwritten; the stacked branches one commit behind #1858; retirement, persistent
unemployment and the truncation defaults in the employment model; the human-wealth weight's conflict with the group's
edits of the same file.

## The HARK session's account, 2026-11-05 at 12:07 EST

The HARK session, which holds HARK's clone and the drafts, answered the same day. Its unposted work is given by what it
does, as the records' rule for that clone requires; its measurements are its own, with HARK's main at 4c285e86 unless
a draft is named.

**On the standard consumer, measured or read on main.**
- The one-period natural limit always takes ψ's minimum; when next period's lowest resources exceed the worst
  transitory income, which needs an artificial constraint above it, ψ's supremum is the binding one. Read, not run.
- The kink under an artificial constraint is the crossing of two interpolants, not a gridpoint, so its location
  depends on the interpolant: with ℘ = 0.05, ξ_u = 0.5, ℒ = 0.99375, a ≥ 0 and HARK's default nodes it sits at 0.8725
  under linear interpolation and 0.8730 under the cubic, with the lowest employed income node, 0.87281, between them;
  over the last hundred of three hundred simulated periods with twenty thousand agents, the constrained households
  numbered 35,053 under the one and 41,646 under the other. The simulation itself is exact at the atoms: a
  constrained household has c = m and a = 0.
- Human wealth comes from the atoms' mean income; the worst income's probability from the atoms, ℘ with a zero-income
  event and otherwise the product of the lowest atoms' probabilities, a property of the discretization.
- The newborn: the first transitory shock pinned at one unless `NewbornTransShk` draws it, when unemployment can be
  drawn since it is an atom; ψ drawn with growth in the birth period, nothing letting a newborn enter at P = 1; initial
  assets about 6·10⁻⁶ from the default of −12 for the log mean; one of HARK's own simulation tests misspells the flag
  and runs with newborns mismatched, passing either way.
- The model-file route to a population replaces the asset grid by the arrival grid when a twist is specified, and a
  uniform arrival grid's first cell inflates the mass at the constraint: 0.026 on a uniform grid of 801 points to 40
  against 0.018 on a geometric one.
- With HARK's atoms, the cubic rule violates concavity at 200 gridpoints and above.
- `MPCmaxEff` is not in the standard solver; it is in the fast solver, the bequest model and the Markov solver.

**On the Markov consumer.** All four condition methods raise `NotImplementedError` and `pre_solve` does not call the
check; `calc_stable_points` returns early for every subclass, so there is no target; the value function on main is a
linear interpolant of the pseudo-inverse value with its limit suppressed, which #1858 changes; the natural limit and
the worst income's probability come from the atoms per next state and are combined across states, with the top MPC
set to one where the artificial constraint binds. A transition matrix is not a cost on main: the model-file route,
`initialize_sym`, the transition matrices with the previous state's grid given, and the steady state, gives total mass
one for a default Markov consumer; leaving the previous state's grid out aborted the interpreter rather than raising,
which the session traces, unconfirmed, to a compiled helper writing past a one-node grid. Not checked: the employment
chain under the income measure with mortality.

**Its unposted work, by what it does.** A group built from 2026-10-28 to 2026-10-31, reviewed by the owner on
2026-10-29, carries issue #1869's plan: a shape-preserving cubic, a rational cubic of least tension on a segment whose
data are concave but whose cubic is not, used for the standard consumer's rule under `CubicBool`; the lognormal laws'
new names with the old kept; truncation bounds on the standard consumer's income constructor, in standard deviations
of the log, with the laws' bounds recorded; the natural limit from the infima restacked on #1861; an expectation over
independent continuous laws by Gauss–Legendre quadrature in pieces split at kinks the caller gives; a lognormal mixture
with a construction from points; and a continuous solver for the standard consumer, chosen by an option whose default
keeps the atoms bit for bit, in which the employed branch is integrated against its laws with weight 1 − ℘ and the
unemployed branch is a point at its income with weight ℘, zero allowed; the natural limit comes from the infima and the
asset grid starts at the binding constraint; where an artificial constraint binds the grid includes the constraint,
whose endogenous gridpoint is the kink, recorded, with the period before split there; where the natural limit binds,
consumption falls to zero at it with no kink and seventeen asset points are placed by next period's MPC transition,
constants tuned rather than derived. A defect in that solver, found on 2026-11-04 and not yet fixed: where the natural
limit binds without a kink and the zero-income event puts mass on the worst landing, it uses a worst-income
probability of zero, so the top MPC is one instead of 1 − ℘^(1/ϱ) Þ_R, 0.7863 in its test case, and the value misses
the envelope condition by 38 percent just above the limit; the fix, prototyped and tested, uses that mass and sets the
cubic's slope at the limit, and waits on the owner. On the Markov line: persistent unemployment in the employment
states through a mean spell length, with the separation rate set to keep the stationary unemployment rate, on #1860;
and HARK.stationary's Markov value function built as the exact solver builds it. Two branches of 2026-10-23 that the
group superseded are left out of the records at the owner's request of 2026-10-25.

**Its view of a fresh class.** For a nonpersistent unemployment state the Markov route buys only the newborn
convention. A buffer-stock class could keep the standard consumer's one-state machinery and make these first-class:
the laws rather than their nodes, with the natural limit from recorded infima and ψ's infimum or supremum chosen by the
sign of next period's lowest resources less the worst transitory income, so that nothing moves with the node count;
the zero-income event as parameters, ℘ and ξ_u ≥ 0, never a transitory atom, so that the mass at the worst landing is
℘ or zero under densities and the top MPC is 1 − ℘^(1/ϱ) Þ_R exactly, the same value in the solution, the report and
the cubic's slope at the limit; an artificial constraint only when tighter, with a knot at the constraint so that the
kink is its endogenous gridpoint, recorded; expectations against the continuous laws by kink-split quadrature with
atoms kept as an option, and a rule that stays increasing and concave at any grid size; at requested points the rule
and its derivative from the interpolant, the value through its inverse, and Euler residuals computed with the same
expectation operator; the conditions and targets built in, the patience factors named as factors, with `MPCmin`,
`hNrm` and `MPCmax` from the laws; the newborn stated, born employed at P = 1 and k = 0 with its first draw from the
employed branch, the same in simulation and in the transition matrices; the stationary distribution by the model-file
route with nodes at the requested points and at the constraint, geometric above it, under the income measure; the
effective member stated from what was solved, which with laws instead of nodes is the stated member plus the
quadrature; and persistence, if ever wanted, as a Markov extension of the same class rather than another solver.

## The HAFiscal session's account, 2026-11-05

The HAFiscal-Latest session's emitter, the benchmark's private program, has solved the model with the standard
consumer since 2026-10-18, by the endogenous grid method with the cubic rule and the value function; its files were
the gate's reference. Its account, with HARK's line numbers at main 4c285e86 and three scratch computations of the day
on the toy's median type at the first level; one finding, withheld until the owner's word of 12:40:42, is the last
part of this section.

**The standard consumer against the model as stated.**
- The emitter reports its nodes' natural limit as the effective member's, and refuses a natural member whose stated
  limit lies above it, since the checker would hand the stated limit over as an artificial constraint and HARK would
  bind there. It solves a natural member only when the two limits coincide, as they do with a zero-income event, both
  zero. That is the reading above confirmed from the emitter's side.
- When the artificial constraint binds, HARK's `BoroCnstNat` is not the model's natural limit but the one-step limit
  from next period's constraint, −θ_min 𝒢 ψ_min / R: −0.5066 on the toy against the nodes' −5.540. The grid is that
  limit plus `aXtraGrid`, cut by the constraint line, so no gridpoint sits at a = a_Art: the kink fell between
  a = −0.00046 and a = 0.0092, and HARK records no kink. The emitter finds the kink where the rule leaves the
  forty-five-degree line, bracketed by the Euler kink computed from the rule; the two differ by 2.0·10⁻⁶, the
  interpolation's error, which shrinks with the grid. The Markov solver builds its grids the same way.
- The value function is −∞ at `mNrmMin` for ϱ > 1 whichever constraint binds, the pseudo-inverse value being zero
  there with slope `MPCmaxNow`^(−ϱ/(1−ϱ)); the emitter's distribution grid therefore has no node at a natural
  constraint, an early file of the library member having had infinite welfare from exactly that.
- A law with no atom at its infimum still gets one at its lowest node, of mass 1/n for n equiprobable nodes, so
  HARK's MPC at its natural limit is 1 − `WorstIncPrb`^(1/ϱ) Þ_R where the stated model's is one, and the welfare
  conditions see an atom the model does not have; the emitter decides every condition on its effective member, with
  that atom, and says which case applies.
- Human wealth and the limiting MPC are updated by their own recursions and can be unconverged at HARK's default
  tolerance of 10⁻⁶, while above the grid the rule follows their line; the emitter solves at 10⁻⁸ to 10⁻¹² and reports
  nothing above the grid's top. HARK's two conventions for human wealth give 50.5 and 51.5 for its default agent.
- The newborn and the zero-income event as the HARK session says; the emitter sets `UnempPrb` and `IncUnemp` to zero
  and supplies the atoms itself, the event as its own atom with the member's employed scale, and builds the newborn
  itself, born employed at P = 1 with the employed branch and no assets. With `IncUnemp` = 0 HARK's natural limit is
  zero and its worst-income probability is ℘, both right.
- Assigning `IncShkDstn` leaves the two marginals as the constructor's placeholders, which the condition checks and
  the post-solve target read; since its version 0.6 of 2026-10-21 the emitter constructs them after assigning and
  asserts afterwards that HARK rebuilt nothing.
- **The cost of precision by nodes.** On the toy of 2026-10-18, at 7, 15, 31 and 63 equiprobable nodes per shock, the
  Euler residual at the kink was 9.8·10⁻³, 3.9·10⁻³, 1.4·10⁻³ and 5.3·10⁻⁴, about n^(−1.4); the kink moved from
  0.8417 to 0.8298; and HARK's solve time rose from 3.5 to 190 seconds, about linear in the joint nodes (on jhu-dell,
  threads and environment not stated). A residual of 10⁻⁴ near the kink is out of practical reach by refining the
  nodes, which is the case for a continuous expectation.

**What the emitter computes outside HARK, and why.** The discretization, since HARK had no truncated law; the
effective member, with its expectations, lowest values, natural limit, constraint in force and worst income with its
mass under the solver's nodes, every condition decided by the checker's arithmetic on it, because the schema asks for
what was actually solved and HARK's own checks cover neither the schema's set nor, before version 0.6, the nodes
actually used; the stationary population and the income measure by a lottery histogram on an asset grid and one
sparse linear solve, because HARK's simulator is Monte Carlo and its transition matrices place newborns at m = 1, have
no income measure and keep a dense matrix per period, which stopped the refinement of HARK's own Jacobians; the kink
and the two targets by root-finding, since HARK records no kink; the Euler residuals against Gauss–Legendre quadrature
in the logs split where next period's resources cross the kink, with 32 nodes a piece, beside the residual under the
solver's own nodes, the first including the discretization's error and the second the solver's alone.

**The Markov route against the standard consumer.** The gate's outcome as recorded above. The session's own check of
2026-10-20, rerun on 2026-10-27 on a HARK build carrying #1858 to #1860, for the toy's median type: both states'
rules equal the standard consumer's to 2.7·10⁻¹⁵ for m from 0.6 to 50; all 94,985 newborns in twenty thousand
households over six hundred quarters were born employed with permanent income exactly one and an employed first draw;
the cross-section's mean of assets, 0.333084 with a standard error of 1.7·10⁻⁴, against the specification's 0.333075,
cannot tell the newborn rules apart, since a control with the full draw is as close. The benefit seen is the
born-employed newborn in the simulator, which the standard consumer cannot state; with #1858 the solution is the
same, and without it the Markov solver did not reproduce the standard consumer; the cost seen is the route's
dependence on three unmerged drafts. Not measured: the Markov solve's time against the standard consumer's, and the
transition-matrix path under the Markov formulation.

**The finding released on the owner's word.** It is the HARK session's defect, found here independently on 2026-11-04,
and what it adds is that HAFiscal's own continuous solver treats the point mass the same way. A solver that integrates
the income shocks' continuous laws sets the worst-income probability to zero, so its top MPC, the MPC at the natural
limit, is one. That is right only when the worst income carries no mass. With a continuous permanent shock, the worst
income has mass exactly when the worst transitory value is a zero-income point mass: income is then zero whatever ψ
is, with the event's probability ℘, and the limit is 1 − ℘^(1/ϱ) Þ_R with Þ_R = (R β ℒ)^(1/ϱ) / R; with a positive
benefit the worst income ψ_min ξ_u has no mass under a continuous ψ and one is right. HAFiscal's continuous solver,
the one that serves its first estimation step and served the restrained member in the reference probe of
2026-11-04, has a worst-income probability of zero under the continuous laws, so its recorded MPC at the natural
limit is one and so is the slope at its cubic rule's first knot there. It refuses whenever the natural limit binds,
that is, with no artificial constraint or one below the limit its atoms give, so it never solves a natural member as
stated; the assignment is reached only where the artificial constraint sits exactly at the natural limit, as with a
zero-income event and a ≥ 0, both zero, and there the bottom slope and the recorded top MPC are one instead of
1 − ℘^(1/ϱ) Þ_R. It builds no value function, so the envelope-condition error the HARK session measured does not
arise in it. Unaffected: every case where the artificial constraint binds above the natural limit, where the MPC at
the constraint is one by the constrained segment, correctly, which covers the restrained member, the toy-hafiscal
member and HAFiscal's first estimation step; and the reference probe on the restrained member. For the reference's
certified errors near the limit: on the restrained member they hold, as far as this defect goes; a natural member
with a zero-income point mass cannot come from HAFiscal's solver as stated, since it refuses, and through any
continuous solver that member needs the fix, which in HARK's solver is the one prototyped; HAFiscal is to adopt
HARK's continuous solver rather than keep its own, so its copy would not be fixed in place. Not measured: the
defect's size in HAFiscal's solver at a ≥ 0 with a zero-income event; the HARK session's figure for consumption is
its own solver's on its grid.

## What the harness asks of any route

Whatever class solves the model, the comparison needs from it what the results schema and the experiments ask
(`schemas/bst/results.md`, `schemas/experiments.md`, `schemas/constraint-scenarios.md`, `schemas/reference-solution.md`),
and the exactness criterion asks that every choice of the method be refinable without bound, with no default that is
not a valid method (`project-a/exact-definition.md`):

- the stated laws as parameters, truncated lognormals by default and the zero-income event with its probability and
  its income, never a quadrature; the natural limit from the laws' infima, the same at every node count; an artificial
  constraint only where it is tighter than the natural one;
- the natural-constraint case solved as itself, consumption going to zero at the limit with the MPC approaching its
  limit, no kink and no mass at the limit; the artificial case with its kink where a = a_Art and the mass above it; the
  effective member reported with its own lowest values, so that a reader sees which model the code solved;
- the rule and its derivative at requested points, the kink and the two targets, the limiting MPCs, the value;
- the stationary population under both measures with mortality and newborns, which a class can give by a transition
  matrix on an asset grid, as the adapters now do outside HARK;
- the Euler residuals against the stated laws, by a quadrature finer than the household's;
- the condition factors with survival as the paper has them, and verdicts the checker can recompute;
- the newborn as the families state it: employed, permanent income one, no assets;
- settings that name a precision level, nodes, grid and tolerance, each refinable, and a results file whose provenance
  names the versions.

The two modes the ruling of 2026-11-04 asked for would then be one class against HARK's existing types, and the
Markov consumer's place would be a persistent chain, if one is ever wanted, rather than the one-state device.
