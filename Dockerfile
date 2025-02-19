FROM python:3.10-alpine

# Install dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    libpq

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY ./app /src/app
COPY ./alembic /src/alembic
COPY alembic.ini entrypoint.sh pyproject.toml uv.lock /src/

# Install the application dependencies.
WORKDIR /src
RUN uv sync --frozen --no-cache

# Run the application.
RUN chmod +x /src/entrypoint.sh
CMD ["./entrypoint.sh"]
