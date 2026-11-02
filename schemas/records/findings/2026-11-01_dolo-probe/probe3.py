"""The probe at matching nodes and finer grids: dolo against HARK's level-1 and level-3 results files (README.md)."""
import sys
exec(open(__import__("pathlib").Path(__file__).with_name("probe.py")).read().split("for name, scen in")[0])
import numpy as np
F = REPO / "records/findings/2026-11-01_restrained-limit-suite-hark/results"
for name, scen in (("bst-restrained", "artificial"), ("bst-p-zero-0.005", "natural")):
    hk = {lv: json.loads((F / name / f"level-{lv}/results.json").read_text())["types"][0] for lv in (1, 3)}
    pts = np.array(hk[1]["comparison_points"])
    for n_nodes, n_a in ((7, 300), (7, 1200), (31, 1200)):
        member, sol = solve(REPO / "bst" / scen / "members" / f"{name}.yaml", n_nodes=n_nodes, n_a=n_a, m_hi=200.0, n_m=40001, a_top=400.0)
        c_d = sol.dr(pts[:, None]).ravel()
        for lv in (1, 3):
            d = c_d - np.array(hk[lv]["rule"]["c"]); sel = pts <= 20
            print(f"{name} dolo(nodes {n_nodes}, a-points {n_a}) vs HARK level {lv}: max|diff| m<=20 {np.abs(d[sel]).max():.1e}, at m=10 {d[pts==10][0]:+.1e}")
