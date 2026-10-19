"""Check a bst/1 parameter file: validate it, hash it, and report its conditions, domain rules and implications; or verify a
results file against it.

    uv run --with jsonschema --with pyyaml --with scipy python check.py ../bst-1/members/toy.yaml [--json out.json]
    uv run --with jsonschema --with pyyaml --with scipy python check.py ../bst-1/members/toy.yaml --verify-results r.json

Exit status 0 when the file is a valid member whose every type passes the validity conditions (and, with
--verify-results, when the results file validates and its report is consistent), 1 otherwise. The report is the STATED
member's, the limit a toolkit's effective member approaches; a condition whose margin lies within the precision of the
closed forms is marked undecided.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from bst1 import MemberError, load_member, validate_results
from canonical import StrictYAMLError


def _fmt(x) -> str:
    if x is None:
        return "none"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, float):
        return "inf" if math.isinf(x) else ("-inf" if x == -math.inf else f"{x:.6g}")
    return str(x)


def print_report(report: dict) -> None:
    print(f"family   {report['family']}")
    print(f"hash     {report['hash']}")
    print(f"member   {report['member']} (the limit a toolkit's effective member approaches)")
    print(f"valid    {_fmt(report['valid'])}")
    for name, s in report["shocks"].items():
        print(f"{name}: {s['law']}  mean {_fmt(s['mean'])}  E[1/x] {_fmt(s['E_inverse'])}  "
              f"E[log x] {_fmt(s['E_log'])}  E[x log x] {_fmt(s['E_x_log_x'])}  "
              f"support [{_fmt(s['infimum'])}, {_fmt(s['supremum'])}]  mass at infimum {_fmt(s['mass_at_infimum'])}")
    print("implications: " + ", ".join(f"{k} {_fmt(v)}" for k, v in report["implications"].items()))
    for t in report["types"]:
        print(f"\ntype beta {t['beta']}  share {_fmt(t['share'])}  thorn {_fmt(t['thorn'])}  valid {_fmt(t['valid'])}")
        for c in t["conditions"]:
            print(f"  {c['name']:<15} {_fmt(c['factor']):>12} < {_fmt(c['bound']):<10} {c['verdict']:<9} "
                  f"margin {_fmt(c['margin'])}")
        r = t["rate_condition"]
        print(f"  rate condition  (R/G)(thorn/G) {_fmt(r['value'])} against E[psi^2] {_fmt(r['E_psi_squared'])}")
        w = t["welfare"]
        print(f"  welfare: finite {_fmt(w['welfare_finite'])} ({w['welfare_case']}, factor {_fmt(w['welfare_factor'])}); "
              f"marginal: finite {_fmt(w['marginal_finite'])} ({w['marginal_case']}, factor {_fmt(w['marginal_factor'])})")
        print("  implications: " + ", ".join(f"{k} {_fmt(v)}" for k, v in t["implications"].items()))
        print("  defined: " + ", ".join(f"{k} {_fmt(v)}" for k, v in t["domain"].items()))
    print("\npooled: " + ", ".join(f"{k} {_fmt(v)}" for k, v in report["pooled_domain"].items()))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("member", type=Path)
    parser.add_argument("--json", type=Path, help="write the full report as JSON to this file")
    parser.add_argument("--bellman-calibration", type=int, metavar="TYPE",
                        help="print the Bellman calibration of this type (0-based) instead of the report")
    parser.add_argument("--verify-results", type=Path, metavar="RESULTS",
                        help="validate this results file and verify its report against the member, instead of the report")
    args = parser.parse_args(argv)
    try:
        member = load_member(args.member)
    except (StrictYAMLError, MemberError) as error:
        print(f"{args.member}: not a valid bst/1 member\n  {error}", file=sys.stderr)
        return 1
    if args.verify_results is not None:
        results = json.loads(args.verify_results.read_text())
        problems = validate_results(results)
        if not problems:
            problems = member.verify_results(results)
        if problems:
            print(f"{args.verify_results}: {len(problems)} problem(s)")
            for p in problems:
                print(f"  {p}")
            return 1
        print(f"{args.verify_results}: validates, and its report is consistent with the member {member.hash[:12]}…")
        return 0
    if args.bellman_calibration is not None:
        try:
            print(member.bellman_calibration_yaml(args.bellman_calibration), end="")
        except (ValueError, IndexError) as error:
            print(f"{args.member}: no Bellman calibration\n  {error}", file=sys.stderr)
            return 1
        return 0
    report = member.report()
    print_report(report)
    if args.json:
        args.json.write_text(json.dumps(report, indent=2, allow_nan=True))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
