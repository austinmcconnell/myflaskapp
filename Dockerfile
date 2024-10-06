FROM python:3.9-slim AS base

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_VERBOSITY=-1

WORKDIR /app

# Buildtime dependencies
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt/lists \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    graphviz \
    libgraphviz-dev \
    libpq-dev \
    python3-dev

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip setuptools wheel pipenv

COPY Pipfile Pipfile.lock ./

RUN --mount=type=cache,target=/root/.cache/pipenv \
    pipenv install --deploy --verbose

From base as base-dev

RUN --mount=type=cache,target=/root/.cache/pipenv \
    pipenv install --dev --deploy --verbose

FROM python:3.9-slim as dev

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# Runtime dependencies
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt/lists \
    apt-get update && \
    apt-get install --no-install-recommends -y \
    graphviz \
    libpq5

COPY --from=base-dev $VIRTUAL_ENV $VIRTUAL_ENV

COPY . .

RUN flask translate compile

EXPOSE 5000
EXPOSE 5678

ENTRYPOINT ["gunicorn", "--reload"]

FROM python:3.9-slim as prod

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# Runtime dependencies
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt/lists \
    apt-get update && \
    apt-get install --no-install-recommends -y \
    graphviz \
    libpq5

COPY --from=base $VIRTUAL_ENV $VIRTUAL_ENV

COPY . .

RUN flask translate compile

EXPOSE 5000

ENTRYPOINT ["gunicorn"]
