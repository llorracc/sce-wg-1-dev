# The checker

Draft; see the [README](../README.md) of the schemas.

The checker reads a parameter file and does what a validator cannot: it parses the file in the strict YAML subset, validates
it against the family's validator and the [shock-law validator](../shock-laws.schema.json), applies the rules of
[`shock-laws.md`](../shock-laws.md) and of the family, computes each law's moments in closed form, evaluates the family's
validity conditions, domain rules and implications as [`conditions.md`](../bst-1/conditions.md) states them, and prints the
model's hash.

```sh
cd schemas/checker
uv run --with jsonschema --with pyyaml --with scipy python check.py ../bst-1/members/toy.yaml
uv run --with jsonschema --with pyyaml --with scipy python check.py ../bst-1/members/library.yaml --bellman-calibration 0
uv run --with jsonschema --with pyyaml --with scipy --with pytest pytest -q
```

The second command writes the member's one-type calibration for the stage file `bst-1/bellman/buffer_stock.bl`, in the
stage's names, with a̲_Nat computed from the laws; it refuses a member whose laws have no Bellman-SYM family.

- [`canonical.py`](canonical.py): the strict YAML loader, the canonical serialization and the hash.
- [`laws.py`](laws.py): the shock laws, their rules and their closed-form moments.
- [`bst1.py`](bst1.py): the `bst/1` member, its validation, its conditions, its domain rules and its implications.
- [`check.py`](check.py): the command.
- [`test_checker.py`](test_checker.py): the laws' closed forms against numerical integration, the three members, and
  the rejections.
- [`test_results_schema.py`](test_results_schema.py): a results file in the shape of `results.md` against
  [`results.schema.json`](../bst-1/results.schema.json), and the rejections.

## The canonical form and the hash

The hash is the SHA-256 of a canonical JSON serialization of the parsed file: keys sorted, no white space, every number
written as the shortest decimal that reads back to the same double. So `0.10` and `0.1` hash alike, as do `1` and `1.0`,
while any change of value changes the hash. The strict subset keeps the parsed values unambiguous: no anchors, aliases,
tags or merge keys, no repeated keys, no booleans, no infinities.

## Rules of a `bst/1` member that the validator cannot express

- The types' shares sum to one, within 10⁻¹².
- The types are in strictly increasing order of β, so that a member has one written form.
- With an unemployment probability ℘ of zero, the unemployment income ξ̲ is zero, for the same reason.
- ℘ξ̲ < 1, so that employed income is positive.
- The artificial borrowing constraint a̲_Art, a number no greater than zero or the word `natural`, is no lower than the natural
  constraint a̲_Nat = −ξ̲_min κ/(1 − κ), with κ = ψ̲ 𝒢/R; a looser one never binds and would describe the same model.
- Each law passes its own rules.
- Every type passes the validity conditions: the FVAC, and the RIC or the WRIC.

## What the report holds

For each type: the factors and margins of every condition, the welfare condition among them; the implications (the limiting
MPC, the MPC at the lower limit); and the domain statuses (the targets, the kink, the two measures with their tail exponents,
their means and variances, and welfare). For the member: the laws' moments, the lowest value of the transitory shock, the
worst-income probability p̲, the natural borrowing constraint, the constraint written, the employed draw's scale, and the
lowest resources a newborn can have.

## Verifying a results file

    uv run --with jsonschema --with pyyaml --with scipy python check.py ../bst-1/members/toy.yaml --verify-results r.json

validates the results file against `bst-1/results.schema.json` and verifies its report on the toolkit's effective member
against the member (`effective-member.md`): each factor as the arithmetic of the reported expectations and the parameters,
each verdict against its factor, each status against the verdicts, each derived parameter as the arithmetic of the reported
lowest values, the lowest values against the stated member's infima, and the expectations against what every law obeys.
The expectations' values themselves are the toolkit's and are trusted. The member's own report is the stated member's, the
limit a toolkit's effective member approaches; a condition whose margin lies within the closed forms' precision is marked
`undecided`.

When the results file carries `effective_member.population`, the population's expectations decide the GIC-Szeidl, the
GIC-Harmenberg and the welfare conditions, and its lowest values are held to the stated infima too; the household's block
decides the rest.
