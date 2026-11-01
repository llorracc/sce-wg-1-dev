---
name: feedback_markov-family-is-a-device
description: "The Markov UI form is not a model of its own: one non-persistent unemployment state, the disaster, giving the worst state its own parameter and implementing the natural or artificial case without rewriting the i.i.d. solver"
metadata:
  type: feedback
---

The owner's "Markov ui" is not a full statement of HAFiscal's Markov structure, and not a model distinct from the
natural or the artificial case. It has one unemployment state, the disaster, which may pay ξ_x = 0, and it does not
persist: being unemployed this period does not make it likelier next period. It gives the worst state a parameter of its
own and solves either case on a toolkit's Markov machinery without rewriting its i.i.d. solver (2026-11-01, 14:42:57 and
14:49:50).

**Why:** this session read the family's four persistent states as the device and drew wrong per-state limits from it.
The schemas must not require ξ_x > 0 (14:50:39).

**How to apply:**
- A member written this way is an ordinary buffer-stock member; its tests compare it with its counterpart in
  `bst-natural/1` or `bst-artificial/1`.
- HARK's adapter already solves every buffer-stock member on that two-state chain.
- What becomes of the four-state family is the owner's open question (`deferred.md`).

Related: [[feedback_classify-by-what-the-code-solves]], [[project_state]].
