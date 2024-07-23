FROM python:3.12-slim   

RUN apt-get update && apt-get install -y \
        pkg-config \
        python3-dev \
        default-libmysqlclient-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

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

RUN poetry install

COPY . .

EXPOSE 8000
ENTRYPOINT [ "sh", "-c" ]
CMD [ "./docker-entrypoint.sh" ]
