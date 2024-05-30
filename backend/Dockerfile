##
# App build stage
##

FROM python:3.11.3-slim-buster AS backend_build

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SECRET_KEY='build' \
    DB_CONNECTION='{"dbname":"build","username":"build","password":"build","host":"db","port":5432}' \
    PIP_NO_CACHE_DIR=off


RUN apt-get update \
    && apt-get install -y gcc libcurl4-openssl-dev libssl-dev libmagic1 curl gettext \
    && pip install --no-cache-dir setuptools pdm

RUN pdm config python.use_venv False


WORKDIR /pkgs

COPY ./backend/pdm.lock ./backend/pyproject.toml /pkgs/
RUN pdm sync \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

### Dockerfile
WORKDIR /app

COPY ./backend /app/

FROM backend_build AS backend

ENV PYTHONPATH=/pkgs/__pypackages__/3.11/lib \
    PATH=$PATH:/pkgs/__pypackages__/3.11/bin

RUN python manage.py collectstatic --no-input
