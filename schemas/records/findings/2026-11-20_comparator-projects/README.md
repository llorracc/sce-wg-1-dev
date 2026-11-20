# Comparator projects: what other fields built, and what it suggests for the apparatus

What was found on 2026-11-20, on the owner's request of 09:08 that morning: how other fields built open-source
computational comparison tools ("comparator projects", the category of tool this project builds), and suggestions for
improving the apparatus's design from what they decided and learned. Nothing was built or changed; every suggestion
waits on the owner.

## How

- **The survey.** A workflow of 21 agents, which completed with no failures. Eight agents each surveyed one field, and a
  second agent per field re-read each project's primary sources (papers, documentation, source files, GitHub listings)
  and corrected or softened every claim it could not confirm. The fields: computational economics and econometrics;
  numerical methods benchmarked against reference solutions; simulator standards in systems biology and neuroscience;
  cross-code verification in materials science and quantum chemistry; model intercomparison in the earth and physical
  sciences; benchmarks in machine learning and forecasting; conformance suites; provenance and reproducibility
  infrastructure. Fifty-five projects; [the catalog](catalog.md) has each one, with its sources.
- **Our design.** One agent inventoried the apparatus at the fork's main, 4e90bb1 (econ-ark/sce-wg-1's d66f54b, file for
  file), and the two model repositories, which are private: wg1-buffer-stock at 908cfa2 and the perfect-foresight
  repository at dbc4cbc.
- **Suggestions and critics.** A synthesis drew thirteen suggestions. Three critics each tested every one, from a
  different angle: whether it describes our design correctly, whether its precedents really do what it says, and whether
  it is worth its cost at our scale. All thirteen came back "revise", and one was dropped.
- **Practice.** The two model repositories' sessions were asked how the core works in practice there: where it fought
  them, what they built outside it, what a new toolkit's author would trip on, and what they would change first and keep.
  Their answers concern private repositories, so they are not reproduced here and no number of theirs is repeated.
  What they say of the core's code was checked against the core at 4e90bb1.
- **The synthesis below** is the fork's session's, from the revised suggestions, both sessions' answers, the plans
  pending, and this project's rulings. The comparison by dimension and the critics' verdicts cite the private
  repositories' files and records, so they are kept with the session's on-box memory, outside this repository.

It extends [the survey of 2026-11-03](2026-11-03_precedents-for-the-apparatus.md), which the buffer-stock repository's
records also hold and which the owner has not yet read. That survey found that the schemes letting participants run or
report the comparison themselves were the ones that collapsed.

## What it establishes

- **On what is hardest to add later, the design is at the strong end of every field surveyed:**
  - an exact definition as the thing tested;
  - verification and comparison in code the toolkit does not control;
  - the reference's own error beside every distance;
  - no ranking, score or composite, and no default metric;
  - per-job execution records, which no surveyed project requires as fully.
- **Its weaknesses are in the connections between runs:**
  - what a run of record is;
  - when a result is stale;
  - how numbers are matched up for comparison;
  - where shared code stands in for a toolkit.
- **Both model repositories' sessions, asked separately, named the same first problems:** runs of record kept partly by
  hand, and a fingerprint both too broad and too narrow. Both would keep each toolkit as it is, at a pinned commit in its
  own locked environment, with a record of every job.

## What it does not establish

- No suggestion was built or tried, and each one's cost is the critics' estimate.
- Fifty-five projects are a survey, not a census. Each entry is as its verifier left it, softened where a source could
  not be found.
- What the sessions report of practice in their repositories is their account; only what it says of the core's code was
  checked here.

## Two points on how to decide them

- **Amend the pending plan rather than start another.** Five of the recommendations overlap the buffer-stock session's
  plan for the working group's other models, `schemas/other-models.md` in that repository (PROPOSED on 2026-11-19, at
  908cfa2, its decisions listed at its end): the comparator, the bench as a step, the adapter as a command, the pins,
  and the presentation. They should go to the owner as amendments to that plan's decisions.
- **One draft, one rerun.** Each change to the record or registry schemas makes earlier runs look stale and costs a
  rerun of the runs of record. So the run of record, the fingerprints, the comparator, the adapter as a command and the
  level names should be one draft and one rerun.

## Recommendations, in order

### The run of record as a core command

`wg1core run --record`, which:
- starts from an empty folder and reuses no result from another commit;
- refuses a tree that is dirty in a file the jobs depend on, but not merely for an untracked file;
- runs `verify` and `compare`;
- copies the results, methods and settings files, the verification and the comparison, and the manifest into the
  registry, checking each file's hash against its record;
- names each run uniquely;
- registers failed runs, marked as failed;
- appends a row to `runs-of-record.yaml` with the date, the reason and the run it supersedes.

Results files also gain a hash of their numbers alone, without the provenance block.

The evidence:
- **Stale reuse.** A model repository's run of record silently reused a toolkit's results from an earlier commit,
  left in the run folder.
- **Kept by hand.** `register` copies only the records (`cmd_register` in `core/wg1core/runner.py`), so a run of
  record's results files live outside version control on the machine that made them.
- **Stale runs shown as current.** `status` notes a changed experiment, but not changed code: runs whose toolkits'
  code hashes have all changed since are shown with no note.
- **The hash covers the machine.** Results files from one commit hash differently on different machines, because the
  hash covers the provenance, which names the hardware.

Precedents: EBRAINS' validation framework (results never edited, nothing deleted); CMIP6 (data superseded, never
deleted, with errata); the hubverse (checks that flag changes to earlier submissions).

### Fingerprints from declared dependencies, and a diff of two runs

The cheap parts first:
- a glob or path that matches nothing is an error before any job runs. A model repository's worktree without its
  submodules started a run anyway, and every job of one toolkit failed;
- `status` notes each dependency whose present value differs from its run of record's;
- the core checks that every environment pins the same core.

Then replace the hand-kept `code` lists with typed dependencies:
- the toolkit's source, read from its lock: repository and commit, plus a folder's tree ID where history can be rewritten,
  as Bellman's public history was;
- the adapter folder's tree;
- the model inputs a job reads: the stage file, the checker, the request;
- the environment's lock and image.

Each is marked "solved-from" (a change re-solves; the default) or "recorded" (a change is noted, not re-solved).

Add `wg1core diff <run> <run>`, comparing the numbers' hashes and the distances per quantity between two runs of one
experiment. Both sessions do this by hand today; one compares reports byte for byte, which a one-word change in the
core's prose broke.

A misdiagnosis to avoid: the job fingerprint already leaves out the experiment's hash. The needless reruns come from the
stage files and the checker being in every toolkit's code list.

Precedents: airspeed velocity, which ignores results whose code version is not the current one; SLSA's provenance, with
resolved dependencies by digest, whose completeness is best-effort, which is why declarations need enforcing; Guix with
Software Heritage's intrinsic identifiers.

### Fix the comparator

- **Match by point.** Match two files' numbers by the request's points, or refuse a mismatch, instead of flattening them
  by position (`numbers` in `core/wg1core/comparator.py`, which also drops nulls, strings and booleans silently).
- **Undefined values.** Report a value one file gives as undefined as "not compared", counted and shown, not as an error.
- **NaN.** Refuse NaN on every path. This settles the open defect, but it changes earlier reports, so it needs the
  owner's word.
- **Units.** Keep the largest distance per quantity, and a single largest only across quantities that share a metric and
  a unit. Today one maximum folds different units together (the comparator's `largest_distance`, and `status.py`'s
  largest by level).
- **Pairwise distances.** Report pairwise distances between entries for every reported quantity, without verdicts, so
  that a model repository's page stops computing them outside the core.
- **Status against number.** Allow a status in one file to be compared with a number in another; today that is an
  error, which keeps welfare out of the checks.
- **Where the metadata lives.** Each quantity's points, unit and whether it can be undefined belong in the quantity
  catalog that the plan for other models proposes.

Precedents: toml-test's typed values, which separate a defect in the suite from a failure of an implementation; ACWF's
results files, which flag failed and missing outputs; CWL's declared wildcards.

### Pin a buffer-stock reference

The buffer-stock model's experiment pins no reference, so the reference half of `compare` does nothing for it.
[`reference-solution.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/reference-solution.md)
already designs certification: two independent continuous solves, residuals by independent code, and closed forms at
the limits. It waits on the owner's rulings on its decisions R2 to R7. R6, the continuous landing of the distribution,
is the binding technical item, since [the reference probe](2026-11-04_reference-probe/README.md) showed that nodes bound
any distribution at 10⁻³ to 10⁻².

Until then:
- **Rule quantities first.** Pin the probe's continuous solve for the rule quantities, provisional under R1.
- **A reference record:** the method, the settings, a refinement study with its apparent order, the checks made,
  versions, `produced_by` and `certified_by`.
- **A second code.** Certify it against a second code using the same continuous method.
- **Method-different entries are diagnostics.** An entry of a different method, such as time iteration at its finest
  level, is a diagnostic. A disagreement beyond that entry's own convergence is a finding; it never enters the
  reference's stated error.

Do not use value-function iteration on a grid as the second solve: Aruoba, Fernández-Villaverde and Rubio-Ramírez showed
why a brute-force benchmark assumed exact misleads.

Precedents: NIST's reference datasets, whose values were confirmed by at least two algorithms and packages;
posteriordb's reference records (method, arguments, seed, diagnostics, versions).

### The bench as a step, as an amendment to the plan for other models

- **A job may take another job's output** as a declared input. Its first use: the QuantEcon EGM entry gets HARK's
  gridpoints from HARK's job in the same run, so it runs in its own container and the run of record is one run, not
  two. This changes a mechanism the owner ruled in the buffer-stock repository on 2026-11-06, so it is his. Its second
  use is the checks of the forward record.
- **Before that, cut the shared adapter code into modules** with no change in what it does, accepted when the run of
  record reproduces number for number.
- **Later, a measure step** outside the container, reading each entry's exported rule. The experiment names the bench's
  choices (quadrature, distribution method, seed), and the records version the bench. Report the toolkit's own
  stationary distribution beside the bench's, so that error in the rule and error in the distribution method separate.
- **Meanwhile,** the shared code stays unaltered and its hash goes into every record, as MLPerf requires of its load
  generator.

Precedent: the 2011 JEDC test bench of Juillard and Villemot, which rebuilt every team's solution and evaluated all of
them with the same random draws and quadrature. Its documented trap is the lesson: it simulated a second-order
perturbation without its authors' pruning. A uniform evaluator must say how it reads each export.

### The shared nodes, against the rulings of 2026-11-02 and 2026-11-03

These rulings stand:
- [18:28:43 on 2026-11-02](../rulings/2026-11-02_harness-decisions.md): the harness gives a toolkit parameters, not
  methods or settings; the shared nodes, grids and population method are "a departure from the ruling, to be undone";
- [2026-11-03](../rulings/2026-11-03_harness-decisions.md) kept the checks that replaced `same_effective_member`.

Yet the buffer-stock model's run of record still checks `same_effective_member` at 10⁻¹². It passes because every
adapter takes its nodes from the shared code, so it tests that code, not the toolkits. BioSimulators documents the
same trap: conformance taken for correctness hid what was being tested.

The owner's choice: carry the rulings out in the experiment's next version (each toolkit's effective member approaching
the stated one as the level is refined), or rule that the shared nodes stay as the reference realization and say so in
the check's statement. HARK-dev's plan of the same morning bears on it: the HARK adapter would build its income
distribution through HARK's own utilities.

### A protocol for findings, and a register of conventions for each family

[The purpose ruling of 2026-11-04](../rulings/2026-11-04_purpose.md) makes the conventions found the project's product.
No page says how a divergence becomes one. One page, for the owner's approval:
- **Isolate** a divergence with a one-convention experiment, using modes of solution as the switch.
- **Notify** the toolkit's maintainers, with the record IDs, once the owner agrees to disclose them.
- **Resolve** by the stage file, then the source paper's text, then its code, the owner deciding.
- **Record** the outcome either way, resolved or not, with a visible mark.
- **Version.** Each resolution makes a new family or experiment version and a row in the family's register: the
  convention, the value fixed, the records that revealed it.
- **An independent reading.** Before a finding is recorded, a fresh agent given only the records reads it, never the
  adapter's author.

ReScience C's public challenge period is left out while the repositories are private.

Precedents: ReScience C's procedure for a failed replication; the Delta test's identical-settings case, which isolated
one convention.

### The adapter as a command, with a conformance check, as an amendment to the plan for other models

In the registry entry:
- **A command:** an argument list, `python <adapter>` by default, used as given in both runtimes. `apparatus.md` says
  an adapter's command line may be in any language, but the runner starts every adapter with `python`
  (`core/wg1core/runner.py`, on the host and in a container); the sentence should be corrected now
  ([the defects](../defects.md)).
- **What it supports:** the families and kinds an entry supports; a job outside them is recorded "not applicable by
  declaration".
- **No level for an exact entry.**
- **Modes as entries:** each mode its own entry.

A conformance check goes into the smoke run: three files written and valid, versions reported, the level honored, the
inputs unchanged, and a rerun giving the same numbers' hash. A describe handshake and a contract version wait until an
adapter comes from outside the organizer's sessions or in another language.

Precedents: Bowtie's versioned handshake and smoke command; `benchopt test`.

### Levels named by the experiment

- **Names.** Each experiment declares its level names, mapped by name to the adapter's ladder. Drop the registry's
  integers: a level is spelled three ways today, and a toolkit's fourth rung cannot be named.
- **Toolkit defaults.** Add the toolkit's own out-of-the-box settings, accepted in the buffer-stock repository on
  2026-11-06, under a name that does not collide with "default", the name proposed for a rung.
- **Distance by level.** Once a reference is pinned, show each level's distance from it.

Precedents: COCO, which requires the same settings on every problem and benchmarks other settings as different
algorithms; McCullough's separate tables at default and other settings.

### Pins, CI and archives

- **The tag.** Tag `v0.1.0` on econ-ark/sce-wg-1 at d66f54b, on the owner's word, and move both model repositories'
  pins to it, accepted when both runs of record reproduce number for number.
- **The core's tests in CI.** Run them in the working group's CI, which has only `publish.yml` now.
- **Submodules.** The model repositories' CI fetches submodules, so that it runs every entry and not one alone.
- **Base images** pinned by digest in each Dockerfile.
- **Where the images live:** put to the owner ([the deferred list](../deferred.md)).
- **Archives.** When a model repository goes public: a Zenodo release of its run of record, and Software Heritage saves
  of it, the core and each toolkit's pinned commit. HARK's pin is a commit of a fork, and Bellman's public history was
  started again.

Precedents: the Macroeconomic Model Data Base, broken by Dynare 6; the economics language comparison's repository
drifting from the code it timed; measured source decay in Guix and Software Heritage.

### Presentation text

- **A standing caveat** opens every comparison report and page: consistent with the definition and the others, not
  proved right; nothing here ranks toolkits.
- **Rules of quotation in `apparatus.md`.** A claim names the experiment and its hash, the run of record, the reference
  version and the core version. A subset of members is not the experiment. No composite. Durations only with the
  machine and conditions.
- **The member-by-check view** belongs in the page library the plan for other models proposes.

Precedents: MLPerf's guidelines for messaging results; Mittelmann's 2018 episode, when a vendor presented a
self-selected subset of his logs as independent analysis.

## Set aside

- **Graded provenance flags, attestation of CI runs and a "submitted" record kind.** No one has offered to submit, and
  runs of record are not made in CI. "Submitted" comes back with the first offer.
- **A machine-readable block of departures read by the verifier.** Departures stay in the stones' prose, each linked
  to its row in the register.
- **New check kinds for equivalence and refusal.** The existing `compare: members` with `expect: {at_most: ...}` states
  agreement, and inadmissible members belong in the checker's tests.

## Keep

- The exact definition as the thing tested.
- The reference's own error beside every distance, and kind (exact or numerical) apart from role.
- Distances without verdicts; only stated checks decide.
- No ranking, score or composite, and no default metric.
- Per-job records.
- Each toolkit as it is, pinned and locked.
- The container contract.
- Canonical hashes of members.
- Each toolkit reporting the effective member it solved.
- Earlier schema drafts kept for checking old records.
- The clean-room regeneration test of the stones.

## Avoid

The failures the survey documented that bear on this project most:
- **Negotiated tolerances:** loosened at the request of those tested, as the SBML Test Suite's were.
- **Trimmed statistics** that drop the worst point, which would hide a discrepancy at the kink.
- **Failures turned into passes,** or dropped from a denominator: BioSimulators' warnings; wpt.fyi's stale denominator.
- **Truth from the wrong source:** from the best entrant (Benchopt), from an old release's files (Dynare 4.3.2), or
  from an engine that shares a family with an entrant (posteriordb and Stan).
- **Hosted dashboards that vanish:** DeltaCodesDFT's page; the JEDC bench's wiki; test262.report.
- **Documentation drifting from the runs.**
- **Names standing in for settings:** AiiDA's fast, moderate and precise.

## Pending

The owner's decisions, none yet made:
- which recommendations to take, and the schema changes among them as one draft;
- the shared nodes: carry out the rulings of 2026-11-02, or rule otherwise;
- the five recommendations that overlap the plan for other models, as amendments to its decisions;
- the tag `v0.1.0`, waiting on his word since 2026-11-17;
- the survey of 2026-11-03, unread.
