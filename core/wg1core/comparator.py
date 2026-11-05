"""The comparator (../../schemas/experiments.md): the experiment's checks evaluated as written on a run's results
files, and every job's distance from its member's reference with the reference's own error beside it.

A check compares one quantity, a path into the results file, between members of one toolkit at one level, between
toolkits for one member at one level, or between successive levels of one toolkit for one member, the levels ordered
as the experiment lists them, under a metric and an expectation; its verdict is pass, fail, not applicable when the run
holds too little to apply it, or error when the files cannot be compared. The distance from the reference gets no
verdict: it is reported, with the reference's error, for every quantity the experiment names. A comparison that
cannot be computed for a member that pins a reference, the reference not loading, not answering the same question by
the identity keys the model names, or a quantity not comparable, is an error. The comparator's exit status is the
checks' and the errors', never a distance's.

It writes `comparison.json` and `comparison.md` in the run folder, `comparison.json` in each job's folder, and the
comparison block of each job's record.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

from . import records


# Quantities and metrics ------------------------------------------------------------------------------------------------

def numbers(value: dict, quantity: str) -> list[float]:
    """Every number a quantity holds, in a fixed order: along a path such as types[].rule.c, lists in order and
    mappings by sorted key, so that two files are compared element by element."""
    nodes = [value]
    for segment in quantity.split("."):
        key, every = (segment[:-2], True) if segment.endswith("[]") else (segment, False)
        nxt = []
        for node in nodes:
            if not isinstance(node, dict) or key not in node:
                raise KeyError(f"no {quantity}")
            item = node[key]
            if every:
                if not isinstance(item, list):
                    raise KeyError(f"{quantity}: not a list at {key}")
                nxt += item
            else:
                nxt.append(item)
        nodes = nxt
    out: list[float] = []

    def flatten(v):
        if isinstance(v, bool) or v is None or isinstance(v, str):
            return
        if isinstance(v, (int, float)):
            out.append(float(v))
        elif isinstance(v, list):
            for x in v:
                flatten(x)
        elif isinstance(v, dict):
            for k in sorted(v):
                flatten(v[k])

    for n in nodes:
        flatten(n)
    return out


def distance(a: list[float], b: list[float], metric: str) -> float:
    """max_abs_difference, or max_relative_difference: the absolute difference divided by the larger of one and the
    first value's magnitude; the largest over every number."""
    if len(a) != len(b):
        raise ValueError(f"the two files hold {len(a)} and {len(b)} numbers")
    if not a:
        raise ValueError("no numbers to compare")
    if metric == "max_abs_difference":
        return max(abs(x - y) for x, y in zip(a, b))
    if metric == "max_relative_difference":
        return max(abs(x - y) / max(1.0, abs(x)) for x, y in zip(a, b))
    raise ValueError(f"unknown metric {metric}")


def compare(a: dict, b: dict, quantity: str, metric: str) -> float:
    return distance(numbers(a, quantity), numbers(b, quantity), metric)


# The checks -------------------------------------------------------------------------------------------------------------

def _levels_in_order(levels, order: list[str]) -> list[str]:
    """Levels as the experiment lists them, coarse to fine; a level the experiment does not list comes last."""
    return sorted(levels, key=lambda lv: (order.index(lv) if lv in order else len(order), lv))


def value_at(data: dict, path: str):
    """One value along a path with no [] in it, such as parameter_file_sha256; None when absent."""
    node = data
    for key in path.split("."):
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
    return node


def _verdict(outcomes: list[bool], errors: list[str]) -> str:
    if errors:
        return "error"
    if not outcomes:
        return "not applicable"
    return "pass" if all(outcomes) else "fail"


def evaluate_check(check: dict, results: dict, members: list[str], order: list[str]) -> dict:
    """One check on a run's results, `results[toolkit][member][level]`, the levels ordered as the experiment lists
    them. Returns the verdict and the numbers behind it. A comparison the run holds too little for is not applicable,
    never a failure."""
    quantity, metric, expect = check["quantity"], check["metric"], check["expect"]
    at_most = expect.get("at_most") if isinstance(expect, dict) else None
    values, outcomes, errors = [], [], []

    def dist(x: dict, y: dict, label: str) -> float | None:
        try:
            return compare(x, y, quantity, metric)
        except (KeyError, ValueError) as e:
            errors.append(f"{label}: {e}")
            return None

    if check["compare"] == "members":
        for toolkit, by_member in results.items():
            levels = set().union(*(set(v) for v in by_member.values())) if by_member else set()
            for level in _levels_in_order(levels, order):
                series = []
                for a, b in check["pairs"]:
                    ra, rb = by_member.get(a, {}).get(level), by_member.get(b, {}).get(level)
                    if ra is None or rb is None:
                        series = None
                        break
                    d = dist(ra, rb, f"{toolkit} {a} against {b} at {level}")
                    series.append(d)
                if series is None or any(d is None for d in series):
                    continue
                values.append({"toolkit": toolkit, "level": level, "pairs": [[a, b] for a, b in check["pairs"]], "values": series})
                if expect == "decreasing":
                    outcomes.append(all(later < earlier for earlier, later in zip(series, series[1:])))
                elif at_most is not None:
                    outcomes.append(all(d <= at_most for d in series))
    elif check["compare"] == "toolkits":
        chosen = check.get("members") or members
        for t1, t2 in itertools.combinations(sorted(results), 2):
            for member in chosen:
                levels = _levels_in_order(set(results[t1].get(member, {})) & set(results[t2].get(member, {})), order)
                series = []
                for level in levels:
                    d = dist(results[t1][member][level], results[t2][member][level], f"{t1} against {t2}, {member} at {level}")
                    if d is None:
                        series = None
                        break
                    series.append((level, d))
                if not series:
                    continue
                values.append({"toolkits": [t1, t2], "member": member, "values": {lv: d for lv, d in series}})
                if expect == "falls_with_level":
                    if len(series) >= 2:
                        outcomes.append(all(later < earlier for (_, earlier), (_, later) in zip(series, series[1:])))
                elif at_most is not None:
                    outcomes.append(all(d <= at_most for _, d in series))
    elif check["compare"] == "levels":
        chosen = check.get("members") or members
        for toolkit, by_member in results.items():
            for member in chosen:
                levels = _levels_in_order(by_member.get(member, {}), order)
                steps = []
                for lo, hi in zip(levels, levels[1:]):
                    d = dist(by_member[member][lo], by_member[member][hi], f"{toolkit} {member}, {lo} to {hi}")
                    if d is None:
                        steps = None
                        break
                    steps.append((f"{lo}-{hi}", d))
                if not steps:
                    continue
                values.append({"toolkit": toolkit, "member": member, "values": {k: d for k, d in steps}})
                if expect == "falls_with_level":
                    if len(steps) >= 2:
                        outcomes.append(all(later < earlier for (_, earlier), (_, later) in zip(steps, steps[1:])))
                elif at_most is not None:
                    outcomes.append(all(d <= at_most for _, d in steps))
    return {"id": check["id"], "statement": check["statement"], "compare": check["compare"], "quantity": quantity,
            "metric": metric, "expect": expect, "verdict": _verdict(outcomes, errors), "values": values,
            "errors": errors}


# The reference ----------------------------------------------------------------------------------------------------------

def reference_quantities(experiment: dict) -> list[dict]:
    """The quantities compared with the reference: the experiment's own list, or its reports under the absolute
    metric when it names none."""
    return experiment.get("reference_quantities") or [{"quantity": q, "metric": "max_abs_difference"}
                                                       for q in experiment["reports"]]


def load_reference(experiment_file: Path, member: dict) -> tuple[dict | None, str | None, str | None]:
    """A member's reference results file, its hash checked: (results, hash, problem)."""
    ref = member.get("reference")
    if not ref:
        return None, None, None
    path = Path(experiment_file).resolve().parent / ref["results_file"]
    if not path.is_file():
        return None, None, f"no reference file {ref['results_file']}"
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != ref["results_sha256"]:
        return None, digest, f"the reference file {ref['results_file']} does not hash as the experiment says"
    return json.loads(data.decode("utf-8")), digest, None


def reference_distances(results: dict, reference: dict, quantities: list[dict], errors: dict) -> list[dict]:
    """Every distance from the reference, each with the reference's own error for that quantity beside it, or the
    reason it could not be computed. No verdict."""
    out = []
    for q in quantities:
        row = {"quantity": q["quantity"], "metric": q["metric"]}
        try:
            row["distance"] = compare(results, reference, q["quantity"], q["metric"])
        except (KeyError, ValueError) as e:
            row["problem"] = str(e)
        if q["quantity"] in errors:
            row["reference_error"] = errors[q["quantity"]]
        out.append(row)
    return out


# The run ----------------------------------------------------------------------------------------------------------------

def run_comparison(experiment: dict, experiment_file: Path, jobs: list[dict], run: Path,
                   identity: list[str] = ()) -> dict:
    """Everything the comparator writes for one run folder, as one object; the files are written by the caller.
    `identity` names the results-file keys, such as parameter_file_sha256 and request_file_sha256, that a job's file
    and its reference must agree on for the reference to answer the same question."""
    results: dict = {}
    job_results = {}
    for j in jobs:
        f = j["dir"] / "results.json"
        if f.is_file():
            data = json.loads(f.read_text(encoding="utf-8"))
            results.setdefault(j["toolkit"], {}).setdefault(j["member"], {})[j["level"]] = data
            job_results[id(j)] = data
    members = [m["id"] for m in experiment["members"]]
    checks = [evaluate_check(c, results, members, list(experiment["levels"])) for c in experiment["checks"]]
    quantities = reference_quantities(experiment)
    by_member = {m["id"]: m for m in experiment["members"]}
    per_job = []
    for j in jobs:
        entry = {"toolkit": j["toolkit"], "member": j["member"], "level": j["level"], "dir": str(j["dir"])}
        data = job_results.get(id(j))
        reference, digest, problem = load_reference(experiment_file, by_member[j["member"]])
        pinned = bool(by_member[j["member"]].get("reference"))
        if data is None:
            entry.update({"status": "not run", "reason": "no results file"})
        elif not pinned:
            entry.update({"status": "not run", "reason": "the member pins no reference"})
        elif reference is None:
            entry.update({"status": "error", "reason": problem})
            if digest:
                entry["reference"] = digest
        else:
            mismatched = [k for k in identity if value_at(data, k) != value_at(reference, k)]
            errors = by_member[j["member"]]["reference"].get("errors", {})
            rows = reference_distances(data, reference, quantities, errors)
            problems = [f"{r['quantity']}: {r['problem']}" for r in rows if "problem" in r]
            entry.update({"reference": digest, "distances": rows})
            if mismatched:
                entry.update({"status": "error", "reason": "the reference does not answer the same question: "
                              + ", ".join(f"{k} differs" for k in mismatched)})
            elif problems:
                entry.update({"status": "error", "reason": "a distance could not be computed: " + "; ".join(problems)})
            else:
                entry["status"] = "computed"
                largest = max(rows, key=lambda r: r["distance"])
                entry["largest_distance"] = {k: largest[k] for k in ("quantity", "metric", "distance", "reference_error") if k in largest}
        per_job.append(entry)
    failed = any(c["verdict"] in ("fail", "error") for c in checks) or any(j["status"] == "error" for j in per_job)
    return {"experiment": experiment["experiment"], "run": run.name, "checks": checks, "reference": per_job,
            "failed": failed}


def as_markdown(report: dict) -> str:
    """The run's comparison as tables a findings README can include: the checks, then the distances."""
    lines = [f"# Comparison: {report['experiment']}, run {report['run']}", "", "## The experiment's checks", "",
             "| check | compare | quantity | metric | expectation | verdict |", "|---|---|---|---|---|---|"]
    for c in report["checks"]:
        exp = c["expect"] if isinstance(c["expect"], str) else f"at most {c['expect']['at_most']:g}"
        lines.append(f"| `{c['id']}` | {c['compare']} | `{c['quantity']}` | {c['metric']} | {exp} | **{c['verdict']}** |")
    for c in report["checks"]:
        if c["values"] or c["errors"]:
            lines += ["", f"`{c['id']}`:"]
            for v in c["values"]:
                vals = v["values"]
                shown = ", ".join(f"{x:.3g}" for x in vals) if isinstance(vals, list) else ", ".join(f"{k} {x:.3g}" for k, x in vals.items())
                who = v.get("toolkit") or " against ".join(v.get("toolkits", []))
                where = v.get("level") or v.get("member", "")
                lines.append(f"- {who}, {where}: {shown}")
            for e in c["errors"]:
                lines.append(f"- error: {e}")
    lines += ["", "## Distances from the reference", "",
              "| toolkit | member | level | quantity | metric | distance | the reference's error |", "|---|---|---|---|---|---|---|"]
    for j in report["reference"]:
        if j["status"] != "computed":
            lines.append(f"| {j['toolkit']} | {j['member']} | {j['level']} | | | **{j['status']}**: {j['reason']} | |")
            if "distances" not in j:
                continue
        for r in j["distances"]:
            d = f"{r['distance']:.3g}" if "distance" in r else f"not computed: {r['problem']}"
            e = f"{r['reference_error']:.3g}" if "reference_error" in r else "not stated"
            lines.append(f"| {j['toolkit']} | {j['member']} | {j['level']} | `{r['quantity']}` | {r['metric']} | {d} | {e} |")
    lines += ["", "A distance is reported with the reference's error beside it and carries no verdict; the exit status is the checks' alone."]
    return "\n".join(lines) + "\n"


def write_outputs(report: dict, jobs: list[dict], run: Path) -> None:
    """The run's files, each job's file, and each record's comparison block."""
    (run / "comparison.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    (run / "comparison.md").write_text(as_markdown(report), encoding="utf-8")
    by_dir = {str(j["dir"]): j for j in jobs}
    for entry in report["reference"]:
        job = by_dir[entry["dir"]]
        job_report = {k: v for k, v in entry.items() if k != "dir"}
        (job["dir"] / "comparison.json").write_text(json.dumps(job_report, indent=1) + "\n", encoding="utf-8")
        record = job["dir"] / "record.json"
        if record.is_file():
            data = json.loads(record.read_text(encoding="utf-8"))
            block = {"status": entry["status"], "report": "comparison.json"}
            if entry.get("reason"):
                block["reason"] = entry["reason"]
            if entry.get("reference"):
                block["reference"] = entry["reference"]
            if entry.get("largest_distance"):
                block["largest_distance"] = entry["largest_distance"]
            data["extensions"]["sce-wg-1"]["comparison"] = block
            records.write(data, record)
