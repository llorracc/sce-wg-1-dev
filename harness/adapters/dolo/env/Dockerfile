# dolo's environment as an image: the interpreter of .python-version, uv, and the lock file's packages, and nothing of
# the model. A job mounts the repository read-only at /src and runs the adapter from there (schemas/registry.md, "The
# container contract, exactly"); the image is identified by its ID, which the registry records. Built with
#   docker build --file harness/adapters/dolo/env/Dockerfile --tag sce-wg-1/dolo:<tag> harness/adapters/dolo/env
FROM python:3.11.14-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.9.28 /uv /uvx /bin/
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1 UV_PYTHON_DOWNLOADS=never
WORKDIR /opt/env
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev
ENV VIRTUAL_ENV=/opt/env/.venv PATH=/opt/env/.venv/bin:/usr/local/bin:/usr/bin:/bin
WORKDIR /src
