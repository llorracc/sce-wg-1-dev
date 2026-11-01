# Rulings of 2026-11-01

The owner's decisions that reach the ontology of buffer-stock models, in substance and by time (EST, since daylight
saving time ended at 02:00 that morning). His words are kept outside this public repository.

- **09:13:31, weak return impatience.** An issue in the paper's repository is to take up the question of whether the
  WRIC is necessary without an artificial constraint. Until a proof is added, the ontology assumes the claim is true.
  The issue was filed at 09:26:00 in the paper's private repository, with a route to a proof. The ontology's row
  `wric-without-artificial-constraint` records the decision.
- **09:13:31, Ma, Stachurski and Toda.** Their papers are to be read, and their conditions stated in the ontology's terms.
  Done as the liquidity-constrained class, the condition MST-βR and four results
  ([the findings](../findings/2026-11-01_ontology-draft2.md)).
- **09:23:51, no toolkit in the ontology.** The semantic ontology names no toolkit, and nothing peculiar to how a toolkit
  solves or simulates the problem. Each toolkit used to solve the buffer-stock problem has a document of its own. Applied
  through the schemas' Rosetta Stones: HARK's names and its ten departures moved to HARK's stone
  ([[feedback_ontology-names-no-toolkit]]).
- **10:05:57, the cyclical index, clarified.** His ruling of 19:38:51 on 2026-10-31 is that HARK's solver and its
  simulation be consistent with each other. It does not find either one right: the simulation may be the one that is
  right now and the solver the one in error, though he does not think so. The direction to fix the simulation side
  stands. The ontology's draft and then HARK's stone had recorded the ruling as "the solver's convention stands and the
  simulation is to follow it". That wording, never committed, is corrected, and the HARK-dev session was told at 10:08:48
  ([defects](../defects.md)).
- **10:05:57, β.** A requirement in the schemas or the ontology that β ≤ 1 would be an error in them, not a divergence of
  a paper or its code. Neither states one: both parameter schemas require only β > 0, and the ontology's sampled models
  draw β up to 1.3 ([[feedback_no-upper-bound-on-beta]]).
- **10:05:57, "commit and memorialize".**

**What stays open:**
- whether HAFiscal's cap on its types' discount factors, which places survival outside the patience factor in a condition
  its code calls the GIC-Mod, is a divergence of HAFiscal or a condition the ontology should state;
- what belongs in a Rosetta Stone, against which the HARK section moved there is to be judged. The owner offered a fuller
  account of a stone's scope;
- from the reading of Ma, Stachurski and Toda:
  - whether their results hold for a continuous permanent shock, where the normalized problem's discount factor and
    return share an innovation;
  - whether their 2022 approach extends to the normalized problem's random discount factor;
  - what holds for a borrowing limit strictly between the natural one and zero;
- the questions still open from 2026-10-31 ([the rulings of that day](2026-10-31_ontology-decisions.md)).
