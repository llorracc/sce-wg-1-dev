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
- **10:05:57, "commit and memorialize".** Committed at 10:14:35.
- **10:18:27, HAFiscal's cap.** HAFiscal's code caps each type's β through a growth-patience factor held a little below
  one. That cap is a pragmatic implementation detail. It cuts off the numerical problems that arise when parameters too
  near the boundary are tried, where the solution slows drastically. If HAFiscal's code and documentation do not explain
  this clearly, they should. It is not an intrinsic feature of the ontology or the schemas for generic buffer-stock
  models. The ontology's divergence `BSM_0000152` is retired. The public package's comments present the cap as a
  theoretical requirement ([the findings](../findings/2026-11-01_ontology-draft2.md)), so the explanation is still to be
  written, by the HAFiscal-Latest session.
- **10:18:41, "memorialize here and in HAFiscal".** The memorial in HAFiscal-Latest is that session's. It was sent both
  rulings in his words at 10:19:34, with what the public package's comments say.

- **11:12:02, in the HAFiscal session, relayed and checked there: the published package corrected.** HAFiscal-QE's
  comments on the cap are to say what it is too; done there as commit `8d8b71e`, pushed at 11:13:57.
- **11:44:52 and 11:46:18, every configuration a schema.** The family's definition has variants that call for different
  specifications. With the natural constraint in force, the permanent and transitory shocks need strictly positive lower
  and finite upper bounds; with an artificial constraint binding, no such requirement holds. The ontology and the
  schemas are to state every configuration that makes a valid buffer-stock model, and each is to be a schema with its own
  stage file.
- **12:19:08, the scenarios.** BST defines the model, with strictly positive bounds on both shocks. A discretized solution
  that is not told the laws' infima takes the natural constraint from the lowest atoms, and assuming the infima are zero
  would rule out the natural constraint ever mattering, which is not wanted. Even with an artificial constraint in
  force, the consumption function may be computed as the min of the constraint line and the consumption that a
  one-period relaxation toward the natural constraint gives. The BST, HARK and HARK-dev sessions are to be consulted, to
  refine at least three scenarios, each with its stage file:
  - the natural constraint, a > −hNrmMin, with hNrmMin strictly positive;
  - an artificial constraint tighter than the natural one, typically a ≥ 0, with hNrmMin strictly positive;
  - zero infima, where both constraints give a ≥ 0, after Ma, Stachurski and Toda.

  He placed HAFiscal in the second, and asked what had put it outside BST's class.
- **12:30:17, condition names.** A modified condition carries its modifier after the base name: `fvac-pf`, not `pf-fvac`
  ([[feedback_modified-condition-names]]).
- **12:50:56, the scenarios ruled** ([`constraint-scenarios.md`](../../constraint-scenarios.md)):
  - the natural scenario widened to hNrmMin ≥ 0, so that BST's own model belongs to it;
  - the natural scenario without a point mass made a scenario of its own;
  - the point mass required at the joint worst income, in place of the worst transitory realization of the ruling of
    2026-10-31;
  - `library`'s laws truncated;
  - the families' names `bst-natural/1`, `bst-natural-no-point-mass/1`, `bst-artificial/1` and `bst-zero-infima/1`,
    with the Markov family's artificial and zero-infima versions;
  - `a_Art` left out of the zero-infima scenario;
  - PF-FVAC renamed FVAC-PF in the schemas.

**What stays open:**
- what belongs in a Rosetta Stone, against which the HARK section moved there is to be judged. The owner offered a fuller
  account of a stone's scope;
- the existence of a solution in the natural scenario with a positive benefit, conjectured and not proved, and in the
  artificial scenario with a_Art strictly between −hNrmMin and 0;
- from the reading of Ma, Stachurski and Toda:
  - whether their results hold for a continuous permanent shock, where the normalized problem's discount factor and
    return share an innovation;
  - whether their 2022 approach extends to the normalized problem's random discount factor;
  - what holds for a borrowing limit strictly between the natural one and zero;
- the questions still open from 2026-10-31 ([the rulings of that day](2026-10-31_ontology-decisions.md)).
