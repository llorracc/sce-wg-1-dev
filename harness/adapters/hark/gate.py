"""The gate a version of HARK's adapter passes before it is published (README.md).

For one member at one precision level:
  1. the gap between the Markov solution's rule and HARK's standard consumer's on the same nodes, for every type, on a fine
     grid of m from just above the constraint in force to the top of the distribution grid;
  2. when a reference results file is given, the adapter's file against it, number by number: relative differences for
     numbers of size one or more, absolute ones below; the largest of each kind is reported, by top-level part;
  3. the checker's verification of the adapter's file (check.py --verify-results).

    python gate.py <member.yaml> --level 1 --out <dir> [--reference <results.json> --request <request.yaml>]
"""
import argparse
import json
import math
import pathlib
import subprocess
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import adapter  # noqa: E402


def rule_gaps(member_path, level):
    """For each type, the largest relative difference between the Markov rule and the standard consumer's rule, and between the
    two employment states' rules, on 4,000 points of m."""
    bst1, _ = adapter.load_checker(str(adapter.SCHEMAS))
    member = bst1.load_member(pathlib.Path(member_path))
    lev = adapter.LEVELS[level]
    nodes, P, PSI, XI, _ = adapter.shocks(member, lev["nodes"])
    out = []
    for t in member.types:
        beta = float(t["beta"])
        markov = adapter.solve_type(member, beta, nodes, lev)
        standard = adapter.solve_standard(member, beta, P, PSI, XI, lev).solution[0]
        lo = markov.solution[0].mNrmMin
        m = lo + np.geomspace(1e-6, lev["dist_top"] - lo, 4000)
        c_m = np.asarray(markov.solution[0].cFunc(m), float)
        c_s = np.asarray(standard.cFunc(m), float)
        sol = markov.agent.solution[0]
        c_u = np.asarray(sol.cFunc[1](m), float)
        out.append({"beta": beta, "markov_vs_standard": float(np.max(np.abs(c_m - c_s) / c_s)),
                    "employed_vs_unemployed": float(np.max(np.abs(c_m - c_u) / c_m)),
                    "lower_limits": [float(lo), float(standard.mNrmMin)]})
    return out


def leaves(x, path=""):
    """Every number in a results file, by its path; strings and nulls are skipped."""
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, f"{path}/{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, f"{path}[{i}]")
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        yield path, float(x)


def compare(new_path, reference_path):
    """The largest relative difference (numbers of size one or more) and absolute difference (smaller numbers) between two
    results files, by top-level part and, within `types`, by the part of a type's record; the paths only one file has."""
    new, ref = dict(leaves(json.load(open(new_path)))), dict(leaves(json.load(open(reference_path))))
    skip = ("/toolkit", "/provenance", "_sha256")
    worst = {}
    for p in sorted(set(new) & set(ref)):
        if any(s in p for s in skip):
            continue
        a, b = new[p], ref[p]
        size = max(abs(a), abs(b))
        kind, d = ("relative", abs(a - b) / size) if size >= 1 else ("absolute", abs(a - b))
        parts = p.split("/")
        key = parts[1] if parts[1] != "types[0]" and not parts[1].startswith("types[") else "types/" + parts[2].split("[")[0]
        best = worst.get((key, kind))
        if best is None or d > best[0]:
            worst[(key, kind)] = (d, p, a, b)
    only = {"new": sorted(p for p in set(new) - set(ref) if not any(s in p for s in skip))[:12],
            "reference": sorted(p for p in set(ref) - set(new) if not any(s in p for s in skip))[:12]}
    return {f"{k} ({kind})": v for (k, kind), v in sorted(worst.items())}, only


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("member")
    ap.add_argument("--level", type=int, default=1)
    ap.add_argument("--out", required=True)
    ap.add_argument("--reference", default=None)
    ap.add_argument("--request", default=None)
    args = ap.parse_args()
    print("rule gaps, by type:", flush=True)
    for g in rule_gaps(args.member, args.level):
        print(f"  beta {g['beta']}: Markov vs standard {g['markov_vs_standard']:.2e}, employed vs unemployed "
              f"{g['employed_vs_unemployed']:.2e}, lower limits {g['lower_limits']}", flush=True)
    argv = [args.member, "--out", args.out, "--level", str(args.level)] + (["--request", args.request] if args.request else [])
    results = adapter.main(argv)
    check = subprocess.run([sys.executable, str(adapter.SCHEMAS / "checker" / "check.py"), args.member, "--verify-results", results],
                           capture_output=True, text=True)
    print("checker:", (check.stdout.strip().splitlines() or [""])[-1], f"(exit {check.returncode})", flush=True)
    if args.reference:
        worst, only = compare(results, args.reference)
        print("against the reference, the largest differences:", flush=True)
        for k, (d, p, a, b) in worst.items():
            print(f"  {k}: {d:.2e} at {p} ({a!r} vs {b!r})", flush=True)
        print("only in the adapter's file:", only["new"], "\nonly in the reference:", only["reference"], flush=True)
    return check.returncode


if __name__ == "__main__":
    sys.exit(main())
