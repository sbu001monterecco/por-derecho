#!/usr/bin/env python3
"""Bounded public-web discovery intake for RICPE / Canary private-capital research.

Uses a public search RSS endpoint for discovery only. Results are leads, not facts.
No result is promoted automatically to canonical identity/evidence.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, pathlib, urllib.parse, urllib.request, xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTER = ROOT / "assets/data/ricpe-capital-ecosystem-actor-register-v1.json"

BASE_QUERIES = [
    '"RIC Private Equity" CNMV',
    '"RIC Private Equity" BORME',
    '"RIC Private Equity" Tenerife inversores',
    '"RIC Private Equity" Lanzarote',
    '"RIC Private Equity" "MYND Yaiza"',
    '"RIC Private Equity" "Hotel New Trend"',
    '"RIC Private Equity" ampliación capital',
    '"RIC Private Equity" accionistas',
    '"RIC Private Equity" CEOE Tenerife',
    '"RIC Private Equity" FEPECO',
    '"RIC Private Equity" ASHOTEL',
    '"RIC Private Equity" RECABA',
]

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def rss_search(q: str) -> dict:
    url = "https://www.bing.com/search?format=rss&q=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={"User-Agent":"PorDerecho-RICPE-PublicDiscovery/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read(2_000_000)
        root = ET.fromstring(raw)
        items = []
        for item in root.findall(".//item")[:10]:
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            desc = (item.findtext("description") or "").strip()
            items.append({"title":title,"url":link,"description":desc[:1200]})
        return {"query":q,"state":"FETCHED","results":items,"rss_sha256":hashlib.sha256(raw).hexdigest()}
    except Exception as e:
        return {"query":q,"state":"ERROR","error_type":type(e).__name__,"error":str(e)[:300],"results":[]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--max-person-queries", type=int, default=30)
    args = ap.parse_args()
    reg = json.loads(REGISTER.read_text(encoding="utf-8"))
    queries = list(BASE_QUERIES)
    for row in reg.get("people", [])[:args.max_person_queries]:
        name = row.get("name")
        if name:
            queries.append(f'"{name}" "RIC Private Equity"')
    seen = set()
    ordered = []
    for q in queries:
        if q not in seen:
            seen.add(q); ordered.append(q)
    rows = [rss_search(q) for q in ordered]
    out = {
        "schema":"por-derecho.ricpe-public-web-discovery.v1",
        "generated_at":now(),
        "classification":"RAW_SEARCH_DISCOVERY_INTAKE_NOT_CANONICAL_FACT",
        "register":"assets/data/ricpe-capital-ecosystem-actor-register-v1.json",
        "query_count":len(rows),
        "promotion_rule":"Search hit -> source read -> source/date/proposition capture -> identity reconciliation -> contrary check -> canonical PR/MR.",
        "queries":rows,
    }
    p=pathlib.Path(args.output); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"query_count":len(rows),"output":str(p),"generated_at":out["generated_at"]}))

if __name__ == "__main__":
    main()
