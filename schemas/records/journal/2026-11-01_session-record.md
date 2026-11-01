# Journal of 2026-11-01

Times are EST, from the session's transcript; daylight saving time ended at 02:00. The day opens on the uncommitted
draft.2 of the ontology and the open pull request #15 ([the journal of 2026-10-31](2026-10-31_session-record.md), after
its memorial).

- **09:13:31.** The owner rules on weak return impatience and asks that Ma, Stachurski and Toda's conditions be stated in
  the ontology's terms (see the rulings).
- **09:14:07, a question.** How do the ontology and the schema relate? Answered from the README: a schema fixes one
  family's written form, while the ontology states the model class, which each written form denotes; SBML and SBO split
  in the same way.
- **09:15:34, a question.** What are the 46 tests: did they solve the model 46 times? They do not. None solves a model.
  They check the ontology's consistency, its agreement with the schemas' checker on the members' conditions, the moments'
  closed forms, and the implications among conditions on 6000 sampled parameter sets. A result about solutions is
  recorded with its source, not tested ([[feedback_say-what-tests-establish]]).
- **09:16:28.** The owner asks for the ontology and the schema in VS Code. They opened at 09:17:13 on the machine's
  desktop: the repository, the ontology's source and README, bst/1's parameter schema and `model.md`, and the rewritten
  stage file from #15's worktree.
- **09:19:36 and 09:20:38.** Ma, Stachurski and Toda (2020) and (2022) are fetched in their arXiv versions and read.
- **09:23:51.** The owner rules that the ontology names no toolkit (see the rulings).
- **09:26:00.** The issue on the WRIC is filed in the paper's private repository. It quotes the sentence, states the claim,
  and sketches a proof from results the paper already has.
- **09:27:39.** HARK's names, sources and ten departures start to leave the ontology; their identifiers are retired, and a
  test now holds the ontology to naming no toolkit.
- **09:30:39.** Nine rows state Ma, Stachurski and Toda's conditions in the ontology's terms (`BSM_0000197` to
  `BSM_0000205`). One deduction of 2026-10-31 is restricted to a borrowing limit (see the defects).
- **09:31:32.** The ontology's 47 tests pass, and the generated files are current. The ontology of probability
  distributions' 12 and the checker's 175 pass as well.
- **09:32:09.** The HARK material goes into a new section of HARK's Rosetta Stone. At 09:34:26 the changelog is
  rewritten, and the tests pass again at 09:34:36 and 09:36:58.
- **09:36:07 and 09:37:01.** The private page of the ontology and the schemas is republished.
- **10:05:57.** The owner clarifies the cyclical ruling and rules on β (see the rulings). He asks what the HAFiscal
  divergence is, and what the question about HARK's stone was. He asks for a commit and a memorial.
- **10:08:48.** The HARK-dev session is sent the clarification in his words, for its records.
- **From 10:08.** The ruling's wording is corrected in HARK's stone and the changelog, and the memorial is written; the
  clock read 10:10:42 as the records began.

- **10:14:35.** The memorial is committed as `427136d`, and the page is republished.
- **10:18:27.** The owner rules that HAFiscal's cap is an implementation detail, and at 10:18:41 asks for a memorial here
  and in HAFiscal (see the rulings). The public package's comments, read at HAFiscal-QE `1afdf80`, present the cap as a
  theoretical requirement.
- **10:19:34.** The HAFiscal-Latest session is sent both rulings in his words, to be checked with the relay checker, with
  what those comments say.
- **From 10:20.** The ontology's divergence on the cap is retired, and the ontology's 47 tests pass. The second memorial
  is written.

- **10:18–11:44.** HAFiscal-Latest commits its memorial (`764c0d37`, 10:24:21). On the owner's word in that session at
  11:12:02, HAFiscal-QE's comments on the cap are corrected and pushed as `8d8b71e` (11:13:57).
- **11:44:52 and 11:46:18.** The owner asks for every configuration of a valid buffer-stock model, each a schema with its
  own stage file (see the rulings). A proposal follows; at 12:19:08 he asks for at least three scenarios, refined with
  the BST, HARK and HARK-dev sessions, and places HAFiscal in the second.
- **12:28:24 to 12:32:00.** The four sessions answer, in order:
  - HARK-dev, at 12:28:24: the min construction, the point-mass rule, and the third scenario's mass at zero;
  - HAFiscal-Latest, at 12:28:51: its published model is in the third scenario by its stated laws, and computed as if in
    the second, on atoms;
  - HARK, at 12:30:00: which scenarios its types can express, and that h_min > 0 needs both infima positive;
  - BST, at 12:32:00: its own model has h_min = 0, the point mass is joint, and there is a fourth scenario.

  The proposal is written as `constraint-scenarios.md`.
- **12:30:17.** The owner rules that a modified condition's modifier follows its base name: FVAC-PF.
- **12:50:56.** The owner rules on the proposal (see the rulings).
- **From 12:51.** The six families are written and tested: the four buffer-stock families and the Markov family's two
  versions, each with its own stage file, all six elaborating on Bellman-SYM's current main; the checker, the adapter,
  the stones, the documents and the ontology follow. At 13:23:13 the checker's 194 tests, the ontology's 52 and the
  ontology of probability distributions' 12 pass; the adapter's 7 passed earlier at its pinned HARK.

**State at the second memorial** (10:21):
- Draft.2 of the ontology, HARK's stone, these records and the memory are committed on `buffer-stock-ontology`, in the
  memorial of 10:14:35 and the one after it. Nothing is pushed.
- The HAFiscal-Latest session holds the owner's two rulings of 10:18, for its own memorial and its code's comments.
- Pull request #15, the stage files' rewrite, is open against the schemas' branch, unmerged.
- The issue on the WRIC is open in the paper's repository.
- The open decisions are in the rulings and the deferred follow-ups.

- **13:25:11.** The scenarios are committed on `buffer-stock-ontology`. The push and the draft pull request against
  the schemas' branch are refused by the session's permission check as an external write, and wait for the owner. The
  sessions whose work reads the families are told: HAFiscal-Latest (its emitter's family keys, FVAC-PF and the binding
  case's wording) and the community library's (the `library` member truncated, its new path and calibration).
- **13:26:39.** The community library's session notes that its published model description, v0.1, states untruncated
  laws, so the truncated `library` is no longer its model as published, and its results will differ slightly from its
  HARK solution's. Put to the owner, with three options: a v0.2 of the description with truncated laws (recommended), a
  renamed member, or a note. Under the rulings the untruncated model, with its zero-income event, is in no scenario.
- **13:27:45.** HAFiscal-Latest corrects this session's message to it: it had not advised leaving `borrowing_constraint`
  out of the zero-infima members, which is the owner's decision. It cautions that a solver taking the natural limit from
  atoms would let agents borrow. Both families' model documents now say that the zero-infima stage files impose a ≥ 0
  themselves and that a toolkit imposes it as stated; the commit is amended at 13:28:22 as `5cdda98`. HAFiscal's emitter
  hardcodes the old family key and folder; that session has told the owner.
- **13:31:21.** The owner asks where a revision of the library's description to v0.2, and its push, would be done. The
  answer: in neither this session nor the working group's, but in `llorracc/community-library`, by its own session. That
  repository is public, so a relay can carry the commit and not the push, which needs his word in that session.
- **13:32:13.** "memorialize".

**State at the memorial (13:33):**
- The scenarios and the memorials are committed on `buffer-stock-ontology` and unpushed; the push and the draft pull
  request wait for the owner's permission.
- #15 stays open.
- Open with the owner: `library` against the community library's v0.1.

- **By 13:39:27.** The community library's session relays the owner's ruling, typed there at 13:38:32: two principal
  families, natural and artificial, and the others in `other/`. It is checked against that session's transcript as typed
  by the owner, in reply to the report on `library` against v0.1. The session's reading had the Markov family with only
  a zero-infima version; it has an artificial version too, which that session corrected by 13:40.
- **By 13:40:52.** The same session relays an instruction of the owner's to the HAFiscal-Latest session, typed there at
  13:39:43, about HAFiscal's laws; checked the same way, and kept outside this repository.
- **13:40–13:43.** Applied. The natural scenario without a point mass and the zero-infima scenario move to `bst/other/`,
  and the Markov family's zero-infima version to `bst-markov_ui-and-agg/other/`, with `git mv`. The moved parameter
  schemas' references to the shared definitions go up one more level. The checker and the Markov checker resolve each
  family's folder from the list of principal scenarios. The tests, the ontology's family entries and the documents name
  the new folders. Family keys, file contents and hashes are unchanged. The checker's 194 tests and the ontology's 52
  pass, and its generated files are current; the adapter's 7 pass at its pinned HARK, the moved members among them.
- **By 13:43:46.** The same session relays the owner's answer to it, typed there at 13:43:31, on the same subject;
  checked the same way, and kept outside this repository.
- **After 13:44.** The HAFiscal-Latest session asks that `paper-published` and `paper-one-group` stay where they are
  until the owner answers its question; they stay. The Markov model's sentence on HAFiscal's plans is taken out.
- **By 13:46:49.** The community library's session relays the owner's ruling, typed there at 13:46:13 and checked: the
  Markov family is to correspond to what HAFiscal does, which has no zero infima. HAFiscal-Latest is asked for its
  values and which of them are unpublished; the revision is put to the owner as a proposal.
- **By 13:47:31.** The same session relays the owner's ruling, typed there at 13:47:07 and checked, that the published
  paper's results are not redone; at most, documents or comments point to later developments.
- **13:49:47.** The owner types "No; we need", which arrives cut off; he is asked to finish it.
- **13:51:57.** The owner, in this session: HAFiscal never used the zero-infima version, which is to be replaced with
  artifacts that follow what HAFiscal does. HAFiscal-Latest is asked for the atoms its published code solves on and for
  its current values.
- **13:52–13:58.** The Markov checker is reduced to the artificial version: a law with a zero floor is refused, and so
  is the retired version's key. Its tests lose the cases that wrote the untruncated buffer-stock toy in the family and
  test both refusals instead. The ontology's family row for the zero-infima version is retired.
- **13:59:03.** HAFiscal-Latest answers: the published code builds each shock as 7 equiprobable atoms of the mean-one
  lognormal (HARK's `construct_lognormal_income_process_unemployment`, no unemployment atom, HARK 0.14.1 for the
  estimates of record) and imposes `BoroCnstArt` = 0 in every state. `paper-published`'s discount factors and splurge are
  the estimates of record, in HAFiscal-QE's `Code/HA-Models/Results/attribution/DiscFacEstim_preOptionD.txt`; the
  published simulations also cap age at 200 quarters, and newborns start with assets of 1e-5. Its current model's values
  are unpublished. It reports that the owner settled in its session at 13:49:54 that nothing in HAFiscal changes.
- **14:00–14:04.** Applied. `paper-published` and `paper-one-group` move to `artificial/members/` with the atoms as
  `Discrete` laws and `borrowing_constraint: 0.0`; their hashes change. The zero-infima version's stage file, schema and
  three calibrations are removed. The Markov checker's search for the tail exponent stops where its function leaves the
  floating range, which bounded laws reach for the impatient types, instead of failing. The Markov model and conditions,
  the READMEs, the scenarios proposal, the design note and the ontology are rewritten for the one version.
- **14:42:57.** The owner on what the Markov family is for, and on BST's experiment as a test comparison (rulings). BST's
  subsection "The Liquidity Constrained Solution as a Limit" is read in BufferStockTheory's public source: the
  natural-constraint rule converges, as ℘ ↓ 0, to that of the "restrained" consumer, with ℘ = 0 and c ≤ m. Put to him:
  the experiment's members in the buffer-stock families, a natural version of the Markov family, and what becomes of the
  paper's members.
- **14:49:50.** The owner corrects the reading: one unemployment state, the disaster, with ξ_x = 0, not persistent. Put
  to him: retiring the four-state family and treating the device as method (recommended), rebuilding it as the device,
  or keeping it.
- **14:50:39.** The owner: the schema is not to require ξ_x > 0. Applied by 14:52: the parameter schema allows 0, the
  stage file's ξ_x is in ℝ₊, and the checker's chance of the worst income takes a zero-income state's mass from ξ alone,
  since its income is zero whatever ψ is. A new test puts ξ_x = 0 in `toy-as-hafiscal`: U_1 and X get natural limit 0
  with chance 1 − `find`, E and U_2 stay below zero, and a ≥ 0 has a kink in E and U_2 only. The checker's 189 tests and
  the ontology's 52 pass, and the stage file elaborates.
- **14:55:52.** The owner asks what `toy-as-hafiscal` does, and wants it renamed as the artificial version of the
  Markov model, with unemployment probability 0.05 and benefit 0.5. Told: it was the toy written in the family, already
  non-persistent, since its job finding was one minus its job loss and its three unemployment states paid the same.
- **14:56–14:57.** Applied as `iid-ui-artificial` (`git mv`), with job loss 0.05, job finding 0.95, both benefits 0.5
  and employed income scaled to mean one; its hash changes. The consistency test now checks it against its
  buffer-stock counterpart, the toy with ℘ = 0.05 and ξ_u = 0.5, which is a valid `bst-artificial/1` member, and the
  reduction tests run on that counterpart too. The checker's 191 tests and the ontology's 52 pass.
- **14:59:32.** The owner: the natural version's calibration straight from BST, with three values of ℘, to show the
  convergence to the artificial version. BST's table "Microeconomic Model Calibration" is read in its public source:
  𝒢 1.03, R 1.04, β 0.96, ϱ 2, ℘ 0.005, σ_ψ and σ_θ 0.1, which is `library`'s. The limit is BST's restrained consumer,
  with ℘ = 0 and c ≤ m, not `iid-ui-artificial`.
- **15:00–15:02.** The four members are written; the checker accepts them, the first rung with `library`'s hash. The
  HARK adapter turns out to solve every buffer-stock member with HARK's Markov consumer on a two-state chain that is not
  persistent, the device the owner described at 14:42:57.
- **15:01:21.** The owner: these four are one suite of tests for every toolkit's BST solution.
- **15:02–15:03.** The four solved with the adapter's route at level 1: the largest gap to the restrained rule over m
  in (0, 10] is 0.138, 0.061 and 0.027, largest at m ≈ 0.98, the restrained rule's kink. The suite is written into
  `bst/model.md` with that result; a checker test confirms that the four differ only in ℘ and the constraint, and the
  ontology's test classifies them. The checker's 192 tests and the ontology's 64 pass. The adapter gains a test that each
  rung's gap is smaller than the last, and its 8 tests pass at its pinned HARK.
- **15:06:08.** The owner specifies a toy-hafiscal suite (rulings) and asks for it to be explained back. Explained, with
  four questions: what the Jacobians need beyond a steady state, how the types are set, which targets, which
  unemployment calibration.
- **15:09:16.** The owner answers all four (rulings). The suite is written into `bst/model.md`; the section of the
  first suite is renamed "The restrained-limit suite", since parts get names. HAFiscal-Latest is asked for the targets,
  their sources and weights, and whether its estimation code can run the model, and told not to start on this
  session's word.
- **By 15:20.** HAFiscal-Latest answers from the published package: the Lorenz points of liquid wealth from the 2004
  SCF, the iMPC profile of Fagereng, Holm and Natvik, the mapping from quarters to years, and the objectives. Its
  estimation code is the model class of its first step and would need the toy's parameters, three types, a choice of
  objective blocks and the toy's laws. It flags two points to the owner: the paper's wording on ranking (by income,
  where the code ranks by liquid wealth) and a switch for a random prize that never runs. The public facts are written
  into `bst/model.md`; the toy's prize law and whether it targets the wealth-to-income ratio are put to the owner.
- **15:57:06.** The owner: include the wealth-to-income ratio, use the single prize, memorialize. Both written into the
  suite's section; the memorial follows.

**State at the memorial (15:59):**
- Everything since `4f20864` is uncommitted until this memorial's commit, which holds it all, on `buffer-stock-ontology`,
  unpushed. The push and the draft pull request still wait for the owner.
- Two buffer-stock families principal, `bst-natural/1` and `bst-artificial/1`; the other two in `bst/other/`. The Markov
  family has one version, `bst-markov_ui-and-agg-artificial/1`, with `paper-published`, `paper-one-group` and
  `iid-ui-artificial`, and allows ξ_x = 0.
- Two suites: the restrained-limit suite, written and tested; the toy-hafiscal suite, specified, its estimation
  HAFiscal's to do on the owner's word.
- The checker's 192 tests, the ontology's 64 and the adapter's 8 pass; every stage file elaborates.
- Open with the owner: the four-state Markov family's fate; the Jacobian interface; the smallest ℘ of the first suite;
  `library` against v0.1; the push.

- **16:10:29.** The owner: retire the four-state Markov family, replace it with the one-state version, and propose a name
  distinct from HARK's tools. HARK's source is searched: its tools are the `…ConsumerType` classes and `Cons…Model`
  modules, none called "disaster". Proposed `bst-unemployment-state/1`, with the question what it states that the
  buffer-stock families cannot.
- **16:16:38.** The owner: why a new name, when it is a calibration of the artificial-constraint model? Agreed.
- **16:17:30 and 16:17:44.** The owner, mid-turn: no version with zero unemployment income was asked for. Answered that
  none is built; the members with zero unemployment income are the restrained-limit suite's rungs, BST's own, and
  `bst-restrained`, which has no unemployment.
- **16:17–16:20.** Applied: `iid-ui-artificial` moved to `bst/artificial/members/` (`git mv`) as the toy with ℘ = 0.05
  and ξ_u = 0.5; the folder `bst-markov_ui-and-agg/`, `markov.py` and its tests removed; the checker's command and the
  notation test without the family; the validator's refusal names the retirement; the ontology's family row retired; the
  READMEs, the adapter's and the stone's descriptions, the scenarios proposal and the dated notes rewritten. The
  checker's 169 tests and the ontology's 67 pass, the adapter's 8 pass at its pinned HARK, and no link is broken.
- **By 16:25.** HAFiscal-Latest: its emitter never named the Markov family, and its one note that did records the
  retirement. It adds that its estimation code's newborn differs from the family's: a first permanent shock and growth,
  a transitory shock of 1, assets of 1e-5. Written into the toy-hafiscal suite: the delivered member states the family's
  newborn, and its fit is to be evaluated again on it with HARK's adapter.
- **16:33:50.** "memorialize".

**State at the memorial (16:34):**
- Everything since `d60d9d8` is in this memorial's commit, on `buffer-stock-ontology`, unpushed; the push and the draft
  pull request still wait for the owner.
- The buffer-stock families: `bst-natural/1` and `bst-artificial/1` principal, two in `bst/other/`. The Markov family is
  retired; `iid-ui-artificial` is a `bst-artificial/1` member.
- The two suites: the restrained-limit suite, written and tested; the toy-hafiscal suite, specified, its estimation
  HAFiscal's on the owner's word, its fit to be checked on the delivered member with the family's newborn.
- The checker's 169 tests, the ontology's 67 and the adapter's 8 pass.
- Open with the owner: the Jacobian interface; the smallest ℘ of the first suite; `library` against v0.1; the push.

- **16:37:49.** The owner: draft the Jacobian interface with the toolkits, looking at DolARK, HARK and HAFiscal.
- **16:38–16:40.** The HARK, HARK-dev, HAFiscal-Latest and QuantEcon (community library) sessions are consulted with the
  same questions: what each computes now, whether to expose the Jacobians or the ingredients of a shared computation,
  the first inputs and outputs, and the checks. Three read-only surveys:
  - HARK's main branch: `make_basic_SSJ`, the fake-news algorithm on any scalar parameter, T × T, per type;
  - HAFiscal's published package: its own fake-news code on HARK, 8 inputs, the sequence_jacobian package for the
    general equilibrium only, the iMPC by simulation;
  - DolARK (EconForge/dolark.py) and DARKolo: no sequence-space Jacobians, but the backward and forward operators and the
    projection of aggregates into the agent's problem.
- **By 16:45.** The QuantEcon session answers: no machinery yet; the Jacobians in a results file as the canonical form,
  the two steps optional for Python toolkits; the conventions to pin; its module stopped since 2026-10-21.
- **By 16:45:27.** The draft written, `schemas/jacobians.md`, as a proposal: the Jacobians required in results, the
  household's two steps optional, the conventions, the checks the checker can make without solving, the decisions for the
  owner. It waits for the HARK, HARK-dev and HAFiscal-Latest sessions' answers.
- **By 16:52.** HAFiscal-Latest answers from its published package: its own fake-news code, the inputs in levels, a
  transfer that does not reach newborns, the splurge added afterwards, the general-equilibrium layer taking only the
  matrices; its advice to require the matrices, report both iMPCs, and leave the UI inputs for later. Folded into the
  draft, with three decisions added: the third input, whether a transfer reaches newborns, and the finite-prize iMPC. It
  also reports that the owner has asked it to make Step 1's prize random, as the paper describes, which bears on the
  toy's single prize of 15:57:06.
- **By 16:58.** The HARK and HARK-dev sessions answer, each with measurements on HARK's main branch at `4c285e86`: the
  two routes, dating as a flag the caller sets, the open pull requests that bear on it (#1823, #1826, #1828, #1835,
  #1842, #1860, #1863); the Jacobians required with their metadata, and the ingredients as data rather than a callable;
  the transfer proportional to permanent income; Y as an output; the flow budget, which closed to about 10⁻¹² and caught
  a one-row shift in R by 0.53. The draft's proposal half rewritten from all four answers; two items HARK-dev marked
  private are left out. HARK-dev notes that the stamp this session sent, 16:41, was inferred; the request was at
  16:37:49, and both sessions are told.
- **By 17:04.** The HARK session corrects its stamp to 16:37:49, checked in this session's transcript, and one number:
  HARK's two routes agree to within about half a percent once newborns start from the same wealth; the gap it had first
  measured came from its own setup. The draft's sentence that the older route dates R one period differently, taken from
  this session's reading of the code, is corrected to the sessions' measurement: R and income dated alike, the discount
  factor one period later.
- **17:05:24.** The owner decides the eight points (rulings). Written into `jacobians.md`, now marked as an approved
  design: the outputs C, A and Y; the matrices as `.npy` files beside the results file, listed with their hashes; the
  shared grid on end-of-period assets under the neutral measure, a_j = 500 (j/999)³ for 1000 nodes, with Young's lottery;
  the finite-prize iMPC dropped; the tolerance of 10⁻¹⁰; the QuantEcon item answered from the ruling of 2026-10-21.
- **17:09:41.** The owner: the toy uses the four random prize sizes. The sizes and their equal probabilities are read in
  the published package's `lottery_size_USD` and written into the suite's section, superseding the single prize of
  15:57:06.
- **By 17:12.** HAFiscal-Latest confirms the four-prize rule matches its fix, and asks what "of quarterly permanent
  income" means for the toy, whose population's mean permanent income is about 1.43 newborn units; put to the owner, with
  the prize as a level scaled to the population's mean income recommended. HARK-dev confirms HARK can follow the shared
  grid exactly and write the format, with three tasks for an adapter and HARK's memory at T = 300; written into the
  design.
- **17:12:52.** The owner chooses, tentatively, the prize as a level scaled to the population's mean quarterly income.
  Written into the suite's section, with the toy's mean permanent income, (1 − ℒ)/(1 − ℒ𝒢) ≈ 1.434.
- **By 17:13.** The HARK session confirms that HARK main can follow the grid and the format. Its one blocker for the
  suite is the truncated lognormal, which is in open draft #1863, not on main; the rest is adapter code. Its polynomial
  grid differs from the formula by up to four units in the last place, so the design now defines the nodes by correctly
  rounded operations, x = j/999, a_j = 500((x·x)·x), with the checker stating their hash; and sparse arrays sorted with
  zeros dropped, so that two files of one matrix are identical. HAFiscal-Latest confirms that the prize's units under the
  owner's choice are one line in the toy's parameter block, scaling its levels by about 1.434.
- **By 17:20.** HAFiscal-Latest confirms that HAFiscal can follow the design for the toy, with plumbing to do, and makes
  three corrections, all applied: mean non-capital income per unit of aggregate permanent income is ℒ𝒢 + (1 − ℒ𝒢)κ, not
  one, since newborns draw the employed branch (1.000115 for `iid-ui-artificial`), which also corrects the prize's units
  to about 1.4339; ρ is written R ℒ, so that the member's growth is not taken for the newborns' inherited trend; and the
  output Y is renamed Y_hh, so as not to collide with a general-equilibrium layer's Y. With all three toolkits'
  confirmations in, the results-schema block can be drafted.
- **17:19:01.** The owner asks for HARK's draft pull request #1863, the truncated lognormal, to be opened in the browser;
  opened.
- **17:21:37.** "go ahead; memorialize".
- **17:21–17:23.** The block drafted: `bst/jacobians.schema.json`, a JSON Schema of draft 2020-12 for an optional key
  `jacobians` of a results file, and a section of `jacobians.md` with the request's keys and the shared grid's SHA-256,
  `e8817602…`. In a scratch run the draft is a valid schema, an example with 36 matrices validates, and four deliberate
  breaks are refused.

**State at the memorial (17:24):**
- Everything since `d04e35d` is in this memorial's commit, on `buffer-stock-ontology`, unpushed.
- The Jacobian interface: design approved at 17:05:24; the results-schema block drafted, outside the results schema,
  for the owner's approval. HARK, HARK-dev and HAFiscal-Latest confirm they can follow the grid and the format; HARK's
  one blocker is the truncated lognormal of #1863.
- The toy-hafiscal suite: four random prizes, as levels scaled to the population's mean income; its estimation waits
  for the owner's word in HAFiscal's session.
- The checker's 169 tests, the ontology's 67 and the adapter's 8 pass.
- Open with the owner: approving the block; the smallest ℘ of the first suite; `library` against v0.1; the push.
