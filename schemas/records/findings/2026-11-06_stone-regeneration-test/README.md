# Rebuilding a toolkit's part of its adapter from its Rosetta Stone: a clean-room test

Run on 2026-11-06 between 16:36 and 17:35 EST, for [the proposals on what a Rosetta Stone
holds](../../plans/2026-11-06_stones-as-data.md). The question: does a stone, with the hub beside it, hold what is
needed to write its toolkit's own part of an adapter?

## The set-up

For HARK and for dolo a sandbox was made in this session's scratchpad from the buffer-stock model's repository at its
commit `af1539c` of that day, holding only:

- the stone, its cards and the convention's page; for HARK, its adapter's ladder file, which the stone points to;
- the schemas without the records, so that no finding or journal about an adapter was there;
- the code the adapters share, whose header states what a toolkit's part must supply, and the harness's page with the
  adapter's command line;
- a wrapper for the interpreter of the toolkit's pinned environment.

A fresh agent was started in each. It was told to write the toolkit's part from those documents alone; to read nothing
under the repositories, in any git history or on the web, the adapter above all; that it might read the toolkit's own
installed source, as any user can; to run its adapter on `bst-restrained` and `bst-p-zero-0.005` at the low level with
the restrained-limit experiment's request files and verify each results file with the checker; and to keep three
logs: every fact it needed that the documents did not give, every choice they left open, and every statement in them
it found wrong, stale or contradictory. The model repository's own adapters were run on the same two members beforehand
as the measure. A first pair of agents, started at 16:08, ended at 16:10 on the usage limit of the account then in
use, having written nothing; the pair reported here started at 16:36:51 and 16:37:04.

| file | what it is |
|---|---|
| [`hark/LOG.md`](hark/LOG.md), [`dolo/LOG.md`](dolo/LOG.md) | each agent's three logs, as it wrote them |
| [`hark/adapter.py`](hark/adapter.py), [`dolo/adapter.py`](dolo/adapter.py) | the toolkit's part each agent wrote |
| [`measure.py`](measure.py) | a regenerated adapter's results file against the committed adapter's |

## HARK

Both runs completed and verified at the first attempt, and the agent went on to the other members and levels, which
verified too.

| member, low level | numbers the two files share | equal to the last bit | largest difference in c, and in the MPC, at the comparison points |
|---|---|---|---|
| `bst-restrained` | 1568 | 1568 | 0 and 0 |
| `bst-p-zero-0.005` | 1529 | 1529 | 0 and 0 |

- **What the documents did not give, and HARK's source did:** eleven facts. Three were needed before the solve would
  run: the arguments and layout of the labeled distribution each state is given; that the solver reads the two shocks
  by position in some places and by label in others, so both the order and the names bind; and that a value per state
  must be a NumPy array, a list being refused. The others: the keys of a distribution's bounds, the Markov consumer's
  own defaults, how an infinite-horizon solve ends and that it stops silently at a cap, the integer type two settings
  must have, the seed, where the version and commit are read, that nothing else needs switching off, and where the
  grid's top is.
- **What only the shared code gave, and no document:** four facts. What the nodes handed to a toolkit's part are; that
  one shared routine gives each state's shocks; the member object's attributes; and that a version must be a string,
  where the protocol's header allows none.
- **What was left to the agent:** nineteen choices, from the placeholders' values and the numbers in each state's
  bounds to how the assertions are made.
- **What it could not rebuild is what no file states:** the method file, the names in the settings file, and the five
  strings by which a results file describes its toolkit. The two pairs of files differ in exactly those: two hashes,
  three strings and the free-form report of how the solve ended.
- **It passed eleven fewer arguments than the committed adapter and lost nothing.** Six of the eight placeholders,
  `T_retire`, `T_age`, `AgentCount`, the extra gridpoints and the printing switch were left to HARK's defaults. All
  seven arguments for which [the prototype](../2026-11-06_stone-data-prototype/README.md) found no stated reason are
  among them.
- **Fourteen statements were wrong, stale or at odds with each other**, in the stone, the cards or the hub: among them
  the method on the policy's interpolation, stated three ways that cannot all hold; the cards' setting names against
  the ladder's; source lines cited at HARK's main where the adapter runs the pin; and that the stone says "the adapter"
  of things the shared code does, never drawing the line between the two.

## dolo

Both runs completed and verified at the first attempt, and the agent went on to the other members, a variant with
a negative constraint, and the medium and high levels, which verified too. It reproduces every number the hub quotes
of dolo's committed files, to the digits quoted: the restrained kink and its slopes at the high level, the mass at the
constraint, the gaps to the restrained rule and their fall by decade of ℘, the shortfall of the MPC at the natural
limit and how it closes with the level, and the quantile table of the reference-solution document.

| member, low level | numbers the two files share | equal to the last bit | largest difference in c, and in the MPC, at the comparison points |
|---|---|---|---|
| `bst-restrained` | 1564 | 686 | 2.8 · 10⁻⁹ and 1.6 · 10⁻⁶ |
| `bst-p-zero-0.005` | 1525 | 546 | 4.5 · 10⁻⁹ and 1.3 · 10⁻⁶ |

The kink agrees to nine digits and the targets to 3 · 10⁻⁹. The differences are the size of the solver's tolerance,
the sum of the largest changes in the rule and the state falling below 10⁻⁸, reached from a different first rule.

- **What the documents did not give:** fourteen facts. Three were settled only by trial against numbers the hub
  quotes of the committed files: where the nested savings grid begins, how far above a natural limit the grid starts
  (10⁻⁶ reproduces three quoted numbers; 10⁻⁷, 10⁻⁹ and 10⁻⁵ do not), and that dolo's default limit of a thousand
  iterations is too few for the toy. One rests on knowledge from outside the sandbox: what the levels' nesting means,
  which no document defines. The rest came from dolo's source: the form the exogenous block must take for the model
  to be discretized at all, that the model file needs a calibration and a first rule, how the rule's values are read
  back and how it continues outside its points, that the request points fall on the uniform grid's nodes, what the
  solver returns, and that importing dolo silences NumPy's errors for the whole process and leaves an empty folder in
  the temporary directory each time, which the day's runs did thirty-one times.
- **What was left to the agent:** eighteen choices. The largest is the convention for the MPC at a point that is a
  node of the grid, which every request point is: the segment to its right, or to its left. The other choice moves
  the reported MPC at most of the request points, by up to 1.3 · 10⁻² at the low level, and nothing in the stone or
  the hub decides it.
- **What it could not rebuild:** the method file, the settings file and the five strings, as for HARK; and dolo's own
  worked example, which the stone describes without its calibration.
- **Ten statements were wrong, stale or at odds**, one of them only imprecise: the stone and the harness plan say the
  two adapters solve on the same savings grids, which the hub's own numbers contradict for the one setting the stone
  omits; the capabilities table says survival is tested at one only, while the toy it lists as tested has survival
  below one; the recast model, as the stone prints it, cannot be solved without a calibration and an exogenous block;
  two links point to the layout before the move; and the results document and its validator disagree on what a type
  holds.

## What it establishes, and what it does not

- **HARK's stone, with its ladder file and the shared code, is enough for the numbers.** The committed adapter's
  results were reproduced to the last bit by a reader that had never seen it. That reader read HARK's source eleven
  times to get there, so what sufficed was the stone and the toolkit's source together, not the stone alone.
- **dolo's stone is enough for the numbers to the solver's tolerance**, and not for the reported MPC, which rests on
  a convention no document states. Where its agent could not read a value in the stone it found it by trial against
  numbers the hub quotes of the committed files; a stone that stated them would have cost nothing.
- **Neither stone states what a results file says of its toolkit:** the method file, the settings file's names and
  the five identifying strings. These are the files and the block [the proposals](../../plans/2026-11-06_stones-as-data.md)
  add.
- **The shared code's protocol is understated.** Four facts both agents needed are in that code and in no document.
- **Both stones carry statements that are stale or wrong**, twenty-four between them, and the hub three of its own.
  The lists are in the two logs, for the model repository's session.
- It does not establish anything for the third toolkit, whose environment needs Bellman's package and HARK's run; nor
  what a reader without the toolkit's source could do; nor identity across machines, the measure having been taken on
  one. One agent wrote each part, once.

## The measure's commands

In each sandbox, with the toolkit's pinned interpreter, bytecode writing off and two threads:

```sh
./run-python harness/adapters/<toolkit>/adapter.py schemas/bst/artificial/members/bst-restrained.yaml \
    --out out/bst-restrained --level low --request schemas/bst/experiments/restrained-limit/bst-restrained.request.yaml
./run-python schemas/checker/check.py schemas/bst/artificial/members/bst-restrained.yaml \
    --verify-results out/bst-restrained/results.json
python measure.py <the committed adapter's results.json> out/bst-restrained/results.json
```
