# Where a method attaches, Matsya's third session on HARK's source, and a natural constraint in HARK

Found on the afternoon of 2026-10-22. The bellman session ran Bellman's own check of a methods file against the schemas'
stage files and reported what it admits; Matsya's third session read HARK's source. Both are recorded here in substance.
Bellman's documentation is not published (its site returned "Site not found" that day, and its repository is private),
so the schemas state the rules below as their own and cite no Bellman page ([checkable
sources](../memory/feedback_checkable-sources.md)).

## What Bellman's check admits on `bst/1`

Run on `bst/1`'s stage file at `69efda7` (the operator then `E_ψ_θ_z`) and again with #10's names (`E_ψ_θ_j`), with no
calibration needed. Bellman lists the stage's places as five blocks (`arvl_to_dcsn`, `dcsn_to_cntn`, `cntn_to_dcsn`,
`dcsn_to_arvl`, `policy`), nine named lines, and two operators, the joint expectation and `policy.euler.solve`.
- **An expectation's method goes on its operator.** `!quadrature` on the block `dcsn_to_arvl` is refused, and so is a
  method on one of its lines. On the operator's name it is admitted, and binds at the expectation in both lines.
- **`!egm` needs the method's own lines.** It is refused on `policy`, since the block writes neither the endogenous grid
  (m = a + c) nor a maximization carrying its first-order condition. Renaming the Euler line does not help. As the stage
  is written, the solution's method goes on `policy.euler.solve`: `!time-iteration` or `!root-find`. Bellman's own
  buffer-stock stage admits `!egm` because its policy block writes the inverted Euler equation, the endogenous grid and
  the choice; a constrained version adds a slackness line. The owner ruled at 15:11:02 that `bst/1` stays free of any
  method's lines.
- **`evaluate` is no target in `bst/1`.** The interpolation goes on `policy` (`!Linear` is admitted there, and on
  `cntn_to_dcsn.value`). `!time-iteration` on `policy.euler.solve` and `!Linear` on `policy` bind at two places and
  stand in one file.
- **Only Bellman's tags are methods.** A toolkit's own name as a method is refused everywhere; a toolkit's routine goes
  in `handler:`. A handler with no method is admitted on an operator and on a block, and refused on a line.
- **Settings.** A setting the tag does not name is refused without a handler and admitted with one. `!Linear` names
  `orders` (points by coordinate), `bounds` (a pair by coordinate) and `grid`; `!histogram` names `orders` and `bounds`;
  `!gauss-hermite` names `n_nodes`; `!monte-carlo` names `n_paths` and `seed`; `!quadrature` and `!sum` name none.
- **One target, one method.** Two entries on one target are refused. Bellman does not check that a law is finite, so
  `!sum` against `!quadrature` is the author's statement: `!quadrature` for nodes that approximate continuous laws.
- **A whole-stage handler** has no place: a handler on `policy.euler.solve` binds to the solve alone, and a handler for
  a whole block stands on the block. What else a toolkit's solver does is the card's `interior_policy`, which Bellman
  does not record.
- **The Markov family.** One operator takes one method, so `!exact-markov` for the chains and `!quadrature` for the
  shocks cannot both stand on E_{reg,j,ψ,θ}. Splitting it inside one line elaborates, but the two expectations form one
  place; two methods need the inner expectation on its own line, marked as a node of its own, a spelling not yet tried.

After #11 the two cards' entries on stage targets and the adapter's method file were run through the same check on the
stage file with #10's names, and all were admitted.

## ϱ in Bellman

On `bst/1`'s stage file and the community library's calibration at `69efda7`: the stage elaborates, the calibration's
key ϱ binds, and no ρ appears. A compiled kernel spells ϱ as ρ and ℒ as L in its Python arguments, which bind by
position, and its values are right. A stage declaring both ρ and ϱ gets the second renamed with a suffix, and both
compute correctly. The pitfall is Python's: `stage.par.ϱ` in Python source reads `stage.par.ρ`, an error on these files
and a silent misread only where a stage declares both; `stage.par["ϱ"]` is exact. Nothing in Bellman needed changing for
#9.

## Matsya's third session, on HARK's source

Run from the bellman session, 14:52 to 15:09, on the owner's word there, with six excerpts of HARK's code at `4c285e86`,
each checked block by block against HARK's own files (67 blocks, none differing), beside the brief, the stage file and
the two members as the second session had them. Six turns, all answered, citing the excerpts and HARK's published pages.
Its answers are kept outside this repository. What they settle, all of it on HARK's standard consumer at that commit:
- **The income process.** The unemployment atom comes first and the employed atoms are rescaled to θ(1 − ℘ξ_u)/(1 − ℘),
  so the transitory mean is one; the joint law is the independent product, permanent shock first. HARK's
  `neutral_measure` reweights only the permanent shock by ψ, so a solver given those weights would integrate against the
  wrong law.
- **Discretization.** Equiprobable atoms at their bins' conditional means; the tail options add bins and massless atoms,
  and none truncates, so a truncated law needs the adapter's own distribution.
- **The solver.** Survival enters once, in DiscFac·LivPrb; the natural limit comes from the discretized minima; the grid
  is aXtraGrid above it; under `CubicBool` the slopes are the MPCs, dcda/(dcda + 1).
- **The defaults.** `aXtraNestFac` = −1 gives a uniform grid. `pre_solve` does not rebuild `IncShkDstn`; only the income
  process's update does. The stable points are computed only for an infinite horizon.
- **The stationary distribution.** At this commit the transition-matrix methods belong to another consumer type; the
  other route is the simulator.
- **Newborns.** Assets of exactly zero cannot be set through the initial law (the default gives about 6·10⁻⁶); permanent
  income of one is the default; by default a newborn draws ψ and gets a transitory shock of exactly one, and with
  `NewbornTransShk` the full joint draw, unemployment included.

Each of these agrees with HARK's Rosetta Stone as revised in #11. The answers use the members' names of that commit (ρ,
ξ_min), not the registry's.

**What it does not establish:** anything about HARK's Markov solver, which the adapter uses at #1858's commit and which
this session's own reading of that commit, and the adapter's gate, cover.

## A natural constraint in HARK (evening)

Measured on the toy member with its borrowing constraint written `natural` (stated `a_Nat` = −1.729), at level 1 (7
nodes per shock), with HARK at the adapter's pin:
- **HARK's own limit from the nodes** (no artificial constraint): −5.54, the closed form of the lowest nodes, which
  HARK's iteration reached to 9·10⁻⁸. The stationary population then holds −4.82 in assets on average, below the stated
  limit, and the Euler residuals against the stated laws are not defined at the low request points: those laws send next
  period's resources below HARK's limit, so no valid results file is written.
- **Zero-probability atoms at the laws' infima**, so that HARK's minimum over its atoms finds them: the value function
  is not finite at 1,539 of 2,000 points, and the lower limit comes out at −0.513 rather than −1.729. A zero weight
  meets an infinite value in HARK's expectation.

So computing the stated limit in HARK needs its solvers to read each law's lower bound directly, not the lowest atom;
the owner's clarification of 18:18:56 asks for that, and the HARK session is drafting it.

**HARK's own change** (draft econ-ark/HARK#1862, `11852805`): its standard and Markov solvers take the natural limit
from each distribution's recorded infima by default. On HARK's defaults with both laws truncated at three standard
deviations, the limit is −0.782670 at 5, 7, 15, 40 and 200 nodes, where the nodes alone give −1.706, −1.524, −1.255,
−1.052 and −0.880; with the option on, the solution equals one with that limit as an artificial constraint to about
10⁻¹⁵.

**The adapter at that commit** (#12): the toy stated `natural` is solved under −1.729 at 5 and 9 nodes per shock, HARK's
iteration stopping 4·10⁻⁹ above it at level 1, and its results file passes the checker. The limit binds in the effective
member, whose nodes would allow −5.54, and the Euler residuals against the stated laws are large near it, where those
laws' worst draws leave nothing to consume. The toy and the library member as filed give results identical to the old
pin's.
