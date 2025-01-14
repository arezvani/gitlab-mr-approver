ARG PYTHON_VERSION=$PYTHON_VERSION

FROM python:$PYTHON_VERSION-slim as builder

ARG OS_PACKAGES=$OS_PACKAGES
ARG DOCKERFILE_PATH=$DOCKERFILE_PATH

ENV PIP_DEFAULT_TIMEOUT=1000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    DOCKERFILE_PATH=$DOCKERFILE_PATH \
    OS_PACKAGES=$OS_PACKAGES

RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update && \
    apt-get install -y --no-install-recommends `echo $OS_PACKAGES | sed 's+,+ +g'`

RUN groupadd -g 1001 app && \
    useradd -r -u 1001 -g app app

RUN mkdir -p /opt/app/src && chown -R app:app /opt/app/src
RUN mkdir -p /opt/app/utils && chown -R app:app /opt/app/utils
RUN mkdir -p /opt/app/config && chown -R app:app /opt/app/config

COPY --chown=app:app $DOCKERFILE_PATH/requirements.txt .

RUN pip install --no-cache -r requirements.txt

COPY --chown=app:app utils /opt/app/utils
COPY --chown=app:app config/ws_logger.py /opt/app/config/ws_logger.py
COPY --chown=app:app config/base_logger.py /opt/app/config/base_logger.py

WORKDIR /opt/app/src

COPY --chown=app:app src .

USER 1001

ENTRYPOINT /usr/local/bin/gunicorn --workers 4 --bind 0.0.0.0:8000 wsgi:app