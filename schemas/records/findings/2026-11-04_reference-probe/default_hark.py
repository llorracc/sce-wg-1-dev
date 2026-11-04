"""HARK 0.17.2 at its default settings on one member: the member's horizon, constraint and laws; HARK's own grid (48 points
nested 3 times from 0.001 to 20), 7 equiprobable nodes a shock with each node its bin's conditional mean (the adapter's
construction of the member's law at HARK's count), linear interpolation, no value function, the solver's tolerance 1e-6.
A scratchpad probe (2026-11-04). Run in the harness's locked HARK environment:

    uv run --project harness/envs/hark --frozen python default_hark.py <member.yaml> --out <dir>
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import yaml

REPO = Path("/home/shared/github/llorracc/sce-wg-1-dev")
sys.path.insert(0, str(REPO / "schemas" / "checker"))
sys.path.insert(0, str(REPO / "harness" / "adapters"))
sys.path.insert(0, str(REPO / "harness" / "adapters" / "hark"))
import bst1  # noqa: E402
import common  # noqa: E402
import adapter as hark_adapter  # noqa: E402

DEFAULTS = dict(aXtraMin=0.001, aXtraMax=20.0, aXtraCount=48, aXtraNestFac=3, aXtraExtra=None, CubicBool=False,
                vFuncBool=False, tolerance=1e-6, nodes=7)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("member")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cubic", action="store_true", help="HARK's cubic instead of its default linear interpolation")
    args = ap.parse_args(argv)
    from HARK.ConsumptionSaving.ConsIndShockModel import IndShockConsumerType
    import HARK
    member = bst1.load_member(Path(args.member))
    name = Path(args.member).stem
    beta = float(member.types[0]["beta"])
    nodes, P, PSI, XI, nb = common.shocks(member, DEFAULTS["nodes"])
    p = dict(CRRA=member.rho, Rfree=[member.R], PermGroFac=[member.G], LivPrb=[member.L], DiscFac=beta,
             BoroCnstArt=hark_adapter.boro_cnst_art(member), cycles=0, T_cycle=1,
             vFuncBool=DEFAULTS["vFuncBool"], CubicBool=args.cubic or DEFAULTS["CubicBool"],
             PermShkStd=[0.1], TranShkStd=[0.1], PermShkCount=7, TranShkCount=7,
             UnempPrb=0.0, IncUnemp=0.0, UnempPrbRet=0.0, IncUnempRet=0.0, T_retire=0, T_age=None, AgentCount=1,
             tolerance=DEFAULTS["tolerance"], aXtraMin=DEFAULTS["aXtraMin"], aXtraMax=DEFAULTS["aXtraMax"],
             aXtraCount=DEFAULTS["aXtraCount"], aXtraNestFac=DEFAULTS["aXtraNestFac"], aXtraExtra=[None])
    agent = IndShockConsumerType(**p, verbose=False)
    agent.IncShkDstn = [hark_adapter._labeled(P, PSI, XI, "income", hark_adapter.shock_bounds(member)["joint"])]
    agent.solve()
    d = agent.IncShkDstn[0]
    assert np.array_equal(np.asarray(d.pmv), P) and np.array_equal(np.asarray(d.atoms[1]), XI), "HARK rebuilt the income process"
    sol = agent.solution[0]
    req = REPO / "schemas" / "bst" / "experiments" / "restrained-limit" / f"{name}.request.yaml"
    pts = np.asarray([float(x) for x in yaml.safe_load(open(req))["types"][0]["points"]])
    cf = sol.cFunc
    a_lo = float(sol.mNrmMin)
    kink = None
    if not member.natural:
        kink, _ = common.kink_point(cf, member, beta, float(member.a_art), P, PSI, XI)
    r, r_max = common.euler_residuals(cf, member, beta, float(member.a_art), pts.tolist(), kink["m"] if kink else None,
                                      m_floor=a_lo)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    result = {"member": name, "toolkit": "HARK", "version": HARK.__version__, "settings": dict(DEFAULTS, cubic=bool(args.cubic)),
              "mNrmMin": a_lo, "completed_cycles": int(getattr(agent, "completed_cycles", -1)),
              "solution_distance": float(getattr(agent, "solution_distance", float("nan"))),
              "request_points": pts.tolist(), "c": np.asarray(cf(pts), float).tolist(),
              "mpc": np.asarray(cf.derivative(pts), float).tolist(), "kink": kink,
              "euler_stated": {"r": r, "max_abs": r_max}}
    (out / "result.json").write_text(json.dumps(result, indent=1))
    print(f"{name}: cycles {result['completed_cycles']}, distance {result['solution_distance']:.2e}, max |r| {r_max:.2e}, "
          f"kink {kink and kink['m']}")


if __name__ == "__main__":
    main()
