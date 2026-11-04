# Participation: what a toolkit's author provides

Proposed on 2026-11-03 on the owner's request of that day; nothing below is applied until the owner has read it.
Revised the same evening by [`comparing-solutions.md`](comparing-solutions.md), on the lessons of the precedents, of
Bellman and of the Matsya consultations; where the two differ, that note is the revision.

Paths are relative to the repository's root. Anything marked *proposed* is not built. The precedents this plan rests on
are recorded in [`schemas/records/findings/2026-11-03_precedents-for-the-apparatus.md`](records/findings/2026-11-03_precedents-for-the-apparatus.md),
proposed with this plan; the page an author would be sent is [`schemas/for-toolkit-authors.md`](for-toolkit-authors.md),
revised with this plan from the draft of the same afternoon. The three are in the tree, uncommitted, for the owner's
reading.

## The question this answers

The owner asked, in substance, what the proprietor of a new toolkit would see as the information about what they must
provide to take part in the comparison; whether the scheme has become more elaborate than it needs to be; how it compares
with software and numerical-coding architectures that have worked; and for a revised plan.

What an author would have seen in the afternoon's draft of that page is a list of five artifacts before a run counts: a Rosetta Stone
with cards written in a private project's field vocabulary, an adapter with a fixed command line, a ladder with method
and settings files and a locked environment, a registry entry, and a findings record; and it puts the stone, every
lexicon row in the stage file's names, before any code. The results file it asks for carries about 1,400 numbers for a
single-type member (dolo's `bst-restrained` file at its finest level holds 1,408), of which the exported rule is about
800 and most of the rest is arithmetic the organizer's own code already performs from less: the thirteen conditions'
factors and verdicts, the derived parameters, the special points, the pooled blocks, the hashes, and the Euler
residuals' quadrature. The thirteen documents that draft links come to about 2,700 lines of cross-referenced prose,
beside a 1,010-line results schema, a 117-line checker command with its 631-line member module, and a 929-line shared
adapter module. No measured onboarding effort exists: the only onboarding
on record is dolo's, written by the organizer's own session with the schemas in hand, and no hour count is recorded in
the repository. Any estimate below is this plan's own guess and is marked so.

The short answer is that the apparatus is not over-designed in its parts; every part has a counterpart in a scheme that
lasted. It is over-exposed: it shows the participant the organizer's whole machine and asks the participant to operate
it. The precedents all turn that around. This plan keeps every schema, validator, hash rule and ruling and changes who
does what, in what order, and what the author reads.

## What the precedents do

Six families were read; the precedents record (*proposed*) has the detail and the sources. The table gives the division
of labor in each, with our apparatus as it stands in the last row.

| family | the organizer provides | the participant provides | exchange format | verification and comparison |
|---|---|---|---|---|
| Climate model intercomparison (CMIP, CMOR, CF, ESGF, obs4MIPs, ESMValTool, PMP) | peer-reviewed experiment protocols; forcings in the output format; a tiered data request; a reference writer (CMOR) and a validator (PrePARE); registration by issue; publication infrastructure; evaluation packages | a small mandatory entry card of experiments plus optional tiers; conforming files; a registered identifier; documentation on a common template, required since CMIP5 and CMIP6, with CMIP7 adding a short essential-documentation card required of every model | netCDF under the public CF conventions and JSON vocabularies | structural at the publication gate, by tool; no certification of numbers; comparison downstream by the organizer's packages against references in the same format |
| Systems biology (SBML, SED-ML, KiSAO, SBML Test Suite, OMEX, BioSimulators) | public versioned specifications with reference libraries; per-case model, settings, expected results and tags; a runner and a results database; a one-command container convention with a capabilities file | one results file per case, self-uploaded; or a capabilities file, one command line, one image | XML with public schemas; HDF5 reports; OWL vocabularies | one tolerance formula per case with expected values from closed forms or two independent tools; cases a tool's capabilities file does not claim are skipped; a wrong value fails; a crash is an error by default, a warning only where a case's own settings say so |
| Co-simulation (FMI, the Cross-Check, Reference FMUs, SSP) | a free standard with public schemas and headers; reference models with a reference simulator and validators; rules fixed in advance; a tools page by pull request | a minimum count of models with the vendor's own reference results and an options file; today a self-maintained compatibility page | a ZIP container with an XML description; CSV results; a key-value options file | the vendor's own reference as the oracle; bands; a steering committee that could demand evidence; no certification, no accuracy ranking; the central cross-check archived as unmanageable |
| Benchmark libraries and solver competitions (SMT-LIB and SMT-COMP, MiniZinc, CUTEst, COPS, Mittelmann, the Bari test set, MLPerf) | a public input format with a reference document; a library with expected answers; the execution environment and limits; a published selection and scoring method; a report per round | one registration file by pull request, one container or one interface program, a short system description; the solver | text formats read directly by solvers; JSON registrations | answers compared with stored status, wrong answers penalized heavily; the organizer runs everything identically; profiles and shifted means with their limits stated |
| Computational-economics comparisons (Taylor and Uhlig, the JEDC suites, the Macroeconomic Model Data Base, Dynare, REMARK) | the equations and parameter cases; a tasks document; the random elements; a test bench fed only a policy function; a platform with a small common interface | a policy function or decision rules on a grid, a companion paper; a mod file with a standard preamble; a reproduction script in a pinned environment | tables and files per exercise; Dynare mod files; a shell script and environment file | one bench computes every diagnostic from the reported rule on fixed points; a unit-free Euler residual in base-10 logarithm as the shared currency; reported times judged not comparable |
| Software architecture for interchange (LLVM, Pandoc, LSP, WPT and Interop, JSON Schema and Bowtie, Unicode, NIST StRD) | a public hub format with a compatibility promise; the test corpus with its expected results; a runner and a public scoreboard; reference implementations of the interface; one pass formula | a thin wrapper against one small interface, returning its own name, version and capabilities; honest non-answers | textual and JSON hub formats; line-delimited JSON protocols; test files | expected results owned by the organizer; boolean conformance, tolerance bands, or digits of agreement with certified values; the organizer runs the comparison and publishes the dashboard |
| Our apparatus today | two stage files (normative, in a language with no public documentation) with prose readings; members with canonical hashes; a checker; request files; a results schema; an experiment file; a harness with locked environments; two reference adapters | a stone with cards in a private field vocabulary before any code; an adapter; a ladder with method and settings files; a locked environment; a registry entry; twelve verified results files; a findings record | strict YAML members; JSON results; YAML method, settings, request and experiment files; the stage file | the checker's arithmetic identities and closed forms at the gate, numbers trusted; three experiment checks of convergence; no ranking, no timings; the comparator planned |

What lasted in the precedents: a small mandatory entry card with optional tiers; a public hub format with a writer and a
validator shipped by the organizer; expected results owned by the organizer and runnable by anyone; structural
verification at entry and comparison downstream, run by the organizer and published with discrepancies; documentation
required on a common template with the submission, and in CMIP7 shortened to an essential card; versioning that never
invalidates a published result; written governance. What collapsed or went wrong: vendor-run cross-checking and
self-reported ledgers (FMI's Cross-Check, SBML's database); documentation that arrived too late to be of use through
tools that were hard to use (CMIP5's); a normative artifact nobody outside could read (CMIP's attributes document behind
a sign-in wall); curated experiment files with mistakes nobody caught until a validator read them (almost all of
BioModels' SED-ML files had at least one mistake that made them impossible to run, and the official SED-ML examples
needed correction by the validator); and the withdrawal of commercial solvers from a public benchmark, for reasons the
withdrawing vendor stated as test-set sizes, a validation and tuning-detection burden beyond the administrators'
resources, machine-learning tuning and diminished utility, which this plan reads as the cost of running a contest rather
than a comparison.

## Where our apparatus is like them, and where it is more elaborate

Like them, and worth keeping as it is: the experiment file (CMIP's protocol and data request in one file); the request
file (SBML's settings file, the JEDC bench's fixed points); the member's canonical hash as the model's identity, stronger
than any precedent's identifier; the results schema with a validator at the gate (CMOR tables and PrePARE); the
statuses `undefined` and `not computed` (Bowtie's skipped, NIST's allowance for a different minimum); levels as settings
and not error targets; the organizer-run harness in locked environments (Bowtie, BenchExec, BioSimulators); the Euler
residual under the stated laws (Judd's unit-free error); the rule that no run time was published, revoked on 2026-11-04 (times are recorded since, with their
machine and settings), stricter than any precedent and supported by the precedents' own conclusions; and the effective-member report, which has no precedent and
is this project's contribution: the toolkit reports the model it actually solved in numbers free of any representation,
so a difference of representation is seen before a difference of solution.

More elaborate than any precedent, and the subject of this plan:

- Five artifacts before a run counts, where every precedent asks for one artifact the author already has plus a short
  card. The stone first, in a private vocabulary, where the precedents collect documentation with the runs.
- A results file that asks the toolkit for statistics the organizer's code computes from less. Both reference adapters
  obtain the conditions block by importing the checker's own module; the special points are roots the adapters find on
  the rule; the pooled blocks are share-weighted arithmetic; the Euler residuals use one shared quadrature. An author
  outside Python would reimplement the arithmetic of the checker's 631-line member module, of which the conditions'
  factors are one part, to report what the checker then recomputes.
- One mapping spelled three times (the method file, the stone's methods section, the cards' methods list), a level
  spelled three ways (named levels, the adapter's integers, a planned ladder's elements), and one run's numbers copied
  into a stone, a cards file, an adapter README and a findings record.
- Pieces that exist on paper only: the ladder file, the method registry, the validators for method, settings and request
  files, the comparator, continuous runs, three results blocks.
- A normative statement in a language whose documentation is not public, and cards in a field vocabulary defined only by
  example. Every precedent's normative statement is public; the one that was not is the one recorded as a failure.
- The experiment file on disk is version one and still requires two toolkits' effective members to agree to one part in
  a trillion, which a toolkit with its own representation fails by design; the documents say the opposite.
- The environment for a toolkit outside Python is undefined: the registry admits a uv project or nothing.
- The reference runs agree because they shared nodes, grids and population code, so their agreement measures the
  solvers alone; a newcomer's honest representation difference would read as a disagreement against two witnesses.
- Things no precedent leaves unsaid and this apparatus does: who the organizer is and under what license anything is
  exchanged; what happens when the gate refuses a file; how a dispute over a difference is settled; how the model
  statement is versioned; what a run may consume on the organizer's machine; how a toolkit's entry is retired or
  re-pinned. Each has a section below.

## The revised design

### The stages, by name

Participation is tiered, as CMIP's entry card and endorsed MIPs are. Each stage is named; the first is the smallest
thing that can be verified.

- **The probe.** One results file for the entry member, `bst-restrained` (one discount-factor type, no mortality, no
  zero-income event, a borrowing constraint at zero, a kink to find), at one level of the toolkit's own numerics, with
  its method and settings files and a half-page card. Results only: no adapter, no environment, no registry entry, no
  stone beyond the card. The organizer verifies it, compares it at the request points with every file on record, and
  reports back through the private channel the card names. A probe is recorded in no finding and placed on no ledger
  row; it is the author's feedback and the organizer's first look. Its files stay outside the repository, on the
  organizer's machine, and are deleted on the author's request; the journal records a probe by toolkit name and outcome
  only with the author's consent, never its numbers.
- **The restrained-limit experiment.** The experiment's four members at two levels at least, three recommended, still
  results only if the author prefers. Two levels let the checks that need successive levels run. A verified experiment
  submission is placed on the ledger as submitted-only.
- **The integration.** The author keeps two commands stable and names a version to pin with a requirement list; the
  organizer wraps the commands in the adapter contract, locks the environment, writes the registry entry and reruns the
  toolkit on every experiment. A harness-reproduced run is what a findings record is made from.
- **The stone.** The organizer generates the Rosetta Stone's skeleton from the card, the method file and the verified
  runs; the author fills the rows only the author knows (names, timing, normalization, departures) and reviews the rest.
  The cards in the stone registry's field vocabulary are the organizer's export. What exactly a stone holds is the
  owner's to explain, and the owner has offered that account and not yet given it; this two-stage shape waits on it and
  is listed among the decisions.

### The participant's surface

Each step names what the author reads and what the author provides. No hours appear on the page the author is sent; the
plan's guess is at the end of this section, with its caveat.

- **Read.** The participate page; `schemas/bst/model.md`; the TruncatedLogNormal section of `schemas/shock-laws.md`;
  `schemas/bst/results.md`; the method and settings sections of `schemas/numerics.md`; the checker's printed report on
  the entry member, which gives the hash, the closed-form moments and every condition's factor and verdict; the stage
  file once beside `model.md`, with the reading guide (*proposed*). About 1,100 lines of prose for the Python and kit
  paths; the by-hand path adds `schemas/bst/conditions.md`, since that path computes the thirteen factors with their
  bounds and classifies the welfare lower-tail case by that document's domain rules. Nothing in the stage file's syntax
  is written by the author.
- **Send the card.** The first section of `rosetta/<toolkit>.md`, half a page, on the pattern of the capabilities
  table in `rosetta/dolo.md`: the toolkit's name, version or commit, language and license; the families it solves;
  how it represents the laws; the method on each of the stage's seven targets in the author's words; its names, timing
  and normalization for the parameter file's keys and the results objects, which only the author knows; what it does
  not compute; a pointer to the toolkit's own buffer-stock example; a maintainer contact for the private channel; and
  the author's consent, or not, to be named by GitHub handle. The organizer answers it before any code is written, which
  keeps the pause the owner asked for after a stone.
- **Encode and solve the entry member.** Represent the two truncated lognormals in the toolkit's own way (the stated
  standard deviation is that of the log after truncation, the bounds are in standard deviations of the log, the mean is
  one), the constraint at zero, one type. Check the representation's moments against the checker's closed forms. A
  Python author may call the shared module's node and population functions and declare it in the card, if the owner
  keeps them as a declinable library. Compare the kink, target, mass at the constraint and mean MPC with the reference
  numbers on the page, labeled as two shared-node runs.
- **Produce a results file that passes the checker.** In Python, today: write the toolkit object that `run` in
  `harness/adapters/common.py` expects, as `DoloToolkit` in dolo's adapter does: the strings `name`, `driver`,
  `description`, `representation`, `diagnostics_method`, `methods` and `solver`; `version()` and `commit()`;
  `settings(level, lev)`, which takes the level's number and the shared module's level dictionary; and
  `solve(member, beta, nodes, lev)`, which receives the module's nodes and returns the rule with its derivative, the
  value function or none, and the lower limit. The module writes the three files; dolo's adapter is the worked example. In any language, once the kit exists (*proposed*): write two commands, `solve`,
  which solves and writes the quantities only the toolkit can produce, and `evaluate`, which returns c, the toolkit's
  own MPC and the value at points the kit names; the kit assembles the file. Without the kit, today: write
  `results.json` to `results.md` by hand, which an author outside Python faces until the kit exists. Either way, run
  `check.py <member> --verify-results` until it passes.
- **Write the two small files.** `settings.yaml`, a flat map of plain values with a `level` key, as the committed files
  are today; `methods.yaml`, the seven targets, each with the tag as its method where the stage gives one
  (`!time-iteration`, `!Linear`, `!quadrature`, `!histogram`) and the toolkit's routine as its handler, words only where
  no tag fits, no values. Until `schemas/numerics.md`'s template gains the `arvl_to_dcsn` entry it lacks (a proposal
  below), the template is a committed `methods.yaml` under the findings. The method file is the one spelling of the
  mapping; the cards' methods list and the stone's table are generated from it.
- **Send the probe.** A folder `<toolkit>/<member>/<level>/` with the three files, and the card, through the private
  channel. The organizer runs the submission command (*proposed*: the validator, the checker and the experiment's
  reports list in one call), the comparison at the request points, and sends back the report with the numbers.
- **Then, if the author continues:** the four members at two or three levels (the restrained-limit experiment); two
  stable commands and a pin (the integration); corrections to a generated stone (the stone); a paragraph of judgment,
  signed by handle, for the hand-written findings record.

A guess, this plan's own and not a measurement: a probe in Python is one to three days for an author who already solves
this model in the toolkit; the experiment adds a day or two of the author's attention, most of it reading
disagreements; an author in another language can reach a probe once the kit exists and until then faces the hand-written
file. The first outside onboarding should be measured, the author's own account of their hours kept in the records and
never published beside the toolkit, where it would read like a toolkit's timing.

### The organizer's side

- **Before anything is sent.** Extend `schemas/experiment.schema.json`, `schemas/checker/experiment.py` and
  `schemas/checker/test_experiment.py` so that an experiment can compare a toolkit's effective member with the stated
  member and expect agreement within the toolkits' own convergence (the validator's enumerations admit neither today);
  this is a schema change and is listed among the decisions. Rewrite
  `schemas/bst/experiments/restrained-limit/experiment.yaml` as version two, dropping the check that two toolkits share
  an effective member, and give the two new checks a floor: a distance or residual at or below a stated round-off level
  passes at any level, so a representation that reproduces the closed forms is not failed for a distance that cannot
  fall; and a check whose quantity does not change across a toolkit's levels (a ladder whose levels change only
  method-only settings) is reported as not applicable, never failed; with the thirteen-break test's counterparts for
  both cases. Run the adapters' independence and record it, so that the reference runs no longer share nodes and
  grids; fix the stale strings (the old driver paths and `bst-1` links); push the branch at a named commit and name the
  first author and the vehicle (the owner's, as the deferred item of 2026-11-03 records).
- **The kit** (*proposed*), at `harness/kit/`, inside the harness piece: carved from the toolkit-neutral parts of
  `harness/adapters/common.py` before the adapters' independence strips that module: reading and checking the member
  and the request; the hashes by the canonical hasher's one implementation; the special points found as roots on the
  rule through `evaluate`; the pooled blocks; the provenance; the writing of the three files; and an Euler-residual
  cross-check at the request points by the verifier's Gauss-Legendre quadrature of the stated laws, evaluating the
  toolkit's own interpolant through `evaluate` and never an exported rule, recorded beside the toolkit's own required
  residuals and never in their place. Why not the export: on the committed files at the finest level,
  linear interpolation of the exported rule differs from the reported c at the request points by about 3e-5 for both
  toolkits, read on 2026-11-03; that is below their residual under the stated laws there, about 2.1e-4, and far above
  their residual under their own laws, under 1e-6, so a residual from the export would carry the export's error. The effective member's derived parameters and the conditions block stay the
  toolkit's own report, as the rulings of 2026-10-18 require: the kit offers the checker's arithmetic as a library the
  author runs and declares in the card, and records its own recomputation beside the author's values with any
  discrepancy on the ledger, so that the checker's verification of the factors stays a check of the toolkit's report and
  not of organizer code against itself. Three commands: `assemble`, `verify` (a wrapper on `check.py --verify-results`
  that also recomputes the method, settings and request hashes from the files beside the results file and compares the
  file's comparison points with the request file's, refusing a mismatch) and `compare` (a wrapper on
  `compare_toolkits.py` at the request points, which today serves the restrained-limit experiment only). The kit wraps
  the checker and adds nothing to what the checker verifies, so the gate and the writer stay two programs, as PrePARE and
  CMOR were. Every block the kit can compute may be supplied by the toolkit instead, declared in the card, and then the
  kit's recomputation is recorded beside the author's value with the discrepancy on the ledger, never replaced.
- **The two-command protocol over files** (*proposed*), specified in the kit's README: `solve <member> --level <name>
  --out <dir>` writes to the directory a small JSON holding the expectations the family names, the lowest values, the
  lower limit, the derived parameters the toolkit used and the exported rule; `evaluate <dir> <points file>` reads a
  JSON array of points and writes the arrays c, mpc and value (null where the toolkit keeps no value) for all points in
  one call; the kit guarantees batching, so the kink and target root finds and the quadrature cost a handful of calls,
  never one subprocess per point. The syntax follows Bowtie's command-per-request protocol with JSON on files in place
  of line-delimited JSON on standard streams, which is a coined departure and needs a ruling under the existing-syntax
  rule. A toolkit outside Python records a minimal provenance in place of a uv lock file: the language's own lock or
  manifest file, or a version list under the provenance's environment object, kept in the manifest beside the bundle's
  hash.
- **A hash command** (*proposed*): `check.py --hash <file>` prints the canonical hash of any strict-YAML file, with a
  test that it reproduces the `method_file_sha256`, `settings_sha256` and `request_file_sha256` values in the committed
  results files. Today no command hashes a method, settings or request file: `canonical.py` has no command line,
  `check.py` hashes only the member, and `file_hash` lives inside the adapters' shared module, so the by-hand path and
  every non-Python path lack a tool they need.
- **The population block.** By default it stays the toolkit's own: generalized Lorenz ordinates, quantiles, the mass at
  the constraint, the MPC statistics and the stationarity residual computed inside the toolkit from its own stationary
  distribution, as the rulings of 2026-10-18 require and the validator demands. The blocks behind a status (`value`,
  `undefined`, `not computed`) are the kink, the target, the pseudo-target, the income-measure block, welfare, marginal
  welfare and the quantiles; the population block, its ordinates and statistics, the stationarity residual's population
  number, the Euler residuals and the conditions block carry none and are required of every type. A toolkit with no
  stationary-population routine or no second quadrature of the stated laws therefore cannot produce a valid probe at
  all; a block-level status for the population block, the stationarity residual and the Euler residuals is listed among
  the decisions as a schema change routed to the HARK and HAFiscal sessions first. Offered, pending the owner's word:
  the toolkit's stationary population as weighted points (a grid method's nodes with masses, a simulation's agents with
  equal weights, with agents, periods, burn-in and seed) as a never-published kit input, so that one code computes the
  block for every toolkit and one forward step under the stated laws gives a stationarity residual that tests
  stationarity, where every committed file's residual today is one forward step of the adapter's own lottery
  transition on the reported distribution, from under 1e-14 to about 2.5e-10. Until then the ledger says that the
  stationarity check bites only on iterated and simulated distributions. The estimator of the generalized Lorenz
  ordinates and quantiles from a weighted set is pinned nowhere: `results.md` defines GL(p) through the quantile function
  without a convention for a discrete weighted set (the atom at the constraint and its ties, the quantile's
  interpolation, the 0.999 ordinate, how the top is chosen), so an outside toolkit's own estimator differs from the one
  `common.py` implements and ordinate differences mix estimator with solution. Proposed: write into `results.md` the
  estimator `gl_ordinates` and `quantiles` implement, with the estimator's own difference stated as a tolerance; or,
  if the owner admits weighted points, make the kit's computation the one estimator.
- **The ingest path** (*proposed*): a registry entry of kind `submission` (a bundle path and a levels map, no
  environment), an extension of the existing `harness/toolkits.yaml` entry rather than a new file kind, and a short
  adapter on the pattern of `harness/test_support/stub_adapter.py`, so that the runner's `verify` and the comparator
  treat a submitted folder exactly like a harness run and the run folder's manifest records the bundle's hash. The
  runner's `verify` gains the same three-hash and comparison-point check as the kit's, for harness runs too, since the
  checker's `verify_results` today checks the parameter-file hash only and only `compare_toolkits.py` asserts the points.
  The ledger marks such rows as submitted-only; a submission entry is never silently promoted.
- **The expected file** per member (*proposed*), on the SBML Test Suite's expected-results convention: written by
  command, never by hand, from the checker's closed forms of the stated member (expectations, factors, verdicts,
  implications), with a changelog; and, after the adapters' independence has run, the values at the request points that
  two independent toolkits agreed on with the band they agreed within and its provenance, marked informative.
  Continuous integration (*proposed*; the only workflow today, `.github/workflows/publish.yml`, builds the site and runs
  no tests) runs the test files and the checker on every member, request, expected and experiment file on every change,
  so that no curated file goes stale.
- **The ledger** (*proposed*), generated by the comparator from verified results files, as a table and as JSON on the
  pattern of Bowtie's report and the web-platform-tests dashboard: one row per toolkit, member and check, with the
  numbers behind each verdict and the movements between levels printed beside each agreement verdict. Each difference
  between two toolkits is classed as within the toolkits' own convergence, a difference of regime (opposite verdicts on
  a condition, both factors shown), a difference of method (dolo's segment-slope MPC, a kink read differently), or a
  disagreement to trace. A block reported `not computed` is a gap, never a failure. A one-level entry is verified, not
  placed. Harness-reproduced rows and submitted-only rows stay distinguishable in every table and figure. No score, no
  ordering; a time, recorded since the ruling of 2026-11-04, shown with its machine and settings. The two toolkits whose adapters the organizer wrote, HARK (econ-ark's) and dolo (EconForge's), go
  through the same gate and are marked as such. A toolkit's first rows appear after its author has seen them, and a
  failed check is sent to the author as compatibility information before any publication. The ledger is kept per family
  version, with one set of rows per toolkit version.
- **Disputes.** The organizer decides a difference's class and publishes the numbers behind it. The author sees the row
  before publication and may contest its class within the comment window; an unresolved contest is shown on the ledger
  as contested, with both readings and both toolkits' movements between levels. The deferred method-only ladder at fixed
  nodes is the named remedy for two toolkits that both pass while disagreeing. The multiplier k of about two or three in
  the stone README is fixed in `results.md` by proposal. Conduct follows the working group's code of conduct, linked from
  the page.
- **Refusals.** `check.py` exits 1 with a list of problems, and the page distinguishes three kinds. A refusal by design:
  a lowest value below the stated infimum (nodes beyond the truncation bounds), or a factor that is not the arithmetic
  of the reported expectations; not a defect but a representation to change or declare. A suspected checker or schema
  defect: reported in an issue labeled for the checker, recorded in `schemas/records/defects.md`, answered by the
  organizer within a stated window. A plain file error: a wrong hash, a missing key. An effective member that fails a
  validity condition the stated member passes is reported, not refused, as `conditions.md` reads it (a discretization
  too coarse).
- **Certified values** (*proposed*) for `bst-restrained` by two methods independent of HARK and dolo, as NIST certifies
  reference values, published beside the checker's closed forms; until then the closed forms are the only certified
  reference and the Euler residual under the stated laws the only check that trusts no toolkit.
- **The stone's skeleton**, generated from the card, the method file and the verified runs: the lexicon's
  parameter-key rows from the card, the stage-parameter rows from the parameter-key rows by the map `test_rosetta.py`
  already holds (eight stage names collapse onto two law symbols), the results-object rows from the writer, the methods
  table from `methods.yaml`, the evidence from `verification.json` and the ledger; the cards exported from the same
  source for the stone registry's intake, with the bellman session confirming the export's fields; `test_rosetta.py`
  discovers stones and admits a card-only stone. The findings record stays hand-written, as the approved harness plan
  states: the harness gives the numbers and a person says what they establish. The kit may print a table of a run's
  numbers for the record to cite, which is listed among the decisions because of its bearing on the memory that says
  what tests establish; the author's paragraph of judgment, signed by handle, is part of the record.
- **The reading guide** (*proposed*), `schemas/bst/reading-a-stage-file.md`: one page on the syntax the two stage files
  use (declarations, laws, functions with ids, the three perches and their marks, the annotations, derivative terms),
  drawn from `schemas/bst/model.md`'s reading of the stage files and the ontology README's public explanation of the
  language's terms, stated as the schemas' own rules, citing nothing private, naming the commit it reads and tested so
  that every parameter and target it names exists in `natural.bl` and `artificial.bl`.
- **Versioning of the model statement.** The family key carries a version (`bst-artificial/1`), but no document says
  what increments it, the stage files carry no version string, and the parameter hash covers the parameter file only.
  Proposed rule: a change to a stage file, a parameter validator, a condition or a derived parameter that could change a
  verified result makes a new family version, with the old version's documents and members kept; a results file records
  the stage file's hash, which is a change to results content and goes to the HARK and HAFiscal sessions first; the
  ledger is per family version, and verified files stay valid for theirs.
- **The results schema's release.** A release number named in every results file, with a changelog. A new required key
  applies only to files naming the new release or later; the validator keeps each release's rules (one validator with a
  release-conditioned required list, or one validator per release); the test suite keeps the committed files of
  2026-11-01 validating. Without this, the distributions of permanent income and of wealth in levels, which the results
  document marks as required blocks behind a status, would fail every committed file the day they enter the validator.
  The release field goes to the HARK and HAFiscal sessions with this gating rule.
- **Resource envelope.** Per harness job: the thread cap the runner sets today, a memory limit and a time cap, stated in
  `harness/README.md`; a job that exceeds them gets the status not run within the limits, recorded in the manifest and
  shown on the ledger as a gap, never as a failure of the toolkit. This is the organizer's execution limit, as
  competitions and BenchExec publish theirs, not a toolkit's timing.
- **An experiment with large outputs,** such as Jacobian matrices and a joint file that stay out of git with hashes in
  the results file. Proposed: a large-file rule for submissions (hashes in the results file, the files sent by a stated
  means, kept outside git, verified against their hashes on receipt); tiered participation (the steady state, the
  distributions and the joint required, the Jacobians behind a status, so a toolkit without Jacobian machinery may
  take part); and the memory the harness offers stated. The experiment that first raised these is with the
  HAFiscal-Latest repository since 2026-11-04, until it is ready.
- **Registration and identifiers.** The working group already registers toolkits by an issue form
  (`.github/ISSUE_TEMPLATE/register-toolkit.yml`, feeding the Community Library's directory), which the existing-syntax
  rule reaches first; the decision is whether that form, extended with the card's fields, is the registration channel,
  or why a pull request replaces it. One identifier spelling, as CMIP's `source_id` vocabulary does, used in the registry
  key, the results file's `toolkit.name`, the stone's filename, the findings folder and the ledger, with a test; today
  the registry keys are lowercase, the committed files carry `HARK` and `dolo`, and the findings folders spell their own.
- **Lifecycle.** One set of ledger rows per toolkit version. A re-pin is a registry change by pull request from the
  author or the organizer, with a rerun; old rows stay, marked by version. Withdrawal on the author's request removes
  the rows from the ledger while the records' history stays, which the page says. A pin that stops resolving (the
  harness plan names HARK's fork commit as a risk) marks its rows as no longer reproducible.
- **Attribution.** The toolkit by its registry identifier and its own citation; the author by GitHub handle only, with
  consent given in the card; the author's paragraph signed by handle; no email addresses in the repository, as the
  working group's issue forms already say.
- **License.** The repository root has no LICENSE file; only the two ontologies carry CC BY 4.0. Nothing states the terms
  under which a submitted results file, method and settings files, card, stone text and adapter code are published, nor
  the terms under which an author uses the checker, the kit, the schemas and the reference files. Proposed: a code
  license at the root for the checker, kit, harness and adapters, and a data license for results files, stones and
  findings (the ontologies' CC BY 4.0 is the existing choice), stated on the page before the author sends anything, the
  author granting the data license on submission. Closed-source and commercial toolkits are admitted to the probe and
  the experiment submission, pinned by a version string and a binary hash; whether a closed binary may be
  harness-reproduced is the owner's decision.
- **One spelling of each thing.** The method file is the source of the cards' methods list and the stone's table; the
  ladder file is merged into the settings file's named elements and the registry's levels map; the design documents
  point at the rulings file instead of restating the rulings; a run's numbers live in the findings record and the stone's
  evidence points at it.
- **Governance** written as a records entry (*proposed*): the owner as the schemas' owner and the organizer, running the
  comparison from the fork `llorracc/sce-wg-1-dev` until the route to the working group's repository `econ-ark/sce-wg-1`
  is started, which is the owner's to start; whether participation needs working-group membership, which is by
  invitation; a change by proposal with its consequences, the toolkits' sessions consulted on results content, a stated
  comment window that also covers a contested ledger row; the release and family-version rules above; the registration
  channel; the toolkits whose adapters the organizer wrote marked and, as SMT-COMP and MiniZinc do for organizers'
  entries, ineligible for anything a ledger could be read as awarding, which here is nothing, since there is no score;
  no ranking restated for participants, the rule against run times revoked on 2026-11-04; the private channel and the rule that no probe number is posted
  in a public issue or committed to the records.
- **The method vocabulary** stays in `schemas/` and deferred: tags as methods where the stage has one, the handler
  naming the routine, toolkit-prefixed words only where no tag fits, until two toolkits claim one shared method; it does
  not move under `ontologies/`, where toolkit names would breach the ruling that the ontology names no toolkit.
- **Toolkits outside Python.** Until the owner adopts a container convention (an image built from a file under
  `harness/adapters/<toolkit>/env/` that the runner invokes in place of `uv run`), such a toolkit can reach a probe and an
  experiment submission but cannot be harness-reproduced; the page says so. Such an author runs Python once per file,
  for the checker and, once it exists, the hash command; before the kit exists, that author faces the by-hand path.

### What each existing component becomes

| component | verdict | what changes |
|---|---|---|
| stage file (`.bl`), one per family | keep | normative by ruling; read once beside `model.md`; the reading guide (*proposed*) beside it; which statement a participant is held to is the owner's decision; a family version rule (*proposed*) |
| parameter file and its canonical hash | keep | unchanged; the author never writes one for the restrained-limit experiment |
| parameter validators, shock-law validator | keep | organizer-run through the checker and, *proposed*, continuous integration |
| results file (JSON) | keep | content unchanged by this plan's core; who assembles the arithmetic blocks changes; the release field and the stage-file hash are separate proposals put to the toolkits' sessions |
| results validator | keep | the gate's first half; release-conditioned required lists, once consulted and approved; the errors tree and the free-text `representation` field offered to the author on the page |
| request file | keep | organizer-written by `make_requests.py`; the author reads the points only |
| method file (`methods.yaml`) | keep | separate from settings by ruling; the one spelling of the seven entries; the tag as the method where one exists, the handler as the routine; the template in `numerics.md` gains `arvl_to_dcsn` by proposal |
| settings file and the named levels | keep | a flat map of plain values with a `level` key, the author's own; the hash's input |
| ladder file | merge | into the settings file's named elements plus the registry's levels map; a change to `schemas/numerics.md`, so a proposal |
| method registry | defer | until two toolkits claim one shared method; stays in `schemas/` |
| validators for method, settings and request files | defer | a shape-only check for settings built with the adapters' independence; the rest when needed |
| experiment file and its validator | keep | the validator extended (a schema change, among the decisions) and the restrained-limit experiment rewritten as version two with floors before anything is sent |
| report scripts (`compare.py`, `compare_toolkits.py`, `make_requests.py`) | keep | the kit's `compare` wraps `compare_toolkits.py`; both fold into the comparator |
| Rosetta Stone document | keep, in two stages (*proposed*) | the capabilities section first, as the card; the lexicon, handlers and evidence after the first verified run on a generated skeleton; waits on the owner's account of a stone's scope |
| QuantEcon-JAX stone and cards | decide | no adapter, no registry entry, no run; still checked by `test_rosetta.py`; under the ruling that no QuantEcon module is published it becomes a card-only stone or is retired to the history |
| HAFiscal's emitter | decide | a third producer of results files in the schema's form, private, at a retired family key; registered as a submitted-only entry once it writes the current family keys, or kept outside the ledger, as the owner decides |
| cards file in the stone registry's fields | generate | by the organizer from the stone and the method file; never asked of an author |
| adapter with the fixed command line | keep, at the integration | the one artifact nothing can generate; for Python, the `Toolkit` protocol's four functions and seven strings; for other languages, the kit's two commands wrapped by the organizer |
| shared adapter module (`common.py`) | merge | split into the kit (toolkit-neutral reading, hashing, writing) and, pending the owner's word, a declinable numerical library (nodes with exact conditional means, the lottery population, the conditions' arithmetic) a toolkit may call and must declare |
| toolkit registry (`harness/toolkits.yaml`) | generate | written by the organizer; gains entries of kind `submission`; one identifier spelling with a test; the registration channel decided against the existing issue form |
| toolkit environment (uv project) | generate | locked by the organizer from the author's requirement list and interpreter; a container convention for other languages is a proposal; a closed binary's reproduction is a decision |
| run folder artifacts | keep | an ingested bundle lands in the same layout with its hash and, for other languages, its manifest in the run manifest |
| Jacobian files and the joint-distribution file | defer | an experiment's that needs them, with the HAFiscal-Latest repository since 2026-11-04; the joint as weighted points is the unanswered proposal of 2026-11-02; the large-file rule and the tiers above |
| checker | keep | the only gate; gains `--expected` and `--hash` commands (*proposed*); the kit wraps it; `verify` recomputes the three file hashes and the comparison points |
| model, conditions and results documents | keep | the author's reading of the hub; stale strings cleaned; `results.md` gains the GL estimator and k by proposal |
| design documents and plans | keep | off the author's path; pointing at the rulings file instead of restating it |
| conventions registry | keep | organizer-side |
| author's briefing (`for-toolkit-authors.md`) | rewrite | the afternoon's draft replaced at the same path by the page drafted with this plan |
| HARK's gate script with private references | keep | organizer-side; never on the author's surface |
| test files | keep | run in continuous integration (*proposed*); `test_rosetta.py` discovers stones |
| ontologies | keep | the deliverable; off the author's path; their CC BY 4.0 the model for the data license |
| records | keep | findings records hand-written from the run folder with the author's signed paragraph; a governance entry added; a refusal route into `defects.md` |
| findings page source | keep | regenerated per run; captions say what each picture computes |
| git guard hook | keep | unchanged |
| license | add (*proposed*) | a code license at the root and a data license for results, stones and findings, decided by the owner |
| encode: the laws under the stated convention, the atom and scale, the types, the newborn | keep | the author's irreducible task; a declinable library lowers its cost without prescribing a representation |
| effective-member block: expectations, lowest values, derived parameters | keep | the author's own report, the checker their reference; the kit's recomputation recorded beside |
| conditions block | keep | the toolkit's own report of every factor and verdict, as both rulings of 2026-10-18 require; the checker's arithmetic offered as a declinable library the author runs and declares; the kit's recomputation beside |
| the rule at the request points and the exported rule | keep | the author's; the MPC as the toolkit's own derivative, returned by `evaluate` |
| special points | generate, declared | roots on the rule through `evaluate`, statuses from the toolkit's verdicts; the author may supply their own, and then the kit's are recorded beside |
| population block, income-measure block, stationarity residual | keep | the toolkit's own by default; computed by the kit from weighted points if the owner admits that input; a block-level status is a decision |
| welfare and marginal welfare | keep | behind statuses; `not computed` admitted |
| Euler residuals under the stated laws | keep, cross-checked | the toolkit's own, required; the kit's through `evaluate` with the verifier's quadrature recorded beside, never in place; a block-level status is a decision |
| pooled blocks | generate, declared | share-weighted arithmetic |
| identity and provenance | generate | hashes, hardware and threads by the kit or the runner; the version pin the author's; the run time with its machine and threads in the run registry since the ruling of 2026-11-04, not in the file; no machine name or operating system in the file |
| running the restrained-limit experiment through the harness | keep, organizer-run | the author's local run is a self-test; the organizer's run in a locked environment, within the stated envelope, is the record |
| findings record per toolkit | keep, hand-written | the harness gives the numbers, a person says what they establish; the author's paragraph signed by handle |

### Acceptance

The kit is accepted when it assembles HARK's and dolo's committed files at low byte for byte from their solve outputs and
refuses a mismatch of any hash or of the comparison points. The ingest path is accepted when a bundle of the committed
files runs through `verify` and the comparator as a submitted-only row with the bundle's hash in the manifest. The ledger
is accepted when its verdicts and numbers on the committed runs match the prototype's and `compare_toolkits.py`'s. The
hash command is accepted when it reproduces every method, settings and request hash in the committed results files.

## How it honors the owner's rulings

- 2026-10-17: the artifacts are schemas; the points at which a rule is reported live in a request file, not in the
  schema; levels are optional and named in words; the export of the rule is required. All kept; the request file and
  the exported rule stay required of every author.
- 2026-10-17 and 2026-10-18, standing: one written form of a member and the canonical hash as its identity. Unchanged;
  the author never edits a member for the restrained-limit experiment.
- 2026-10-18, morning: methods and settings are separate schemas; an ergodic-distribution measure and the target are
  required results. Both files stay; the population block and the target stay required; a block-level status for the
  population block is a decision put to the owner, not a change made here.
- 2026-10-18, 10:35: the truncated lognormal's convention; Euler and stationarity residuals required of the toolkit.
  Kept; the kit's residual through `evaluate` is a cross-check recorded beside the toolkit's own, never in its place; a
  substitution would be a change to what a toolkit must compute and would go to the HARK and HAFiscal sessions first.
- 2026-10-18, 14:21, standing: propose before changing a schema, with consequences. This plan is a proposal; nothing in
  it is applied; the pieces that change a schema are listed as the owner's decisions, the experiment validator's
  extension among them.
- 2026-10-18, 17:30:27: the stage file is the normative statement; a method file names the stage's targets. The stage
  file stays normative and is read once beside `model.md`; `methods.yaml` keeps the seven targets.
- 2026-10-18, 18:28:39: levels are settings, not error targets. The page says so; no level promises accuracy.
- 2026-10-18, 21:54:41: the derived parameters a toolkit used are reported, the checker their reference. Kept as the
  toolkit's own report: the problem the ruling names, a toolkit taking its natural limit from its discretized minimum,
  is visible only if the toolkit reports what it used; the kit's recomputation from the reported lowest values is
  recorded beside it, never in its place.
- 2026-10-18, 22:08:10 to 22:41:43: the effective member; no discretization prescribed; no form of the representation
  required; the toolkit reports the expectations its conditions rest on, its lowest values, every condition's factor
  and its verdicts. Kept as the toolkit's report; this plan's one change is that the checker's arithmetic is offered as
  a library the author may run and must declare, with the kit's recomputation beside; the weighted-points input is
  offered and never required, and the default keeps the population block the toolkit's own.
- 2026-10-19, 10:03:43: adopt existing syntax from few sources. The card is the stone's first section and the method
  and settings files stay as they are. Four kinds are new, each named with its convention or marked for a ruling: the
  expected file follows the SBML Test Suite's expected-results files; the ledger's table and JSON follow Bowtie's report
  and the web-platform-tests dashboard; the `submission` registry entry extends the existing registry file; the
  `evaluate` exchange, JSON on files on Bowtie's command-per-request pattern, is coined and needs a ruling.
- 2026-10-20 and 2026-10-21, standing: what a results file carries is put to the toolkits' sessions first. The results
  file's content is unchanged by the core of this plan; the release field with its gating, the stage-file hash, a
  block-level status and any substitution of a kit computation for a toolkit's required one go to the HARK and HAFiscal
  sessions before they are drafted; dolo has no session, which is said.
- 2026-10-21, 07:39:20: stones are shaped like the stone registry's cards so that the bellman session can turn them
  into cards. Kept; the cards are the organizer's export and the bellman session confirms the fields.
- 2026-10-21, 08:27:33, revoked on 2026-11-04 (times recorded since, with their machine and settings): no run times anywhere. No timing on the page, in the ledger or in a results file; the
  first onboarding's hours stay in the records and are never published beside the toolkit; the harness's execution
  limits are the organizer's envelope, not a toolkit's timing.
- 2026-10-21, 12:14:52, standing: checkable sources only; nothing private cited by identifier. The reading guide is
  stated as the schemas' own; the page cites only public paths.
- 2026-10-21, 20:36:49: the modules are adapters living in this repository, a parameter file in and a results file
  out. Kept at the integration; the probe is a results file produced the author's own way, which the stub adapter's
  pattern already admits.
- 2026-10-21, 23:03:44 and 2026-10-22, 10:45:11: provenance carries only what the schema asks for; a toolkit is pinned
  by commit or release. Kept; a closed toolkit's pin is a version string and a binary hash; another language's manifest
  sits in the run manifest, not in the results file.
- 2026-10-22, 15:11:02, standing: a method-free stage file; tag versus handler. Kept; where a computation has a tag the
  method is the tag and the routine is the handler, as the committed method files write them; words only where no tag
  fits.
- 2026-10-22, 18:06:54: the natural limit from the laws' infima, never from the lowest node. Kept; the checker verifies
  the lowest values against the infima, and the toolkit reports the limit it used.
- 2026-10-22, 21:42:05: the route to the working group's repository is the owner's to start. Nothing here starts it;
  the page says the comparison is run from the fork until it is.
- 2026-11-01, 09:23:51, standing: the ontology names no toolkit. The method vocabulary stays out of `ontologies/`.
  Among that day's open points, what belongs in a stone, on which the owner offered a fuller account; the two-stage
  stone waits on it.
- 2026-11-01, 18:22:40: a result whose point is a shape goes as a picture built from the results files. The ledger's
  figures are regenerated per run.
- 2026-11-01, 18:46:57 and 19:05:20: a toolkit's stone first, then a pause, then the adapter and the runs. Kept in
  reduced form: the stone's capabilities section comes before any code and the organizer answers it; the rest of the
  stone follows the first verified run. The ruling was made for dolo's stone; whether the reduced form satisfies it is
  the owner's decision.
- 2026-11-01, 12:50:56, standing: reaching the limit, not binding; where binding is said, it is defined once. The page
  defines it once in `conditions.md`'s sense.
- 2026-11-01, standing: say what a test establishes; a result counts as untested unless a results file checks it. The
  ledger's rows carry the numbers behind each verdict; the findings record stays hand-written; a probe is recorded in no
  finding.
- 2026-11-02, 09:48:03: four pieces, an intercomparison on the climate pattern. The kit lives inside the harness piece;
  nothing is moved between pieces.
- 2026-11-02, 10:33:47: the layout, lock files from the start, large outputs out of git. Kept; a submitted-only row is
  marked as such because it has no lock file, and only a harness-reproduced run becomes a finding; an experiment's
  large files stay out of git under the large-file rule.
- 2026-11-02, 18:24:32: a memorial is a commit, not a push. Nothing is pushed or sent by this plan.
- 2026-11-02, 18:28:43 and 19:09:13: the harness gives parameters only; the representation is each toolkit's; what the
  harness asks for; discussion before anything is built. The kit offers and never insists; the declinable library is a
  decision put to the owner against the adapters' independence plan; a shared grid, if an experiment asks for one, is put
  to the owner against this ruling; this document is the discussion.
- 2026-11-03, 04:37:53 and 05:12:27: no survival-based validity condition; the distribution blocks are a proposal. No
  condition is reintroduced; the blocks stay proposals, and the release gating keeps them from failing committed files.
- 2026-11-03, 17:59:50: two families. The page names two.
- 2026-11-03, deferred: the vehicle and the author are the owner's. Nothing is sent.
- Standing: the repository is public; the owner's words stay outside it; documents and their parts get names, never
  numbers; American English. Observed throughout; the experiment is named restrained-limit, with
  first and second used only where the order of running is the point.

## What changes in the repository if approved

In order, each a commit with its record:

- First, the prerequisites that no author may be sent before: once the owner has ruled on the validator's extension,
  extend `schemas/experiment.schema.json`, `schemas/checker/experiment.py` and `schemas/checker/test_experiment.py` with
  the comparison against the stated member, the expectation of agreement within the toolkits' own convergence, the
  round-off floor and the not-applicable outcome; rewrite `schemas/bst/experiments/restrained-limit/experiment.yaml` as
  version two and its `README.md`; run the adapters' independence (the three pending decisions plus the library
  decision below) and record the finding; clean the stale strings in `schemas/effective-member.md` and wherever the old
  driver path appears in prose.
- Commit `schemas/participation.md` (this plan), the precedents record and the revised `schemas/for-toolkit-authors.md`,
  in the tree uncommitted since 2026-11-03 with their lines in `schemas/README.md`'s contents map, in
  `schemas/records/MEMORY.md`, the journal and the deferred list.
- Add the license files the owner chooses, at the root and for the data.
- Add `check.py --hash` with its test; add `harness/kit/` with `assemble`, `verify` and `compare`, the two-command
  protocol over files and its README, carved from `harness/adapters/common.py`'s toolkit-neutral functions; update
  `harness/README.md` with the execution envelope and `harness/adapters/README.md`; sequence this before the module is
  stripped.
- Add `harness/adapters/submission/adapter.py` on the stub adapter's pattern and the `submission` kind to
  `harness/toolkits.yaml` and `harness/runner.py`, with the three-hash and comparison-point check in the runner's
  `verify` and a test in `harness/test_runner.py`; fix one identifier spelling with its test.
- Add `schemas/bst/reading-a-stage-file.md` with a test that pins it to the stage files' declarations.
- Add `check.py --expected` and the expected files under `schemas/bst/experiments/restrained-limit/`, with a continuous
  integration workflow that runs the test files and the checker on every member, request, expected and experiment file.
- Change `rosetta/README.md` to describe the stone's two stages and the card, after the owner's account of a stone's
  scope; change `schemas/checker/test_rosetta.py` to discover stones and admit a card-only stone; add the generator of
  the stone's skeleton and the cards' export; settle the QuantEcon-JAX stone.
- Change `schemas/numerics.md`: the ladder file merged into the settings elements and the registry's levels map; the
  method file's template with the `arvl_to_dcsn` entry; the method registry deferred. Change `schemas/bst/results.md`:
  the GL estimator written out, k fixed.
- After consulting the HARK and HAFiscal sessions: the results schema's release field with release-conditioned required
  lists, the stage-file hash, and any block-level status, in `schemas/bst/results.schema.json` and
  `schemas/bst/results.md`, with a changelog and the test that the files of 2026-11-01 still validate.
- Add the governance entry under `schemas/records/rulings/` once the owner has ruled on it, and the comparator (the
  harness plan's stage after the adapters' independence) with the ledger's generator from the findings page source.
- Add the container convention for `harness/adapters/<toolkit>/env/`, adopted on 2026-11-04 through REMARK's machinery (`registry.md`), with the runner's change; and the
  large-file rule and tiers when an experiment with large outputs is delivered.

## The decisions the owner must make

Each decision, what it blocks, who is consulted first, and the proposed order of asking.

| order | decision | blocks | consulted first |
|---|---|---|---|
| 1 | the governance entry: the owner as organizer running the comparison from the fork; whether participation needs working-group membership; the comment window; the private channel; the registration channel (the existing issue form extended, or a pull request); the toolkits whose adapters the organizer wrote marked and ineligible for anything a ledger could award | the page's What this is and Where to ask sections; the lifecycle and dispute rules | nobody |
| 2 | the license: a code license at the root, a data license for results, stones and findings (CC BY 4.0 is the ontologies' choice); closed-source toolkits admitted to the probe and the experiment submission with a version string and a binary hash; whether a closed binary may be harness-reproduced | sending the page to anyone | nobody |
| 3 | the experiment validator's extension (comparison against the stated member, agreement within the toolkits' own convergence, the round-off floor, not applicable), a schema change | version two of restrained-limit; the adapters' independence; every stage | nobody; a schema-document proposal under the standing rule |
| 4 | whether `common.py`'s nodes with exact conditional means, its lottery population and the conditions' arithmetic stay as a declinable library a toolkit may call and must declare, instead of being deleted as the adapters' independence plan proposes | the adapters' independence; the kit | nobody |
| 5 | whether a results-only probe is admitted (verified, compared, reported back through the private channel, recorded in no finding, on no ledger row, its files outside the repository and deleted on request), and whether a verified experiment submission may appear on the ledger as submitted-only, with only a harness-reproduced run becoming a finding | the ingest path; the page's first stage | nobody |
| 6 | whether the entry member is `bst-restrained` at one level, and whether the experiment tier needs two levels or three | the page | nobody |
| 7 | whether the kit may assemble, from the toolkit's reported expectations, lowest values and rule, the special points, the pooled blocks and the hashes, declared by the author and recorded beside any value the author supplies; the derived parameters and the conditions block staying the toolkit's own report with the kit's recomputation beside; the kit's Euler residual a cross-check beside the toolkit's required one | the kit | the HARK and HAFiscal sessions, since the kit changes who computes what |
| 8 | whether the kit lives at `harness/kit/` inside the harness piece and wraps the checker, so that the gate and the writer stay two programs; and whether the `evaluate` exchange, JSON on files on Bowtie's pattern, is admitted as coined syntax | the kit | nobody |
| 9 | the block-level status on the population block, the stationarity residual and the Euler residuals, a schema change, with the kit's computation from the author's weighted points as the alternative; and whether the toolkit's stationary population as weighted points may be a never-published kit input (touching the rulings of 2026-10-18 and the unanswered joint proposal of 2026-11-02) | the kit's population path; a non-Python probe from a toolkit without a stationary-population routine | the HARK and HAFiscal sessions |
| 10 | whether a results file names the results schema's release, with release-conditioned required lists, a changelog, the promise that a later release never invalidates a verified file and the test that the files of 2026-11-01 still validate; and whether it records the stage file's hash under a family-version rule | the distribution blocks' entry into the validator; the ledger per family version | the HARK and HAFiscal sessions |
| 11 | which statement a participant is held to while the stage file's language has no public documentation: the stage file read through the reading guide at a named commit, or `model.md` with the parameter and results schemas; and whether to ask the private project, through the bellman session, for a public rendering of the subset the stage files use | the reading guide; the page's What you receive | the bellman session, for the rendering |
| 12 | whether the stone-first order of 2026-11-01 is satisfied in reduced form by the stone's capabilities section (the card) before any code, with the lexicon, handlers and evidence following the first verified run on a generated skeleton; this waits on the owner's account of what a stone holds; and whether the QuantEcon-JAX stone becomes card-only or is retired | the stone stage; `rosetta/README.md`; `test_rosetta.py` | the bellman session, on the cards' fields |
| 13 | whether the findings record stays wholly hand-written or may cite a table of numbers the kit prints, with its consequence for the memory that says what tests establish | the stone's evidence section | nobody |
| 14 | whether the ladder file is merged into the settings elements and the registry's levels map, the method file's template gains `arvl_to_dcsn`, and the method registry and the method, settings and request validators stay deferred; changes to `schemas/numerics.md`; and whether `results.md` gains the GL estimator and k | the page's template pointer; the ledger's tolerances | nobody; schema-document proposals |
| 15 | whether a container convention is adopted for toolkits outside Python, and until then whether the page says plainly that such toolkits reach a probe and an experiment submission only; and the execution envelope (threads, memory, time) per harness job | the integration for other languages; `harness/README.md` | nobody |
| 16 | whether the ledger is organizer-run with the four difference classes, discrepancies shown, gaps never failures, one-level entries verified but not placed, the organizer's adapters' toolkits marked, no score, times with their machine and settings since the ruling of 2026-11-04, a toolkit's first rows appearing only after its author has seen them, contested rows shown with both readings, rows per toolkit version with withdrawal and broken pins marked; and the attribution rule (toolkit by identifier and citation, author by handle with consent) | the comparator; the page's reporting section | nobody |
| 17 | whether certified values for `bst-restrained` are computed by two methods independent of HARK and dolo | nothing; an improvement to the reference | nobody |
| 18 | withdrawn on 2026-11-04: the experiment it concerned moved to the HAFiscal-Latest repository until it is ready; its terms return with it | nothing | nobody |
| 19 | whether HAFiscal's emitter is registered as a submitted-only entry once it writes the current family keys, or stays outside the ledger | the ledger's third row | the HAFiscal session |
| 20 | the vehicle and the first author, and whether the page waits for the kit and the comparator or goes out with their status marked as proposed; nothing is pushed, sent or published before the owner's word | sending anything | nobody |

## Sources

Addresses fetched in the precedents' research of 2026-11-03; the precedents record carries the full list.

- Eyring et al. 2016, CMIP6 overview: https://gmd.copernicus.org/articles/9/1937/2016/gmd-9-1937-2016.xml
- Guide to CMIP6 participation for modeling groups: https://pcmdi.llnl.gov/CMIP6/Guide/modelers.html
- CMOR: https://cmor.llnl.gov/
- PrePARE: https://cmor.llnl.gov/mydoc_cmip6_validator/
- CF conventions: https://cfconventions.org/
- CF contributing rules: https://github.com/cf-convention/cf-conventions/blob/main/CONTRIBUTING.md
- CMIP6 controlled vocabularies: https://github.com/WCRP-CMIP/CMIP6_CVs
- Dunne et al. 2025, CMIP7: https://gmd.copernicus.org/articles/18/6671/2025/
- Pascoe et al. 2020, ES-DOC documentation for CMIP6: https://gmd.copernicus.org/articles/13/2149/2020/
- Balaji et al. 2018, data infrastructure requirements: https://gmd.copernicus.org/articles/11/3659/2018/gmd-11-3659-2018.xml
- Righi et al. 2020, ESMValTool v2: https://gmd.copernicus.org/articles/13/1179/2020/
- Lee et al. 2024, PMP v3: https://gmd.copernicus.org/articles/17/3919/2024/
- Hausfather et al. 2022, the hot model problem: https://media.nature.com/original/magazine-assets/d41586-022-01192-2/d41586-022-01192-2.pdf
- WIP standards governance proposal, 2014: https://wcrp-cmip.github.io/WGCM_Infrastructure_Panel/Papers/standards-governance.pdf
- SBML Test Suite, test case organization: https://sbml.org/software/sbml-test-suite/docs/test-case-details
- SBML Test Suite, evaluating outputs: https://sbml.org/software/sbml-test-suite/docs/evaluating-outputs
- SBML Test Suite results database: https://sbml.bioquant.uni-heidelberg.de/Simulator
- SBML Level 3 package process: https://sbml.org/documents/process/level-3-process
- SED-ML: https://sed-ml.org/
- SED-ML validator, Shaikh et al.: https://arxiv.org/abs/2106.00844
- KiSAO: https://github.com/SED-ML/KiSAO/
- BioSimulators simulator interfaces: https://docs.biosimulations.org/concepts/conventions/simulator-interfaces/
- BioSimulators capabilities format: https://docs.biosimulations.org/concepts/conventions/simulator-capabilities/
- BioSimulators test suite: https://github.com/biosimulators/Biosimulators_test_suite
- BioModels verification, Smith et al. 2025: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1013239
- FMI standard: https://fmi-standard.org/
- FMI Cross-Check rules: https://raw.githubusercontent.com/modelica/fmi-cross-check/master/FMI-CROSS-CHECK-RULES.md
- FMI Cross-Check repository (archived): https://github.com/modelica/fmi-cross-check
- FMI Implementers' Guide: https://modelica.github.io/fmi-guides/main/fmi-guide/
- Reference FMUs: https://github.com/modelica/Reference-FMUs
- Gomes et al. 2020, model-based testing of FMUs: https://2020.american.conference.modelica.org/proceedings/papers/Modelica2020US_paper_1.pdf
- SMT-LIB: https://smt-lib.org/
- SMT-COMP 2026 solver submission: https://smt-comp.github.io/2026/solver_submission/
- SMT-COMP 2026 rules: https://smt-comp.github.io/2026/rules.pdf
- MiniZinc Challenge 2025 rules: https://www.minizinc.org/challenge/2025/rules/
- Dolan and Moré, performance profiles: https://arxiv.org/pdf/cs/0102001
- Gould and Scott, a note on performance profiles: https://numerical.rl.ac.uk/media/people/nick-gould/GoulScot16_toms.pdf
- Mittelmann benchmarks: https://plato.asu.edu/bench.html
- Gurobi's statement on the Mittelmann benchmarks: https://www.gurobi.com/resources/blog/an-update-on-gurobi-s-participation-in-the-mittelmann-benchmarks
- Bari test set prologue: https://archimede.uniba.it/~testset/report/prologue.pdf
- MLPerf Training benchmark paper: https://arxiv.org/pdf/1910.01500
- MLCommons submission rules: https://github.com/mlcommons/policies/blob/master/submission_rules.adoc
- Taylor and Uhlig 1990, NBER working paper 3117: https://www.nber.org/system/files/working_papers/w3117/w3117.pdf
- Den Haan's suite page: http://www.wouterdenhaan.com/datasuite.htm
- Den Haan 2010, the comparison of the Krusell-Smith suite, JEDC 34(1): https://doi.org/10.1016/j.jedc.2008.12.010
- Juillard and Villemot 2011, the test bench: https://www.robertkollmann.com/JUILLARD_VILLEMOT_TESTBENCH_JEDC2011.pdf
- Kollmann, Maliar, Malin and Pichler 2011, the comparison: https://www.robertkollmann.com/KOLLMANN_PUBL_MALIAR_MALIN_PICHLER_JEDC_2011.pdf
- Aruoba, Fernández-Villaverde and Rubio-Ramírez, working paper: https://economics.sas.upenn.edu/sites/default/files/filevault/working-papers/04-003.pdf
- Macroeconomic Model Data Base user guide: https://www.macromodelbase.com/files/userguide.pdf
- REMARK standard: https://raw.githubusercontent.com/econ-ark/REMARK/master/STANDARD.md
- The Architecture of Open Source Applications, LLVM: https://aosabook.org/en/v1/llvm.html
- Pandoc filters: https://pandoc.org/filters.html
- Language Server Protocol overview: https://microsoft.github.io/language-server-protocol/overviews/lsp/overview/
- web-platform-tests: https://web-platform-tests.org/
- JSON Schema Test Suite: https://github.com/json-schema-org/JSON-Schema-Test-Suite
- Bowtie, adding a new implementation: https://docs.bowtie.report/en/stable/implementers/
- NIST StRD nonlinear regression information: https://www.itl.nist.gov/div898/strd/nls/nls_info.shtml
- acidtests.org: https://acidtests.org/
- W3C Process Document: https://www.w3.org/policies/process/
- The Tao of IETF: https://www.ietf.org/about/participate/tao/
- The working group's register-a-toolkit issue form: `.github/ISSUE_TEMPLATE/register-toolkit.yml` in this repository
- The working group's code of conduct: `docs/code-of-conduct.html` in this repository
