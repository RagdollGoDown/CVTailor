"use client";

import { useState } from "react";

import { ApiError, extractItems, type ExtractItemsResponse } from "@/lib/api";

export default function ExtractDemo() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<ExtractItemsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      setResult(await extractItems(text));
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Could not reach the server.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <form onSubmit={onSubmit} className="space-y-3">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste a course description, a job you held, a letter of recommendation…"
          rows={6}
          className="w-full rounded-lg border border-border bg-surface p-3 text-sm outline-none focus:ring-2 focus:ring-accent"
        />
        <button
          type="submit"
          disabled={loading || !text.trim()}
          className="rounded-lg bg-accent px-4 py-2 text-sm font-medium text-white transition hover:opacity-90 disabled:opacity-40"
        >
          {loading ? "Extracting…" : "Extract experience"}
        </button>
      </form>

      {error && <p className="text-sm text-red-600">{error}</p>}

      {result && (
        <div className="space-y-3">
          {result.items.map((item, i) => (
            <article key={i} className="rounded-lg border border-border bg-surface p-4">
              <div className="flex items-baseline justify-between gap-4">
                <h3 className="font-medium">{item.title}</h3>
                <span className="text-xs uppercase tracking-wide text-muted">{item.type}</span>
              </div>
              <p className="text-sm text-muted">
                {[item.organization, [item.start_date, item.end_date].filter(Boolean).join(" – ")]
                  .filter(Boolean)
                  .join(" · ")}
              </p>
              <p className="mt-2 text-sm">{item.body}</p>
              {item.skills.length > 0 && (
                <ul className="mt-3 flex flex-wrap gap-1.5">
                  {item.skills.map((skill) => (
                    <li key={skill} className="rounded-full bg-accent/10 px-2 py-0.5 text-xs text-accent">
                      {skill}
                    </li>
                  ))}
                </ul>
              )}
            </article>
          ))}
          <p className="text-xs text-muted">
            {result.usage.input_tokens + result.usage.output_tokens} tokens used
          </p>
        </div>
      )}
    </div>
  );
}
