---
name: feedback_upstream-series-tracks-main
description: "Merged on 2026-11-16, the working group's repository then equal to the fork's main. The working group's open pull requests were kept as a series that, merged in order, brings econ-ark/sce-wg-1 to the fork's main file for file, each part comprehensible on its own; when main moves, the series is brought along"
metadata:
  type: feedback
---

The pull requests from the fork to the working group's repository, econ-ark/sce-wg-1 #14–#20 and #22, are a series. Merged in
their order, they bring that repository to the fork's main file for file, each pull request one comprehensible part,
so the work never arrives as one commit holding everything. When the fork's main moves, each pull request's head is
brought to main's version of its own files.

**Why:** the owner's purpose for the series, stated on 2026-11-14 at 10:12:36 ([the rulings](../rulings/2026-11-14_core-fixes-ontology-held-and-the-series.md)):
the working group reads the work as parts it can review.

**How to apply:**
- Update a head by a commit that checks out main's version of its files, or by merging the branch it is stacked on:
  #17 on #15, #20 on #19. Never rebase or force-push. Push the heads to the fork. Opening, merging or closing a pull
  request in the working group's repository needs his word each time.
- Check by merging the heads in the series' order onto the working group's main with `git merge-tree --write-tree`,
  chained with `git commit-tree`, and comparing the result's tree with main's. Then run the core's and the ontologies'
  tests on the result.
- Two pull requests appending to the same end of one file always conflict. Give each part its own file, as
  `core/.gitignore` does for the core, rather than stacking unrelated parts.
- A file on main that no pull request carries is a gap. The site's deploy job was one until #22 opened on
  2026-11-16.
- Each description's series sentence names the fork's main at its last check and the tests on the result; keep it
  current when main moves, on his word.
- **Done on 2026-11-16:** all eight merged by 23:23:40, the working group's main (bc8596b) then the fork's main
  (495817f) file for file, and their branches deleted from the fork. A later series follows the same practice.
- **A later change goes to the fork first, then to the working group** (as #30, then #23, on 2026-11-16 and 17). The two
  mains hold the same files through different merge commits. So before opening a fork branch there, merge the working
  group's main into it with an ordinary merge commit, which leaves its tree unchanged. Otherwise GitHub diffs from an
  older common ancestor and lists every file of the series.
- They go in order, #14 first, then #16, then the rest, #22 last. On 2026-11-16 he named his own second account,
  ccarrollATjhuecon, as the reviewer, and had each reviewed from it and merged: #14 and #16 that night, the rest under
  way. For each: read the diff, check that the branch merges cleanly onto the group's main, run the tests on the tree it
  makes where its checks did not run, mark it ready, request the review, post the approval from that account (switching
  `gh` to it and back to llorracc in one command), saying what was checked and that it was generated with Claude Code,
  then merge with a merge commit and check the series again.
- Related: [[feedback_merge-commits-keep-pins]], [[project_state]].
