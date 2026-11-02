# Adapters

An adapter runs one toolkit on the schemas' files. It reads a parameter file, solves the member with its toolkit, and
writes the files the schemas define: a request file of comparison points, a method file, a settings file and a results
file. The [checker](../checker/) then verifies the results file against the member
(`check.py <member> --verify-results <results.json>`). Two toolkits' results files for the same member can then be
compared by the rules of the [Rosetta Stones](../rosetta/).

An adapter states what its toolkit actually solved, its effective member ([effective-member.md](../effective-member.md)).
It reports every condition and status on that member by its own verdicts, and it pins the toolkit's version.

| adapter | toolkit | family | status |
|---|---|---|---|
| [`hark/`](hark/) | HARK's `MarkovConsumerType`, at the head of HARK's draft pull request #1862, stacked on #1858 | the four buffer-stock families | first version |
| [`dolo/`](dolo/) | dolo's release 0.4.9.20, its endogenous grid method `egm`, on Python 3.11 | `bst-natural/1` and `bst-artificial/1`; the two in `bst/other/` not yet tried | first version, written from the schemas; its Rosetta Stone is [`../rosetta/dolo.md`](../rosetta/dolo.md) |

What does not depend on the toolkit is shared, in [`common.py`](common.py): the laws' nodes, the effective member and
its conditions, the stationary population, the statistics, the residuals and the files. Each adapter supplies its
toolkit's solve and its description, and calls `common.run`. On the same member, level and request, the two adapters
solve on the same nodes and savings grids, so a difference between their results files is the toolkits'.
