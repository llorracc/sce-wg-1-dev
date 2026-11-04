"""The two questions of ../../../comparing-solutions.md, put to the restrained-limit runs: fidelity to the stated member,
and agreement between the toolkits. Reads results files only and solves nothing; writes report.md beside itself.

    uv run --with jsonschema --with pyyaml --with scipy --with referencing --with numpy \
        python schemas/records/findings/2026-11-03_two-questions-on-the-committed-runs/two_questions.py

The committed runs are the restrained-limit suite's of 2026-11-01, HARK's and dolo's, at levels 1 to 3. The method-only
step is in method-only/<toolkit>/<member>/level-4-nodes-31/: level 4's grids with level 3's nodes, so the same effective
member as level 3 and a finer solution of it.
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
METHOD_ONLY = HERE / "method-only"
if not METHOD_ONLY.is_dir():
    METHOD_ONLY = None
sys.path.insert(0, str(REPO / "schemas" / "checker"))
import bst1  # noqa: E402

FINDINGS = REPO / "schemas" / "records" / "findings"
RUNS = {"HARK": FINDINGS / "2026-11-01_restrained-limit-suite-hark" / "results",
        "dolo": FINDINGS / "2026-11-01_restrained-limit-suite-dolo" / "results"}
MEMBERS = {"bst-p-zero-0.005": "natural", "bst-p-zero-0.0005": "natural", "bst-p-zero-0.00005": "natural",
           "bst-restrained": "artificial"}
LABEL = {"bst-p-zero-0.005": "℘ = 0.005", "bst-p-zero-0.0005": "℘ = 0.0005", "bst-p-zero-0.00005": "℘ = 0.00005",
         "bst-restrained": "restrained"}
LEVELS = [1, 2, 3]
FLOOR = 1e-12          # the round-off floor on a named expectation's distance from its closed form
STEP = "3+"            # the method-only step's name in the tables: level 3's nodes, level 4's grids


def sci(x) -> str:
    if x is None:
        return "—"
    if x == 0:
        return "0"
    e = int(np.floor(np.log10(abs(x))))
    m = x / 10 ** e
    return f"{m:.2g} · 10^{e}"


def load(path: Path) -> dict | None:
    return json.loads(path.read_text()) if path.is_file() else None


files = {}
for tk, run in RUNS.items():
    for mem in MEMBERS:
        for lv in LEVELS:
            files[(tk, mem, lv)] = load(run / mem / f"level-{lv}" / "results.json")
        files[(tk, mem, STEP)] = load(METHOD_ONLY / tk.lower() / mem / "level-4-nodes-31" / "results.json") if METHOD_ONLY else None
closed = {mem: bst1.load_member(REPO / "schemas" / "bst" / scen / "members" / f"{mem}.yaml").expectations()
          for mem, scen in MEMBERS.items()}


def distance(E: dict, mem: str) -> dict:
    """Each named expectation's distance from its closed form: absolute, divided by the larger of one and the closed
    form's magnitude, as experiments.md defines max_relative_difference."""
    return {k: abs(E[k] - closed[mem][k]) / max(1.0, abs(closed[mem][k])) for k in closed[mem]}


def moved(a: dict, b: dict) -> float:
    """The largest relative movement of the named expectations between two effective members."""
    return max(abs(a[k] - b[k]) / max(1.0, abs(a[k])) for k in a)


out = []
P = out.append

# ---- Question 1a: the effective member against the closed forms
P("## Question 1a. Does the effective member approach the stated member?")
P("")
P("The largest distance of the ten named expectations from the checker's closed forms, by level, and the name that "
  "sets it. The two toolkits share one representation at every level (their effective members agree to 3 · 10^-15), "
  "so one table serves both. The mean of each law and E[ψ^(ϱ−1)] with ϱ = 2 sit at the floor at every level.")
P("")
P("| member | level 1 | level 2 | level 3 | ratio 1→2 | ratio 2→3 | at the floor at level 3 |")
P("|---|---|---|---|---|---|---|")
for mem in MEMBERS:
    d = [distance(files[("HARK", mem, lv)]["effective_member"]["expectations"], mem) for lv in LEVELS]
    worst = [max(x, key=x.get) for x in d]
    vals = [x[w] for x, w in zip(d, worst)]
    floor = sorted(k for k, v in d[2].items() if v <= FLOOR)
    P(f"| {LABEL[mem]} | {sci(vals[0])} ({worst[0]}) | {sci(vals[1])} ({worst[1]}) | {sci(vals[2])} ({worst[2]}) | "
      f"{vals[0] / vals[1]:.2f} | {vals[1] / vals[2]:.2f} | {', '.join(floor)} |")
P("")
P("Every name's distance by level, for the restrained member (the natural members' differ only in the worst income's "
  "mass, which is the stated ℘ at every level):")
P("")
names = list(closed["bst-restrained"])
P("| expectation | closed form | level 1 | level 2 | level 3 |")
P("|---|---|---|---|---|")
for k in names:
    row = [files[("HARK", "bst-restrained", lv)]["effective_member"]["expectations"][k] - closed["bst-restrained"][k] for lv in LEVELS]
    P(f"| {k} | {closed['bst-restrained'][k]:.10g} | {sci(row[0])} | {sci(row[1])} | {sci(row[2])} |")
P("")

# ---- Question 1b: the Euler residual under the stated laws, and under the toolkit's own laws
P("## Question 1b. Does the Euler residual under the stated laws fall along the ladder?")
P("")
P("The largest |r| over the request points, under the stated laws (the diagnostics' Gauss-Legendre quadrature, "
  "precision stated in each file) and under the toolkit's own representation of the laws (its nodes exactly), by "
  f"level. `{STEP}` is the method-only step: level 3's nodes with level 4's grids.")
P("")
P(f"| member | toolkit | laws | level 1 | level 2 | level 3 | {STEP} | ratio 2→3 | ratio 3→{STEP} |")
P("|---|---|---|---|---|---|---|---|---|")
for mem in MEMBERS:
    for tk in RUNS:
        for laws in ("stated", "own"):
            vals = []
            for lv in LEVELS + [STEP]:
                f = files[(tk, mem, lv)]
                if f is None:
                    vals.append(None)
                    continue
                er = f["types"][0]["euler_residuals"]
                vals.append(er["max_abs"] if laws == "stated" else max(abs(x) for x in er["under_effective_laws"]["r"]))
            r23 = vals[1] / vals[2]
            r3s = (vals[2] / vals[3]) if vals[3] else None
            P(f"| {LABEL[mem]} | {tk} | {laws} | {sci(vals[0])} | {sci(vals[1])} | {sci(vals[2])} | {sci(vals[3])} | "
              f"{r23:.2f} | {'—' if r3s is None else f'{r3s:.2f}'} |")
P("")

# where the residuals sit, for the member whose rule bends most
mem = "bst-p-zero-0.00005"
H, D = files[("HARK", mem, 3)]["types"][0], files[("dolo", mem, 3)]["types"][0]
pts = np.array(H["comparison_points"])
P(f"Where the residuals sit at level 3, {LABEL[mem]}, at the request points up to m = 0.2 and at m = 1:")
P("")
P("| m | c, HARK | c, dolo | \\|Δc\\|/c | r under own laws, HARK | r under own laws, dolo | r under stated laws, HARK | r under stated laws, dolo |")
P("|---|---|---|---|---|---|---|---|")
for i, m in enumerate(pts):
    if m <= 0.2 or m == 1.0:
        ch, cd = H["rule"]["c"][i], D["rule"]["c"][i]
        P(f"| {m:g} | {ch:.6f} | {cd:.6f} | {sci(abs(ch - cd) / ch)} | {sci(H['euler_residuals']['under_effective_laws']['r'][i])} | "
          f"{sci(D['euler_residuals']['under_effective_laws']['r'][i])} | {sci(H['euler_residuals']['r'][i])} | {sci(D['euler_residuals']['r'][i])} |")
P("")

# ---- Question 2: agreement, beside each toolkit's own movements and the kind of each step
P("## Question 2. Do the two toolkits' solutions coincide, and within what?")
P("")
P("The largest |c_HARK − c_dolo| at the request points (m ≤ 20, and all 39 points), beside each toolkit's own movement "
  f"of the rule between levels. The kind of each step is read from the effective member: it moves across a step that "
  f"changes the representation and is identical across one that does not.")
P("")
P(f"| member | HARK − dolo, level 3 (m ≤ 20 / all) | HARK 2→3 | dolo 2→3 | kind of 2→3 | HARK 3→{STEP} | dolo 3→{STEP} | kind of 3→{STEP} | HARK − dolo at {STEP} |")
P("|---|---|---|---|---|---|---|---|---|")
rel_rows = []
for mem in MEMBERS:
    h3, d3 = files[("HARK", mem, 3)], files[("dolo", mem, 3)]
    c_h3, c_d3 = np.array(h3["types"][0]["rule"]["c"]), np.array(d3["types"][0]["rule"]["c"])
    pts = np.array(h3["types"][0]["comparison_points"])
    diff = np.abs(c_h3 - c_d3)
    mv = {}
    for tk, f3, c3 in (("HARK", h3, c_h3), ("dolo", d3, c_d3)):
        c2 = np.array(files[(tk, mem, 2)]["types"][0]["rule"]["c"])
        mv[(tk, "2→3")] = float(np.abs(c3 - c2)[pts <= 20].max())
        fs = files[(tk, mem, STEP)]
        mv[(tk, f"3→{STEP}")] = float(np.abs(np.array(fs["types"][0]["rule"]["c"]) - c3)[pts <= 20].max()) if fs else None
        mv[(tk, f"3→{STEP} rel")] = float(np.max(np.abs(np.array(fs["types"][0]["rule"]["c"]) - c3) / c3)) if fs else None
    kind23 = moved(h3["effective_member"]["expectations"], files[("HARK", mem, 2)]["effective_member"]["expectations"])
    hs, ds = files[("HARK", mem, STEP)], files[("dolo", mem, STEP)]
    if hs and ds:
        kind3s = max(moved(hs["effective_member"]["expectations"], h3["effective_member"]["expectations"]),
                     moved(ds["effective_member"]["expectations"], d3["effective_member"]["expectations"]))
        dd = np.abs(np.array(hs["types"][0]["rule"]["c"]) - np.array(ds["types"][0]["rule"]["c"]))
        diff_s = float(dd[pts <= 20].max())
        rel_s = float(np.max(dd / np.array(hs["types"][0]["rule"]["c"])))
        where_s = float(pts[np.argmax(dd / np.array(hs["types"][0]["rule"]["c"]))])
    else:
        kind3s, diff_s, rel_s, where_s = None, None, None, None
    P(f"| {LABEL[mem]} | {sci(float(diff[pts <= 20].max()))} / {sci(float(diff.max()))} | {sci(mv[('HARK', '2→3')])} | "
      f"{sci(mv[('dolo', '2→3')])} | representation ({sci(kind23)}) | {sci(mv[('HARK', f'3→{STEP}')])} | {sci(mv[('dolo', f'3→{STEP}')])} | "
      f"{'—' if kind3s is None else ('method-only (' + sci(kind3s) + ')' if kind3s <= FLOOR else 'representation (' + sci(kind3s) + ')')} | {sci(diff_s)} |")
    rels = []
    for lv in LEVELS:
        a = np.array(files[("HARK", mem, lv)]["types"][0]["rule"]["c"]); b = np.array(files[("dolo", mem, lv)]["types"][0]["rule"]["c"])
        r = np.abs(a - b) / a
        rels.append((float(r.max()), float(pts[np.argmax(r)])))
    rel_rows.append((mem, rels, rel_s, where_s, mv.get(("HARK", f"3→{STEP} rel")), mv.get(("dolo", f"3→{STEP} rel"))))
P("")
P("The same on the relative scale, |c_HARK − c_dolo| / c_HARK over all 39 points, which the stone guide asks for the rule, "
  "with the point that sets it; and each toolkit's own relative movement across the method-only step:")
P("")
P(f"| member | level 1 | level 2 | level 3 | {STEP} | HARK 3→{STEP} | dolo 3→{STEP} |")
P("|---|---|---|---|---|---|---|")
for mem, rels, rel_s, where_s, mh, md in rel_rows:
    cells = " | ".join(f"{sci(r)} at m = {w:g}" for r, w in rels)
    P(f"| {LABEL[mem]} | {cells} | {'—' if rel_s is None else f'{sci(rel_s)} at m = {where_s:g}'} | {sci(mh)} | {sci(md)} |")
P("")
(HERE / "report.md").write_text("# The two questions, put to the committed runs: the tables\n\nWritten by `two_questions.py` "
                                 "from the results files; see README.md.\n\n" + "\n".join(out) + "\n", encoding="utf-8")
print(HERE / "report.md")
