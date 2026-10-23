# The Markov family's first measurements

Found on the evening of 2026-10-22, while beginning the family's results document, validators and members.

## HARK's Markov solver for the family's chains

Read by the HARK session at the adapter's pin (`11852805`), with a test chain over the four employment states and an
eight-state product with the regime, normal absorbing:
- **Indexing.** `Rfree`, `PermGroFac` and `IncShkDstn` are indexed by the next state, `LivPrb` by the current one, and
  `MrkvArray` is square. So `grows` (ψ fixed at one when unemployed) and `frozen` (growth one as well) can be written
  directly.
- **The limits.** Each state's natural limit is the largest, over reachable next states, of (`mNrmMin` next − the income
  floor)·𝒢ψ_min/R, with the artificial limit inside: the schemas' recursion. Under `BoroCnstInfimum` it reads each
  state's recorded infima.
- **Four states or eight.** The eight-state solve's normal block equals the four-state solve to the stopping error, not
  to rounding: 9.1·10⁻⁹ in c and 3.5·10⁻⁹ relative in v at a tolerance of 10⁻¹⁰, while the four-state solve alone moves
  by 6.1·10⁻⁷ in c between tolerances of 10⁻¹⁰ and 10⁻¹³ on a quarterly chain. The four-state solve is the one for the
  stationary normal-regime results; the eight-state solve gives the recession's rule, which differed from the normal one
  by up to 0.073 in c.
- **Human wealth lags.** The solution's `hNrm` was 130.342583 at 10⁻¹⁰ and 130.358825 at 10⁻¹³, against the closed form
  (I − A)⁻¹A E[ψξ], A_ij = P_ij 𝒢_j/R, of 130.358841; the closed form is what a results file reports.
- **The income measure.** HARK has no transition matrix for the Markov consumer that an adapter can rely on. The measure
  is a linear solve, (I − ℒK_G)μ = the newborns' income mass, normalized afterwards, which needs no stochastic kernel
  but needs the spectral radius of ℒK_G below one.
- **The splurge** has two readings in HAFiscal's code. The family's model schema writes the one the paper's published
  results come from, as the HAFiscal session confirmed (below). An earlier line here called it "in-budget"; HAFiscal and
  HARK use that name for the other reading, so it is dropped.

## The checker's module for the stated member

`markov.py` computes, for each group and type, the chain, the employment marginal μ, the constraint in force and the
natural limits by state, every condition of the family's conditions document as a dominant eigenvalue or by state, the
tail exponents and the income measure's condition. GIC-Harmenberg with ℒ = 1 is not computed: its chain is stated in
words only. Written as the model schema describes, `bst/1`'s toy and untruncated toy reproduce `bst/1`'s condition
margins to 7·10⁻¹⁶, its natural limit in every state (−1.7294 for the toy) and its population tail exponent (33.8601).
Lognormal laws give a zero limit in every state under every switch.

**What it does not establish:** anything about a toolkit's results for the family, whose results document is not yet
written; or the conditions document's deductions (the atom welfare case, the targets by state).

## What HAFiscal's published code and estimates say

From the HAFiscal session's reading of the paper's public replication package, llorracc/HAFiscal-QE, and the paper, on
the evening of 2026-10-22:
- **The discount factors.** The paper's estimates, (β, ∇), are (0.7188167711862781, 0.3176632347321634) for dropouts,
  (0.9290316496364721, 0.07165577531276898) for high school and (0.9825066423553497, 0.013964210199835361) for college,
  in `Results/DiscFacEstim_CRRA_2.0_R_1.01.txt`. The values in `EstimParameters.py`, 0.9647 ± 0.025, 0.98051 ± 0.01676
  and 0.99160 ± 0.00480, which the schemas had carried, are defaults from the Pandemic paper's code. Each group's seven
  types are the equiprobable points center + width·k/3.5, k = −3, …, 3, with a cap that binds for none of them;
  recomputed here, they agree to the last bit.
- **The other values.** Growth 1 + g/4, g = 0.01421, 0.01812, 0.01958; spreads √0.003 and √0.12; the splurge
  0.24611389063967778; job loss u (1/D)/(1 − u), with u = 0.085, 0.044, 0.027 (doubled in a recession) and D = 1.5
  quarters (4 in a recession); job finding 2/3, and 1/4 in a recession; the recession's exit hazard 1/6. The code's
  floats for the rates differ from the doubles nearest their exact values in the last digits; the schemas write the
  nearest doubles.
- **The newborn.** The code sets HARK's mean of log permanent income to the logs of 6.2, 11.1 and 14.5 (thousands of
  dollars a quarter), with spreads 0.32, 0.42 and 0.53, so these are medians, though the paper's text calls them
  averages; the arithmetic means are 6.5257, 12.1235 and 16.6865.
- **What the paper's estimation uses**, group by group, with household wealth (1 − ℷ) a 𝐩: the median ratio of wealth to
  permanent income and the Lorenz shares at 20, 40, 60 and 80 within the group. Its other moments: each group's share of
  total wealth, each pooled quartile's share, and the lottery-year MPC by group, by quartile and pooled. Every one is a
  ratio of partial sums, so generalized Lorenz ordinates and the means carry them exactly.
- **The paper's MPC** is ℷ + (1 − ℷ) c̃′ in the quarter of a win, compounded over the rest of the year, with the
  quarters left drawn at random; its expectation is 1 − (1 − ℷ) ¼ Σ_{n=1..4} (1 − c̃′)^n, which a results file can
  report exactly. Being nonlinear in c̃′, it is not a function of the mean MPC.
- **Tails.** Permanent income's Pareto index under `continues` is 1.47, 1.27 and 1.21 for the three groups, so mean
  wealth is finite and its variance is not; simulated shares converge slowly, and the published model numbers are Monte
  Carlo estimates from one panel.
- **The splurge.** The published code solves the standard problem, takes the optimizer's assets in its own units, and
  reports consumption (1 − ℷ) c̃ 𝐩 + ℷ θ 𝐩 and wealth (1 − ℷ) a 𝐩: the model schema's map exactly, which HAFiscal's
  documents call the bonded-pair reading. The other reading, which they call the splurge in the budget, evaluates c̃ at
  the household's own m; it is not the results of record.
- **Welfare** in the paper is simulated from total consumption, discounted at 1/R, in the experiments; nothing in the
  paper uses the stationary population's E[v], which for the family is a new object.
- **The GIC bound** in the estimation caps β at (1 − ℒ) + 𝒢^ρ/R times a logistic factor; a family that states the GIC
  exactly gets a slightly different bound.
