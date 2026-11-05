# Revising HARK's outstanding pull requests for the point mass at the natural limit

**Status: PROPOSED, 2026-11-05 in the afternoon, on the owner's request for a plan.** Nothing here changes HARK: the
pull requests are the HARK session's to revise, on the owner's word in that session, and this plan goes to that session
for its reading first. The finding it answers is in
[the survey of the Markov route](../findings/2026-11-05_hark-markov-route-survey.md), the HAFiscal session's last part.

## The bug, stated for the plan

The MPC at the natural borrowing limit is 1 − p_worst^(1/ϱ) Þ_R, where p_worst is the probability that next period's
income is at its worst. With a zero-income event of probability ℘, income is zero whatever the permanent shock, so
p_worst = ℘. With a positive income while unemployed and a continuous permanent shock, the worst income ψ_min ξ_u
carries no mass, p_worst = 0, and the MPC at the limit is one. With a genuinely discrete permanent shock and a
positive benefit, p_worst is ℘ times the mass at ψ_min (`schemas/constraint-scenarios.md`, "What separates the
scenarios").

HARK's solvers get this wrong in two opposite ways, and right only in between:
- **The atoms-based solvers**, the standard consumer's and the Markov consumer's, take p_worst as the mass of the
  smallest product of the discretized atoms (`calc_worst_inc_prob`; the Markov solver per next state, combined through
  the chain). With a zero-income atom that is ℘, right. With a positive benefit and a continuous permanent shock
  discretized to N atoms it is ℘/N, where zero is right: a value of the discretization, not of the model (the stone's
  departure BSM_0000156).
- **The continuous-expectation solvers**, HARK's unposted one and HAFiscal's own, take p_worst as zero under the
  continuous laws, right with a positive benefit and wrong with a zero-income event, where ℘ is right: the MPC at the
  limit comes out as one instead of 1 − ℘^(1/ϱ) Þ_R, 0.7863 in the HARK session's test case, and the value function
  misses the envelope condition by 38 percent just above the limit (the survey).

What depends on p_worst: the top MPC and the cubic rule's slope at the limit, the value function's boundary, the weak
return impatience factor p_worst^(1/ϱ) Þ/R and its condition, and the rule of the revised #1862 that halts when the
natural limit binds without a point mass at the lowest reachable state.

## The principle

The mass at the worst income is a property of the law, not of its discretization and not of the expectation's method.
So it is recorded once, on the law beside its bounds, by whatever constructs the law, and every solver reads it there:
the atoms-based solvers in place of the atoms' product, the continuous solvers in place of zero. One place computes it,
and the two expectation methods then agree on the limit exactly, which is also what a `ConsBufferStockModel` class
would read. This is the same move #1862 made for the natural limit itself: the bound from the law's recorded infimum
rather than from the lowest atom.

## The changes, pull request by pull request

- **#1861, the true bounds in a discretized distribution's limit.** Beside `infimum` and `supremum`, each law's `limit`
  records the mass the true law puts at its infimum: zero for a continuous law; the atom's mass for a discrete one;
  one for a degenerate law. `add_discrete_outcome_constant_mean` sets the transitory law's mass at its infimum when
  it adds the unemployment outcome: the outcome's probability when the outcome lies below the rescaled law's infimum,
  which is then the new infimum; that probability plus the law's own mass when they coincide; the law's own otherwise.
  `make_univariate` keeps the joint law's record, as #1861 already keeps its bounds. A joint law's worst-income mass
  follows the rule above: with a zero transitory infimum, the transitory mass alone; otherwise the product of the two
  laws' masses at their infima. Tests on each case, and on the degenerate lognormal whose bounds #1861's local commit
  already fixes.
- **#1863, the truncated lognormal.** Its `limit` records mass zero at both bounds, and the option that adds
  zero-probability atoms at the bounds leaves the mass zero: an atom present and a mass are two different things, and
  the solver must not read the first as the second.
- **#1862 revised, restacked on #1861 as its own plan says.** `calc_worst_inc_prob` with the infimum option returns the
  recorded worst-income mass rather than summing atoms at the product of the infima; the standard solver calls it with
  that option whenever `BoroCnstInfimum` is on, so `MPCmaxUnc` is the model's; `BoroCnstInfimum = False` keeps today's
  atoms for the limit and the mass alike, for the comparisons with the kinked-return type the maintainer wants. The
  halt planned in #1869 is then exactly the finding's rule: when the natural limit binds, no artificial constraint at or
  above it, and the recorded mass at the worst landing is zero, the solver halts, says why, and names
  `BoroCnstNatCheck = False` as the override. This answers the maintainer's comment of 2026-10-23 on its own ground: the
  case he hit, a natural limit binding with no mass at the bottom, is the case the solver now refuses; where it does
  solve, the slope at the limit is the model's, 1 − p_worst^(1/ϱ) Þ_R, and the cubic is anchored by it. The Markov
  solver's part, each next state's recorded mass combined through the chain over the states that set the limit, as its
  code combines the atoms' masses today, goes with #1862's Markov checks or with the Markov solver's rules that #1869
  places last, the owner's choice below.
- **#1858, the Markov solver exact at its gridpoints.** Nothing for the finding. Its third commit, the rule undefined
  below the limit, is carried into the branches stacked on it, which lack it.
- **#1859, unemployment as a Markov state.** The employment income process records the masses: the unemployed state's
  transitory law is a point at the income while unemployed with mass one, the employed state's law has mass zero at its
  infimum under continuous laws, and the chain's ℘ then gives p_worst = ℘ with a zero income while unemployed and zero
  with a positive one, through the solver's own combination. Its test that the Markov statement matches the standard
  consumer gains the two cases of the limit's MPC, exact rather than within 10⁻¹².
- **#1860, the newborn.** Nothing for the finding.
- **The unposted continuous expectation** (#1869's `expected_continuous` and the continuous expectation in the standard
  solver), when posted: the HARK session's prototyped fix, made general by reading the recorded mass rather than
  computing it in the solver: p_worst from the law, the top MPC 1 − p_worst^(1/ϱ) Þ_R, the cubic's slope at the limit
  the largest of that, the first segment's secant and the MPC at the first knot, and the value function's boundary from
  it. Tests: BST's own case gives the HARK session's numbers, the top MPC 0.7862948224 and the envelope error of order
  10⁻⁶ in its test case; a positive benefit gives mass zero and the halt without an artificial constraint; and the atoms
  path and the continuous path give the same top MPC in both cases, which also retires BSM_0000156.
- **#1855 and #1827.** Nothing for the finding; they share the trailer condition below.
- **Not HARK's pull requests.** HAFiscal's own continuous solver is to be replaced by HARK's, so it is not fixed in
  place. The working group's checker already computes p_worst from the stated laws and the adapters report the limiting
  MPCs from its closed forms, so the harness is unaffected; the HARK stone's departure BSM_0000156 is resolved when the
  plan merges.

## The order, and one rewrite per branch

The maintainer's condition of 2026-11-05, that the drafts stay unapproved while their commits carry session trailers,
means every branch's history is rewritten anyway. The plan rewrites each branch once: the trailers stripped, the
branch restacked, and the finding's changes added, then force-pushed to the fork on the owner's word in the HARK
session, each push his to approve there. The order follows #1869's and the stacking:

1. #1861, with the recorded masses;
2. #1863, with mass zero at its bounds;
3. #1862 revised, restacked on #1861, with the mass-based top MPC and the halt;
4. #1858 with its third commit, then #1859 with the recorded masses, then #1860, each restacked;
5. the new pull requests of #1869, without trailers from the start: the shape-preserving cubic, the truncation bounds
   on the standard consumer's income constructor, the continuous expectation with the fix, the mixture; before or
   after the Markov group as the owner chooses;
6. the Markov solver's rules of #1869's last item, if not taken with #1862.

Each description gains a paragraph saying what the mass at the worst income is, where it is recorded and who reads it,
and names its tests. The reply to the maintainer's comment on #1862 is written from the paragraph above. The HARK-dev
status page is the HARK session's to bring current.

## What it costs

Small code: a field on the law, one function's option made exact, the constructor's bookkeeping, the solver's halt; a
test for each case; and the rewrite of seven branches, which the trailer condition requires regardless. The risk is in
the rewrite, not in the change: a branch restacked by hand can lose a commit, as the stacked branches have already lost
#1858's third, so each rewrite ends with a diff against the old branch that shows only the intended changes.

## Decisions for the owner

- **Where p_worst lives:** on the law, recorded by its constructor and read by every solver (recommended), or computed
  in each solver from the event's parameters, which covers neither hand-built distributions, the adapters' among them,
  nor the Markov states.
- **The case without a point mass:** the halt with an override, as #1869 plans (recommended, since the owner abolished
  that scenario's family as uninteresting on 2026-11-03), or solving it with the MPC at the limit equal to one.
- **The rewrite:** one rewrite per branch now, trailers and the finding together, with his word in the HARK session for
  each force-push.
- **The Markov group:** revised as above, or left as it stands until the `ConsBufferStockModel` class decides whether
  the Markov route is kept at all; #1858 is a correctness fix to HARK in either case.
- **The Markov solver's rules:** with #1862's revision, or last as #1869 has them.
