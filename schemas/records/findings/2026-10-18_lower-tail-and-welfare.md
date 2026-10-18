# The lower tail of the stationary distribution, and when welfare is finite

A finding of 2026-10-18, derived here while specifying the welfare block of the results schema, checked and corrected by the
BufferStockTheory session the same day, and recorded in that repository. BST's notation.

**What it establishes.** Population welfare W = E[v(m)] and the mean felicity F = E[u(c(m))] need E[(m − m̲)^{−(ρ−1)}] under
the stationary population to be finite, and the mean marginal utility M = E[u′(c(m))] needs E[(m − m̲)^{−ρ}], where m̲ is the
lowest resources from which positive consumption is feasible. The lower tail depends on the constraint and on the laws at
their lowest values:
- With a binding artificial constraint (a̲_Art > a̲_Nat, the kink's existence), all three means are finite. An income floor
  alone does not bound consumption below: the natural constraint moves down by the floor's capitalized value and consumption
  still goes to zero there, which is BST's own remark on a nonzero minimum of ξ.
- Under the natural constraint alone with an atom of mass p̲ at the worst income (BST's zero-income event), the tail is a
  power law from runs of worst-income draws, each continuing with probability p̲ℒ and shrinking resources above m̲ by
  p̲^{1/ρ}Þ/(𝒢ψ), and E[(m − m̲)^{−q}] is finite exactly when p̲^{1−q/ρ} ℒ (𝒢/Þ)^q E[ψ^q] < 1. At q = ρ this reads
  ℒ(𝒢/Þ)^ρ E[ψ^ρ] < 1, which the GIC defeats without mortality: in BST's baseline the mean marginal utility is infinite for
  every growth-impatient household, although each household's is finite.
- Under the natural constraint alone with a positive density at the floor in n of the two shocks, the stationary tail's
  exponent is max(n, ρ): W and F are finite for every ρ, and M exactly when ρ < n.
- A density that vanishes at the floor faster than any power, the untruncated lognormal at zero, leaves every moment finite.

**Evidence.** The BufferStockTheory session checked the slope near the constraint against the paper's lemma (κ̄ exactly),
found that the paper states no lower-tail result, and measured the tail exponent on an EGM solution at the paper's baseline,
1.974 against a predicted 1.977, with the truncated mean of u′(c) climbing about five percent per decade of truncation as
predicted; it also gave a second proof for the marginal case by integrating the Euler equation over the stationary
distribution. The value's condition number at the baseline, 0.0729, reproduces. The mirror with the paper's upper-tail
condition is exact in form: ℒ E[(Þ_𝒢/ψ)^ζ] = 1 above, p̲ℒ E[(δ/ψ)^{−α}] = 1 below.

**What it does not establish.** The two-density landing law (n = 2) and the logarithmic factor at ρ = n are deductions not
yet run; the regimes were checked numerically for one density only.

**Consequences.** `conditions.md` carries the four cases in its simulation-phase section; the checker classifies every member
and reports W, F and M, and M's bottom quartile, as `undefined` where the moment is infinite; a results file must report that
status with the number, since a finite-sample estimate of an infinite mean looks stable.
