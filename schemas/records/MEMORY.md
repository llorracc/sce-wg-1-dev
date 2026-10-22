# The schema project's memory

Read this first when working on `schemas/`. One line per record; the records hold the content. This repository is public,
so every record here is written for publication: the owner's decisions are recorded in substance and by date, not in his
words, and nothing from private repositories appears beyond a pointer.

Standing rules and state:
- [Project state](memory/project_state.md) — what exists in `schemas/`, the eleven pull requests, all merged; HARK's adapter; what is settled, what is open, as of the second memorial of 2026-10-22.
- [Notation and foundation](memory/feedback_notation-and-foundation.md) — BST's notation with econ-ark's registry as the authority beside it; two spellings of each symbol; the symbols in force (Þ̊, β̊, ϱ, ε, ξ_u, ξ_x, j); the Bellman-SYM stage file is the foundation.
- [Method attachment](memory/feedback_method-attachment.md) — an expectation's method on its operator, the solution on `policy.euler.solve`, the interpolation on `policy`; tags as methods, routines as handlers; `bst/1` free of any method's lines (#11).
- [Not yet: w3id.org/sce](memory/feedback_w3id-not-yet.md) — never raise registering the namespace before a pull request from this fork is merged into econ-ark/sce-wg-1; even then, much too early.
- [Iterate and propose](memory/feedback_iterate-and-propose.md) — a schema changes only after the proposed change and its downstream consequences have been put to the owner.
- [One written form](memory/feedback_one-written-form.md) — a model has one spelling in a parameter file, because the hash is its identity.
- [Matsya's answers are weighed](memory/feedback_matsya-answers-are-weighed.md) — judged against this project's needs and pushed back on where they do not fit.
- [Matsya's work goes to Matsya](memory/feedback_route-matsya-work-to-matsya.md) — through the bellman session; what Matsya cannot do is said first and asked about.
- [Consult the toolkits](memory/feedback_consult-the-toolkits.md) — what a results file carries, or a toolkit must compute, goes to the HARK and HAFiscal sessions for their views before a change is drafted.
- [No timings](memory/feedback_no-timings.md) — public material carries no run times or speed figures of a toolkit.
- [Checkable sources](memory/feedback_checkable-sources.md) — public documents cite what a reader can check; who read what stays in the records; Bellman's unpublished rules are stated as the schemas' own.
- [References](memory/reference_pointers.md) — pull requests, sessions, other repositories' records that this work points to.

Rulings, journal, findings:
- [Rulings of 2026-10-17](rulings/2026-10-17_schema-decisions.md) — the handoff day: the word "schema", the shock laws, the truncated lognormal default, the guard hook.
- [Rulings of 2026-10-18](rulings/2026-10-18_schema-decisions.md) — the family's name, the toy's laws, notation, the stage-file foundation, the newborn, the bounds, welfare, ρ > 1, the restructuring; in the evening, the three-valued switch, the levels as settings, the optional keys.
- [Rulings of 2026-10-19](rulings/2026-10-19_schema-decisions.md) — the population block of the results file; no Matsya consultation on the Bellman defect; the truncated lognormal for Bellman-SYM, with its defaults; the five corrections; in the afternoon, an omitted bound as three standard deviations, existing syntax adopted where it can be, and an ontology of probability distributions through Matsya.
- [Rulings of 2026-10-20](rulings/2026-10-20_schema-decisions.md) — the ontology's decisions, with Bellman's truncated lognormal aligned with its truncated normal; the four draft pull requests; the emitter program resumed; Q(1) dropped after the toolkits' sessions were consulted; the coverage check.
- [Rulings of 2026-10-21](rulings/2026-10-21_schema-decisions.md) — nothing above 0.999 in the quantile maps; the coverage points each toolkit's; the Rosetta Stones and their home; no run time in results files; checkable sources; the BST paper the authority on notation, with two spellings; in the evening, the targets as the registry has them, 𝒢_t, ξ_U in place of μ, #6 onto #7 by a merge, `\IncUnemp` fixed in econ-ark-tools; the notation batch, the adapters, and the fork's seven pull requests merged.
- [Rulings of 2026-10-22](rulings/2026-10-22_schema-decisions.md) — the registry's rulings that reach the schemas (Þ̊, ϱ, ε, ξ_u, ξ_x, j); #8 out of draft and merged; #9 with v5, v6 and the design note, merged; the rulings PR approved; in the afternoon, `bst/1` free of any method's lines, #10 and #11 merged.
- [Journal of 2026-10-18](journal/2026-10-18_session-record.md) — the day's events in order, with their stamps.
- [Journal of 2026-10-19](journal/2026-10-19_session-record.md) — the population block applied; the bellman session's reading of the Bellman defect; the constraint in force corrected; levels bold; the truncated lognormal scoped and its pull request planned; after the memorial, the survey of existing syntax, the gathering of material and Matsya's four ontology sessions.
- [Journal of 2026-10-20](journal/2026-10-20_session-record.md) — the ontology and the shock laws on it as draft pull requests; the converter checked at Bellman's draft; the emitter's ladder; Q(1) and the coverage check; through the ladder's end and its rerun early on 2026-10-21.
- [Journal of 2026-10-21](journal/2026-10-21_session-record.md) — the records reviewed, the coverage check's final commit, the memorial; then the Rosetta Stones, draft pull requests #5 and #6, Matsya's sessions, the toy's fourth level, the notation; in the evening, econ-ark's registry in force, draft #7, and #6 rebuilt on it.
- [Journal of 2026-10-22](journal/2026-10-22_session-record.md) — registry v5, v6 and v8 into the schemas; #8 and #9 merged; the rulings of 13:59 and 14:00; the first memorial; the bellman session's update, Matsya's third session, the method targets fixed; #10 and #11 merged; the second memorial.
- [The lower tail of the stationary distribution](findings/2026-10-18_lower-tail-and-welfare.md) — when population welfare and marginal welfare are finite; verified against an EGM solution.
- [The checker's first verdicts](findings/2026-10-18_checker-and-emitter.md) — the toy's and the library member's condition margins; the emitter's first results file and its convergence measurement.
- [The Matsya completeness job](findings/2026-10-18_matsya-completeness-job.md) — one job on the pushed bst/1 documents: a flipped unemployment law in the round trip, one borrowing limit for two, the rest in agreement.
- [The Markov family's constraint in force](findings/2026-10-19_markov-constraint-in-force.md) — a fixed point with the artificial limit inside, as HARK computes it; the maximum understates it at low benefits.
- [Matsya on an ontology of probability distributions](findings/2026-10-19_distribution-ontology-matsya.md) — ProbOnto as a copied vocabulary layer; three operators (pushforward, conditioning, kernel product); the schemas' laws placed in that algebra; weighed.
- [The ontology's tests and the converter at Bellman's draft](findings/2026-10-20_ontology-and-converter-checks.md) — twelve tests and every deliberate break caught; the members' hashes unchanged; the converter's eleven calls elaborate with mean one at Bellman's draft; the uniform not yet integrated by Bellman's comparator.
- [The emitter's ladder of 2026-10-20](findings/2026-10-20_emitter-ladder.md) — eight results files verified by both checkers, the toy's fourth level from its rerun; round-off agreement with version 0.2 except Q(1); each level's changes about three times smaller.
- [The Rosetta Stones' first findings](findings/2026-10-21_rosetta-stones.md) — the household recast exactly in the lecture's form; HARK's limiting MPCs, targets and tolerance above the grid; Matsya's three sessions weighed; the community library's HARK solution and a local QuantEcon module that agrees with HARK.
- [The quantile at probability 1](findings/2026-10-20_the-quantile-at-one.md) — infinite in the model, a Pareto tail; a computed Q(1) tracks the grid's top and turns on the reading rule's round-off; both toolkits' answers.
- [How far a representation reaches](findings/2026-10-20_coverage-of-the-representation.md) — the top node's mass at the first two levels; an upper bound on the per-period flow beyond the top; what a clipped representation misses of the mean.
- [Econ-ark's notation sources](findings/2026-10-21_notation-sources.md) — the registry, the shortcuts and NARK; where the schemas agree with registry 1.0.0, what #7 fixed, what is undecided; the census of free letters; `\IncUnemp`.
- [HARK's Markov consumer for bst/1](findings/2026-10-21_hark-markov-for-bst1.md) — the nonpersistent chain's mapping; HARK silently replacing a passed matrix; the per-state interpolation gap and #1858's fix; the gate for HARK's adapter.
- [Where a method attaches, and Matsya on HARK's source](findings/2026-10-22_method-attachment.md) — what Bellman's check admits on the stage files; ϱ in Bellman; Matsya's third session on HARK's standard consumer, agreeing with the revised stone.
- [Deferred follow-ups](deferred.md) — what was put off, and what brings each item back.
- [Defects](defects.md) — faults found and their status.

Plans keep their status lines in place: [`foundation.md`](../foundation.md), [`effective-member.md`](../effective-member.md),
[`hafiscal-models-and-test-suite.md`](../hafiscal-models-and-test-suite.md) and [`existing-syntax.md`](../existing-syntax.md). The plan for the Bellman pull request on the
truncated lognormal is kept outside this repository, since it names the private repository's files. The glossary is the [README](../README.md)'s
vocabulary section.
