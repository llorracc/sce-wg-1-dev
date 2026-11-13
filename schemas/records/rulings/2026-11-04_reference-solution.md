# Rulings of 2026-11-04

The owner's decisions, in substance and by time (EST). His words are kept outside this public repository.

- **06:23:39, a reference solution is the standard.** Answering [the two questions of
  `comparing-solutions.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/comparing-solutions.md), fidelity and agreement, put to him the evening before with
  [the record of the committed runs](../findings/2026-11-03_two-questions-on-the-committed-runs/README.md), the owner
  rules that the apparatus needs a reference solution of each member, solved to very high precision, and that actual
  solutions at default settings are compared to it. Four requirements, the first two marked as closed:
  1. **A reference solution** at very high precision is what every other solution is compared to.
  2. **Its solver is the continuous solution methods** developed in the HAFiscal and HARK contexts: the expectation
     over the income shocks taken against their continuous laws, split at next period's kink, rather than summed over
     atoms; with the cubic Hermite interpolation that the continuous expectation makes legal; and the natural borrowing
     constraint from the laws' infima.
  3. **A wide and dense grid** for the solution.
  4. **Its ergodic distribution constructed on a dense grid** that extends up to the 99.9th percentile of the wealth
     distribution.

  What it supersedes: the agreement question as the design of 2026-11-03 posed it, a tolerance for two toolkits from
  their own ladders, is replaced by each toolkit's distance from the reference; the fidelity question's two checks become
  the reference's own certification; the ladders of levels become the reference's convergence study, not what a toolkit
  is held to. The precision ladder stays optional for a toolkit, as ruled on 2026-10-17. What stays open: which code
  solves the reference and where it lives, what "default settings" means for each toolkit, the reference's precision
  target and how its error is stated, the distribution grid beyond the percentile, and the form of the comparison's
  report. The proposal that follows is [`reference-solution.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/reference-solution.md); the HAFiscal-Latest,
  HARK-dev and HARK sessions were asked between 06:28 and 06:29 which of their methods solve the members as stated and
  what their toolkits' defaults are.
- **Before 10:19:44, the seven decisions answered in part.** R1, the bench's solve as the provisional reference,
  accepted. R5, the comparison as a report with no verdict, accepted, with the question whether a tolerance makes
  sense only for a seeded simulation. R4 ruled: the harness is silent about method and so has no default settings;
  each Rosetta Stone states three precision levels, with standard names to be proposed (coarse, default and fine
  proposed in the reply). R3 questioned, the residual's points and whether the target bounds its maximum, and answered.
  R6, the distribution's method, to be discussed in more detail. R7's word "ladder" explained. And a registry of every
  run of every toolkit requested, with the tools' exact provenance, everything needed to reproduce a stored result, the
  machine and the time it took, which the standing rule against timings of 2026-10-21 turns into a decision for him.
- **Before 10:56:29, the results schema: the quantiles required, the distribution function at the comparison points
  added.** On R2 the owner asked that the harness ask every toolkit only for statistics computable under any
  representation of its stationary distribution, a grid, a lottery, a simulation or a parametric density, since "its
  grid's top" assumes a grid. Shown that the results document's population block already reports functionals at fixed
  probabilities and a self-reported coverage, and asked whether the quantiles should be required and the distribution
  function of m at the request points added, he ruled: require the quantiles and add the CDF at the request points.
  Applied the same morning to [`bst/results.schema.json`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/bst/results.schema.json),
  [`bst/results.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/bst/results.md), the checker's verifier and the shared emitter: the quantiles required in
  every distribution block; the distribution function F(x) = P(X ≤ x) at the comparison points, in the request file's
  order, for m, a and c under the population measure and m and a under the income measure, required in a type's blocks
  and given in the pooled blocks when the types share the points. Consequence: results files written before this day
  carry no distribution function and no longer validate; the committed runs of 2026-11-01 stay as the record of the
  first design until the experiment's second version supersedes them. What stays open from R2: the broadening of the
  coverage block's `kept` to any representation that loses nothing, proposed and not ruled; and the rest of R2 as
  answered, the reference's own top placed by its precision target and nothing about grids asked of a toolkit.
- **Before 11:31:06, the request rule: points off genuine atoms, and a's own points.** On the HAFiscal session's two
  measurements of the morning, a comparison point sitting on the genuine atom of m at ξ_u and a's distribution
  function at m's points reading m's tail, the owner rules: move request points off genuine atoms and give a its own
  points. Applied the same hour. The request rule moves a point that lands on a genuine atom, m = ξ_u when the
  constraint is artificial at zero and the unemployed income positive, one unit up in its third figure; the request
  file gives a its own points, `a_points`, the stationary quantiles of a at the request probabilities above the
  constraint's atom and the same multiples of its 99th percentile, off a(ξ_u); the results file carries them as
  `a_comparison_points` with a's distribution function at them; the checker flags a comparison point at a genuine atom
  and holds a's function to a's points. Consequences: the generated requests of toy and iid-ui-artificial change; the
  four committed request files of restrained-limit, written by hand, give a no points, so runs on them carry a's
  function nowhere until the experiment's second version regenerates them; the field required for m alone stands, c's
  optional. Pooled points for multi-type members remain open.
