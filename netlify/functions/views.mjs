import { getStore } from "@netlify/blobs";

const headers = { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "x-content-type-options": "nosniff", "referrer-policy": "no-referrer" };
const reply = (body, status = 200) => new Response(JSON.stringify(body), { status, headers });

export const createHandler = (resolveStore = getStore) => async (request) => {
  if (request.method !== "POST" && request.method !== "GET") return reply({ error: "Method not allowed" }, 405);
  try {
    const store = resolveStore("portfolio-metrics");
    if (request.method === "GET") {
      const value = await store.get("site-visits", { type: "text" });
      return reply({ total: Math.max(0, Number.parseInt(value ?? "0", 10) || 0) });
    }
    for (let attempt = 0; attempt < 12; attempt += 1) {
      const entry = await store.getWithMetadata("site-visits", { type: "text" });
      const current = Math.max(0, Number.parseInt(entry?.data ?? "0", 10) || 0);
      const options = entry?.etag ? { onlyIfMatch: entry.etag } : { onlyIfNew: true };
      const result = await store.set("site-visits", String(current + 1), options);
      if (result.modified) return reply({ total: current + 1 });
    }
    return reply({ error: "Counter busy; retry on next visit" }, 503);
  } catch {
    return reply({ error: "Counter storage unavailable" }, 503);
  }
};

export default createHandler();

