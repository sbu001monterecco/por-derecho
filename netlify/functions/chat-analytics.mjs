import { getStore } from "@netlify/blobs";

const ALLOWED_INPUT = new Set(["text", "audio"]);
const ALLOWED_LANG = new Set(["es", "en"]);
const ALLOWED_STATUS = new Set(["answered", "insufficient", "error"]);
const ALLOWED_TOPIC = new Set(["insolvency", "title-control", "community-cexp", "ricpe-finance", "public-funds", "regulatory", "professional", "operator-hotel", "lender-credit", "recovery", "general-record"]);
const ALLOWED_INTEREST = new Set(["general", "hospitality", "legal-finance", "media-research", "public-institutional", "directly-connected", "prefer-not-to-say"]);
const CONSENT_VERSION = "20260821a";
const PAGE_RE = /^\/(?:por-derecho\/)?(?:es|en)(?:\/[a-z0-9._~!$&'()*+,;=:@%/-]*)?$/i;

function safe(v, allowed, fallback) { return allowed.has(String(v || "")) ? String(v) : fallback; }
function inc(obj, key, amount = 1) { obj[key] = (obj[key] || 0) + amount; }
function cleanPage(value) {
  const p = String(value || "").split(/[?#]/)[0].slice(0, 220);
  return PAGE_RE.test(p) ? p : "/unknown";
}
function allowedOrigin(req) {
  const origin = req.headers.get("origin") || "";
  const allowed = new Set(["https://sbu001monterecco.github.io", ...(process.env.PSR_ALLOWED_ORIGINS || "").split(",").map(x => x.trim()).filter(Boolean)]);
  try { allowed.add(new URL(req.url).origin); } catch {}
  return allowed.has(origin) ? origin : "";
}
function json(data, status = 200, origin = "") {
  const headers = { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex, nofollow" };
  if (origin) { headers["access-control-allow-origin"] = origin; headers.vary = "Origin"; }
  return new Response(JSON.stringify(data), { status, headers });
}
function blank(date) {
  return { schema: 1, date, total: 0, input: {}, language: {}, topic: {}, page: {}, interest: {}, country: {}, status: {}, sourceCount: { "0": 0, "1-2": 0, "3-5": 0 }, consentVersion: {} };
}
function mergeEvent(data, event, country) {
  data.total += 1;
  inc(data.input, event.inputType);
  inc(data.language, event.lang);
  inc(data.topic, event.topic);
  inc(data.page, event.pagePath);
  inc(data.interest, event.interest);
  if (country) inc(data.country, country);
  inc(data.status, event.status);
  inc(data.consentVersion, event.consentVersion);
  const sc = Number(event.sourceCount || 0);
  inc(data.sourceCount, sc <= 0 ? "0" : sc <= 2 ? "1-2" : "3-5");
  return data;
}

async function updateDaily(date, event, country) {
  const store = getStore({ name: "psr-chat-analytics", consistency: "strong" });
  const key = `daily/${date}`;
  for (let attempt = 0; attempt < 6; attempt += 1) {
    const existing = await store.getWithMetadata(key, { type: "json", consistency: "strong" });
    const next = mergeEvent(existing?.data ? structuredClone(existing.data) : blank(date), event, country);
    const result = existing
      ? await store.setJSON(key, next, { onlyIfMatch: existing.etag })
      : await store.setJSON(key, next, { onlyIfNew: true });
    if (result.modified) return;
  }
  throw new Error("aggregate_write_conflict");
}

export default async (req, context) => {
  const origin = allowedOrigin(req);
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: origin ? { "access-control-allow-origin": origin, "access-control-allow-methods": "POST, OPTIONS", "access-control-allow-headers": "content-type", vary: "Origin" } : {} });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405, origin);
  if (req.headers.get("origin") && !origin) return json({ error: "origin_not_allowed" }, 403);
  let body;
  try { body = await req.json(); } catch { return json({ error: "invalid_json" }, 400, origin); }
  if (body?.analyticsConsent !== true || body?.consentVersion !== CONSENT_VERSION) return json({ stored: false, reason: "no_consent" }, 200, origin);

  const event = {
    inputType: safe(body?.inputType, ALLOWED_INPUT, "text"),
    lang: safe(body?.lang, ALLOWED_LANG, "es"),
    topic: safe(body?.topic, ALLOWED_TOPIC, "general-record"),
    pagePath: cleanPage(body?.pagePath),
    interest: safe(body?.interest, ALLOWED_INTEREST, "prefer-not-to-say"),
    status: safe(body?.status, ALLOWED_STATUS, "error"),
    sourceCount: Math.max(0, Math.min(5, Number(body?.sourceCount || 0))),
    consentVersion: CONSENT_VERSION,
  };
  const countryRaw = String(context?.geo?.country?.code || "").toUpperCase();
  const country = /^[A-Z]{2}$/.test(countryRaw) ? countryRaw : "";
  const date = new Date().toISOString().slice(0, 10);
  try {
    await updateDaily(date, event, country);
    return json({ stored: true, mode: "daily-aggregate-only" }, 200, origin);
  } catch {
    return json({ stored: false, reason: "aggregate_unavailable" }, 202, origin);
  }
};

export const config = {
  path: "/api/psr-chat-analytics",
  region: "fra",
  rateLimit: { windowLimit: 30, windowSize: 60, aggregateBy: ["ip", "domain"] },
};
