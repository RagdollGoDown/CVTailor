# CVTailor

Tailor your CV to each job application, from everything you've done. Your data stays in your browser.

1. **Your background**: add jobs, courses, projects and letters (PDF or pasted text).
2. **The job**: paste the job description, and get a profile of what the role is looking for.
3. **The match**: review which experience is highlighted, and steer it with notes.
4. **Your CV**: a tailored CV generated with [Typst](https://typst.app), rendered in the browser.

Design notes live in [`docs/`](docs/): [Decisions](docs/Decisions.md), [Data models](docs/DataModels.md),
[Security](docs/Security.md), [Privacy](docs/Privacy.md). How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md).

## Structure

```
api/        Laravel REST API: replaces backend/ as the port progresses
backend/    FastAPI: LLM calls (stateless), course cache, usage tracking
frontend/   Next.js: the app; personal data is stored in the browser
docs/       Living design documents
docker-compose.yml   Development stack: MariaDB, plus PHP-FPM and nginx for api/
```

The backend is being ported to Laravel with MariaDB ([Decisions D-24 to D-28](docs/Decisions.md)).
Until the port is finished, `backend/` is the FastAPI app that the frontend uses, and `api/` grows next to it.

## Development

Requirements: Docker, Python 3.12+, Node 20+. The Laravel API runs entirely in Docker, so PHP is not needed locally.

```bash
# Laravel API: http://localhost:8080 (health check at /api/health). Run from the repository root.
cp api/.env.example api/.env
docker compose up -d --build --wait              # MariaDB, PHP-FPM, nginx
docker compose exec php composer install
docker compose exec php php artisan key:generate
docker compose exec php php artisan migrate
docker compose exec php composer check           # Pint + Larastan + Pest
docker compose exec php composer format          # fix formatting

# Database only, for the FastAPI backend
docker compose up -d --wait db

# Backend: http://localhost:8000 (API docs at /docs)
cd backend
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
cp .env.example .env                 # LLM_PROVIDER=dummy by default: no API key, no cost
.venv/bin/python -m app.init_db      # create tables
.venv/bin/uvicorn app.main:app --reload
.venv/bin/pytest                     # tests
.venv/bin/ruff check . && .venv/bin/ruff format .

# Frontend: http://localhost:3000
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

## License

[AGPL-3.0](LICENSE)
