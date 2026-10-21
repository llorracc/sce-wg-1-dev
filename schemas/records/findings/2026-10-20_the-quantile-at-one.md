# The quantile at probability 1

**The question** (2026-10-20). `bst/1`'s results schema asked for each distribution's quantiles at the fifteen
probabilities of the generalized Lorenz ordinates, 1 included. Should a results file carry Q(1)?

**What moved it** (the HAFiscal-Latest session, from its emitter's ladder of 2026-10-20).
- The emitter's version 0.2 ran on 2026-10-18 and 2026-10-19 under Python 3.11. Version 0.3 ran on 2026-10-20 under
  Python 3.12.3 and numpy 2.5.4, with identical solution code.
- Between them, Q(1) moved in 6 of the 40 values in each of the toy's files at the first three levels, and in 12 of 40 in
  the untruncated toy's first-level file. The largest move was from 61.56 to 4.40, where the distribution grid's top is
  60.
- Q(0.999) moved in none of 160 values. Every other quantity agreed to 3.4·10⁻¹³, or 5.6·10⁻¹² on a Lorenz ordinate
  of 4.6·10⁻⁷.

**The cause is the reading rule.** That session measured it from 22:30 to 22:38 by wrapping its emitter's own population
class.
- Q(p) is read as the first point at which the running total of mass reaches p. Each population's total, summed in
  sorted order, ends within 5·10⁻¹³ of one, from −3.1·10⁻¹³ to +4.8·10⁻¹³ at the first two levels, with either sign.
- **When the total falls short,** the reading returns the last sample: the largest arrival with any positive weight. For
  the untruncated toy's type with β = 0.906, under the income measure at the first level, that is 61.56, with weight
  1.7·10⁻¹⁷⁰. It is an arrival from the grid's top node at the lowest permanent shock, so it lies beyond the grid.
- **When the total overshoots,** the reading returns the point where the tail's remaining mass equals the overshoot:
  4.401, with 1.2·10⁻¹⁵ beyond it.
- So the move between versions is a round-off of 10⁻¹⁵ changing sign. At p < 1 the running total crosses p where the
  distribution function still rises, and a shift of 10⁻¹³ moves nothing.

**In the model, Q(1) is infinite.** The argument is the HARK session's, checked here against the checker.
- At large m saving is asymptotically linear, a(m) ≈ (Þ/R)m. So among survivors m′ ≈ (Þ/(𝒢ψ))m + ξ, a process of
  Kesten's type.
- Where Þ/(𝒢ψ) exceeds one with positive probability, a run of low permanent shocks carries m up without bound. The
  stationary distribution then has a Pareto upper tail, whose index α solves ℒ·E[(Þ/(𝒢ψ))^α] = 1.
- For the toy's most patient type, Þ/𝒢 = 0.9949, but the worst draw gives a factor above one:
  - 1.177 under the toy's truncated law, whose lowest ψ is 0.8453;
  - 1.086 with seven equiprobable points;
  - 1.141 for the community library's member with seven.

  So even a discretized population has no top.
- The checker's own report gives every type of the three members a finite tail exponent:
  - under the population measure: 3.565 for the toy's most patient type (3.563 untruncated), 5.072 for the library
    member, and 89.7 for the toy's least patient type (64.4 untruncated);
  - under the income measure, Harmenberg's: 4.978 for the toy's most patient type and 7.072 for the library member.

  The schema was asking for a number its own checker implies is infinite.

**What a computed Q(1) tracks.** The toy's pooled m in the emitter's ladder of 2026-10-20, read here from its results
files:

| level | grid's top | Q(1) | Q(0.999) | Q(0.99) | mean, GL(1) |
|---|---|---|---|---|---|
| first | 60 | 67.7 | 8.487 | 5.538 | 1.5993 |
| second | 120 | 136.5 | 9.435 (+11%) | 5.992 | 1.6405 (+2.6%) |
| third | 240 | 275.5 | 9.808 (+4%) | 6.166 | 1.6555 (+0.9%) |

Q(1) doubles with the grid's top, while Q(0.999) settles, its changes shrinking with the mean's. At the third level the
top 1 percent hold 4.7 percent of the toy's total m and the top 0.1 percent hold 0.71 percent, from GL(0.99), GL(0.999)
and GL(1).

**The toolkits' answers.** Both were consulted at 22:28, on the owner's question at 22:26.
- **HARK's session: drop Q(1) and keep GL(1).** HARK would stand behind no finite Q(1) from any of its methods:
  - its grid methods put the mass at or above the top on the top node by construction;
  - a simulation's maximum grows with the number of agents, roughly as N^(1/α);
  - analytically, Q(1) = ∞.

  It adds that quantiles read off grid points err by up to a cell's width, and cells are widest near the top. So Q(0.99)
  and Q(0.999) need interpolation within the cell, or tolerances set from the cell's width.
- **HAFiscal-Latest's session: drop Q(1).** HAFiscal uses neither Q(1) nor any maximum of a distribution:
  - the paper's wealth statistics are Lorenz shares and quantile-based targets;
  - the benchmark scores quantiles at 1 to 99 percent, Lorenz shares, the distribution function at points, and capped
    means.

  Where the shocks are bounded, the upper end of the ergodic set is a property of the model, but no quantile of a computed
  distribution. If it is wanted, it would be an optional quantity of its own, with an infinite status.
- **Both:** an optional coverage check beside the maps, which is the next record.

**What follows.** The quantile maps carry the fourteen probabilities 0.01 to 0.999, and the Lorenz maps keep 1, since GL(1)
is the mean (draft pull request #3). Nothing replaces Q(1): Q(0.999) is the maps' top entry. An entry above it would be
the least converged in the map: on a grid it rises with each level, and in a simulation it needs ten times the agents for
each further decade of probability.

**What it does not establish.**
- The tail figures beyond the checker's exponents are HARK's, worked out by hand from the asymptotic saving rule, not
  measured on a solved member.
- The fourth level was not measured.
- Whether interpolating quantiles within a cell should change the comparison's tolerances is left open, with the
  comparison rules.
