"""The harness's runner (../schemas/harness.md): every toolkit on an experiment's members and levels, then the checker
on every results file it wrote.

    uv run --project harness --frozen python harness/runner.py list
    uv run --project harness --frozen python harness/runner.py run <experiment.yaml> --toolkits hark,dolo \\
        [--levels low,medium] [--members <id>,...] [--jobs 8] [--out <run folder>]
    uv run --project harness --frozen python harness/runner.py verify <run folder>

`run` checks the experiment (schemas/checker/experiment.py) and refuses one with problems. It then runs one job for
each toolkit, member and level, in parallel, each through the toolkit's adapter in the toolkit's locked environment. Each toolkit's first job runs
alone before its others, so that one process writes what the toolkit compiles and caches.
A job writes into <run folder>/<toolkit>/<member>/level-<n>/, n being 1, 2 and 3 for low, medium and high, and leaves
there the adapter's log and `job.json`: its status, and a fingerprint of everything its output depends on. A job whose
fingerprint is unchanged and whose results file exists is skipped, so a rerun redoes only what failed or changed.
`manifest.json` in the run folder names every hash. Nothing records how long anything took.

`verify` runs `check.py --verify-results` on every results file and checks that each carries the quantities the
experiment's `reports` names, writing `verification.json`. The experiment's checks are the comparator's, which is not
written yet.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import glob
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCHEMAS = ROOT / "schemas"
sys.path.insert(0, str(SCHEMAS / "checker"))
import canonical  # noqa: E402
import experiment as experiments  # noqa: E402

REGISTRY = HERE / "toolkits.yaml"
LEVEL_NUMBER = {"low": 1, "medium": 2, "high": 3}
THREAD_VARIABLES = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rel(path: Path) -> str:
    """A path relative to the repository, for the records; absolute if it lies outside."""
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(Path(path).resolve())


# The registry ---------------------------------------------------------------------------------------------------------

def load_registry(path: Path = REGISTRY) -> dict:
    """The toolkits, with their paths resolved against the registry file's folder."""
    path = Path(path).resolve()
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))["toolkits"]
    out = {}
    for name, entry in raw.items():
        unknown = set(entry) - {"adapter", "code", "environment", "stone", "levels", "threads"}
        if unknown or not {"adapter", "levels"} <= set(entry):
            raise SystemExit(f"toolkits.yaml: {name}: unknown keys {sorted(unknown)} or no adapter or levels")
        tk = {"name": name, "adapter": (path.parent / entry["adapter"]).resolve(),
              "levels": dict(entry["levels"]), "threads": int(entry.get("threads", 2))}
        tk["environment"] = (path.parent / entry["environment"]).resolve() if entry.get("environment") else None
        tk["stone"] = (path.parent / entry["stone"]).resolve() if entry.get("stone") else None
        files = set()
        for pattern in entry.get("code", []) + [entry["adapter"]]:
            for f in glob.glob(str(path.parent / pattern)):
                if not Path(f).name.startswith("test_"):
                    files.add(Path(f).resolve())
        tk["code"] = sorted(files)
        out[name] = tk
    return out


def environment_identity(tk: dict) -> dict | None:
    """What identifies a toolkit's environment: its lock file and interpreter."""
    env = tk["environment"]
    if env is None:
        return None
    version = env / ".python-version"
    return {"project": rel(env), "lock_sha256": sha256_file(env / "uv.lock"),
            "python": version.read_text(encoding="utf-8").strip() if version.is_file() else None}


def code_sha256(tk: dict) -> str:
    h = hashlib.sha256()
    for f in tk["code"]:
        h.update(rel(f).encode() + b"\0" + Path(f).read_bytes() + b"\0")
    return h.hexdigest()


# The experiment and the jobs ------------------------------------------------------------------------------------------

def load_experiment(path: Path) -> tuple[dict, str]:
    """The experiment and its hash; refuses one with problems."""
    path = Path(path).resolve()
    data = canonical.load_strict(path.read_text(encoding="utf-8"))
    problems = experiments.problems(data, path.parent)
    if problems:
        raise SystemExit("the experiment has problems:\n  " + "\n  ".join(problems))
    return data, canonical.model_hash(data)


def plan_jobs(exp_path: Path, exp: dict, registry: dict, toolkits: list[str], levels: list[str], members: list[str],
              out: Path) -> list[dict]:
    folder = Path(exp_path).resolve().parent
    by_id = {m["id"]: m for m in exp["members"]}
    unknown = [m for m in members if m not in by_id] + [t for t in toolkits if t not in registry]
    unknown += [lv for lv in levels if lv not in LEVEL_NUMBER]
    if unknown:
        raise SystemExit(f"unknown toolkit, member or level: {unknown}")
    jobs = []
    for name in toolkits:
        tk = registry[name]
        missing = [lv for lv in levels if lv not in tk["levels"]]
        if missing:
            raise SystemExit(f"{name} offers no level {missing}")
        for mid in members:
            m = by_id[mid]
            for lv in levels:
                jobs.append({"toolkit": name, "member": mid, "level": lv, "level_arg": tk["levels"][lv],
                             "parameter_file": (folder / m["parameter_file"]).resolve(),
                             "request_file": (folder / m["request_file"]).resolve(),
                             "parameter_file_sha256": m["parameter_file_sha256"],
                             "request_file_sha256": m["request_file_sha256"],
                             "dir": out / name / mid / f"level-{LEVEL_NUMBER[lv]}"})
    return jobs


def fingerprint(job: dict, tk: dict) -> dict:
    """Everything a job's output depends on that the harness can name."""
    return {"toolkit": tk["name"], "member": job["member"], "level": job["level"], "level_arg": job["level_arg"],
            "parameter_file_sha256": job["parameter_file_sha256"], "request_file_sha256": job["request_file_sha256"],
            "environment": environment_identity(tk), "code_sha256": code_sha256(tk), "threads": tk["threads"]}


def command(job: dict, tk: dict) -> list[str]:
    args = [str(tk["adapter"]), str(job["parameter_file"]), "--out", str(job["dir"]), "--level", str(job["level_arg"]),
            "--request", str(job["request_file"])]
    if tk["environment"] is None:
        return [sys.executable] + args
    return ["uv", "run", "--quiet", "--project", str(tk["environment"]), "--frozen", "python"] + args


def run_job(job: dict, tk: dict) -> dict:
    d = job["dir"]
    fp = fingerprint(job, tk)
    record = d / "job.json"
    if record.is_file() and (d / "results.json").is_file():
        old = json.loads(record.read_text(encoding="utf-8"))
        if old.get("status") == "ok" and old.get("fingerprint") == fp:
            return {**old, "skipped": True}
    d.mkdir(parents=True, exist_ok=True)
    for stale in ("results.json", "job.json"):
        (d / stale).unlink(missing_ok=True)
    env = os.environ.copy()
    env.update({v: str(tk["threads"]) for v in THREAD_VARIABLES})
    cmd = command(job, tk)
    with open(d / "adapter.log", "w", encoding="utf-8") as log:
        code = subprocess.run(cmd, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    ok = code == 0 and (d / "results.json").is_file()
    shown = [rel(Path(c)) if c.startswith("/") else c for c in cmd]
    if tk["environment"] is None:
        shown[0] = "python"
    out = {"status": "ok" if ok else "failed", "exit_code": code, "command": shown, "fingerprint": fp}
    record.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    return {**out, "skipped": False}


def harness_commit() -> dict:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", "harness", "schemas", "rosetta"], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()
    return {"commit": head or None, "uncommitted_changes": "yes" if dirty else "no"}


def cmd_run(args) -> int:
    exp_path = Path(args.experiment).resolve()
    exp, exp_hash = load_experiment(exp_path)
    registry = load_registry(Path(args.registry))
    toolkits = args.toolkits.split(",")
    levels = args.levels.split(",") if args.levels else list(exp["levels"])
    members = args.members.split(",") if args.members else [m["id"] for m in exp["members"]]
    out = Path(args.out).resolve() if args.out else HERE / "runs" / exp["experiment"].replace("/", "-")
    jobs = plan_jobs(exp_path, exp, registry, toolkits, levels, members, out)
    for name in toolkits:
        env = registry[name]["environment"]
        if env is not None:
            sync = subprocess.run(["uv", "sync", "--quiet", "--project", str(env), "--frozen"], cwd=ROOT)
            if sync.returncode:
                raise SystemExit(f"{name}: its environment could not be built from {rel(env)}/uv.lock")
    out.mkdir(parents=True, exist_ok=True)
    started = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    # Each toolkit's first job runs before its others, so that what a toolkit compiles and caches on its first use
    # (numba's cache, for dolo) is written by one process. On 2026-11-02 four dolo jobs started together on a newly
    # built environment, and three failed with an LLVM error as they raced to write numba's cache.
    lead = list({j["toolkit"]: j for j in reversed(jobs)}.values())
    rest = [j for j in jobs if all(j is not k for k in lead)]
    outcomes = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        for batch in (lead, rest):
            futures = {pool.submit(run_job, j, registry[j["toolkit"]]): j for j in batch}
            for f in concurrent.futures.as_completed(futures):
                j, r = futures[f], f.result()
                outcomes.append((j, r))
                print(f"{j['toolkit']:6s} {j['member']:22s} {j['level']:7s} {'skipped' if r['skipped'] else r['status']}",
                      flush=True)
    order = {id(j): i for i, j in enumerate(jobs)}
    outcomes.sort(key=lambda p: order[id(p[0])])
    manifest = {
        "experiment": {"name": exp["experiment"], "file": rel(exp_path), "sha256": exp_hash},
        "members": [{k: m[k] for k in ("id", "parameter_file_sha256", "request_file_sha256")} for m in exp["members"]
                    if m["id"] in members],
        "levels": levels,
        "toolkits": {n: {"adapter": rel(registry[n]["adapter"]), "environment": environment_identity(registry[n]),
                         "code_sha256": code_sha256(registry[n]), "threads": registry[n]["threads"]} for n in toolkits},
        "harness": harness_commit(),
        "started": started,
        "jobs": [{"toolkit": j["toolkit"], "member": j["member"], "level": j["level"], "dir": rel(j["dir"]),
                  "status": r["status"], "skipped": "yes" if r["skipped"] else "no"} for j, r in outcomes],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    failed = [m for m in manifest["jobs"] if m["status"] != "ok"]
    print(f"{len(jobs)} jobs, {len(failed)} failed; the run is in {rel(out)}")
    return 1 if failed else 0


# Verification ---------------------------------------------------------------------------------------------------------

def carries(results: dict, quantity: str) -> bool:
    """Whether a results file holds a quantity, a path such as types[].kink, with a value in every item."""
    nodes = [results]
    for segment in quantity.split("."):
        key, every = (segment[:-2], True) if segment.endswith("[]") else (segment, False)
        nxt = []
        for node in nodes:
            if not isinstance(node, dict) or node.get(key) is None:
                return False
            value = node[key]
            if every:
                if not isinstance(value, list) or not value:
                    return False
                nxt += value
            else:
                nxt.append(value)
        nodes = nxt
    return True


def verify_job(job: dict, reports: list[str]) -> dict:
    results = job["dir"] / "results.json"
    if not results.is_file():
        return {"status": "no results file"}
    check = subprocess.run([sys.executable, str(SCHEMAS / "checker" / "check.py"), str(job["parameter_file"]),
                            "--verify-results", str(results)], cwd=ROOT, capture_output=True, text=True)
    lines = [ln for ln in (check.stdout + check.stderr).splitlines() if ln.strip()]
    missing = [q for q in reports if not carries(json.loads(results.read_text(encoding="utf-8")), q)]
    ok = check.returncode == 0 and not missing
    return {"status": "ok" if ok else "failed", "checker_exit_code": check.returncode,
            "checker": lines[-1].replace(str(ROOT) + "/", "") if lines else "", "missing_reports": missing}


def cmd_verify(args) -> int:
    run = Path(args.run).resolve()
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    exp_path = ROOT / manifest["experiment"]["file"]
    exp, exp_hash = load_experiment(exp_path)
    if exp_hash != manifest["experiment"]["sha256"]:
        raise SystemExit("the experiment file has changed since the run")
    registry = load_registry(Path(args.registry))
    jobs = plan_jobs(exp_path, exp, registry, list(manifest["toolkits"]), manifest["levels"],
                     [m["id"] for m in manifest["members"]], run)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        verdicts = list(pool.map(lambda j: verify_job(j, exp["reports"]), jobs))
    out = []
    for j, v in zip(jobs, verdicts):
        out.append({"toolkit": j["toolkit"], "member": j["member"], "level": j["level"], **v})
        print(f"{j['toolkit']:6s} {j['member']:22s} {j['level']:7s} {v['status']}"
              + (f"  missing: {', '.join(v['missing_reports'])}" if v.get("missing_reports") else "")
              + ("" if v["status"] == "ok" else f"  {v.get('checker', '')}"))
    (run / "verification.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    failed = [v for v in out if v["status"] != "ok"]
    print(f"{len(out)} results files, {len(failed)} failed")
    return 1 if failed else 0


def cmd_list(args) -> int:
    print("experiments:")
    for p in sorted(SCHEMAS.glob("**/experiments/*/experiment.yaml")):
        e = canonical.load_strict(p.read_text(encoding="utf-8"))
        print(f"  {e['experiment']:22s} {rel(p)}: {len(e['members'])} members, levels {', '.join(e['levels'])}")
    print("toolkits:")
    for name, tk in load_registry(Path(args.registry)).items():
        env = environment_identity(tk)
        print(f"  {name:6s} {rel(tk['adapter'])}, levels {', '.join(tk['levels'])}"
              + (f", Python {env['python']} locked in {env['project']}/uv.lock" if env else ", the harness's own Python"))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--registry", default=str(REGISTRY), help="the toolkits file (default: toolkits.yaml beside this)")
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    r = sub.add_parser("run")
    r.add_argument("experiment")
    r.add_argument("--toolkits", required=True)
    r.add_argument("--levels")
    r.add_argument("--members")
    r.add_argument("--jobs", type=int, default=4)
    r.add_argument("--out")
    v = sub.add_parser("verify")
    v.add_argument("run")
    v.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args(argv)
    return {"list": cmd_list, "run": cmd_run, "verify": cmd_verify}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
