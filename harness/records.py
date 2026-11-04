"""The run registry's records (../schemas/registry.md): what the runner writes for every build and every job, in the
format of `execution-record.schema.json` (the core, destined for REMARK) with the fork's fields under the namespace
`sce-wg-1` (`runs.registry.schema.json`). Everything here is a fact read from git, the machine or the job; nothing is
inferred.

The repository's state: the remote normalized to https, the commit, whether the working tree was dirty by
`git status --porcelain`, and when it was, the tree of the working tree written through a temporary index. An
environment's hash is taken over the files git records under its directory in the tree that ran, each blob read from
git, then a sorted listing hashed, so that untracked files and caches never enter it and two specifications compare
file by file.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import platform
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CORE_SCHEMA = HERE / "execution-record.schema.json"
FORK_SCHEMA = HERE / "runs.registry.schema.json"
RECORD_VERSION = "0.1.0-draft.4"
FORK_SCHEMA_ID = json.loads(FORK_SCHEMA.read_text(encoding="utf-8"))["$id"]


def git(*args: str, cwd: Path = ROOT) -> str:
    done = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if done.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {done.stderr.strip()}")
    return done.stdout.strip()


def now() -> str:
    """An RFC 3339 stamp with an offset, to the second, as the schema's pattern wants."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def https_remote(url: str) -> str:
    """A remote normalized to the https form the catalog names: ssh and git forms rewritten, `.git` dropped."""
    u = url.strip()
    if u.startswith("git@") and ":" in u:
        host, _, path = u[4:].partition(":")
        u = f"https://{host}/{path}"
    elif u.startswith("ssh://"):
        u = "https://" + u[6:].split("@", 1)[-1]
    elif u.startswith("git://"):
        u = "https://" + u[6:]
    return u[:-4] if u.endswith(".git") else u


def worktree_tree() -> str:
    """The tree of the working tree as it is, tracked changes and untracked unignored files included, written
    through a temporary index that both commands read, so that the real index is neither read nor changed."""
    index = tempfile.mktemp(prefix="sce-index-")
    env = {**os.environ, "GIT_INDEX_FILE": index}
    try:
        for args in (["add", "-A"], ["write-tree"]):
            done = subprocess.run(["git", *args], cwd=ROOT, env=env, capture_output=True, text=True)
            if done.returncode:
                raise RuntimeError(f"git {' '.join(args)} on a temporary index: {done.stderr.strip()}")
        return done.stdout.strip()
    finally:
        Path(index).unlink(missing_ok=True)


def repository() -> dict:
    """The repository block: remote, commit, dirty, and the working tree's tree when dirty."""
    out = {"remote": https_remote(git("remote", "get-url", "origin")), "commit": git("rev-parse", "HEAD"),
           "dirty": bool(git("status", "--porcelain"))}
    if out["dirty"]:
        out["worktree_tree"] = worktree_tree()
    return out


def tree_that_ran(repo: dict) -> str:
    return repo["worktree_tree"] if repo["dirty"] else repo["commit"]


def environment_hash(tree: str, path: str) -> tuple[str, str | None]:
    """The schema's hash of an environment directory in a tree, and git's own name for that directory's tree.

    `git ls-tree -r <tree> -- <path>` lists what git records there, never the index or the files on disk. Each blob's
    bytes, or a symbolic link's text, are hashed alone; then the listing `<type> <mode> <sha256> <path>` with the path
    relative to the directory, sorted bytewise on the path, is hashed."""
    listing = git("ls-tree", "-r", tree, "--", path)
    lines = []
    for line in listing.splitlines():
        meta, _, name = line.partition("\t")
        mode, kind, obj = meta.split()
        if kind != "blob":
            continue
        blob = subprocess.run(["git", "cat-file", "blob", obj], cwd=ROOT, capture_output=True).stdout
        relname = name[len(path):].lstrip("/") if name.startswith(path) else name
        lines.append((relname.encode("utf-8"), f"{'link' if mode == '120000' else 'blob'} {mode} "
                      f"{hashlib.sha256(blob).hexdigest()} {relname}\n"))
    if not lines:
        raise RuntimeError(f"nothing tracked under {path} in {tree[:12]}")
    lines.sort(key=lambda p: p[0])
    digest = hashlib.sha256("".join(text for _, text in lines).encode("utf-8")).hexdigest()
    done = subprocess.run(["git", "rev-parse", f"{tree}:{path}"], cwd=ROOT, capture_output=True, text=True)
    return digest, (done.stdout.strip() if done.returncode == 0 else None)


def environment(repo: dict, path: str, kind: str, builder: str | None = None) -> dict:
    digest, git_tree = environment_hash(tree_that_ran(repo), path)
    out = {"path": path, "kind": kind, "sha256": digest}
    if git_tree:
        out["git_tree"] = git_tree
    if builder:
        out["builder"] = builder
    return out


def _read(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return ""


def machine(runtime: str) -> dict:
    """The `where` block: the machine's facts and the runtime, nothing of the run's settings."""
    cpu = next((ln.split(":", 1)[1].strip() for ln in _read("/proc/cpuinfo").splitlines()
                if ln.startswith("model name")), platform.processor() or platform.machine())
    mem = next((int(ln.split()[1]) * 1024 for ln in _read("/proc/meminfo").splitlines()
                if ln.startswith("MemTotal:")), 0)
    pretty = next((ln.split("=", 1)[1].strip().strip('"') for ln in _read("/etc/os-release").splitlines()
                   if ln.startswith("PRETTY_NAME=")), platform.platform())
    return {"host": platform.node(), "cpu": cpu, "cores": os.cpu_count() or 1, "memory_bytes": mem, "os": pretty,
            "kernel": platform.release(), "runtime": runtime}


def docker_runtime() -> str | None:
    """'docker <server version>' when the daemon answers, else None."""
    done = subprocess.run(["docker", "version", "--format", "{{.Server.Version}}"], capture_output=True, text=True)
    return f"docker {done.stdout.strip()}" if done.returncode == 0 and done.stdout.strip() else None


def outputs(folder: Path, names: tuple[str, ...]) -> list[dict]:
    out = []
    for n in names:
        p = folder / n
        if p.is_file():
            data = p.read_bytes()
            out.append({"path": n, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    return out


def validate(record: dict) -> None:
    """Refuses a record that does not match the fork's schema, which covers builds and executions alike."""
    import jsonschema
    from referencing import Registry, Resource

    core = json.loads(CORE_SCHEMA.read_text(encoding="utf-8"))
    fork = json.loads(FORK_SCHEMA.read_text(encoding="utf-8"))
    registry = Registry().with_resources([(core["$id"], Resource.from_contents(core)),
                                          (fork["$id"], Resource.from_contents(fork))])
    errors = list(jsonschema.Draft202012Validator(fork, registry=registry).iter_errors(record))
    if errors:
        raise ValueError("the record does not match runs.registry.schema.json:\n  "
                         + "\n  ".join(f"{e.json_path}: {e.message}" for e in errors[:5]))


def write(record: dict, path: Path) -> None:
    validate(record)
    path.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
