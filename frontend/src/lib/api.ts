export function getToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("lensecode_token");
  }
  return null;
}

export function setToken(token: string) {
  localStorage.setItem("lensecode_token", token);
}

export function clearToken() {
  localStorage.removeItem("lensecode_token");
}

export async function login(password: string): Promise<string> {
  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password }),
  });
  if (!res.ok) throw new Error("Şifre yanlış");
  const data = await res.json();
  setToken(data.token);
  return data.token;
}

function authHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function uploadZip(file: File): Promise<{ project_id: string }> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("/api/upload/zip", {
    method: "POST",
    headers: authHeaders(),
    body: form,
  });
  if (!res.ok) {
    if (res.status === 401) { clearToken(); window.location.reload(); }
    throw new Error("Yükleme başarısız");
  }
  return res.json();
}

export async function uploadGithub(url: string): Promise<{ project_id: string }> {
  const res = await fetch("/api/upload/github", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ url }),
  });
  if (!res.ok) throw new Error("GitHub yükleme başarısız");
  return res.json();
}

export async function uploadPaste(code: string, filename?: string): Promise<{ project_id: string }> {
  const res = await fetch("/api/upload/paste", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ code, filename: filename || "paste.txt" }),
  });
  if (!res.ok) throw new Error("Kod yükleme başarısız");
  return res.json();
}

export async function analyzeProject(projectId: string): Promise<any> {
  const res = await fetch("/api/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ project_id: projectId }),
  });
  if (!res.ok) throw new Error("Analiz başarısız");
  return res.json();
}

export async function getReport(projectId: string): Promise<any> {
  const res = await fetch("/api/report", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ project_id: projectId }),
  });
  if (!res.ok) throw new Error("Rapor alınamadı");
  return res.json();
}