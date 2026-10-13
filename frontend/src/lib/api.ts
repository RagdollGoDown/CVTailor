// Mirrors backend/app/schemas.py. Keep in sync until we generate these types from the OpenAPI schema.

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type ItemType =
  | "job"
  | "education"
  | "course"
  | "project"
  | "extracurricular"
  | "award"
  | "recommendation"
  | "other";

export interface ExperienceItemDraft {
  type: ItemType;
  title: string;
  organization: string | null;
  start_date: string | null;
  end_date: string | null;
  body: string;
  skills: string[];
}

export interface Usage {
  input_tokens: number;
  output_tokens: number;
}

export interface ExtractItemsResponse {
  items: ExperienceItemDraft[];
  usage: Usage;
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    throw new ApiError(response.status, typeof detail?.detail === "string" ? detail.detail : "Request failed");
  }
  return response.json();
}

export function extractItems(text: string, typeHint?: ItemType): Promise<ExtractItemsResponse> {
  return post("/api/items/extract", { text, type_hint: typeHint ?? null });
}
