---
name: feedback_reaching-the-limit
description: "Say whether an agent ever ends a period at the borrowing limit itself, not whether the constraint \"binds\"; and state a threshold such as rho < k with k as a property of the model's laws"
metadata:
  type: feedback
---

On 2026-11-01 at 12:50:56 the owner found the proposal's row "does the constraint bind?" confusing. In the natural
scenario the natural constraint guarantees a > −h_min, which is one sense of binding. He also read "ϱ < 1 or 2" as two
thresholds for one model.

**Why:** a constraint in force is never violated: borrowing past the natural limit is infeasible. What differs between
the scenarios is whether an agent ever chooses to end a period exactly at the limit, consuming c = m − a_min. A threshold
written with alternatives reads as a choice, when it is one number that the model's laws fix.

**How to apply:**
- Write "ends a period at the limit" or "reaches the limit"; when "binds" is used, define it once in that sense, as
  [`constraint-scenarios.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/constraint-scenarios.md) does.
- State ϱ < k with k defined as the number of shocks with densities at their floors, so that each model has one
  threshold; say what the class's ϱ > 1 leaves of it.

See [[project_state]].
