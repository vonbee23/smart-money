const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error(`${path} failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  conviction: () => request("/api/conviction"),
  convictionDetail: (ticker) => request(`/api/conviction/${encodeURIComponent(ticker)}`),
  polymarket: () => request("/api/polymarket"),
  polymarketDetail: (id) => request(`/api/polymarket/${encodeURIComponent(id)}`),
  insiders: (buysOnly) => request(`/api/insiders${buysOnly ? "?buys_only=true" : ""}`),
  congress: () => request("/api/congress"),
  meta: () => request("/api/meta"),
  refresh: async () => {
    const res = await fetch(`${API_BASE}/api/refresh`, { method: "POST" });
    if (!res.ok) throw new Error(`refresh failed: ${res.status}`);
    return res.json();
  },
};
