import { getStore } from "@netlify/blobs";

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex, nofollow" } });
}
function add(target, source) { for (const [k, v] of Object.entries(source || {})) target[k] = (target[k] || 0) + Number(v || 0); }
function dates(days) {
  const out = [];
  const now = new Date();
  for (let i = 0; i < days; i += 1) { const d = new Date(now); d.setUTCDate(d.getUTCDate() - i); out.push(d.toISOString().slice(0, 10)); }
  return out;
}
function top(obj, limit = 12, suppressBelow = 1) {
  return Object.entries(obj || {}).filter(([, v]) => Number(v) >= suppressBelow).sort((a, b) => b[1] - a[1]).slice(0, limit).map(([key, count]) => ({ key, count }));
}

export default async (req) => {
  if (req.method !== "GET") return json({ error: "method_not_allowed" }, 405);
  const expected = process.env.CHAT_ANALYTICS_ADMIN_TOKEN || "";
  const supplied = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
  if (!expected || supplied !== expected) return json({ error: "unauthorized" }, 401);

  const url = new URL(req.url);
  const days = Math.max(1, Math.min(90, Number(url.searchParams.get("days") || 30)));
  const store = getStore("psr-chat-analytics");
  const sum = { total: 0, input: {}, language: {}, topic: {}, page: {}, interest: {}, country: {}, status: {}, sourceCount: {} };
  const daily = [];
  for (const date of dates(days)) {
    const row = await store.get(`daily/${date}`, { type: "json" });
    if (!row) continue;
    daily.push({ date, total: Number(row.total || 0) });
    sum.total += Number(row.total || 0);
    ["input", "language", "topic", "page", "interest", "country", "status", "sourceCount"].forEach(k => add(sum[k], row[k]));
  }
  return json({
    periodDays: days,
    total: sum.total,
    daily: daily.sort((a, b) => a.date.localeCompare(b.date)),
    input: top(sum.input),
    language: top(sum.language),
    topics: top(sum.topic),
    pages: top(sum.page, 15),
    interests: top(sum.interest, 10, 3),
    countries: top(sum.country, 10, 3),
    status: top(sum.status),
    sourceCount: top(sum.sourceCount),
    privacy: { rawQuestionsStored: false, transcriptsStored: false, answersStored: false, ipStored: false, persistentVisitorId: false, rareInterestAndCountryCellsSuppressedBelow: 3 },
  });
};

export const config = {
  path: "/api/psr-chat-insights",
  region: "fra",
  rateLimit: { windowLimit: 30, windowSize: 60, aggregateBy: ["ip", "domain"] },
};
