FROM python:3.13-slim as builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

RUN pip install --no-cache-dir .

COPY src/ src/
RUN uv sync --frozen --no-dev

EXPOSE 8000
CMD ["uvicorn", "hebrew_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
