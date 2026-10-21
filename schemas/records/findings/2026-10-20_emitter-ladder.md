# The emitter's ladder of 2026-10-20

**What ran.** The HAFiscal-Latest session ran it, on the owner's word there at 20:43:29.
- **The emitter.** Its benchmark's emitter of `bst/1` results files, version 0.3, from the first level, one step at a
  time.
- **The environment.** Python 3.12.3, numpy 2.5.4 and scipy 1.17.1, with HARK at a tagged commit of the llorracc fork,
  version string 0.17.2. Eight threads, a memory limit of 20 GB, and the fork's schemas at `4f99d01`.
- **What changed from 0.2.** Version 0.3 changes only a results file's provenance. It reads the toolkit's commit from the
  installed package, where 0.2 wrote a constant that a repin had made wrong. It reports the thread count the linear
  algebra actually uses.

| member | level | wall time | verified |
|---|---|---|---|
| toy, seven types | first | 29.6 s | yes |
| library, one type | first | 7.4 s | yes |
| toy-untruncated, seven types | first | 29.5 s | yes |
| toy | second | 185.7 s | yes |
| library | second | 41.9 s | yes |
| toy-untruncated | second | 183.3 s | yes |
| toy | third | 2,955.6 s | yes |
| toy | fourth, with the population block | stopped after 6 h 42 m | no file |

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
- The rerun takes about seven hours, and follows a kernel comparison that has had the machine since 04:38:45.
- It reads its own read-only copy of the schemas at `4f99d01`.

**What it establishes.**
- The seven files, the three members' first two levels and the toy's third, validate and verify against both checkers. The shock-law pull
  request's filled form leaves the members' hashes unchanged.
- A change of Python and numpy versions leaves every reported quantity at round-off, except Q(1).

**What it does not:** the fourth level's file, with the population block, which waits for the rerun.
