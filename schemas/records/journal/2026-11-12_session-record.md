# Journal of 2026-11-12

Times are EST, from the clock, the transcript or git.

- **08:59:20, the owner's word here: the push.** The branch `reference-as-its-own-kind`, the reference as an object
  of its own in the core, built overnight and reviewed ([the journal of 2026-11-11](2026-11-11_session-record.md)),
  is pushed to the fork at 08:59, its head 6c12de1 on GitHub as it was tested. The perfect-foresight session is
  told the commit and the address of the pin; what it does on it is on his word in its own session.
- **By 09:00, his word here for a pull request to merge the branch.** Opened in the fork, from the branch into the
  fork's main: [#16](https://github.com/llorracc/sce-wg-1-dev/pull/16), open, not a draft, mergeable, its two checks
  pending when read at 09:00. Its base is the fork's own main and not the working group's repository, whose main
  holds no core until the pull requests open there are merged. Merging it is his.
- **09:02, the pull request's checks pass,** the fork's three jobs, the core's tests among them. *Corrected at
  17:03: the three jobs, `wg1`, `primer` and `assemble` of `publish.yml`, build and check the website; none runs the
  core's tests, which were run locally.* On his word it is
  opened in his browser.
- **By 09:02, his request for a plan to consolidate the fork's branches and worktrees;** written by 09:06 as
  [a proposed plan](../plans/2026-11-12_branches-and-worktrees.md), nothing in it done. Read for it, after a fetch:
  ten worktrees, all clean; seventeen local branches and nineteen on the fork; ten open pull requests, seven of them
  in the working group's repository from the fork's branches. Of the branches, nine are wholly in main already,
  three are October's work on the model, superseded when the model moved to its own repository, five are the
  fork's copies of the working group's own branches, three are live work, and two stay. The plan would leave two
  worktrees and two local branches, with the working group's seven pull requests the last to go.
- **The perfect-foresight repository's main pins the pushed commit by its hash; reported here by 09:14.** As its
  session reports: it found the commit on GitHub at 08:59:53, its locks held against GitHub, it made its
  experiment's second version's run of record with all five checks passing, and its main was pushed at 09:03 with
  its continuous integration passing. Its pin rests on the branch `reference-as-its-own-kind` until that branch is
  in the fork's main. So the branch stays on GitHub as it is, neither rebased nor deleted, until the merge, and the
  merge is a merge commit, which keeps the pinned commit in main's history
  ([the plan](../plans/2026-11-12_branches-and-worktrees.md) says so).
- **11:00, his question whether #16 is ready to merge.** Read on GitHub then: open, not a draft, mergeable and
  clean against the fork's main at 7a4889f, its head still 6c12de1, its three checks passing; main is not protected
  and requires no review; the fork allows a merge commit, a squash and a rebase, of which the pinned commit needs
  the first. Answered that it is.
- **10:33:47 and 10:59:42, in the perfect-foresight repository's session; relayed here and checked by 11:01.** He
  holds that no metric is the default and that which metric, or which several, is the user's to define, and he has
  that session propose to this one that an experiment may define a metric of its own. Both typed by him. What he
  approved there is the proposing; building it is on his word here. That session's proposal: a map of named
  metrics in the experiment, each a pointwise distance with an aggregate, a largest, a mean, a root mean square or
  a quantile, optionally weighted, the three metrics the core has now being such pairs with the largest as
  aggregate and keeping their names; a function of the model repository as a further way to define one, its file's
  hash recorded; a reference's errors and the checks naming a defined metric as they name the three; the report
  stating each definition. Its occasion: in that repository a uniform small shift of a rule became, under the
  metric relative to the reference, a large distance at the single point nearest the limit, where an average over
  the points was what he asked for and the core has none. Put to the owner here with this session's
  recommendations, and not built ([the deferred items](../deferred.md)).
- **11:02:56, the owner's word here: the merge.** Pull request #16 is merged into the fork's main at 11:03 with a
  merge commit, f557ef4, whose parents are the earlier main and the branch's head, so the commit the
  perfect-foresight repository pins is in main's history; the merge adds no change of its own. The core's
  thirty-four tests pass on main. The branch is still on the fork, not deleted. The other two live branches still
  merge into the new main without conflict. The perfect-foresight session is told; moving its pin to follow main is
  on his word there. This is the first part of the first step of
  [the plan for the fork's branches](../plans/2026-11-12_branches-and-worktrees.md).
- **11:05:21, the owner's word here: the metrics an experiment defines,** the declarative ones as this session
  described them and the function of the model's repository as well. Built by 11:12 on the local branch
  `experiment-metrics` (09a4548), off the fork's main, unpushed and unmerged.
  - **The experiment schema** takes `metrics`, a map from a name to a definition. A definition is a pointwise
    distance, the absolute difference, the earlier relative one, or the one relative to the reference with its
    floor, with an aggregate, the largest, the mean, the root mean square or a quantile; or a function of the
    model's repository, by its file and name, with the file's hash and parameters. A check, a reference quantity
    and a reference's errors name a defined metric as they name the core's three, whose names are reserved.
  - **A new module of the core** holds the three as such pairs with the largest as aggregate, so that there is one
    path, and loads a function once its file hashes as stated. The checker of experiments reads a function's file,
    checks its hash and that it defines the function, and runs nothing; the comparator imports and runs it.
  - **The registry schema's eighth draft:** a record names its largest distance's metric by any metric's name.
    Records of the seventh draft validate under it.
  - **The documents:** a section on metrics in the experiments' document, which says that no metric is the
    default; the core's README and the vocabulary.
  Decisions taken in building it, each his to change: a function's file is pinned by its hash in the experiment, as
  a member's files are, where the proposal had the hash only recorded; a quantile takes no interpolation and reads
  its fraction as the decimal written; a defined metric refuses a value that is not a number wherever it is used;
  where the largest pointwise distance sits is reported for every aggregate; a bare error is shown under the
  absolute metric and the earlier relative one and never under a defined metric; no weights by point.
- **Tried.** The core's tests pass, forty-two: main's thirty-four, one assertion on the draft's number loosened,
  and eight new ones, with means, root mean squares and quantiles against values computed by hand, the core's
  three against their pairs on random numbers, functions that keep and break the contract, and what the checker
  refuses. Four real runs, the buffer-stock repository's and the perfect-foresight repository's three, compared on
  scratch copies under main's core and under the branch: the comparison's data and every record are identical,
  the report differing in one closing sentence. The branch merges with the two other unpushed branches. No
  independent review was run on this one.
- **The buffer-stock session's view,** asked at 11:06 and received while building. The design covers what its
  experiment and its proposed reference comparison name; the quantile is right for it. It asks for more, none of it
  built and all put to the owner: a definition naming companion quantities that the metric also receives, such as
  the comparison points and a distribution's ordinates, which would give weights by where households are and
  regions stated in the points' own values; a declarative region; `at` reported as a type and a point, not only an
  index over the flattened numbers; a quantity that one file reports as undefined or not computed giving "not
  compared" with its reason, where today the two files hold different counts of numbers and the comparison is an
  error; and a statement of what a function may import, which is in this build. A function's contract, two lists
  and parameters by name, leaves room for companions as a further named argument. Both model repositories'
  sessions have the branch and the commit.
- **A notice from the HARK-dev session, read at 11:23.** On the owner's word there, the fork branch of HARK's pull
  request 1863, the truncated lognormal, is rebased onto HARK's current main and force-pushed, its code unchanged.
  Neither the old head nor its parent is named anywhere in this fork, on any branch, by a search of both hashes;
  the records cite the pull request by its number. Answered so; nothing changes here.
- **11:42:37, the owner's word here: memorialize.** Every category of the records brought current and committed on
  this branch, unpushed. Written for it: the rulings of [2026-11-09](../rulings/2026-11-09_bellman-dev.md),
  [2026-11-11](../rulings/2026-11-11_registry-method-files-and-kind.md) and
  [2026-11-12](../rulings/2026-11-12_metrics-the-merge-and-the-branches.md), which until now stood only in the
  journals; two findings, [the review of Bellman's changes](../findings/2026-11-09_bellman-dev-review.md) and
  [the core's two changes tried on real runs](../findings/2026-11-12_the-cores-changes-on-real-runs.md); a rule of
  memory, [that the fork merges by a merge commit](../memory/feedback_merge-commits-keep-pins.md), and five more
  lapses added to [the rule on stamps](../memory/feedback_stamps-from-the-clock.md); the project's state; a suspected
  defect of the runner's manifest; and two deferred items, the plan's decisions and the reader's reading of records
  of earlier drafts. The vocabulary's new terms are in `vocabulary.md` on the branches that coin them: the kind and
  the role of a solution on main; the place, the methods addition and the method files on `stone-method-files`; the
  kind of unit and the status table on `status-reader`; the metric on `experiment-metrics`. No report to others
  quotes a result that changed.

**State at the memorial, 11:46 on 2026-11-12.**
- **Running:** nothing of this session's. A tab of the owner's browser shows pull request #16, merged.
- **The fork:** main at f557ef4, pushed. Eleven worktrees, all clean. Local and unpushed: `stone-method-files`
  (2700da6), `status-reader` (74312f9), `experiment-metrics` (09a4548), and this records branch, held. The branch
  `reference-as-its-own-kind` is merged and still on the fork.
- **Elsewhere, as their sessions report:** the perfect-foresight repository's main pins the commit that #16 merged;
  the buffer-stock repository's main holds the method files as ruled. Nothing of this session's is uncommitted in
  another repository.
- **Open with the owner:** the three branches; four further points on metrics; the plan's five decisions; and what
  [the deferred items](../deferred.md) carried from before.

**State at the end of the entry.** The fork's main at f557ef4, pushed, with the reference as an object of its own
merged by pull request #16; its branch still on the fork at 6c12de1, to delete with the plan's other steps on his
word; two local branches unpushed and unmerged, for him to read: `stone-method-files` (2700da6) and `status-reader`
(74312f9); the plan for the fork's branches and worktrees proposed, its first step begun; an experiment's own metrics built on the local branch `experiment-metrics` (09a4548), unpushed and unmerged, with four
further points from the buffer-stock session put to him; this records branch not pushed, held on the HAFiscal session's open question; the
ontology's statement on Bellman's documentation still with him; REMARK's updates merged into its main and not yet
tagged; four changes to the core and one to the record schema's rule on the image proposed, none made.

**After the memorial.**
- **15:43:03, his request again for a plan to consolidate the worktrees and branches,** there being eleven
  worktrees. The plan of the morning revised in place by 15:47 against a fresh fetch
  ([the plan](../plans/2026-11-12_branches-and-worktrees.md)): eleven worktrees, all clean, with no other session in
  any; eighteen local branches, nineteen on the fork, nine open pull requests, no tags. Found in the reading: the
  buffer-stock model's repository names `tree/d8f65e2` in its ontology's source, a commit reachable on the fork only
  through this records branch; the Markov results schema's commit dcb3bb4 is in no other repository found; the
  fork's pull requests run the website's build and not the core's tests (the correction above); of the 94 files this
  branch carries besides the records, the model repository has 80 at the same path, main 8 under the same name, and
  6 are nowhere else.
- **17:02:06, his word here: clear locally,** the plan's first step. Each branch checked again after a fetch, in
  main or on the fork at the same commit, and each worktree clean, its ignored files only caches and virtual
  environments. From 17:02:18 to 17:02:29: the worktrees `reference-kind`, `comparator`, `stone-convention`,
  `harness-core` and `stage-derivative-terms` removed; deleted with `git branch -d` from main's worktree, none
  forced, the local branches `reference-as-its-own-kind` (6c12de1), `comparator` (f0c8f14), `stone-convention`
  (359fb78), `exact-definition` (5a4d160), `ontology-probability-distributions` (c3f3f15), `apparatus` (d1b50b0),
  `ontology-buffer-stock-models` (d329bce), `shock-laws-and-stones` (12e8120), `experiment-and-record-schemas`
  (4912255), `harness-core` (fc5b3ac), `buffer-stock-schema-work_CDC` (d8f65e2) and `stage-derivative-terms`
  (73c063f). Nothing changed on GitHub. Six worktrees and six local branches remain: this records branch, `main`,
  `markov-results`, and the three of live work.
- **By 17:03, his request for this session's recommendations on the plan's four remaining decisions,** given in
  the reply.

**State at 17:05 on 2026-11-12.** The fork unchanged on GitHub: main at f557ef4, nineteen branches, the two open pull
requests in the fork and seven in the working group's repository. Locally six worktrees and six branches. This records
branch 62 commits ahead of the fork, its push held; the plan's revision and this entry uncommitted.

