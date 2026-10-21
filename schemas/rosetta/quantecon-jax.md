# QuantEcon's JAX code: a Rosetta Stone for `bst/1`

Draft, begun on 2026-10-21; see the [Rosetta Stones](README.md).
- **The toolkit** is the code of QuantEcon's lecture *The Income Fluctuation Problem V: Stochastic Returns on Assets*:
  `lectures/ifp_advanced.md` of QuantEcon/lecture-python.myst, read at commit `96ede2993` of 2026-08-12. It has a model
  container `IFP` with its constructor `create_ifp`, the time-iteration operator `K`, which uses the endogenous grid method,
  and the solver `solve_model`, all in JAX.
- **The cards** are in [`quantecon-jax.cards.yaml`](quantecon-jax.cards.yaml).

## The lecture's model

- **Wealth.** It moves as a′ = R′(a − c) + Y′, with 0 ≤ c ≤ a. The lecture's a is cash on hand.
- **Return and income.** The return is R′ = exp(a_r ζ′ + b_r), and income is Y′ = exp(a_y η′ + z′ b_y). Their innovations
  are IID and independent of each other. z is a Markov state, which the return ignores.
- **Preferences.** The discount factor β is a constant, and utility is CRRA with coefficient γ.
- **The expectation** is an average over Monte Carlo draws of ζ and η.
- **The Euler equation:** (u′∘σ)(a, z) = max{β E_z R̂ (u′∘σ)[R̂(a − σ(a, z)) + Ŷ, Ẑ], u′(a)}.
- **Its conditions** follow Ma, Stachurski and Toda (2020): β E R < 1 for an IID return, and E Y < ∞ and E u′(Y) < ∞.

## The recasting: `bst/1`'s household in the lecture's form

`bst/1`'s normalized household has a law of the right form, m′ = (R/(𝒢ψ′))a + ξ′. But its continuation is
βℒE[(𝒢ψ′)^(1−ρ)v(m′)], with a factor that a constant β cannot carry. Tilting ψ's law by ψ^(1−ρ) removes it. With the
member's nodes ψᵢ and weights wᵢ:
- the weights become w̃ᵢ = wᵢψᵢ^(1−ρ) / Σⱼ wⱼψⱼ^(1−ρ);
- the discount factor is β̃ = βℒ𝒢^(1−ρ) Σᵢ wᵢψᵢ^(1−ρ);
- the returns are R̂ᵢ = R/(𝒢ψᵢ), with the tilted weights;
- ξ's nodes and weights are unchanged, since ξ is independent of ψ.

Then v(m) = max_c {u(c) + β̃ Ẽ[v(m′)]}, the lecture's form, holds exactly. So does the Euler equation:
β̃Ẽ[R̂u′(c′)] = βℒR𝒢^(−ρ)E[ψ^(−ρ)u′(c′)]. The HARK session solved one member both ways, on the same nodes and the same
grid: the rules agree to 1.3·10⁻¹⁵ and the values to 1.2·10⁻¹³.

**An equivalent change of the code, suggested by Matsya.** Keep the untilted law and R̂ = R/(𝒢ψ′). In `K`'s integrand,
return R̂^ρ·u′(c′) in place of R̂·u′(c′), and replace β by βℒR^(1−ρ). This is the same Euler equation, since
R̂(𝒢ψ′)^(1−ρ) = R^(1−ρ)R̂^ρ. The tilt is preferred: it leaves the lecture's operator as written, and needs only the weighted
nodes that the unemployment node needs anyway.

Three cautions:
- **Tilt the member's nodes; don't discretize a tilted law.** Then the two toolkits' effective members have the same
  nodes.
  - For an untruncated lognormal ψ, the tilted law is a lognormal whose log-mean moves by (1 − ρ)σ². That gives a_r = σ
    and b_r = log R − log 𝒢 + σ²/2 − (1 − ρ)σ².
  - The lecture's R is never truncated, so the toy needs nodes.
- **Only the household's problem is tilted.** Anything that is an expectation of m′ uses the untilted law: the target, the
  balanced-growth point and the growth patience factors.
  - With HARK's rule for one member, the target is 2.138153 under the true law and 2.213246 under the tilted one.
  - The households' stationary measure uses ψ's law as given. The income measure tilts by ψ, not by ψ^(1−ρ).
- **β̃ < 1 is the FVAC.** The lecture's check, β E R < 1, becomes βℒR𝒢^(−ρ)E[ψ^(−ρ)] < 1.
  - That is sufficient for the lecture's argument, and stricter than the GIC-Mod for ρ ≥ 1.
  - A `bst/1` member that satisfies the RIC and the FVAC but fails that check still has a solution. So the adapter reports
    the check's value and does not stop on it.

## The lexicon

| `bst/1` | the lecture | where the lecture differs, and what the adapter does |
|---|---|---|
| m | `a`, cash on hand | — |
| a = m − c | `s`, savings | — |
| ρ, `crra` | `γ` | — |
| β, `types[].beta`, with the shares, `types[].share`; ℒ, `survival`; 𝒢, `income.growth`; the law of ψ, `income.permanent_shock` | `β`, as β̃ | the recasting, with one solution per type; the adapter pools the types with the shares |
| R, `return`, with ψ and 𝒢 | `R`, as R̂ᵢ = R/(𝒢ψᵢ) with the tilted weights | `R = exp(a_r ζ + b_r)` is an untruncated lognormal, so the adapter passes nodes |
| ξ, from θ (`income.employed_shock`), ℘ (`income.unemployment.prob`) and ξ̲ (`income.unemployment.income`) | `Y` | `Y = exp(a_y η + z b_y)` cannot hold the unemployment node, and with one state its mean is exp(a_y²/2), not one. The adapter passes ξ's nodes and weights |
| the shocks' independence over time | `P`, the Markov chain of z | one state |
| a̲_Art, `borrowing_constraint`, and a̲_Nat | 0 ≤ c ≤ a | the lecture has no borrowing: its constraint in force is 0, which is `bst/1`'s max(a̲_Art, a̲_Nat) when a̲_Art = 0. A constraint below 0 needs the savings grid to start at a̲, and the anchor at (m, c) = (a̲, 0) |
| the newborn, and deaths at 1 − ℒ | none | the lecture's households start at half the grid's top and never die. The adapter computes the population itself |
| V | none | the lecture iterates on consumption only. The adapter adds an evaluation of v under the converged rule |

## What the code needs, beyond the recasting

These come from the HARK and HAFiscal-Latest sessions' readings of the lecture's code, checked here against its source.
1. **Weighted nodes.** `K` averages with `jnp.mean` over the product of 100 draws of η and 100 of ζ, and equal weights
   cannot carry the tilted ψ or the unemployment node. Two weight vectors replace the mean.
2. **Double precision.** The lecture never enables 64-bit floats, so it runs in single precision, about 10⁻⁷. The adapter
   enables them before any array is made.
3. **The kink.**
   - After the endogenous-grid step, `K` sets the first pair to (0, 0), on `s_grid = linspace(0, grid_max, grid_size)`.
     By default that is 100 points up to 100.
   - This replaces the point where the constraint starts to bind with a chord from the origin, which undershoots c = m near
     it.
   - The adapter keeps the kink's point, prepends (0, 0), and nests the grid toward the constraint.
4. **Above the grid.** `jnp.interp` holds c constant beyond the last point, so savings rise one for one there.
   - That changes the rule near the top, and the distribution's upper tail, for the patient types.
   - Linear extrapolation is the least fix. Better is the approach to the limiting linear function, as HARK does.
5. **The value.** An evaluation step for v, for the welfare blocks, in pseudo-inverse form to avoid −∞ at the limit.
   Discounted utility along simulated paths, which the method target `cntn_to_dcsn.value` also allows, carries a standard
   error, and so compares only at that error.
6. **The population:** deaths at 1 − ℒ, `bst/1`'s newborns, the two measures, and the coverage of the representation.
   - The adapter's own lottery does all of these.
   - By simulation instead, the lecture's code would need three things. A household dies with probability 1 − ℒ, and is
     replaced by a newborn whose m is an employed draw. Permanent income p is tracked, since the income measure weights
     households by p. And the run lasts until the stationarity residual is small, not a fixed T.
7. **The MPC.** A linear interpolant's MPC is piecewise constant, so the MPC is compared at the request points, or by one
   common finite difference.

The lecture's assumption E u′(Y) < ∞ fails when ξ̲ = 0, as in the `library` member. So the lecture's theory does not
cover that member, although the algorithm still runs on nodes.

## The method, the adapter and the evidence

- **The method.** Time iteration with the Coleman–Reffett operator, by the endogenous grid method. Its settings are:
  - the savings grid: `grid_max` and `grid_size`;
  - `tol` and `max_iter`;
  - the nodes.
- **The adapter** is not written yet. Its legs:
  - *encode*, from a member and the settings to an `IFP` with β̃, the R̂ᵢ with the tilted weights, and ξ's nodes;
  - the call, `solve_model`;
  - *decode*, from the rule σ to the results file. The adapter computes the population, the value and the conditions from
    the untilted laws.
- **The evidence.** The recasting, checked by the HARK session on one member against BST's form and HARK's solution. No
  adapter run yet.

## Sources

- The lecture's source, `lectures/ifp_advanced.md` at `96ede2993`.
- Ma, Stachurski and Toda (2020), *The income fluctuation problem and the evolution of wealth*, for the lecture's
  conditions.
- The HARK session's and the HAFiscal-Latest session's readings of the code, on 2026-10-21, and the HARK session's check of
  the recasting.
