# Data Models

Living document. Field lists are drafts and will change.

## Guiding principle: text first, with a thin envelope

Most content is used as **context for the LLM**, so the main body of each item is free text (Markdown).
Around that text sits a small set of structured fields. These are needed for things the LLM shouldn't do or can't do reliably:

- **`id`**: lets the LLM *select* items by reference instead of copying text (cheaper, and no invented content; see Security.md S1).
- **`type`**: decides which CV section an item goes in (Experience, Education, …).
- **dates**: for sorting chronologically and "most recent first" without trusting the LLM.
- **`user_notes`**: user guidance the LLM should take into account.

Rule: if code needs to read a field (sort, filter, route to a template section), make it structured.
If only the LLM reads it, free text is fine.

## Pipeline overview

```
Phase 1  inputs (PDF / pasted text) ──LLM extract──▶ ExperienceItem[]        (user reviews & edits)
Phase 2  job description            ──LLM extract──▶ JobProfile              (user reviews & edits)
Phase 3  ExperienceItem[] + JobProfile ──LLM select──▶ Selection             (user reviews, adds notes, re-runs)
Phase 4  Selection + items + JobProfile ──LLM write──▶ CVContent ──Typst──▶ PDF   (user edits / regenerates)
```

Each phase result is saved, so going back to a phase never re-runs earlier phases.

## Models (on the user's device unless noted)

### Profile
```
Profile {
  personal: { name, email, phone, location, links[], photo? }   // filled in by hand, never sent to the LLM unless needed
  items: ExperienceItem[]
  schema_version: int                                         // for migrating exported files
}
```

### ExperienceItem
```
ExperienceItem {
  id: uuid
  type: "job" | "education" | "course" | "project" | "extracurricular" | "award" | "recommendation" | "other"
  title: string                   // "Software Engineering Intern", "Machine Learning (CS-433)"
  organization?: string
  start_date?: "YYYY-MM"          // partial dates allowed
  end_date?: "YYYY-MM" | "present"
  body: markdown                  // main content: what was done, learned, achieved
  skills: string[]                // extracted by the LLM, editable
  user_notes?: string             // "Emphasize the leadership part", "Don't mention for finance jobs"
  source?: { kind: "pdf" | "paste", filename?, course_cache_key? }
  created_at, updated_at
}
```
A `recommendation` item can point to the item(s) it supports (`related_item_ids`), e.g. a letter from an internship manager.

### JobProfile
```
JobProfile {
  id: uuid
  company: string
  role: string
  language: "en" | "fr" | "de" | ...    // language the CV should be written in
  summary: markdown                    // what the role is about
  required_skills: string[]
  nice_to_have: string[]
  keywords: string[]                   // terms to reuse literally (applicant-tracking filters)
  tone?: string                        // "corporate", "startup", "academic"
  raw_text: string                     // the original posting, kept locally for re-runs
  user_notes?: string                  // "I really want to highlight my teaching experience"
}
```

### Selection (phase 3 result)
```
Selection {
  job_profile_id
  picks: { item_id, relevance: 1-5, reason: string, emphasis?: string }[]
  excluded: { item_id, reason }[]      // shown to the user, who can bring them back
  user_overrides: { item_id, action: "force_include" | "force_exclude" }[]
  user_notes?: string                  // global notes for the next re-run
}
```
Re-running selection is cheap: the input is item summaries and the output is IDs and short reasons.

### CVContent (phase 4 result, input to Typst)
```
CVContent {
  language
  headline?: string
  summary?: string
  sections: {
    kind: "experience" | "education" | "projects" | "skills" | "activities" | ...
    entries: {
      source_item_id                    // grounding: every entry points to a real item
      title, organization, dates        // copied from the item by code, not written by the LLM
      bullets: string[]                 // written by the LLM, editable by the user
    }[]
  }[]
  template_id: string
}
```
- Facts (titles, organizations, dates) are copied by **code**. The LLM only writes bullets, summary and headline.
- The user can edit any text directly (free) or ask for one section to be regenerated with a note (cheap), instead of regenerating the whole CV.
- Typst receives this as JSON data, never as string-built markup (Security.md S4).

### Application (ties it together)
```
Application {
  id, job_profile_id, selection, cv_versions: CVContent[]   // keep history so the user can compare / go back
  created_at
}
```

## Server-side models

### CourseCacheEntry
```
CourseCacheEntry {
  key: sha256(normalized_text) + ":" + extraction_prompt_version
  title, institution?, body: markdown, skills: string[]
  created_at, hit_count
}
```
Normalization: lowercase, collapse whitespace, remove page headers and footers where possible. See Privacy.md Q1 on what is allowed in here.

### UsageRecord
```
UsageRecord { session_id, endpoint, model, input_tokens, output_tokens, cost_chf, created_at }
```
Feeds the "your compute cost" display and the global budget cap. No content.

## Open questions

- Do we need a vector index? **Not for now.** A profile is ~20–100 items, which fits in one LLM context.
  Revisit if profiles get much larger or if we want semantic search over the course cache.
- Should `body` length be capped per item, to control token cost?
- How to migrate exported profile files when the schema changes → `schema_version` + migration functions.
