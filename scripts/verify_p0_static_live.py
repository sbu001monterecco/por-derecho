#!/usr/bin/env python3
"""Verify the P0 static/criminal-framing release on public GitHub Pages."""
from __future__ import annotations
import argparse
import json
import time
import urllib.request
from pathlib import Path

CHECKS = {
    "es/actualizaciones/": ["20 agosto 2026", "arquitectura-nodo-20ago", "ricpe-series-fg-18ago"],
    "es/comunidad-instrumentalizacion/actas-2011-2022/": ["matriz-evento-penal", "no se ha localizado una resolución penal competente"],
    "es/mismo-hotel-multiples-vidas-financieras/": ["6.570.713,56", "6.573.703,10", "2.989,54"],
    "es/reconstruccion-unitaria-autoridades-publicas/": ["SEIS NODOS CLAVE", "matriz-conversiones", "No convertir la narrativa en conclusión penal"],
    "es/ric-private-equity-sun-park/": ["Comunicación formal presentada · 17 agosto 2026", "ricpe-series-fg-control"],
    "es/": ["data-series-fg-priority"],
    "en/community-instrumentalisation/minutes-2011-2022/": ["criminal-event-matrix", "no competent criminal finding establishing a concerted plan has been located"],
    "en/same-hotel-multiple-financial-lives/": ["€6,570,713.56", "€6,573,703.10", "€2,989.54"],
}


def fetch(url: str, timeout: int) -> tuple[int, str, dict[str, str | None]]:
    req = urllib.request.Request(url, headers={"User-Agent":"Por-Derecho-P0-Live-Verify/1.0","Cache-Control":"no-cache, no-store, max-age=0","Pragma":"no-cache"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read().decode("utf-8", errors="replace")
        return r.status, data, {"last_modified":r.headers.get("Last-Modified"),"etag":r.headers.get("ETag"),"server":r.headers.get("Server"),"cache_control":r.headers.get("Cache-Control")}


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--base-url", default="https://sbu001monterecco.github.io/por-derecho/")
    ap.add_argument("--attempts", type=int, default=60)
    ap.add_argument("--interval", type=int, default=10)
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--output", default="artifacts/p0-static-live/verification.json")
    a=ap.parse_args()
    out=Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    last=[]
    for attempt in range(1,a.attempts+1):
        rows=[]; ok=True
        nonce=str(int(time.time()))
        for rel, markers in CHECKS.items():
            url=a.base_url.rstrip("/")+"/"+rel+"?p0_static="+nonce
            row={"path":rel,"url":url,"markers":markers}
            try:
                status,text,headers=fetch(url,a.timeout)
                missing=[m for m in markers if m not in text]
                row.update({"status":status,"headers":headers,"bytes":len(text.encode('utf-8')),"missing":missing,"ok":status==200 and not missing})
            except Exception as exc:
                row.update({"ok":False,"error":f"{type(exc).__name__}: {exc}"})
            ok=ok and row["ok"]; rows.append(row)
        last=rows
        print(f"attempt {attempt}/{a.attempts}: "+", ".join(f"{r['path']}={'OK' if r['ok'] else 'WAIT'}" for r in rows), flush=True)
        if ok:
            payload={"verified":True,"attempt":attempt,"minimum_public_release":"912a23db310776316e3dc206f04c3e3e0018f503","checks":rows,"verified_unix":int(time.time())}
            out.write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding="utf-8")
            print("P0_STATIC_PUBLIC_EDGE_VERIFIED")
            return 0
        if attempt<a.attempts: time.sleep(a.interval)
    out.write_text(json.dumps({"verified":False,"checks":last},indent=2,ensure_ascii=False),encoding="utf-8")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
