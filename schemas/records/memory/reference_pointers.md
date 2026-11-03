---
name: reference_pointers
description: "Pull requests, repositories and sessions that the schema work points to"
metadata:
  type: reference
---

- The fork's eleven pull requests, all merged: https://github.com/llorracc/sce-wg-1-dev/pull/1 (the ontology, into
  `main`) and pulls 2 to 7 on 2026-10-21, 8 to 11 on 2026-10-22 (into the schemas' branch). The project state lists what
  each held.
- HARK's draft pull requests from the owner's fork that bear on the adapters: econ-ark/HARK#1858 (the Markov solver's
  expectations on the current state's points, and its value function; the HARK adapter's pin, commit `03a2c7a1` on
  llorracc/HARK's branch `markov-exact-expectations`), #1859 (the employment income process for the Markov consumer),
  #1860 (`NewbornPermShk`), #1862 (the natural limit from the shock laws' recorded infima, stacked on #1858; head
  `11852805`, the adapter's pin in the fork's #12). The fork's tags `sce-adapter/2026-10-22` (`03a2c7a1`) and
  `sce-adapter/2026-10-22.2` (`11852805`) keep the pins reachable. Others' open ones: #1848 (cubic interpolation above
  the grid), #1853 (human wealth in the Markov solver).
- Econ-ark's notation registry, `@resources/notation/notation.yml` in econ-ark/econ-ark-tools, with the generated
  `econark-notation.sty`, `notation-math.yml` and `NOTATION.md`: version 1.0.0 on its master once econ-ark-tools' pull
  requests #38 to #44 merged on 2026-10-21, then 2.1.0 (#46), with rows for the schemas' own symbols, and 3.0.0 (#47)
  that evening; 5.0.0 (#49), 6.0.0 (#50) and 8.0.0 (#52) on 2026-10-22. A branch `notation-v8.1-spic` of the clone at
  `/home/shared/github/econ-ark/econ-ark-tools` (commit `68a242d7`, 2026-11-02, unpushed) holds an 8.1.0 that the
  ruling of 2026-11-03 superseded, to delete. Beside it, `econark-shortcuts.sty` in the same repository's `@resources`, the macros most papers load,
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
- HAFiscal's published replication package, llorracc/HAFiscal-QE (public): `Results/DiscFacEstim_CRRA_2.0_R_1.01.txt`
  for the estimated discount factors, `EstimParameters.py` for the defaults the schemas had mistaken for them,
  `Parameters.py` for how the types are built. The Markov family's members take their values from it (#13).
- The community library's buffer-stock model: QuantEcon community-library pull request 5, the `library` member of bst/1.
  Its HARK implementation now lives at `solutions/buffer-stock/001-hark-egm/` in QuantEcon/community-library, moved there
  by a later pull request of the library; it uses HARK alone.
- The lower-tail finding's record in the paper's working repository (private as of 2026-10-18): a note among its theory
  notes on power-law decay, committed on its port branch and on master with a numerical battery, unpushed that day.
- Bellman-SYM: the stage files here were elaborated and calibrated by the bellman session under Bellman at its repository
  head and under the Matsya service's installed version; the repository and its documentation site were not public on
  2026-10-18, nor on 2026-10-22, so its pages were cited by title, and since 2026-10-22 its rules are stated as the
  schemas' own.
- Matsya: the design review of 2026-10-18 ran as four questions in one session and one stage-file question in another; the
  client is `bellman-matsya`. Its four questions-only sessions on the ontology of probability distributions ran from the
  bellman session on 2026-10-19; their answers are kept outside this repository, and the findings of that day hold what
  they say.
- The buffer-stock benchmark `bst_bench` lives in HAFiscal-Latest, destined for its own econ-ark repository; its emitter of
  results files in this schema's form is the HAFiscal-Latest session's.
- The ontology of buffer-stock models' sources, pinned on 2026-10-31:
  - BST's published page, https://llorracc.github.io/BufferStockTheory/, an older build than the paper's working copy;
    its anchors are in `ontologies/buffer-stock-models/bst-anchors.txt`;
  - econ-ark's notation registry 8.0.0, at econ-ark-tools commit `9d3d108a`;
  - HAFiscal-QE's public head, `1afdf80` (2026-06-12);
  - HARK main at `4c285e86`, now cited only by HARK's stone.
- HARK's commit `54083db5` (2021-07-09; issue econ-ark/HARK#1022, merged in #1039): the cyclical solve order, under which
  entry k of a time-varying list is the move into k. Its simulation of shocks, growth and the return was left reading
  entry s − 1.
- The fork's pull request #15, open: https://github.com/llorracc/sce-wg-1-dev/pull/15, the stage files' rewrite with
  derivative terms (2026-10-31).
- An issue in the paper's private repository (2026-11-01) asks for a proof that the WRIC is necessary without an
  artificial constraint; this public repository gives no link to it.
- Ma, Stachurski and Toda, read for the ontology on 2026-11-01 in their arXiv versions:
  https://arxiv.org/abs/1905.13045v3 (the income fluctuation problem, 2020) and https://arxiv.org/abs/2012.00219v2 (the
  Q-transform, 2022).
- HARK's Rosetta Stone holds, since 2026-11-01, HARK's names for the ontology's terms and its departures from them:
  `schemas/rosetta/hark.md`, section "The ontology's terms in HARK".
- HARK's draft econ-ark/HARK#1869: the continuous path, expectations by quadrature over the true truncated laws. HARK's
  kink-split page, https://econ-ark.github.io/HARK-dev/kink-split-quadrature/, is public; the HARK-dev repository is not.
- The community library's buffer-stock model description: `models/buffer-stock/model-description.md`, version 0.1, in
  `llorracc/community-library`, a public fork of QuantEcon/community-library whose push to QuantEcon is disabled. It has
  its own session; a change there is that session's, and a push needs the owner's word in it.
- HAFiscal's emitter of results files in this schema's form is `Code/HA-Models/bst_bench/schema_results.py` in
  HAFiscal-Latest; it writes the retired family key `bst/1` and reads `bst-1/` until the HAFiscal session updates it.
- BST's public source, https://github.com/llorracc/BufferStockTheory: the table "Microeconomic Model Calibration"
  (`Tables/Calibration.tex`), the restrained-limit suite's calibration, and the subsection "The Liquidity Constrained
  Solution as a Limit" (`sec:deatonIsLimit`), its experiment; the published page, https://llorracc.github.io/BufferStockTheory/.
- HAFiscal's published package, llorracc/HAFiscal-QE: the toy-hafiscal suite's targets and objective in
  `Code/HA-Models/Target_AggMPCX_LiquWealth/Estimation_BetaNablaSplurge.py` (`lorenz_target`, `Agg_MPCX_target`,
  `KY_target`), the Lorenz data in `Code/Empirical/make_liquid_wealth.py`, the discount factors of record in
  `Code/HA-Models/Results/attribution/DiscFacEstim_preOptionD.txt`.
- DolARK, EconForge/dolark.py at `b0eef38` (2023-04-12), and econ-ark/DARKolo at `8e428de` (2021-11-16): read for the
  Jacobian interface's design, which takes DolARK's split of the agent into a backward and a forward operator.
- HARK's sequence-space Jacobians: `AgentType.make_basic_SSJ` in `HARK/core.py` and `HARK/SSJutils.py` on main at
  `4c285e86`; the open pull requests that bear on the interface, econ-ark/HARK#1823 (an unperturbed baseline for
  patient households), #1826 (the direct column's dating), #1828 (the income mass's response), #1835 (aggregating types,
  a flow-budget check), #1842 (the economy's trend), #1860 (`NewbornPermShk`), #1863 (the truncated lognormal).
- HAFiscal's household Jacobians in its published package, llorracc/HAFiscal-QE,
  `Code/HA-Models/FromPandemicCode/HA-Fiscal-HANK-SAM.py` and `HA-Fiscal-HANK-SAM-to-python.py`.
- The page "The Restrained Limit", https://claude.ai/artifact/Lp8sHuCW2EoAvqDYfmBcdb: a private claude.ai page,
  published 2026-11-01, drawing the restrained-limit suite's HARK run; its source is
  `findings/2026-11-01_restrained-limit-suite-hark/page/`. Only the owner can open it until he shares it.
