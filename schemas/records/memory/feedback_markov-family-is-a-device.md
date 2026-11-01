---
name: feedback_markov-family-is-a-device
description: "The Markov UI form is not a model of its own: one non-persistent unemployment state, a calibration of bst-natural/1 or bst-artificial/1; a Markov state is a way to solve it. The Markov family is retired (2026-11-01)"
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
- Such a model is a calibration of `bst-natural/1` or `bst-artificial/1`, written there with no family or name of its
  own (16:16:38); `iid-ui-artificial` is one. The four-state family is retired (16:10:29).
- HARK's adapter already solves every buffer-stock member on that two-state chain.
- Build only the calibrations asked for: no version with zero unemployment income was asked for (16:17:30).

Related: [[feedback_classify-by-what-the-code-solves]], [[project_state]].
