---
name: feedback_say-what-tests-establish
description: "When reporting that tests pass, say what they check; the ontology's tests solve no model, and a bare count read as if they did"
metadata:
  type: feedback
---

On 2026-11-01 at 09:15:34 the owner asked whether the ontology's "46 tests that pass" meant the model had been solved
under 46 configurations, each to convergence. They meant nothing of the kind. They check the ontology's consistency, its
agreement with the schemas' checker, closed forms, and implications among conditions on sampled parameters. None solves
a model.

**Why:** in this project, "tests pass" most naturally means solutions computed and verified, as the results files and the
checker's verification do. A bare count invites that reading, and it overstates what is known about solutions.

**How to apply:**
- Report a test count with one clause on what the tests check. Say plainly when no model was solved.
- Keep the distinction the ontology keeps: a result about solutions carries its source (proved, cited, stated, deduced)
  and is untested unless a results file checks it.

See [[project_state]].
