---
name: reference_pointers
description: "Pull requests, repositories and sessions that the schema work points to"
metadata:
  type: reference
---

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
  client is `bellman-matsya`.
- The buffer-stock benchmark `bst_bench` lives in HAFiscal-Latest, destined for its own econ-ark repository; its emitter of
  results files in this schema's form is the HAFiscal-Latest session's.
