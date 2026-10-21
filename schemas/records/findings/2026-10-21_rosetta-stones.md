# The Rosetta Stones' first findings

What was learned on 2026-10-21 while the stones for HARK and QuantEcon's JAX code were drafted (draft pull request #6).
Times are EDT.

## The recasting of `bst/1`'s household into the lecture's form

The lecture on the income fluctuation problem with stochastic returns, `ifp_advanced` at `96ede2993`, has a constant
discount factor. `bst/1`'s normalized household has a law of the lecture's form, but its continuation carries the factor
(𝒢ψ′)^(1−ρ). The proposal: tilt ψ's nodes by ψ^(1−ρ). Then
- the discount factor is β̃ = βℒ𝒢^(1−ρ) Σᵢ wᵢψᵢ^(1−ρ);
- the returns are R̂ᵢ = R/(𝒢ψᵢ), with the tilted weights;
- the household's problem is exactly the lecture's.

**The check.** The HARK session solved one calibration both ways, on the same nodes and grid, with HARK's code at
`4c285e86`. The calibration was HARK's defaults with the income while unemployed set to 0 and the natural limit, on 200 grid
points up to 40. It was not a `bst/1` member.
- The rules agree to 1.3·10⁻¹⁵, and the values to 1.2·10⁻¹³.
- HARK's own consumption rule agrees with both to 2.2·10⁻⁵. The gap stays at HARK's tolerance 10⁻¹³, so HARK's stopping
  rule does not cause it. Its value function agrees to 5.4·10⁻⁴ relative, falling to 3.6·10⁻⁴ at that tolerance.
- **Only the household's problem is tilted.** Every expectation of m′ uses the untilted law. With HARK's rule for that
  calibration, the target is 2.138153 under the true law and 2.213246 under the tilted one.
- The lecture's stability check becomes βℒR𝒢^(−ρ)E[ψ^(−ρ)] < 1: a sufficient condition, stricter than the GIC-Mod.
- β̃ is HARK's `VAFac` times ℒ: HARK's `VAFac` leaves ℒ out, where its other factors include it.

The community-library session's module (below) took the other exact route, the normalized Euler equation written into
the code. It showed the tilt agrees through its weights, to 4·10⁻¹⁶ in the rule and 7·10⁻¹⁵ in the value, on the
`library` member.

## Readings of HARK at `4c285e86`

Read there by the HARK session for the HARK stone, with these corrections to the first draft:
- **The limiting MPCs** are `bilt`'s closed forms, max(1 − `RPFac`, 0) and 1 − `WorstPrb`^(1/ρ)·`RPFac`, or 1 where the
  artificial constraint binds. `solution[0]`'s values are the solver's iterates, which approach them.
- **The target and the balanced-growth point** are NaN unless the GICRaw holds. A subclass must call
  `calc_stable_points(force=True)` itself.
- **Harmenberg's measure by simulation.** `neutral_measure` is an argument of HARK's own lognormal constructor, so with a
  member's own nodes the adapter tilts its own weights. Each death is replaced by one unweighted newborn, so the tilt alone
  is exact only when 𝒢 = 1 or ℒ = 1. This was derived from the code, not measured.
- **HARK stores no natural limit;** it is a local variable of the solver. An adapter computes the effective member's limit
  from the nodes' lowest values.

**A finding about HARK's default tolerance.** HARK's infinite-horizon iteration stops on the distance between successive
rules, measured on the rule's knots alone. Human wealth `hNrm` and the limiting function above the grid are left out of
that distance, and lag. On HARK's defaults, at the default tolerance of 10⁻⁶:
- `hNrm` is 44.99, against its limit of 50.50;
- consumption above the grid is off by 0.0115 at m = 60 and 0.035 at m = 100, against less than 4·10⁻⁵ within the grid;
- a tolerance of 10⁻⁸ keeps the gap at m = 60 below 10⁻⁴.

This is a HARK matter, and it is on the HARK session's own list. The benchmark's emitter is not affected: it solves at
tolerances of 10⁻⁸ to 10⁻¹², and every point it reports, and its whole population, lies below its solution grid's top.

## Matsya's three sessions

Run from the bellman session, questions only, with public material.
- **The first,** 08:57 to 09:09, on four questions:
  - Its index holds one public passage on Bellman's Rosetta stone, and nothing on a card's fields.
  - Its HARK answers were its own recollection, since its retrieval allowance was spent.
  - On the lecture, it found that the code cannot state `bst/1` as written, and proposed changing the Euler integrand: an
    equivalent route, though it missed the tilt. It also found that the kink is lost.
  - On comparison, it put the effective members first.
  - Taken: Bellman's narrower notion of a stone, with this project's two ends added; the effective members compared first;
    a Monte Carlo toolkit's suite varying its draws, seed, periods and households; the residuals as diagnostics; the
    equivalent change of the code.
  - Out of date where it differed from HARK's code: the newborn's older parameter names, and transition-matrix methods that
    now live on another of HARK's types.
- **The second,** 09:24 to 09:35, on HARK alone: the parameter names were confirmed from HARK's documentation pages, and the
  rest stayed open, the solver's module exceeding the retrieval allowance.
- **The third** waits for the owner's word in the bellman session. Its material is six verbatim excerpts of HARK at
  `4c285e86`, checked block by block: the income process, the discretization, the one-period solver, the type's defaults,
  the stationary distribution, and the newborns.

## The community library

- **Akshay Shanker's solution.** QuantEcon's community library merged it as pull request 5, late on 2026-10-19: the
  library's shared description of the buffer-stock model and a HARK implementation. A later pull request of the library
  moved the implementation to `solutions/buffer-stock/001-hark-egm/`. It uses HARK alone, at `econ-ark` 0.17.1. Its
  independent check is an endogenous-grid solver written in NumPy and SciPy, and it uses no QuantEcon package. Its
  calibration is `bst/1`'s `library` member.
- **A QuantEcon module, local and unpublished,** in the owner's fork of the library, by a session started on 2026-10-21. It
  extends the lecture's code so that a `bst/1` adapter can drive it.
  - It writes the normalized Euler equation in, handles unemployment exactly and keeps the kink.
  - It extrapolates linearly, evaluates the value by policy evaluation, and simulates the population with deaths, `bst/1`'s
    newborns and both measures.
  - Its reported numbers agree with `001-hark-egm` to 4·10⁻⁶ up to m = 15. At m = 20, the top of `001-hark-egm`'s grid,
    that solution's published consumption is 1.3·10⁻⁴ high.
  - Its natural borrowing limit, computed from its own nodes, matches HARK's on the same nodes to 10⁻¹², on the toy's laws
    untruncated. Consumption agrees to 10⁻¹² from just above the limit to 20 above it.
  - The value needs the grid's bottom near 10⁻⁶ where the worst income is zero or the limit is the natural one. From
    10⁻³, the value is off by about 10⁻³ relative, in HARK as in the module.

## What it establishes

- `bst/1`'s household can be stated exactly in the lecture's form, and the code needs eight extensions, which the stone
  lists.
- HARK's limiting MPCs, its targets and its tolerance above the grid each need care that the stone now records.
- A QuantEcon solution of `bst/1`'s members exists and agrees with HARK, locally.

## What it does not

- The recasting was checked on one calibration with HARK's defaults, not on a `bst/1` member.
- No adapter is written, and no two toolkits' results files have yet been compared through the results schema.
- The QuantEcon module is not published, so nothing pins it.
