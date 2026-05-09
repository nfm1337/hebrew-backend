#!/bin/sh
set -e

uv run --no-dev alembic upgrade head
exec uv run --no-dev uvicorn hebrew_backend.main:app --host 0.0.0.0 --port "${PORT:-8000}"
