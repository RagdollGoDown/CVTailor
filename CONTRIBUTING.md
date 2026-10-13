# Contributing

Development setup is in the [README](README.md). Design documents are in [docs/](docs/).

## How work flows

1. Every change starts from a **GitHub issue** (use the "Task" template). An issue says what to build, links to the relevant docs,
   and lists acceptance criteria.
2. The work happens on a **branch** named `<type>/<issue-number>-<short-slug>`, e.g. `feat/12-profile-storage`.
3. Commits follow [Conventional Commits](https://www.conventionalcommits.org): `<type>(<scope>): <summary>`.
   Types: `feat`, `fix`, `refactor`, `test`, `docs`, `build`, `ci`, `chore`. Scopes: `backend`, `frontend`, `docs`, …
4. A **pull request** closes the issue. CI must pass. The maintainer reviews and merges, usually with a squash or rebase merge.

AI agents follow the same flow. Their rules are in [AGENTS.md](AGENTS.md).
