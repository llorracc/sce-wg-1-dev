# Describing HAFiscal's household models with the schemas, and a test suite

Draft, fourth version, 2026-10-18, written in the sce-wg-1-dev session. Status at 08:10 EDT on 2026-10-19, with the
results schema and the checker now governed by the effective-member restructuring of the previous evening
([`effective-member.md`](effective-member.md)): of the milestones
at the end, the first is done (the checker and the `bst/1` validators and members), the second is under way (the emitter's
first results files validate; its ladder levels are running), and the Markov family has its stage file, with its
three-valued switch for permanent income while unemployed, and its model and conditions documents
(`bst-markov_ui-and-agg/model.md` and `conditions.md`, written the same evening once every open point was ruled on); its
results, validator and members are still to write. It rests on the paper's public model and parameterization
sections (`HAFiscal-Public/Subfiles/Model.tex`, `Parameterization.tex`, `Tables/calibration.tex`), the public code
(`HAFiscal-Public/Code/HA-Models/FromPandemicCode/`), the benchmark `bst_bench` in HAFiscal-Latest, the schemas in
`llorracc/sce-wg-1-dev/schemas/`, and the answers of the HAFiscal-Latest, HARK and bellman sessions. Nothing here quotes a
private document; the unpublished state of HAFiscal's model is left out; and Bellman's pages are cited by title, since its
repository is not public yet. The method addresses named below (`household.choice` and the rest) predate the ruling of the
same evening that a method file names the stage file's own targets; `bst-1/model.md`'s "Method targets" table gives the
current names, and the suite's method files will use those. The benchmark's atoms and its dry-run
results are left out of this copy until the benchmark has its public home.

## What HAFiscal solves

### The household problem of the paper

The paper states the problem in sequence form; the recursive, normalized form below is what its code solves, one problem for
each of 21 types: three education groups times seven discount-factor atoms.

**Population.**
- Three education groups: dropout, high school and college, with population shares 9.3, 52.7 and 38.0 percent (SCF 2004).
- Within each group, seven discount-factor types with equal shares, the equiprobable points of a uniform distribution on
  [β − ∇, β + ∇], the group's own center and half-width: β + ∇ (2i − 6)/7 for i = 0, …, 6. The published estimates are 0.9647 ± 0.025 (dropout),
  0.98051 ± 0.01676 (high school) and 0.99160 ± 0.00480 (college), in the public code's `EstimParameters.py`.
- Perpetual youth: a quarterly survival probability 1 − D = 1 − 1/160, the same for every household; no annuities; no
  bequest motive. A dead household is replaced by a newborn of the same group and type.
- A newborn starts with no assets and draws its permanent income level from a lognormal whose mean and log standard
  deviation depend on its group: quarterly means of $6,200, $11,100 and $14,500, with log standard deviations 0.32, 0.42
  and 0.53. In ratios to permanent income this draw is invisible; it matters for every statistic in levels, such as the
  wealth Lorenz curve the estimation targets, and for the means-tested check.

**The order of events in a quarter**, for a household of one group:
1. The employment state j is drawn from the group's chain.
2. The permanent shock: 𝐩 = Γ ψ 𝐩_{−1}, with Γ the group's growth factor, 1.0036, 1.0045 and 1.0049 by group, and ψ mean-one lognormal with
   σ_ψ = 0.0548.
3. Income: 𝐲 = θ 𝐩 if employed, with θ mean-one lognormal and σ_θ = 0.346 (the paper writes this shock as ξ), drawn only
   in that state; ξ_U 𝐩 = 0.7 𝐩 with benefits; ξ_X 𝐩 = 0.5 𝐩 without (the paper's ρ_b and ρ_nb, renamed since ρ is risk
   aversion in BST's notation). Employed income is not rescaled, so the unconditional mean of income relative to 𝐩 is
   below one.
4. Market resources 𝐦 = R 𝐚_{−1} + 𝐲, with R = 1.01.
5. The splurge: 𝐜_sp = ℷ 𝐲 is consumed mechanically, with ℷ about a quarter (0.246 in the paper's text).
6. The household chooses 𝐜_opt, whose utility is CRRA with γ = 2.
7. End-of-period assets 𝐚 = 𝐦 − 𝐜_sp − 𝐜_opt ≥ 0: no borrowing.
8. Death with probability D; replacement by a newborn.

**The employment chain** has 2 + T_UI states: employed (E); unemployed with k quarters of benefits left (U_k); unemployed
without benefits (X). In normal times T_UI = 2, so four states.
- From E: to U_{T_UI} with the group's job-loss probability `sep` (6.2, 3.1 and 1.8 percent by group), else stay.
- From U_k: to E with probability `find` = 2/3, else to U_{k−1} (to X from U_1).
- From X: to E with probability `find`, else stay.

The chain is the same for every type within a group; only `sep` differs across groups.

**The splurge has two readings, which are one model.** In the budget reading above, the splurge is deducted inside the
household's budget before the choice. In the other reading the splurge stands outside the optimizer's problem: the optimizer
receives the share 1 − ℷ of income and solves the standard buffer-stock problem, which by CRRA homotheticity is the same
problem rescaled by 1 − ℷ. The public code's total consumption, (1 − ℷ) cLvl + ℷ pLvl TranShk, is the second reading.
For the schema it is the natural one: the household problem stays in the standard form, and ℷ enters an
**observation map** from the standard rule c̃(m̃) to what the household does. With m the household's resources ratio and ξ its
income ratio:

    m̃ = (m − ξ)/(1 − ℷ) + ξ,      c = (1 − ℷ) c̃(m̃) + ℷ ξ,      a = (1 − ℷ)(m̃ − c̃(m̃)).

The MPC out of a transitory income gain is then ℷ + (1 − ℷ) c̃′(m̃), and the paper's lottery MPCs include the splurge's
share. Every MPC in the results must say which definition it uses. The parameter file's `borrowing_constraint` is in the
household's units, a bound on a; the optimizer's limit is then `a_min`/(1 − ℷ), the map's consequence. The public code
applies its zero limit inside the optimizer, where zero reads the same either way, so this only makes explicit what the
code left implicit.

**Numerics in the published code** (settings, not model): an end-of-period asset grid of 48 points from 0.001 to 40 above the
borrowing limit, with nesting factor 3 and two forced points; 7 equiprobable nodes for each shock, from untruncated lognormals;
50,000 simulated agents; 80 quarters in experiments; the endogenous grid method in a Markov-consumer solver. The code has
two agent classes of the same name: the estimation's, in `EstimAggFiscalModel.py`, extends HARK's `MarkovConsumerType`, and
the experiments', in `AggFiscalModel.py`, extends `AggIndMrkvConsumerType`. The stationary household problem is the
estimation's.

### The recession and the policies: the experiments layer

These change the household's environment, and the household re-solves with them in its chain once they arrive:
- **Recession:** unannounced. At onset the unemployment rate doubles in every group; while it lasts, `find` = 0.25 and
  `sep` = 5.1, 2.4 and 1.4 percent by group; it ends with probability 1/6 each quarter, a hazard the household knows, so
  during a recession the regime is a state of its problem.
- **Stimulus check:** a lump-sum transfer at onset, $1,200 to each household with permanent income below $100,000, phased out
  linearly to zero at $150,000; means-tested in levels, so the newborn income law and the group's growth matter.
- **Extended unemployment benefits:** benefit states added to the chain for spells begun in the policy window, T_UI from 2
  to 4.
- **Payroll tax cut:** employed income scaled up by 2 percent for 8 quarters, with a 50–50 belief in a two-year extension if
  the recession has not ended.
- **Aggregate demand feedback:** income multiplied by AD(C) = (C/C̃)^Ω with Ω = 0.3 while the recession lasts, where C
  is aggregate consumption relative to its steady path. This is the closure: the one piece outside any single
  household's problem. Under it the household's rule takes the aggregate as an argument, c(m, j, C), with a belief about
  next quarter's C as a linear rule per state, and an outer loop finds the equilibrium path of C.

Each is a dated, non-stationary problem solved backward from the stationary solution, then simulated from a population drawn
from the stationary distribution. With the regime inside the family, the recession experiment is the onset itself: the
population is moved into the recession regime at a date, where the member's own rule already applies. The schemas have no
experiment layer yet; a sketch is below. One requirement is already
clear: a schema that cannot say "the household's policy is conditional on an aggregate that the closure determines" would
misdescribe HAFiscal.

### The toy: `bst_bench`

HAFiscal-Latest's `Code/HA-Models/bst_bench/` holds a toy of the paper's machinery, specified as a benchmark for other
toolkits: one education group's problem with the splurge and the employment chain removed. Its household is a `bst/1`
member:

| | the toy | the paper |
|---|---|---|
| types | seven β, equal shares: 0.906 + 0.098 (2i − 6)/7, i.e. 0.822 … 0.990 | 3 groups × 7 β |
| survival | 1 − 1/160 | the same |
| R, ρ | 1.01, 2 | the same |
| growth | one 𝒢 = 1.0019026 | Γ by group |
| unemployment | i.i.d. each quarter with probability 0.044, income 0.7 𝐩 | the chain with benefit duration and exhaustion |
| employed income | θ (1 − ℘ξ_U)/(1 − ℘), so E[ξ] = 1 | θ, no rescaling |
| shocks | the 7-point atoms of lognormals with log variances 0.003 and 0.12, declared as the model | 7-point discretizations, as numerics |
| splurge | none | ℷ |
| newborn | 𝐩 = 1, a = 0, born employed: its first draw is the employed branch of ξ; the benchmark's own specification follows since 2026-10-18 | the same, with 𝐩 drawn from the group's level law (decided 2026-10-18) |
| borrowing | a ≥ 0 | the same |
| regime, feedback | none | the recession and AD, in the experiments |

What the benchmark already has, which the suite below generalizes rather than replaces:
- a complete specification, a reference (HARK's EGM with cubic interpolation, a numpy ergodic tool) on a ladder of four grid
  refinements, bands set at ten times the ladder's top-level disagreement, and a scorer;
- outputs close to the results schema: the rule and a finite-difference MPC at nine test points, the target and the kink, the
  ergodic distribution as capped means E[min(a, x)], the mean MPC, Lorenz shares of a, and the submission's own Euler errors;
- an independent EGM code and an SSJ household block for the dynamics rungs;
- a dry-run protocol: a toolkit's own method is used blind, from the specification alone, and the specification is revised
  until the toolkit reaches the finest band.

Its reference ladder is the prototype of the settings suite. The schemas change three things: the shocks become continuous
laws and the atoms a setting; the method and settings are stated in files of their own; and the comparison points come from
a request file.

## Describing the models with the schemas

### The toy as a `bst/1` member

Two forms, which the suite should both carry. The first is the benchmark as it stands, with its atoms as `Discrete` laws, so
that every existing reference number is reproducible exactly:

```yaml
family: bst/1
period: quarter
crra: 2.0
types:
  - {beta: 0.822, share: 0.142857142857142857}
  - {beta: 0.850, share: 0.142857142857142857}
  - {beta: 0.878, share: 0.142857142857142857}
  - {beta: 0.906, share: 0.142857142857142857}
  - {beta: 0.934, share: 0.142857142857142857}
  - {beta: 0.962, share: 0.142857142857142857}
  - {beta: 0.990, share: 0.142857142857142857}
survival: 0.99375
return: 1.01
borrowing_constraint: 0.0
income:
  growth: 1.0019026
  permanent_shock: {Discrete: {values: [the seven atoms of the benchmark's atoms file], probs: [1/7 each]}}
  unemployment: {prob: 0.044, income: 0.7}
  employed_shock: {Discrete: {values: [the seven employed atoms before rescaling], probs: [1/7 each]}}
```

The atoms are copied from `atoms_base.json` at full precision, with the employed atoms divided by the rescaling factor
(1 − ℘ξ_U)/(1 − ℘), since `bst/1` applies that factor itself. The checker then verifies that each law's mean is one.

The second form is the true model, with continuous laws. Chris decided on 2026-10-18 that the toy's true model is the
truncated one, at ±3 standard deviations with the stated standard deviation kept, the convention HAFiscal's own shocks
follow; an untruncated member stays in the suite beside it, since the published atoms converge to the untruncated law as the
node count grows:

```yaml
  permanent_shock: {TruncatedLogNormal: {sd_log: 0.0547722558, bot: -3.0, top: 3.0}}
  employed_shock:  {TruncatedLogNormal: {sd_log: 0.3464101615, bot: -3.0, top: 3.0}}
```

### The paper's model as a family: `bst-markov_ui-and-agg/1`

The paper's household problem is not a `bst/1` member and should not be forced into one. It is a `bst/1` problem with five
additions and one convention change, and a new family states it; `bst/1` stays as it is. Chris named the family
`bst-markov_ui-and-agg` on 2026-10-18: buffer-stock theory with Markov employment and unemployment-insurance states, and an
aggregate state. The aggregate state is read here as the macro regime, normal or recession, which the household carries as a
Markov state of its problem with the regime's hazards as parameters, so that its chain is the product of the regime and the
employment state, as in HARK's aggregate-and-individual Markov consumer. The aggregate-demand feedback, under which the rule
also carries aggregate consumption as an argument, stays in the experiments layer as the closure: Chris confirmed on
2026-10-18 that "agg" names the regime alone, the feedback being a different household problem, for a later family or
version that would also state the household's belief rule about the aggregate.

**What it adds to `bst/1`:**
1. **Employment as a Markov chain** with benefit duration and exhaustion, in place of i.i.d. unemployment, with an income map
   by state: the transitory law drawn in one state only, fixed replacement incomes in the others, and a stated rule for
   permanent income while unemployed. The chain's structure (the states, which transitions exist, the countdown) is fixed by
   the family; the parameter file gives T_UI, `find` and each group's `sep`. Bellman's own fixture for HAFiscal writes
   the chain the same way, as four named states in one stage, since a state set of unstated size has no spelling there.
2. **Groups of types.** A group has its own growth factor, job-loss probability, newborn income law and list of types; a
   type's weight is its group's share times its share within the group. Every other primitive is common.
3. **The newborn's permanent income in levels**, a lognormal with a free mean. This is not a mean-one shock law; it is a
   level law, and the family defines it.
4. **The splurge**, as the observation map above, with ℷ = 0 switching it off.
5. **The aggregate regime** as a Markov state: normal, which is absorbing in the stationary problem since a recession arrives
   unannounced, and recession, which ends with a stated hazard. The job-finding probability and each group's job-loss
   probability are given per regime. The stationary population is computed in the normal regime; the recession regime's rule
   is part of every member's solution, so the recession experiment is the onset alone.

**The convention change:** employed income is e θ 𝐩 with e a parameter, 1 in the paper. `bst/1` fixes e = (1 − ℘ξ_U)/(1
− ℘) so that E[ξ] = 1. Making e explicit is what lets a `bst/1` member be written as a `bst-markov_ui-and-agg/1` member
exactly (below).

**Conventions the paper leaves open, and how the family fixes them** (the HAFiscal session checked the code):
- The newborn follows `bst/1`'s convention (the owner's ruling of 2026-10-18): born employed, with no assets, its permanent
  income drawn from the group's level law, no ψ in its first quarter, and its first transitory draw the employed branch,
  e θ. The paper's text is silent on a newborn's employment state and first-quarter shocks; its revised text gives a
  newborn zero assets and market resources equal to its first income draw, which this convention satisfies. The code does
  otherwise: a newborn takes one transition of the current regime's chain from the state of the household whose place it
  takes (the chain's stationary distribution, in a stationary population under one regime, since death is independent of
  the state), draws ψ in its first quarter, and gets a transitory shock of one. A toolkit that cannot birth a household
  employed without a first-quarter ψ records the deviation in its provenance. An earlier version of this note said the
  code draws the state from the stationary distribution; it does not.
- The onset of a recession is unanticipated: the normal regime is absorbing in the household's problem, so the parameter
  file carries no hazard of entering a recession; the onset is the experiments layer's event, and the recession's exit
  hazard is the parameter the household knows (the owner's ruling of 2026-10-18, after confirming that this is how the
  published code treats it).
- Permanent income in a quarter of unemployment: the paper's text keeps growth going and does not say whether ψ is drawn.
  The code has growth and ψ as two separate settings: growth applies in every state, ψ is drawn in every state in its
  default world, and ψ = 1 while unemployed in the paper's corrected text. The family carries a required parameter,
  `unemployed_permanent_income`, with three values: `continues` (Γψ applies every quarter), `grows` (Γ applies and ψ = 1
  while unemployed) and `frozen` (𝐩 is unchanged while unemployed). `continues` is the family's standard world and the one
  the paper's text describes: its income equation applies to every household, and its footnote keeps each group's growth
  rate unchanged during unemployment. `frozen` reproduces the published numbers, since the published code neither grew
  permanent income nor drew ψ while a household was unemployed; `grows` is the corrected code's world. The published code's
  choice had a computational motive: with ψ fixed at one in the unemployed states, each of those states carries a single
  income atom instead of a full set, which keeps a Markov solve and a transition matrix small, and the few unemployed
  households of a simulated panel add no shock noise. Against that, only under `continues` is permanent income independent
  of the employment state, which a one-dimensional transition-matrix method (the Harmenberg factorization) needs to be
  exact; that, and the paper's text, make `continues` the standard, confirmed by the owner on 2026-10-18. No file omits the
  key, since a default would be a second written form of one model.
- Survival is a constant 1 − D at every age, in the solution and in the simulation: perpetual youth with no maximum age. A
  toolkit's maximum-age setting (HARK's `T_age`) must be off.

**A parameter file**, with the paper's normal-times calibration and the laws as the published code discretized them:

```yaml
family: bst-markov_ui-and-agg/1
period: quarter
crra: 2.0
splurge: 0.246
survival: 0.99375
return: 1.01
borrowing_constraint: 0.0
shocks:
  permanent_shock: {LogNormal: {sd_log: 0.0548}}
  employed_shock:  {LogNormal: {sd_log: 0.346}}
regimes:
  recession: {exit_hazard: 0.1666666666666667}
employment:
  benefit_quarters: 2
  job_finding: {normal: 0.6666666666666667, recession: 0.25}
  income_employed: 1.0
  income_with_benefits: 0.7
  income_without_benefits: 0.5
  unemployed_permanent_income: continues
groups:
  - name: dropout
    share: 0.093
    growth: 1.0036
    job_loss: {normal: 0.062, recession: 0.051}
    newborn_income: {mean: 6200.0, sd_log: 0.32}
    types:
      - {beta: 0.943271, share: 0.142857142857142857}
      - {beta: 0.950414, share: 0.142857142857142857}
      - {beta: 0.957557, share: 0.142857142857142857}
      - {beta: 0.964700, share: 0.142857142857142857}
      - {beta: 0.971843, share: 0.142857142857142857}
      - {beta: 0.978986, share: 0.142857142857142857}
      - {beta: 0.986129, share: 0.142857142857142857}
  - name: highschool
    share: 0.527
    growth: 1.0045
    job_loss: {normal: 0.031, recession: 0.024}
    newborn_income: {mean: 11100.0, sd_log: 0.42}
    types: [the seven points of 0.98051 ± 0.01676]
  - name: college
    share: 0.380
    growth: 1.0049
    job_loss: {normal: 0.018, recession: 0.014}
    newborn_income: {mean: 14500.0, sd_log: 0.53}
    types: [the seven points of 0.99160 ± 0.00480]
```

Shares within a group sum to one, and group shares sum to one. The file lists the β values as numbers: how they were chosen is
estimation, the group's layer, not the family's. The member above, solved with 7 nodes per shock, is the paper's calibration in the family's standard world, and with the
switch at `frozen` it is the member that reproduces the published numbers; the
same file with `TruncatedLogNormal` laws at ±3 is the truncated variant the shock-law spec recommends.

**A `bst/1` member as a `bst-markov_ui-and-agg/1` member.** One group with the `bst/1` types; `growth` = 𝒢; `job_loss` = ℘ and
`job_finding` = 1 − ℘, so that the chain is i.i.d. with unemployment probability ℘ every quarter; `income_with_benefits` =
`income_without_benefits` = the `bst/1` member's ξ_U; `income_employed` = (1 − ℘ξ_U)/(1 − ℘); `splurge` = 0;
`unemployed_permanent_income` = `continues`, since `bst/1` draws ψ every quarter; any `benefit_quarters`; and one
regime, the normal one, with the recession's parameters equal to the normal ones. The two families must then produce the
same rule and, since this family's newborn follows `bst/1`'s convention, the same stationary distribution, exactly. That
is a cross-family consistency test the suite should run, and it is the test that the Markov machinery reduces correctly.

**Conditions.** The conditions of `bst-1/conditions.md` carry over with 𝒢 = Γ, the group's growth factor, since the chain
touches only transitory income and the permanent shock is unchanged. Two differences:
- The worst income is the lesser of the exhaustion income and the lowest employed income, times the lowest ψ: zero with an
  untruncated law, so `a_Nat` = 0 for every member with lognormal laws; with truncated laws it is positive and depends on the
  switch for permanent income while unemployed; the constraint in force is then computed state by state, as the
  family's conditions document states. A continuous law puts no mass at its infimum, so `p_worst` = 0 and the WRIC reduces
  to the RIC. (Corrected on 2026-10-18 from "ρ_nb P > 0", which holds only when the employed income cannot fall below it.)
- The paper's estimation imposes the GIC on every type, with an upper bound β^GIC per group; the checker computes that bound
  from the parameter file, so the suite can verify that every estimated β is below it.

The stationary population over (m, j) exists for every valid member when ℒ < 1, by the same mixture-over-ages argument.

**Results for `bst-markov_ui-and-agg/1`.** Everything in `bst-1/results.md`, indexed by group, type and employment state, plus what the
paper's own targets need:
- the rule c(m, j) and its MPC at comparison points chosen per state, since the kink and the support differ by state;
- the targets for the employed state, with their domain rules;
- the stationary distribution of (m, j) per group and type, pooled within a group, and pooled over groups by share;
- the unemployment rate and the share in each state per group, which the chain determines exactly, as a check;
- **statistics in levels:** the generalized Lorenz ordinates of liquid wealth 𝐚 = a 𝐩 pooled over groups, the median
  wealth-to-permanent-income ratio per group, and the Lorenz shares at 20, 40, 60 and 80 percent per group and for the whole
  population, which are the estimation's targets; these need the distribution of 𝐩, hence the newborn income law and the
  income measure's machinery;
- the mean MPC by wealth quartile, the paper's non-targeted moment, in both definitions: the optimizer's c̃′ and the
  household's ℷ + (1 − ℷ) c̃′;
- the aggregate ratio of consumption to income by group.

**The experiments layer, sketched.** An experiment file names a base member and a dated sequence of changes to its
environment: the regime chain (the recession with its exit hazard) applied from an unannounced onset; dated parameter paths
(the benefit states opened for a window, the income scale of the tax cut, the belief about its extension); transfers in levels
(the check with its means test); and a closure block (the aggregate-demand rule with Ω, and the household's belief about
the aggregate), under which the household's rule carries the aggregate as an argument. Its results are paths: aggregate
consumption and income by quarter, each policy's consumption multipliers over horizons, and the welfare measures. This
is the group's layer in the handoff's terms, and the schemas should reserve its place without designing it now.

### What the shared schemas need, in order of difficulty

1. A **level law** for the newborn's permanent income: `{mean, sd_log}` lognormal in levels. Small.
2. **Groups** in the parameter schema: a list of groups each with group-level parameters and its own `types`. Small.
3. **Two MPC definitions** in the results schema where an observation map exists. Small.
4. **Per-state comparison points** in the request file, and per-state results. Moderate.
5. **Statistics in levels** in the results schema, which means the results schema must know the law of 𝐩: the income
   measure's total weight and the GL ordinates of 𝐚 = a 𝐩. Moderate; the theory is in `bst-1/conditions.md`.
6. A **Markov employment construct** that other families can reuse: a family-defined state set and transition structure with
   named probabilities and an income map by state. Moderate; the alternative, a general Markov shock law with a free
   transition matrix, would break the one-written-form rule and is not needed by HAFiscal.
7. An **observation map** section in a model schema, for the splurge. Small as prose; its consequences for the MPC and the
   wealth ratios are stated above.
8. The **experiments layer**, with a policy conditional on an aggregate the closure determines. Large; deferred.

## The test suite

### Purpose

To construct many solutions of these models, across members, methods and settings, so that (a) each toolkit's convergence is
measured and its tolerances set from measurement; (b) toolkits are compared on identical true models; (c) the published
HAFiscal numbers are placed on that map: how far the 7-node, 48-point solution of the paper is from the converged solution of
its own model, and how its estimates move when the shock law changes.

The suite is the product of three axes, each a set of files with a hash:

    members (parameter files)  ×  methods (method files)  ×  settings (settings elements, from suite files)

and every run is one (member, method, settings element, request file) → one results file.

### Members

| name | family | what it is | why it is in the suite |
|---|---|---|---|
| `toy-atoms` | bst/1 | the benchmark as specified: Discrete laws from `atoms_base.json` | reproduces every existing reference number; tests Discrete laws |
| `toy` | bst/1 | the same with `TruncatedLogNormal` laws at ±3 | the true toy |
| `toy-untruncated` | bst/1 | the same with `LogNormal` laws | the law the published atoms converge to as the node count grows |
| `toy-no-mortality` | bst/1 | `toy` with ℒ = 1 | the ℒ = 1 conditions (Szeidl, Harmenberg) |
| `toy-zero-income` | bst/1 | `toy` with ξ_U = 0 | no kink; `undefined` statuses |
| `toy-one-type` | bst/1 | `toy` with the median β only | the smallest member; quick checks |
| `library` | bst/1 | the community library's model | a published model from outside; untruncated laws |
| `toy-crra-3`, `toy-R-1005`, `toy-R-1015` | bst/1 | the paper's robustness variants applied to the toy | mirrors HAFiscal's own sensitivity set, less its ρ = 1 variant, which `bst/1` excludes |
| `toy-as-hafiscal` | hafiscal/1 | `toy` rewritten as a `bst-markov_ui-and-agg/1` member | cross-family consistency |
| `paper-published` | hafiscal/1 | the paper's normal-times calibration with `LogNormal` laws and the switch at `frozen`; 21 problems | with 7 nodes as a setting, the published numbers |
| `paper-text` | hafiscal/1 | the same with the switch at `continues`, the family's standard world | the model the paper's text describes |
| `paper-truncated` | hafiscal/1 | the same with `TruncatedLogNormal` laws at ±3 | the truncated variant; where the N-node solutions must converge |
| `paper-no-splurge` | hafiscal/1 | ℷ = 0 with the paper's re-estimated β | the paper's splurge-free robustness |
| `paper-low-benefits` | hafiscal/1 | ξ_U = 0.3, ξ_X = 0.15 | the paper's benefits robustness |
| `paper-one-group` | hafiscal/1 | the high-school group alone | HAFiscal's own development member |
| `paper-recession-permanent` | hafiscal/1 | the recession's chain as a stationary member | a stress test of the chain; not the paper's experiment |

### Methods

One method file per toolkit route.

| route | toolkit | household.choice | expectations | household.rule | population.distribution |
|---|---|---|---|---|---|
| `hark-egm-linear` | HARK | `hark:egm` | equiprobable nodes, the two shocks fused into one product distribution | linear, with the constraint's lower envelope and HARK's decay extrapolation above the grid | transition matrices (`make_transition_matrices`, `find_steady_state`) |
| `hark-egm-cubic` | HARK | `hark:egm` | equiprobable nodes | cubic Hermite with the EGM slopes | transition matrices |
| `hark-egm-hermite` | HARK | `hark:egm` | Gauss–Hermite nodes | cubic Hermite | transition matrices |
| `hark-egm-mc` | HARK | `hark:egm` | equiprobable nodes | linear | Monte Carlo |
| `hafiscal-egm` | HAFiscal's code | EGM with the per-state lower envelope | the atoms | cubic | transition matrices on an asset grid, or Monte Carlo with a stratified shuffle of the chain's transitions |
| `hafiscal-continuous` | HAFiscal's code | the same | exact integration against the truncated densities, the integral split at the kink | cubic | the same |
| `bench-egm` | `bst_bench` `dynamics.py` | EGM, cubic Hermite carrying the MPC | the member's atoms | cubic Hermite | the lottery on an a-grid (`ergodic.py`) |
| `dolo-ti` | dolo | time iteration | the member's atoms or its own nodes | cubic spline | its own ergodic tool |
| `workbench` | Bellman | not a route today: Bellman declares and binds a model and solves nothing (below) | | | |
| `ssj-steady` | the SSJ household template | seeded by another route's rule | the member's atoms | linear | its own |

HARK has no value-function iteration for this model, nothing for `diagnostics.expectation`, and simulates from the household's
discretized shocks, so `population.transition.*` uses the household's method unless the harness installs a finer discretization
after solving. The diagnostics' expectation therefore belongs to the harness, shared by every toolkit, which also guarantees
that it differs from each toolkit's own.

**The HARK registry, by part** (from the HARK session, checked against HARK main):
- `hark:egm` reads `aXtraMin`, `aXtraMax`, `aXtraCount`, `aXtraNestFac`, `aXtraExtra` (a grid of assets above the
  borrowing limit) and `tolerance`, the largest change in the rule between iterations; the cycle limit is fixed at 5,000.
- The expectation rules on a lognormal are `equiprobable` (`PermShkCount`, `TranShkCount`, with `tail_N` and `tail_bound`)
  and `hermite`; the unemployment atom is exact.
- The rule is `LinearInterp` or cubic Hermite (`CubicBool`); `vFuncBool` adds the value function for the optional Bellman
  residual.
- The distribution is Monte Carlo (`AgentCount`, `T_sim`, `seed`, `T_age` = `None`) or the transition-matrix route, whose
  `grid_specs` give the histogram's range and size and whose `norm` selects the population or the income-weighted measure.
- Shared-vocabulary candidates: `grid_points`, `grid_min`, `grid_max`, `nodes_per_shock` (or one count per shock),
  `simulated_agents`, `simulated_periods`, `seed`, `histogram_points`, `histogram_max`, `solution_tolerance` (defined as
  the largest change in c between iterations), and multi-exponential grid placement with `grid_nesting`, which other
  toolkits can implement exactly. Under `hark:`: `aXtraExtra`, `tail_N`, `tail_bound`, the decay extrapolation, `norm`,
  `newborn_growth`.

**Realizing a `bst/1` member in HARK:** one `IndShockConsumerType` per type (`cycles` 0, `T_cycle` 1) with `CRRA`,
`DiscFac`, `LivPrb`, `Rfree`, `PermGroFac`, `BoroCnstArt` = `a_Art`, `T_retire` 0, `UnempPrb` = ℘, `IncUnemp` = ξ_U, and
the shock standard deviations; the solver discounts by `DiscFac·LivPrb` and survivors earn `Rfree`, which is `bst/1`'s
perpetual youth. The unemployment atom is built exactly as `bst/1`'s ξ. Types with unequal shares are pooled by the
harness, not by `AgentPopulation`. Newborns need overrides: `kLogInitMean` = −1000 for a = 0, `pLogInitMean` = 0 and
`pLogInitStd` = 0 for 𝐩 = 1, and a first transitory draw from the employed branch of ξ, which `NewbornTransShk` does not
give, since it draws the full shock with the unemployment event, so the adapter draws it itself. One thing more HARK
cannot do as it stands: a newborn draws ψ and growth in its first period, so its 𝐩 is 𝒢ψ rather than 1; the fix is the
`NewbornPermShk` flag, implemented in the HARK session's branch and awaiting its pull request. `Discrete` and `Uniform`
laws need a custom income-distribution constructor; the truncated, mixture and tabulated laws need the distribution pull
requests already proposed.

**Bellman's place** (from the bellman session, which read its repository without running Matsya). Bellman is a declaration
and binding layer, not a solver: its documentation says the Workbench solves nothing and the package stores no value
function; its one endogenous-grid routine is one-dimensional with linear interpolation and no stationary distribution, and its
Gauss–Hermite and value-iteration routines live inside one application's finite-horizon solver. So Bellman cannot be a route
in the suite today. It could be the layer that declares a member and binds its calibration, methods and settings, with a
solver supplied by HARK or written for it, which is what its internal adapter specification plans.

What Bellman already states for HAFiscal: a test fixture, not an application: one stage file with the four employment states
as a named set, the row of the transition matrix selected by the previous state, state-selected shock standard deviations (zero
while unemployed, a point mass at one), income by state, the splurge as intermediate lines of the budget, and mortality as
discounting. A blind reconstruction of that file found it agreed with the model on every item but one, the boundary condition:
the language has no horizon, no terminal rule and no statement of stationarity. The 21 types lie outside the stage, there is no
construct for a population of types with shares, and none for a newborn's initial distribution. Those are the same items
that `bst-markov_ui-and-agg/1` adds above `bst/1`, which is some evidence that the family's additions are the right cut.

How the three files map to Bellman's, and what is lost:
- The parameter file maps to a calibration file, a flat mapping of names to values ("The Bellman factory"). The law family
  lives in the stage file, so a change of law is a different stage file; structured values (types with shares, laws as
  mappings) have no place; and the mean-one condition is never enforced. Of the shock laws, `Degenerate` is a lognormal with
  zero standard deviation, `Discrete` a mixture of point masses, `LogNormalMixture` a mixture of lognormals with the shift
  folded in, and `Uniform` Bellman's own; `TruncatedLogNormal` and `TruncatedLogNormalMixture` wait for Bellman-SYM's
  truncated lognormal, and `Tabulated` has no counterpart (`shock-laws.md`, "Bellman-SYM counterparts").
- The method file maps to a per-stage methods file whose `on:` addresses are syntactic and local to one stage: a block, a
  line, an operator name covering every occurrence, or one occurrence ("Methodization"). The two expectation parts of
  `bst/1` fall on one joint expectation in Bellman's buffer-stock stage; `household.rule` has no separate target, since the
  endogenous-grid method takes the policy's evaluation; `population.*` and `diagnostics.*` have no target; and Bellman's
  method entries may hold literal settings, which the schema's may not.
- The settings file maps to a flat settings file, which may hold settings no method reads.
- The suite file has no counterpart: the pieces are the recipe's fill slots and variants, and a parameter grid, labeled
  specifications and a sweep in Bellman's testing package.
- The results file has no counterpart: Bellman's saved solutions are grid arrays by stage, perch and field with metadata
  ("Solutions at the perches"), with no hashes, request points, special points, Lorenz ordinates, residuals or statuses.
- Hashing: Bellman digests one stage occurrence's bindings as type-tagged canonical JSON with floats in binary form, so
  `0.10` and `0.1` agree while `1`, `1.0` and `true` differ, and it hashes recipe and source files by their bytes; there is no
  single model hash. The schema's canonical form should adopt the binary-float rule and add the model-level hash.
- A converter from the three files to a Bellman recipe is mechanical only for members whose laws are among Bellman's seven
  families, with a stage-file template per combination of laws and a table from the schema's addresses to `on:` targets.

The bellman session's edits that would turn Bellman's buffer-stock stage into `bst/1` (survival in the discounting, the
unemployment atom as a mixture component, the borrowing limit as a complementarity clause on the Euler line, one instance per
type by fill) are about an hour's work by hand. A Matsya job on `bst-1/model.md` would return roughly those edits; its value
would be the prose judges' ten-item comparison, which shows where the model schema leaves something unsaid. Three of the shock
laws would stop such a job with a question, since the distribution check admits only the seven families. The cheaper first step
is the hand-written stage file and one question with `--stage-file`, which elaborates it for the price of a turn.

### Settings suites

| setting | what varies | levels | what it tests |
|---|---|---|---|
| solution grid | points, upper bound, nesting | 48 (the paper), 300, 600, 1200, 2400 (the benchmark's ladder) | grid convergence; whether 48 was enough |
| nodes per shock | the quadrature of each continuous law | 3, 5, 7, 11, 21, 51 | convergence of the discretized solution to the true model; how far the published 7-node numbers sit from it |
| distribution grid | the lottery's nodes | 2,000 … 32,000 | the ergodic distribution's convergence (second order in spacing) |
| Monte Carlo | agents, periods, seed | 50,000 × 80 (the paper); 500,000 × 400; three seeds | simulation error against the transition-matrix answer |
| tolerances | the solver's stopping rule | 1e-6 … 1e-12 | that the stopping rule is not what limits accuracy |
| precision levels | named elements `low`, `medium`, `high` | one each | the optional ladder of the results schema |

Truncation is not a setting: a truncated and an untruncated law are different members.

### What is compared, and how tolerances are set

1. **Within a toolkit, across settings:** the ladder. For each quantity, the gap between successive levels and the gap to the
   top level, as the benchmark's `LADDER.md` already tabulates. A quantity whose gap does not shrink is ill-conditioned
   (the benchmark found quantiles near a mass point and the constrained mass to be such) and is reported but not banded.
2. **Across toolkits, on one member:** agreement within the tolerance set from the ladders, widened by simulation standard
   errors. The benchmark's bands are ten times the top-level disagreement, rounded up to a decade.
3. **Across families, on one model:** `toy` against `toy-as-hafiscal`, which must agree to the solver's own precision.
4. **Against the true model:** the N-node solutions of `toy` must converge, in N, to the `hafiscal-continuous` solution; the
   N-node solutions of `toy-untruncated` must converge to its continuous solution, with `toy-atoms` as their N = 7 member; and
   the gap between `toy` and `toy-untruncated` at the same N measures what the truncation changes.
5. **Across engines, on one route:** transition matrices against Monte Carlo on the same rule.
6. **Diagnostics in every results file:** Euler residuals with the harness's own quadrature and the stationarity residual,
   which catch a wrong solution without a reference.

### Runs of particular value to HAFiscal itself

- The estimation of the splurge against the truncation (none, ±2, ±3) and the node counts, continuous against discretized,
  made routine.
- The continuous expectation against the atoms through the whole pipeline.
- The 21 published problems at the paper's settings and on the ladder: how far the published rule, wealth distribution and
  MPCs sit from the converged solution of the same model.
- Transition matrices against Monte Carlo at the paper's 50,000 × 80, type by type; the public code's comments say the patient
  types' mixing time is comparable to the simulation length.
- The cross-family check, which exercises the chain's reduction to the i.i.d. case.
- Seed bands (the paper's three seeds) and HARK-version parity, as named suites.

### The harness

```
suite/
  members/        parameter files (YAML), one per member above
  requests/       request files: comparison points per member, from a quick solution by the stated rule
  methods/        method files, one per route
  settings/       suite files, one per route, with the named levels
  registry/       the method registry: each method's contract and declared settings
  results/        <parameter-hash>/<method-hash>/<settings-hash>.json
  adapters/       one module per toolkit: run(member, method, settings, request) -> results file
  checker/        the parameter checker (validation, exact moments, regularity verdicts, hashes)
  compare/        ladder.py (within-toolkit gaps), agree.py (cross-toolkit), consistency.py (cross-family)
```

- An **adapter** loads and validates the three files and hashes each; turns them into a toolkit's objects; solves, recording
  whether the solve converged and how; computes the stationary distribution; evaluates the results-schema quantities; and
  writes the file with the hashes, the toolkit's version and commit, the hardware, the threads and the wall time. The
  benchmark's `make_reference.py` and `ergodic.py` are the first adapter's seed; HAFiscal's `AggFiscalType` the second's;
  HARK's agent classes the third's.
- **The quantities, in a HARK adapter:** the rule at the request points from the interpolant; the MPC as the interpolant's
  derivative (piecewise constant for a linear rule, so the schema must say which side at a knot); the kink by bisection on
  m − c(m); the targets by solving their defining equations on the rule with the checker's exact moments, with HARK's own
  `calc_stable_points` recorded as a cross-check; the stationary population from the transition-matrix route (integrating
  the quantile function of the bin masses) or the last Monte Carlo cross-section after burn-in; the income measure by
  weighting with 𝐩, which needs the newborn fix; the Euler and stationarity residuals computed by the harness with the exact
  laws on the toolkit's rule; the condition verdicts from the checker, with the toolkit's own factors recorded as a diagnostic.
- A **driver** expands a suite file into elements, runs each as one process started by `spawn` or `forkserver` (never `fork`
  after JAX) with `OMP_NUM_THREADS` and `NUMBA_NUM_THREADS` set to 1 and recorded, gives each element its own seed, and files
  the result under its three hashes, so that reruns are idempotent. Elements are independent, so a suite runs in parallel on
  one machine or several.
- **Comparison** reads results files by hash, never by file name, so that results for different models cannot be compared by
  mistake. HAFiscal's provenance sidecars, one next to every output with the resolved settings and the code and HARK commits,
  are the model for the results file's provenance block.
- **Continuous integration:** a smoke suite (`toy-one-type`, `low`, one route) on every change; the full suite on demand.

**The benchmark as an emitter.** `bst_bench` already computes per type the rule and the MPC as a derivative, the kink and the
target, the ergodic distribution with its point masses, and Euler errors. For the schema's results file it lacks the GL
ordinates at the schema's probabilities, the income measure's stationary distribution (its income-weighted transition exists
for the dynamics rungs), the pseudo-target, the stationarity residual (one push-forward through its own transition), the
request file's points from a quick solution, an Euler residual whose expectation differs from the household's, the provenance
block and hashes, and the JSON shape. The HAFiscal session estimates about two days for the emitter and a request-file
generator, after which its scorer can compare two results files instead of its own scorecard.

**Settings that silently solve a different model in HARK** (from the HARK session), which the adapter must set and the
results file must record:
1. `NewbornTransShk` defaults to `False`: newborns get ξ = 1, not a draw.
2. `kLogInitMean` defaults to −12: newborns hold about 6e-6, not 0.
3. Newborns draw ψ and growth in the birth period: 𝐩 = 𝒢ψ, not 1, which changes the income measure.
4. `PermGroFacAgg` must stay 1; and the transition-matrix route's `newborn_growth` must be 1, not 𝒢, for `bst/1`'s income
   measure (to be verified against a P-weighted simulation).
5. `T_age` must be `None`.
6. `BoroCnstArt` = `None` means no artificial limit: with ξ_U > 0 that allows borrowing to the natural limit computed
   from the discretized worst income; pass `a_Art` explicitly.
7. The simulation draws the discretized shocks, so a simulated distribution belongs to the discretized model.
8. Solving stops on the rule's change between iterations or silently at 5,000 cycles, neither an Euler criterion.
9. Comparison points above the grid's top fall in the decay extrapolation; choose `grid_max` beyond the largest request point
   or report the extrapolation.
10. Until the bounds-fix pull request merges, the bounds recorded with discretized shocks are wrong for finite-support laws;
    the checker never reads them.
11. `NewKeynesianConsumerType`'s transition-matrix code places newborns at 𝐩 = 1 and m = 1, with no ξ and no ψ, whatever the
    newborn flags say; only the simulators read the flags, and the model-file transition matrices follow `ConsIndShock.yaml`,
    where newborns draw both shocks. A histogram route therefore needs the harness to place newborns itself.

### Milestones, in order

1. The checker and the `bst/1` parameter validator; `toy-atoms`, `toy` and `library` as parameter files, with their condition
   margins.
2. The benchmark adapter: `bst_bench`'s reference pipeline writes results files in the schema's form, and its ladder becomes
   the first settings suite (about two days, in the HAFiscal-Latest session).
3. The HARK adapter for `bst/1`, with the newborn subclass; the first cross-toolkit comparison in the new form. The
   `NewbornPermShk` flag as a small HARK pull request, after the bounds fix.
4. The `bst-markov_ui-and-agg/1` model schema and parameter validator; `paper-published`, `paper-truncated` and `toy-as-hafiscal`; the
   cross-family check.
5. The HAFiscal code adapter (the estimation's `AggFiscalType`) for the stationary problem, with its per-state lower
   envelope; the level statistics; the published numbers placed on the ladder.
6. The dolo adapter; a Bellman declaration of `bst/1`, by hand, checked with one `--stage-file` question, as the binding
   layer for a solver supplied later.
7. The experiments layer.

## Questions

For the HAFiscal session: nothing open; the benchmark's toy specification follows `bst/1`'s newborn since its version of
2026-10-18, and it answered which world produced the published numbers. The bellman session's corrections to the June Bellman description of the household
problem were passed to it to check.

For the HARK session: nothing open; the `NewbornPermShk` pull request is for Chris to approve in that session.

For the bellman session: nothing open.

**Decisions taken by Chris, 2026-10-18:**
1. The family is named `bst-markov_ui-and-agg`, version 1. "agg" covers the aggregate regime alone (confirmed 2026-10-18):
   under the aggregate-demand feedback the rule takes aggregate consumption as an argument, a different household problem,
   which belongs to a later family or version, with the closure in the experiments layer.
2. The toy's true model is truncated at ±3; an untruncated member stays in the suite.
3. The draft goes into the public fork without the benchmark's atoms and the dry-run results.
4. The emitter and the newborn flag go ahead, iteratively: any improvement to the schema that the work suggests is to be
   proposed to Chris, with its downstream consequences thought through, before it is made.
5. The bellman session writes the `bst/1` stage file by hand, filed in the fork; one Matsya question checks it; a Matsya job
   follows once, later, as the completeness test.
6. Later the same day: BST's notation throughout (ξ the transitory shock, θ the employed draw, ℘, the income while unemployed, ℒ, 𝒢, `a_Art` and
   `a_Nat`); ρ ≥ 1 with the log amendment, revised the same evening to ρ > 1 as in BST, log utility outside the family for
   now; a newborn is born employed; the natural borrowing constraint and ℘ are
   implications, not conditions; the welfare condition is a regularity condition for every bst-class problem, and population
   welfare is reported.
7. In the evening: the permanent-income switch has three values, with `continues` the standard; the precision levels are
   settings, not error targets; the results file gains three optional provenance keys; the replacement incomes are ξ_U
   and ξ_X, and groups are named, not indexed; the borrowing limit is stated in the household's units; the benchmark's
   toy follows `bst/1`'s newborn.
8. Later that evening: this family's newborn follows `bst/1`'s convention; the normal regime is absorbing and the parameter
   file carries no hazard of entering a recession; "agg" is the regime alone; the Matsya completeness job on `bst/1` goes
   ahead. Nothing of the stage file's points stays open.
