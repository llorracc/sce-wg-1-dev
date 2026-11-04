# HARK's environment as an image: the interpreter of .python-version, uv, and the lock file's packages, and nothing of
# the model. A job mounts the repository read-only at /src and runs the adapter from there (schemas/registry.md, "The
# container contract, exactly"); the image is identified by its ID, which the registry records. Built with
#   docker build --file harness/adapters/hark/env/Dockerfile --tag sce-wg-1/hark:<tag> harness/adapters/hark/env
FROM python:3.12.3-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.9.28 /uv /uvx /bin/
# git, for the pinned HARK commit the lock file names.
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1 UV_PYTHON_DOWNLOADS=never
WORKDIR /opt/env
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev
ENV VIRTUAL_ENV=/opt/env/.venv PATH=/opt/env/.venv/bin:/usr/local/bin:/usr/bin:/bin
WORKDIR /src
