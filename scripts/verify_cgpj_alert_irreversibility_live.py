#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
import urllib.request
from pathlib import Path

TARGETS = [
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/es/cgpj-alerta-irreversibilidad/",
        "markers": ["De la alerta a la irreversibilidad.", "CONSECUENCIA ≠ CONOCIMIENTO JUDICIAL HISTÓRICO", "EL RESULTADO NO RESPONDE EL ORIGEN", "Matkator"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/en/cgpj-alert-to-irreversibility/",
        "markers": ["From alert to irreversibility.", "CONSEQUENCE ≠ HISTORICAL JUDICIAL KNOWLEDGE", "THE RESULT DOES NOT ANSWER THE ORIGIN", "Matkator"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/assets/cgpj-alzada-regage-20260816.js",
        "markers": ["CGPJ_ALERT_VISUAL_INTEGRATION_V1", "CGPJ_ALERT_CONTRAST_FIX_V1", ".hero-map .rule{color:#13252d}", "/por-derecho/es/cgpj-alerta-irreversibilidad/", "/por-derecho/en/cgpj-alert-to-irreversibility/", "PUENTE EXTRACONCURSAL", "LATER PUBLIC RELIANCE"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/assets/site.js",
        "markers": ["cgpj-alzada-regage-20260816.js"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/es/cgpj-comision-permanente-sala-lectura/",
        "markers": ["SALA DE LECTURA", "site.js"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/en/cgpj-permanent-commission-reader-room/",
        "markers": ["PERMANENT COMMISSION", "site.js"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/es/concurso-36-2012-magistrado-juez/",
        "markers": ["Alberto López Villarrubia", "site.js"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/es/ric-private-equity-sun-park/",
        "markers": ["Alerta 2021", "site.js"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/es/toma-control-sun-park-7-junio-2018/",
        "markers": ["LPB era la concursada", "site.js"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/deployment-probes/cgpj-alert-irreversibility-20260818.txt",
        "markers": ["CGPJ-ALERT-IRREVERSIBILITY-LIVE-PROBE-20260818-V1"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/sitemap-cgpj.xml",
        "markers": ["/es/cgpj-alerta-irreversibilidad/", "/en/cgpj-alert-to-irreversibility/"],
    },
]


def fetch(url: str, timeout: int) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "por-derecho-cgpj-alert-live-verifier/3"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.status, response.read().decode("utf-8", errors="replace")


def verify_once(timeout: int) -> tuple[bool, list[dict]]:
    rows = []
    ok = True
    for target in TARGETS:
        row = {"url": target["url"], "status": None, "missing_markers": [], "error": None}
        try:
            status, body = fetch(target["url"], timeout)
            row["status"] = status
            row["missing_markers"] = [m for m in target["markers"] if m not in body]
            if status != 200 or row["missing_markers"]:
                ok = False
        except Exception as exc:
            row["error"] = repr(exc)
            ok = False
        rows.append(row)
    return ok, rows


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--attempts", type=int, default=36)
    p.add_argument("--interval", type=int, default=10)
    p.add_argument("--timeout", type=int, default=20)
    p.add_argument("--output", default="artifacts/cgpj-alert-irreversibility-live/verification.json")
    args = p.parse_args()

    last = []
    for attempt in range(1, args.attempts + 1):
        ok, rows = verify_once(args.timeout)
        last = rows
        print(json.dumps({"attempt": attempt, "ok": ok, "results": rows}, ensure_ascii=False, indent=2))
        if ok:
            payload = {"verified": True, "attempt": attempt, "results": rows}
            out = Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            return 0
        if attempt < args.attempts:
            time.sleep(args.interval)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"verified": False, "results": last}, ensure_ascii=False, indent=2), encoding="utf-8")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
