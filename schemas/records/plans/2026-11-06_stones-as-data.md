# What a Rosetta Stone holds: desiderata for a competent reader, and the record of each realization

**Status: ACCEPTED on 2026-11-06 at 18:46:34 EST, all nine decisions as recommended; proposed at 17:40 on the owner's
request of 16:01:18 and revised at 18:45 on his direction of 18:36:57.** The convention's text is drafted on the fork's
branch `stone-convention`, cut from main, at 359fb78, put to him before it merges; the rest is the model repository's
session's, on his word there. Nothing here changes a stone, an adapter or the convention. The stones and the adapters are the
buffer-stock model's repository's, and its session carries out what is adopted, on the owner's word there; the
convention's text, `rosetta/README.md` on this fork's main and in the series upstream, is this fork's. The model
repository's session and the bellman session were consulted for the first version, and their answers stand below in
substance.

## The direction, in substance

The system will be operated by capable AI sessions. It is not to be designed as prescriptions that a rigid script
could carry out, with every detail spelled out, but as desiderata that a competent reader can be trusted to meet:
one that reads each toolkit's documentation and code, understands the mathematical structure of the problem, takes
the parameters and settings it is given, and works out how to make the toolkit perform what is expected of it.

The first version of this plan, written that afternoon, had taken the other road: a data file the adapter reads,
holding every argument the toolkit is called with. The owner's direction reverses that choice and keeps the rest.

## What the day's measurements say under this direction

Three things were measured for the first version; read again, they argue for the direction more than for the file.

- **The clean-room test is the demonstration.**
  [Two agents](../findings/2026-11-06_stone-regeneration-test/README.md) that had never seen an adapter were each
  given one stone, the schemas, the shared code and the toolkit's installed source, and told to write the toolkit's
  part. HARK's came back with every number the committed adapter's; dolo's within the solver's tolerance. They read
  the toolkit's source eleven and fourteen times for facts the stone did not state, and that is what a competent
  reader does: the arguments' shapes, a distribution's layout, where a version is read, what a solver returns. None
  of those needs writing down for such a reader. What they could not settle from any document were things of
  another kind: a convention that moves a reported number, a grid's start above a natural limit, a tolerance, an
  iteration cap, and the names a results file carries. Those are desiderata, and they were missing.
- **The prototype shows the file road works and is not needed.**
  [HARK's arguments moved into a data file](../findings/2026-11-06_stone-data-prototype/README.md) gave identical
  results, and a reader found the same facts in HARK's source in an afternoon. What the prototype was worth is one
  rule it enforced: a reason for every fixed value, which exposed seven arguments nobody could justify and, with the
  clean-room result, eleven that are not needed. The rule survives as a desideratum on the reader's record.
- **The hand spellings disagree** in the cards, the prose and the adapters, on six, seven and seven of seven
  targets. That is not cured by more spellings: it is cured by one place for each expectation and a test that holds
  the rest to it.

## What a stone holds

A stone is the toolkit's side of the correspondence, in two parts that answer two questions.

**The desiderata: what the toolkit is expected to perform.** Short, exact, and the only things a reader may not
decide for itself:

- the model, by reference: the family's stage file and the member's parameter file, which the hub owns;
- the method expected on each of the stage's targets, as a tag: time iteration on the policy's solution, a
  quadrature on the expectation, a histogram on the population's transition, and so on, in the method file;
- the settings at each named level, in the toolkit's own names and with their values, in the ladder file: the
  grid, the tolerance, the limit of iterations, the nodes; and the toolkit's own defaults as an element of their own,
  with where they were read;
- the conventions that move a reported number and that neither the mathematics nor the toolkit's documentation
  decides: which side's segment gives the slope at a point that is a node, how far above a natural limit a grid
  starts, what a solve that stops at its cap is. Where a convention is the hub's, as the slope's is, the stone points
  to it;
- what the results file must say of the toolkit: its name, how it represents the laws, the diagnostics' method; the
  hub names these and the stone fills them.

**The realization: what a reader did, so that the next reader can check it.** The adapter, in code, and beside it
the reader's record: what it read in the toolkit's documentation and source and where, every choice the desiderata
left to it with its reason, every fixed value with its reason, and every statement in the documents it found wrong.
The two clean-room logs are the first two such records. The evidence closes it: the checker's verdict, the
comparator's distances from the reference, and the ladder's convergence.

The document, the lexicon of names with their timing and normalization and the departures with what was done about
each, remains for people. It is written from the record, not before it, and it states no value that the desiderata
state: it points.

What a stone does not hold is whatever is the same for every toolkit. That has two homes: the adapter contract, the
command line and the files between the core and an adapter, in the hub; and the shared code's protocol, what a
toolkit's part hands the code the adapters of one model share, in the adapters' own page, with the code's header
pointing there. The shared code is a reference realization of the toolkit-neutral desiderata, the effective member,
the population, the residuals and the files, which a reader may use or replace, held to the same acceptance.

The cards, in Project Bellman's field names, become an export from the method and ladder files when that registry
takes cards again; its public page *Core concepts* says they are being rebuilt. Until then nobody edits them.

## Acceptance

A stone is accepted by its outcome, not by its form:

- a reader given the stone's folder and the hub, and nothing of an earlier adapter, produces a toolkit's part whose
  results verify with the checker and stand from the reference within the level's own error, with no quantity the
  experiment asks for missing;
- its record names a source for every value that is not in the desiderata: the toolkit's documentation, a decision
  with its reason, or a convention of the hub;
- what two readers decide differently is a desideratum that was missing, and goes into the stone.

This is run when a stone's desiderata change, and when a toolkit's pin changes; not on every commit. The checks of
form that the test keeps today, the lexicon's coverage and the cards' shape, stay as they are.

## The ladder file, and the levels

The ruling of 2026-11-04 has each stone state three precision levels, the harness being silent about method. The
ladder file of [`numerics.md`](../../numerics.md) is where, and the model repository has begun it for two toolkits.
Settings are the one thing a reader must not infer, and five things would complete this:

- **dolo.** Its adapter takes its grid from the shared code's table. A ladder file in dolo's own names, read by its
  adapter, would not touch the toolkit. The owner ruled that morning that dolo is not to be treated as the other
  two were, so this is his to say.
- **The shared code's own settings**, the nodes per shock, the population's grid, the diagnostics' nodes and the top
  to which the targets are sought, as a ladder file of its own, each marked as changing the effective member or only
  the method.
- **The toolkit's own defaults as a named element**, which the reader fills from the toolkit's documentation at the
  pin, with the citation. It answers what "default settings" means for a toolkit, which the ruling left open.
- **A setting made at run time by another toolkit's program.** One toolkit takes its list of gridpoints from
  another's run each time. The ladder says so where the setting is named; the run's settings file records the value;
  the container runtime, which gives a job one environment, cannot run it as built, which is open with the model
  repository's session.
- **The document's tables of settings** are hand copies of the ladder files in two stones. Each becomes a pointer.

The names of the three levels are still with the owner: coarse, default and fine were proposed on 2026-11-04, and the
experiments say low, medium and high.

## The method file

One file for each toolkit, beside its ladder: the target, the tag expected there, and, once realized, the handler as
the reader names it, in the form Bellman's public page *Handler* gives, a package and a callable in it. The adapter
copies it to the run folder, where today it writes out a list kept in its code. A toolkit that also binds method files
in another form keeps those; this is a third file beside them.

One target needs settling first. The schemas name the policy's solution `policy.euler.solve`. The Euler line of the
stage files, as they stand, carries one operator, the derivative, and no solve, so the name points at nothing the
stage states. It is the model repository's schema and has gone to that session with what the bellman session found.

## Conventions the hub owes

The clean-room test found two choices that no document makes and that move reported numbers, and both are the hub's
to make, since every toolkit meets them:

- the slope reported at a point that is a node of a toolkit's grid: the results document asks for a derivative and not
  a finite difference, and a linear rule has two one-sided slopes there, which differ by up to 1.3 · 10⁻² at the low
  level on dolo's grid;
- how far above a natural limit a grid may start, where the stage's constraint is never reached but a grid must begin
  somewhere: 10⁻⁶ reproduces the committed files and 10⁻⁹ does not.

They go in the results document as what is reported, with the stones pointing to them.

## The vocabulary

A parameter is the model's and a setting is a method's, as Project Bellman's public pages on parameters and settings
have it; an input of a call is an argument. A desideratum names what is expected; a realization is what a reader did.
Nothing in a stone calls a setting a parameter, whatever the toolkit calls it.

## What changes, and for whom

- **The convention's text** says what the desiderata are, what a realization's record holds and how a stone is
  accepted. It is in this fork's main and in the open upstream pull request that carries the stone convention, so the
  change is a further commit there or a pull request after it.
- **The model repository** gains a method file for each toolkit, a ladder file for dolo if the owner says so and one
  for the shared code, the conventions' pointers, and for each of its three adapters a realization record, which the
  two clean-room logs begin. Its documents lose their hand copies, and the twenty-four stale statements the logs list.
  No results file changes.
- **The hub** gains the two conventions in the results document and the two homes of what is shared.
- **The participation plan**, still awaiting the owner's reading, fits: an author's card states the desiderata it
  knows, and the organizer's reader realizes and records.
- **The adapters' independence**, the harness plan's stage still proposed, is the same direction taken further: a
  reader may replace the shared code's representation of the laws and its population, held to the same acceptance.

## The order

1. The owner's decisions below: taken at 18:46:34, all nine as recommended.
2. The convention's text, as a change to `rosetta/README.md` on a branch of this fork, put to him before it merges:
   drafted at 18:48 on `stone-convention` (359fb78). The two conventions in the family's results document are the
   model repository's, and go to its session with the rest.
3. In the model repository, on his word in its session: the method files and the ladders; then each stone's
   realization record from the logs it has, HARK's and dolo's first; the third toolkit's by a reader of its own.
4. The acceptance run for each stone.
5. The convention's change upstream, with the series.

## Decisions for the owner

- **No executable data file.** A stone states desiderata and records realizations; the arguments a toolkit is called
  with are the reader's to find and record, not the stone's to prescribe (recommended, on his direction). The
  prototype's file is kept as a finding and used for nothing.
- **Where a stone's files sit:** one folder for each toolkit under `rosetta/`, holding the desiderata, the record,
  the evidence and the document, so that a stone is one folder and an adapter's folder is code and environment
  (recommended); or the two files an adapter reads left beside it, which the model repository's session prefers for
  the smaller move.
- **dolo's settings** in a ladder file in dolo's names (recommended: settings are what a reader must not infer), or
  dolo left as it is.
- **The shared code's settings** as a ladder file of its own, each marked by its kind, and the shared code named a
  reference realization a reader may use or replace (recommended).
- **The toolkit's defaults** as a named element of its ladder, filled by the reader from the toolkit's documentation
  with the citation (recommended).
- **The method file as the one source** of target, tag and handler (recommended), once the target for the policy's
  solution is settled by the model repository's and the bellman sessions.
- **The two conventions** made the hub's, in the results document: the slope at a node, and the grid's start above a
  natural limit (recommended).
- **Acceptance by outcome, through a reader that has seen no adapter** (recommended), run when a stone's desiderata
  or its toolkit's pin change.
- **What may be said here of the model repository.** This document describes its ladder files, its third toolkit's
  dependence on HARK's run and the owner's rulings of that morning there, in substance; that repository is private
  and this branch is not pushed. If any of it should stay out, it comes out before a push.

## Sources

- Project Bellman's public documentation, read on 2026-11-06: *Core concepts*
  (https://econ-ark.github.io/bellman/overview/01-concepts/), on the registry's cards being rebuilt; *Settings*
  (https://econ-ark.github.io/bellman/wiki/settings/) and *Parameters*
  (https://econ-ark.github.io/bellman/wiki/parameters/), on the two words; *Handler*
  (https://econ-ark.github.io/bellman/wiki/handler/), on a handler named as a package and a callable in it, and on
  the adapter as distinct from the callable.
- The stones and adapters of HARK and dolo as this fork holds them, frozen since 2026-11-04 under `rosetta/` and
  `harness/adapters/`; the model repository's current ones were read for the measurements, and are its own.
- The model repository's session's answers of 16:10:08 and the bellman session's of 16:59:10 on 2026-11-06, in
  substance; what either marked as not to be cited is not here.
- The first version of this plan, at commit 0d3f38a of this branch.
