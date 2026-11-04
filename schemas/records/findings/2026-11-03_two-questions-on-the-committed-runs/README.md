# The two questions, put to the committed runs

2026-11-03, in the evening, on the owner's request to pursue the design of
[`comparing-solutions.md`](../../../comparing-solutions.md) and put its two questions to him. The design separates
**fidelity**, one toolkit against the stated member, from **agreement**, two toolkits against each other, and says what
each check needs. This record puts both questions to the restrained-limit suite's committed runs of 2026-11-01, HARK's
and dolo's ([HARK's run](../2026-11-01_restrained-limit-suite-hark/README.md),
[dolo's run](../2026-11-01_restrained-limit-suite-dolo/README.md)), and to one more run per toolkit and member, the
method-only step the design asks every ladder to hold. The tables are in [`report.md`](report.md), written by
`two_questions.py` from the results files; nothing in this record is solved by hand.

## What was run

- **The report.** `two_questions.py` reads the twenty-four committed results files, the eight of the method-only step,
  and the four parameter files, whose closed forms it takes from the checker; it solves nothing:

  ```sh
  uv run --with jsonschema --with pyyaml --with scipy --with referencing --with numpy \
      python schemas/records/findings/2026-11-03_two-questions-on-the-committed-runs/two_questions.py
  ```
- **The method-only step.** Each adapter, in its locked environment, on each of the four members, at level 4's grids
  with level 3's nodes: the household's and the population's laws on 31 nodes per shock as at level 3, the solution
  grid of 2,400 points to m = 800, the distribution grid of 32,000 points to m = 480, and for dolo the rule's grid of
  160,001 points, against level 3's 1,200, 16,000 and 80,001. The request files are the suite's:

  ```sh
  uv run --project harness/envs/<toolkit> --frozen python harness/adapters/<toolkit>/adapter.py \
      schemas/bst/<scenario>/members/<member>.yaml --out <dir> --level 4 --nodes 31 \
      --request schemas/bst/experiments/restrained-limit/<member>.request.yaml
  ```

  The eight results files, with their method and settings files, are in `method-only/<toolkit>/<member>/level-4-nodes-31/`.
  Each validates and is consistent with its member under `check.py --verify-results`. Their effective members are
  level 3's, name for name: the step changed no representation, which is what makes it method-only, and the report
  reads that from the files rather than from the settings.

## Question 1. Did this toolkit solve the stated member?

The design answers with two checks that can fail: the effective member approaches the stated member's closed forms
along the ladder, or sits at a round-off floor; and the Euler residual under the stated laws falls along the ladder.

**The effective member.** The two adapters share one representation of the laws at every level, equiprobable bins
with exact conditional means on 7, 15 and 31 nodes per shock, so their effective members agree to 3 · 10⁻¹⁵ and one
table serves both. The named expectations approach the closed forms by a factor of about 2.9 per level: E[ψ²] sits
6.2 · 10⁻⁴, 2.1 · 10⁻⁴ and 7.3 · 10⁻⁵ from its closed form at the three levels, E[ψ⁻¹] and E[ψ^(1−ϱ)] a little less,
E[log ψ] and E[ψ log ψ] about half as far. Three names sit at the floor from the first level: the two means, which
the construction makes exact, and E[ψ^(ϱ−1)], which is E[ψ] when ϱ = 2. For the restrained member a fourth name does
not approach in the way the others do: the worst income's mass, which the stated member puts at zero and a
representation on N nodes per shock puts at 1/N², is 2.0 · 10⁻², 4.4 · 10⁻³ and 1.0 · 10⁻³. It falls, by about 4.4 per
level, and it can never reach zero on a finite representation.

Two things follow for the check as the design states it:
- **The floor is necessary, not a nicety.** The distance of E[ψ] from its closed form is 0, 1.1 · 10⁻¹⁶ and 2.2 · 10⁻¹⁶
  at the three levels: it rises. A check that only asks the distance to fall fails the one name the representation
  gets exactly right. With the floor at 10⁻¹² the three exact names pass at every level and the others are asked to fall.
- **The metric must be absolute where the closed form is zero.** The worst income's mass has closed form 0 for the
  restrained member; a relative distance is undefined there. The experiment schema's `max_relative_difference`, which
  divides by the larger of one and the magnitude, already handles it, and the report uses that definition.

**The Euler residual under the stated laws.** It falls along both toolkits' ladders for every member: by a factor of
2.9 to 4.2 per level for seven of the eight toolkit-and-member pairs, and by 1.17 per level for dolo on ℘ = 0.00005,
whose residual at level 3 is 6.9 · 10⁻³ against HARK's 1.8 · 10⁻⁴. The check passes everywhere. What tells the two
cases apart is the residual under the toolkit's own representation of the laws, which the results schema makes
optional and both adapters report:

| member | toolkit | under the stated laws, level 3 | under its own laws, level 3 | what remains at level 3 |
|---|---|---|---|---|
| ℘ = 0.005 | HARK | 1.2 · 10⁻⁴ | 4.6 · 10⁻⁹ | the representation's |
| ℘ = 0.005 | dolo | 1.2 · 10⁻⁴ | 7.7 · 10⁻⁵ | both |
| ℘ = 0.0005 | HARK | 1.6 · 10⁻⁴ | 3.6 · 10⁻⁷ | the representation's |
| ℘ = 0.0005 | dolo | 8.3 · 10⁻⁴ | 8.3 · 10⁻⁴ | the solver's |
| ℘ = 0.00005 | HARK | 1.8 · 10⁻⁴ | 4.4 · 10⁻⁵ | mostly the representation's |
| ℘ = 0.00005 | dolo | 6.9 · 10⁻³ | 6.9 · 10⁻³ | the solver's |
| restrained | HARK | 2.1 · 10⁻⁴ | 5.7 · 10⁻⁷ | the representation's |
| restrained | dolo | 2.1 · 10⁻⁴ | 9.6 · 10⁻⁷ | the representation's |

For HARK the residual under its own laws falls by a factor of 9 to 17 per level, so at level 3 what is left under the
stated laws is the representation's: the 31-node discretization of the laws, which the next level halves. For dolo on
the two smaller probabilities the residual under its own laws equals the residual under the stated laws: the solver,
not the representation, is what has not converged.

**Where it sits, and why it is large.** At the request points up to about m = 0.3, where the zero-income event
decides the Euler equation. The three natural members have a closed form there: the MPC at the natural constraint,
1 − ℘^(1/ϱ) Þ̊_R, BST's maximal MPC, which is 0.932063, 0.978517 and 0.993206 for the three probabilities. HARK's rule
has that slope at m = 10⁻⁶ to one part in 10¹⁴ at every level, since HARK builds the limit into its rule. dolo's slope
there falls short of it, relatively, by 8.2 · 10⁻⁴, 2.3 · 10⁻⁴ and 6.1 · 10⁻⁵ at the three levels on ℘ = 0.00005, and
by less on the larger probabilities, so dolo's solver error at the constraint falls by 3.5 to 3.8 per level like its
other errors.
The Euler residual multiplies that small error by a large factor. At m = 0.01 on ℘ = 0.00005 the household saves
(1 − 0.9932) m ≈ 7 · 10⁻⁵, and the zero-income event, which takes next period's resources to that saving alone, carries
a marginal utility near 2 · 10⁸, so that with probability 0.00005 it outweighs the employed branch by about ten thousand
to one. A relative error ε in the slope is an error ε / (1 − κ̄) ≈ 150 ε in the saving, and the residual, relative to
c, is about that: 1.3 · 10⁻³, 3.0 · 10⁻⁴ and 8.0 · 10⁻⁵ predicted against 1.3 · 10⁻³, 2.8 · 10⁻⁴ and 3.2 · 10⁻⁵
reported on ℘ = 0.005; 1.3 · 10⁻², 3.5 · 10⁻³ and 8.0 · 10⁻⁴ against 1.3 · 10⁻², 3.5 · 10⁻³ and 8.3 · 10⁻⁴ on
℘ = 0.0005. On ℘ = 0.00005 the prediction exceeds what the residual can show: the residual is defined as the smaller
of the Euler equation's implied change in consumption and the saving itself, divided by c, and dolo's continuation
there implies consuming everything, so the reported residual is the saving over c, 7.7 · 10⁻³, 7.1 · 10⁻³ and
6.9 · 10⁻³ at the three levels. That cap is why it falls by only 1.17 per level: the underlying error falls by 3.5 to 3.8. Across the method-only
step, which halves dolo's grid spacing, dolo's residual under its own laws falls from 6.9 · 10⁻³ to 2.3 · 10⁻³ on
℘ = 0.00005 and from 8.3 · 10⁻⁴ to 1.7 · 10⁻⁴ on ℘ = 0.0005, and HARK's from 4.4 · 10⁻⁵ to 2.8 · 10⁻⁶ and from
3.6 · 10⁻⁷ to 2.5 · 10⁻⁸; the residual under the stated laws does not move across the step for HARK on any member,
nor for dolo on the restrained member and ℘ = 0.005, where what remained was the representation's.

So the first question has a verdict and three findings beside it. Both toolkits pass both checks on every member. The
pass criterion "falls along the ladder" passed a residual pinned at its cap, whose rate says nothing about the solver.
The number that says what has and has not converged is the residual under the toolkit's own laws, which only the
toolkit can compute and which the schema does not require. And the model has a closed form for the rule itself at the
natural constraint, which one toolkit reproduces to round-off and the other approaches, that no check uses.

## Question 2. Do the two toolkits' solutions coincide, and within what?

The design answers that agreement is reported and classed, never failed, and that the tolerance of the class "within
the solvers' convergence" comes from a method-only step, since a step that changes the representation moves both
toolkits alike and measures nothing about either solver.

**On the absolute scale, at the request points with m ≤ 20,** the two rules differ at level 3 by 1.1 · 10⁻⁵ to
2.4 · 10⁻⁵, and each toolkit's own rule moves by 3.3 · 10⁻³ to 3.5 · 10⁻³ between levels 2 and 3, a step that moves
the effective member and so changes the representation. The check `within_own_convergence` of the experiment's second
version, the sum of the two movements, would accept a difference three hundred times the one observed; the finding of
2026-11-02 said as much. **Across the method-only step** each toolkit moves by 4.1 · 10⁻⁷ (HARK) and
8.1 · 10⁻⁶ (dolo) on the restrained member, and the two differ at that step by 2.9 · 10⁻⁶;
across the four members HARK moves by 7.4 · 10⁻¹¹ to 4.1 · 10⁻⁷ and dolo by 8.1 · 10⁻⁶ to
1.8 · 10⁻⁵, against differences at level 3 of 1.1 · 10⁻⁵ to 2.4 · 10⁻⁵ and at the step of 2.9 · 10⁻⁶ to 6.1 · 10⁻⁶.
The difference between the two toolkits at level 3 is dolo's own grid error, member by member. The sum of the two
movements is the tolerance the design's class "within the solvers' convergence" asks for, and every member's
difference lies within it, where the representation step's tolerance would have been three hundred times wider. The
report read the step as method-only from the files, the effective member having moved by exactly zero.

**On the relative scale, over all 39 points,** which the stone guide asks for the rule, the picture changes where it
should. For the restrained member and ℘ = 0.005 the largest relative difference at level 3 is 1.0 · 10⁻⁵, at m = 50.
For ℘ = 0.00005 it is 6.3 · 10⁻⁵, at m = 0.01, six times larger, and it sits exactly where dolo's residual sits. The
absolute scale, with c ≈ 0.01 there, cannot see it. The relative difference falls with the level for every member, by a
factor of 3 to 4.

## What it establishes, and what it does not

- **The design's two checks of fidelity can be evaluated from results files alone,** and both toolkits pass them on
  every member, with the floor and the absolute metric that the restrained member's exact names and zero closed form
  require.
- **The residual under the toolkit's own laws is the number that tells a solver's error from a representation's.** On
  ℘ = 0.0005 and 0.00005 it shows that dolo's rule, read linearly on a uniform grid, has not converged where the
  zero-income event sends the household; the residual under the stated laws, which the schema requires, cannot show it,
  and the agreement of the two rules at the request points on the absolute scale cannot either.
- **A method-only step is detectable from the files,** by the effective member's identity across it, and it gives the
  agreement report a tolerance the levels cannot: HARK's rule moves by at most 4.1 · 10⁻⁷ across it and dolo's by
  8.1 · 10⁻⁶ to 1.8 · 10⁻⁵, the size of the difference between them at level 3, which falls to 2.9 · 10⁻⁶ to
  6.1 · 10⁻⁶ at the step; and the residual under the stated laws does not move across it where the solver had
  converged, the signature of a step that changes the method alone.
- **The rule is to be compared on the relative scale,** as the stone guide already says and the experiment's first
  version does not.
- **What it is not:** a test of either toolkit's own representation of the laws, since the two share one through the
  adapters' common module until the adapters' independence has run; a verdict on dolo, whose stone records the linear
  reading of its rule as its second departure, with the reason; or an evaluation of the second version of the
  experiment, which is not yet written.

## Pending

- The owner's answers to the two questions, as [`comparing-solutions.md`](../../../comparing-solutions.md) now puts
  them: what fidelity requires, and whether the residual under a toolkit's own laws becomes required; whether agreement
  is reported and classed with the method-only step as its tolerance's source, which brings forward the deferral of
  2026-11-02, and whether the rule is compared on the relative scale.
- The HARK and HAFiscal sessions' views on anything that changes what a results file carries, before a validator changes.
- The same two questions after the adapters' independence, when the two representations differ.
