---
name: feedback_method-attachment
description: "Where a method attaches in a stage file: an expectation's on its operator, the solution on policy.euler.solve, the interpolation on policy; tags as methods, routines as handlers; bst/1 stays free of any method's lines (2026-10-22, #11)"
metadata:
  type: feedback
---

On 2026-10-22 the schemas' method targets were found partly unusable by a methods file in Bellman's form, and fixed in
#11 on the owner's ruling of 15:11:02. The rules, now the schemas' own (`bst-1/model.md`, "Method targets";
`numerics.md`):
- **An expectation's method goes on its operator,** `E_ψ_θ_j` in `bst/1` and `E_reg_j_ψ_θ` in the Markov family, which
  covers both lines; never on the block `dcsn_to_arvl` or one of its lines.
- **The solution goes on `policy.euler.solve`,** as `!time-iteration` or `!root-find`, with a toolkit's endogenous grid
  method named as the handler. **`bst/1`'s stage file stays free of any method's lines** (the owner's ruling): `!egm`
  attaches only to a stage that writes the inverted Euler equation and the endogenous grid, and `bst/1`'s does not.
- **The rule's interpolation goes on `policy`,** such as `!Linear`; there is no `evaluate` target. HARK's cubic, whose
  slopes are the solution's own MPCs, has no tag and is named as a handler.
- **Tags and handlers.** Where a computation has a tag, the method is the tag, quoted in YAML; a toolkit's or the
  registry's own name goes in `handler`. A setting the tag does not name is read through a handler, or stays in the
  toolkit's own map. `!quadrature` for nodes that approximate continuous laws, `!monte-carlo` for a mean over draws,
  `!sum` only where every law has finitely many outcomes.
- **One target, one method.** The Markov family's chains and shocks therefore cannot carry two tags on its one
  expectation operator; that is deferred.

**Why:** the stage file is the foundation, and Bellman reads a methods file against it; a target the stage does not give
the computation is refused there. Keeping `bst/1` free of a method's steps keeps the model's statement method-free, as
the schemas promise.

**How to apply:** name a method's target from the family's table only, and check a new methods file, card or adapter
against it (the Rosetta check and the adapter's test do so for what exists). Ask the bellman session to run Bellman's
own check when a target or tag is new. In public documents state these rules as the schemas' own, without citing
Bellman's unpublished pages ([[feedback_checkable-sources]]). The evidence is in the findings of 2026-10-22.
