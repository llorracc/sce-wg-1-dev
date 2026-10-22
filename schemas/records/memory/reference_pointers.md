---
name: reference_pointers
description: "Pull requests, repositories and sessions that the schema work points to"
metadata:
  type: reference
---

- The fork's nine pull requests, all merged: https://github.com/llorracc/sce-wg-1-dev/pull/1 (the ontology, into `main`)
  and pulls 2 to 7 on 2026-10-21, 8 and 9 on 2026-10-22 (into the schemas' branch). The project state lists what each held.
- HARK's draft pull requests from the owner's fork that bear on the adapters: econ-ark/HARK#1858 (the Markov solver's
  expectations on the current state's points, and its value function; the HARK adapter's pin, commit `03a2c7a1` on
  llorracc/HARK's branch `markov-exact-expectations`), #1859 (the employment
  income process for the Markov consumer), #1860 (`NewbornPermShk`). Others' open ones: #1848 (cubic interpolation
  above the grid), #1853 (human wealth in the Markov solver).
- Econ-ark's notation registry, `@resources/notation/notation.yml` in econ-ark/econ-ark-tools, with the generated
  `econark-notation.sty`, `notation-math.yml` and `NOTATION.md`: version 1.0.0 on its master once econ-ark-tools' pull
  requests #38 to #44 merged on 2026-10-21, then 2.1.0 (#46), with rows for the schemas' own symbols, and 3.0.0 (#47)
  that evening; 5.0.0 (#49), 6.0.0 (#50) and 8.0.0 (#52) on 2026-10-22. Beside it, `econark-shortcuts.sty` in the same repository's `@resources`, the macros most papers load,
  and econ-ark/NARK, econ-ark's naming conventions.
- HARK's main branch at `4c285e86` (2026-10-07), the commit the HARK stone was read at.
- QuantEcon's lecture on the income fluctuation problem with stochastic returns, `lectures/ifp_advanced.md` of
  QuantEcon/lecture-python.myst at `96ede2993` (2026-08-12), the code the QuantEcon stone describes.
- Bellman-SYM's draft pull request for `TruncatedLogNormal(μ, σ, l, u)`, in Bellman's repository, which is private; the
  bellman session's, cited here by subject only.
- ProbOnto (Swat, Grenon, Wimalaratne, Bioinformatics 2016; CC BY 4.0): the knowledge base of distributions and
  parameterizations whose families, charts and conversions the ontology copies, with `skos` cross-references.
- HARK pull request econ-ark/HARK#1855 (draft): the survival probability in the risk-modified finite-value-of-autarky factor.
- HARK, local branches held by the HARK session, unpushed: the distribution-bounds fixes, and a `NewbornPermShk` flag so that
  a newborn's permanent income is its initial draw, bst/1's convention.
- The community library's buffer-stock model: QuantEcon community-library pull request 5, the `library` member of bst/1.
  Its HARK implementation now lives at `solutions/buffer-stock/001-hark-egm/` in QuantEcon/community-library, moved there
  by a later pull request of the library; it uses HARK alone.
- The lower-tail finding's record in the paper's working repository (private as of 2026-10-18): a note among its theory
  notes on power-law decay, committed on its port branch and on master with a numerical battery, unpushed that day.
- Bellman-SYM: the stage files here were elaborated and calibrated by the bellman session under Bellman at its repository
  head and under the Matsya service's installed version; the repository and its documentation site were not public on
  2026-10-18, so its pages are cited by title.
- Matsya: the design review of 2026-10-18 ran as four questions in one session and one stage-file question in another; the
  client is `bellman-matsya`. Its four questions-only sessions on the ontology of probability distributions ran from the
  bellman session on 2026-10-19; their answers are kept outside this repository, and the findings of that day hold what
  they say.
- The buffer-stock benchmark `bst_bench` lives in HAFiscal-Latest, destined for its own econ-ark repository; its emitter of
  results files in this schema's form is the HAFiscal-Latest session's.
