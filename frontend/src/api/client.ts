import createClient from "openapi-fetch";
import type { paths } from "./generated/schema";

export const apiClient = createClient<paths>({
  baseUrl: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
  credentials: "include",
});

let accessToken: string | null = null;

export function setAccessToken(token: string | null) {
  accessToken = token;
}

export function getAccessToken() {
  return accessToken;
}

export function authHeaders() {
  return accessToken
    ? { Authorization: `Bearer ${accessToken}` }
    : {};
}

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

async function refreshAccessToken(): Promise<boolean> {
  const { data, error } = await apiClient.POST("/auth/refresh-jwt");

  if (error || !data?.access_token) {
    setAccessToken(null);
    return false;
  }

  setAccessToken(data.access_token);
  return true;
}

export async function initializeAuth(): Promise<boolean> {
  return refreshAccessToken();
}

export async function authGet<Path extends keyof paths>(
  path: Path,
  options: any = {}
) {
  let result = await apiClient.GET(path as any, {
    ...options,
    headers: {
      ...options.headers,
      ...authHeaders(),
    },
  });

  if (result.response.status !== 401) {
    return result;
  }

  const refreshed = await refreshAccessToken();

  if (!refreshed) {
    return result;
  }

  return apiClient.GET(path as any, {
    ...options,
    headers: {
      ...options.headers,
      ...authHeaders(),
    },
  });
}

export async function authPost<Path extends keyof paths>(
  path: Path,
  options: any = {}
) {
  let result = await apiClient.POST(path as any, {
    ...options,
    headers: {
      ...options.headers,
      ...authHeaders(),
    },
  });

  if (result.response.status !== 401) {
    return result;
  }

  const refreshed = await refreshAccessToken();

  if (!refreshed) {
    return result;
  }

  return apiClient.POST(path as any, {
    ...options,
    headers: {
      ...options.headers,
      ...authHeaders(),
    },
  });
}

export async function authDelete<Path extends keyof paths>(
  path: Path,
  options: any = {}
) {
  let result = await apiClient.DELETE(path as any, {
    ...options,
    headers: {
      ...options.headers,
      ...authHeaders(),
    },
  });

  if (result.response.status !== 401) {
    return result;
  }

  const refreshed = await refreshAccessToken();

  if (!refreshed) {
    return result;
  }

  return apiClient.DELETE(path as any, {
    ...options,
    headers: {
      ...options.headers,
      ...authHeaders(),
    },
  });
}
