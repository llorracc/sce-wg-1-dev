"""Write the restrained-limit suite's request files: one per member, all with the same comparison points in m, so that the
four members' rules can be read side by side (../../model.md, "The restrained-limit suite").

    uv run --with jsonschema --with pyyaml --with scipy --with referencing python make_requests.py

The points run from just above 0 to 50 in market resources, dense around the restrained rule's kink near m = 0.98, each to
three significant figures as the results schema's comparison points are.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent.parent / "checker"))
import bst1  # noqa: E402

MEMBERS = {"bst-p-zero-0.005": "natural", "bst-p-zero-0.0005": "natural", "bst-p-zero-0.00005": "natural",
           "bst-restrained": "artificial"}
POINTS = [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.92, 0.94, 0.95, 0.96, 0.97, 0.975,
          0.98, 0.985, 0.99, 1.0, 1.02, 1.05, 1.1, 1.2, 1.3, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0, 20.0, 50.0]
RULE = ("the restrained-limit suite's common points: m from 0.01 to 50, dense around the restrained rule's kink near "
        "m = 0.98, the same for every member of the suite; three significant figures")


def main() -> None:
    assert POINTS == sorted(set(POINTS)) and all(p == float(f"{p:.3g}") for p in POINTS)
    for name, scenario in MEMBERS.items():
        member = bst1.load_member(HERE.parent.parent / scenario / "members" / f"{name}.yaml")
        request = {"family": member.family, "parameter_file_sha256": member.hash, "rule": RULE,
                   "types": [{"beta": t["beta"], "points": POINTS} for t in member.types]}
        (HERE / f"{name}.request.yaml").write_text(
            yaml.safe_dump(request, sort_keys=False, default_flow_style=None, width=120, allow_unicode=True),
            encoding="utf-8")
        print(name, member.hash[:12])


if __name__ == "__main__":
    main()
