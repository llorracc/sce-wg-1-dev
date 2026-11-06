# What a Rosetta Stone holds: a toolkit's own part of its adapter, as data the adapter reads

**Status: PROPOSED, 2026-11-06 at 17:40 EST, on the owner's request of 16:01:18 EST that day.** Nothing here changes
a stone, an adapter or the convention. The stones and the adapters are the buffer-stock model's repository's, and its session
carries out what is adopted, on the owner's word there; the convention's text, `rosetta/README.md` on this fork's main
and in the series upstream, is this fork's. That session and the bellman session were consulted, and their answers are
below in substance.

## Where this starts

Asked that morning whether the stones contain what is needed to build the adapters, this session answered that a stone
holds nearly enough to write the toolkit's own part of an adapter and nothing of the larger part that is the same for
every toolkit; that it should hold all of the first, as data the adapter reads, and stay out of the second. The owner
agreed and asked for proposals. The reading behind the answer is in
[the journal of the day](../journal/2026-11-06_session-record.md).

Three things were then measured, each a record of its own:

- **The spellings do not agree.** Each toolkit's method on each of the stage's seven targets is written by hand in its
  cards, in its stone's prose and in its adapter. Between the cards and the adapters the tag is the same on all but one
  target of one toolkit, and the handler's name differs on six of HARK's seven targets and on all seven of dolo's and
  of the third toolkit's. The setting names in HARK's cards are those of no file since its settings were put in a
  ladder file under HARK's own names. The test that guards the stones checks their form and never this.
- **The arguments can be data.** [A prototype](../findings/2026-11-06_stone-data-prototype/README.md) moved every
  argument HARK's adapter passes, but the two it builds, into a file that a small helper reads: 6 from the model, 10
  fixed, 8 placeholders, 5 settings by name. On two members its results files are those of the committed adapter,
  every one of some 1,600 leaves, and the helper has nothing of HARK's in it. Writing the file showed what prose had
  let pass: seven of the eighteen fixed arguments have no stated reason.
- **A fresh reader can rebuild a toolkit's part from its stone, and where it cannot, the stone is short.**
  [The regeneration test](../findings/2026-11-06_stone-regeneration-test/README.md) gave an agent that had never seen
  an adapter one stone, the schemas and the shared code, and measured what it wrote against the committed adapter.
  HARK's part came back with every number the committed adapter's; dolo's within the solver's tolerance. Both agents
  had to read their toolkit's source, one eleven times and the other fourteen; both were left choices the documents
  do not make, nineteen and eighteen; and between them they found twenty-four statements in the stones that are
  wrong or stale, and three in the hub. What neither could rebuild is what no file states: the method file, the
  settings file's names and the five strings by which a results file names its toolkit.

## What a stone would be made of

A stone is the toolkit's side, in five files. Each has one job and each fact is written in one of them:

| file | who reads it | what it holds |
|---|---|---|
| the document | people | the toolkit's own model, the lexicon of names with their timing and normalization, the departures and what the adapter does about each, the evidence. It states no value another file states: it points |
| the data file | the adapter, each run | what the toolkit is called with and what is read back: the blocks below |
| the ladder file | the adapter, each run | the toolkit's own settings at each named level, in the toolkit's names |
| the method file | the adapter, which copies it to the run folder | the method on each target: the tag and the handler |
| the cards | Project Bellman's registry, when it takes cards | an export of the three files above, in that registry's field names. Nobody edits it |

What a stone does not hold is whatever is the same for every toolkit. That has two homes, below.

## The data file

Its blocks keep apart what answers different questions. The prototype's file for HARK is
[here](../findings/2026-11-06_stone-data-prototype/hark.stone.yaml).

| block | the question it answers | for HARK | for dolo |
|---|---|---|---|
| `arguments` | what does the model say? Each parameter-file key, with the toolkit's name and shape for it | `crra` to `CRRA`; `return` to `Rfree`, one value per state | the keys to the model text's symbols |
| `fixed` | what does the adapter decide, the same for every member, and why? | an infinite horizon; the cubic rule; the value kept | the normalizing constant |
| `placeholders` | what does the toolkit ask for although the adapter replaces what it would build? | the inputs of HARK's own income process | the model text's exogenous block |
| `settings` | what does the method read? Names only; the ladder has the values | the grid's four and the tolerance | the tolerance, the limit of iterations, the two grids |
| `model_text` | where the toolkit takes a model as text: the text, as a template of the stone | none | the recast household |
| `built_by_the_adapter` | what stays code, routine by routine: what each makes, and what the toolkit requires of it | the chain; the income process: its class, the order and labels of its two shocks, the keys of its bounds, its seed | the nodes as a finite distribution; the savings grid |
| `switched_off`, `replaced_from_outside` | what of the toolkit is turned off or replaced, by what, and why; that a replacement is made in a namespace of its own and does not outlive the call | two constructors | none; a toolkit imported unmodified lists here each function it is given from outside |
| `read_back` | where is the solution read? | the employed state's rule, value and lower limit | the rule's values at its grid, the convergence flags |
| `asserted` | what is checked after the solve, with what tolerance? | the two states agree; HARK kept the adapter's inputs | the solver converged |
| `says_of_itself` | what does a results file say of the toolkit? | its name, the sentence on how it represents the laws, the name of the diagnostics' method | the same |

Three rules go with it.

- **Model inputs and settings never share a block.** A parameter is the model's and a setting is a method's, as
  Project Bellman's published pages on parameters and settings have it; an input of a call is an argument. No field
  calls a setting a parameter, whatever the toolkit calls it.
- **Every fixed value carries its reason.** A value with no reason is a finding, not a default.
- **What stays code is named, and the names are held.** Some of a toolkit's part cannot be data: dolo's reading of its
  rule with the kink's point, the functions an imported toolkit is given from outside. The file lists each routine,
  what it does and where it is, and a test holds that each exists and that the adapter passes exactly what the file
  lists. The model repository's session judged this an honest way to hold them, on that condition.

The file is in the schemas' strict subset of YAML. A value that is not a plain number or string is the toolkit's own
literal, in a string: the toolkit's side is written in the toolkit's language.

## The ladder file, and the levels

The ruling of 2026-11-04 has each stone state three precision levels, the harness being silent about method. The
ladder file of [`numerics.md`](../../numerics.md) is where: named elements, in the toolkit's own names, read by the
adapter. The model repository has begun it for two toolkits. Five things would complete it.

- **dolo.** Its adapter still takes its grid from the shared code's table. A ladder file in dolo's own names, read by
  its adapter, would not touch the toolkit. The owner ruled that morning that dolo is not to be treated as the other
  two were, so this is his to say, not this plan's to infer.
- **The shared code's own settings**, the nodes per shock, the population's grid, the diagnostics' nodes and the top
  to which the targets are sought, as a ladder file of the shared code's own, each marked as changing the effective
  member or only the method, the two kinds `numerics.md` describes. Today they are a table in code, and two toolkits'
  ladders agree with it only by the choice of their values.
- **The toolkit's own defaults as a named element.** The ruling compares solutions at default settings with the
  reference and left open what default settings means for a toolkit. An element holding the toolkit's defaults, in its
  names, answers it in the same file.
- **A setting made at run time by another toolkit's program.** One toolkit takes its list of gridpoints from another's
  run each time. The data file would say so where the setting is named, the run's settings file records the value, as
  it does now, and the container runtime, which gives a job one environment, cannot run it as built. That last is open
  with the model repository's session.
- **The document's tables of settings are hand copies of the ladder files** in two stones. Each becomes a pointer, or
  stays and is held to the file by the test. That session would not generate prose, and this plan agrees.

The names of the three levels are still with the owner: coarse, default and fine were proposed on 2026-11-04, and the
experiments say low, medium and high.

## The method file

One file for each toolkit, in the schemas' form, beside its ladder: target, tag, handler. The adapter reads it and
copies it to the run folder, where today it writes out a list kept in its code. The cards' entries and the document's
section on the method are held to it by the test. A toolkit that also binds method files in another form keeps those;
this is a third file beside them, the targets of the two forms not being the same.

One target needs settling first. The schemas name the policy's solution `policy.euler.solve`. The Euler line of the
stage files, as they stand, carries one operator, the derivative, and no solve, so the name points at nothing the
stage states. It is the model repository's schema and has gone to that session with what the bellman session found.

## The cards

The cards were written in the field names of Project Bellman's Rosetta registry so that Bellman could take them in.
That registry's cards are being rebuilt, as its public page *Core concepts* says, and nothing reads a card today. The
bellman session's advice is that what an adapter reads go in a file beside the cards, never inside them, and that the
fields which restate that file not be written by hand a second time.

- The cards become an export, made from the data, ladder and method files, and checked by making them again.
- Three field names in today's cards are this project's own, `calls`, `target` and `scope`, as are the toolkit
  block's. The export marks its own fields as its own.
- Where a field takes a token, the export writes the token and not a sentence.

## Two contracts, two homes

This changes one sentence of the morning's answer, on the model repository's session's reading.

- **The adapter contract** is the hub's: the command line and the files between the core and an adapter, in any
  language. It stays where it is, in the harness's page and plan.
- **The shared code's protocol** is one level down: what a toolkit's part hands the code the adapters of one model
  share. An adapter written without that code owes it nothing. It is stated today only in that code's header; its
  home is the adapters' own page in the model repository, with the header pointing there.

## The tests that hold it together

- Every name in a stone's data exists in its toolkit at the pin. This is the test of HARK's names deferred since
  2026-10-31, a dozen lines once the names are data.
- The adapter passes exactly what the data lists, and each named routine exists.
- The cards are what the export makes; a document's table equals its file.
- The lexicon covers every parameter and key, as now.
- **Regeneration**, the convention's acceptance for a stone: a reader that has seen no adapter is given the stone
  and the hub, writes the toolkit's part, and the comparator sets its results beside the committed adapter's. It is
  run when a stone's data changes materially, not on every commit.

## What the regeneration test asks of the stones

The two logs are the measure of today's stones, and the proposals answer them item by item.

- **A fixed argument that is not needed is a reason that was never written.** HARK's regenerated part passed eleven
  fewer arguments than the committed adapter and lost nothing; the seven that the prototype found no reason for are
  among them. The data file's rule, a reason for every fixed value, is the test that would have found this.
- **What a built object must satisfy is the toolkit's requirement, not the adapter's habit.** Three of the facts
  HARK's agent had to read in the source are what its income process must look like: its class, the order and the
  labels of its two shocks, and the keys of its bounds. The data file's entry for a built object carries them.
- **A value found by trial is a value the stone should have stated.** dolo's agent found the savings grid's start
  above a natural limit, where the nested grid begins and the iteration limit by matching numbers the hub quotes of
  the committed files. Each is a setting; the ladder file is where it goes.
- **A convention that moves a reported number is part of the method.** The slope reported at a point that is a node
  of dolo's grid depends on which side's segment is read, by up to 1.3 · 10⁻² at the low level, and no document says
  which. The method file's entry for the rule's interpolation names it.
- **The protocol between a toolkit's part and the shared code is in no document.** Both agents learned what the
  nodes they were handed are, which shared routines to call and what the member object holds from the code alone.
  That is the adapters' page's to state.
- **The hand copies drift.** Fourteen and ten statements, the cards' setting names, the links from before the move,
  source lines cited at a commit the adapter does not run: each is a thing written twice. The lists are in the logs,
  for the model repository's session to work through, and the tests above keep them from coming back.

## What changes, and for whom

- **The convention's text** gains the five files and the three rules. It is in this fork's main and in the open
  upstream pull request that carries the stone convention, so the change is a further commit there or a pull request
  after it.
- **The model repository** gains a data file and a method file for each toolkit, a ladder file for dolo if the owner
  says so and one for the shared code, the helper, and the tests; its adapters read them; its cards are exported; its
  documents lose their hand copies. No results file changes: the prototype's are the committed adapter's.
- **A job's fingerprint** must cover the three files an adapter now reads.
- **`numerics.md`** gains the defaults element and the setting made at run time.
- **The participation plan**, still awaiting the owner's reading, already asks for one spelling of each thing; under
  this plan an author fills the data file's rows and the ladder, and the organizer makes the rest.
- **The adapters' independence**, the harness plan's stage still proposed, moves more of the shared part into each
  toolkit's own. The blocks above do not change; a toolkit's file grows.

## The order

1. The owner's decisions below.
2. The convention's text, as a change to `rosetta/README.md` on a branch of this fork, put to him before it merges.
3. In the model repository, on his word in its session: HARK first, from the prototype; then dolo; then the third
   toolkit, most of whose part is named routines. The tests with each.
4. The regeneration test again, as each stone's acceptance.
5. The convention's change upstream, with the series.

## Decisions for the owner

- **Beside the cards, not inside them:** the data an adapter reads in a file of its own, with the cards an export
  (recommended, and the bellman session's advice).
- **Where the files sit:** a folder for each toolkit under `rosetta/`, holding the document, the data, the ladder,
  the method file and the exported cards, so that a stone is one folder and an adapter's folder is code and
  environment (recommended); or the three files an adapter reads left beside it, which the model repository's session
  prefers for the smaller move. Either gives one file and one spelling.
- **How far the data goes:** the arguments, the fixed values with their reasons, the placeholders, the settings'
  names and what is switched off, read at each run; what stays code named routine by routine and held by a test
  (recommended).
- **dolo's settings** in a ladder file in dolo's names (recommended, for the ruling of 2026-11-04), or dolo left as
  it is.
- **The shared code's settings** as a ladder file of its own, each marked by its kind (recommended).
- **The toolkit's defaults** as a named element of its ladder (recommended).
- **The method file as the one source** of target, tag and handler (recommended), once the target for the policy's
  solution is settled by the model repository's and the bellman sessions.
- **Regeneration as a stone's acceptance** (recommended).
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
