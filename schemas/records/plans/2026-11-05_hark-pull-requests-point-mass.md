# Revising HARK's outstanding pull requests for the point mass at the natural limit

**Status: PROPOSED, 2026-11-05 in the afternoon, on the owner's request for a plan; revised the same afternoon on the
HARK session's reading, which corrected the first draft's account of the atoms path and of the halt.** Nothing here
changes HARK: the pull requests are the HARK session's to revise, on the owner's word in that session. The finding it
answers is in [the survey of the Markov route](../findings/2026-11-05_hark-markov-route-survey.md), the HAFiscal
session's last part. The HARK session's measurements cited below were made on 2026-11-05 on HARK's main at 4c285e86
and on its local continuous-expectation work, with ℘ = 0.05, the laws truncated at three standard deviations, seven
atoms per shock and no artificial constraint.

## The bug, stated for the plan

The MPC at the natural borrowing limit is 1 − p^(1/ϱ) Þ_R, where p is the probability that next period's income lands
on its minimum when this period's assets are at the limit. That landing mass depends on the sign of the limit a,
which is the sign of next period's lowest resources less the worst transitory income, the same sign that picks the
permanent shock's end in the limit's own recursion:
- a < 0: the transitory law's mass at its infimum times the permanent law's mass at its infimum;
- a = 0: the transitory law's mass at its infimum alone, since every permanent shock lands there; with a zero-income
  event this is ℘;
- a > 0: the transitory law's mass at its infimum times the permanent law's mass at its supremum, the case of an
  artificial floor above the worst income.

A continuous law has mass zero at either end, a discrete law its atom's mass, a point mass one. So with a zero-income
event p = ℘ whatever the permanent shock, and with a positive income while unemployed and a continuous permanent shock
p = 0 and the MPC at the limit is one (`schemas/constraint-scenarios.md`, "What separates the scenarios"; the HARK
session's landing rule).

Where HARK's solvers stand against this, as measured:
- **The atoms path with the infimum option of #1862 on** gives the model's top MPC in both cases: one with a positive
  benefit, where the infima's limit binds as a constraint, and 0.7862948224 with a zero benefit, which is
  1 − 0.05^(1/2) Þ_R. Its remaining error is in the condition report: the worst income's probability and the weak
  return impatience factor are still taken from the atoms' smallest product, 0.007143 with the positive benefit, where
  the landing mass is zero. The value ℘/N appears in the top MPC only with the infimum option off, where the limit is
  the atoms' too and the pair is the discretized model's, consistent with itself; that path's error is the atoms'
  limit, which #1862 already replaces.
- **The continuous-expectation solvers**, HARK's unposted one and HAFiscal's own, take the landing mass as zero under
  the continuous laws, right with a positive benefit and wrong with a zero-income event: the top MPC comes out as one
  instead of 0.7862948224, and the value function misses the envelope condition by 38 percent just above the limit.
  HARK's fix is prototyped: the landing mass computed in the solver from the laws, and the cubic's slope at the limit
  set from it.
- **The Markov solver's combination** carries per-state masses unchanged, but divides by their chain-weighted sum when
  it forms the expected top MPC; on main that sum is never zero, since atoms always hold mass at their own smallest
  product, and with the laws' masses it can be, which gives a top MPC of NaN. A guard is needed: where the binding
  states' landing mass is zero, the top MPC is one.

## The principle

The landing mass is a property of the laws, not of their discretization and not of the expectation's method, and it
is computed in one place that both expectation paths share: a solver-side function that reads each law's mass at its
ends through the laws' generic interface, which the HARK session's prototype already has, and applies the sign rule.
The event itself needs no new record: the function that adds the unemployment outcome already writes the outcome and
its probability into the transitory law's `limit`, beside the bounds, on main, and the continuous solver reads them
there; with #1861's bounds, `calc_worst_inc_prob` with its infimum option already returns the law's mass, zero or ℘,
on the atoms path. A recorded field would duplicate what the atoms or the laws give and could disagree with them, so
the plan does not add one; if the owner wants a recorded value anyway, it would be the marginal masses at both ends
of each dimension, shaped like the bounds, with the landing still computed by the shared function. A
`ConsBufferStockModel` class would call the same function.

## The changes, pull request by pull request

- **#1861, the true bounds in a discretized distribution's limit.** As posted, with the degenerate lognormal's bounds
  from its local commit. No field is added. Its tests gain the end masses the generic interface reports for a
  continuous law, a discrete law, a point and the law with the unemployment outcome added.
- **#1863, the truncated lognormal.** As posted: the option that adds atoms at the bounds already gives them
  probability zero, so an atom present is not read as a mass.
- **#1862 revised, restacked on #1861 as its own plan says.** Three things. First, the condition report's worst-income
  probability and weak return impatience factor come from the landing mass, not from the atoms' smallest product,
  whenever the infimum option is on; with it off, the atoms stay, for limit and mass alike, for the comparisons with
  the kinked-return type the maintainer wants. Second, the unconstrained rule's bottom slope on the atoms path is left
  as it is: that rule is anchored at the atoms' limit, where the atoms' marginal value is infinite, and the atoms'
  mass is the slope consistent with its gridpoints, while the infima's limit binds above it as a constraint; making
  that slope the model's would be a regression. Third, the halt that #1869 plans, which no branch implements yet, with
  its trigger the owner's decision below. The Markov part, each next state's landing mass by the sign rule and the
  guard on a zero sum, goes with the Markov solver's rules that #1869 places last, or earlier if the owner says.
- **#1858, the Markov solver exact at its gridpoints.** Nothing for the finding. Its third commit, the rule undefined
  below the limit, is missing from every branch built on it, #1859's, #1860's and the posted #1862's; it is added to
  each as a new commit.
- **#1859 and #1860.** Nothing for the finding: the unemployed state's law is a point, whose end mass the generic
  interface reports as one, and the employed state's is a density, so the chain gives ℘ with a zero income while
  unemployed and zero with a positive one through the solver's own combination, once the guard is in. Their content
  waits on the class question below; their trailers are stripped with the rest.
- **The unposted continuous expectation** (#1869's shared expectation and the continuous expectation in the standard
  solver), when posted: the HARK session's prototyped fix as it stands, the landing mass from the laws, the top MPC
  1 − p^(1/ϱ) Þ_R, the cubic's slope at the limit the largest of that, the first segment's secant and the MPC at the
  first knot, and the value function's boundary from it. Its measured numbers are the tests: the top MPC 0.7862948224
  with a slope of 0.7862948227 and an envelope error of 5.5·10⁻⁶ in BST's case; one with a positive benefit; and the
  two paths agreeing on the top MPC in both cases. One quantity on that path still comes from the atoms, human wealth
  and the limiting MPC; whether to take them from the laws' means too is listed below.
- **#1855 and #1827.** Nothing for the finding; they share the trailer condition.
- **Not HARK's pull requests.** HAFiscal's own continuous solver is to be replaced by HARK's, so it is not fixed in
  place. The working group's checker already computes the worst income's mass from the stated laws and the adapters
  report the limiting MPCs from its closed forms, so the harness is unaffected; the stone's departure BSM_0000156, the
  worst income's probability from the atoms, is resolved in the condition report when the plan merges.

## The halt's trigger

Two triggers are on the table, and they differ in one case:
- **#1869's own:** with no artificial constraint at or above the natural limit, the solver halts when the lowest
  reachable next state carries no point mass in transitory income of its own, and names an override. With a positive
  benefit the transitory point mass is there, so the solver goes on and gives a top MPC of one, which both paths do
  today, the continuous one converging in about a hundred cycles.
- **The first draft's:** the halt when the landing mass is zero, which would also halt the positive-benefit case
  under a continuous permanent shock, a case that is solvable and is solved.

The first draft called its trigger "exactly the finding's rule"; it is not. The finding's rule sets the top MPC; the
halt is a separate choice about which models HARK refuses. The owner's ruling of 2026-11-03 abolished the family
without a point mass in the working group's schemas as uninteresting, which says what the group studies and does not
by itself ask HARK to refuse a solvable case. Recommended: #1869's trigger.

## The order, and the rewrites

The maintainer's condition of 2026-11-05, that the drafts stay unapproved while their commits carry session trailers,
is met in a pass of its own on every flagged branch, the Markov group included: the pass changes commit messages
only, every commit's tree is unchanged, and the check against the old branch is an empty diff. The content then
follows as new commits, each rewrite ending with a diff against the old branch that shows only the intended changes.
Each push is a force-push to the fork, on the owner's word in the HARK session. The order follows #1869's and the
stacking:

1. the trailer pass over #1827, #1855, #1858, #1859, #1860, #1861, #1862 and #1863;
2. #1861, with the end-mass tests; #1863 unchanged in content;
3. #1862 revised and restacked on #1861, with the condition report's masses and the halt;
4. #1858's third commit added to the branches built on it; #1859 and #1860 restacked, their content held;
5. the new pull requests of #1869, without trailers from the start: the shape-preserving cubic, the truncation bounds
   on the standard consumer's income constructor, the shared continuous expectation, the continuous expectation in
   the solver with the fix, the mixture; before or after the Markov group as the owner chooses;
6. the Markov solver's rules of #1869's last item, with the landing masses and the guard.

Each description gains a paragraph saying what the landing mass is, where it is computed and who reads it, and names
its tests. The reply to the maintainer's comment of 2026-10-23 on #1862 is written from the paragraph on the revised
#1862: the case he hit, a natural limit binding with no mass at the bottom, keeps its atoms-anchored rule and gains a
top MPC of one where the model's is one, and the shape-preserving cubic answers the cubic's misbehavior. The HARK-dev
status page is the HARK session's to bring current.

## What it costs

Small code: one function shared by the two paths, the condition report's two factors, the Markov guard, the halt, and
tests for each case including the floor-above-the-worst-income case, which no one has measured. The rewrites are the
larger part, and the trailer condition requires them regardless.

## Decisions for the owner

- **The halt's trigger:** #1869's, which halts only where no transitory point mass sits at the lowest reachable state
  (recommended), or the first draft's, which also halts the positive-benefit case.
- **A recorded field or a shared function:** the shared function (recommended), or the marginal end masses recorded
  on each law as well.
- **The trailer pass** as a pass of its own, messages only, before any content (recommended by the HARK session).
- **The Markov group:** #1859 and #1860 restacked with their content held until the `ConsBufferStockModel` class
  decides whether the Markov route is kept; #1858 stands either way (recommended).
- **Human wealth and the limiting MPC on the continuous path:** left from the atoms for now, or taken from the laws'
  means in the same pull request.
- **The Markov solver's rules:** last, as #1869 has them, or with #1862's revision.
