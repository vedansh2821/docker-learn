# docker-learn

A small hands-on repo for learning Docker: a tiny Python web app in a
container, backed by Redis, run locally with Docker Compose and deployed
with a `Dockerfile` on Render. It is a learning project, not a product.

## What it teaches

- Writing a `Dockerfile` — slim base image, layer caching (install
  dependencies before copying app code), running as a non-root user.
- Wiring two containers together with Docker Compose, including a Redis
  `healthcheck` and `depends_on: condition: service_healthy`.
- Configuration through environment variables (`.env`, `APP_GREETING`,
  `REDIS_URL`) and keeping secrets out of the image with `.dockerignore`.
- CI: every push builds the image and scans it with Trivy
  (`.github/workflows/docker-ci.yml`).
- Deploying a containerised app with `render.yaml`.

## Prerequisites

- Docker with Docker Compose v2 (for the recommended path), or
- Python 3.13 for the no-Docker path.

## Run it

### With Compose (recommended — app + Redis)

```bash
cp .env.example .env
docker compose up --build
```

Open <http://localhost:8000> — you should see something like:

```text
Hello from Compose! Visit #1
```

Refresh and the visit counter goes up; the count is stored in Redis, so
it survives app restarts. Stop with `Ctrl+C`, and
`docker compose down -v` to also remove the Redis data volume.

### With plain Docker (no Redis)

```bash
docker build -t docker-learn .
docker run --rm -p 8000:8000 docker-learn
```

Without Redis reachable, the app falls back to an in-memory visit
counter (see `redis_store.py`), so the container still answers on
<http://localhost:8000>. For the real persistent counter, run it with
Compose or point `REDIS_URL` at a Redis instance:

```bash
docker run --rm -p 8000:8000 -e REDIS_URL=redis://<host>:6379 docker-learn
```

### Without Docker

```bash
pip install -r requirements.txt
python app.py
```

The app listens on `PORT` (default `8000`). If no Redis is reachable at
`REDIS_URL` (default `redis://redis:6379`), it uses the in-memory
fallback counter.

## How it works

Every `GET /` returns `{APP_GREETING} Visit #{n}`, where `n` comes from
`INCR visit_count` in Redis.

## Files

| File | What it does |
| --- | --- |
| `Dockerfile` | Builds the app image: `python:3.13-slim`, non-root `appuser`, installs `requirements.txt`, runs `python app.py` on port 8000. |
| `app.py` | Stdlib `http.server` app. Serves the greeting + visit count on `GET /`. No web framework. |
| `redis_store.py` | Redis client + `get_visit_count()`. Falls back to an in-memory counter if Redis is unreachable. |
| `requirements.txt` | Single dependency: `redis==5.2.1` (the only import outside the stdlib). |
| `compose.yaml` | `web` (built from `.`) + `redis:7-alpine` with a healthcheck; maps `8000:8000`; persists Redis data in a named volume. |
| `render.yaml` | Render blueprint: deploys the repo as a Docker web service (free plan, health check on `/`). |
| `.env.example` | Example env vars for Compose: `APP_GREETING`, `REDIS_URL`. Copy to `.env` (git-ignored, never commit a real one). |
| `.dockerignore` | Keeps `__pycache__`, virtualenvs, `.env` and `.git` out of the image. |
| `.github/workflows/docker-ci.yml` | CI: `docker build` on every push/PR, then a Trivy scan (CRITICAL/HIGH, non-blocking). |

## Notes

- The Docker build was not run locally in this environment (no Docker
  daemon here); the GitHub Actions workflow builds the image on every
  push, which is the verification for the `Dockerfile`.
- Nothing here is employer code — this is a personal learning repo.
