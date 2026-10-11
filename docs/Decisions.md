# Decisions

A log of decisions and why we made them. Newest at the bottom. To change a decision, add a new entry that
replaces the old one (mark the old one *Superseded by D-xx*) instead of editing history.

| # | Date | Decision | Why |
|---|---|---|---|
| D-01 | 2026-10-11 | **Four phases:** profile → job profile → selection → CV generation, each with a user review/edit step | The user stays in control. Review steps also guard against made-up content (Security.md S1) |
| D-02 | 2026-10-11 | **One way of doing each thing** for now (one input path, one template, one output format). Extend later | Keeps scope manageable. The MVP grows as we go |
| D-03 | 2026-10-11 | **Input: PDF upload or pasted text only.** No web scraping | Scraping is fragile, often blocked, and has terms-of-service issues |
| D-04 | 2026-10-11 | **Local-first storage:** personal data lives in the browser (IndexedDB) with export/import. The backend is stateless apart from the course cache and usage counts | Privacy, simpler legal obligations, no accounts needed. See Privacy.md |
| D-05 | 2026-10-11 | **No accounts at launch** | Follows from D-04. Can add later (ideally with end-to-end encrypted sync) |
| D-06 | 2026-10-11 | **Data models: free-text body + thin structured envelope** (id, type, dates, notes) | The LLM reads text. Code needs a few fields to sort, route and reference. See DataModels.md |
| D-07 | 2026-10-11 | **LLM selects items by ID; code copies facts** (titles, organizations, dates). The LLM only writes bullets and summaries | Cheaper re-runs, grounded output, less room for invented content |
| D-08 | 2026-10-11 | **Output engine: Typst, compiled in the browser** (typst.ts / WASM) | CVs never reach the server for rendering. Zero server compute. Fast re-renders |
| D-09 | 2026-10-11 | **Backend: Python + FastAPI** | Best ecosystem for PDF parsing and LLM tooling |
| D-10 | 2026-10-11 | **Frontend: Next.js** | Polished UI for the public launch. Can be mostly static because of D-04/D-08 |
| D-11 | 2026-10-11 | **Database: MySQL** (charset `utf8mb4`) | Personal choice, to learn it. The server stores little, so any SQL database works. `utf8mb4` is required for accents and other non-ASCII text |
| D-12 | 2026-10-11 | **No vector index** | A profile (~20–100 items) fits in one LLM context. Revisit if that changes |
| D-13 | 2026-10-11 | **LLM provider: Infomaniak**, behind a provider interface with a dummy implementation for development/tests | Swiss hosting fits the privacy pitch. The dummy allows development without spending tokens |
| D-14 | 2026-10-11 | **Hosting: Infomaniak** | Same provider, Swiss data location |
| D-15 | 2026-10-11 | **Monetization: donations.** Show the compute cost at the end, with an optional payment and tip | Low friction for students. Needs abuse controls (Security.md S2) |
| D-16 | 2026-10-11 | **Target users: Master's graduates / students** | Defaults: education first, courses and thesis prominent |
| D-17 | 2026-10-11 | **Languages: FR / DE / EN** for both the UI and the generated CVs. CV language follows the job posting | Swiss market |
| D-18 | 2026-10-11 | **No photo on the CV** for now | Possible later addition (common in CH/DE) |
| D-19 | 2026-10-11 | **Open-source repository** | Transparency backs up the privacy claims. Good for the LinkedIn launch |
| D-20 | 2026-10-11 | **License: AGPL-3.0** | Anyone hosting a modified version as a service must publish their changes, so the project can't be turned into a closed competitor |
| D-21 | 2026-10-11 | **LLM JSON output: schema in the prompt + Pydantic validation + one retry.** API-level JSON mode is behind a flag (`LLM_JSON_MODE`), off by default | Works with any provider. See open question O-01 |

## Open questions

| # | Question | Notes |
|---|---|---|
| O-01 | Does Infomaniak's API support `response_format` (JSON mode or JSON schema) for the models we'll use? | If yes, set `LLM_JSON_MODE=true` and compare failure rates. Validation stays either way (Security.md S1) |
| O-02 | Extract PDF text in the browser (pdf.js) instead of the backend? | Fits local-first: only text reaches the server, and server-side upload risks (Security.md S3) go away |
| O-03 | Generate the frontend's TypeScript types from the backend's OpenAPI schema? | Removes the hand-kept copy in `frontend/src/lib/api.ts` |
