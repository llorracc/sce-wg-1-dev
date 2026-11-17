---
name: feedback_ontology-home-is-the-fork
description: "The ontology of buffer-stock models lives in this repository; a model repository's copy follows it, and a correction made in a copy is brought here as a pull request; the folder links outward by absolute address (2026-11-14)"
metadata:
  type: feedback
---

This repository's `ontologies/buffer-stock-models/` is the ontology's home, by the owner's decision of 2026-11-14 at
15:54:52 ([the rulings](../rulings/2026-11-14_core-fixes-ontology-held-and-the-series.md)). The buffer-stock model's
repository keeps a copy, and its tests hold the ontology to the families' files there.

**Why:** the copies had drifted. That repository corrected the natural limit and the shocks' written forms on
2026-11-12, and this copy never took them. This one corrected the statement about Bellman's documentation on 2026-11-14,
which that copy lacked. This copy is public, and it is the one the working group's pull request #17 carries upstream.

**How to apply:**
- A change to the ontology is made here, by a pull request on the fork, and then #17's head is brought to main
  ([[feedback_upstream-series-tracks-main]]).
- A correction found or made in a model repository's copy comes here as a pull request of its own: the rows compared
  field by field, and the CHANGELOG entry recorded under the unreleased version.
- Attribution differs on purpose. That copy names who ruled and which session read what. Here public text states the
  rows impersonally ([[feedback_checkable-sources]]), and the family rows carry a `repository` key, since the schemas
  are in the model repository.
- When this copy changes, tell that repository's session. Whether its copy takes the folder is for it and the owner.
  Since 16:18 on 2026-11-14 its copy is this folder unchanged, its `ontologies/home.yaml` recording the fork's commit
  and each file's SHA-256. Send it the merge commit's full hash; it takes the folder with its script and commits it
  when the tests pass (as with #28 on 2026-11-16).
- A link from the folder to anything outside `ontologies/` is an absolute address, since a copy of the folder lives in
  another repository: Project A at https://econ-ark.github.io/sce-wg-1/project-a.html, the Rosetta Stones at the fork's
  `rosetta/README.md` on GitHub. A link to the sibling ontology stays relative, every copy holding both (#27,
  2026-11-14).
