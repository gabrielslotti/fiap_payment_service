#!/bin/sh

# Run migrations
uv run alembic upgrade head

# Start the application
uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT
