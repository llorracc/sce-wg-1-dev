---
name: feedback_ontology-names-no-toolkit
description: "The semantic ontology names no toolkit, and nothing peculiar to how a toolkit solves or simulates the problem; each toolkit's names and departures go in its own document, the schemas' Rosetta Stones (ruled 2026-11-01)"
metadata:
  type: feedback
---

On 2026-11-01 at 09:23:51 the owner ruled that the semantic ontology of buffer-stock models references no particular
toolkit, HARK included, and no aspect of the setup of the solution or the simulation that is peculiar to a toolkit.
There is to be a document for each toolkit used to solve the buffer-stock problem.

**Why:** the ontology states the model class: what a buffer-stock model is, its objects, conditions and results, and
when two models are one. How a toolkit names, approximates, solves or simulates a member is that toolkit's business. It
changes with the toolkit's versions, and it would tie a statement about models to one implementation.

**How to apply:**
- In the ontology: no toolkit as a format of the denotation, no toolkit's source pin, and no toolkit's names, sources or
  divergences in any row. A difference between a reference approximation and its target, the approximation kind of
  divergence, is always a method's, so it is not a kind of the ontology. `test_the_ontology_names_no_toolkit` holds the
  source to this.
- The toolkit documents are the schemas' Rosetta Stones, `schemas/rosetta/<toolkit>.md`. HARK's names for the ontology's
  terms and its ten departures from them moved to HARK's stone on 2026-11-01, keeping their identifiers, which the
  ontology lists as retired.
- A paper is not a toolkit: HAFiscal's three divergences stay, as uses of the terms in its paper. An implementation
  detail of a paper's code is no more the ontology's than a toolkit's. HAFiscal's cap on β, a guard against slow
  solutions near the boundary by the owner's ruling of 2026-11-01, left the ontology then.
- What exactly belongs in a stone, against which the moved HARK section is to be judged, is the owner's to explain. He
  offered on 2026-11-01.

See [[feedback_no-upper-bound-on-beta]] and [[project_state]].
