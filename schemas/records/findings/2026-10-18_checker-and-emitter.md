# The checker's first verdicts, and the emitter's first file

**The checker on the members** (`schemas/checker/check.py`, 2026-10-18):
- The toy (seven types, truncated laws at ±3, survival 1 − 1/160, unemployment income 0.7): every type valid; the most
  patient type at 0.9979 of its GIC-Mod bound; its upper-tail exponent 3.56,
  so its variance is finite; the artificial constraint binds for every type, so welfare and marginal welfare are defined.
- The community library's member (one type, untruncated laws, ℒ = 1, zero income with probability 0.005): valid; no kink; the
  tail exponents 5.07 under the population measure and 7.07 under the income measure; welfare defined with the condition's
  number 0.073; marginal welfare `undefined`, the GIC making the mean marginal utility infinite (factor 1.073).
- The untruncated toy: no kink, since a lognormal law puts the natural constraint at zero; every welfare moment finite.

**The emitter's first results files** (the HAFiscal-Latest session, from `bst_bench`, HARK 0.17.2, the same day): the toy's
validates against `results.schema.json` and agrees with the benchmark's earlier reference to about 10⁻³, the differences
being the truncated laws and the newborn rule; by 17:47 the library member's and the untruncated toy's validate too, the
library's reporting welfare defined and marginal welfare `undefined` as the checker says. Its measurement: with equiprobable nodes per shock at 7, 15, 31 and 63, the Euler
residual at the kink falls as 9.8·10⁻³, 3.9·10⁻³, 1.4·10⁻³, 5.3·10⁻⁴, about n^{−1.4}, and HARK's solve time is linear in the
joint nodes, so a relative error of 10⁻⁴ near the kink would need about two hundred nodes per shock. The precision levels
are therefore settings, and tolerances come from measured convergence, as `results.md` says of the comparison; the wording
of the levels as error targets is open with the owner.
