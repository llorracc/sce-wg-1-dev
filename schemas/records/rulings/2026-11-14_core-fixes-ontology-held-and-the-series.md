# Rulings of 2026-11-14: the core's small fixes, the never-linked rule rescinded, and the working group's pull requests kept as a series

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
