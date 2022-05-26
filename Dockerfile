FROM python:3.9-slim-buster

# python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # flask
    FLASK_APP=movies/entrypoints/flask_app.py \
    FLASK_TEST=1 \
    PYTHONUNBUFFERED=1 \
    # config
    DB_NAME=movies \
    DB_HOST=db \
    DB_PORT=5432 \
    DB_USER=movies \
    DB_PASS=abc123

RUN apt-get update \
    && apt-get install --no-install-recommends -y libpq5

# dev system utilities
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
	less htop inetutils-ping strace curl postgresql-client unzip

# Wait for it
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.5.0/wait /wait
RUN chmod +x /wait

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src

COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests/

WORKDIR /src
CMD /wait && flask run --host=0.0.0.0 --port=80
