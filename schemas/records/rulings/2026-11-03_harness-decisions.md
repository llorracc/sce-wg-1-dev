# Rulings of 2026-11-03

The owner's decisions, in substance and by time (EST). His words are kept outside this public repository.

- **04:37:53, the SPIC removed.** The stationary permanent income condition is not to be required of a member. What is
  needed is a way to calculate permanent income inequality, and Lorenz curves give it. This supersedes the ruling of
  19:17:06 on 2026-11-02 and the four decisions of 21:00:56 that served it
  ([the rulings of 2026-11-02](2026-11-02_harness-decisions.md)). Confirmed at 04:51:10 ("Do it") while the revision was
  being made.

  What goes, out of the proposal of the evening of 2026-11-02, none of it yet in a validator, checker, member or
  adapter:
  - the validity conditions ℒ < 1 and ℒ𝒢 < 1, and the moment conditions SPIC(k) with their tail exponents and closed
    forms; `survival` keeps its domain 0 < ℒ ≤ 1;
  - the member key `newborn.permanent_income`, `one` or `trend`: the families keep their newborn at 𝐩 = 1, as they
    had it, and no hash changes;
  - the restrained-limit members' ℒ = 0.98 at the trend: they keep BST's ℒ = 1, and the experiment's second version
    keeps the first's members and request files, changing only its checks and its reports;
  - `library`'s retirement: it stays, the same model as `bst-p-zero-0.005`, as the member table says;
  - the economy in levels, E[𝐂], E[𝐀], E[𝐌], E[u′(𝐂)] and their log variances. These were the assistant's reading of
    the owner's E[c], E[u′(c)], E[a] and E[m] of 19:09:13, which name the normalized quantities whose population means
    the results schema already carries, as GL(1) and marginal welfare; the records of 2026-11-02 are corrected to the
    owner's lowercase;
  - the expectations E[ψ^(−ϱ)] and E[(log ψ)²];
  - the name, its two vocabulary entries, and the notation registry's row `\SPIFac` on the branch `notation-v8.1-spic`
    of the econ-ark-tools clone, unpushed: superseded, to delete rather than push, the owner's call.

  What stays: the rulings of 18:28:43 and 19:09:13 in full, so the adapters' independence and the representation left
  to each toolkit; the checks that replaced `same_effective_member`; and, as the revised proposal, the distribution of
  permanent income in the results schema, required, behind a status, its Lorenz curve GL(p)/GL(1) defined when ℒ < 1
  and ℒ𝒢 < 1, the income measure's own condition, and the joint of (m, 𝐩, c, a) as weighted points, optional, where
  an experiment asks for it. The owner's "perhaps" of 19:09:13, the log variances, is not added: the GL ordinates and
  quantiles determine each distribution, and the joint gives any moment.

- **05:12:27, the Lorenz targets are of levels.** HAFiscal's Lorenz shares of liquid wealth are of wealth in levels,
  a𝐩 across households, not of normalized a; the HAFiscal session is to be asked why. Asked at 05:14, from the
  published code: the wealth variable, its timing and pooling, the wealth-to-income target's denominator, whether the
  newborns' permanent income is dispersed, and the reason. The consequence, to be drafted on the answer by the rule
  that what a results file carries is put to the toolkits first: the results schema reports the distribution of wealth
  in levels beside the distribution of permanent income, so that the targets are read off a results file and an
  experiment's check can name them; the joint stays the harness's check of both.

- **05:19:52 and 05:22:10, the estimation.** The owner asks whether the toy-hafiscal experiment is implemented and
  tested. Answered: no; the member `toy` is solved and verified, the Jacobian interface is approved and measured on no
  member, and the experiment waits on its member, whose three types are HAFiscal's to estimate in its session on his
  word. He says to ask HAFiscal to do it. The estimation is requested of the HAFiscal-Latest session at 05:23, with
  his words and their stamp for that session's relay check, and the specification as [`bst/model.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/bst/model.md)
  states it at `3ef2423`: the model, the three types, the targets, the objective, the prize and the newborn; to deliver
  the member file, the fit and the code's commit, the wealth variable and the denominator of K/Y, and the provenance of
  6.60.

- **17:59:50 and 18:01:14, two families abolished.** `bst-natural-no-point-mass/1` is to be abolished as an
  uninteresting case, and then `bst-zero-infima/1` also. Two families remain, `bst-natural/1` and `bst-artificial/1`.
  Applied the same evening, as the Markov family's retirement was: the folder `bst/other/`, with both families' stage
  files, validators and members (`toy-natural`, `toy-untruncated`), removed from the tree and kept in the history at
  `2ae4c35`; the checker and its tests, the results validator's list of families, the notation and stone checks,
  HARK's adapter tests, the stones, the adapters' README and the families' documents brought to two families; the
  ontology's two family rows retired, its two scenario classes kept and written by no family; the records. The two
  scenarios stay described in [`constraint-scenarios.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/constraint-scenarios.md), which is why the natural
  family requires a point mass at the joint worst income and the artificial one positive floors; a natural member
  without the point mass is now refused with no family to send it to
  ([the finding](../findings/2026-11-03_two-families-abolished.md)).

**What stays open:**
- the toy-hafiscal member's economy, after the HAFiscal session's answer (the finding, with the HAFiscal-Latest repository since 2026-11-04):
  the family's as stated, 𝒢 = 1.0019026 for every household with newborns at 1, which the estimation was told to
  run, or the published first step's, 𝒢 = 1 with growth through the newborns, which the family cannot state without
  a newborn level law with a trend; the owner's to decide;
- the closed forms E[𝐩] = (1 − ℒ)/(1 − ℒ𝒢) and var(log 𝐩), dropped with the condition, which could test a reported
  distribution exactly ([deferred](../deferred.md));
- whether the joint as weighted points is the owner's word; it was put to him on 2026-11-02 and not yet answered;
- whether the ontology's two scenario classes without a family, `natural-without-point-mass` and `zero-infima`, should
  go as well; the owner abolished the families and said nothing of the classes, which say what exists.
