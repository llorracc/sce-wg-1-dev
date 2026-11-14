# Rulings of 2026-11-14: the core's small fixes, the never-linked rule rescinded, the working group's pull requests kept as a series, and Bellman's public documentation linked

The owner's decisions, in substance and by time (EST). His words are kept outside this public repository.

## The core's small fixes and the ontology's correction

- **09:21:16, here:** the safe core fixes and the ontology's correction are to be made, and the rule that a Bellman
  concept is named in the ontology and never linked is rescinded, since Bellman's documentation is public. It answered
  this session's account at 09:17 of what each would do: four fixes to the core (the environment listed with `-z`,
  each source's anchors checked, a signal recorded by its name, a sentence on memory kills the runtime does not
  report) in one pull request on the fork, and the ontology's statement that Bellman-SYM's documentation is not
  public corrected, as version 0.1.0-draft.3.

**What followed.** The four fixes were made and tested on the branch `core-small-fixes`, committed as 0694471; the
push was refused by the session's auto-mode classifier, so the branch is local and waits on his word to push. The
ontology's correction was not made: at 09:35 bellman.io, its pages and econ-ark.github.io/bellman/ answered 404.
Bellman's development session found that the Pages settings of econ-ark/bellman no longer name the custom domain, a
change made after the site's last build on 2026-11-11 and not recorded anywhere as decided; the repository was already
private while the site was public. Until the site answers, a link to it is a dead link and the statement that the
documentation is public would be false, so the correction and the links wait for the site.

**What it supersedes.** The rule that a Bellman concept is named and never linked, in the ontology's README,
`bellman-concepts.txt` and the generator's definition of `bellmanConcept`. Once the site answers, each concept links to
`https://bellman.io/wiki/<slug>/`, the address Bellman's development session gave.

## The working group's pull requests

- **10:12:36, here:** the working group's seven open pull requests (econ-ark/sce-wg-1 #14–#20) are kept so that when he
  brings the working group's repository up to the fork, the content arrives as a series of comprehensible pull
  requests, not one commit holding everything. Updating them to serve that purpose was approved.
- **10:34:21, here:** fork pull request #22 is merged, the core's environment ignored in `core/.gitignore`, so that #15
  and #20 no longer both append to the repository's `.gitignore`. He is not yet ready to open pull requests in the
  working group's repository, so the eighth, for the site's deploy job, is not opened; its branch,
  `deploy-from-the-group-only`, is on the fork.

**What it supersedes.** Nothing: his word of 2026-11-13 at 15:12:22 not to merge the seven yet stands. The heads were
updated on the fork, by commits and merges and never by a rebase or a force-push; none was merged.

**What stays open.** Whether he merges the series himself or puts it to the group; opening the eighth pull request;
posting the seven updated descriptions, drafted and not posted.

## The core's small fixes merged

- **12:00:25, here:** `core-small-fixes` is to be pushed, its pull request opened on the fork and merged.

**What followed.** The branch was pushed and opened as the fork's pull request #23, its checks passed, and it was
merged at 12:03 with a merge commit, 2311754. Under the standing rule on the series, #19 and #20 were brought to the
new main and pushed; the series, merged in order, reproduces it.

**What it supersedes.** The hold on pushing the branch, which the session's auto-mode classifier had imposed at 10:05
for want of his word.

## The records kept apart from main

- **12:42:32, here:** the records branch and main are kept apart. He had asked at 12:35:30 whether the records branch
  can be merged into main, and was told it cannot by a plain merge without putting the records on main.

**What it supersedes.** Nothing: it confirms his ruling of 2026-11-13 at 14:53:27 that the records branch holds the
records alone.

## The ontology's correction pushed and merged

- **15:12:01, here:** the ontology's correction pushed, opened as a pull request on the fork and merged. The correction
  had waited, under his ruling of 09:21:16, for bellman.io to answer; the site and econ-ark/bellman were public from
  13:38, made so by him in the bellman session.

**What followed.** The fork's pull request #24 was merged at 15:14 with a merge commit, 9648831. The ontology of
buffer-stock models is at version 0.1.0-draft.3, each Bellman-SYM concept it names linked to its page. #17's head was
brought to main under the standing rule on the series.

## Bellman's public documentation linked

- **15:23:52, in the bellman session,** relayed and checked: the links this session's survey proposed are to be made.
- **15:25:28, here:** the items left open are to be fixed: the links; the sentence that the truncated lognormal is in
  preparation in Bellman-SYM; the primer's footnote that Bellman's documentation is not public, live on the working
  group's site, whose correction there takes a pull request in the working group's repository; and the memorial.

**What followed.** The links and both corrections are the fork's pull request #25, with its checks passed. The
session's auto-mode classifier refused its merge at 15:31, so it waits on his word to merge. The series' heads and a
branch for the primer's pull request in the working group's repository were made locally and not pushed.

**What it supersedes.** The rule that a rule learned from Bellman is stated as the schemas' own, with no Bellman page
cited, because its documentation was not published ([the memory](../memory/feedback_checkable-sources.md)). Its pages are
cited now.

**What followed, later.**
- **15:52:59, here:** #25 merged, at 15:53 (c7e7dee), and the series' heads pushed.
- **15:54:31, here:** the primer's pull request opened in the working group's repository and merged. It is
  econ-ark/sce-wg-1 #21, merged at 15:57 (4395e8d); the live page was corrected by 15:59. It is the first pull request
  from the fork to be merged into the working group's repository since the series was opened.

**What stays open.** Nothing on Bellman: public records name it, never its development repository (below).

## The ontology's home

- **15:54:52, here:** this repository's copy of the ontology of buffer-stock models is the ontology's home. It takes the
  two corrections made on 2026-11-12 in the buffer-stock model's repository's copy, as a pull request of its own.
- **16:04:01, here:** that pull request, the fork's #26, merged.

**What followed.** #26 was merged at 16:04 (69bc191), and #17's head was brought to it, so that the working group's
repository receives the corrected ontology. A correction made in a model repository's copy comes here as a pull
request ([the memory](../memory/feedback_ontology-home-is-the-fork.md)).

**What it supersedes.** Nothing ruled. Until then neither copy had been named the home, and each had taken changes the
other lacked.

## The descriptions posted

- **16:07:21, here:** the drafted descriptions of the working group's pull requests posted.

**What followed.** The six drafts, for #15–#20, were brought to the afternoon's state and posted at 16:08. #14's
description stands, since its head is unchanged.

**What it supersedes.** The hold on posting them, open since the descriptions were drafted that morning.

**What stays open.** Opening the deploy job's pull request; merging the series or putting it to the group.

## Bellman named, never its development repository

- **16:17:37, here:** public records name Bellman, and do not name its development repository.

**What followed.** The records' 52 mentions of the development repository were reworded, and two files renamed
([the journal](../journal/2026-11-14_session-record.md)). The rule is in [the memory](../memory/feedback_checkable-sources.md).

**What it supersedes.** The open question, from the bellman session's note at about 14:07, of whether a public record
may name the development repository's commits, pull requests or paths.

## The series held as drafts

- **16:17:55, here:** the working group's seven pull requests, #14–#20, made drafts and marked not ready to be merged.

**What followed.** Done by 16:18:47; each description opens with the mark. None can be merged until he marks it ready.

**What stays open.** When the series is ready, and whether he merges it or puts it to the group.

## The ontologies' table and the copied folder's links

- **16:50:22, here:** the first two of the three points the buffer-stock model's repository's session found in the
  fork's ontology folder fixed, pushed, opened as a pull request on the fork and merged.

**What followed.** The fork's #27 merged at 16:53:11 (bd22255): the table in `ontologies/README.md` lists the ontology
of buffer-stock models, and that ontology's README links Project A and the Rosetta Stones by absolute address. #17's
head was brought to it. A link from the folder to anything outside the ontologies' folder is absolute from here on
([the memory](../memory/feedback_ontology-home-is-the-fork.md)).

**What stays open.** The third point: whether that repository's copy of the ontology of probability distributions, at
draft.1, follows the fork's draft.2. It is that session's question to him.
