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
- **10:39:40.** The owner gives the go-ahead for the layout move. Made by 10:45 as one commit, `9675109`, with nothing else:
  - the Rosetta Stones moved to `rosetta/`;
  - the adapters to `harness/adapters/`;
  - the experiments to `schemas/bst/experiments/`.

  Every path and link to them was rewritten: 43 Markdown links, the adapters' path to the schemas and their own names,
  and the ontology source's comment, whose generated files carry the new digest. Checked:
  - the repository's broken relative links are the 3 there were before;
  - the checker's 200 tests, the ontologies' 67 and 12, HARK's adapter's 8 and dolo's 4 pass;
  - HARK's adapter rerun on `bst-restrained` at `low` gives the committed files, differing only in the adapter's own
    path.

  The records keep the old paths as they were written.
- **11:23:59.** The owner gives the go-ahead for the runner, the plan's second stage. Built by 11:30, uncommitted:
  - `harness/envs/hark` and `harness/envs/dolo`: `uv` projects locked in `uv.lock`, each pinning the interpreter
    and the numpy, scipy and numba of the runs of 2026-11-01. HARK's resolved 45 packages, dolo's 42;
  - the harness's own locked environment;
  - `harness/toolkits.yaml`;
  - `harness/runner.py`, with `list`, `run` and `verify`;
  - the experiment checks moved from the test into `schemas/checker/experiment.py`, which the runner calls;
  - `harness/test_runner.py`, 7 tests on a stand-in toolkit, passing;
  - `.gitignore` for the environments and the run folders.
- **11:27:54–11:30.** The acceptance run, HARK and dolo at `low`:
  - the first try failed three of dolo's four jobs on numba's cache, raced on the new environment;
  - the runner now runs each toolkit's first job alone;
  - from a cold environment, all eight files are those of 2026-11-01 but for the adapter's path, and verify;
  - HARK's jobs were skipped on the rerun, as resumption should (`findings/2026-11-02_harness-acceptance/`).
- **11:30:42.** The runner reported to the owner as built and accepted, uncommitted. What the acceptance does not show:
  the levels `medium` and `high`, and another machine, where the interpreter, the BLAS or the CPU may change the last
  digits.
- **18:24:32.** The owner asks for a memorial. Done by 18:26:
  - the runner's work committed with the records;
  - `harness.md` marked in progress, with stage 2's acceptance recorded; the README points at `harness/`;
  - the project state brought up to the layout and the words: experiments in `schemas/bst/experiments/`, the adapters
    in `harness/adapters/`, and the tests' counts of the day;
  - the numba race filed in the defects as fixed; the rulings carry the go-aheads of 10:39:40 and 11:23:59.

  The checker's 200 tests, the runner's 7, the buffer-stock ontology's 67 and the distributions' 12 pass.

**State at the memorial (18:24):**
- On `buffer-stock-ontology`, unpushed: `9675109`, the layout's move, and this memorial's commit, the runner.
- Nothing runs; the run folders in `harness/runs/` and the environments are ignored by git.
- Next, when the owner asks: the comparator, the plan's third stage, accepted when its verdicts and numbers on the
  committed runs match the prototype's and `compare_toolkits.py`'s; then a full run at the three levels.
- Open with the owner, as at 10:37: the ontology names' hyphens; the three fixes to the stones; the toy-hafiscal
  estimation; a smaller fourth rung; `library` against v0.1; the proposal to the working group; the push; sharing the
  page, which is private.
