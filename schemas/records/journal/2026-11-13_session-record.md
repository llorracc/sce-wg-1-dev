# Journal of 2026-11-13

Times are EST, from the clock, the transcript, git or GitHub.

- **12:56:19, his question what the hold is.** Answered from the records: the HAFiscal session's hold of
  2026-11-05 on HARK's grid at a binding artificial constraint, the question whether it reaches the HARK session's
  measurements in [the survey](../findings/2026-11-05_hark-markov-route-survey.md), and the push of the records branch
  held since. Since then the mechanism had become public twice, in HARK's stone from 2026-11-01 and in econ-ark/HARK#1871
  on his word on 2026-11-07, leaving only the bullet's numbers unpublished. The choice put to him: release, or a
  rewrite of the unpushed commits without them.
- **12:58:10, his word here: release.** At 12:59:27 the records branch is pushed, 643c8c6..b42e4b5, 62 commits.
  The handoff bundle on this machine is restored at its path from the retained full version, the blanked version kept
  beside it, and the six hold markers checked absent. The HAFiscal session and the HARK-dev session are told, with his
  words and their stamp. At 13:00:01 the HAFiscal session checks his word as typed and lifts the hold in its records.
  Its own measured error was never in this repository and stays in its private records, with nothing held.
- **12:58:33, his word here: pursue the other recommendations and workflows** this session had described the
  evening before ([the journal of 2026-11-12](2026-11-12_session-record.md)). Done under it, in the plan's order:
  - **Tags,** pushed by 13:00: `archive/markov-results` at dcb3bb4, the Markov family's first results schema, in no
    other branch or repository found; `archive/buffer-stock-schema-work` at d8f65e2, the commit the buffer-stock model's
    ontology names as its source.
  - **The fork's two October pull requests closed** without merging, each with a sentence saying where the work went:
    #14 at 13:00:07, #15 at 13:00:09.
  - **Ten branches deleted on the fork** after checking each head is held by main, the records branch, a tag or the
    working group's same-named branch: `markov-results`, `stage-derivative-terms`, `buffer-stock-schema-work_CDC`,
    `reference-as-its-own-kind`, `comparator`, `github-forms`, `meeting-slides-forms`, `migrate-wg1-site`,
    `semantic-ontology-slides` and `register-toolkit-template`. The local `markov-results` and its worktree removed,
    the branch deleted with `-D` after checking that the pushed tag points at its head; `-d` had refused, its fork copy
    being gone and main not holding it.
  - **The three live branches merged into the fork's main,** each pushed, given a pull request, its merge with main
    tested locally with the core's tests, its website checks waited for, and merged with a merge commit; GitHub's merge
    tree identical to the tested one each time; then each deleted locally and on the fork and its worktree removed.
    [#17](https://github.com/llorracc/sce-wg-1-dev/pull/17), `stone-method-files`, opened 13:01:03, 34 tests, merged
    13:03:17 (17403b3). [#18](https://github.com/llorracc/sce-wg-1-dev/pull/18), `status-reader`, opened 13:03:48, 42
    tests, merged 13:06:51 (34f2619). [#19](https://github.com/llorracc/sce-wg-1-dev/pull/19), `experiment-metrics`,
    opened 13:07:21, 50 tests, merged 13:11:27 (8b34952). On main as merged, 50 tests pass; the commits the model
    repositories pin, 6c12de1, 7679b48 and 359fb78, are in main.
  - **Found on the way:** the fork's website workflow has failed on every push to main since at least 2026-11-05, in its
    deploy job alone, because the fork has no GitHub Pages; the build passes. Left as it is, for his word.
  - **The records branch.** The evening's uncommitted records committed first (afacdc6). Then the 91 files of the model
    as it stood at the split removed (0f820f8), keeping the instructions file, `schemas/upstreaming.md` and
    `project-a/exact-definition.md`, which are nowhere else. The 70 links to the removed files, from 20 records and the
    two kept documents, made permanent links to b42e4b5. No record's own link broke. 31 links did break in four of the
    16 files this branch shares with main in older versions (`rosetta/README.md`, `schemas/experiments.md`,
    `schemas/shock-laws.md`, the ontology's README), which remain for his decision. The branch renamed `records`
    locally and on GitHub, where the old name redirects, and pushed at 13:14:26 (b42e4b5..0f820f8).

**State at 13:15 on 2026-11-13.** The fork's main at 8b34952. The clone has two worktrees, the records branch in the
clone's own folder and main under `.worktrees/main`, and two local branches. The fork has nine branches (main,
`records`, and the heads of the working group's seven open pull requests), two archive tags, and no open pull
requests. Open with the owner: whether the working group's seven pull requests are merged by him or put to the group
first; the 16 older shared files on the records branch; the fork's failing deploy job; the status reader's reading of
records of earlier drafts, due since the merges; and what [the deferred items](../deferred.md) carried from before.

## After the report

- **13:17, the report to him,** with four questions: the working group's seven pull requests, the 16 files the
  records branch shares with main in older versions, the fork's deploy job, and the status reader's reading of records
  of earlier drafts; a recommendation on the last three.
- **14:53:27, his word here: go with the recommendations on the second, third and fourth.** The first stays his. Done
  under it:
  - **The deploy job** limited to the working group's repository, `github.repository == 'econ-ark/sce-wg-1'`, a fork
    still building and checking the site. [#20](https://github.com/llorracc/sce-wg-1-dev/pull/20) opened 14:56:12,
    its checks passed, merged 15:00:35 (135069e), GitHub's merge tree the branch's own.
  - **The earlier drafts of the registry schema kept in the core,** in `core/wg1core/schemas/earlier/`, each copied
    from git unchanged: the working group's drafts 4 to 7, draft 7 in its last form (6c12de1), and the harness's
    fork-named draft 4 of the registry and execution-record schemas (5c6961b). A record is validated against the draft
    it names. The reader reports a record as unchecked only where the core does not hold its draft. Read at the model
    repositories' pushed main, from copies in a scratch folder, all 70 records they have registered are valid under
    their drafts: the buffer-stock repository's 20 of draft 6 and 10 of the fork-named draft 4, and the
    perfect-foresight repository's 28 of draft 6 and 12 of draft 7. Neither has a file of runs of record yet.
    [#21](https://github.com/llorracc/sce-wg-1-dev/pull/21) opened 14:59:07; 52 tests passed on its merge with the new
    main; its checks passed; merged 15:01:07 (9fc7d27), GitHub's merge tree the tested one.
  - **Both branches and their worktrees deleted,** locally and on the fork.
  - **The records branch holds the records alone** (72231b2). The recommendation had named the 16 files the branch
    shares with main in older versions. The branch shared 56 more, identical to main's, which would go stale as main
    moves, and the recommendation's reason, a branch of the records alone, covers them. So all 72 were removed, except
    that the guard hook is kept. The branch has its own README and `.gitignore`. The 9 links from the records and the
    plan for upstreaming to removed files are permanent links to 72ee2ee. Six files remain besides the records: the
    guard hook, the `.gitignore`, the README, the instructions file, the plan for upstreaming and the applied proposal.
    One link in the records was broken before and stays so: a finding of 2026-10-18 names a path in a checkout. The
    harness's environments, caches and one run's outputs from before the split, 1.5 GB never tracked, stay in the
    clone's folder, excluded in its local `.git/info/exclude`.
  - **The website workflow on the fork's main passes,** for the first time since at least 2026-11-05: the runs on
    135069e and 9fc7d27 succeeded by 15:04, the site built and checked and the deploy job skipped.

**State at 15:10 on 2026-11-13.** The fork's main at 9fc7d27, its workflow passing. The clone has two worktrees and two
local branches, the records branch in the clone's own folder and main under `.worktrees/main`. The fork has nine
branches, two archive tags and no open pull requests. Open with the owner: whether the working group's seven pull
requests are merged by him or put to the group first, and what [the deferred items](../deferred.md) carried from
before. For the model repositories' sessions: declaring the kind, writing the file of runs of record, repinning the
core.
