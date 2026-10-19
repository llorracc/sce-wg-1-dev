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
of the levels as error targets was settled the same evening: the levels are settings.

**The effective member, reported and verified** (the HAFiscal-Latest session's emitter, version 0.2, by 23:24 the same
day, within the hour of the schema's revision): the three members' first-level files carry the effective-member block and
the conditions block, with every status from the toolkit's own verdicts, and the checker's verification finds each
consistent with its member. What moved, as the design note predicted: the untruncated toy has a kink in the effective
member, its natural limit about −5.6 from the lowest node of the permanent shock, behind the zero artificial constraint,
where the stated member has none; the toy keeps its regime, its effective natural limit about −5.5 against the stated
−1.7, both behind the binding zero constraint, with a worst-income mass of about 0.02 where the stated member has none;
the library member keeps its regime, the zero-income atom being in the representation, and its welfare factors agree
with the checker's to the digit. At seven nodes the expectations sit in the fourth digit from the closed forms, so no
verdict crosses a bound for these members. The two residuals separate the errors as intended: at the first level the
residual against the stated law near the kink is about 10⁻², while the diagnostic's own precision is 10⁻⁶ to 4·10⁻⁵ and
the residual under the solver's own nodes 10⁻⁷ to 10⁻⁵, so the 10⁻² is the discretization's distance from the law, not
the solver's or the diagnostic's error. One question came out of it, for the owner: the emitter's fourth level solves the
household on more nodes than it runs the population's forward transition on, and the conditions on the stationary
population's existence are then decided on a law the population does not use. The toy's second level, at fifteen nodes,
verifies clean as well (23:23), with the request file unchanged and the rule unchanged to the last digit; the one reported
quantity that moved with the effective member is the buffer stock target, now found with the effective E[1/ψ], by about
four parts in a thousand for the toy's most patient type and by much less for the impatient ones.
