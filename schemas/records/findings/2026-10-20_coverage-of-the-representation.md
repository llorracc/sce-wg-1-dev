# How far a representation of the stationary distribution reaches

**The question** (2026-10-20). Both toolkit sessions raised it when consulted on Q(1). GL(0.999) and GL(1) depend on how
much of the upper tail a toolkit's representation holds, and nothing in a results file says how much. Two runs that share
a grid's top can agree to 10⁻¹³ and still show only reproducibility: the emitter's versions 0.2 and 0.3 both cut the
distribution at a top of 60.

**The measurement.** The HAFiscal-Latest session took it from 22:30 to 22:38, from its emitter's own population class. The
third and fourth levels were not measured.
- **First level, grid top 60.**
  - The toy's most patient type holds 3.5·10⁻⁹ of the population measure on the top node, and 9.0·10⁻⁷ above 30. Under
    the income measure: 9.4·10⁻¹¹ and 6.4·10⁻⁸.
  - The untruncated toy's most patient type: 2.8·10⁻⁹ and 7.4·10⁻⁷.
  - Every other type holds at most 2.2·10⁻⁴⁰ on the top node, the three least patient exactly zero. The library member
    holds 4.7·10⁻¹⁷.
- **Second level, grid top 120.**
  - The most patient type holds 4.9·10⁻¹⁰ to 5.6·10⁻¹⁰ on the top node across the two toys, and 7.4·10⁻⁸ to 8.5·10⁻⁸
    above 60. Under the income measure the toy's holds 5.4·10⁻¹² on the top node.
  - The next two most patient types hold at most 7.4·10⁻⁴².
- **The benchmark's own reference** reports 1.0·10⁻¹⁶ for its most patient type at its fourth level.

**What the top's mass is.**
- Both toolkits clip. HARK's two lotteries and the emitter's put every arrival at or above the top on the top node, and
  the lottery also lifts part of the last cell's mass to it.
- So the top node holds what the dynamics send beyond the top each period, plus that share. Its mass is an upper bound on
  that flow, and it measures how much the top binds.
- It is not the model's own mass above the top: a household held at the top moves on from the top, not from where the
  model would have it.
- HARK's rough size, for a Pareto tail with α ≈ 3.6 and a last cell from 50 to 60: the top node holds about 1.4 times the
  clipped tail.
- The emitter's arrivals beyond the grid, such as 61.56, are next period's arrivals from the top node, and the next step
  folds them back onto it.

**What it says about the mean.**
- Along a Pareto tail the mass above x falls as x^(−α), so the tail beyond x contributes about α/(α − 1)·x·P(m ≥ x) to
  the mean.
- The computed mean already counts the clipped mass at the top. So a clipped representation misses about
  top·top_mass/(α − 1), for α > 1; at α ≤ 1 the mean is infinite.
- The top's mass is an upper bound on the flow, so this estimate errs high.
- With α near 3.6, the top's contribution to the mean falls as x^(−2.6), about sixfold for each doubling of the top.
  Under the income measure, with α near 5.0, it falls as x^(−4.0).
- When top_mass is well below 1 − 0.999, Q(0.999) lies below the top, so neither it nor GL(0.999) reads the mass held
  there.

**Why one point is not enough.** This is from HAFiscal-Latest's review. One point cannot tell a tail that continues past
the top from mass piled there by the clamp; two or three can. Along the tail the mass above x falls as x^(−α), and a top
far above that line is truncation. At the first level the patient type held 9.0·10⁻⁷ above half the top, against 3.5·10⁻⁹
on the top node.

**What follows.** An optional `coverage` element, per type and pooled, in the population block and the income-measure
block (draft pull request #4). It holds:
- the variable, m or a;
- the top, and the mass at or above it;
- what the representation does beyond the top: clipped; dropped and renormalized; or kept by a simulation, with its sample
  size;
- an optional list of points below the top, with the mass at or above each, at the toolkit's choice.

The pooled element is given only when the types share a top. Both sessions reviewed the draft, at 22:47 and 22:50. Both
gave final looks on its revision, at 22:58:55 and at 04:45:36 on 2026-10-21, and found it correct. Their two wording
changes are in `029a73f`, on the owner's word of 2026-10-21.

**What it does not establish.**
- Whether the coverage is negligible for every type at the third and fourth levels: these were not measured.
- A statistic comparable across toolkits, for which HARK suggested one shared point. It is on the deferred list.
