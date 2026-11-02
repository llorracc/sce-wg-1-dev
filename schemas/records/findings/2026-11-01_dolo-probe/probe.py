"""Feasibility probe: BST's normalized household as a dolo model, solved by dolo's egm on the schemas' own nodes, compared
with HARK's level-1 results at the restrained-limit suite's common points."""
import contextlib, io, json, sys
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[3]   # schemas/
sys.path[:0] = [str(REPO / "checker"), str(REPO / "adapters" / "hark")]
import bst1, adapter as hark_adapter
from dolo import yaml_import
from dolo.algos.egm import egm
from dolo.numeric.distribution import FiniteDistribution

MODEL = """symbols:
    exogenous: [psi, xi]
    states: [m]
    poststates: [a]
    controls: [c]
    expectations: [mr]
    parameters: [beta, L, rho, R, G, a_min, cbar]
equations:
    transition:
        - m[t] = (m[t-1]-c[t-1])*R/(G*psi[t]) + xi[t]
    arbitrage:
        - beta*L*R*((G*psi[t+1]*c[t+1])/c[t])^(-rho) - 1 | 0.0 <= c[t] <= m[t] - a_min
    half_transition: |
        m[t] = a[t-1]*R/(G*psi[t]) + xi[t]
    reverse_state: |
        m[t] = a[t] + c[t]
    expectation: |
        mr[t] = beta*L*R*(G*psi[t+1]*c[t+1]/cbar)^(-rho)
    direct_response_egm: |
        c[t] = cbar*(mr[t])^(-1/rho)
calibration:
    beta: {beta}
    L: {L}
    rho: {rho}
    R: {R}
    G: {G}
    a_min: {a_min}
    cbar: 1.0
    m: 1.5
    c: 1.0
    a: 0.5
    psi: 1.0
    xi: 1.0
domain:
    m: [{m_lo}, {m_hi}]
exogenous: !Normal
    Σ: [[0.01, 0.0], [0.0, 0.01]]
options:
    grid: !Cartesian
        orders: [{n_m}]
"""

def solve(member_path, n_nodes=7, n_a=300, a_top=100.0, m_hi=50.0, n_m=10001, tol=1e-10):
    member = bst1.load_member(member_path)
    t = member.types[0]
    natural = member.family.startswith("bst-natural")
    a_min = 0.0 if natural else float(member.a_art)
    text = MODEL.format(beta=t["beta"], L=member.L, rho=member.rho, R=member.R, G=member.G, a_min=a_min,
                        m_lo=0.0, m_hi=m_hi, n_m=n_m)
    import tempfile
    path = Path(tempfile.mkdtemp()) / "probe_model.yaml"; path.write_text(text, encoding="utf-8")
    model = yaml_import(str(path))
    _, P, PSI, XI, _ = hark_adapter.shocks(member, n_nodes)
    dp = FiniteDistribution(np.column_stack([PSI, XI]), P)
    grid, _ = model.discretize()
    # the savings grid above a_min; a_min itself only where the constraint can bind
    xtra = np.geomspace(1e-6, a_top, n_a)
    a_grid = a_min + (np.concatenate([[0.0], xtra]) if not natural else xtra)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        sol = egm(model, grid=grid, dp=dp, a_grid=a_grid, η_tol=tol, maxit=5000)
    return member, sol

def compare(name, scenario):
    member, sol = solve(REPO / "bst" / scenario / "members" / f"{name}.yaml")
    hark = json.loads((REPO / "records/findings/2026-11-01_restrained-limit-suite-hark/results" / name / "level-1/results.json").read_text())["types"][0]
    pts = np.array(hark["comparison_points"]); c_h = np.array(hark["rule"]["c"])
    c_d = sol.dr(pts[:, None]).ravel()
    d = np.abs(c_d - c_h)
    print(f"{name}: converged {sol.a_converged} after {sol.iterations} iterations (err {sol.err:.1e}); "
          f"largest |c_dolo - c_HARK| {d.max():.2e} at m = {pts[d.argmax()]}; at m=0.975: dolo {c_d[pts==0.975][0]:.6f} HARK {c_h[pts==0.975][0]:.6f}")
    return pts, c_d, c_h

for name, scen in (("bst-restrained", "artificial"), ("bst-p-zero-0.005", "natural")):
    compare(name, scen)
