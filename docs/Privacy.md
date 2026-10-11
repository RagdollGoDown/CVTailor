# Privacy

Living document. Most decisions here are really about **where each piece of data lives**.

## Guiding principle: local-first

The user's personal data (profile, job targets, generated CVs) lives **on the user's device**.
The backend is mostly stateless: it receives what a single LLM call needs, returns the result, and forgets it.

This is also the pitch: *"Your CV data never leaves your browser except for the AI call, which runs on Swiss infrastructure."*
The claim must stay true. If an architecture change breaks it, update this file and the public wording.

## Data inventory

| Data | Stored where | Sent to backend? | Kept on server? |
|---|---|---|---|
| Experience items (jobs, courses, activities…) | Browser (IndexedDB) + export file | Yes, during LLM calls | **No** |
| Uploaded PDFs (letters, course descriptions) | Not stored. Text is extracted, then discarded | Yes, for text extraction | **No** (deleted after the request) |
| Job descriptions / job profiles | Browser | Yes, during LLM calls | **No** |
| User notes to the LLM | Browser | Yes, during LLM calls | **No** |
| Generated CVs (content JSON + PDF) | Browser | Content JSON: only during the generation/regeneration call. PDF: never (compiled in the browser) | **No** |
| Course cache entries | Server | — | **Yes**: public course content only (see open question Q1) |
| Usage records (token counts, cost) | Server | — | Yes: no content, only counts, timestamp, and anonymous session ID |
| Payment / donation info | Payment provider | — | Not by us |

## Rules

- **No request bodies in logs.** Log only metadata: endpoint, duration, token count, status.
- Error reporting (if we add Sentry or similar) must strip request payloads.
- Uploaded files are processed in memory or a temp directory and deleted at the end of the request.
- The LLM provider sees the content. **Check Infomaniak's AI terms**: data retention, use for training, data location. (To do.)

## Trade-offs of local-first

- **Data lost if the browser storage is cleared.** Mitigation: a clear "Export profile" / "Import profile" (JSON file),
  and maybe a reminder after big edits.
- **No sync between devices.** Acceptable for the MVP. If accounts come later, consider *end-to-end encrypted* sync,
  so the server stores only data it can't read and the pitch stays true.
- **No accounts needed at launch.** This removes password storage, account deletion flows, etc.
- Abuse control can't rely on accounts → see Security.md S2.

## Legal (Switzerland nFADP / EU GDPR)

Even without storing anything, we still *process* personal data (it passes through our server and the LLM provider), so we need:
- [ ] A short, readable privacy policy page: what is sent where, how long it's kept, which providers are used (hosting, LLM, payment).
- [ ] Information on the course cache, if user-submitted content is ever cached.
- [ ] Note: recommendation letters contain personal data about **third parties** (the writer). Another reason not to store them.

## Open questions

- **Q1 — Course cache vs. privacy.** We cache by hash of the course text. But how do we know the pasted text is a *public* course
  description and not something private? Options: (a) only cache items of type "course", (b) an explicit
  "share this course description to help others" checkbox, (c) only cache the generic course summary, never user-specific
  parts (grade, personal project). Probably (b) + (c).
- ~~Q2 — Where does Typst compile?~~ **Resolved (Decisions D-08):** in the browser. The generated CV never reaches the server.
- **Q3 — Infomaniak AI data terms.** To verify before launch.
