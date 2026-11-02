# Journal of 2026-11-02

Times are EST, from the session's transcript. The day opens on everything since `97dc728` uncommitted: dolo's adapter,
its run of the restrained-limit suite, the page's version 2, and the records of the evening before
([the journal of 2026-11-01](2026-11-01_session-record.md)).

- **09:27:41.** The owner asks for the departures of HARK and of dolo from the ontology and the schemas, and whether dolo
  has a Rosetta Stone. It does, `rosetta/dolo.md` with its cards. The two stones list different kinds of departure:
  - HARK's lists ten from the ontology's terms, each with its row: differences of meaning, notation and convention,
    two approximations and an absence. Its departures from the schemas are spread through its method and adapter
    sections;
  - dolo's lists six from the schemas. It has none from the ontology's terms: its release computes none of the
    ontology's derived objects. Its stone does not yet say so.

  Three small fixes were offered and are not made:
  - a section in dolo's stone saying it names none of the ontology's terms;
  - HARK's departures from the schemas gathered into one list;
  - the Rosetta README's stale "not yet written" list.
- **09:38:33.** The owner asks to see the two stones in VS Code. Opened.
- **09:43:44.** The owner asks whether hyphens are a standard for ontology terms, against underscores, which are also
  variable names. The answer given:
  - no standard prefers hyphens;
  - OBO's identifiers are opaque, with labels in words;
  - W3C vocabularies use camelCase;
  - the OBO Relation Ontology's short names and LinkML's slots use underscores.

  In this ontology:
  - the identifier is already opaque (`BSM_0000005`);
  - the hyphenated name is a `skos:notation`, and matches econ-ark's notation registry, whose keys are hyphenated
    (33 names shared);
  - 44 terms carry a `symbol` that is a valid variable name.

  Replacing every hyphen with an underscore gives 211 valid, distinct identifiers. The choice is the owner's and open.
- **09:48:03.** The owner sets out four pieces:
  - an ontology consistent with Bellman's;
  - schemas of the experiments every toolkit performs;
  - a Rosetta Stone for each toolkit;
  - a runner or harness.

  The answer: "harness" is the usual word, and the arrangement is a model intercomparison, as CMIP's. The adapters
  join the stones to the harness. What is missing is an experiment schema and the runner.
- **09:57:09.** The owner asks for the experiment schema and the harness plan to be drafted. Drafted:
  - `experiments.md`, `experiment.schema.json` and the first experiment,
    `bst/suites/restrained-limit/experiment.yaml`, with `checker/test_experiment.py`. The 17 tests pass, each of 13
    breaks caught for its own reason;
  - a prototype of the harness's comparator evaluated the experiment's three checks on the committed HARK and dolo
    runs, and all pass;
  - one finding shaped the checks: each toolkit's rule moves about 3 · 10⁻³ between levels, mostly from the nodes,
    against a difference between the toolkits of about 10⁻⁵. So the levels cannot supply a tolerance for comparing
    toolkits. The checks require the same effective member and a difference that falls with the level;
  - `harness.md`, the plan, proposed, with six decisions for the owner;
  - the README lists both, and its vocabulary gains "experiment" and "harness".

  The checker's 200 tests pass.
- **10:33:47.** The owner decides the plan's six questions (see the rulings):
  - experiment and ladder, approved;
  - the sharper tolerance, later;
  - the layout, approved;
  - lock files from the start;
  - the Jacobians out of git for now;
  - underscores in the experiment file, approved.
- **10:33:51.** The owner asks for a memorial. Done by 10:37:
  - the words applied to the live documents: `numerics.md`'s suites are ladders; the restrained-limit and toy-hafiscal
    suites are experiments in `bst/model.md`, `jacobians.md`, the README, the stones and the adapters' README. The
    folder `bst/suites/`, the findings' folder names and the records keep the old word;
  - `harness.md` and `experiments.md` marked approved, with the decisions applied;
  - the comparator's prototype and its verdicts filed as a finding (`findings/2026-11-02_experiment-checks/`);
  - the rulings, the deferred list, the project state and the index brought up to date.

**State at the memorial (10:37):**
- Everything since `97dc728` is in this memorial's commit, on `buffer-stock-ontology`, unpushed:
  - dolo's stone, adapter and run of the restrained-limit experiment;
  - the shared `adapters/common.py`;
  - the page's source, version 2;
  - the experiment schema with its first experiment;
  - the harness plan;
  - the records of 2026-11-01's evening and of this morning.
- Next, approved: the layout's move, as one commit with nothing else; then the harness's registry, lock files and
  runner.
- Open with the owner:
  - the ontology names' hyphens;
  - the three fixes to the stones;
  - the toy-hafiscal estimation, in HAFiscal's session;
  - a smaller fourth rung;
  - `library` against v0.1;
  - the proposal to the working group;
  - the push;
  - sharing the page, which is private.
