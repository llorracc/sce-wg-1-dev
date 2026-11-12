---
name: feedback_merge-commits-keep-pins
description: "Merge into the fork's main with a merge commit, never a squash or a rebase, and never rebase or delete a pushed branch a model repository pins: the model repositories pin the core's commits by hash"
metadata:
  type: feedback
---

A branch reaches the fork's main by a merge commit. Not a squash and not a rebase, and a pushed branch that a model
repository pins is neither rebased nor deleted before it is merged.

**Why:** a model repository pins the core at a commit's hash. On 2026-11-12 the perfect-foresight repository's main
pinned the head of `reference-as-its-own-kind` within minutes of its push, before the branch was merged, and made its
run of record on it. A squash would have left that commit outside main's history, reachable only while the branch
lived. The owner merged pull request #16 on this session's statement that it would be a merge commit; that the fork's
merges stay merge commits is this session's rule drawn from it, not his words.

**How to apply:** `gh pr merge <n> --merge`, with the repository named, since the fork allows all three ways and
`gh` in a fork may take the parent repository as its target. After a merge, check that the pinned commit is an
ancestor of main. Deleting a merged branch is a step of [the plan for the fork's branches](../plans/2026-11-12_branches-and-worktrees.md),
on the owner's word. Related: [[project_state]].
