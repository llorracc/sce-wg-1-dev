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
| [`hark/`](hark/) | HARK's `MarkovConsumerType`, at the head of HARK's draft pull request #1862, stacked on #1858 | `bst/1` | first version |
| `dolo/` | dolo | `bst/1` | planned, written from the schemas |
