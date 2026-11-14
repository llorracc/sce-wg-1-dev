---
name: feedback_checkable-sources
description: "Public documents cite what a reader can check, such as a commit, a public pull request or a published page; who read what, and when, stays in the records; Bellman's documentation, public since 2026-11-14, is cited at bellman.io"
metadata:
  type: feedback
---

On 2026-10-21 the owner ruled that the Rosetta Stones cite their sources by what a reader can check:
- HARK at `4c285e86`; never an unposted branch: its name, commit and code stay out of public text, since the owner's
  rule in the HARK sessions is to perfect a pull request locally before posting it, even as a draft (relayed by the
  HARK session on 2026-11-04, after this repository's records of that morning had named one; corrected the same hour);
- the lecture's source at `96ede2993`;
- HARK's draft pull requests by number;
- the buffer-stock benchmark's emitter, called not yet public.

The sessions that did the reading are not named there. The bellman session had raised the point: a reader cannot consult
a session, and one of the repositories named was not public.

**Why:** a document's source should be checkable by its reader. The sessions' part is provenance, and the records already
hold it with its stamps.

**How to apply:** in a schema document, a stone or a pull request's description, cite a pinned commit, a public pull request
or page, or a named public document. Describe anything private as not public, without its path or identifiers. Keep who read
what, and when, in the journal and the findings. See [[feedback_no-timings]].

**Bellman's documentation is public, and is cited** (since 2026-11-14). From 2026-10-22, when its site returned "Site not
found" and its repository was private, a rule learned from Bellman was stated in a public document as the schemas'
own, with no Bellman page cited; the findings record where each came from ([[feedback_method-attachment]]). From
13:38 EST on 2026-11-14 econ-ark/bellman and https://bellman.io/ are public, and the owner asked that the documents
link them ([the rulings](../rulings/2026-11-14_core-fixes-ontology-held-and-the-series.md)). So:
- cite a page of bellman.io, written without `www`, whose certificate names bellman.io alone; or cite a path on
  econ-ark/bellman's main (`blob/main/<path>`). Don't pin a commit there: the repository changes only when Bellman's
  development repository is exported to it, and its history may be started again;
- a rule still stated in the schemas' own words keeps them, with a link beside it;
- public records name Bellman, never its development repository, which stays private: the owner's ruling of
  2026-11-14 at 16:17:37. A link into that repository reaches no public reader, and its commits and pull requests
  are not found in econ-ark/bellman, so a public record says "Bellman" and gives a hash only where the record needs
  one; the sessions that work in it are "the Bellman session".

**Cite the public commit, not a checkout** (2026-10-31). A local clone can sit on a commit no remote has: the
HAFiscal-Latest session's first line citations came from such a checkout of HAFiscal-QE, and at the public head the
lines, and the formula they cited, had changed. Check each cited line at the public commit before it goes into a public
document, and pin that commit.
