"""The prototype of the harness's comparator (../../../harness.md): an experiment's checks on runs laid out <member>/level-<n>/results.json.

    cd schemas && uv run --with pyyaml python records/findings/2026-11-02_experiment-checks/eval_checks.py \
        bst/suites/restrained-limit/experiment.yaml HARK <HARK run> dolo <dolo run>
"""
import json, sys, pathlib, itertools
sys.path.insert(0, "checker"); import canonical
LEVEL = {"low": 1, "medium": 2, "high": 3}
def numbers(x, path):
    head, _, rest = path.partition(".")
    key, every = (head[:-2], True) if head.endswith("[]") else (head, False)
    v = x[key]
    items = v if every else [v]
    out = []
    for it in items:
        if rest: out += numbers(it, rest)
        else: out += list(flat(it))
    return out
def flat(v):
    if isinstance(v, bool) or v is None or isinstance(v, str): return
    if isinstance(v, (int, float)): yield float(v)
    elif isinstance(v, dict):
        for k in sorted(v): yield from flat(v[k])
    elif isinstance(v, list):
        for i in v: yield from flat(i)
def metric(name, a, b):
    assert len(a) == len(b), (len(a), len(b))
    if name == "max_abs_difference": return max(abs(x - y) for x, y in zip(a, b))
    return max(abs(x - y) / max(1.0, abs(x)) for x, y in zip(a, b))
exp = canonical.load_strict(open(sys.argv[1], encoding="utf-8").read())
runs = dict(zip(sys.argv[2::2], map(pathlib.Path, sys.argv[3::2])))
res = lambda tk, m, lv: json.load(open(runs[tk] / m / f"level-{LEVEL[lv]}" / "results.json"))
ids = [m["id"] for m in exp["members"]]
for c in exp["checks"]:
    verdicts = []
    if c["compare"] == "members":
        for tk, lv in itertools.product(runs, exp["levels"]):
            vals = [metric(c["metric"], numbers(res(tk, a, lv), c["quantity"]), numbers(res(tk, b, lv), c["quantity"])) for a, b in c["pairs"]]
            ok = all(x > y for x, y in zip(vals, vals[1:]))
            verdicts.append((f"{tk} {lv}", vals, ok))
    elif c["compare"] == "toolkits":
        for (ta, tb), m in itertools.product(itertools.combinations(runs, 2), c.get("members", ids)):
            vals = [metric(c["metric"], numbers(res(ta, m, lv), c["quantity"]), numbers(res(tb, m, lv), c["quantity"])) for lv in exp["levels"]]
            e = c["expect"]
            ok = all(x > y for x, y in zip(vals, vals[1:])) if e == "falls_with_level" else all(v <= e["at_most"] for v in vals)
            verdicts.append((f"{ta}-{tb} {m}", vals, ok))
    print(c["id"], "PASS" if all(v[2] for v in verdicts) else "FAIL")
    for name, vals, ok in verdicts: print(f"   {name:34s} {' '.join(f'{v:.3g}' for v in vals)} {'ok' if ok else 'FAILS'}")
