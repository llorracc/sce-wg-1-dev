"""The data of the page "The Restrained Limit", from the level-3 results files beside it, and the page itself.

    uv run --with numpy python extract.py

It writes data.json and restrained-limit.html, the page as published: template.html with the data in place of
__DATA__. The MPC curves are differences of each rule's dense points; their largest distance from the MPCs the results
files report at the common points is printed.
"""
import json, sys
import numpy as np
HERE = __import__("pathlib").Path(__file__).resolve().parent
F = str(HERE.parent / "results")
NAT = ["bst-p-zero-0.005", "bst-p-zero-0.0005", "bst-p-zero-0.00005"]; RES = "bst-restrained"
def t(member, level=3):
    return json.load(open(f"{F}/{member}/level-{level}/results.json"))["types"][0]
def sig(x, n=6): return float(f"{x:.{n}g}")
MMAX = 3.0
rules, mpcs, check = {}, {}, {}
for mem in NAT:
    tt = t(mem); er = tt["exported_rule"]
    m = np.array(er["m"]); c = np.array(er["c"]); o = np.argsort(m); m, c = m[o], c[o]
    keep = m <= MMAX + 1e-12; m, c = m[keep], c[keep]
    rules[mem] = (m, c)
    d = np.gradient(c, m)
    mpcs[mem] = (m, d)
    cp = np.array(tt["comparison_points"]); rep = np.array(tt["rule"]["mpc"]); sel = cp <= MMAX
    check[mem] = float(np.max(np.abs(np.interp(cp[sel], m, d) - rep[sel])))
tt = t(RES); er = tt["exported_rule"]; kink = tt["kink"]
md = np.array(er["m"]); cd = np.array(er["c"]); o = np.argsort(md); md, cd = md[o], cd[o]
cp = np.array(tt["comparison_points"]); cc = np.array(tt["rule"]["c"])
low = cp < md[0]
m = np.concatenate([[0.0], cp[low], md[md <= MMAX + 1e-12], [kink["m"]]]); c = np.concatenate([[0.0], cc[low], cd[md <= MMAX + 1e-12], [kink["m"]]])
o = np.argsort(m, kind="stable"); m, c = m[o], c[o]
u = np.concatenate([[True], np.diff(m) > 1e-12]); m, c = m[u], c[u]
rules[RES] = (m, c)
below = m <= kink["m"] + 1e-12; above = m >= kink["m"] - 1e-12
ma, ca = m[above], c[above]
d_above = np.gradient(ca, ma)
mpcs[RES] = (np.concatenate([m[below], ma]), np.concatenate([np.ones(below.sum()), d_above]))
rep = np.array(tt["rule"]["mpc"]); sel = (cp <= MMAX) & (np.abs(cp - kink["m"]) > 0.02)
mm, dd = mpcs[RES]; check[RES] = float(np.max(np.abs(np.interp(cp[sel], mm[np.argsort(mm, kind='stable')], dd[np.argsort(mm, kind='stable')]) - rep[sel])))
print("max |numerical MPC - reported MPC| at comparison points:", {k: round(v, 4) for k, v in check.items()}, file=sys.stderr)
gmax = min(float(v[0][-1]) for v in rules.values())   # the shortest rule's last point: no extrapolation
grid = np.round(np.arange(0, gmax + 1e-9, 0.005), 3)
cr = np.interp(grid, *rules[RES])
gaps = {mem: cr - np.interp(grid, *rules[mem]) for mem in NAT}
conv = {}
for lv in (1, 2, 3):
    b = t(RES, lv); cpts = np.array(b["rule"]["c"])
    conv[lv] = [float(np.max(np.abs(cpts - np.array(t(mem, lv)["rule"]["c"])))) for mem in NAT]
pop = {}
for mem in NAT + [RES]:
    p = t(mem)["population"]; gl = p["a"]["gl"]
    pop[mem] = {"mean_mpc": p["mean_mpc"], "mass": p["mass_at_constraint"], "bottom10": gl["0.1"] / gl["1"]}
out = {
  "kink": {"m": kink["m"], "slope_above": kink["slope_above"]},
  "rules": {k: [[sig(a), sig(b)] for a, b in zip(*v)] for k, v in rules.items()},
  "mpc": {k: [[sig(a), sig(b, 4)] for a, b in zip(*v)] for k, v in mpcs.items()},
  "gap": {"m": grid.tolist(), **{k: [sig(x, 4) for x in v] for k, v in gaps.items()}},
  "convergence": conv, "population": pop,
}
data = json.dumps(out, separators=(",", ":"))
(HERE / "data.json").write_text(data, encoding="utf-8")
page = (HERE / "template.html").read_text(encoding="utf-8").replace("const DATA = __DATA__;", "const DATA = " + data + ";")
assert "__DATA__" not in page
(HERE / "restrained-limit.html").write_text(page, encoding="utf-8")
print({k: len(v) for k, v in out["rules"].items()}, "max gaps L3:", [round(x, 4) for x in conv[3]], file=sys.stderr)
