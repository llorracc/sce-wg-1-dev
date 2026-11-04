# The reference probe: the bench's continuous EGM on the restrained-limit members, 2026-11-04

A probe, run in the scratchpad on the morning of 2026-11-04 after the owner's ruling of 06:23:39
([the ruling](../../rulings/2026-11-04_reference-solution.md)) and recorded here without its logs. It is step 2 of the
order of work in [`reference-solution.md`](../../../reference-solution.md): the first measurement of what the continuous
solution method reaches on the four members of the restrained-limit experiment, in the bench's own code, before any
reference file exists. Nothing here is a reference of record, and nothing is committed to the harness.

## What was run

**The solver,** `reference_probe.py`: the endogenous grid method with the expectation over the income shocks taken
against the stated continuous laws, not over atoms. Gauss-Legendre in the log of each truncated lognormal law, n nodes
a piece: the permanent law in one piece; the transitory law split at the preimage of next period's kink where the
rule has one, in one piece otherwise; the zero-income event exact. One evaluation of next period's rule and its slope
gives both E[(𝒢ψ)^(−ϱ) u′(c(m′))] and its derivative in assets, so each endogenous point carries the exact MPC, and the
rule is a cubic Hermite through the points and the slopes: below an artificial kink c = m − a_lo, at a natural limit
the segment from (a_lo, 0) with the closed-form MPC 1 − ℘^(1/ϱ) Þ̊_R, above the last point linear with the last slope.
The loop starts from the committed level-3 rule of HARK and stops when the last step times λ/(1 − λ), λ the
contraction factor measured from successive steps, is below 10⁻¹¹ at 3,000 check points and the request points. It
is the kink-split method of HARK's Kink-Split page and of HAFiscal's continuous solver, in independent code, from the
bench's own quadrature (`harness/adapters/common.py`, `law_quadrature`).

The command, for each member and setting:

```
uv run --with numpy --with scipy --with jsonschema --with pyyaml --with referencing python reference_probe.py \
    schemas/bst/<scenario>/members/<member>.yaml --out runs/<member>/<setting> <setting's options> --tol 1e-11
```

The settings, each a refinement of a base so that the movement from the base measures the base's error on what changed:

| setting | the grid and the nodes | its base |
|---|---|---|
| A | 1,000 points nested 3 times from 10⁻⁶ above the constraint to 200; 32 nodes a piece | |
| B | 2,000 points to 400; 32 nodes | A |
| C | B at 64 nodes a piece | B |
| D | 4,000 points to 1,000 at 64 nodes | C |
| E | B with 3,000 extra points, geometric from 10⁻⁷ to 2 above the limit (the natural members) | B |
| F | E at 64 nodes a piece | E |
| G | E with 6,000 extra points instead of 3,000 | E |

A natural member's grid also holds three points at 10⁻⁹, 10⁻⁸ and 10⁻⁷ above the limit; the restrained member's
holds the constraint itself, whose endogenous point is the kink.

**The diagnostics** are the bench's: the Euler residual under the stated laws at the request points by the
diagnostics' expectation at 32 and at 64 nodes a piece (`common.euler_residuals`), the second against the first giving
the diagnostic's own precision; the closed forms; the distance from the committed level-3 rules of HARK and dolo
([the HARK suite](../2026-11-01_restrained-limit-suite-hark/README.md),
[the dolo suite](../2026-11-01_restrained-limit-suite-dolo/README.md)) at the request points, on the relative scale.

**HARK at its default settings,** `default_hark.py`, in the harness's locked HARK environment: HARK 0.17.2, the
member's horizon, constraint and laws, the adapter's equiprobable nodes of the member's laws at HARK's count of 7 a
shock, HARK's own grid of 48 points nested 3 times from 0.001 to 20, linear interpolation, no value function, the
solver's tolerance of 10⁻⁶; the same diagnostics.

**The distribution,** `reference_dist.py`, on a rule from the study: pass 1 on the bench's geometric grid of 4,000
points to 60 gives the 99.9th percentile of end-of-period assets; pass 2 is uniform in assets from the constraint to
that percentile in 32,000 points, then geometric to 300 in 400 points; the transition is the bench's lottery over
equiprobable nodes of the laws at 31 and at 63 nodes a shock, the stationary distribution by power iteration to
10⁻¹⁴, the statistics by the bench's functions. The committed level-3 population blocks give the distance.

`summarize.py` writes [`report.md`](report.md), every table below in full, from the result files.

## What it showed

**The closed forms.** On the three natural members the rule's secants from 10⁻⁹ to 10⁻⁵ above the limit differ
from 1 − ℘^(1/ϱ) Þ̊_R by at most 4 · 10⁻¹², and the EGM slopes at the first three endogenous points, computed from the
expectation's derivative and not from the anchor, equal it to twelve digits. On the restrained member c = m below the
kink exactly, and the kink's position, 0.974084142668 at setting B, moves by less than 10⁻¹² between A and B; it
agrees with the HAFiscal session's probe of the same morning to 2 · 10⁻¹¹, two independent codes on one method, that
session's number being its own until it is a run of record. The committed level-3 rules put the kink 3.2 · 10⁻⁴
higher, and HARK at its default settings 2.0 · 10⁻³ higher.

**The convergence study.** Every run converged in 270 to 350 iterations with the bound on the distance to the fixed
point below 10⁻¹¹. The movements at the request points, relative, and the residuals (the table in `report.md` has
every setting):

| member | A to B (points doubled) | B to C (nodes doubled) | C to D (points and top doubled) | B to E (points near the limit) | E to G (those points doubled) | E to F (nodes doubled) | residual at the finest, 32-node diagnostic | the diagnostic's precision |
|---|---|---|---|---|---|---|---|---|
| ℘ = 0.005 | 8.5 · 10⁻⁹ | 4.7 · 10⁻¹³ | 6.0 · 10⁻¹¹ | 4.0 · 10⁻¹¹ | 3.2 · 10⁻¹³ | 8.2 · 10⁻¹⁴ | 1.5 · 10⁻¹² | 7 · 10⁻¹⁵ |
| ℘ = 0.0005 | 1.4 · 10⁻⁸ | 7.3 · 10⁻¹⁴ | 1.1 · 10⁻⁹ | 1.1 · 10⁻⁹ | 1.3 · 10⁻¹² | 7.3 · 10⁻¹⁴ | 1.4 · 10⁻¹² | 7 · 10⁻¹⁵ |
| ℘ = 0.00005 | 5.1 · 10⁻⁷ | 8.7 · 10⁻¹¹ | 3.4 · 10⁻⁸ | 3.4 · 10⁻⁸ | 8.3 · 10⁻¹³ | 8.1 · 10⁻¹¹ | 1.4 · 10⁻¹² | 3.5 · 10⁻¹⁰ |
| restrained | 8.4 · 10⁻⁹ | 1.9 · 10⁻¹⁰ | 5.9 · 10⁻¹¹ | | | | 2.1 · 10⁻¹⁰ (32); 9.6 · 10⁻¹⁴ (64) | 2.1 · 10⁻¹⁰ |

Three facts in it:
- The nodes do not limit the natural members at ℘ = 0.005 and 0.0005: doubling them moves the rule by 10⁻¹³. The
  points near the limit do: the smaller ℘, the sharper the rule bends just above the limit, and the nested grid alone
  does not resolve the bend, since doubling it to 4,000 points leaves ℘ = 0.00005 at a residual of 3.7 · 10⁻⁷, while
  3,000 extra points there take that residual from 5 · 10⁻⁶ to 2.5 · 10⁻¹¹ and 6,000 move the rule by less than
  10⁻¹² more. On ℘ = 0.00005 the quadrature then shows: doubling the nodes a piece moves the rule by 8 · 10⁻¹¹, at
  m = 0.985, and the diagnostic at 64 nodes a piece differs from the one at 32 by 3.5 · 10⁻¹⁰, so there the nodes,
  not the points, are the last error, at a tenth of what the diagnostic's own precision says.
- The restrained member is limited by the quadrature at the kink split, not by the points: doubling the nodes moves it
  by 1.9 · 10⁻¹⁰ and doubling the points by 5.9 · 10⁻¹¹, and the diagnostic's own precision is the same 2 · 10⁻¹⁰,
  since a split Gauss-Legendre rule on a rule with a kink and knots converges algebraically there, which is why
  HAFiscal's production method takes that integral in closed form on Hermite pieces. At 64 nodes a piece the
  64-node diagnostic finds a residual of 10⁻¹³.
- The reference's error on the rule, as these runs bound it: about 10⁻¹² for ℘ = 0.005 and 0.0005, 10⁻¹⁰ for
  ℘ = 0.00005 from the quadrature, and 2 · 10⁻¹⁰ for the restrained member; the Euler residuals under the stated
  laws at the finest settings are 1.4 · 10⁻¹² to 2 · 10⁻¹⁰.

**The committed level-3 rules against the reference.** HARK's and dolo's level-3 rules, which agree with each other to
1.1 · 10⁻⁵ to 2.4 · 10⁻⁵ ([the record of 2026-11-03](../2026-11-03_two-questions-on-the-committed-runs/README.md)),
both sit 7.8 · 10⁻⁴ to 8.4 · 10⁻⁴ from the continuous solution, relative, at m = 10, on every member: the
representation's error, 31 equiprobable nodes a shock in place of the laws, which no comparison between the two
toolkits could see.

**HARK at its default settings against the reference.** At the request points up to m = 20, 5.4 · 10⁻³ (℘ = 0.005,
at m = 10), 6.5 · 10⁻³ (℘ = 0.0005, at m = 0.3), 1.1 · 10⁻² (℘ = 0.00005, at m = 0.6) and 5.5 · 10⁻³ (restrained,
at m = 10); at m = 50, beyond the default grid's top of 20, 2.3 · 10⁻² on every member. Its Euler residual under the
stated laws is 2 · 10⁻² to 4 · 10⁻² on the natural members, at m between 0.05 and 0.9, and 2 · 10⁻³ on the restrained
member; its loop stops after about 90 cycles at a last step below 10⁻⁶.

**The ergodic distribution.** With the reference rule, refining the grid from 4,000 geometric points to 32,000 uniform
points up to the 99.9th percentile moves the mean of assets by 1 · 10⁻⁶ to 3 · 10⁻⁶ and the quantiles by 10⁻⁵ to
10⁻⁴, relative; the mass beyond the dense part is 9.1 · 10⁻⁴ to 9.3 · 10⁻⁴, as the percentile implies, and the mass
on the last node, at 300, is below 10⁻¹⁵. Doubling the transition's nodes from 31 to 63 a shock moves the restrained
member's mean of assets by 1.4 · 10⁻³, its median by 1.1 · 10⁻², its 99.9th percentile by 1.4 · 10⁻² and the mass at
the constraint by 1.6 · 10⁻³ absolute: a fifth of its households sit at the constraint, and their next period's cash
is the transitory law itself, which 31 atoms place at 31 points. On ℘ = 0.005 the same doubling moves the mean by
3.8 · 10⁻⁴ and the 99.9th percentile by 5.3 · 10⁻³. So on the dense grid the transition's representation of the laws,
not the grid, bounds the distribution's precision, at 10⁻³ to 10⁻² with the nodes the ladder uses; the continuous
landing that decision R6 proposes is a requirement for a reference distribution, not a refinement. The committed
level-3 distributions, from the level-3 rules on the level-3 grids with 31 nodes, sit 2.7 · 10⁻³ to 8.7 · 10⁻³ below
the dense 31-node distributions on the mean of assets and 2.8 · 10⁻³ to 1.3 · 10⁻² on the median: the rule's error,
amplified, with the grid's and the nodes' on top.

## What it establishes, and what it does not

It establishes that the continuous method, in the bench's code, solves all four members to a rule whose error is
between 10⁻¹² and a few 10⁻¹⁰ relative at the request points, with the closed forms at the limits carried to round-off, and that
where the method's error sits is known: the points near a natural limit for small ℘, the quadrature at the split for
an artificial kink. It establishes the size of what the reference is for: the committed ladder's finest level is
8 · 10⁻⁴ from the solution of the stated member while its two toolkits agree to 10⁻⁵, and HARK at its default
settings is 5 · 10⁻³ to 10⁻² within its grid and 2 · 10⁻² beyond it. And it establishes that a dense distribution
grid exposes the transition's node error, 10⁻³ to 10⁻² on the restrained member, so that the reference's
distribution needs the laws integrated in the transition as well as in the solve.

It does not establish any error of the distribution beyond the nodes' effect, since no continuous landing
exists yet; nor anything about dolo at its default settings, which the stone has to define; nor the value function,
which the probe does not compute. HARK's continuous solver was not run here; both HARK sessions ran it on these
members the same morning, and their numbers are theirs until something public reports them. The HAFiscal session's
probe of the restrained member is its own until it is a run of record. Nothing here is a reference file in the
results schema; the probe writes its own result files.

## Pending

- The continuous landing for the transition (decision R6), and the distribution's convergence study on it.
- HARK's continuous solver from an archive of the HARK session's local commit, against these rules; HAFiscal's
  solver on the restrained member as a run of record, on the owner's word in that session.
- The level `default` in both adapters, and dolo's default settings in its stone.
- The reference files in the results schema, certified, once the owner rules on R1 to R7.

## Files

- `reference_probe.py`, `reference_dist.py`, `default_hark.py`, `summarize.py`, `run_study.sh`: the scripts, as run.
- `runs/<member>/<setting>/result.json` and `rule.npz`: each solve's settings, convergence, diagnostics, the rule
  at the request points, the closed forms, the level-3 distances, and the endogenous points with their slopes.
- `dist/<member>/B-n<nodes>/result.json`: each distribution's two passes, the statistics blocks and the level-3
  block; the stationary distribution itself is not kept, being reproducible from the rule and the settings.
- `default/hark/<member>/result.json`: HARK at its default settings.
- `report.md`: the tables, generated.
