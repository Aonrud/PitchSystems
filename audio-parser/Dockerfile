FROM python:3.12

RUN apt-get update && apt-get install -y supervisor

ARG POETRY_VERSION=1.8.3
RUN pip install poetry==$POETRY_VERSION

# PYTHONDONTWRITEBYTECODE: No need to cache when process only runs once
# PYTHONUNBUFFERED: Seems to help prevent logs being held before STOUT/STERR
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1s

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Setup shared socket dir
RUN mkdir -p /run/sockets
RUN chmod 777 /run/sockets

# Set up user
RUN groupadd --gid 1001 audioparser && \
        useradd --uid 1001 --gid audioparser --shell /bin/bash audioparser
USER audioparser

# Set up supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install dependencies
WORKDIR /opt/app
COPY --chown=1001:1001 pyproject.toml poetry.lock .
RUN poetry install --without dev

# Copy app files
COPY --chown=1001:1001 . .

EXPOSE 5678
ENTRYPOINT ["/usr/bin/supervisord"]
