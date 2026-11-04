# Bringing a toolkit to the buffer-stock comparison

Proposed on 2026-11-03, for the owner's reading first, revising the draft of the same afternoon; sent to no one. Paths
are relative to the repository's root at the commit you are sent. Anything marked *proposed* is not built and binds no one; anything marked *today* exists at
that commit.

## What this is

A model intercomparison. Two buffer-stock consumption-saving families, the natural and the artificial
borrowing-constraint scenarios, are stated so completely that every valid solution method, given unbounded computation,
converges to the same solution as every other. No numerical method is prescribed: grids, quadrature, tolerances, sample sizes and
the representation of the income shocks' laws are yours. You solve a member with your own code, your own way, and write
one results file in a fixed form. The organizer verifies the file against the member, compares it with every other
toolkit's at the points the experiment's request file fixes, and publishes the comparison as tables and figures. Nothing ranks toolkits. Run times go into
the run registry with the machine, the threads and the environment they came from; the rule against recording them was
revoked on 2026-11-04. HARK (econ-ark's) and dolo (EconForge's) are in, through adapters the organizer wrote;
their files are in the repository and agree.

Who runs it: the organizer is the owner of the schemas, running the comparison from the public fork
`llorracc/sce-wg-1-dev` of the working group's repository `econ-ark/sce-wg-1`. The comparison has not been proposed to
the working group; the route to the group's repository is the organizer's to start, and the page will say when it has.
The working group's membership is by invitation; whether taking part in the comparison needs membership is the
organizer's decision and is stated here once made. Your toolkit may be open or closed, free or commercial: a closed
toolkit is pinned by a version string and a hash of its binary, and whether the organizer will run a closed binary in
the harness is a decision still open.

The pattern is the one the climate intercomparisons and the systems-biology standards settled on: the organizer states
the protocol and ships a validator; you supply one results file and a short card; verification at entry is structural;
comparison comes afterward and is published with its limits stated.

## What you receive

| what | where |
|---|---|
| the model: the household's problem, the order of events in a period, the income process, the population and the newborn, in Buffer Stock Theory's notation | `schemas/bst/model.md` |
| the conditions, domain rules and implications a solution is tested against; read it if you write the results file by hand, since that path computes thirteen factors with their bounds and classifies the welfare lower-tail case by its domain rules | `schemas/bst/conditions.md` |
| the stage files: the normative statement of each family, in Bellman-SYM, a language whose documentation is not public; `model.md` reads them for you, and a one-page guide to their syntax is *proposed* at `schemas/bst/reading-a-stage-file.md`, naming the commit it reads. Read a stage file once beside `model.md`; nothing you write uses its syntax | `schemas/bst/natural/bellman/natural.bl`, `schemas/bst/artificial/bellman/artificial.bl` |
| the members: parameter files with nothing numerical in them; a file's canonical hash is the model's identity | `schemas/bst/natural/members/`, `schemas/bst/artificial/members/` |
| the laws' convention: the truncated lognormal's stated standard deviation is that of the log after truncation, its bounds are in standard deviations of the log, its mean is one | `schemas/shock-laws.md`, the TruncatedLogNormal section |
| the request files: the points in m at which every toolkit reports its rule | `schemas/bst/experiments/restrained-limit/*.request.yaml` |
| the results schema and its validator | `schemas/bst/results.md`, `schemas/bst/results.schema.json` |
| the checker (*today*): validates and hashes a member, prints its closed-form moments and the stated member's verdicts, and verifies a results file against the member; a `--hash` command for method, settings and request files is *proposed* | `schemas/checker/`, with its README's commands |
| the method and settings files' form; the levels are named there | `schemas/numerics.md`, the method file and settings file sections |
| the restrained-limit experiment: four members, named levels, the checks | `schemas/bst/experiments/restrained-limit/` |
| the reference runs: HARK's and dolo's verified files at three levels, with a committed `methods.yaml` to copy | `schemas/records/findings/2026-11-01_restrained-limit-suite-hark/`, `schemas/records/findings/2026-11-01_restrained-limit-suite-dolo/` |
| the writer for Python toolkits (*today*), and two worked adapters | `harness/adapters/common.py`; `harness/adapters/dolo/`, `harness/adapters/hark/` |
| the kit (*proposed*): assembles a results file from two commands of yours in any language, verifies it, compares it | `harness/kit/` |
| the licenses (*proposed*): the code license for the checker, kit, harness and adapters, and the data license you grant on submission for your results file, card and stone text | the repository root, once the organizer has chosen them |

The entry member, `schemas/bst/artificial/members/bst-restrained.yaml`: Buffer Stock Theory's own calibration, annual,
one discount-factor type (β 0.96, share 1), ϱ 2, survival 1, return 1.04, growth 1.03, both shocks truncated lognormal
with `sd_log` 0.1 and bounds at plus and minus three, no zero-income event, and a borrowing constraint at zero. The model
is the one with these continuous laws, not with any discretization of them. A newborn is born employed at permanent
income one with no assets; this member needs none. The natural family's members add a zero-income event with a small
probability, which is why they need a point mass at the joint worst income and why a solver reaching the natural limit
must be ready for zero consumption next period.

## What you provide first

- **A card:** the first section of your Rosetta Stone, `rosetta/<toolkit>.md`, half a page on the pattern of the
  capabilities table in `rosetta/dolo.md`: the toolkit's name, its version or commit, language and license; the families
  it solves; how it represents the laws; the method on each of the stage's seven targets, in your words; your names,
  timing and normalization for the parameter file's keys and the objects a results file reports; what it does not
  compute; a pointer to the toolkit's own buffer-stock example; a maintainer contact, which is the private channel for
  everything below; and whether you consent to be named by GitHub handle. The organizer answers the card before you
  write code, so that what the toolkit cannot do is settled first.
- **One results file** for `bst-restrained` at one level of your own numerics, with `methods.yaml` and `settings.yaml`.
  It must pass `check.py <member> --verify-results results.json`. Three ways to make it, each labeled by what exists:
  - *In Python, today:* write the toolkit object that `run` in `harness/adapters/common.py` expects, as `DoloToolkit`
    in dolo's adapter does: the strings `name`, `driver`, `description`, `representation`, `diagnostics_method`,
    `methods` and `solver`; `version()` and `commit()`;
    `settings(level, lev)`, which receives the level's number and the module's level dictionary; and
    `solve(member, beta, nodes, lev)`, which receives the module's nodes and returns the rule with its derivative, the
    value function or none, and the rule's lower limit. The module writes the three files. dolo's adapter is the
    worked example.
  - *In any language, with the kit (proposed):* write `solve <member> --level <name> --out <dir>`, which solves and
    writes a small JSON of what only your toolkit can produce (the expectations the family names and the lowest values
    of the permanent shock and of income under your representation of the laws; the derived parameters you used; the
    lowest m you solved; the exported rule), and `evaluate <dir> <points file>`, which reads a JSON array of points and
    writes c, your own MPC as a derivative, and the value where you have one, for all the points in one call. The kit
    batches its calls and assembles the rest. Its exact syntax is *proposed* and waits on a ruling.
  - *By hand, today:* write `results.json` to `schemas/bst/results.md`, computing every block yourself, the conditions
    by `schemas/bst/conditions.md`. An author outside Python who starts before the kit exists takes this path.

What a results file reports, in outline: the family and the hashes of the parameter, method, settings and request files;
your toolkit's name and version; the effective member you solved, as the expectations the family names under your laws,
your lowest values (at or above the stated laws' infima) and the derived parameters you used; every condition's factor
and verdict; c and the MPC at the request file's points and at dense points of your own, the kink included; the kink,
the target and the pseudo-target behind statuses; the stationary distribution of m, a and c as generalized Lorenz
ordinates and quantiles, with the mass at the constraint and the mean MPC; the income-measure block, welfare and
marginal welfare behind statuses; the Euler residuals at the request points under the stated laws; the stationarity
residual; then the same pooled over types. The optional `errors` tree, mirroring the value tree, is the place for your
own error estimates, and the free-text `representation` field is where you describe your representation in words.
Never your grid, histogram or interpolant; never a run time, machine name or operating system: a run's time, with its machine and threads, goes into the run
registry (the ruling of 2026-11-04) and not into the file.

What the validator requires of every file, and what sits behind a status:

| required of every type | behind a status (`value`, `undefined`, `not computed`) |
|---|---|
| the effective member: ten expectations, the two lowest values, the derived parameters | the kink, the target, the pseudo-target |
| every condition's factor and verdict, the welfare conditions' lower-tail case | the income-measure block |
| c and the MPC at the request points; the exported rule with its range | welfare and marginal welfare, with the quartile entries |
| the population block: the generalized Lorenz ordinates of m, a and c, the mean of c, the mass at the constraint, the share with nonpositive a, the mean MPC and the MPC by quartile of a | the quantiles inside a distribution block |
| the Euler residuals: the values, their maximum, the expectation method and its precision | |
| the stationarity residual's population number | |

`undefined` means the member defines no such value; `not computed` means you did not compute one that sits behind a
status. So a probe today needs a stationary population under the population measure and Euler residuals computed by a
quadrature of the stated laws separate from the one you solved with; a toolkit without either cannot produce a valid
file until a block-level status for those blocks is adopted, which is *proposed* and goes to the participating toolkits'
authors first.

- **The two small files.** `settings.yaml`: a flat map of your plain values with a `level` key, as the committed files
  are. `methods.yaml`: the seven targets, each with the tag as its method where the stage gives one (`!time-iteration`,
  `!Linear`, `!quadrature`, `!histogram`) and your routine as its handler, words only where no tag fits, no values. Copy a
  committed `methods.yaml` under the findings folders above as the template; the template in `schemas/numerics.md`
  lacks the `arvl_to_dcsn` entry until a proposal adds it. A level names your settings and promises no accuracy.

Send a folder `<toolkit>/<member>/<level>/` holding the three files, and the card, through the private channel. This is
the whole first stage: no adapter, no environment, no registry entry, no stone beyond the card.

A first check for yourself, before the checker: at their finest level, HARK's and dolo's committed files report for
`bst-restrained` a kink near m = 0.974, a target near m = 1.041, a mass at the constraint near 0.213 and a mean MPC
near 0.456. Those two runs shared one representation of the laws, so their agreement checks the solvers and not the
representation; your numbers will differ by your representation's error, and the checks below measure that. For scale,
until an expected file with an informative band exists (*proposed*): between their medium and high levels those
shared-node runs' rules moved by about 3.5e-3 at the request points up to m = 20, and their largest Euler residuals
under the stated laws at the finest level were about 2.1e-4, both read from the committed files on 2026-11-03. A probe
far outside them is reported back to you, not failed.

## How your results are verified and reported

- **The checker is the only gate,** and it certifies no number. It validates the file and verifies what needs no
  representation: each condition's factor as arithmetic on your expectations, each verdict against its factor, each
  status against the verdicts, each derived parameter against your lowest values, your lowest values against the stated
  infima, and your expectations against what every law obeys; and, *proposed*, the method, settings and request hashes
  against the files beside the results file and the comparison points against the request file. Your expectations'
  values are yours and are trusted.
- **The comparison** sets your rule beside every file on record for the member at the request file's points and
  classes each difference: within the toolkits' own convergence; a difference of regime, when two effective members sit
  on opposite sides of a condition; a difference of method; or a disagreement to trace to a convention before it is
  called an error. A quantity present in one file only is reported, not failed. A block you report as `not computed`
  is a gap, never a failure.
- **The Euler residuals** under the stated laws are the test against the model itself; they trust no toolkit's
  representation, yours included. Yours are required. Where the kit computes them too, it evaluates your own rule
  through `evaluate` and records its value beside yours as a cross-check, never in place of yours.
- **Your first file is a probe.** The organizer verifies it, compares it, and sends you the report with the numbers
  behind it through the private channel. A probe is recorded in no finding and appears on no published page; no probe
  number is posted in a public issue or committed to the records; its files stay outside the repository and are deleted
  on your request; the journal mentions the probe by toolkit name and outcome only with your consent. Nothing about your
  toolkit is published before you have seen it.
- **The ledger** (*proposed*): one row per toolkit, member and check, with the numbers behind each verdict,
  discrepancies included; no score, no ordering; a time, recorded since the ruling of 2026-11-04, shown only with the
  machine and settings it came from. Rows the organizer reproduced in a locked environment are
  marked apart from rows verified from submitted files alone. The two toolkits whose adapters the organizer wrote go
  through the same gate and are marked as such. Rows are kept per toolkit version; a new release of your toolkit is a
  re-pin with a rerun, and the old rows stay, marked by version. You may withdraw: on your request your rows leave the
  ledger, while the records' history stays, since the repository's history is permanent. A pin that stops resolving
  marks its rows as no longer reproducible.
- **Disputes.** The organizer decides a difference's class and publishes the numbers behind it. You see your rows
  before publication and may contest a class within the comment window; an unresolved contest is shown on the ledger as
  contested, with both readings and both toolkits' movements between levels. For two toolkits that both pass while
  disagreeing, the remedy is a method-only ladder at fixed nodes, deferred. Conduct follows the working group's code of
  conduct, `docs/code-of-conduct.html`.
- **The organizer's envelope** (*proposed*) for a harness run: a thread cap, a memory limit and a time cap stated in
  `harness/README.md`. A job that exceeds them is marked not run within the limits, which the ledger shows as a gap,
  never as a failure of your toolkit.

## When the checker refuses your file

`check.py` exits 1 with a list of problems. They come in three kinds.

- **A refusal by design.** A lowest value reported below the stated infimum (nodes placed beyond the truncation
  bounds), or a factor that is not the arithmetic of your reported expectations and the parameters. This is not a defect
  in the checker: it is a representation to change, or one to declare in the card if it is what your toolkit does. An
  effective member that fails a validity condition the stated member passes is reported, not refused; `conditions.md`
  reads it as a discretization too coarse.
- **A suspected defect in the checker or a schema.** Open an issue labeled for the checker; it is recorded in
  `schemas/records/defects.md` and answered by the organizer within the comment window. Put no probe number in the
  issue; send those through the private channel.
- **A plain file error.** A hash that is not the member's, a missing key, a value out of range. The message names the
  path in the file.

## What the later stages add

| stage | you | the organizer |
|---|---|---|
| the restrained-limit experiment | its four members at two of your levels at least, three recommended | runs the experiment's checks: each natural rule closer to the restrained rule than the rung before; your effective member approaching the stated member's closed forms with the level, a distance at round-off passing at any level; your rule and another toolkit's agreeing within the sum of their own movements between their two finest levels; your residuals falling with the level, or reported as not applicable where your levels change only method-only settings; places a verified submission on the ledger as submitted-only |
| the integration | keep `solve` and `evaluate` stable; name a version to pin and a requirement list with the interpreter; outside Python, your language's own lock or manifest file, or a version list, for the run's manifest | wraps them in the adapter contract, locks a `uv` environment under `harness/adapters/<toolkit>/env/`, writes the registry entry, reruns your toolkit on every experiment within the envelope; only a reproduced run becomes a findings record. For a toolkit outside Python a container convention is *proposed*; until it exists such a toolkit reaches a probe and an experiment submission only |
| the stone | fill the rows only you know on a skeleton the organizer generates from your card, your method file and your runs; review the rest; a paragraph of judgment, signed by your handle, for the hand-written findings record | generates the lexicon, the methods table and the evidence; writes the cards for the stone registry's intake; writes the findings record from the numbers, saying what they establish |
| a second experiment | later: an estimated member with several types, solved, simulated and, where your toolkit can, differentiated for its Jacobians (`schemas/jacobians.md`); the steady state, the distributions and the joint required, the Jacobians behind a status (*proposed*); its large files sent by a stated means and kept outside git, with their hashes in the results file. It is with the HAFiscal-Latest repository since 2026-11-04 until its member is ready | delivers the member and the interface when ready; nothing is asked now |

## Rules both sides keep

- The stated model has continuous truncated lognormal laws; the representation is yours; a results file reports the
  effective member through the expectations the family names, never through a form of the laws.
- The organizer gives you parameters only: the member, the request file and a level's name; never a method, a setting or
  a representation. A declinable library of nodes, a population method and the conditions' arithmetic may be offered
  (*proposed*); if you use any of it, say so in the card.
- Two files are compared as solutions of one member only when their parameter-file hashes match. A results file names the family's version and,
  *proposed*, the results schema's release and the stage file's hash; a later release never invalidates a verified file,
  a new required key applying only to files that name the new release; a change to the model statement that could change
  a verified result makes a new family version, and your file stays valid for the version it names.
- A schema changes only after a proposal stating its consequences, and what a results file carries is put to the
  participating toolkits' authors first.
- Your toolkit is named on the ledger and in the records by its registry identifier, one spelling everywhere, and cited
  as you cite it; you are named by GitHub handle only, and only with the consent given in the card; no email address
  enters the repository.
- You grant the data license on submission for what you send; the code you run is under the code license; both are
  stated at the root before anything is sent (*proposed*).
- Public documents cite what a reader can check: a pinned public commit, a public pull request, a published page. The
  repository is public and its history permanent.

## Words

Family, member, stated member and effective member, request file, method target, handler: `schemas/README.md`. Level:
`schemas/numerics.md`. Three that trip newcomers: the *effective member* is the model your representation of the laws
defines, which is what you solved; the stated member is its limit. *Generalized Lorenz ordinates* are the cumulative
mean below each of fifteen fixed probabilities, finite where the mean is not, which is how a distribution is reported
without a histogram. The *lower-tail case* of the welfare conditions is one of four, named in `schemas/bst/conditions.md`:
an atom at the floor, a constraint the agent reaches (a binding constraint, in this page's one use of the word: the
artificial limit lies strictly above the natural one, so the agent ends a period at it), densities at the floor, or a
vanishing density; it is decided on your effective member by that document's domain rules.

## Where to ask

Open an issue in `llorracc/sce-wg-1-dev` at the commit you were sent for a question about the documents, the checker or
the schemas, with no probe numbers in it; send the card, the probe and anything about your numbers through the maintainer
contact the card names, which is the private channel in both directions. A question about the stage file is answered in
`model.md`'s terms.
