# HARK's adapter with its arguments in a data file: a prototype

Made on 2026-11-06 between 17:02 and 17:05 EST, for [the proposals on what a Rosetta Stone
holds](../../plans/2026-11-06_stones-as-data.md). The question: can the arguments an adapter passes its toolkit be data
that the adapter reads, in place of code?

## What was done

A scratch copy was taken of HARK's adapter, with its ladder file, the code the adapters share and the schemas, from the
buffer-stock model's repository at its commit `af1539c` of that day. In the copy's solve, the block of literal keyword
arguments was replaced by two calls to a helper that reads a data file; the two objects the adapter builds itself, the
chain and the income process, stay code and are handed to the helper by name. Nothing was changed in that repository.

| file | what it is |
|---|---|
| [`hark.stone.yaml`](hark.stone.yaml) | the data file, in the schemas' strict YAML subset: every value is the committed adapter's |
| [`from_stone.py`](from_stone.py) | the helper: it assembles a handler's keyword arguments from such a file; nothing in it is HARK's |
| [`compare_leaves.py`](compare_leaves.py) | two results files compared leaf by leaf |

The data file keeps apart what answers different questions:

| block | what it holds | entries for HARK |
|---|---|---|
| `arguments` | the model's inputs: each parameter-file key with the toolkit's name and shape for it | 6 |
| `fixed` | what the adapter decides, the same for every member, each with its reason | 10 |
| `placeholders` | what the toolkit asks for although the adapter replaces what it would build from it | 8 |
| `settings` | the method's inputs, by name only; their values at each level are the ladder file's | 5 |
| `built_by_the_adapter` | what stays code, by the routine's name and what it makes | 2 |
| `switched_off` | the toolkit's constructors the adapter turns off, and why | 2 |
| `read_back`, `asserted_after_the_solve` | where the solution is read and what is checked; listed, still code | 3 and 3 |

A value that is not a plain number or string is written as the toolkit's own literal in a string, `"True"`, `"None"`,
`"[None]"`, since the strict subset has no booleans or nulls; `as: array` makes an array of it. The helper refuses what
would otherwise fail inside the toolkit, far from its cause: a member key the parameter file lacks, a shape the file
does not define, a setting the ladder does not state, an argument given twice, a built object the file does not name.

## What it showed

On one machine, in HARK's pinned environment with two threads, for `bst-restrained` and `bst-p-zero-0.005` at the low
level with the restrained-limit experiment's request files:

| member | leaves in the results file | of them numbers | that differ from the committed adapter's |
|---|---|---|---|
| `bst-restrained` | 1627 | 1568 | 0 |
| `bst-p-zero-0.005` | 1596 | 1529 | 0 |

The method, settings and gridpoints files are identical byte for byte.

- **The names can be checked against the toolkit.** Of the 33 names in the data file, 28 are keys of HARK's own
  dictionary of defaults at the pin; `tolerance` is read by HARK and not listed there; the chain and the income process
  are constructors HARK has. A test that every name in a stone exists in its toolkit at the pin, deferred since
  2026-10-31, is a dozen lines once the names are data.
- **A reason has to be written for each fixed argument, and seven have none in the stone:** `T_retire`, `T_age`,
  `AgentCount`, `TranShkStd`, `TranShkCount`, `UnempPrbRet` and `IncUnempRet`. The file marks them.

## What it establishes, and what it does not

- For a toolkit called with keyword arguments, every argument but those the adapter builds can leave the adapter's
  code without a number changing, and the helper that reads them is the same for any such toolkit.
- It establishes nothing for a toolkit whose part is mostly a model's text, as dolo's is, or functions replaced from
  outside in an imported toolkit: those need the file's lists of named routines, which this prototype states and
  does not use.
- The read-back and the assertions are listed in the file and still code.
- Whether HARK needs each placeholder was not tested.
- A data file read at run time is one more file that a job's fingerprint has to cover.

## The commands

In the scratch copy, with HARK's pinned interpreter, bytecode writing off and two threads:

```sh
python harness/adapters/hark/adapter.py schemas/bst/artificial/members/bst-restrained.yaml \
    --out out/bst-restrained --level low --request schemas/bst/experiments/restrained-limit/bst-restrained.request.yaml
python harness/adapters/hark/adapter.py schemas/bst/natural/members/bst-p-zero-0.005.yaml \
    --out out/bst-p-zero-0.005 --level low --request schemas/bst/experiments/restrained-limit/bst-p-zero-0.005.request.yaml
python compare_leaves.py <the committed adapter's results.json> out/<member>/results.json
```
