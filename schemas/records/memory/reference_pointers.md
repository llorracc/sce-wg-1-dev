---
name: reference_pointers
description: "Pull requests, repositories and sessions that the schema work points to"
metadata:
  type: reference
---

- The fork's draft pull requests of 2026-10-20 (see the project state for their branches, heads and order):
  - the ontology of probability distributions, https://github.com/llorracc/sce-wg-1-dev/pull/1, into `main`;
  - the shock laws on the ontology, https://github.com/llorracc/sce-wg-1-dev/pull/2, into the schemas' branch;
  - the quantile maps without Q(1), https://github.com/llorracc/sce-wg-1-dev/pull/3, into the schemas' branch;
  - the coverage of the representation, https://github.com/llorracc/sce-wg-1-dev/pull/4, into the schemas' branch.
- Bellman-SYM's draft pull request for `TruncatedLogNormal(μ, σ, l, u)`, in Bellman's repository, which is private; the
  bellman session's, cited here by subject only.
- ProbOnto (Swat, Grenon, Wimalaratne, Bioinformatics 2016; CC BY 4.0): the knowledge base of distributions and
  parameterizations whose families, charts and conversions the ontology copies, with `skos` cross-references.
- HARK pull request econ-ark/HARK#1855 (draft): the survival probability in the risk-modified finite-value-of-autarky factor.
- HARK, local branches held by the HARK session, unpushed: the distribution-bounds fixes, and a `NewbornPermShk` flag so that
  a newborn's permanent income is its initial draw, bst/1's convention.
- The community library's buffer-stock model: QuantEcon community-library pull request 5, the `library` member of bst/1.
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
