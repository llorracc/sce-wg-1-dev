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
- **13:32:13, "memorialize".**
- **13:38:32, two principal families,** typed in the community library's session, in reply to its report that the
  truncated `library` no longer matches the library's published description; relayed here and checked against that
  session's transcript. The schemas are to have two principal versions, under the natural constraint and under a
  binding artificial one. In practice the model is solved numerically under an artificial constraint, and the natural
  scenario without a point mass is of more theoretical than practical interest. The other scenarios' folders go into a
  subdirectory `other/`. Applied to both families: `bst/other/` holds `natural-no-point-mass/` and `zero-infima/`, and
  `bst-markov_ui-and-agg/other/` holds `zero-infima/`. The families, their keys and their members' hashes are unchanged.
  It supersedes nothing; all six families stand.
- **13:39:43 and 13:43:31, two instructions on HAFiscal's laws,** typed in the same session and addressed to the
  HAFiscal-Latest session; they concern HAFiscal's own work, and are kept outside this public repository. By that
  session's report, the owner settled there at 13:49:54 that nothing in HAFiscal changes.
- **13:46:13, the Markov family to correspond to what HAFiscal does,** typed in the same session and checked the same
  way: `bst-markov_ui-and-agg/` is to be revised to correspond to HAFiscal, which does not have zero infima.
- **13:47:07, the published paper's results are not redone,** typed in the same session and checked the same way. At
  most, new documents or comments point from them to later developments.
- **13:51:57, the Markov zero-infima version replaced,** typed in this session. HAFiscal never used the zero-infima
  version; what was recorded for it is to be replaced with artifacts that follow what HAFiscal does, in the appropriate
  place. Applied: the version `bst-markov_ui-and-agg-zero-infima/1`, its stage file, its parameter schema and its three
  calibrations are retired, and `paper-published` and `paper-one-group` are members of
  `bst-markov_ui-and-agg-artificial/1` with the laws the published code solves on, 7 equiprobable atoms of each
  lognormal, under its a ≥ 0. Their other values are unchanged, so they reproduce the published numbers and nothing is
  redone. It supersedes this session's move of that version to `other/` at 13:43, and the reading of the 2026-11-01
  scenarios proposal that put the paper's members in the zero-infima scenario by the paper's stated laws.
- **14:42:57, what the Markov family is for.** It is not meant as a full statement of HAFiscal's Markov structure, whose
  benefits can run longer. It gives the worst, "disaster", state a parameter of its own, and it is not a model distinct
  from the natural or the artificial case: it implements either without rewriting a toolkit's i.i.d. solver. A test
  comparison the owner wants among candidate buffer-stock models is BST's own experiment, "The Liquidity Constrained
  Solution as a Limit": a natural constraint at 0 from a very small point mass of zero income, against an artificial
  constraint at 0.
- **14:49:50, the device is one disaster state, not persistent.** There is one unemployment state, the disaster, with
  ξ_x = 0, and being in it this period does not make it likelier next period. It corrects this session's reading at
  14:43, which took the family's four-state, persistent chain as the device.
- **14:50:39, the schema is not to require ξ_x > 0.** Applied: `income_without_benefits` may be 0 in the Markov
  family's parameter schema and stage file, and the checker counts the chance of a zero-income state from ξ's mass
  alone.
- **14:55:52, `toy-as-hafiscal` renamed and recalibrated:** it is to be the artificial version of the Markov model, with
  unemployment probability 0.05 and benefit 0.5. Applied as `iid-ui-artificial`: job loss 0.05 and job finding 0.95 in
  both regimes, so the one unemployment state does not persist; both benefits 0.5; a ≥ 0; employed income scaled to
  mean one, (1 − 0.05·0.5)/0.95, as in the buffer-stock families; the toy's other values. Its counterpart is the toy
  with ℘ = 0.05 and ξ_u = 0.5.
- **14:59:32, the natural version's calibration straight from BST,** with three values of ℘, to show the convergence to
  the artificial version as ℘ falls.
- **15:01:21, a suite of tests for every toolkit's BST solution:** the three natural members and the one artificial.
  Applied: `bst-p-zero-0.005`, `-0.0005` and `-0.00005` in `bst-natural/1`, BST's calibration with ξ_u = 0, and
  `bst-restrained` in `bst-artificial/1`, the same with no zero-income event and a ≥ 0, BST's restrained consumer
  (`bst/model.md`, "A test suite"). The first rung is the same model as `library`.

- **15:06:08, a toy-hafiscal suite.** A suite of solutions of the artificial version, "toy-hafiscal": HARK's and
  HAFiscal's machinery estimates three discount-factor types to match the Lorenz curve's moments and the iMPC, with no
  splurge. The resulting calibration goes to every toolkit, which solves and simulates the steady state, so that the
  SSJ exercise can be done on each. The estimation is not asked of the other toolkits.
- **15:09:16, its details.** The toolkits are to expose whatever is needed to compute their Jacobians. The types are a
  center and a spread; the targets are HAFiscal's Lorenz targets and the iMPC's whole profile; every value but the
  discount factors is `iid-ui-artificial`'s (`bst/model.md`, "The toy-hafiscal suite").
- **15:57:06, the toy-hafiscal targets completed, and "memorialize".** The toy also targets the ratio of liquid wealth
  to quarterly income, 6.60, with the published objective's block for it; the wealth-quartile block is left out. Every
  winner gets the same prize, as the published code has it. Then a memorial.
- **16:10:29 and 16:16:38, the Markov family retired.** The four-state family is to be retired and replaced with the
  one-state version, under a name distinct from HARK's tools. Asked why a new name was needed, the owner answered that
  what he asked for is a particular calibration of the artificial-constraint model. Applied: `bst-markov_ui-and-agg`, its
  stage file, schemas, documents, members and checker module are retired; `iid-ui-artificial` is a `bst-artificial/1`
  member, the toy with ℘ = 0.05 and ξ_u = 0.5. It supersedes the morning's two versions and this afternoon's one.
- **16:17:30 and 16:17:44, no version with zero unemployment income was asked for.** This session had offered a natural
  counterpart of `iid-ui-artificial` paying zero; none is built.
- **16:33:50, "memorialize".**
- **16:37:49, the Jacobian interface to be drafted with the toolkits,** looking at DolARK, HARK and HAFiscal.
- **17:05:24, its design decided** (`jacobians.md`): the Jacobians with their metadata required and the fake-news
  ingredients optional, as data; all three inputs as proposed, the income scale moving all non-capital income and the
  transfer proportional to permanent income, reaching newborns; the outputs and the file format left to this session,
  which chose C, A and Y and `.npy`; one distribution grid for every toolkit; the finite-prize iMPC omitted; a
  steady-state tolerance of 10⁻¹⁰. Asked why the QuantEcon module would be restarted: it would not; under the ruling of
  20:36:49 on 2026-10-21 the next toolkit is dolo.
- **17:09:41, the toy's prize: the four random sizes.** The toy-hafiscal estimation draws each winner's prize from
  Fagereng, Holm and Natvik's four sizes, with equal probability, as the paper describes. It supersedes the single prize
  of 15:57:06.
- **17:12:52, the prize's units, "b, I guess?":** each prize a level, equal to its fraction of the population's mean
  quarterly income, about 1.434 newborn units in the toy, rather than of a newborn's permanent income or of each winner's
  own. Given tentatively, so open to change.
- **17:21:37, "go ahead; memorialize":** the Jacobians' results-schema block to be drafted, and a memorial. Drafted as
  `bst/jacobians.schema.json`, outside `results.schema.json` until he approves it.

**What stays open:**
- the Jacobians' results-schema block, drafted, for the owner's approval; where the target 6.60 is computed; the estimation itself, which HAFiscal's tools do on the owner's word in that
  session;
- whether the suite's smallest ℘ should be smaller: at 0.00005 the largest gap to the restrained rule is still 0.027;
- members for HAFiscal's model as its current code solves it, and calibrations for the artificial stage file: their
  values are unpublished, and wait for the owner's word that they may go into this public repository. The published
  package's atoms have no stage file;
- `library` against the community library's published description, v0.1, with untruncated laws: a v0.2 of the
  description with truncated laws, which is the community library's session's to write in `llorracc/community-library`;
  a renamed member; or a note;
- the push of `buffer-stock-ontology` and its draft pull request, refused by the session's permission check;
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
