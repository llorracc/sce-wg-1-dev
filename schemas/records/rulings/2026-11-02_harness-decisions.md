# Rulings of 2026-11-02

The owner's decisions on the experiments and the harness, in substance and by time (EST). His words are kept outside
this public repository.

- **09:48:03, the four pieces.** The project needs four things:
  - one ontology of buffer-stock models, consistent with Bellman's ontologies;
  - schemas of the experiments every toolkit is to perform;
  - a Rosetta Stone for each toolkit;
  - a harness that runs each toolkit's solutions.

  The owner asked whether the fourth has a usual name. The answer given: "harness", as in a test or evaluation harness,
  and the whole is a model intercomparison, as CMIP is for climate models.
- **09:57:09, the drafts.** The experiment schema and the harness plan to be drafted. Done:
  - [`experiments.md`](../../experiments.md), [`experiment.schema.json`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/experiment.schema.json) and the first
    experiment;
  - [`harness.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/harness.md).
- **10:33:47, the plan's six decisions** ([`harness.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/harness.md), "The owner's decisions"):
  - **Words:** approved. What were called test suites are experiments, and `numerics.md`'s suite of settings elements is
    a ladder.
  - **When two toolkits agree:** the first experiment's two checks stand: the same effective member, and a difference
    between the rules that falls with the level. A tolerance from a ladder of method-only settings at fixed nodes is
    deferred until later.
  - **The layout:** approved. `schemas/` keeps the families, the experiments and the checker; the Rosetta Stones move to
    `rosetta/`, and the adapters with the toolkit registry to `harness/`. The move is to be one commit with nothing else
    in it.
  - **The environments:** lock files from the start, one for each toolkit.
  - **Large outputs:** the Jacobians' matrices are kept out of git for now. The results file's hashes are the record.
  - **The spelling of names:** the experiment file's underscores, following the schemas' keys, approved. Whether the
    ontology's names keep their hyphens is still open.
- **10:33:51, memorialize.**
- **10:39:40, the layout's move:** go ahead, as approved at 10:33:47. Made as commit `9675109`, with nothing else in it.
- **11:23:59, the runner:** go ahead with the plan's second stage, the registry, the lock files and the runner. Built
  and accepted by 11:30 ([the findings](../findings/2026-11-02_harness-acceptance/README.md)).
- **18:24:32, memorialize.** Not a push: pushing stays the owner's to approve.
- **18:28:43, what the harness gives a toolkit.** Parameters, not methods or settings. The runner as built passes a level
  number that the adapters' shared code turns into grids, nodes and tolerances, and hands both toolkits the same nodes,
  grids and population method; a departure from the ruling, to be undone ([`harness.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/harness.md)).
- **19:09:13, what the harness asks.** The buffer-stock target; the ergodic distributions of m or a and of permanent
  income, and the joint distributions an economy of these consumers generates, from which population-wide E[c],
  E[u′(c)], E[a] and E[m], and perhaps their log variances, are computed. The shared code must not insist on one
  representation of the shocks: the true model has truncated lognormals, which each toolkit represents as it likes,
  discretized, continuous or otherwise. He asked for discussion before anything was built.
- **19:17:06, mortality.** The owner was inclined to rule that the framework require a mortality probability sufficient
  to guarantee a stationary distribution of permanent income. Put to him: existence needs only ℒ < 1, but the stationary
  distribution has power-law tails, so the moment of order k exists exactly when ℒ𝒢^k E[ψ^k] < 1 with newborns at
  𝐩 = 1 (ℒ E[ψ^k] < 1 with newborns at the trend); which tail binds, and what 𝒢 means, turns on where newborns enter;
  BST's annual calibration needs ℒ < 0.971 for a finite mean at 𝐩 = 1 and gives E[𝐩] = 33 at ℒ = 0.97, while the toy
  passes everything asked but the variance (factor 1.0005). Four decisions were put with recommendations.
- **21:00:56, the four decisions,** all as recommended:
  1. the newborn's permanent income is a member-level choice, `one` or `trend`; the toy at `one`, the restrained-limit
     members at the trend;
  2. validity: ℒ < 1, and ℒ𝒢 < 1 at `one`; the variance and the marginal-utility conditions are domain rules with
     statuses;
  3. the restrained-limit members' ℒ gives a tail exponent of at least 2 with 𝒢 = 1.03 kept: ℒ = 0.98 proposed
     (exponent 2.57; ℒ = 0.99 sits on the variance's boundary);
  4. the name: the stationary income condition, SIC, with its moment conditions SIC(k).
- **21:16:02.** The owner asks what SIC stands for. Answered: the stationary income condition, its factor ℒ𝒢 at `one`
  and ℒ at the trend, no patience term in it, unlike the GIC-Liv; and the alternative name SPIC.
- **21:24:16.** The owner chooses **SPIC, the stationary permanent income condition**, with its moment conditions
  SPIC(k); the documents were renamed at once. He asks whether it needs to be added to core BST; the answer given is in
  the journal.
- **21:28:43.** The owner: add the SPIC to econ-ark's notation registry. Done on branch `notation-v8.1-spic` of
  econ-ark-tools, commit `68a242d7`, unpushed: version 8.1.0, the row `stationary-perm-inc-factor` with `\SPIFac` = ℒ𝒢
  (ℒ at the trend), the defined term, the changelog. The registry quotes his words of the evening, as its rows do.

  Consequences, written into the documents the same evening as a proposal ([`bst/conditions.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/bst/conditions.md),
  [`bst/results.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/bst/results.md), [`bst/model.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/bst/model.md), [`experiments.md`](../../experiments.md),
  [`harness.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/harness.md)): every member carries `newborn: {permanent_income: one | trend}`, so every hash
  changes; BST's baseline and `library` (the same model as `bst-p-zero-0.005`, hash `b2e365cd…`) are out as written,
  `library` retired; the restrained-limit experiment's four members take ℒ = 0.98 at the trend and the experiment its
  second version, with the hand run of 2026-11-01 as the first version's record; the results schema gains the economy
  in levels with the joint as weighted points out of git; the check `same_effective_member` goes, replaced by each
  toolkit approaching the stated member and the pair agreeing within their own convergence.

  **Superseded on 2026-11-03** ([the rulings of 2026-11-03](2026-11-03_harness-decisions.md)): the owner removed the
  SPIC requirement, and with it the decisions of 21:00:56 and every consequence above but the representation left to
  each toolkit, the distribution of permanent income reported behind a status, the joint, and the checks that
  replaced `same_effective_member`.

**What stays open:**
- whether the ontology's names keep their hyphens, as econ-ark's notation registry has them, or take underscores;
- three fixes offered at 09:27 and not yet taken up:
  - a section in dolo's stone saying it names none of the ontology's terms;
  - HARK's departures from the schemas gathered into one list;
  - the Rosetta README's list of what is not yet written;
- the toy-hafiscal estimation, a smaller fourth rung, `library` against v0.1, and the push, as on 2026-11-01.
