# Rulings of 2026-11-02

The owner's decisions on the experiments and the harness, in substance and by time (EST). His words are kept outside
this public repository.

- **09:48:03, the four pieces.** The project needs four things:
  - one ontology of buffer-stock models, consistent with Bellman's ontologies;
  - schemas of the experiments every toolkit is to perform;
  - a Rosetta Stone for each toolkit;
  - a harness that runs each toolkit's solutions.

  The owner asked whether the fourth has a usual name. The answer given: "harness", as in a test or evaluation harness,
  and the whole is a model intercomparison, as CMIP is for climate models.
- **09:57:09, the drafts.** The experiment schema and the harness plan to be drafted. Done:
  - [`experiments.md`](../../experiments.md), [`experiment.schema.json`](../../experiment.schema.json) and the first
    experiment;
  - [`harness.md`](../../harness.md).
- **10:33:47, the plan's six decisions** ([`harness.md`](../../harness.md), "The owner's decisions"):
  - **Words:** approved. What were called test suites are experiments, and `numerics.md`'s suite of settings elements is
    a ladder.
  - **When two toolkits agree:** the first experiment's two checks stand: the same effective member, and a difference
    between the rules that falls with the level. A tolerance from a ladder of method-only settings at fixed nodes is
    deferred until later.
  - **The layout:** approved. `schemas/` keeps the families, the experiments and the checker; the Rosetta Stones move to
    `rosetta/`, and the adapters with the toolkit registry to `harness/`. The move is to be one commit with nothing else
    in it.
  - **The environments:** lock files from the start, one for each toolkit.
  - **Large outputs:** the Jacobians' matrices are kept out of git for now. The results file's hashes are the record.
  - **The spelling of names:** the experiment file's underscores, following the schemas' keys, approved. Whether the
    ontology's names keep their hyphens is still open.
- **10:33:51, memorialize.**

**What stays open:**
- whether the ontology's names keep their hyphens, as econ-ark's notation registry has them, or take underscores;
- three fixes offered at 09:27 and not yet taken up:
  - a section in dolo's stone saying it names none of the ontology's terms;
  - HARK's departures from the schemas gathered into one list;
  - the Rosetta README's list of what is not yet written;
- the toy-hafiscal estimation, a smaller fourth rung, `library` against v0.1, and the push, as on 2026-11-01.
