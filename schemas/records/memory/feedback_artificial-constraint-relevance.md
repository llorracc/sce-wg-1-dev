---
name: feedback_artificial-constraint-relevance
description: "An artificial borrowing constraint has an effect only where it is strictly tighter than the natural constraint; one no tighter has no effect, so the member is the natural-constraint member there (ruled 2026-10-22)"
metadata:
  type: feedback
---

On 2026-10-22 at 22:04:28 the owner ruled on how to read an artificial borrowing constraint: the requirement is not that
`a_Art` lie strictly above the natural limit. It is that **a relevant artificial constraint, where one exists, lies
strictly above the natural one**. Imposing an artificial constraint that is no tighter than the natural constraint has
no effect.

**Why:** at or below the natural limit the household never reaches the artificial one, since u(0) = −∞ already keeps it
above the natural limit. Such a constraint changes nothing: no kink, no mass at a constraint, no binding case for the
welfare conditions. The model is the natural-constraint model.

**How to apply:**
- **Validity.** A written `a_Art` equal to the natural limit is valid and means no effective artificial constraint: in
  `bst/1`, `library`'s 0.0 with ξ_u = 0, where `a_Nat` is 0; in the Markov family, HAFiscal's 0.0 under lognormal laws,
  where every state's natural limit is 0. The family documents' "above the lowest `a_Nat(j)`" is read in this sense, and
  their wording is to be corrected by proposal. bst/1's checker refuses an `a_Art` below `a_Nat` as a second written
  form of `natural`, and accepts equality; the Markov checker does the same against the lowest natural limit.
- **Analysis.** Decide relevance where the constraint acts: in `bst/1`, `a_Art` > `a_Nat`; in the Markov family, state
  by state, where the constraint in force from the recursion with `a_Art` inside exceeds what the following states
  impose (conditions.md, "The kink"). A kink, a mass at the constraint and the binding welfare case exist only where it
  is relevant; elsewhere use the natural-constraint statements.
- **Effective members.** A toolkit's discrete laws have a lower natural limit than the stated laws, so a constraint
  irrelevant for the stated member can bind in the effective one (the findings of 2026-10-22 on `natural`). Judge
  relevance for the member being analyzed, from its own lowest values.

See [[feedback_notation-and-foundation]] and [[project_state]].
