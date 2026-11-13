# Plan: fewer branches and worktrees in the fork

**Status: EXECUTED in the fork on 2026-11-13 by 13:14, on the owner's word of 12:58:33 to pursue its recommendations,
after his release of the records branch's hold at 12:58:10; what remains is the working group's repository, whose seven
pull requests wait on whether he merges them or puts them to the group first. The two questions the execution raised
were settled on his word at 14:53:27: the records branch holds the records alone (72231b2), and the fork's deploy job
runs only in the working group's repository, by pull request #20 ([the journal](../journal/2026-11-13_session-record.md)). PROPOSED on 2026-11-12, on the owner's request of that
morning; REVISED at 15:47 EST the same day, on his second request, against the state read then.** Done so far: the fork's pull request #16 merged with a merge commit
(f557ef4) on his word at 11:03; its branch is not yet deleted on the fork. **Clearing locally DONE** on his word at
17:02:06, by 17:02:29: five worktrees removed and twelve local branches deleted, none forced; six of each remain
([the journal](../journal/2026-11-12_session-record.md)). Every step that merges, closes a pull request, deletes
a branch on GitHub or makes a tag waits on his word. The revision adds the fourth branch of live work,
`experiment-metrics`, the model repository's link to an October commit, the inventory of the records branch, and a
correction: the checks a pull request runs in the fork build the website; they do not run the core's tests.

## What there is

Read on 2026-11-12 between 15:30 and 15:47 EST, after a fetch of the fork and of the working group's repository.

- **Eleven worktrees** on jhu-dell: the clone's own folder and ten under `.worktrees/`. All are clean: nothing
  uncommitted, nothing untracked, no stash. No session or process other than this session's has its directory in
  any of them.
- **Eighteen local branches,** and **nineteen on the fork,** five of which have no local copy. No tags.
- **Nine open pull requests:** seven in the working group's repository, from branches of the fork, and two in the
  fork.

Every branch falls in one of six groups, and each group gets one treatment.

| group | branches | state | treatment |
|---|---|---|---|
| **Live work** | `stone-method-files` (2 commits); `status-reader` (2); `experiment-metrics` (1) | local only, not in main; a worktree each | merge into main, a pull request each |
| **Merged, the branch now redundant** | `reference-as-its-own-kind` (merged by #16); `comparator`; `stone-convention` | every commit in main; the first two also on the fork, the third local; a worktree each | delete |
| **Heads of the working group's open pull requests** | `exact-definition` (#14), `ontology-probability-distributions` (#15), `apparatus` (#16), `ontology-buffer-stock-models` (#17), `shock-laws-and-stones` (#18), `experiment-and-record-schemas` (#19), `harness-core` (#20) | every commit in the fork's main; open there since 2026-11-04, unreviewed; one worktree, `harness-core` | delete the local copies; keep them on the fork until the pull requests are settled |
| **The model's work of October** | `buffer-stock-schema-work_CDC`; `stage-derivative-terms` (the fork's #15); `markov-results` (the fork's draft #14) | superseded on 2026-11-04, when the model moved to its own repository; two worktrees | close the two pull requests, tag what would otherwise be lost, delete |
| **The fork's copies of the working group's branches** | `github-forms`, `meeting-slides-forms`, `migrate-wg1-site`, `semantic-ontology-slides`, `register-toolkit-template` | on the fork only; the working group's same-named branch holds each in full | delete on the fork |
| **The two that stay** | `main`; `buffer-stock-ontology`, the records branch | main pushed; the records branch 62 commits ahead of the fork, its push held | main as it is; the records branch renamed and slimmed, on his decision below |

## The facts the steps rest on

- **What the model repositories reference stays reachable.** The buffer-stock model's repository pins the core at
  7679b48 and links the stone convention at 359fb78, both in main; its ontology's `source.yaml`, and the JSON and
  Turtle generated from it, name `tree/d8f65e2`, the head of `buffer-stock-schema-work_CDC`, which is not in main and
  is reachable on the fork only through the records branch. The perfect-foresight repository pins 6c12de1 and
  7679b48, both in main.
- **The three live branches merge into main without conflict,** one after another in the order of the steps. They
  touch five files in common (`apparatus.md`, `vocabulary.md`, `core/README.md`, `core/wg1core/__init__.py`,
  `core/wg1core/runner.py`), and git merges each cleanly. `stone-method-files` and `status-reader` were cut from main
  before #16; a merge commit takes them as they are, with no rebase.
- **A pull request in the fork does not run the core's tests.** The fork's one workflow, `publish.yml`, builds the
  website (`primer`, `wg1`, `assemble`; `deploy` skipped on a pull request); those were the checks that passed on #16.
  The core's tests are run locally on the merge before each merge, whichever way a branch reaches main.
- **The working group's seven pull requests merge there in their order,** the first six cleanly; the seventh then
  conflicts in one file, `.gitignore`, which the fork's main has already resolved. The fork's main is 48 commits ahead
  of the working group's main, 41 of them (25 not merges) beyond the seven.
- **One commit of October is in no branch that stays, and in no other repository found:** `markov-results` holds the
  first version of the Markov family's results schema (dcb3bb4, 1,623 lines across eight files). Neither the
  buffer-stock model's repository nor HAFiscal's clones on this machine have it. `buffer-stock-schema-work_CDC` and
  `stage-derivative-terms` are wholly inside the records branch, locally and on the fork.
- **What the records branch carries besides the records.** It has 389 files that main lacks: the 295 records, and 94
  others. Of the 94, 80 are in the buffer-stock model's repository at the same path, continued there since the split
  (the instructions file among them, under the same name, with that repository's own content), and 8 are on main
  under the same name at another path. Six are nowhere else: `schemas/upstreaming.md`, the plan for the pull requests
  upstream; `project-a/exact-definition.md`, the applied proposal of the purpose's amendment, whose result main holds;
  the QuantEcon JAX stone's two files, which the model repository's QuantEcon EGM stone succeeded; and
  `harness/test_runner.py` with its stub adapter, which the core's tests on main replaced.

## The steps, in order

Each step is safe to stop after. A step marked *his word* needs it; the first removes only local copies of what main
or the fork already holds.

- **Clear away what is merged, locally.** Delete the local branches `reference-as-its-own-kind`, `comparator`,
  `stone-convention`, the seven heads, `buffer-stock-schema-work_CDC` and `stage-derivative-terms`, and remove the
  worktrees `reference-kind`, `comparator`, `stone-convention`, `harness-core` and `stage-derivative-terms`. Before
  each deletion, check again that the branch is in main or on the fork; `git branch -d` refuses a branch it cannot
  find merged, and that refusal is kept, never forced. Eleven worktrees become six, eighteen branches six.
- **Merge the live work.** *His word, for each.* Push the branch, open a pull request into the fork's main, run the
  core's tests on the merge locally, and merge with a merge commit (`gh pr merge <n> --merge -R llorracc/sce-wg-1-dev`).
  Then delete the branch, locally and on the fork, and remove its worktree. In this order:
  `stone-method-files`, three documents, the smallest; `status-reader`, the core's reader for REMARK's status table;
  `experiment-metrics`, the metrics an experiment defines, with the registry schema's eighth draft. The buffer-stock
  session's four further points on metrics stay deferred: none of them is needed for the merge.
- **Delete the two merged branches on the fork.** *His word.* `reference-as-its-own-kind` and `comparator`. The
  deferred upstream pull request for the comparator can be cut from f0c8f14 in main's history whenever it is wanted.
- **Retire October's work.** *His word.* Tag `archive/markov-results` at dcb3bb4 and `archive/buffer-stock-schema-work`
  at d8f65e2 and push both tags, so that the stray commit and the model repository's link outlive any branch. Close
  the fork's pull requests #14 and #15, each with a sentence saying where the work went, before deleting #15's base.
  Then delete the three branches on the fork, the local `markov-results`, and its worktree.
- **Delete the fork's copies of the working group's branches.** *His word.* The five. Nothing is lost.
- **Settle the records branch.** *His decision, below;* its part on the fork waits on the hold.
- **Bring the working group's repository up to the fork.** *His word, there.* Merge the seven pull requests in their
  order, resolving `.gitignore` at the seventh; open one pull request from the fork's main for everything since; when
  it merges, delete the seven heads on the fork.

## What it leaves

| | now | after clearing locally | after the steps in the fork | after the working group's repository catches up |
|---|---|---|---|---|
| worktrees | 11 | 6 | 2: the records branch and main | 2 |
| local branches | 18 | 6 | 2 | 2 |
| branches on the fork | 19 | 19 | 9: main, the records branch, the seven heads | 2 |
| open pull requests | 9 | 9 | 7, all in the working group's repository | 0 |
| tags | 0 | 0 | 2, the archives | 2 |

From then on a piece of work is one branch off main with one worktree, a pull request into the fork's main merged
with a merge commit, and the branch and worktree deleted when it merges.

## Decisions

- **How the three live branches reach main.** Recommended: a pull request each, as for #16, for the review page, the
  website's build and a merge commit made by GitHub; the core's tests run locally either way. The alternatives: one
  pull request for all three, which merge cleanly together but are three separate things to read; or local merges and
  a push of main, as before #16.
- **What becomes of the stray Markov commit.** Recommended: the tag. No other repository found has its content, and
  a tag costs nothing.
- **Where the records live.** The records branch began as the branch of the ontology of buffer-stock models and kept
  that name. The project's instructions file is on it and not on main, so a clone at main does not have the memory.
  - *Recommended:* keep the records on a branch of their own, renamed `records`, and remove from it the 88 files that
    the model repository or main holds, keeping the six found nowhere else (the two test files and the superseded
    stone can go, since history and the archive tag keep them; the plan for upstreaming and the applied proposal
    stay as records). The local part can be done at any time; the rename and push on the fork wait on the hold.
  - *The alternative:* move the records and the instructions file onto main and retire the branch. Every clone would
    have the memory, but every pull request from main to the working group's repository would carry about 300 files
    of the fork's records unless they were cut out there, and the records' push would still wait on the hold.
- **The hold on the records branch's push** ([the deferred items](../deferred.md)). The HAFiscal session holds one
  fact on his word in its session and asked him on 2026-11-05 whether the hold reaches the HARK session's measurement
  of the same thing, which the records carry. His answer, release or hold, unblocks the records branch's 62 commits
  and its part of this plan; a hold means rewriting the unpushed commits, to be proposed to him first.
- **Whether the seven pull requests in the working group's repository stand.** Recommended: merge them as they are,
  in their order, and follow with one pull request for the rest; they are small and were cut to be read one at a
  time. The alternative is to close the seven and open one from the fork's main, which carries everything at once
  and is larger to read.

## What it does not touch

The model repositories; the commits they pin, which stay reachable since each is in main or under a tag; the other
sessions' clones.
