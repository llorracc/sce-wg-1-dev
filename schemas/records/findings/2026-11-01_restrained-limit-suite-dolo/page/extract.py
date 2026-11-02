"""The data of the page "The Restrained Limit", with both toolkits, from the level-3 results files of HARK's run and
dolo's, and the page itself.

    uv run --with numpy python extract.py

It writes data.json and restrained-limit.html, the page as published: template.html with the data in place of
__DATA__. For each toolkit: the rules on dense points, the MPCs as differences of those points, each natural rule's gap
to the restrained one, the largest gaps at every level, and the stationary population; and the two toolkits' difference
at the common points. The largest distance between the differenced MPCs and the MPCs the results files report at the
common points is printed.
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RUNS = {"HARK": HERE.parent.parent / "2026-11-01_restrained-limit-suite-hark" / "results",
        "dolo": HERE.parent / "results"}
NAT = ["bst-p-zero-0.005", "bst-p-zero-0.0005", "bst-p-zero-0.00005"]
RES = "bst-restrained"
MMAX = 3.0


def t(run, member, level=3):
    return json.loads((run / member / f"level-{level}" / "results.json").read_text())["types"][0]


def sig(x, n=6):
    return float(f"{x:.{n}g}")


def rule_points(tt):
    """The rule on its dense points up to MMAX, with the common points below them and the kink's point added."""
    er = tt["exported_rule"]
    md, cd = np.array(er["m"]), np.array(er["c"])
    cp, cc = np.array(tt["comparison_points"]), np.array(tt["rule"]["c"])
    low = cp < md.min()
    m = np.concatenate([[0.0], cp[low], md[md <= MMAX + 1e-12]])
    c = np.concatenate([[0.0], cc[low], cd[md <= MMAX + 1e-12]])
    if tt["kink"]["status"] == "value":
        m = np.append(m, tt["kink"]["m"]); c = np.append(c, tt["kink"]["m"])
    o = np.argsort(m, kind="stable"); m, c = m[o], c[o]
    u = np.concatenate([[True], np.diff(m) > 1e-12])
    return m[u], c[u]


def mpc_points(tt, m, c):
    """The MPC as differences of the rule's points; exactly 1 below a kink, and differenced separately above it."""
    if tt["kink"]["status"] != "value":
        return m, np.gradient(c, m)
    k = tt["kink"]["m"]
    below, above = m <= k + 1e-12, m >= k - 1e-12
    return np.concatenate([m[below], m[above]]), np.concatenate([np.ones(below.sum()), np.gradient(c[above], m[above])])


out = {"toolkits": {}}
check = {}
for name, run in RUNS.items():
    rules, mpcs = {}, {}
    for mem in NAT + [RES]:
        tt = t(run, mem)
        m, c = rule_points(tt)
        rules[mem] = (m, c)
        mm, dd = mpc_points(tt, m, c)
        mpcs[mem] = (mm, dd)
        cp, rep = np.array(tt["comparison_points"]), np.array(tt["rule"]["mpc"])
        sel = (cp <= MMAX) & (np.abs(cp - (tt["kink"].get("m") or -9)) > 0.02)
        o = np.argsort(mm, kind="stable")
        check[(name, mem)] = float(np.max(np.abs(np.interp(cp[sel], mm[o], dd[o]) - rep[sel])))
    gmax = min(float(v[0][-1]) for v in rules.values())
    grid = np.round(np.arange(0, gmax + 1e-9, 0.005), 3)
    cr = np.interp(grid, *rules[RES])
    gaps = {mem: cr - np.interp(grid, *rules[mem]) for mem in NAT}
    conv = {}
    for lv in (1, 2, 3):
        base = np.array(t(run, RES, lv)["rule"]["c"])
        conv[lv] = [float(np.max(np.abs(base - np.array(t(run, mem, lv)["rule"]["c"])))) for mem in NAT]
    pop = {}
    for mem in NAT + [RES]:
        p = t(run, mem)["population"]; gl = p["a"]["gl"]
        pop[mem] = {"mean_mpc": p["mean_mpc"], "mass": p["mass_at_constraint"], "bottom10": gl["0.1"] / gl["1"]}
    kink = t(run, RES)["kink"]
    out["toolkits"][name] = {
        "kink": {"m": kink["m"], "slope_above": kink["slope_above"]},
        "rules": {k: [[sig(a), sig(b)] for a, b in zip(*v)] for k, v in rules.items()},
        "mpc": {k: [[sig(a), sig(b, 4)] for a, b in zip(*v)] for k, v in mpcs.items()},
        "gap": {"m": grid.tolist(), **{k: [sig(x, 4) for x in v] for k, v in gaps.items()}},
        "convergence": conv, "population": pop}
out["difference"] = {}
for mem in NAT + [RES]:
    a, b = t(RUNS["HARK"], mem), t(RUNS["dolo"], mem)
    assert a["comparison_points"] == b["comparison_points"]
    d = np.abs(np.array(a["rule"]["c"]) - np.array(b["rule"]["c"]))
    out["difference"][mem] = [[p, sig(max(x, 1e-17), 4)] for p, x in zip(a["comparison_points"], d)]
print("max |differenced MPC - reported MPC| at the common points:", {f"{k[0]} {k[1]}": round(v, 4) for k, v in check.items()},
      file=sys.stderr)
data = json.dumps(out, separators=(",", ":"))
(HERE / "data.json").write_text(data, encoding="utf-8")
page = (HERE / "template.html").read_text(encoding="utf-8").replace("const DATA = __DATA__;", "const DATA = " + data + ";")
assert "__DATA__" not in page
(HERE / "restrained-limit.html").write_text(page, encoding="utf-8")
