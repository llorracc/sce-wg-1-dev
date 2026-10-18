---
name: feedback_iterate-and-propose
description: "Build iteratively; when the work suggests a change to a schema, pause and put the proposal and its downstream consequences to the owner before making it (owner's ruling of 2026-10-18)"
metadata:
  type: feedback
---

On 2026-10-18, approving the emitter and the HARK newborn flag, the owner ruled that the work proceed iteratively and that
any improvement to a schema the work suggests be explained to him, with its downstream consequences thought through, before
it is made.

**Why:** a schema is the group's shared statement of a model; a change made in passing while coding ripples into every
parameter file, results file, validator, checker and adapter, and into the hashes that identify models.

**How to apply:** do not edit `schemas/` to fit what code finds convenient. Write the proposed change with what it alters
downstream, put it to the owner, and continue on his word. The same rule binds the sessions building adapters, which send
their proposals here.
