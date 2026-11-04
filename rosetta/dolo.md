# dolo: a Rosetta Stone for the buffer-stock families

Draft, begun on 2026-11-01; see the [Rosetta Stones](README.md).
- **The toolkit** is dolo, EconForge's language and solvers for dynamic models (github.com/EconForge/dolo.py). It is
  read in its release 0.4.9.20, tag `v0.4.9.20` at `d782336b`, with dolang 0.0.20, on Python 3.11. That release needs
  Python ≥ 3.9 and < 3.12, numpy < 2, pandas < 2 and xarray < 2023. The repository's master, at `33f873ee` of
  2026-10-19, has moved to Python ≥ 3.12, numpy ≥ 2 and JAX, but is untagged and still says 0.4.9.20. The stone and the
  adapter use the release.
- **The cards** are in [`dolo.cards.yaml`](dolo.cards.yaml).
- **What a model is in dolo:**
  - a YAML file: symbols, equations, a calibration, a domain for the states, an exogenous process and options;
  - the solvers in `dolo.algos`: time iteration, improved time iteration, value iteration, perturbation, and the
    endogenous grid method;
  - `ergodic_distribution`.

## dolo's own buffer-stock model

`examples/models/consumption_savings_iid.yaml`, the same at the tag and on master, is solved by `dolo.algos.egm.egm` in
`tests/test_egm.py::test_egm_iid`:

```yaml
symbols: {exogenous: [y], states: [w], expectations: [mr], poststates: [a], controls: [c],
          parameters: [β, γ, σ, ρ, r, cbar]}
equations:
    transition:   w[t] = exp(y[t]) + (w[t-1]-c[t-1])*r
    arbitrage:    β*( c[t+1]/c[t] )^(-γ)*r - 1  | 0.0<=c[t]<=w[t]
    half_transition:     w[t] = exp(y[t]) + a[t-1]*r
    reverse_state:       w[t] = a[t] + c[t]
    expectation:         mr[t] = β*( c[t+1]/cbar )^(-γ)*r
    direct_response_egm: c[t] = cbar*(mr[t])^(-1/γ)
exogenous: !UNormal {sigma: σ}          # y, i.i.d. normal
```

- **It is Deaton's problem,** not BST's. Cash on hand w moves as w′ = r(w − c) + exp(y′), with i.i.d. normal y, a
  constant gross return r, and no borrowing. It has no permanent shock, no growth and no zero-income event, and its
  income exp(y) is lognormal with mean exp(σ²/2), not one.
- **Its four EGM blocks:**
  - `half_transition` takes this period's savings to next period's state;
  - `expectation` is the discounted marginal value next period;
  - `direct_response_egm` inverts the Euler equation for c;
  - `reverse_state` recovers the state from the savings and the choice.
- **Ran on 2026-11-01** in the pinned environment: it converges in 475 iterations, with c = w below its kink and c(4) =
  1.149.

## The recasting: the buffer-stock families' household in dolo

The household, normalized by permanent income, fits dolo's blocks directly. dolo lets the transition use the exogenous
variables of the same period and the arbitrage those of the next. So R/(𝒢ψ′) in the transition and (𝒢ψ′)^(−ϱ) inside
the expectation are written as they are. A bound of the complementarity may depend on the state, so c ≤ m − a_min is
allowed:

```yaml
symbols:
    exogenous: [psi, xi]
    states: [m]
    poststates: [a]
    controls: [c]
    expectations: [mr]
    parameters: [beta, L, rho, R, G, a_min, cbar]
equations:
    transition:
        - m[t] = (m[t-1]-c[t-1])*R/(G*psi[t]) + xi[t]
    arbitrage:
        - beta*L*R*((G*psi[t+1]*c[t+1])/c[t])^(-rho) - 1 | 0.0 <= c[t] <= m[t] - a_min
    half_transition: |
        m[t] = a[t-1]*R/(G*psi[t]) + xi[t]
    reverse_state: |
        m[t] = a[t] + c[t]
    expectation: |
        mr[t] = beta*L*R*(G*psi[t+1]*c[t+1]/cbar)^(-rho)
    direct_response_egm: |
        c[t] = cbar*(mr[t])^(-1/rho)
domain:
    m: [0.0, 200.0]
options:
    grid: !Cartesian
        orders: [40001]
```

- **The exogenous process.** The block `exogenous:` holds only a placeholder. The adapter passes the member's joint
  nodes of (ψ, ξ) to `egm` as `dp`, a `dolo.numeric.distribution.FiniteDistribution` of points and weights. Those are the
  same nodes HARK's adapter builds: `law_nodes`, then `joint_shocks`. `FiniteDistribution` has no tag in the model-file
  language, but the solvers take it as an argument.
- **Survival** enters as β ℒ in the expectation, as in the stage file. R is not divided by ℒ: the assets of the dead
  vanish.
- **The savings grid** is `egm`'s `a_grid`.
  - For an artificial member it starts at a_min = `a_Art`, so that the kink's point is solved.
  - For a natural member it starts just above the limit. At a = 0 the zero-income event would put next period's c at
    0, where marginal utility has no finite value.
- **The rule.** `egm` iterates on the endogenous points with linear interpolation. It then evaluates that rule, clipped
  to the bounds, at the nodes of the model's uniform grid (`domain` and `options.grid`), and returns a cubic spline
  through those values. So the uniform grid must be fine near the kink: the adapter puts a point every 0.005 at every
  level, 20,001 points up to m = 100 at level 1 and 80,001 up to m = 400 at level 3.

## Capabilities against the ontology and the schemas

| | what dolo's model file expresses | what the adapter supplies | tested |
|---|---|---|---|
| the natural scenario with a point mass, `bst-natural/1` | the transition, the Euler equation, and c ≤ m as the bound, which coincides with the natural limit at 0 | the laws' nodes with the zero-income atom; a savings grid starting above 0 | yes: the restrained-limit suite's three members and `library`, verified; within 2.4 · 10⁻⁵ of HARK at level 3 |
| the artificial scenario, `bst-artificial/1` | c ≤ m − a_Art | the savings grid from a_Art, and the kink's point | yes, a_Art = 0: `bst-restrained` and `toy`, verified; the same as HARK's below the kink to machine precision, within 1.1 · 10⁻⁵ above it at level 3 |
| truncated lognormal laws | none: `Truncation` exists in Python only, and needs a `cdf` that `LogNormal` lacks | the nodes, as a `FiniteDistribution` | yes |
| untruncated lognormal laws | `!LogNormal`, whose default μ is 1, not −σ²/2 | the nodes. dolo's own equiprobable nodes are bin medians, not conditional means, so their mean is not one | — |
| the zero-income event | `!Mixture` with `!Bernouilli`, its inner laws cut into a fixed 5 nodes | the atom ξ_u with weight ℘, in the joint nodes | yes |
| discount-factor types | one β per model | one solve per type, pooled with the shares | `toy`'s types |
| survival ℒ | β ℒ | — | ℒ = 1 only |
| the newborn and deaths | none: `ergodic_distribution` has no deaths and no newborns | the shared population of the adapters | yes, through the shared code |
| Markov states | `!MarkovChain`; `egm` loops over the chain's states | — | no |
| the value V | none from `egm`; `evaluate_policy` needs a `felicity` block | welfare reported as not computed | — |
| the MPC | the `DecisionRule` has no derivative | the slope of the rule read linearly through the spline's node values | yes: within 0.012 of HARK's at level 3 |

## The lexicon

| the buffer-stock families | dolo | where dolo differs, and what the adapter does |
|---|---|---|
| m | `m`, the state | — |
| a = m − c | `a`, the poststate | — |
| c | `c`, the control | — |
| ϱ, `crra` | `rho` | — |
| β, `types[].beta`, with the shares, `types[].share` | `beta` | one model and one solve per type; the adapter pools them with the shares |
| ℒ, `survival` | `L`, in the expectation as `beta*L` | R is not divided by L, so the assets of the dead vanish, as in the stage file |
| R, `return` | `R`, in the transition as R/(G ψ′) | — |
| 𝒢, `income.growth` | `G` | — |
| ψ, `income.permanent_shock`, with its spread σ_ψ, or μ_ψ, s_ψ, ψ_min and ψ_max for a truncated law | the exogenous `psi`, as the first column of the nodes | the adapter's nodes: equiprobable bins of the member's law, each node its bin's conditional mean |
| θ, `income.employed_shock`, with σ_θ, or μ_θ, s_θ, θ_min and θ_max | the exogenous `xi`, as the second column | the adapter's nodes, scaled by (1 − ℘ξ_u)/(1 − ℘) |
| ℘, `income.unemployment.prob`, and ξ_u, `income.unemployment.income` | one more value of `xi`, ξ_u, at each node of ψ, with weight ℘ times ψ's | the joint nodes are the product of ψ's and ξ's, as HARK's adapter builds them |
| `a_Art`, `borrowing_constraint`, and `a_Nat` | `a_min`, in the bound `c <= m - a_min` | `a_Art` for an artificial member; the natural limit for a natural one, which at 0 coincides with the bound c ≤ m |
| the newborn, and deaths at 1 − ℒ | none | the adapter builds the population itself |
| V | none | welfare reported as not computed |

## Departures, and what the adapter does about them

1. **The laws.** dolo's model file cannot state a truncated lognormal, and its equiprobable nodes are bin medians. The
   adapter passes the member's nodes, so that dolo and HARK solve the same effective member.
2. **The rule.** `egm` returns a cubic spline on the model's uniform grid, not its endogenous points. The spline rounds
   the kink and ripples just below it: read as the spline, the restrained member's mass at the constraint came out
   0.166 against HARK's 0.231 at level 1, and the kink's slopes were wrong. So the adapter reads the rule as `egm`'s own
   iteration holds it: linear between the spline's node values, which are `egm`'s endogenous rule evaluated there,
   with the kink's point m_k = a_min + u′⁻¹(β ℒ R E[(𝒢ψ′)^(−ϱ) c(m′)^(−ϱ)]) added from the Euler equation at
   a = a_min. The MPC is the slope of the segment. Between nodes 0.005 apart, a sharply bending rule's MPC differs from
   HARK's by up to 0.012 at level 3, for ℘ = 0.00005.
3. **The printing.** `egm` prints three numbers for every node at every iteration, a leftover at `egm.py` line 110 of
   the release. The adapter silences standard output around the call.
4. **The population.** `ergodic_distribution` puts mass on the model's uniform grid with no deaths or newborns, and
   builds a dense N × N matrix. The adapter uses the population code it shares with HARK's adapter: the same lottery on
   the same a-grid, with the family's newborns. A difference in the population is then the rule's, not the
   distribution's.
5. **The value.** `egm` gives no value function, and the adapter reports welfare as not computed. Policy evaluation
   by the adapter would supply it, and is not written.
6. **Convergence.** `egm` returns `a_converged` and `err`, the largest change in the rule and the state between its last
   two iterations. The adapter records both.

## The method, the adapter and the evidence

- **The method.** The endogenous grid method, `dolo.algos.egm.egm`, iterated to convergence (`η_tol`, `maxit`), with
  these settings:
  - the savings grid `a_grid`;
  - the uniform grid of m (`domain`, `options.grid`);
  - the nodes.

  In the tags of the [method targets](../schemas/bst/model.md#method-targets), the solve is `!time-iteration` on
  `policy.euler.solve`, with `egm` as its handler. `policy` is `!Linear`, read by the adapter through the spline's
  node values with the kink's point. The expectation on `E_ψ_θ_j` is a `!quadrature` over the member's nodes, which
  `egm` takes as `dp`.
- **The adapter** is [`../adapters/dolo/adapter.py`](../harness/adapters/dolo/adapter.py), with HARK's adapter's command line.
  Its legs:
  - *encode*, from a member and the settings to the recast model file, the nodes and the grids;
  - the call, `egm`, with standard output silenced; it stops with an error if `egm` does not converge;
  - *decode*, from the rule to the results file. The population, the effective member, the conditions and the
    statuses come from the code the adapters share, [`../adapters/common.py`](../harness/adapters/common.py).
- **The evidence: the probe of 2026-11-01**, in the pinned environment. The recast model was solved for `bst-restrained`
  and `bst-p-zero-0.005` on the schemas' nodes, and compared with HARK's adapter at the restrained-limit experiment's
  common points. HARK's results files are in `schemas/records/findings/2026-11-01_restrained-limit-suite-hark/`.
  - Both converged to an error of 10⁻¹⁰.
  - Below its kink the restrained rule is c = m, to 10⁻¹⁶.
  - With HARK's level-1 nodes, 7 per shock, and 1200 savings points, the rules agree with HARK's level 1 to within
    5.2 · 10⁻⁵ (restrained) and 6.0 · 10⁻⁵ (℘ = 0.005), for m up to 20.
  - With 31 nodes per shock they agree with HARK's level 3 to within 5.2 · 10⁻⁵ and 5.9 · 10⁻⁵.
  - With only 300 savings points, the gap to HARK grows with m, to 10⁻³ at m = 10. That is the coarser grid's error.
  - The node count changes both toolkits' rules alike, by about 10⁻² at m = 10.
- **The evidence: the restrained-limit experiment, 2026-11-01**, with the adapter at levels 1 to 3
  (`schemas/records/findings/2026-11-01_restrained-limit-suite-dolo/`). All twelve results files validate and are consistent
  with their members (`check.py --verify-results`), and so do `toy`'s and `library`'s at level 1, in the adapter's
  tests. Against HARK's adapter, on the same nodes and savings grids:
  - the rules' largest difference for m up to 20 falls with the level, from about 1.5 · 10⁻⁴ at level 1 to
    1.1–2.4 · 10⁻⁵ at level 3; over all the common points, up to m = 50, it is 3.9 · 10⁻⁵ at level 3;
  - the restrained kink at level 3: m = 0.974402 against HARK's 0.974405, slopes 1 and 0.4206 against 1 and 0.4185;
  - the stationary populations: the mean MPCs equal to five digits, the restrained member's mass at the constraint
    0.21273 against 0.21274;
  - each natural rule's gap to the restrained one falls by 2.254 and 2.286 per decade of ℘ in both toolkits.

  That is agreement between two toolkits on the same effective member, not a proof that either is right.

## Sources

- dolo's source at `v0.4.9.20` (`d782336b`):
  - `src/dolo/algos/egm.py`, `ergodic.py`, `time_iteration.py`, `improved_time_iteration.py`, `value_iteration.py`,
    `results.py`;
  - `src/dolo/numeric/distribution.py`, `processes.py`, `decision_rule.py`;
  - `examples/models/consumption_savings_iid.yaml`, `tests/test_egm.py`.
- Master at `33f873ee` for its Python and numpy requirements.
- dolo's open issues #173, the lognormal's parametrization; #188, more general grids; and #206, value iteration.
