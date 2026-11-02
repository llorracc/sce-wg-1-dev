"""Compare two toolkits' results files for the restrained-limit suite (../../model.md, "The restrained-limit suite"),
member by member and level by level, at the suite's common points.

    uv run --with matplotlib --with numpy python compare_toolkits.py NAME_A RUN_A NAME_B RUN_B OUT_DIR

Each RUN holds one folder per member, each with `level-<n>/results.json`, as compare.py reads them. OUT_DIR receives
`toolkits.md`, the tables, and `toolkits.png`, the figure. Nothing is solved: everything comes from the results files.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

NATURAL = ["bst-p-zero-0.005", "bst-p-zero-0.0005", "bst-p-zero-0.00005"]
P_ZERO = {"bst-p-zero-0.005": "0.005", "bst-p-zero-0.0005": "0.0005", "bst-p-zero-0.00005": "0.00005"}
RESTRAINED = "bst-restrained"
MEMBERS = NATURAL + [RESTRAINED]


def load(run: Path) -> dict:
    out = {}
    for member in MEMBERS:
        for level_dir in sorted((run / member).glob("level-*")):
            f = level_dir / "results.json"
            if f.is_file():
                out[(member, int(level_dir.name.split("-")[1]))] = json.loads(f.read_text())["types"][0]
    return out


def fmt(x) -> str:
    return "—" if x is None else f"{x:.3g}"


def label(member: str) -> str:
    return f"℘ = {P_ZERO[member]}" if member in P_ZERO else "restrained"


def main(name_a: str, run_a: Path, name_b: str, run_b: Path, out: Path) -> None:
    A, B = load(run_a), load(run_b)
    levels = sorted({lv for (m, lv) in A if all((x, lv) in A and (x, lv) in B for x in MEMBERS)})
    out.mkdir(parents=True, exist_ok=True)
    lines = [f"# The restrained-limit suite: {name_a} against {name_b}", "",
             f"From the results files in `{run_a.parent.name}/{run_a.name}` ({name_a}) and `{run_b.parent.name}/{run_b.name}` ({name_b}), levels "
             f"{', '.join(map(str, levels))}, at the suite's common points in m. Both toolkits' adapters solve the same "
             "effective member on the same nodes and savings grid at each level.", "",
             "![The two toolkits' rules near the kink, and their difference](toolkits.png)", "",
             f"## The largest difference between the rules, |c_{name_a} − c_{name_b}|", "",
             "| member | " + " | ".join(f"level {lv}, m ≤ 20" for lv in levels) + " | " + " | ".join(f"level {lv}, all" for lv in levels) + " |",
             "|---|" + "---|" * (2 * len(levels))]
    for member in MEMBERS:
        row = []
        for lv in levels:
            a, b = A[(member, lv)], B[(member, lv)]
            assert a["comparison_points"] == b["comparison_points"], (member, lv)
            pts = np.array(a["comparison_points"])
            d = np.abs(np.array(a["rule"]["c"]) - np.array(b["rule"]["c"]))
            row.append((float(d[pts <= 20].max()), float(d.max())))
        lines.append(f"| {label(member)} | " + " | ".join(fmt(r[0]) for r in row) + " | " + " | ".join(fmt(r[1]) for r in row) + " |")
    lines += ["", f"## The largest difference between the MPCs at the common points", "",
              "| member | " + " | ".join(f"level {lv}" for lv in levels) + " |", "|---|" + "---|" * len(levels)]
    for member in MEMBERS:
        cells = []
        for lv in levels:
            a, b = A[(member, lv)], B[(member, lv)]
            cells.append(fmt(float(np.max(np.abs(np.array(a["rule"]["mpc"]) - np.array(b["rule"]["mpc"]))))))
        lines.append(f"| {label(member)} | " + " | ".join(cells) + " |")
    top = levels[-1]
    ka, kb = A[(RESTRAINED, top)]["kink"], B[(RESTRAINED, top)]["kink"]
    lines += ["", f"## The restrained rule's kink at level {top}", "",
              f"| | m | slope below | slope above |", "|---|---|---|---|",
              f"| {name_a} | {ka['m']:.6f} | {ka['slope_below']:.4f} | {ka['slope_above']:.4f} |",
              f"| {name_b} | {kb['m']:.6f} | {kb['slope_below']:.4f} | {kb['slope_above']:.4f} |", "",
              f"## The stationary population at level {top}", "",
              f"| member | mean MPC, {name_a} | mean MPC, {name_b} | mass at a = 0, {name_a} | mass at a = 0, {name_b} | "
              f"mean a, {name_a} | mean a, {name_b} |", "|---|---|---|---|---|---|---|"]
    for member in MEMBERS:
        pa, pb = A[(member, top)]["population"], B[(member, top)]["population"]
        lines.append(f"| {label(member)} | {pa['mean_mpc']:.5f} | {pb['mean_mpc']:.5f} | {pa['mass_at_constraint']:.5f} | "
                     f"{pb['mass_at_constraint']:.5f} | {pa['a']['gl']['1']:.5f} | {pb['a']['gl']['1']:.5f} |")
    lines += ["", "## Each toolkit's convergence to the restrained rule", "",
              "The largest gap between a natural rule and the restrained one, at the common points:", "",
              "| ℘ | " + " | ".join(f"{name_a}, level {lv} | {name_b}, level {lv}" for lv in levels) + " |",
              "|---|" + "---|" * (2 * len(levels))]
    gaps = {}
    for which, R in ((name_a, A), (name_b, B)):
        for lv in levels:
            base = np.array(R[(RESTRAINED, lv)]["rule"]["c"])
            gaps[(which, lv)] = [float(np.max(np.abs(base - np.array(R[(m, lv)]["rule"]["c"])))) for m in NATURAL]
    for i, member in enumerate(NATURAL):
        lines.append(f"| {P_ZERO[member]} | " + " | ".join(f"{gaps[(name_a, lv)][i]:.4f} | {gaps[(name_b, lv)][i]:.4f}" for lv in levels) + " |")
    for which in (name_a, name_b):
        g = gaps[(which, top)]
        lines.append("")
        lines.append(f"{which} at level {top}: the gap falls by {g[0] / g[1]:.3f} and {g[1] / g[2]:.3f} for each tenfold fall in ℘.")
    (out / "toolkits.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11, 4.4))
    colors = {"bst-p-zero-0.005": "#86b6ef", "bst-p-zero-0.0005": "#3987e5", "bst-p-zero-0.00005": "#184f95",
              RESTRAINED: "#0b0b0b"}
    for member in MEMBERS:
        for which, R, style in ((name_a, A, "-"), (name_b, B, "--")):
            t = R[(member, top)]
            m = np.concatenate([np.array(t["exported_rule"]["m"]), np.array(t["comparison_points"])])
            c = np.concatenate([np.array(t["exported_rule"]["c"]), np.array(t["rule"]["c"])])
            o = np.argsort(m, kind="stable"); m, c = m[o], c[o]
            keep = (m >= 0.6) & (m <= 1.4)
            ax.plot(m[keep], c[keep], style, color=colors[member], lw=1.6,
                    label=f"{label(member)}, {which}" if member in (RESTRAINED, NATURAL[0]) else None)
        a, b = A[(member, top)], B[(member, top)]
        pts = np.array(a["comparison_points"])
        d = np.abs(np.array(a["rule"]["c"]) - np.array(b["rule"]["c"]))
        bx.semilogy(pts, np.maximum(d, 1e-17), "o-", ms=3, color=colors[member], label=label(member))
    ax.set_xlabel("market resources m"); ax.set_ylabel("consumption c(m)")
    ax.set_title(f"Near the kink, level {top}: {name_a} solid, {name_b} dashed"); ax.legend(frameon=False, fontsize=8)
    bx.set_xscale("log"); bx.set_xlabel("market resources m"); bx.set_ylabel(f"|c_{name_a} − c_{name_b}|")
    bx.set_title(f"The difference at the common points, level {top}"); bx.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "toolkits.png", dpi=150)
    print(out / "toolkits.md")


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4]), Path(sys.argv[5]))
