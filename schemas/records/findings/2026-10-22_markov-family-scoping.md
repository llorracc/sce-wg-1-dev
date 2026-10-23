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
- **The splurge** has two readings in HAFiscal's own code, in the budget or outside it; the family's model schema writes
  the in-budget one. Which the paper's results use is asked of the HAFiscal session.

## The checker's module for the stated member

`markov.py` computes, for each group and type, the chain, the employment marginal μ, the constraint in force and the
natural limits by state, every condition of the family's conditions document as a dominant eigenvalue or by state, the
tail exponents and the income measure's condition. GIC-Harmenberg with ℒ = 1 is not computed: its chain is stated in
words only. Written as the model schema describes, `bst/1`'s toy and untruncated toy reproduce `bst/1`'s condition
margins to 7·10⁻¹⁶, its natural limit in every state (−1.7294 for the toy) and its population tail exponent (33.8601).
Lognormal laws give a zero limit in every state under every switch.

**What it does not establish:** anything about a toolkit's results for the family, whose results document is not yet
written; or the conditions document's deductions (the atom welfare case, the targets by state).
