"""The ergodic distribution of one member under a reference rule, on a dense grid to the 99.9th percentile of wealth: a
scratchpad probe (2026-11-04). Two passes: the bench's geometric grid gives the percentile; the dense grid is built to it,
uniform in a, with a geometric continuation to a top beyond which the mass is below round-off. The transition is the
bench's lottery over equiprobable nodes of the laws, at a node count given on the command line, so that the dependence on
the nodes can be measured by doubling them.

    uv run --with numpy --with scipy --with jsonschema --with pyyaml --with referencing python reference_dist.py \
        <member.yaml> <run dir with rule.npz> --out <dir> --dense 32000 --coarse 400 --top 300 --nodes 31
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = Path("/home/shared/github/llorracc/sce-wg-1-dev")
sys.path.insert(0, str(REPO / "schemas" / "checker"))
sys.path.insert(0, str(REPO / "harness" / "adapters"))
sys.path.insert(0, str(HERE))
import bst1  # noqa: E402
import common  # noqa: E402
from reference_probe import LEVEL3, Rule  # noqa: E402


def load_rule(run_dir):
    z = np.load(Path(run_dir) / "rule.npz")
    m, c, k, a_lo, kinked = z["m"], z["c"], z["k"], float(z["a_lo"]), bool(z["kinked"])
    return Rule(m, c, k, a_lo, True, None) if kinked else Rule(m[1:], c[1:], k[1:], a_lo, False, float(k[0]))


def blocks(pop, mean_defined=True):
    c, a, mpc, at_floor = pop.derived()
    return common.population_block(pop.m, pop.w, c, a, mpc, at_floor, mean_defined)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("member")
    ap.add_argument("run")
    ap.add_argument("--out", required=True)
    ap.add_argument("--dense", type=int, default=32000)
    ap.add_argument("--coarse", type=int, default=400)
    ap.add_argument("--top", type=float, default=300.0)
    ap.add_argument("--nodes", type=int, default=31)
    ap.add_argument("--pass1-points", type=int, default=4000)
    ap.add_argument("--pass1-top", type=float, default=60.0)
    args = ap.parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    common.QUANTILE_PROBS = common.schema_quantile_probabilities(str(REPO / "schemas"))
    member = bst1.load_member(Path(args.member))
    name = Path(args.member).stem
    cf = load_rule(args.run)
    a_lo = float(member.a_art)
    natural = member.natural
    R, G, L = member.R, member.G, member.L
    nodes, P, PSI, XI, nb = common.shocks(member, args.nodes)
    t0 = time.time()
    # pass 1: the bench's geometric grid, as level 1 has it
    g1 = common.make_agrid(args.pass1_points, args.pass1_top, a_lo, natural)
    pop1 = common.Population(cf, g1, P, PSI, XI, R, G, a_lo, L, nb[0], nb[1], False)
    b1 = blocks(pop1)
    a999 = b1["a"]["quantiles"]["0.999"]
    m999 = b1["m"]["quantiles"]["0.999"]
    print(f"{name}: pass 1 ({len(g1)} points to {args.pass1_top}, {args.nodes} nodes): a at 0.999 = {a999:.6f}, "
          f"m at 0.999 = {m999:.6f}, mean a {b1['a']['gl']['1']:.8f}, {time.time() - t0:.0f}s", flush=True)
    del pop1
    # pass 2: dense and uniform to the percentile, geometric beyond it
    h = (a999 - a_lo) / args.dense
    dense = a_lo + h * np.arange(0 if not natural else 1, args.dense + 1)
    coarse = a999 * np.geomspace(1.0, args.top / a999, args.coarse + 1)[1:]
    g2 = np.concatenate([dense, coarse])
    pop2 = common.Population(cf, g2, P, PSI, XI, R, G, a_lo, L, nb[0], nb[1], False)
    b2 = blocks(pop2)
    mu = pop2.mu
    top_mass = float(mu[len(dense):].sum())
    end_mass = float(mu[-1])
    stat = pop2.stationarity_residual()
    print(f"{name}: pass 2 ({len(dense)} dense to {a999:.4f}, spacing {h:.2e}; {len(coarse)} coarse to {args.top}): "
          f"a at 0.999 = {b2['a']['quantiles']['0.999']:.6f}, mean a {b2['a']['gl']['1']:.8f}, mass beyond the dense part "
          f"{top_mass:.3e}, on the last node {end_mass:.3e}, stationarity {stat:.1e}, {time.time() - t0:.0f}s", flush=True)
    # the committed level-3 population block, for the distance
    comp = {}
    for tk, root in LEVEL3.items():
        f = root / name / "level-3" / "results.json"
        if f.is_file():
            comp[tk] = json.loads(f.read_text())["types"][0]["population"]
    result = {"member": name, "rule_run": str(args.run), "nodes_per_shock": args.nodes,
              "pass1": {"points": len(g1), "top": args.pass1_top, "a_999": a999, "m_999": m999, "block": b1},
              "pass2": {"dense_points": len(dense), "spacing": h, "dense_top": a999, "coarse_points": len(coarse),
                        "top": args.top, "mass_beyond_dense": top_mass, "mass_on_last_node": end_mass,
                        "stationarity_residual": stat, "block": b2},
              "level3": comp}
    (out / "result.json").write_text(json.dumps(result, indent=1))
    np.save(out / "mu.npy", mu)
    np.save(out / "agrid.npy", g2)


if __name__ == "__main__":
    main()
