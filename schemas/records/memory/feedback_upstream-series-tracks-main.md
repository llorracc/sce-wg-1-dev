---
name: feedback_upstream-series-tracks-main
description: "The working group's open pull requests are kept as a series that, merged in order, brings econ-ark/sce-wg-1 to the fork's main file for file, each part comprehensible on its own; when main moves, the series is brought along"
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
- All of them are drafts, marked not ready to be merged. They go to the group, not merged by him (2026-11-16): once the
  fork's main is quiet, #14 is marked ready first, with a reviewer he names, then #16, then the rest in order, #22
  last.
- Related: [[feedback_merge-commits-keep-pins]], [[project_state]].
