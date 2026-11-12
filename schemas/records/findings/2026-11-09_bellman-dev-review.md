# Bellman's changes since the fork last read it: a review

Made on 2026-11-09 between 10:34 and 10:45 EST on [the owner's ruling of that morning](../rulings/2026-11-09_bellman-dev.md),
and repeated on 2026-11-11 at a later commit. Bellman's repositories are private; its documentation is public at
https://bellman.io/ since the evening of 2026-11-08, and what is cited here is public there or is a commit's hash.

## What was compared

- **The base:** `bellman-dev`'s commit `461ee659c`, of the evening of 2026-10-31, when the fork's stage files were
  last checked against Bellman's main.
- **The head:** its main of the morning of 2026-11-09, `2f11e0ddc`, 195 commits later; and on 2026-11-11 the commit
  `930199a`, whose package tree is that of its main of that morning.
- **What the fork takes from Bellman:** its two stage files, `natural.bl` and `artificial.bl`, as the records
  branch holds them; the distribution grammar that the shock laws, the ontology of probability distributions and the
  core's converter write; the 61 concept slugs the ontology of buffer-stock models pins; and the account of
  Bellman's methods in the stone convention.

## How

Read-only, and never with a tool run inside Bellman's clone. The package at each commit was taken out with
`git archive <commit> packages/bellman` into a scratch folder and installed into a scratch environment of its own
(Python 3.12). Each stage file was then run through `python -m bellman <file>`, with `--encoding` and with
`--dossier`, at each commit, and the outputs compared; the stage's places were listed with the package's
`elaborate_text` and the stage's `places()`. The distribution families were read in the package's families module
at both commits, and the concept pages listed at both.

## What it found

- **The stage files need no change.** At the base and at the head, each file's view and dossier are identical. The
  encodings differ only in the hashes of the three grammar files, which the language's specification 0.7 rewrote.
  The package's version is 0.1.6 at both ends, so the number says nothing. At `930199a`: the same.
- **The distribution grammar is unchanged:** the same families with the same argument forms; the families module
  changed only the wording of its refusals.
- **The concept slugs stand:** none of the 61 is gone; three pages were added, on the addition, the grid and the
  methods.
- **The methods side changed.** A stage's methods are now in a methods file beside the stage file, an addition to
  it, whose entries type a method, a grid and a handler at a place named by its path. Under the new package the
  fork's stage files have no place for the solution of the Euler line; the policy's method is typed at the policy's
  block.
- **Bellman refuses what the amended convention says it refuses** (tried on 2026-11-11 at `930199a`, on the fork's
  natural stage file): an addition typing a method at a place the stage does not have is refused, one typing a word
  at a place of a kind that does not admit it is refused, and a well-formed one binds.

## What it establishes, and what it does not

It establishes that nothing in Bellman's changes over that interval alters what the fork's two stage files mean to
Bellman, nor the grammar the fork writes distributions in. It does not establish anything about the model
repository's stage files, which have since moved on from the fork's copies by a few lines each; that repository's
session checks its own, and reported the compiled pieces of its three builders identical at its two pins. It says
nothing of whether a toolkit's methods file is right, only that the form exists and is checked.

## Pending

- The ontology's statement that Bellman's documentation is not public, and its rule that a concept is named and
  never linked ([the deferred items](../deferred.md)).
- The stone convention's amendment for the methods file, drafted and unmerged.
- The three changes asked of Bellman on 2026-10-31, which appear in none of the commits read.
