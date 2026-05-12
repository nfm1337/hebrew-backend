# Hebrew Learning Backend

AI-powered backend for a Hebrew vocabulary learning app. Generates personalized Hebrew texts at the user's level using Claude, with spaced repetition for vocabulary retention.

## Stack

- **FastAPI** + **SQLModel** + **asyncpg** (PostgreSQL)
- **Anthropic Claude** via `instructor` for structured Hebrew text generation
- **Alembic** for migrations
- **uv** for dependency management

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Docker + Docker Compose

## Setup

```bash
git clone https://github.com/nfm1337/hebrew-backend
cd hebrew-backend
uv sync
cp .env.example .env  # fill in your values
```

`.env` variables:

```
PORT=8000
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=hebrew_db
POSTGRES_PORT=5432
ANTHROPIC_API_KEY=sk-ant-...
```

## Running locally

Start the database:

```bash
docker compose up db -d
```

Run migrations:

```bash
uv run alembic upgrade head
```

Start the API:

```bash
uv run uvicorn hebrew_backend.main:app --reload --port 8000
```

API docs available at `http://localhost:8000/docs`.

## Running with Docker

```bash
docker compose up -d
```

Migrations run automatically on container start.

## Linting and type checking

```bash
uv run ruff check .
uv run mypy src/
```

## Eval Results

Baseline results (20 test cases, 3 levels × 6 topics):

| Model                                    | Level ↑ | Topic ↑ | Grammar ↑ | All pass ↑ |
| ---------------------------------------- | ------- | ------- | --------- | ---------- |
| anthropic/claude-sonnet-4-6              | 90%     | 55%     | 100%      | 50%        |
| openrouter/google/gemma-4-31b-it         | 90%     | 30%     | 100%      | 30%        |
| openrouter/google/gemini-3-flash-preview | 42%     | 42%     | 95%       | 11%        |

Judge: `openrouter/qwen/qwen-2.5-72b-instruct`
