# Rulings of 2026-10-22

The owner's decisions, in substance and by time (EDT). His words are kept outside this public repository.

**In econ-ark's notation registry**, given in the econ-ark-tools session and recorded with his words in that repository's
`notation.yml` and `CHANGELOG.md`:
- 07:17 to 08:39, version 5.0.0 (merged 10:26): the ring marks survival-inclusive symbols (β̊ = β ℒ, Þ̊); ε is the Pareto
  exponent and ζ the leisure share; ℘ is the probability of unemployment whatever the income then; R is typeset sans-serif
  and levels bold italic.
- 10:58:30 to 11:17:23, version 6.0.0 (merged 11:39:51): relative risk aversion is ϱ; the survival-inclusive factors are
  named `\DiscFacEff`, `\APFacEff`, `\RPFacEff`, `\GPFacEff`, and `\GPFacLiv` is ℒ Þ̊_𝒢, HARK's `GPFacLiv`, whose
  condition is the GIC-Liv.
- 13:59:19 and 14:00:45, version 8.0.0 (merged 14:18:09), relayed to this session and checked as typed by him: the incomes
  while unemployed are ξ_u, with benefits, and ξ_x, after they expire, in place of ξ_U and ξ_X; the HAFiscal design note's
  passage on the paper's replacement rates is to be fixed; the employment state is j, leaving z to the matching
  elasticity; ℘ is glossed as the probability of unemployment.

**In this session and the others:**
- **10:45:11** (the HAFiscal-Latest session, reported here). A results file records neither the machine's name nor its
  operating system. HARK's adapter already followed this.
- **10:47:07** (question tool). Registry v5.0.0 is taken into the schemas as one draft pull request: Þ̊ and β̊, ε for the
  tail exponents, the glosses of ℘ and `p_worst`, the typeset forms of R and the levels, and "kapital". `bst/1`'s
  unemployment-event label becomes z, resolving e's two meanings. Opened as #9.
- **12:39:05.** #8, HARK's adapter, is taken out of draft.
- **12:41:52.** All four open items: registry v6.0.0 into #9; the HAFiscal design note in the schemas' symbols (𝒢, ϱ, ℒ),
  also in #9 (`a6f06d1`); a tag on HARK's fork at the adapter's pinned commit, asked of the HARK session, where his word is
  needed; and the merge of #8, which this session's permission check refused and left to him.
- **12:56:05.** He merges #8 himself (`0cfe05c0`, 12:56:07).
- **12:56:36.** #9 is merged, after a trial merge onto the branch with #8 passed the checker's 150 tests and the
  adapter's 5: taken out of draft and merged at 12:58:17 (`673405fd`).
- **14:35:13** (question tool). Registry v8.0.0's four rulings are made as one draft pull request, pushed: ξ_u and ξ_x
  everywhere, the stage files' identifiers, the checker's attribute and HARK's adapter included; the HAFiscal design
  note's passage fixed; j for the employment state, `bst/1`'s label included, the same object; and ℘'s last gloss. The
  records are memorialized first.

**After the first memorial (14:37):**
- **14:40:40 to 14:43:21.** The bellman session's checkout of Bellman's repository is to be brought up to date: GitHub's
  main merged into the feature branch it works on. Relayed there, and checked as typed by him; main was already in that
  branch, so nothing was merged (the journal).
- **About 14:48, in the bellman session** (reported here). Matsya's third session on HARK's source runs, once the six
  excerpts of HARK's code are checked against HARK's own files at `4c285e86`. They were, and it ran (the findings).
- **15:11:02** (question tool). `bst/1`'s stage file stays free of any method: it states the Euler equation and not the
  endogenous grid method's lines, so the solution's method is time iteration on `policy.euler.solve`, with a toolkit's
  endogenous grid method named as its handler, rather than `!egm` on a stage rewritten to admit it. In the same answer,
  the fix of the method targets is made as one draft pull request on top of #10, tested, and pushed: both families'
  tables, `numerics.md`, both Rosetta cards, the adapter's method file, and HARK's stone revised for its Markov adapter.
  Opened as #11 at 15:26:33.
- **16:01:39.** #10, then #11, merged in that order: both taken out of draft by this session, #10 merged at 16:02:08
  (`613a9fb`), and #11, moved onto the schemas' branch, at 16:02:43 (`a3f897a`).
- **17:57:03 and 17:57:06.** This memorial, and its push.

Open with him from the afternoon: whether HARK's adapter should keep passing a member's `natural` constraint to HARK as
the stated laws' natural limit (the defects); no member states `natural` yet.

**After the second memorial:**
- **18:06:54.** Four answers:
  - **A `natural` constraint is the toolkit's own:** the toolkit computes the natural borrowing constraint itself,
    rather than receiving the stated laws' limit as an artificial one. This session first read it as each toolkit's
    limit from its own nodes, a change to the checker and `model.md`; the clarification of 18:18:56 below supersedes
    that reading.
  - **The tag:** HARK's fork is tagged at the adapter's pinned commit. Made at 18:07 as `sce-adapter/2026-10-22`,
    through GitHub's interface, and confirmed by the HARK session, which keeps it.
  - **Registering `w3id.org/sce` waits** until the plans mature. It is not to be raised again before a pull request from
    this fork has been merged into econ-ark/sce-wg-1, and even then he expects the answer to be that it is much too
    early ([the memory](../memory/feedback_w3id-not-yet.md)).
  - **What goes to the working group's repository:** he asked for the question to be set out in full.
- **18:07:14.** The merged branches and their worktrees are deleted: the eleven pull requests' branches, on GitHub and
  here. The five branches in the fork from the working group's repository, by its co-chairs, are not this project's and
  were left.
- **18:18:56** (question tool). The clarification: HARK computes the natural borrowing constraint from the lower of the
  unemployment income and the transitory shocks' infimum, with the permanent shock's infimum entering as in the closed
  form, −`ξ_min` `ψ_min`/(ℛ − `ψ_min`). That is the stated member's `a_Nat`, so `natural` keeps meaning `a_Art` =
  `a_Nat`, and the checker and `model.md` do not change. The change is HARK's: its solvers are to read each shock law's
  lower bound, not the lowest discretized node; asked of the HARK session to draft. Until it lands, the adapter keeps
  passing the stated limit, and no member states `natural` (the findings).

**In the evening:**
- **In HARK's window** (reported here by the HARK session): the reading of 18:18:56 confirmed, with the limit from the
  infima HARK's default (reported 19:25:38); "push" for the branch `natural-limit-infimum` (reported 19:47:50); "add a
  tag", `sce-adapter/2026-10-22.2` at its head `11852805` (reported 19:53:34); and "open", HARK's draft pull request
  #1862, opened at 20:18:00.
- **19:17:15.** The records correction `5efba47` is pushed.
- **21:16:42.** HARK's adapter under `natural` is committed and pushed as a draft pull request: #12, opened at 21:17:05.
- **21:21:24.** This memorial.
- **21:22:11 to 21:32:01.** Asked why #12's work sat in a second worktree, and whether it could merge: the memorial
  pushed, then #12 taken out of draft and merged at 21:32:14 (`d240a48`), its branch and worktree deleted.
- **21:32:50 and 21:33:11.** Nothing was left to push; this memorial of the merge, and its push.
- **21:42:05** (question tool, on his "ask me the open questions" of 21:40:05). Four answers: the fork's work goes to
  the working group's repository after dolo's adapter and the first comparison of two toolkits, by an issue to the
  co-chairs proposing a series that starts with the ontology; the next work is the Markov family's results document,
  validator and members, with HARK's adapter extended to its chains; the bellman session is asked to move Bellman's
  truncated-lognormal draft, with the uniform folded in, toward merging and to file the parameter-condition defect, each
  on his word in its window; HARK's #1858 and #1862 stay drafts.
- **About 21:49, in the bellman session** (reported there and here): Bellman's truncated-lognormal draft marked ready
  and merged, which it was at 21:56 with the uniform comparator folded in; and the parameter-condition defect filed as
  an issue in Bellman's repository.
- **21:46:59.** The Markov family's work goes on in collaboration with the HARK and HAFiscal sessions.
- **22:04:28.** The artificial borrowing constraint: the requirement is not that `a_Art` lie strictly above the natural
  limit, but that a relevant artificial constraint, where one exists, does; one no tighter than the natural constraint
  has no effect, so a written `a_Art` equal to the natural limit, such as HAFiscal's 0.0 under lognormal laws, is valid
  and means the natural-constraint member ([the memory](../memory/feedback_artificial-constraint-relevance.md)). This
  memorial follows.

**The Markov family's first pull request:**
- **22:11:25** (question tool, on the proposal after HAFiscal's answers). The family's documents, calibrations and
  members take the paper's published estimates and the exact values of its public replication package, in place of the
  Pandemic paper's defaults; the first results document carries what the paper uses (the wealth statistics by group and
  pooled, the paper's lottery-year MPC, the rule and limits by state, the employment shares and the effective member),
  the targets, W, F, M and the recession's rule waiting; the first members are `toy-as-hafiscal`, `paper-one-group` and
  `paper-published`. Asked how the newborn's income should be stated, he asked what HARK does.
- **22:12:16** (question tool). HARK draws the newborn's permanent income as a lognormal with mean of log
  `pLogInitMean`, so the file states it by its median and the standard deviation of its log, `{median, sd_log}`.
- **22:25:50.** The pull request committed and pushed as a draft: #13, opened at 22:26:18.
- **22:43:40 and 22:43:48.** #13 merged, at 22:44:03 (`2910efe`), and the memorial pushed, after it was replayed on the
  merge (`873fd49`); #13's branch and worktree deleted, as for #12.
- **22:44:50.** This memorial, and its push.
