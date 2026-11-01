"""Compare a toolkit's results files for the restrained-limit suite (../../model.md, "The restrained-limit suite"):
the natural members' consumption rules against the restrained consumer's, at the suite's common points.

    uv run --with matplotlib --with numpy python compare.py RUN_DIR OUT_DIR

RUN_DIR holds one folder per member, named as the members are, each with one folder per precision level, `level-<n>`,
holding the toolkit's `results.json`. OUT_DIR receives `comparison.md`, the tables, and `convergence.png`, the figure.
The comparison needs no solution of its own: everything comes from the results files.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

NATURAL = ["bst-p-zero-0.005", "bst-p-zero-0.0005", "bst-p-zero-0.00005"]
P_ZERO = {"bst-p-zero-0.005": 0.005, "bst-p-zero-0.0005": 0.0005, "bst-p-zero-0.00005": 0.00005}
RESTRAINED = "bst-restrained"


def load(run: Path) -> dict:
    out = {}
    for member in NATURAL + [RESTRAINED]:
        for level_dir in sorted((run / member).glob("level-*")):
            f = level_dir / "results.json"
            if f.is_file():
                out[(member, int(level_dir.name.split("-")[1]))] = json.loads(f.read_text())
    return out


def gaps(results: dict, level: int) -> dict:
    """At one level: each natural rule's gap to the restrained rule at the common points, and the population's numbers."""
    base = results[(RESTRAINED, level)]["types"][0]
    m = np.array(base["comparison_points"], float)
    c_r = np.array(base["rule"]["c"], float)
    rows = {}
    for member in NATURAL:
        t = results[(member, level)]["types"][0]
        assert t["comparison_points"] == base["comparison_points"], f"{member} level {level}: not the suite's points"
        c = np.array(t["rule"]["c"], float)
        g = c_r - c
        rows[member] = {"max_gap": float(np.max(np.abs(g))), "at": float(m[int(np.argmax(np.abs(g)))]),
                        "gap": g, "c": c, "mpc": np.array(t["rule"]["mpc"], float), "population": t["population"]}
    rows[RESTRAINED] = {"c": c_r, "mpc": np.array(base["rule"]["mpc"], float), "population": base["population"],
                        "kink": base.get("kink")}
    return {"m": m, "rows": rows}


def fmt(x: float) -> str:
    return f"{x:.4g}"


def main(run: Path, out: Path) -> None:
    results = load(run)
    levels = sorted({lv for (_, lv) in results if all((mem, lv) in results for mem in NATURAL + [RESTRAINED])})
    out.mkdir(parents=True, exist_ok=True)
    lines = ["# The restrained-limit suite: the comparison", "",
             f"From the results files in `{run.name}`, levels {', '.join(map(str, levels))}. The gap is the restrained "
             "rule's consumption less the natural member's, at the suite's common points in m.", "",
             "![The rules at the top level, and the largest gap against ℘ at every level](convergence.png)", ""]
    table = {lv: gaps(results, lv) for lv in levels}
    lines += ["## The largest gap to the restrained rule", "",
              "| ℘ | " + " | ".join(f"level {lv}" for lv in levels) + " | where, at the top level |",
              "|---|" + "---|" * len(levels) + "---|"]
    for member in NATURAL:
        cells = [fmt(table[lv]["rows"][member]["max_gap"]) for lv in levels]
        lines.append(f"| {P_ZERO[member]:.5f}".rstrip("0") + " | " + " | ".join(cells) + f" | m = {fmt(table[levels[-1]]['rows'][member]['at'])} |")
    top = table[levels[-1]]
    ratios = [top["rows"][a]["max_gap"] / top["rows"][b]["max_gap"] for a, b in zip(NATURAL, NATURAL[1:])]
    lines += ["", f"At the top level the gap falls by a factor of {' and '.join(fmt(r) for r in ratios)} for each tenfold "
              "fall in ℘.", ""]
    lines += ["## The rules at the top level", "",
              "| m | restrained c | " + " | ".join(f"c, ℘ = {P_ZERO[mem]:.5f}".rstrip("0") for mem in NATURAL)
              + " | restrained MPC | " + " | ".join(f"MPC, ℘ = {P_ZERO[mem]:.5f}".rstrip("0") for mem in NATURAL) + " |",
              "|---|" + "---|" * (2 + 2 * len(NATURAL))]
    for j, mj in enumerate(top["m"]):
        r = top["rows"]
        lines.append(f"| {fmt(mj)} | {fmt(r[RESTRAINED]['c'][j])} | "
                     + " | ".join(fmt(r[mem]["c"][j]) for mem in NATURAL)
                     + f" | {fmt(r[RESTRAINED]['mpc'][j])} | " + " | ".join(fmt(r[mem]["mpc"][j]) for mem in NATURAL) + " |")
    lines += ["", "## The stationary population at the top level", "",
              "| member | mass at the constraint | fraction with a ≤ 0 | mean MPC | share of a held by the bottom 10% |",
              "|---|---|---|---|---|"]
    for member in NATURAL + [RESTRAINED]:
        pop = top["rows"][member]["population"]
        gl = pop["a"]["gl"]
        bottom = gl.get("0.1") / gl.get("1") if gl.get("0.1") is not None and gl.get("1") else float("nan")
        lines.append(f"| `{member}` | {fmt(pop['mass_at_constraint'])} | {fmt(pop['fraction_a_nonpositive'])} | "
                     f"{fmt(pop['mean_mpc'])} | {fmt(bottom)} |")
    (out / "comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11, 4.4))
    for member, style in zip(NATURAL + [RESTRAINED], ["-", "--", ":", "-"]):
        t0 = results[(member, levels[-1])]["types"][0]
        er = t0["exported_rule"]
        # the dense points cover the population's own range, which for the restrained consumer starts at its lowest income;
        # the suite's common points run down to m = 0.01, so the two together show every rule from there
        m = np.concatenate([np.array(er["m"], float), np.array(t0["comparison_points"], float)])
        c = np.concatenate([np.array(er["c"], float), np.array(t0["rule"]["c"], float)])
        order = np.argsort(m, kind="stable")      # a toolkit's dense points need not come in order (the kink is added)
        m, c = m[order], c[order]
        keep = m <= 3.0
        label = f"natural, ℘ = {P_ZERO[member]:.5f}".rstrip("0") if member in P_ZERO else "restrained: ℘ = 0, a ≥ 0"
        ax.plot(m[keep], c[keep], style, color="black" if member == RESTRAINED else None, lw=1.6, label=label)
    ax.plot([0, 3], [0, 3], color="0.75", lw=0.8)
    ax.set_xlabel("market resources m"); ax.set_ylabel("consumption c(m)")
    ax.set_title(f"The rules, level {levels[-1]}"); ax.legend(frameon=False, fontsize=8)
    for lv in levels:
        bx.loglog([P_ZERO[mem] for mem in NATURAL], [table[lv]["rows"][mem]["max_gap"] for mem in NATURAL], "o-",
                  label=f"level {lv}")
    bx.set_xlabel("probability of the zero-income event ℘"); bx.set_ylabel("largest gap to the restrained rule")
    bx.set_title("Convergence as ℘ falls"); bx.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "convergence.png", dpi=150)
    print(out / "comparison.md")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
