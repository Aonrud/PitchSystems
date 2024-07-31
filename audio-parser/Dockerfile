FROM python:3.10-slim

ARG POETRY_VERSION=1.8.3
RUN pip install poetry==$POETRY_VERSION

# PYTHONDONTWRITEBYTECODE: No need to cache when process only runs once
# PYTHONUNBUFFERED: Seems to help prevent logs being held before STOUT/STERR
ENV PYTHONDONTWRITEBYTECODE=1 \ 
    PYTHONUNBUFFERED=1s 


ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /opt/app
COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev

COPY . .

CMD ["poetry", "run", "gunicorn", "--config", "audio_parser/gunicorn_conf.py", "audio_parser.app:app"]
