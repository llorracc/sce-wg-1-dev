# The emitter's ladder of 2026-10-20

**What ran.** The HAFiscal-Latest session ran it, on the owner's word there at 20:43:29.
- **The emitter.** Its benchmark's emitter of `bst/1` results files, version 0.3, from the first level, one step at a
  time.
- **The environment.** Python 3.12.3, numpy 2.5.4 and scipy 1.17.1, with HARK at a tagged commit of the llorracc fork,
  version string 0.17.2. Eight threads, a memory limit of 20 GB, and the fork's schemas at `4f99d01`.
- **What changed from 0.2.** Version 0.3 changes only a results file's provenance. It reads the toolkit's commit from the
  installed package, where 0.2 wrote a constant that a repin had made wrong. It reports the thread count the linear
  algebra actually uses.

| member | level | verified |
|---|---|---|
| toy, seven types | first | yes |
| library, one type | first | yes |
| toy-untruncated, seven types | first | yes |
| toy | second | yes |
| library | second | yes |
| toy-untruncated | second | yes |
| toy | third | yes |
| toy | fourth, with the population block | yes, from the rerun of 2026-10-21; the first attempt stopped for lack of memory |

**What "verified" means.** The ladder ran `check.py --verify-results` at `4f99d01` after each file. It found each file
valid, and its report consistent with the member: `2fe95c8cf8e5…` for the toy, `fee9fcced828…` for the library member,
`32a326c4bfd5…` for the untruncated toy. The checker of the shock-law pull request on the ontology (#2, `0583a60`) verified
the same seven files with the same hashes: the six of the first two levels by 21:06, and all seven at 04:32 on 2026-10-21.

**Against version 0.2's files.** That session compared them, and every quantity agrees at round-off.
- Outside the Euler residuals, which are themselves round-off, the largest relative difference is 5.6·10⁻¹², on a
  generalized Lorenz ordinate of 4.6·10⁻⁷. Everything else agrees to 3.4·10⁻¹³.
- At the toy's third level the figures are 1.0·10⁻¹¹ on that ordinate and 1.5·10⁻¹² elsewhere.
- The one exception, Q(1), has its own record.

**The fourth level** solved all seven types. Its log's last line is the most patient type's: target 3.1352, mean a
2.36394, stationarity residual 1.4·10⁻¹².
- At 04:31:53 the kernel's out-of-memory killer stopped it, inside the run's own memory limit and at about 20 GB resident,
  before the pooled stage wrote anything. The machine has 60 GB.
- The cause, from that session: each type kept two populations, under the population measure and the income measure, of
  about 31.7 million arrivals each. Each population held six arrays, about 2.9 GB a type with u′, so the seven types held
  about 20 GB when the pooled stage began.

**The rerun.** That session announced it at 04:45:36 on 2026-10-21.
- It uses the emitter's version 0.5, which keeps only m and the weights across types. It recomputes c, a, the MPC and u′
  from each type's rule when the pooled stage asks for them, the same function at the same points, so the numbers should
  agree bit for bit.
- Its estimated peak is about 23 GB, under a limit of 32 GB.
- Version 0.5 is first checked against version 0.3's files for exact equality outside the provenance and the toolkit.
- The rerun follows a kernel comparison that has had the machine since 04:38:45.
- It reads its own read-only copy of the schemas at `4f99d01`.

**The rerun's result,** reported by that session at 12:16 on 2026-10-21.
- The toy's fourth level, with the population block, validates, and `check.py --verify-results` finds its report
  consistent with the member `2fe95c8cf8e5…`. The checker of the shock-law pull request (#2, `0583a60`) finds the same, here.
- Its seven types' lines are identical to the first attempt's. The population's transition kept the third level's 31
  nodes a shock, and only the household's nodes doubled.
- Its farthest mass point in m is 549, below the solution grid's top of 800.

**Convergence across the ladder,** the toy's largest relative change over its seven types, from each level to the
next:

| from, to | kink | target | mean a | W |
|---|---|---|---|---|
| first to second | 9.4·10⁻³ | 6.8·10⁻² | 9.1·10⁻² | 4.8·10⁻³ |
| second to third | 3.6·10⁻³ | 2.4·10⁻² | 3.1·10⁻² | 1.5·10⁻³ |
| third to fourth | 1.4·10⁻³ | 8.5·10⁻³ | 8.9·10⁻³ | 5.6·10⁻⁴ |

- Each change is 2.6 to 3.5 times smaller than the one before; each level doubles the nodes and the grids.
- Dividing the last change by that ratio less one estimates what the fourth level still misses: about 9·10⁻⁴ in the
  kink, 5·10⁻³ in the target, 4·10⁻³ in mean a and 3·10⁻⁴ in W. That is an extrapolation from three changes, not a
  measurement.
- The most patient type, β = 0.99, moves most in the target and mean a.
- These are the first measured error estimates e for the Rosetta Stones' comparison rule, |A − B| ≤ k(e_A + e_B).

**What it establishes.**
- All eight files, the three members' first two levels and the toy's third and fourth, validate and verify against
  both checkers. The shock-law pull request's filled form leaves the members' hashes unchanged.
- The emitter's use of the population block at the fourth level, where its two node counts differ, verifies.
- A change of Python and numpy versions leaves every reported quantity at round-off, except Q(1).
- Each level's changes fall by a factor of about three.

**What it does not:** a measured error at the fourth level, which the extrapolation only estimates; and any comparison
with a second toolkit.

**Added on 2026-10-22.** The HAFiscal-Latest session reports the checker's verdict on the toy's levels 3 and 4, run against
the schemas and checker at `4f99d01`, the ones the ladder was written against: each validates, and its report is
consistent with the member. It re-ran them that day after taking the machine's name and operating system out of the files,
on the owner's word, and every number was unchanged. The files still carry the quantiles at probability 1 and the run
time, which the schema has since dropped (#3, #5); the emitter's next ladder will not.
