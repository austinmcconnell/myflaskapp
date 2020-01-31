FROM python:3.6-slim AS builder

WORKDIR /home/myflaskapp

RUN apt-get update && \
    apt-get install -y \
    gcc \
    graphviz \
    libgraphviz-dev \
    libpq-dev \
    python3-dev

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir --upgrade pip setuptools pipenv \
    && PIPENV_VERBOSITY=-1 PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

COPY . .

ENV FLASK_APP wsgi.py

FROM python:3.6-slim

COPY --from=builder /home/myflaskapp /home/myflaskapp

WORKDIR /home/myflaskapp

RUN apt-get update && \
    apt-get install -y \
    graphviz \
    libpq5

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
