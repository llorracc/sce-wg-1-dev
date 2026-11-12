# Plan: fewer branches and worktrees in the fork

**Status: PROPOSED on 2026-11-12, on the owner's request of that morning; its first step begun on his word at 11:03
that day, the fork's pull request #16 merged with a merge commit (f557ef4), its branch not yet deleted. Nothing else
in it is done.** Every step that
merges, closes a pull request, deletes a branch on GitHub or makes a tag waits on his word.

## What there is

Read on 2026-11-12 between 09:02 and 09:05 EST, after a fetch of the fork and of the working group's repository.

- **Ten worktrees** on jhu-dell: the clone's own folder and nine under `.worktrees/`. All are clean, with nothing
  uncommitted and nothing untracked.
- **Seventeen local branches,** and **nineteen on the fork,** five of which have no local copy.
- **Ten open pull requests** hold some of them: seven in the working group's repository, from branches of the fork,
  and three in the fork.

Every branch falls in one of six groups.

| group | branches | where | state |
|---|---|---|---|
| **Live work** | `reference-as-its-own-kind`; `status-reader`; `stone-method-files` | the first pushed, with the fork's pull request #16 open and its checks passing; the other two local | not in main; the three merge together without conflict; a worktree each |
| **Heads of the working group's open pull requests** | `exact-definition` (#14), `ontology-probability-distributions` (#15), `apparatus` (#16), `ontology-buffer-stock-models` (#17), `shock-laws-and-stones` (#18), `experiment-and-record-schemas` (#19), `harness-core` (#20) | local and on the fork | every commit already in the fork's main; open there since 2026-11-04, unreviewed; one worktree, `harness-core` |
| **Merged, with no pull request** | `comparator`; `stone-convention` | the first local and on the fork, the second local | every commit in main; a worktree each |
| **The model's work of October** | `buffer-stock-schema-work_CDC`; `stage-derivative-terms` (the fork's #15); `markov-results` (the fork's #14) | local and on the fork | superseded on 2026-11-04, when the model moved to its own repository; two worktrees |
| **Copies of the working group's branches** | `github-forms`, `meeting-slides-forms`, `migrate-wg1-site`, `semantic-ontology-slides`, `register-toolkit-template` | on the fork only | the working group's repository holds each in full |
| **The two that stay** | `main`; `buffer-stock-ontology`, which is the records branch | local and on the fork | main pushed; the records branch 56 commits ahead of the fork, its push held |

Three facts that the steps rest on:
- **The fork's main is 45 commits ahead of the working group's main.** The seven pull requests there carry the
  first seven of those; 38 commits made since are in none of them: the comparator, the stone convention's revision
  and what followed.
- **The seven would merge there in their order,** the first six cleanly; the seventh then conflicts in one file,
  `.gitignore`, which the fork's main has already resolved.
- **One commit of October is in no branch that stays:** `markov-results` holds the first version of the Markov
  family's results schema (dcb3bb4), which left this repository with that family on 2026-11-04. The other two
  October branches are wholly inside the records branch.

## The steps, in order

Each step is safe to stop after. A step marked *his word* needs it; the others remove only local copies of what the
fork or main already holds.

- **Merge the live work.** *His word.* Merge the fork's pull request #16, with a merge commit as the fork's merges
  have been and not a squash, so that the commit a model repository pins stays in main's history: the perfect-foresight repository's main pins
  6c12de1 by its hash since 2026-11-12, so until the merge that branch is neither rebased nor deleted on the fork. Then push `stone-method-files` and
  `status-reader` and open a pull request for each into the fork's main, so that the checks run on them as they did
  on #16, and merge them. Afterwards delete the three branches, locally and on the fork, and remove their worktrees.
- **Drop the local copies of the working group's seven heads.** Delete the seven local branches and the
  `harness-core` worktree. The fork keeps the seven, since deleting a pull request's head closes it.
- **Drop the two merged branches.** Delete `comparator` and `stone-convention` locally and remove their worktrees.
  *His word* for deleting `comparator` on the fork.
- **Retire October's work.** *His word.* Close the fork's pull requests #14 and #15 with a sentence saying where
  the work went. Keep the one stray commit under a tag, `archive/markov-results`. Then delete the three branches,
  locally and on the fork, and remove the two worktrees.
- **Drop the fork's copies of the working group's branches.** *His word.* Delete the five on the fork. Nothing is
  lost, since the working group's repository has each.
- **Settle the records branch.** *His decision, below.*
- **Bring the working group's repository up to the fork.** *His word, there.* Merge the seven pull requests in
  their order, resolving `.gitignore` at the seventh; open one pull request from the fork's main for everything
  since; when it merges, delete the seven heads on the fork.

## What it leaves

| | now | after the steps in the fork | after the working group's repository catches up |
|---|---|---|---|
| worktrees | 10 | 2: the records branch and main | 2 |
| local branches | 17 | 2 | 2 |
| branches on the fork | 19 | 9: main, the records branch, the seven heads | 2 |
| open pull requests | 10 | 7, all in the working group's repository | 0 |

From then on a piece of work is one branch off main with one worktree, a pull request into the fork's main, and the
branch and worktree deleted when it merges.

## Decisions

- **Whether to merge #16 now.** Recommended: yes. Its checks pass, an independent review found no defect in its main
  paths, and the perfect-foresight repository's pin names its commit.
- **How the other two live branches reach main.** Recommended: a pull request each, as for #16, so that the fork's
  checks run before the merge. The alternative is a local merge and a push of main, as was done until now.
- **What becomes of the stray Markov commit.** Recommended: a tag on the fork, which costs nothing and keeps it
  findable. The alternative is to confirm first that the repository the family moved to holds it, and then let it go.
- **Where the records live.** The records branch began as the branch of the ontology of buffer-stock models and
  kept that name. Beside the records, 288 files, it still carries about 70 files of the model as it stood at the
  split, nearly all of which the model's own repository has since continued, so they are stale copies here; two
  documents are on this branch alone, the plan for upstreaming and the registry's design. The project's
  instructions file is on this branch and not on main, so a clone at main does not have the memory.
  - *Recommended now:* keep the records on a branch of their own, renamed `records`, and remove from it the stale
    copies of the model, after an inventory that keeps whatever is here alone. The rename on the fork waits on the
    hold on this branch's push.
  - *The alternative:* move the records and the instructions file onto main, so that every clone has them, and
    retire the branch. It makes the records part of what a pull request from main would carry to the working group's
    repository, unless they are left out there.
- **Whether the seven pull requests in the working group's repository stand.** Recommended: merge them as they are,
  in their order, and follow with one pull request for the rest; they are small and were cut to be read one at a
  time. The alternative is to close the seven and open one from the fork's main, which carries everything at once
  and is larger to read.

## What it does not touch

The hold on the records branch's push; the model repositories; the pins those repositories hold on the fork's
commits, which stay reachable whatever branch is deleted once main contains them.
