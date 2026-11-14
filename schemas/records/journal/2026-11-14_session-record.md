# Journal of 2026-11-14

Times are EST, from the clock, the transcript, git or GitHub.

- **09:17:01, his question.** He asked what this session would do if he asked for the safe core fixes and the
  ontology's correction. He got an account of four core fixes in one pull request on the fork and the ontology's
  statement on Bellman's documentation corrected as version 0.1.0-draft.3. Whether to keep the rule that a concept is
  named and never linked was left to him.
- **09:21:16, his word here:** the fixes and the correction made, and the never-linked rule rescinded
  ([the rulings](../rulings/2026-11-14_core-fixes-ontology-held-and-the-series.md)).
- **09:22:02, his question here:** which pull requests are unmerged, what they would do, and whether to merge, retire
  or rework them. The answer compared each of the seven working-group pull requests with the fork's main:
  - #14, #15 and #17 matched it but for a line or two;
  - #16 and #18 had fallen behind main's revisions;
  - #19 and #20 were far behind.

  None had a review or a comment, and the working group's main had not moved since 2026-11-03.
- **09:24 to 10:05, the four core fixes** on the branch `core-small-fixes`, from main at 9fc7d27:
  - **The environment listed with `-z`.** Old and new code hash every environment of both model repositories alike:
    the buffer-stock repository's three and the perfect-foresight repository's two.
  - **Each source's anchors.** The registry file's `anchors` takes a path, BST's as before, or a file per source key.
  - **A signal by its name.** It is named by Linux's numbering for a container. A process the core started and a
    signal killed is now recorded as a signal, as REMARK's `by_signal` does; it was recorded as an exit with a negative
    code.
  - **The sentence on unreported memory kills,** in `schemas/execution-record.md`.

  Five tests were added, each failing on main's code; 57 pass. Committed as 0694471. The auto-mode classifier refused
  the push, so the branch is local.
- **About 09:35, bellman.io found down.** Every page of bellman.io and econ-ark.github.io/bellman/ answered GitHub's
  404, including the four the journal of 2026-11-09 cites. The Pages settings of econ-ark/bellman, a private repository,
  answered `status: built`, `public: true`, `cname: null`. On his request of 09:23 Bellman's development session was
  asked whether the site had been made private again. Its answer, by 09:45:
  - the repository was private while the site was public;
  - the custom domain was removed from the Pages settings after the site's last build, at 11:29 UTC on 2026-11-11, the
    settings last changed at 01:41 UTC on 2026-11-12;
  - the branch `gh-pages` still holds `CNAME`;
  - nothing records that the change was decided;
  - a concept's page, when the site answers, is `https://bellman.io/wiki/<slug>/`.

  The ontology's correction is held on that.
- **10:12:36, his word here:** the series is kept so that the working group's repository takes the fork's content as
  comprehensible pull requests, and the heads are to be updated to serve that
  ([the memory](../memory/feedback_upstream-series-tracks-main.md)). Done by 10:30, each head by commits or merges, no
  rebase and no force:

  | pull request | the change | head |
  |---|---|---|
  | #15 | the `ontologies/` folder's README and `.gitignore` added | 0f944f7 |
  | #16 | the apparatus and the vocabulary brought to main | 0942441 |
  | #17 | the updated #15 merged | 9a09cc5 |
  | #18 | the stone convention's revision and the method files | 9aac359 |
  | #19 | its schemas put in `core/wg1core/schemas/`, where main has them, and brought to main with their documents | 63e730e |
  | #20 | the updated #19 merged, then the core brought to main: the comparator, the metrics, the status reader, the earlier drafts | e527936 |

  #14 needed nothing. The two gaps:
  - **`.gitignore`:** #15 and #20 both appended to its end, so the second would conflict. The core's line moved to
    `core/.gitignore`, on the fork's main by pull request #22.
  - **The site's deploy job,** which no pull request carried, got the branch `deploy-from-the-group-only` (bbd3f1d).

  Merged in the order #14, #16, #15, #17, #18, #19, #20 and that branch onto the working group's main, the series
  reproduced #22's tree exactly, with no conflicts. On the result the core's 52 tests and the ontologies' 37 and 12
  pass. Updated descriptions for the seven were drafted and are not posted.
- **10:34:21, his word here:** merge #22. It is not yet time for pull requests in the working group's repository, so
  the eighth is not opened. #22 was merged at 10:35 with a merge commit, dcd0fa6, its tree the one tested. Merged
  without the eighth, the seven reproduce main except for the deploy job's `if:` line.
- **By 10:55, Bellman's development session reported a tag** made on the owner's word in that session:
  `pinned/main-with-the-forward-record-2026-11-14` in econ-ark/bellman-dev, pushed at 10:54, on 3937a8eb2. That is
  the Bellman commit both model repositories pin, bellman-dev's main with pull request 34 merged. It stood on a branch
  alone that is to be retired, and the tag keeps it fetchable; it is no release. Nothing in the fork pins a Bellman
  commit, so nothing here changes. The pointer is in [the references](../memory/reference_pointers.md).
- **By 11:30, the buffer-stock repository's session asked what it needs to appear in REMARK's status table,** on the
  owner's instruction there to confer. It was answered from the code, with the core's reader run on a scratch clone of
  its main at 539aa8a:
  - `kind: canonical-model` can go in its `REMARK.md` now, and REMARK's main reads it;
  - a catalog entry in REMARK, `private: true`, pinned by a tag, is still to be made, by the REMARK session or the
    owner;
  - the core requires neither containers nor every level of a run of record, and what it must meet is the owner's to
    say;
  - an entry with `mode: markov` would be a problem, since the core's runner records no mode;
  - main's code is unchanged since 9fc7d27;
  - the reader finds no problem on the repository today.
- **12:00:25, his word here:** the core's fixes to be pushed, opened as a pull request on the fork and merged
  ([the rulings](../rulings/2026-11-14_core-fixes-ontology-held-and-the-series.md)). Its merge with main at dcd0fa6
  was built first, and the core's 57 tests pass on it. Pushed at 12:01 and opened as the fork's pull request #23; its
  checks passed (`primer`, `wg1`, `assemble`; `deploy` skipped, as on the fork), and it was merged at 12:03 with a
  merge commit, 2311754, its tree the one tested.
- **By 12:05, #19 and #20 brought to the new main,** under the standing rule
  ([the memory](../memory/feedback_upstream-series-tracks-main.md)):
  - #19 took main's `schemas/execution-record.md` and `schemas/experiments.md`, at 97039e6;
  - #20 merged the updated #19 and took main's `core/`, at 21f2d2a.

  Both were pushed as fast-forwards. Merged in the series' order with the deploy job's branch onto the working group's
  main, the eight reproduce 2311754's tree; without that branch they differ in the deploy job's `if:` line alone. On
  the result the core's 57 tests and the ontologies' 37 and 12 pass. The drafted descriptions of #19 and #20 now name
  the fixes and 57 tests, and all seven name 2311754; none is posted. The worktree `.worktrees/core-small-fixes` and
  the local branch were removed; the fork's branch `core-small-fixes` remains.
- **By 12:06, the perfect-foresight repository's session reported** that the repository pins the core at 9fc7d27 on
  the owner's word there, committed and not pushed. A trial of `closed-form-agreement/3` at that core passes its
  three checks with files identical to the run of record's, and `records.validate` reads its 46 registered records
  as valid. It has not taken the four fixes.

**State at the memorial of 12:15 on 2026-11-14.**
- **The fork's main** is at 2311754, and its `.worktrees/main` is fast-forwarded to it. Two worktrees, `records` and
  `.worktrees/main`, and two local branches.
- **The fork's branches:** the seven heads are updated and pushed. `deploy-from-the-group-only`, and `core-gitignore`
  and `core-small-fixes` (both merged), are on the fork.
- **Open with the owner:**
  - posting the descriptions;
  - the eighth pull request;
  - merging the series himself or putting it to the group;
  - the ontology's correction, once bellman.io answers;
  - who removed the site's domain, a question for Bellman's maintainers or an owner of the econ-ark organization.
