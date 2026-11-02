"""The harness's runner (runner.py), tested on a stand-in toolkit that copies committed results files, so that the
tests need neither HARK nor dolo:

    uv run --project harness --frozen pytest -q harness/test_runner.py

What they establish: the registry names files that exist; a run lays out its jobs, records each job's status and
fingerprint and a manifest with no timings; a rerun skips what is done and redoes what changed or failed; a failure is
recorded and the other jobs run; verification passes good files and catches a missing quantity; an experiment with
problems is refused. They solve nothing. Whether the real toolkits reproduce their committed files is the acceptance
run, recorded in the findings.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import runner  # noqa: E402

EXPERIMENT = runner.SCHEMAS / "bst" / "experiments" / "restrained-limit" / "experiment.yaml"
STUB = HERE / "test_support" / "stub_adapter.py"


def stub_registry(tmp_path: Path) -> tuple[Path, Path]:
    stub = tmp_path / "stub_adapter.py"
    shutil.copyfile(STUB, stub)
    reg = tmp_path / "toolkits.yaml"
    reg.write_text(yaml.safe_dump({"toolkits": {"stub": {"adapter": str(stub), "levels": {"low": 1, "medium": 2, "high": 3},
                                                         "threads": 1}}}), encoding="utf-8")
    return reg, stub


def run(reg: Path, out: Path, *extra: str) -> int:
    return runner.main(["--registry", str(reg), "run", str(EXPERIMENT), "--toolkits", "stub", "--out", str(out), *extra])


def manifest(out: Path) -> dict:
    return json.loads((out / "manifest.json").read_text(encoding="utf-8"))


def test_the_registry_names_files_that_exist():
    registry = runner.load_registry()
    assert set(registry) == {"hark", "dolo"}
    for tk in registry.values():
        assert tk["adapter"].is_file() and tk["stone"].is_file()
        assert all((tk["environment"] / f).is_file() for f in ("pyproject.toml", "uv.lock", ".python-version"))
        assert runner.HERE / "adapters" / "common.py" in tk["code"] and tk["adapter"] in tk["code"]
        assert set(tk["levels"]) >= {"low", "medium", "high"}


def test_a_run_lays_out_its_jobs(tmp_path):
    reg, _ = stub_registry(tmp_path)
    out = tmp_path / "run"
    assert run(reg, out, "--levels", "low,medium") == 0
    m = manifest(out)
    assert len(m["jobs"]) == 8 and {j["status"] for j in m["jobs"]} == {"ok"}
    for j in m["jobs"]:
        d = out / "stub" / j["member"] / f"level-{runner.LEVEL_NUMBER[j['level']]}"
        assert (d / "results.json").is_file() and (d / "adapter.log").is_file()
        assert json.loads((d / "job.json").read_text())["fingerprint"]["parameter_file_sha256"]
    assert m["experiment"]["name"] == "restrained-limit/1" and m["toolkits"]["stub"]["code_sha256"]
    words = json.dumps(m).lower()
    assert not any(w in words for w in ("duration", "elapsed", "seconds")), "a run records no timings"


def test_a_rerun_skips_what_is_done_and_redoes_what_changed(tmp_path):
    reg, stub = stub_registry(tmp_path)
    out = tmp_path / "run"
    assert run(reg, out, "--levels", "low") == 0
    assert run(reg, out, "--levels", "low") == 0
    assert {j["skipped"] for j in manifest(out)["jobs"]} == {"yes"}
    stub.write_text(stub.read_text() + "\n# changed\n")
    assert run(reg, out, "--levels", "low") == 0
    assert {j["skipped"] for j in manifest(out)["jobs"]} == {"no"}


def test_a_failure_is_recorded_and_the_rest_run(tmp_path, monkeypatch):
    reg, _ = stub_registry(tmp_path)
    out = tmp_path / "run"
    monkeypatch.setenv("STUB_FAIL", "bst-restrained")
    assert run(reg, out, "--levels", "low") == 1
    status = {j["member"]: j["status"] for j in manifest(out)["jobs"]}
    assert status.pop("bst-restrained") == "failed" and set(status.values()) == {"ok"}
    monkeypatch.delenv("STUB_FAIL")
    assert run(reg, out, "--levels", "low") == 0
    skipped = {j["member"]: j["skipped"] for j in manifest(out)["jobs"]}
    assert skipped.pop("bst-restrained") == "no" and set(skipped.values()) == {"yes"}


def test_verification_passes_good_files(tmp_path):
    reg, _ = stub_registry(tmp_path)
    out = tmp_path / "run"
    assert run(reg, out, "--levels", "low") == 0
    assert runner.main(["--registry", str(reg), "verify", str(out)]) == 0
    verdicts = json.loads((out / "verification.json").read_text())
    assert len(verdicts) == 4 and {v["status"] for v in verdicts} == {"ok"}


def test_verification_catches_a_missing_quantity(tmp_path, monkeypatch):
    reg, _ = stub_registry(tmp_path)
    out = tmp_path / "run"
    monkeypatch.setenv("STUB_DROP", "kink")
    assert run(reg, out, "--levels", "low") == 0
    assert runner.main(["--registry", str(reg), "verify", str(out)]) == 1
    verdicts = json.loads((out / "verification.json").read_text())
    assert all("types[].kink" in v["missing_reports"] for v in verdicts)


def test_an_experiment_with_problems_is_refused(tmp_path):
    reg, _ = stub_registry(tmp_path)
    bst = tmp_path / "bst"
    shutil.copytree(runner.SCHEMAS / "bst", bst, ignore=shutil.ignore_patterns("__pycache__"))
    path = bst / "experiments" / "restrained-limit" / "experiment.yaml"
    path.write_text(path.read_text().replace("6e8651cdf2cd0baa", "0e8651cdf2cd0baa"))
    with pytest.raises(SystemExit, match="the parameter file's hash differs"):
        runner.main(["--registry", str(reg), "run", str(path), "--toolkits", "stub", "--out", str(tmp_path / "run")])
