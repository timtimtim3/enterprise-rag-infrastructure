import createClient from "openapi-fetch";
import type { paths } from "./generated/schema";

export const apiClient = createClient<paths>({
  baseUrl: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
  credentials: "include",
});

export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public body?: unknown
  ) {
    super(message);
    this.name = "ApiError";
  }
}

function getErrorMessage(error: unknown): string {
  if (
    error &&
    typeof error === "object" &&
    "detail" in error
  ) {
    const detail = error.detail;

    if (typeof detail === "string") {
      return detail;
    }

    if (Array.isArray(detail)) {
      return detail.map((item) => item.msg).join(", ");
    }
  }

  return "Request failed";
}

export function throwApiError(error: unknown): never {
  throw new ApiError(
    getErrorMessage(error),
    undefined,
    error
  );
}
