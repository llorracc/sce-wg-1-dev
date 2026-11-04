"""The bench's continuous EGM: a reference solve of one buffer-stock member by the kink-split continuous expectation and a
cubic Hermite carrying the EGM slopes. A scratchpad probe (2026-11-04); nothing here is committed.

    uv run --with numpy --with scipy --with jsonschema --with pyyaml --with referencing python reference_probe.py \
        <member.yaml> --out <dir> [--points 1000 --top 200 --nest 3 --nodes 32 --tol 1e-11 --max-iter 5000]

The expectation: Gauss-Legendre in the log of each truncated lognormal law, the transitory law's support split at the
preimage of next period's kink (where there is one), the permanent law in one piece, the zero-income event exact; both
E[(G psi)^-rho u'(c(m'))] and its derivative in a from one evaluation of next period's rule and its slope. The rule: a cubic
Hermite through the endogenous points with the EGM slopes; below an artificial kink c = m - a_lo; at a natural limit the
segment from (a_lo, 0) with the closed-form MPC; above the last point, linear with the last slope. The loop stops when the
last step times lambda / (1 - lambda), lambda the measured contraction factor, is below the tolerance.
"""
import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import CubicHermiteSpline, PchipInterpolator

REPO = Path("/home/shared/github/llorracc/sce-wg-1-dev")
sys.path.insert(0, str(REPO / "schemas" / "checker"))
sys.path.insert(0, str(REPO / "harness" / "adapters"))
import bst1  # noqa: E402
import common  # noqa: E402

FINDINGS = REPO / "schemas" / "records" / "findings"
LEVEL3 = {"HARK": FINDINGS / "2026-11-01_restrained-limit-suite-hark" / "results",
          "dolo": FINDINGS / "2026-11-01_restrained-limit-suite-dolo" / "results"}


def nested_grid(lo, hi, n, nest):
    """HARK's make_grid_exp_mult: n points from lo to hi, nested `nest` times in the exponential."""
    a, b = lo, hi
    for _ in range(nest):
        a, b = math.log(a + 1.0), math.log(b + 1.0)
    g = np.linspace(a, b, n)
    for _ in range(nest):
        g = np.exp(g) - 1.0
    g[0], g[-1] = lo, hi
    return g


class Rule:
    """c(m) and its slope from the endogenous points (m, c, kappa)."""

    def __init__(self, m, c, k, a_lo, kinked, kappa_lo):
        m, c, k = (np.asarray(x, float) for x in (m, c, k))
        if not kinked:
            m, c, k = np.r_[a_lo, m], np.r_[0.0, c], np.r_[kappa_lo, k]
        assert np.all(np.diff(m) > 0), "the endogenous points are not increasing"
        self.a_lo, self.kinked = float(a_lo), kinked
        self.spl = CubicHermiteSpline(m, c, k, extrapolate=False)
        self.dspl = self.spl.derivative()
        self.m0, self.m_top, self.c_top, self.k_top = float(m[0]), float(m[-1]), float(c[-1]), float(k[-1])
        self.pts = (m, c, k)

    @property
    def kink(self):
        return self.m0 if self.kinked else None

    def __call__(self, m):
        m = np.asarray(m, float)
        out = self.spl(m)
        low = np.maximum(m - self.a_lo, 0.0) if self.kinked else np.zeros_like(m)
        out = np.where(m < self.m0, low, out)
        out = np.where(m > self.m_top, self.c_top + self.k_top * (m - self.m_top), out)
        return out

    def derivative(self, m):
        m = np.asarray(m, float)
        out = self.dspl(m)
        out = np.where(m < self.m0, 1.0 if self.kinked else 0.0, out)
        out = np.where(m > self.m_top, self.k_top, out)
        return out


class StartRule:
    """A start for the loop: PCHIP through a committed exported rule, linear outside it."""

    def __init__(self, m, c, a_lo, kinked):
        self.p = PchipInterpolator(m, c, extrapolate=False)
        self.d = self.p.derivative()
        self.m0, self.m_top, self.c_top = float(m[0]), float(m[-1]), float(c[-1])
        self.k0, self.k_top = float(self.d(m[0])), float(self.d(m[-1]))
        self.c0 = float(c[0])
        self.a_lo, self.kinked = a_lo, kinked

    def __call__(self, m):
        m = np.asarray(m, float)
        out = self.p(m)
        out = np.where(m < self.m0, np.maximum(self.c0 + self.k0 * (m - self.m0), 0.0), out)
        return np.where(m > self.m_top, self.c_top + self.k_top * (m - self.m_top), out)

    def derivative(self, m):
        m = np.asarray(m, float)
        out = self.d(m)
        out = np.where(m < self.m0, self.k0, out)
        return np.where(m > self.m_top, self.k_top, out)


class Expectation:
    """E1(a) = E[(G psi)^-rho u'(c(m'))] and E2(a) = dE1/da at an array of end-of-period assets, against the continuous laws."""

    def __init__(self, member, n):
        self.member = member
        self.R, self.G, self.rho = member.R, member.G, member.rho
        self.wp, self.xi_u = float(member.wp), float(member.xi_u)
        self.scale = common.employed_scale(member)
        self.w_psi, self.psi = common.law_quadrature(member.psi, n)
        th = member.theta.normal
        self.loc, self.s, self.bot, self.top, self.mass = th.location, th.scale, th.bot, th.top, th.mass
        self.gx, self.gw = leggauss(n)
        self.n = n

    def _piece(self, lo, hi):
        """Nodes and weights of one piece [lo, hi] in z, lo and hi arrays of one shape; returns shape + (n,)."""
        h = (hi - lo)[..., None]
        z = lo[..., None] + h * (self.gx + 1.0) / 2.0
        w = h / 2.0 * self.gw * np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi) / self.mass
        return z, w

    def theta_nodes(self, base, m_kink):
        if m_kink is None:
            lo = np.full(base.shape, self.bot)
            hi = np.full(base.shape, self.top)
            return self._piece(lo, hi)
        th_star = (m_kink - base) / self.scale
        with np.errstate(divide="ignore", invalid="ignore"):
            z_star = np.where(th_star > 0, (np.log(np.maximum(th_star, 1e-300)) - self.loc) / self.s, self.bot)
        z_star = np.clip(z_star, self.bot, self.top)
        z1, w1 = self._piece(np.full(base.shape, self.bot), z_star)
        z2, w2 = self._piece(z_star, np.full(base.shape, self.top))
        return np.concatenate([z1, z2], -1), np.concatenate([w1, w2], -1)

    def __call__(self, cf, a, m_kink):
        rho = self.rho
        a = np.asarray(a, float)
        base = self.R * a[:, None] / (self.G * self.psi[None, :])          # (N_a, n_psi)
        z, w = self.theta_nodes(base, m_kink)                              # (N_a, n_psi, nodes)
        m_next = base[..., None] + self.scale * np.exp(self.loc + self.s * z)
        c_next = cf(m_next)
        k_next = cf.derivative(m_next)
        E1_emp = np.sum(w * c_next ** (-rho), axis=-1)
        E2_emp = np.sum(w * (-rho) * c_next ** (-rho - 1.0) * k_next, axis=-1)
        if self.wp > 0:
            m_u = base + self.xi_u
            c_u, k_u = cf(m_u), cf.derivative(m_u)
            E1_s = self.wp * c_u ** (-rho) + (1.0 - self.wp) * E1_emp
            E2_s = self.wp * (-rho) * c_u ** (-rho - 1.0) * k_u + (1.0 - self.wp) * E2_emp
        else:
            E1_s, E2_s = E1_emp, E2_emp
        fac = (self.G * self.psi) ** (-rho)
        dm_da = self.R / (self.G * self.psi)
        return np.sum(self.w_psi * fac * E1_s, axis=1), np.sum(self.w_psi * fac * dm_da * E2_s, axis=1)


def closed_forms(member, beta):
    E = member.expectations()
    thorn_R = (member.R * beta * member.L) ** (1.0 / member.rho) / member.R
    kappa_bar = 1.0 - (float(member.wp) ** (1.0 / member.rho)) * thorn_R if member.wp > 0 else 1.0
    return dict(thorn_R=thorn_R, mpc_limit_natural=kappa_bar, mpc_min=1.0 - thorn_R, expectations=E)


def start_from_level3(member_name, a_lo, kinked):
    f = LEVEL3["HARK"] / member_name / "level-3" / "results.json"
    if not f.is_file():
        return None
    t = json.loads(f.read_text())["types"][0]["exported_rule"]
    m, c = np.asarray(t["m"], float), np.asarray(t["c"], float)
    return StartRule(m, c, a_lo, kinked)


def solve(member, beta, args, log):
    a_lo = float(member.a_art)
    kinked = not member.natural
    cf_ = closed_forms(member, beta)
    grid = a_lo + nested_grid(1e-6, args.top - a_lo, args.points, args.nest)
    grid = np.r_[a_lo, grid] if kinked else np.r_[a_lo + np.array([1e-9, 1e-8, 1e-7]), grid]
    if args.extra_near_limit:
        # more points where the rule bends most, just above the constraint: geometric from 1e-7 to 2 above it
        grid = np.unique(np.r_[grid, a_lo + np.geomspace(1e-7, 2.0, args.extra_near_limit)])
    E = Expectation(member, args.nodes)
    fac = beta * member.L * member.R
    rho = member.rho
    cf = start_from_level3(args.member_name, a_lo, kinked) or StartRule(np.array([a_lo + 1e-6, args.top]),
                                                                        np.array([1e-6, 0.05 * args.top]), a_lo, kinked)
    check = np.r_[a_lo + np.geomspace(1e-6, args.top - a_lo, 3000), args.request]
    prev_step, lam, bound = None, None, None
    t0 = time.time()
    for it in range(1, args.max_iter + 1):
        m_kink = cf.kink if isinstance(cf, Rule) else (float(cf_["expectations"] and 0.0) if False else None)
        if kinked and not isinstance(cf, Rule):
            m_kink = None          # the start has no recorded kink; the first iteration integrates in one piece
        E1, E2 = E(cf, grid, m_kink)
        c = (fac * E1) ** (-1.0 / rho)
        dcda = -(1.0 / rho) * c ** (1.0 + rho) * fac * E2
        kappa = dcda / (1.0 + dcda)
        new = Rule(grid + c, c, kappa, a_lo, kinked, cf_["mpc_limit_natural"])
        step = float(np.max(np.abs(new(check) - cf(check))))
        if prev_step is not None and prev_step > 0:
            lam = step / prev_step
            bound = step * lam / (1.0 - lam) if lam < 1.0 else math.inf
        cf, prev_step = new, step
        if it % 25 == 0 or it <= 3:
            log(f"iteration {it}: step {step:.3e}, lambda {lam if lam is None else round(lam, 5)}, "
                f"bound {bound if bound is None else f'{bound:.3e}'}, kink {new.kink}, elapsed {time.time() - t0:.1f}s")
        if bound is not None and bound < args.tol and step < args.tol:
            log(f"converged at iteration {it}: step {step:.3e}, bound {bound:.3e}")
            break
    else:
        log(f"NOT converged after {args.max_iter} iterations: step {step:.3e}")
    return cf, dict(iterations=it, last_step=step, contraction=lam, distance_bound=bound), cf_


def diagnostics(cf, member, beta, a_lo, points, cf_, args):
    rho = member.rho
    pts = np.asarray(points, float)
    out = {"c": cf(pts).tolist(), "mpc": cf.derivative(pts).tolist()}
    r32, max32 = common.euler_residuals(cf, member, beta, a_lo, list(points), cf.kink, n=32, m_floor=a_lo)
    r64, max64 = common.euler_residuals(cf, member, beta, a_lo, list(points), cf.kink, n=64, m_floor=a_lo)
    out["euler_stated"] = {"max_abs_32": max32, "max_abs_64": max64,
                           "precision": float(max(abs(x - y) for x, y in zip(r32, r64))), "r_64": r64}
    if cf.kinked:
        out["kink"] = {"m": cf.kink, "slope_right": float(cf.derivative(np.array([cf.kink + 1e-9]))[0]),
                       "c_minus_m_below": float(cf(np.array([cf.kink - 1e-3]))[0] - (cf.kink - 1e-3 - a_lo))}
    else:
        eps = np.array([1e-9, 1e-8, 1e-7, 1e-6, 1e-5])
        sec = (cf(a_lo + eps) / eps).tolist()
        out["mpc_at_limit"] = {"closed_form": cf_["mpc_limit_natural"], "secants": dict(zip(map(str, eps), sec)),
                               "first_points_slope": cf.pts[2][1:4].tolist()}
    out["mpc_min"] = {"closed_form": cf_["mpc_min"], "slope_at_top": cf.k_top, "m_top": cf.m_top}
    # the committed level-3 rules at the request points
    comp = {}
    for tk, root in LEVEL3.items():
        f = root / args.member_name / "level-3" / "results.json"
        if f.is_file():
            t = json.loads(f.read_text())["types"][0]
            if [float(x) for x in t["comparison_points"]] == [float(x) for x in points]:
                c3 = np.asarray(t["rule"]["c"], float)
                d = np.abs(c3 - cf(pts))
                comp[tk] = {"max_abs": float(d.max()), "max_abs_m_le_20": float(d[pts <= 20].max()),
                            "max_rel": float(np.max(d / cf(pts))), "at_m": float(pts[int(np.argmax(d / cf(pts)))])}
    out["level3_distance"] = comp
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("member")
    ap.add_argument("--out", required=True)
    ap.add_argument("--points", type=int, default=1000)
    ap.add_argument("--top", type=float, default=200.0)
    ap.add_argument("--nest", type=int, default=3)
    ap.add_argument("--nodes", type=int, default=32, help="Gauss-Legendre nodes a piece, each shock")
    ap.add_argument("--tol", type=float, default=1e-11)
    ap.add_argument("--max-iter", type=int, default=5000)
    ap.add_argument("--extra-near-limit", type=int, default=0, help="extra geometric points from 1e-7 to 2 above the constraint")
    ap.add_argument("--request", default=None)
    args = ap.parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    logf = open(out / "log.txt", "a")

    def log(s):
        print(s, flush=True)
        logf.write(s + "\n")
        logf.flush()

    member = bst1.load_member(Path(args.member))
    args.member_name = Path(args.member).stem
    beta = float(member.types[0]["beta"])
    scen = "artificial" if not member.natural else "natural"
    req = args.request or (REPO / "schemas" / "bst" / "experiments" / "restrained-limit" / f"{args.member_name}.request.yaml")
    import yaml
    request = yaml.safe_load(open(req))
    args.request = np.asarray([float(x) for x in request["types"][0]["points"]])
    log(f"member {args.member_name} ({scen}), beta {beta}, settings points {args.points} top {args.top} nest {args.nest} "
        f"nodes {args.nodes} tol {args.tol}")
    cf, conv, cf_ = solve(member, beta, args, log)
    a_lo = float(member.a_art)
    diag = diagnostics(cf, member, beta, a_lo, args.request.tolist(), cf_, args)
    m, c, k = cf.pts
    np.savez(out / "rule.npz", m=m, c=c, k=k, a_lo=a_lo, kinked=cf.kinked)
    result = {"member": args.member_name, "beta": beta,
              "settings": {"points": args.points, "top": args.top, "nest": args.nest, "nodes_per_piece": args.nodes,
                           "tolerance": args.tol, "extra_near_limit": args.extra_near_limit, "grid_size": int(len(m))},
              "convergence": conv, "closed_forms": {k_: v for k_, v in cf_.items() if k_ != "expectations"},
              "request_points": args.request.tolist(), **diag}
    (out / "result.json").write_text(json.dumps(result, indent=1))
    log(f"max |r| under the stated laws: {diag['euler_stated']['max_abs_32']:.3e} (64 nodes: "
        f"{diag['euler_stated']['max_abs_64']:.3e}); level-3 distances: {diag['level3_distance']}")
    if cf.kinked:
        log(f"kink {diag['kink']}")
    else:
        log(f"MPC at the limit {diag['mpc_at_limit']}")
    log(f"limiting MPC {diag['mpc_min']}")


if __name__ == "__main__":
    main()
