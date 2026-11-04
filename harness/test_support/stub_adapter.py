"""A stand-in toolkit for the harness's tests (../test_runner.py). It takes an adapter's command line and copies the
results, method and settings files of HARK's committed run of the restrained-limit experiment for the member and level
it is given, solving nothing, and adds a stand-in for the distribution function at the comparison points, which those
files predate (results.md, 2026-11-04). STUB_FAIL names a member to fail on; STUB_DROP names a key to remove from every
type of the results file."""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path.cwd()  # the runner runs every adapter from the repository's root; the tests copy this file elsewhere
RUN = ROOT / "schemas" / "records" / "findings" / "2026-11-01_restrained-limit-suite-hark" / "results"

ap = argparse.ArgumentParser()
ap.add_argument("member")
ap.add_argument("--out", required=True)
ap.add_argument("--level", required=True)
ap.add_argument("--request", required=True)
a = ap.parse_args()
member = Path(a.member).stem
if os.environ.get("STUB_FAIL") == member:
    print("stub: failing as asked", file=sys.stderr)
    sys.exit(3)
src, out = RUN / member / f"level-{a.level}", Path(a.out)
out.mkdir(parents=True, exist_ok=True)
for name in ("methods.yaml", "settings.yaml", "results.json"):
    shutil.copyfile(src / name, out / name)
results = json.loads((out / "results.json").read_text(encoding="utf-8"))
for t in results["types"]:
    n = len(t["comparison_points"])
    stand_in = [(i + 1) / n for i in range(n)]
    t["population"]["m"]["cdf"] = list(stand_in)            # m's alone: the files' requests give a no points of its own
    if t["income_measure"]["status"] == "value":
        t["income_measure"]["m"]["cdf"] = list(stand_in)
    if os.environ.get("STUB_DROP"):
        t.pop(os.environ["STUB_DROP"], None)
(out / "results.json").write_text(json.dumps(results), encoding="utf-8")
print(f"stub: {member} level {a.level}")
