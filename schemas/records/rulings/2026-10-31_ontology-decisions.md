# Rulings of 2026-10-31

The owner's decisions that reach the ontology of buffer-stock models, in substance and by time (EDT). His words are
kept outside this public repository.

**In the HARK-dev session,** reported to this one and recorded there with his words:
- **13:26:48.** Wherever the natural borrowing constraint is as tight as or tighter than every artificial constraint, a
  buffer-stock model's lowest transitory realization must be a point mass. A semantic ontology of what makes a model a
  buffer-stock model is this session's task, not HARK's or HARK-dev's.
- **13:44:30, his choices from a menu.**
  - The atom is required at the worst transitory shock, not at income in both shocks jointly.
  - HARK halts on its continuous path for a model outside the rule; its classic path solves as before.
  - The edge, where an artificial constraint equals the natural limit, is inside the rule.

  The ontology states the rule as the membership axiom `point-mass-at-worst-transitory`.

**In this session:**
- **15:36:03, his request.** A semantic ontology of buffer-stock saving models:
  - BST is the primary source;
  - the HARK, HARK-dev and HAFiscal-Latest sessions are consulted on ambiguities;
  - it is related to the schemas.

  He asked which of the two, the ontology or the schema, the working group needs. The answer given was both: the
  semantic ontology is the deliverable, and the schemas are its syntax
  ([the ontology's README](../../../ontologies/buffer-stock-models/README.md)).
- **17:44, "memorialize".**

**Earlier rulings the ontology takes,** recorded where they were made:
- **2026-10-22, 11:00:07,** in econ-ark's notation registry (v6.0.0, in the rulings of that day): the GIC-Liv is HARK's
  `GPFacLiv` < 1, that is ℒ Þ̊_𝒢 < 1. The ontology's condition `gic-liv` follows it.
- **2026-10-22,** in the HARK-dev session's line of work:
  - the natural borrowing limit comes from the true laws' infima, never from a lowest atom;
  - a discretized law carries its true bounds.
- **2026-10-24,** there: the shocks' true laws are the continuous truncated lognormals, which atoms approximate.
- **2026-10-27,** there: a buffer-stock model with a risky asset has a target, its formula not yet worked out. The
  ontology takes this as making `with-risky-asset` a member class, a reading the owner has not yet confirmed.

**What stays open,** proposed in the ontology and not yet ruled
([deferred](../deferred.md)):
- whether BST's bounded support, iid shocks and zero-income event are hypotheses of its theorems, as drafted, or
  conditions of membership;
- whether buffer-stock saving means an individual target, as drafted, or the pseudo-target suffices;
- whether the perfect-foresight model is outside the class, as drafted, and the risky-asset model inside;
- whether the schemas' keys carry the ontology's identifiers;
- whether the atom axiom becomes a validity condition of bst/1, which would reject `toy-untruncated`;
- which convention HARK's time-varying lists follow in a cyclical model, where its solver and its simulation disagree.
