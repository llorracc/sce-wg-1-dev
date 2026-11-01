---
name: feedback_no-upper-bound-on-beta
description: "Neither the schemas nor the ontology may require β ≤ 1; such a requirement would be their error, never a divergence of a paper (ruled 2026-11-01)"
metadata:
  type: feedback
---

On 2026-11-01 at 10:05:57 the owner ruled that a requirement in the schemas or the ontology that the discount factor
satisfy β ≤ 1 would be an error in the schemas or the ontology, not a divergence in a paper or its code that uses a
larger β.

**Why:** with income growth and risk, what disciplines patience is the set of conditions (the FVAC, the WRIC, the RIC,
the growth conditions), not β itself. A model with β > 1 can satisfy all of them. BST cites Szeidl and Ma, Stachurski
and Toda for βR < 1 not being necessary either.

**How to apply:**
- bst/1's and the Markov family's parameter schemas, and bst/1's results schema, require only β > 0 (checked
  2026-11-01). The ontology's sampled models draw β from 0.3 to 1.3. Keep it so.
- Before calling another paper's restriction on β a divergence, check that the ontology or a schema is not the one
  imposing a bound it should not have.
- A cap a paper places on β to meet a condition, such as HAFiscal's, is to be read as the condition it enforces, not
  as a bound on β.

See [[feedback_ontology-names-no-toolkit]].
