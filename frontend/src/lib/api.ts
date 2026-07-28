import type { AnalysisResponse, Report, UploadResult } from "./types";

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export function errorMessage(err: unknown, fallback: string): string {
  if (err instanceof Error && err.message) return err.message;
  return fallback;
}

export function getToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("lensecode_token");
  }
  return null;
}

const TOKEN_EVENT = "lensecode_token_change";

function notifyTokenChange() {
  if (typeof window !== "undefined") {
    window.dispatchEvent(new Event(TOKEN_EVENT));
  }
}

export function setToken(token: string) {
  localStorage.setItem("lensecode_token", token);
  notifyTokenChange();
}

export function clearToken() {
  localStorage.removeItem("lensecode_token");
  notifyTokenChange();
}

export function subscribeToken(callback: () => void): () => void {
  if (typeof window === "undefined") return () => {};
  window.addEventListener("storage", callback);
  window.addEventListener(TOKEN_EVENT, callback);
  return () => {
    window.removeEventListener("storage", callback);
    window.removeEventListener(TOKEN_EVENT, callback);
  };
}

async function readDetail(res: Response, fallback: string): Promise<string> {
  try {
    const data = await res.json();
    if (typeof data?.detail === "string") return data.detail;
  } catch {
    // JSON okunamadi, varsayilan mesaji kullan
  }
  return fallback;
}

export async function login(password: string): Promise<string> {
  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password }),
  });
  if (!res.ok) throw new ApiError(await readDetail(res, "Şifre yanlış"), res.status);
  const data = (await res.json()) as { token: string };
  setToken(data.token);
  return data.token;
}

function authHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function uploadZip(file: File): Promise<UploadResult> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("/api/upload/zip", {
    method: "POST",
    headers: authHeaders(),
    body: form,
  });
  if (!res.ok) {
    if (res.status === 401) {
      clearToken();
      window.location.reload();
    }
    throw new ApiError(await readDetail(res, "Yükleme başarısız"), res.status);
  }
  return res.json();
}

export async function uploadGithub(url: string): Promise<UploadResult> {
  const res = await fetch("/api/upload/github", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ url }),
  });
  if (!res.ok) throw new ApiError(await readDetail(res, "GitHub yükleme başarısız"), res.status);
  return res.json();
}

export async function uploadPaste(code: string, filename?: string): Promise<UploadResult> {
  const res = await fetch("/api/upload/paste", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ code, filename: filename || "paste.txt" }),
  });
  if (!res.ok) throw new ApiError(await readDetail(res, "Kod yükleme başarısız"), res.status);
  return res.json();
}

export async function analyzeProject(projectId: string): Promise<AnalysisResponse> {
  const res = await fetch("/api/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ project_id: projectId }),
  });
  if (!res.ok) throw new ApiError(await readDetail(res, "Analiz başarısız"), res.status);
  return res.json();
}

export async function getReport(projectId: string): Promise<Report> {
  const res = await fetch("/api/report", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ project_id: projectId }),
  });
  if (res.status === 401) {
    clearToken();
    throw new ApiError("Oturum süresi doldu", 401);
  }
  if (!res.ok) {
    const detail = await readDetail(res, "Rapor alınamadı");
    throw new ApiError(detail, res.status);
  }
  return res.json();
}
