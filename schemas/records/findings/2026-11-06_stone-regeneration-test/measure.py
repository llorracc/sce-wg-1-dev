"""A regenerated adapter's results file against the committed adapter's, for one member.

    python measure.py <the committed adapter's results.json> <the regenerated adapter's results.json>

Prints how many leaves the two files share and how many are equal, the largest differences in the rule and its
slope at the comparison points, the kink, the target and the mass at the constraint, and the leaves that differ
most. A difference is absolute for the rule and relative, floored at one, elsewhere.
"""
import json
import sys


def leaves(x, path=""):
    if isinstance(x, dict):
        for key, value in x.items():
            yield from leaves(value, f"{path}.{key}" if path else key)
    elif isinstance(x, list):
        for i, value in enumerate(x):
            yield from leaves(value, f"{path}[{i}]")
    else:
        yield path, x


def number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


a_doc, b_doc = (json.load(open(p, encoding="utf-8")) for p in sys.argv[1:3])
a, b = dict(leaves(a_doc)), dict(leaves(b_doc))
shared = [k for k in a if k in b]
numbers = [k for k in shared if number(a[k]) and number(b[k])]
equal = [k for k in numbers if a[k] == b[k]]
gap = {k: abs(a[k] - b[k]) / max(1.0, abs(a[k])) for k in numbers}
print(f"leaves: {len(a)} and {len(b)}; shared {len(shared)}; only in the first {len(set(a) - set(b))}, only in the second {len(set(b) - set(a))}")
print(f"shared numbers: {len(numbers)}; equal exactly {len(equal)}; within 1e-12 {sum(g <= 1e-12 for g in gap.values())}; "
      f"within 1e-8 {sum(g <= 1e-8 for g in gap.values())}; within 1e-4 {sum(g <= 1e-4 for g in gap.values())}")
for i, (ta, tb) in enumerate(zip(a_doc.get("types", []), b_doc.get("types", []))):
    dc = max(abs(x - y) for x, y in zip(ta["rule"]["c"], tb["rule"]["c"]))
    dm = max(abs(x - y) for x, y in zip(ta["rule"]["mpc"], tb["rule"]["mpc"]))
    line = f"type {i}: largest difference in c at the comparison points {dc:.2e}, in the MPC {dm:.2e}"
    for what in ("kink", "target", "pseudo_target"):
        ka, kb = ta.get(what, {}), tb.get(what, {})
        if ka.get("status") == "value" and kb.get("status") == "value":
            line += f"; {what} {ka['m']:.9f} against {kb['m']:.9f}"
        elif ka.get("status") != kb.get("status"):
            line += f"; {what} status {ka.get('status')} against {kb.get('status')}"
    print(line)
strings = [k for k in shared if not (number(a[k]) and number(b[k])) and a[k] != b[k]]
print(f"shared leaves that are not numbers and differ: {len(strings)}")
for k in strings[:12]:
    print("   ", k, "|", str(a[k])[:70], "|", str(b[k])[:70])
print("the numbers that differ most:")
for k in sorted(gap, key=gap.get, reverse=True)[:10]:
    if gap[k] > 0:
        print(f"    {gap[k]:.2e}  {k}  {a[k]!r} | {b[k]!r}")
