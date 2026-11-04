"""Tables from the convergence study, the default-settings solves and the committed level-3 files. Reads only."""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from reference_dist import load_rule  # noqa: E402

MEMBERS = ["bst-p-zero-0.005", "bst-p-zero-0.0005", "bst-p-zero-0.00005", "bst-restrained"]
SETTINGS = ["A", "B", "C", "D", "E", "F", "G"]
# each setting's base: what it refines, so that the movement from the base is the base's error on what changed
BASE = {"B": "A", "C": "B", "D": "C", "E": "B", "F": "E", "G": "E"}
WHAT = {"A": "1,000 points to 200, 32 nodes a piece", "B": "2,000 points to 400 (A doubled)", "C": "B at 64 nodes a piece",
        "D": "4,000 points to 1,000 at 64 nodes (C doubled)", "E": "B with 3,000 extra points near the limit",
        "F": "E at 64 nodes a piece", "G": "E with 6,000 extra points near the limit"}


def sci(x):
    return "—" if x is None else f"{x:.2e}"


def main():
    runs, rules = {}, {}
    for mem in MEMBERS:
        for s in SETTINGS:
            f = HERE / "runs" / mem / s / "result.json"
            if f.is_file():
                runs[(mem, s)] = json.loads(f.read_text())
                rules[(mem, s)] = load_rule(HERE / "runs" / mem / s)
    defaults = {}
    for mem in MEMBERS:
        f = HERE / "default" / "hark" / mem / "result.json"
        if f.is_file():
            defaults[mem] = json.loads(f.read_text())
    print("## The convergence study: each setting, and the rule's movement from its base, at the request points up to m = 50")
    print()
    for s in SETTINGS:
        print(f"- {s}: {WHAT[s]}" + (f"; its base is {BASE[s]}" if s in BASE else ""))
    print()
    print("| member | setting | grid size | iterations | bound on the distance | max abs r (32) | (64) | diagnostic's precision | movement from the base (max rel, at m) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for mem in MEMBERS:
        for s in SETTINGS:
            r = runs.get((mem, s))
            if r is None:
                continue
            pts = np.asarray(r["request_points"])
            move = "—"
            b = BASE.get(s)
            if b and (mem, b) in rules:
                c0, c1 = rules[(mem, b)](pts), rules[(mem, s)](pts)
                rel = np.abs(c1 - c0) / c1
                move = f"{rel.max():.2e} (m = {pts[int(np.argmax(rel))]:g})"
            st, e, c = r["settings"], r["euler_stated"], r["convergence"]
            print(f"| {mem} | {s} | {st['grid_size']} | {c['iterations']} | "
                  f"{sci(c['distance_bound'])} | {sci(e['max_abs_32'])} | {sci(e['max_abs_64'])} | {sci(e['precision'])} | "
                  f"{move} |")
    print()
    print("## The closed forms")
    print()
    for mem in MEMBERS:
        for s in SETTINGS:
            r = runs.get((mem, s))
            if r is None:
                continue
            if "kink" in r:
                k = r["kink"]
                print(f"- {mem} {s}: kink m = {k['m']:.12f}, slope above {k['slope_right']:.8f}, c − (m − a_lo) below: {k['c_minus_m_below']:.1e}")
            else:
                k = r["mpc_at_limit"]
                sec = k["secants"]
                worst = max(abs(v - k["closed_form"]) for v in sec.values())
                print(f"- {mem} {s}: MPC at the limit, closed form {k['closed_form']:.12f}; the rule's secants from 1e-9 to 1e-5 "
                      f"above it differ from it by at most {worst:.1e}; the first endogenous points' EGM slopes "
                      f"{[f'{x:.12f}' for x in k['first_points_slope']]}")
    print()
    print("## Distances from the finest setting available: the committed level-3 rules and HARK at its default settings")
    print()
    print("| member | finest | HARK level 3, max rel (at m) | dolo level 3 | HARK default, max rel (at m) | HARK default, m ≤ 20 (at m) | HARK default, kink | HARK default, max abs r | finest's max abs r |")
    print("|---|---|---|---|---|---|---|---|---|")
    for mem in MEMBERS:
        avail = [s for s in SETTINGS if (mem, s) in runs]
        if not avail:
            continue
        s = avail[-1]
        r = runs[(mem, s)]
        pts = np.asarray(r["request_points"])
        cref = rules[(mem, s)](pts)
        l3 = r["level3_distance"]
        dft = defaults.get(mem)
        if dft:
            cd = np.asarray(dft["c"])
            rel = np.abs(cd - cref) / cref
            dd = f"{rel.max():.2e} (m = {pts[int(np.argmax(rel))]:g})"
            sel = pts <= 20
            d20 = f"{rel[sel].max():.2e} (m = {pts[sel][int(np.argmax(rel[sel]))]:g})"
            dk = f"{dft['kink']['m'] - r['kink']['m']:+.2e}" if dft.get("kink") and r.get("kink") else "—"
            dr = sci(dft["euler_stated"]["max_abs"])
        else:
            dd, d20, dk, dr = "—", "—", "—", "—"
        print(f"| {mem} | {s} | {l3['HARK']['max_rel']:.2e} (m = {l3['HARK']['at_m']:g}) | {l3['dolo']['max_rel']:.2e} (m = {l3['dolo']['at_m']:g}) | "
              f"{dd} | {d20} | {dk} | {dr} | {sci(r['euler_stated']['max_abs_32'])} |")
    dists = {}
    for f in sorted((HERE / "dist").glob("*/*/result.json")):
        d = json.loads(f.read_text())
        dists[(d["member"], d["nodes_per_shock"])] = d
    if dists:
        print()
        print("## The ergodic distribution on the dense grid: the grid's effect, the transition's nodes' effect, and level 3")
        print()
        print("Pass 1 is the bench's geometric grid (4,000 points to 60); pass 2 is uniform to the 99.9th percentile of a, "
              "32,000 points, then geometric to 300. Relative changes; the mass at the constraint absolute.")
        print()
        print("| member | nodes a shock | a at 0.999 (dense) | mean a: pass 2 − pass 1 | median a | a at 0.999 | mean MPC | mass at the constraint | mass beyond the dense part | level 3 − dense: mean a | median a | mean MPC |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for (mem, n), d in dists.items():
            b1, b2, l3 = d["pass1"]["block"], d["pass2"]["block"], d["level3"]["HARK"]
            g = lambda b, k: b["a"]["gl"]["1"] if k == "mean" else b["a"]["quantiles"][k] if k in ("0.5", "0.999") else b[k]
            rel = lambda k: (g(b2, k) - g(b1, k)) / g(b2, k)
            rel3 = lambda k: (g(l3, k) - g(b2, k)) / g(b2, k)
            mass = f"{b2['mass_at_constraint'] - b1['mass_at_constraint']:+.1e}" if not isinstance(b2["mass_at_constraint"], dict) else "—"
            print(f"| {mem} | {n} | {b2['a']['quantiles']['0.999']:.6f} | {rel('mean'):+.1e} | {rel('0.5'):+.1e} | {rel('0.999'):+.1e} | "
                  f"{rel('mean_mpc'):+.1e} | {mass} | {d['pass2']['mass_beyond_dense']:.2e} | {rel3('mean'):+.1e} | {rel3('0.5'):+.1e} | {rel3('mean_mpc'):+.1e} |")
        pairs = [(mem, 31, 63) for mem in MEMBERS if (mem, 31) in dists and (mem, 63) in dists]
        if pairs:
            print()
            print("The transition's nodes doubled, on the dense grid (relative change from 31 to 63 nodes a shock; the mass "
                  "at the constraint absolute):")
            print()
            print("| member | mean a | median a | a at 0.9 | a at 0.999 | mean MPC | mass at the constraint |")
            print("|---|---|---|---|---|---|---|")
            for mem, n1, n2 in pairs:
                a, b = dists[(mem, n1)]["pass2"]["block"], dists[(mem, n2)]["pass2"]["block"]
                r = lambda f: (f(b) - f(a)) / f(a) if f(a) else float("nan")
                mass = (f"{b['mass_at_constraint'] - a['mass_at_constraint']:+.1e}"
                        if not isinstance(a["mass_at_constraint"], dict) else "—")
                print(f"| {mem} | {r(lambda x: x['a']['gl']['1']):+.1e} | {r(lambda x: x['a']['quantiles']['0.5']):+.1e} | "
                      f"{r(lambda x: x['a']['quantiles']['0.9']):+.1e} | {r(lambda x: x['a']['quantiles']['0.999']):+.1e} | "
                      f"{r(lambda x: x['mean_mpc']):+.1e} | {mass} |")
    if defaults:
        print()
        print("## HARK at its default settings: the kink, and the residual by point")
        print()
        for mem, d in defaults.items():
            pts = np.asarray(d["request_points"])
            rr = np.asarray(d["euler_stated"]["r"])
            worst = np.argsort(-np.abs(rr))[:4]
            print(f"- {mem}: cycles {d['completed_cycles']}, last step {d['solution_distance']:.1e}, kink {d['kink'] and round(d['kink']['m'], 8)}; "
                  f"the largest |r| at m = {[f'{pts[i]:g}: {rr[i]:.1e}' for i in worst]}")


if __name__ == "__main__":
    main()
