# HARK's Markov consumer for `bst/1`

Found on the evening of 2026-10-21, for HARK's adapter, which the owner ruled is to solve `bst/1` with HARK's
`MarkovConsumerType` rather than its standard consumer, as the nonpersistent chain of the Markov family's nesting.

**The mapping.** Two states, employed E and unemployed U, with every row of the transition matrix [1 − ℘, ℘]. E's income
is ψ's nodes times θ's nodes scaled by (1 − ℘ξ_U)/(1 − ℘). U's is ψ's nodes times a point mass at ξ_U, since ψ is still
drawn. Return, growth and survival are the same in both states. The artificial constraint is `a_Art`, or none. Newborns
start in E. The HARK session confirmed the mapping, and HARK's draft pull request #1859 builds the same process.

**What was measured.**
- **HARK 0.17.2 replaces a transition matrix passed to the constructor** with its own defaults, [[0.9, 0.1], [0.6, 0.4]],
  with no warning. HARK's `construct()` rebuilds every key that has a constructor, and a later `update()` rebuilds an
  income process assigned after construction. Main behaves the same way. The adapter sets those constructors to none and
  asserts the matrix and the income process it solved with.
- **With the right matrix the two states' rules are identical** (difference 0.0), and so are their values. The natural
  limit, the limiting MPC and the MPC at the lower limit equal the standard consumer's.
- **The Markov rule still differs from the standard consumer's on HARK 0.17.2 and main.** The gap grows with m and does
  not depend on the convergence tolerance: 2.3e-4 relative on a linear rule with 200 grid points, 4.0e-5 at 800 and
  2.1e-6 at 3,200, and 5.4e-7 with a cubic rule at 200.
  - A one-state Markov consumer given the standard consumer's own distribution matches it to 3e-15. So does a two-state
    one with that distribution in both states.
  - The gap comes from the solver: it interpolates each next state's marginal value on a grid that starts at that state's
    own natural limit, then evaluates it on the current state's grid.
  - The HARK session measured the same on main. On HARK's default grid the rule's gap reaches 1e-2, and the value function
    is off by 8–30% within 0.04 of the lower limit, 2–4e-3 in the middle and about 3% at high wealth.
- **HARK's draft pull request #1858 removes the gap.** It evaluates each next state's expectation at the current state's
  points, as the standard solver does. It also orders the rule's first points correctly at a binding constraint and builds
  the value function as the standard solver does. On it, the rule and the value agree with the standard consumer to about
  1e-14, and the MPC to 4e-14. Hence the owner's pin.

**HARK's other gaps for the Markov consumer:**
- It has no condition checks, limiting values, Euler-error function or targets. The adapter takes those from the
  schemas' checker, and the limiting MPCs from the solution, per state.
- Human wealth lags its limit even at a tolerance of 1e-10, so the adapter reports the closed form.
- Above the grid, a cubic rule with a limiting line diverges or jumps at the top gridpoint, which HARK's draft #1848
  fixes. Cubic values are reported inside the grid only.
- HARK has no Markov transition matrix of its own. The emitter's own population, Young's lottery with newborn replacement
  and Harmenberg's measure, stays exact for this chain, since the next state does not depend on the current one. The Markov
  family will need the joint state (a, s), as in Auclert, Bardóczy, Rognlie and Straub (2021).
- Newborns: use HARK's `NewbornTransShk` and an initial state of E. Newborn assets are an exact zero only with a point mass
  in place of HARK's default initial law.

**The gate before the adapter is public**, as the HAFiscal-Latest session proposed and this session adopted. At each
precision level:
1. measure the gap between the Markov and standard rules on a fine m grid;
2. compare the adapter's results file with the emitter's field by field, within about 100 times that gap. Use relative
   differences for levels and absolute ones for numbers near zero. Allow for amplification at root-found points and in the
   far tail;
3. `check.py --verify-results` passes.

A difference near a level's convergence size is then a failure to explain, not a pass.

**From the community-library session's harness work:**
- Python normalizes identifiers, so a keyword argument named ℒ arrives as L. Schema symbols are passed as string keys.
- The natural limit uses the lowest node actually used, not the law's infimum.
- The value function needs a grid starting about 1e-6 above a zero-income or natural limit.
- Near a binding artificial limit, solvers agree to about 1e-5, not round-off.
- A grid's top should lie well above the largest point evaluated.

**What it does not establish:** the adapter itself, the gate's outcome, and anything about the Markov family's own
chains.
