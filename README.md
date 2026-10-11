# CVTailor

Tailor your CV to each job application, from everything you've done. Your data stays in your browser.

1. **Your background**: add jobs, courses, projects and letters (PDF or pasted text).
2. **The job**: paste the job description, and get a profile of what the role is looking for.
3. **The match**: review which experience is highlighted, and steer it with notes.
4. **Your CV**: a tailored CV generated with [Typst](https://typst.app), rendered in the browser.

Design notes live in [`docs/`](docs/): [Decisions](docs/Decisions.md), [Data models](docs/DataModels.md),
[Security](docs/Security.md), [Privacy](docs/Privacy.md).

## Structure

```
backend/    FastAPI: LLM calls (stateless), course cache, usage tracking
frontend/   Next.js: the app; personal data is stored in the browser
docs/       Living design documents
docker-compose.yml   MySQL for development
```

## Development

Requirements: Python 3.12+, Node 20+, Docker.

```bash
# Database (only needed for features that use it)
docker compose up -d --wait

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
