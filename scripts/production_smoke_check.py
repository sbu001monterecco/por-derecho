#!/usr/bin/env python3
"""External smoke test for the Por Derecho production GitHub Pages host."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_BASE = "https://sbu001monterecco.github.io/por-derecho/"
CHECKS = [
    {"path": "deployment-probes/mission-critical-hardening-20260818.json",
     "markers": ["psr-mission-critical-hardening-20260818-v1"], "kind": "hardening_probe", "min_bytes": 80},
    {"path": "es/", "markers": ["Project Sun Rock", "resumen-60-segundos"],
     "kind": "homepage_es", "min_bytes": 1000},
    {"path": "en/", "markers": ["Project Sun Rock", "sixty-second-summary"],
     "kind": "homepage_en", "min_bytes": 1000},
    {"path": "es/ric-private-equity-sun-park/", "markers": ["RIC Private Equity", "Registro unitario"],
     "kind": "ricpe_es", "min_bytes": 1000},
    {"path": "es/cnmv-ricpe-verificacion/", "markers": ["CNMV / RICPE", "EXPEDIENTE ABIERTO"],
     "kind": "cnmv_es", "min_bytes": 1000},
    {"path": "es/rsm/nnr4-1025c2f66/", "markers": ["NNR4-1025C2F66", "Perímetro profesional y preservación", "18 ago 2026"],
     "kind": "rsm_es", "min_bytes": 1000},
    {"path": "en/rsm/nnr4-1025c2f66/", "markers": ["NNR4-1025C2F66", "Professional perimeter and preservation", "18 Aug 2026"],
     "kind": "rsm_en", "min_bytes": 1000},
    {"path": "en/pacto-comisorio-credit-to-title-architecture/",
     "markers": ["The strongest defensible case is an appropriation architecture", "indirect commissory appropriation"],
     "kind": "pacto_credit_title_en", "min_bytes": 5000},
    {"path": "es/pacto-comisorio-arquitectura-credito-titulo/",
     "markers": ["El caso más fuerte defendible es una arquitectura de apropiación", "apropiación comisoria indirecta"],
     "kind": "pacto_credit_title_es", "min_bytes": 5000},
    {"path": "en/ph122-cerberus-haya-bankia-external-perimeter/",
     "markers": ["This was not a passive servicing inbox", "Promontoria Holding 122 B.V. / PH122"],
     "kind": "ph122_perimeter_en", "min_bytes": 5000},
    {"path": "es/perimetro-ph122-cerberus-haya-bankia-externo/",
     "markers": ["No fue un buzón pasivo de servicing", "Promontoria Holding 122 B.V. / PH122"],
     "kind": "ph122_perimeter_es", "min_bytes": 5000},
    {"path": "en/insolvency-administrator-credit-to-title-gatekeeper/",
     "markers": ["The Insolvency Administrator was not an observer", "CENTRAL CORRECTION", "withdrawal was filed in LPB's name", "Article 51.2"],
     "kind": "administrator_gatekeeper_en", "min_bytes": 7000},
    {"path": "es/administrador-concursal-puerta-credito-titulo/",
     "markers": ["El Administrador concursal no fue un observador", "CORRECCIÓN CENTRAL", "desistimiento en nombre de LPB", "art. 51.2"],
     "kind": "administrator_gatekeeper_es", "min_bytes": 7000},
    {"path": "en/pp1041-withdrawal-authority-authenticity-benefit/",
     "markers": ["It is not established that LPB withdrew", "POR DERECHO'S CENTRAL ALLEGATION", "de facto functional agent", "Article 51.2"],
     "kind": "pp1041_withdrawal_en", "min_bytes": 9000},
    {"path": "es/desistimiento-pp1041-autoridad-autenticidad-beneficio/",
     "markers": ["No está acreditado que LPB desistiera", "ALEGACIÓN CENTRAL DE POR DERECHO", "agente funcional de facto", "art. 51.2"],
     "kind": "pp1041_withdrawal_es", "min_bytes": 9000},
    {"path": "en/lender-of-record/liability/",
     "markers": ["A creditor chain is not a clean slate", "indirect credit-to-control-to-title appropriation architecture"],
     "kind": "lender_liability_en", "min_bytes": 5000},
    {"path": "es/acreedor-de-registro/responsabilidad/",
     "markers": ["Una cadena de acreedores no es una tabla rasa", "arquitectura indirecta crédito-control-título de apropiación"],
     "kind": "lender_liability_es", "min_bytes": 5000},
    {"path": "sitemap-lender-liability.xml",
     "markers": ["pacto-comisorio-credit-to-title-architecture", "perimetro-ph122-cerberus-haya-bankia-externo", "administrador-concursal-puerta-credito-titulo", "desistimiento-pp1041-autoridad-autenticidad-beneficio", "pp1041-withdrawal-authority-authenticity-benefit"],
     "kind": "lender_liability_sitemap", "min_bytes": 700},
    {"path": "assets/pp1041-withdrawal-authority-correction-20260820.js",
     "markers": ["pp1041-authority-correction", "withdrawal was filed in LPB's name", "desistimiento en nombre de LPB"],
     "kind": "pp1041_global_correction", "min_bytes": 5000},
    {"path": "assets/site.js", "markers": ["site-base-20260819.js?v=20260819a", "case-information-architecture-20260819.js?v=20260819b", "pp1041-withdrawal-authority-correction-20260820.js?v=20260820a"],
     "kind": "global_loader", "min_bytes": 1000},
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def fetch(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={
        "User-Agent": "Por-Derecho-Mission-Critical-Smoke/1.0",
        "Cache-Control": "no-cache, no-store, max-age=0",
        "Pragma": "no-cache",
        "Accept": "text/html,application/json,text/javascript,*/*;q=0.8",
    })
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read()
        return {
            "status": response.status,
            "final_url": response.geturl(),
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified"),
            "server": response.headers.get("Server"),
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "text": body.decode("utf-8", errors="replace"),
        }


def one_pass(base_url: str, timeout: int, attempt: int) -> tuple[bool, list[dict[str, Any]]]:
    all_ok = True
    records: list[dict[str, Any]] = []
    nonce = f"{int(time.time())}-{attempt}"
    for check in CHECKS:
        url = urllib.parse.urljoin(base_url.rstrip("/") + "/", check["path"])
        checked_url = f"{url}{'&' if '?' in url else '?'}psr_smoke={nonce}"
        record: dict[str, Any] = {
            "kind": check["kind"],
            "path": check["path"],
            "url": url,
            "checked_at": utc_now(),
            "required_markers": check["markers"],
        }
        try:
            response = fetch(checked_url, timeout)
            missing = [m for m in check["markers"] if m not in response["text"]]
            record.update({k: v for k, v in response.items() if k != "text"})
            record["missing_markers"] = missing
            record["ok"] = (
                response["status"] == 200
                and response["bytes"] >= check["min_bytes"]
                and not missing
            )
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            record["ok"] = False
            record["error"] = f"{type(exc).__name__}: {exc}"
        if not record["ok"]:
            all_ok = False
        records.append(record)
    return all_ok, records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    parser.add_argument("--attempts", type=int, default=1)
    parser.add_argument("--interval", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--output", default="artifacts/production-smoke/latest.json")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    started_at = utc_now()
    final_records: list[dict[str, Any]] = []

    for attempt in range(1, max(1, args.attempts) + 1):
        ok, records = one_pass(args.base_url, args.timeout, attempt)
        final_records = records
        print(", ".join(f"{r['kind']}={'OK' if r['ok'] else 'FAIL'}" for r in records), flush=True)
        if ok:
            payload = {
                "ok": True,
                "base_url": args.base_url,
                "started_at": started_at,
                "verified_at": utc_now(),
                "attempt": attempt,
                "checks": records,
            }
            output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print("PRODUCTION SMOKE CHECK: PASS")
            return 0
        if attempt < args.attempts:
            time.sleep(max(1, args.interval))

    output.write_text(json.dumps({
        "ok": False,
        "base_url": args.base_url,
        "started_at": started_at,
        "failed_at": utc_now(),
        "attempts": args.attempts,
        "checks": final_records,
    }, indent=2), encoding="utf-8")
    print("PRODUCTION SMOKE CHECK: FAIL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
