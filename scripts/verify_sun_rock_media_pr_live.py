#!/usr/bin/env python3
"""Live verification for the Sun Rock Capital Media/PR bilingual routes."""
from __future__ import annotations
import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
from pathlib import Path
from typing import Any
from production_smoke_check import fetch, utc_now

DEFAULT_BASE = "https://sbu001monterecco.github.io/por-derecho/"
CHECKS = (
    {"path":"en/capital/","kind":"sun_rock_capital_en","markers":("Sun Rock Capital","Media &amp; PR","PRE-ISSUANCE"),"min_bytes":8000},
    {"path":"en/capital/media/","kind":"sun_rock_media_en","markers":("Investing in the next chapter.","Corporate news is not a securities offer.","How we work"),"min_bytes":8000},
    {"path":"en/capital/media/how-we-work/","kind":"sun_rock_how_we_work_en","markers":("How we work.","Build trust before asking for it.","Preserve what helps and what hurts."),"min_bytes":6000},
    {"path":"es/capital/prensa/","kind":"sun_rock_media_es","markers":("Invertir en el próximo capítulo.","La comunicación corporativa no es una oferta de valores.","Cómo trabajamos"),"min_bytes":8000},
    {"path":"es/capital/prensa/como-trabajamos/","kind":"sun_rock_how_we_work_es","markers":("Cómo trabajamos.","Construir confianza antes de pedirla.","Preservar lo que ayuda y lo que perjudica."),"min_bytes":6000},
)

def run_once(base_url: str, timeout: int, attempt: int) -> tuple[bool,list[dict[str,Any]]]:
    rows=[]
    ok=True
    nonce=f"{int(time.time())}-{attempt}"
    for check in CHECKS:
        url=urllib.parse.urljoin(base_url.rstrip("/")+"/",check["path"])
        probe=f"{url}?sun_rock_media_pr={nonce}"
        row={"kind":check["kind"],"path":check["path"],"url":url,"checked_at":utc_now(),"required_markers":list(check["markers"])}
        try:
            response=fetch(probe,timeout)
            missing=[m for m in check["markers"] if m not in response["text"]]
            row.update({k:v for k,v in response.items() if k!="text"})
            row["missing_markers"]=missing
            row["ok"]=response["status"]==200 and response["bytes"]>=check["min_bytes"] and not missing
        except (urllib.error.URLError,urllib.error.HTTPError,TimeoutError,OSError) as exc:
            row["ok"]=False
            row["error"]=f"{type(exc).__name__}: {exc}"
        ok=ok and bool(row["ok"])
        rows.append(row)
    return ok,rows

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--base-url",default=DEFAULT_BASE)
    ap.add_argument("--attempts",type=int,default=1)
    ap.add_argument("--interval",type=int,default=10)
    ap.add_argument("--timeout",type=int,default=20)
    ap.add_argument("--output",default="artifacts/mission-critical-live/sun-rock-media-pr.json")
    args=ap.parse_args()
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    started=utc_now()
    final=[]
    for attempt in range(1,max(1,args.attempts)+1):
        ok,rows=run_once(args.base_url,args.timeout,attempt)
        final=rows
        print(", ".join(f"{r['kind']}={'OK' if r['ok'] else 'FAIL'}" for r in rows),flush=True)
        if ok:
            out.write_text(json.dumps({"ok":True,"started_at":started,"verified_at":utc_now(),"attempt":attempt,"checks":rows},indent=2,ensure_ascii=False),encoding="utf-8")
            print("SUN ROCK MEDIA/PR LIVE CHECK: PASS")
            return 0
        if attempt<args.attempts:
            time.sleep(max(1,args.interval))
    out.write_text(json.dumps({"ok":False,"started_at":started,"failed_at":utc_now(),"attempts":args.attempts,"checks":final},indent=2,ensure_ascii=False),encoding="utf-8")
    print("SUN ROCK MEDIA/PR LIVE CHECK: FAIL",file=sys.stderr)
    return 1

if __name__=="__main__":
    raise SystemExit(main())
