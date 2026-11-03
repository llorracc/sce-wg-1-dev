# HAFiscal's Lorenz targets are computed on wealth in levels

Asked of the HAFiscal-Latest session at 05:14 on 2026-11-03, after the owner's ruling of 05:12 that the targets must be
of wealth in levels; answered the same morning from the published code, llorracc/HAFiscal-QE, paths under
`Code/HA-Models/` unless they say otherwise. Two public versions differ on some points:
- **[P]** branch `qe2442-proof-sync`, commit `5aa25fb`: the code the paper's numbers come from;
- **[D]** the default branch `with-precomputed-artifacts`, commit `8d8b71e`: the replication package, a later revision.

Line numbers are [P]'s; [D]'s follow in brackets where they differ. The reading is the HAFiscal session's; the schema
session has not opened the files.

## The variable

End-of-period liquid assets in levels, aLvl = aNrm · pLvl: after the quarter's consumption, before the next quarter's
return and income, read from every agent's state at the last simulated quarter and given to HARK's `get_lorenz_shares`.
- Step 1, `Target_AggMPCX_LiquWealth/Estimation_BetaNablaSplurge.py`, the model the toy-hafiscal experiment follows:
  the raw aLvl at :146 [D :360, through a splurge correction in levels that equals aLvl at splurge 0]; the whole curve
  at 1% to 99% (:164, :167) after shifting wealth so that the poorest agent holds zero (:166), which does nothing with
  a ≥ 0 and someone at the constraint; the targeted points the 20/40/60/80 shares (:169), as fractions, against
  [0.029, 0.354, 1.84, 7.42]/100 (:93), the population-wide SCF curve [D 379, 382, 381, 384, 230].
- Step 2, `FromPandemicCode/EstimAggFiscalMAIN.py`, not the toy's model: (1 − s) · aLvl (:163), the shares at
  20/40/60/80 in percent (:170), per education group with each group's median wealth-to-permanent-income ratio;
  the population-wide curve is computed (:90) but not targeted.

## Why levels

Neither the code nor the paper says so in words; it is in how the targets are built. `Code/Empirical/make_liquid_wealth.py`,
the same in both versions, sorts households by liquid wealth in dollars (:274), accumulates weighted dollars (:275-277)
and reads the share held by the bottom 20/40/60/80% of weighted households (:281-282; by education, :304-317). The
model's statistic is built the same way from aLvl. Where a data statistic is a ratio to the household's own permanent
income, Step 2's median of liquid wealth over permanent income (:241), the model uses aNrm. So each model statistic is
computed on the same object as its data counterpart: dollars with aLvl, ratios with aNrm. The Lorenz curve of aNrm is a
different curve whenever pLvl varies across households. It is not a convention of HARK's tools: `get_lorenz_shares`
takes whatever array it is given. The paper's words "at the 20th, 40th, 60th, and 80th income percentiles"
(`Subfiles/Parameterization.tex:23`) are to be read as wealth percentiles: the data script and the code both rank
households by liquid wealth.

## Pooling and timing

- Pooling by population shares, through agent counts, with equal weight per agent: Step 1 has seven types (:36) at the
  midpoints of seven equal parts of [β − ∇, β + ∇] (:127), 5,000 agents each (:50), concatenated unweighted (:146,
  :164).
- One date, the last simulated quarter: every agent starts at birth and `simulate()` runs T_sim quarters, 800 in Step 1
  (:52, :145); nothing is averaged over periods.
- Stationarity: Step 1 has survival 1 − 1/160 (:57) and no age cap (:69), so at 800 quarters about 0.66% of agents are
  the original newborns; close to stationary. [D] caps age at 200 quarters (`EstimParameters.py:496`).

## The wealth-to-income target, 6.60 (Step 1 only)

- Numerator: the sum of the same wealth array the Lorenz shares use (:172).
- Denominator: the sum of pLvl × TranShk over the same agents in the same quarter (:173-175): realized quarterly
  non-capital income, the unemployment benefit inside TranShk (UnempPrb 0.044, IncUnemp 0.60, :62-63), the shock's
  mean one. Not permanent income and not annualized: 6.60 is 6.6 quarters of income.
- Distance ((6.60 − K/Y)/6.60)² (:344) [D 396, 397-399, 191-192, 574].
- Source: the paper calls it "the mean liquid wealth to income ratio of 6.60" (`Subfiles/Parameterization.tex:23`) and
  the package's table notes a "US capital-to-income ratio" (`Tables/MPC_WQ_sources.md:64-65`); neither gives one. The
  HAFiscal session is looking further.

## The newborns' permanent income

- Step 1: not dispersed; pLogInitStd 0.0 (`Target_AggMPCX_LiquWealth/SetupParamsCSTW.py:126` [D :136]), inherited at
  `Estimation_BetaNablaSplurge.py:42`, pLogInitMean 0 (:61). But HARK multiplies a newborn's pLvl by the aggregate
  level PlvlAgg, which grows by PermGroFacAgg = 1.01^0.25 each quarter (:67), while an incumbent's pLvl does not grow
  (PermGroFac 1, `SetupParamsCSTW.py:66`). So later cohorts start higher, by 1% a year of birth date: a dispersion of
  levels the normalized distribution does not see. Checked by that session in HARK 0.17.2 (`sim_birth` multiplies by
  PlvlAgg, `transition` grows it), not in 0.14.1.
- Step 2: dispersed by education group, 0.32/0.42/0.53 (`EstimParameters.py:88-90`).

## What it establishes for the schemas

- The targets are Lorenz shares of end-of-period assets in levels, a𝐩, across households ranked by them, at p = 0.2,
  0.4, 0.6 and 0.8: GL(p)/GL(1) of a𝐩 under the population measure, pooled over types by share. That is the block
  "the distribution of wealth in levels" of the results schema ([`bst/results.md`](../../bst/results.md)), drafted on
  this answer.
- K/Y is E[a𝐩] over the economy's mean income E[ξ𝐩]: the income measure's mean of a, up to the newborns' employed
  branch (about 10⁻⁴). HAFiscal's realized-income denominator equals it in expectation.
- The schemas' populations are stationary distributions, not dates; a toolkit that simulates records its periods,
  burn-in and seed with the joint, as the results schema asks.
- **The economy differs, and the choice is the owner's.** The published Step 1 household has 𝒢 = 1, and its economy
  grows through its newborns: relative to the current newborn, an agent's permanent income is 𝒢_agg^(−age) Π ψ with
  𝒢_agg = 1.01^0.25, falling with age. The toy-hafiscal member states 𝒢 = 1.0019026 for every household with the
  newborn at 𝐩 = 1 ([`bst/model.md`](../../bst/model.md)): relative to the newborn, 𝒢^age Π ψ, rising with age. The
  household's problem and the distribution in levels both differ, so a Lorenz fit on one economy does not transfer to
  the other. HAFiscal's tools can estimate the member as stated, with PermGroFac = 1.0019026, PermGroFacAgg = 1 and
  newborns at 1; the HAFiscal session was told so. Mirroring the published Step 1 instead would need the family to
  state a newborn's permanent income as a level law carrying a trend, which it does not have.

## What it does not establish

- The source of the data value 6.60.
- How close to stationary 800 quarters is for the levels distribution; the HAFiscal session was asked to read the
  statistics on a pooled set of late quarters as well, if cheap.
- The newborn's first-period conventions in the estimation, HARK's defaults against the family's, already recorded
  as a reason to evaluate the fit again on the delivered member.
