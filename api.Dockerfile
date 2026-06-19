FROM python:3.12-slim-bookworm AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app


FROM base AS build-stage

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements & install dependencies.
COPY ./requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip wheel \
    && python -m pip wheel --no-cache-dir --wheel-dir /wheels \
    -r /app/requirements.txt


FROM base AS runtime-deps-stage

# Install runtime dependencies.
RUN apt-get update && apt-get install --no-install-recommends -y \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build-stage /wheels /wheels
COPY --from=build-stage /app/requirements.txt /app/requirements.txt

RUN python -m pip install --no-index /wheels/* \
    && rm -rf /wheels /app/requirements.txt


FROM runtime-deps-stage AS run-stage

ENV USER=tribunal
ENV GROUP=tribunal

# Create user with limited permissions.
RUN addgroup --gid 10001 --system ${GROUP} && \
    adduser --no-create-home --shell /bin/false \
    --disabled-password --uid 10001 --system --group ${USER}

# Copy gunicorn config.
COPY --chown=${USER}:${GROUP} ./etc/gunicorn.conf.py /etc/gunicorn.conf.py
RUN sed -i "s/\r$//g" /etc/gunicorn.conf.py

# Copy alembic config.
COPY --chown=${USER}:${GROUP} ./etc/alembic.ini /etc/alembic.ini
RUN sed -i "s/\r$//g" /etc/alembic.ini

# Copy application files.
COPY --chown=${USER}:${GROUP} ./src/python/url_tribunal/ /app/url_tribunal/

ENV PYTHONPATH=/app

# Switch to created user.
USER ${USER}

EXPOSE 8000

CMD [ "gunicorn", "-c", "/etc/gunicorn.conf.py", "url_tribunal.api.main:app" ]