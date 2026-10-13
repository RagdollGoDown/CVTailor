# AGENTS.md

Instructions for AI coding agents working on this repository. Humans: see [CONTRIBUTING.md](CONTRIBUTING.md).

CVTailor tailors a CV to a job posting in four phases: background → job profile → selection → Typst CV.
Personal data lives in the browser. The backend handles LLM calls and stores no personal data.

## Read before designing anything

- [docs/Decisions.md](docs/Decisions.md): what is decided and why. Don't contradict it silently.
- [docs/DataModels.md](docs/DataModels.md), [docs/Security.md](docs/Security.md), [docs/Privacy.md](docs/Privacy.md): read the one(s) your change touches.

## Layout and commands

```
api/        Laravel 13 (PHP 8.5)     docker compose exec php composer check   (from the repo root, stack running; `composer format` fixes style)
backend/    FastAPI (Python 3.12+)   cd backend && .venv/bin/pytest && .venv/bin/ruff check . && .venv/bin/ruff format .
frontend/   Next.js 16 + Tailwind    cd frontend && npm run lint && npm run build   (read frontend/AGENTS.md first)
docs/       Living design documents
```

Run the checks for every part you touched before committing. CI runs the same checks.

The backend is being ported to Laravel (Decisions.md D-24 to D-28), one issue at a time. Until the port is finished,
`backend/` is FastAPI and the rules below that name Python tools still apply to it. New backend code goes in `api/`.
Don't port code outside the issue you work on. PHP and Composer run inside the `php` container (`docker compose exec php …`), not on the host.

## Rules

- **Privacy:** never store personal data server-side, and never log request bodies (Privacy.md).
- **LLM calls:** go through `complete_structured` with a Pydantic response model. Untrusted text goes inside delimiters (Security.md S1).
- **Grounding:** facts (titles, organizations, dates) are copied by code. The LLM only selects by ID and writes prose.
- **Typst:** content is passed as JSON data, never by building markup from strings (Security.md S4).
- **Docs stay current:** a new decision adds a row to Decisions.md. A security or privacy impact updates those files in the same PR.
- **Tests:** new behaviour comes with tests. Use the dummy LLM provider in tests, never a real API.
- Match the surrounding code style. Keep changes scoped to the issue.

## Workflow

1. Work on **one GitHub issue** at a time. Branch from `main`: `<type>/<issue-number>-<short-slug>`, e.g. `feat/12-profile-storage`.
2. Make **small commits** in [Conventional Commits](https://www.conventionalcommits.org) style (`feat(backend): …`, `fix(frontend): …`, `docs: …`, `test: …`, `ci: …`).
   Each commit should pass the checks on its own.
3. Open a **pull request** that fills in `.github/pull_request_template.md`. The "How it works" section matters most:
   the maintainer reviews PRs to learn, so explain the concepts and the reasoning, not just the changes.
4. **Never push to `main` and never merge.** The maintainer reviews and merges.
5. If the issue needs a decision that the docs don't cover, stop and ask (or say so in the PR) instead of guessing.
