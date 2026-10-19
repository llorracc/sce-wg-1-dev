# The Markov family's constraint in force is a fixed point, not a maximum

**The question** (2026-10-19, raised while weighing the bellman session's advice on the stage files' `max`). Is the
constraint in force in employment state z of `bst-markov_ui-and-agg/1` the larger of the artificial limit and that state's
natural limit, max(a̲_Art, a̲_Nat(z)), as the family's conditions document then said? Or must the artificial limit enter the
recursion over the states, a̲(z) = max(a̲_Art, max over successors z′ of (Γ(z′) ψ̲(z′)/R)(a̲(z′) − ξ̲(z′)))? The second
follows from the household's problem: a state's limit must keep feasible the constraint in force in every state that can
follow, and where the artificial limit binds next quarter, it is the constraint to keep feasible.

**HARK computes the second.** Its Markov solver (`HARK/ConsumptionSaving/ConsMarkovModel.py`) takes a state's natural bound
from the next states' lowest resources, `solution_next.mNrmMin`, which already include the artificial limit `BoroCnstArt`.

**The computation.** Both forms by iteration over the family's four states, E → {E, U_2}, U_2 → {E, U_1},
U_1 → {E, X}, X → {E, X}, at R = 1.01, 𝒢 = 1.0036, and the lowest values of the toy's truncated laws at ±3, ψ̲ = 0.84531
and θ̲ = 0.328485, with employed income e θ and e = 1. The multiplier Γψ̲/R is 𝒢ψ̲/R in every state under `continues`; under
`frozen` the unemployed states' is 1/R. For each calibration the artificial limit was swept from the lowest to the highest
natural limit and beyond, and the largest gap between the two forms recorded:

| world | ξ_U | ξ_X | natural limits (E, U_2, U_1, X) | largest gap |
|---|---|---|---|---|
| `continues` | 0.7 | 0.5 | −1.724 in every state | 0 |
| `continues` | 0.7 | 0.15 | −1.637, −1.249, −0.787, −0.787 | 0 |
| `frozen` | 0.7 | 0.5 or 0.15 | −1.724 in every state | 0 |
| `continues` | 0.3 | 0.5 | −1.616, −1.624, −1.633, −1.633 | 0.012 |
| `continues` | 0.05 | 0.5 | −0.668, −0.745, −0.837, −0.837 | 0.119 |
| `continues` | 0.0 | 0.5 | −0.478, −0.569, −0.677, −0.677 | 0.141 |

**What it establishes.** The two forms agree whenever the states without a self-transition, U_2 and U_1, have high incomes,
as the paper's benefits are; they differ, by up to a seventh of permanent income in these examples, when benefits are low,
because the artificial limit binding in such a state tightens the limit of the state before it. They agree in `bst/1`, which
has one state, at a zero artificial limit, and under untruncated laws, where the employed state, which can follow every
state, has a lowest income of zero and so every limit is zero. Under `frozen` the limits came out the same in every state,
since a larger multiplier makes a state's term more negative and so loosens the limits before it; the conditions document had
said the reverse.

**What followed.** The family's conditions and model documents state the constraint in force as the fixed point
(2026-10-19, on the owner's word); the stage file's single limit stays, exact for the lognormal laws it states; a stage file
with bounded laws will need the four per-state limits, which the bellman session showed the language can state.

**What it does not establish.** The examples are four states with the toy's laws; no general bound on the gap is derived.

The computation, for reproducing it:

```python
succ = {"E": ["E", "U2"], "U2": ["E", "U1"], "U1": ["E", "X"], "X": ["E", "X"]}
def limits(kappa, xi_lo, a_art=None, n=20000):
    a = {z: -100.0 for z in succ}
    for _ in range(n):
        new = {z: max(kappa[s] * (a[s] - xi_lo[s]) for s in succ[z]) for z in succ}
        a = new if a_art is None else {z: max(a_art, v) for z, v in new.items()}
    return a
# the gap at a given a_art: max over z of |limits(kappa, xi_lo, a_art)[z] - max(a_art, limits(kappa, xi_lo)[z])|
```
