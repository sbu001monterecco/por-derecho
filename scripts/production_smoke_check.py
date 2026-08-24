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
    {"path": "es/", "markers": ["Project Sun Rock", "resumen-60-segundos", 'id="private-actors"'],
     "kind": "homepage_es", "min_bytes": 1000},
    {"path": "en/", "markers": ["Project Sun Rock", "sixty-second-summary"],
     "kind": "homepage_en", "min_bytes": 1000},
    {"path": "es/ricpe-hnt-gc836-trazabilidad/",
     "markers": ["Sun Park / MYND Yaiza: seguir la estructura y los fondos, capa por capa.", "GC/836/P06"],
     "kind": "sent_email_ricpe_hnt_gc836_es", "min_bytes": 8000},
    {"path": "es/concurso-36-2012-autos-decisiones/",
     "markers": ["Ruta de compatibilidad para enlaces ya enviados", "concurso-36-2012-autos-resoluciones"],
     "kind": "sent_email_concurso36_legacy_es", "min_bytes": 700},
    {"path": "es/activo-financiacion-sun-park-mynd/",
     "markers": ["Ruta de compatibilidad para enlaces ya enviados", "cadena-instrumentalizacion-ric-fondos-incentivos"],
     "kind": "sent_email_asset_finance_legacy_es", "min_bytes": 700},
    {"path": "es/yaiza-obras-trazabilidad/",
     "markers": ["Ruta de compatibilidad para enlaces ya enviados", "yaiza-trazabilidad-institucional"],
     "kind": "sent_email_yaiza_works_legacy_es", "min_bytes": 700},
    {"path": "de/lava-verde-club-sei-meeting-point/",
     "markers": ["Kompatibilitätsroute für einen bereits versandten Link", "en/lava-verde-club-sei-meeting-point"],
     "kind": "sent_email_lava_verde_legacy_de", "min_bytes": 700},
    {"path": "es/concurso-36-2012-autos-resoluciones/",
     "markers": ["Autos, decisiones y escritos localizados del Concurso 36/2012", "INVENTARIO PARCIAL — FALTA ÍNDICE CERTIFICADO O DOCUMENTACIÓN"],
     "kind": "concurso36_corpus_es", "min_bytes": 100000},
    {"path": "en/insolvency-36-2012-orders-decisions/",
     "markers": ["Located orders, decisions and filings in Insolvency 36/2012", "INVENTORY PARTIAL — CERTIFIED DOCKET OR RECORDS STILL MISSING"],
     "kind": "concurso36_corpus_en", "min_bytes": 100000},
    {"path": "es/concurso-36-2012-que-ordeno-el-juzgado/",
     "markers": ["Qué ordenaron los autos críticos localizados", "doce instrumentos críticos"],
     "kind": "concurso36_orders_reader_es", "min_bytes": 15000},
    {"path": "en/concurso-36-2012-what-the-court-ordered/",
     "markers": ["What the located critical orders did", "twelve critical instruments"],
     "kind": "concurso36_orders_reader_en", "min_bytes": 15000},
    {"path": "es/concurso-36-2012-columna-judicial/",
     "markers": ["Qué autorizó realmente el Juzgado", "columna judicial"],
     "kind": "concurso36_judicial_spine_es", "min_bytes": 7000},
    {"path": "en/concurso-36-2012-judicial-spine/",
     "markers": ["What the court actually authorized", "judicial spine"],
     "kind": "concurso36_judicial_spine_en", "min_bytes": 7000},
    {"path": "es/solicitud-seguridad-administracion-concursal-sun-park-27-febrero-2018/",
     "markers": ["Solicitud de convocatoria para considerar la contratación de seguridad", "27 de febrero de 2018"],
     "kind": "concurso36_security_request_es", "min_bytes": 6000},
    {"path": "en/insolvency-administrator-security-request-sun-park-27-february-2018/",
     "markers": ["Request to convene a meeting to consider hiring security", "27 February 2018"],
     "kind": "concurso36_security_request_en", "min_bytes": 6000},
    {"path": "es/concurso-36-2012-separacion-ac-honorarios/",
     "markers": ["Separación, honorarios y control integral del Administrador Concursal", "110.956,97"],
     "kind": "concurso36_removal_fees_es", "min_bytes": 18000},
    {"path": "en/insolvency-36-2012-administrator-removal-fees/",
     "markers": ["Removal, remuneration and integrated control of the Insolvency Administrator", "110,956.97"],
     "kind": "concurso36_removal_fees_en", "min_bytes": 18000},
    {"path": "es/acreedor-de-registro/credito-litigioso-escritura/",
     "markers": ["La cesión PH122 → Construcciones Acosta Matos exige separar cuatro preguntas", "15 de febrero de 2018"],
     "kind": "concurso36_assignment_es", "min_bytes": 10000},
    {"path": "en/lender-of-record/litigious-credit-hidden-deed/",
     "markers": ["The PH122 → Construcciones Acosta Matos assignment requires four questions", "15 February 2018"],
     "kind": "concurso36_assignment_en", "min_bytes": 10000},
    {"path": "es/reconstruccion-unitaria-autoridades-publicas/",
     "markers": ["Reconstruir la cadena completa sin asumir la teoría de ninguna parte.", "Concurso 36/2012"],
     "kind": "concurso36_authorities_es", "min_bytes": 20000},
    {"path": "en/public-authority-unitary-case-reconstruction/",
     "markers": ["Reconstruct the complete chain without adopting any party's theory.", "Insolvency 36/2012"],
     "kind": "concurso36_authorities_en", "min_bytes": 20000},
    {"path": "en/ric-private-equity-sun-park/",
     "markers": ["RIC Private Equity", "Unitary Sun Park record"],
     "kind": "ricpe_en", "min_bytes": 1000},
    {"path": "es/adjudicacion-2022-reconstruccion-documental/",
     "markers": ["La cuestión central ya no es un recálculo de intereses", "Adjudicación de 2022"],
     "kind": "concurso36_adjudication_es", "min_bytes": 20000},
    {"path": "en/2022-adjudication-documentary-reconstruction/",
     "markers": ["The central issue is no longer a recalculation of interest", "2022 adjudication"],
     "kind": "concurso36_adjudication_en", "min_bytes": 18000},
    {"path": "es/ric-private-equity-sun-park/", "markers": ["RIC Private Equity", "Registro unitario"],
     "kind": "ricpe_es", "min_bytes": 1000},
    {"path": "es/cnmv-ricpe-verificacion/", "markers": ["CNMV / RICPE", "EXPEDIENTE ABIERTO"],
     "kind": "cnmv_es", "min_bytes": 1000},
    {"path": "es/rsm/nnr4-1025c2f66/", "markers": ["NNR4-1025C2F66", "Perímetro profesional y preservación", "18 ago 2026"],
     "kind": "rsm_es", "min_bytes": 1000},
    {"path": "en/rsm/nnr4-1025c2f66/", "markers": ["NNR4-1025C2F66", "Professional perimeter and preservation", "18 Aug 2026"],
     "kind": "rsm_en", "min_bytes": 1000},
    {"path": "en/insolvency-36-2012-insolvency-administrator/",
     "markers": ["Supervision is not a substitute for historical responsibility", "Non-erasure rule", "Article 82 TRLC"],
     "kind": "ac_accountability_en", "min_bytes": 5000},
    {"path": "es/concurso-36-2012-administrador-concursal/",
     "markers": ["Supervisión no equivale a resolver la responsabilidad histórica", "Regla de no borrado", "artículo 82 TRLC"],
     "kind": "ac_accountability_es", "min_bytes": 5000},
    {"path": "en/cam-creditor-control-shadow-administration-judicial-omission/",
     "markers": ["They are not judicial findings.", "DIRECT CRIMINAL-ATTRIBUTION · PRIVATE INSTRUCTION", "the 2018 provisional dismissal and appellate confirmation remain prominent."],
     "kind": "cam_creditor_control_criminal_lead_en", "min_bytes": 25000},
    {"path": "es/control-acreedor-cam-administracion-hecho-omision-judicial/",
     "markers": ["No son declaraciones judiciales.", "ATRIBUCIÓN PENAL DIRECTA · INSTRUCCIÓN PRIVADA", "mientras el archivo provisional de 2018 y su confirmación en apelación permanecen destacados."],
     "kind": "cam_creditor_control_criminal_lead_es", "min_bytes": 25000},
    {"path": "en/reverse-engineering-360-sun-park-chain/",
     "markers": ["Supervision is not a historical clean-slate", "360° non-erasure rule", "Article 82/83 control"],
     "kind": "reverse_engineering_ac_en", "min_bytes": 5000},
    {"path": "es/ingenieria-inversa-360-cadena-sun-park/",
     "markers": ["La supervisión no crea un «borrón y cuenta nueva» histórico", "Regla 360° de no borrado", "Control artículos 82/83"],
     "kind": "reverse_engineering_ac_es", "min_bytes": 5000},
    {"path": "en/dp-1956-2026/",
     "markers": ["Correction is evidence, not erasure", "retroactive exoneration", "proof of prior guilt"],
     "kind": "dp1956_non_erasure_en", "min_bytes": 5000},
    {"path": "es/dp-1956-2026/",
     "markers": ["Corregir es prueba, no borrado", "exoneración retroactiva", "prueba de culpabilidad previa"],
     "kind": "dp1956_non_erasure_es", "min_bytes": 5000},
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
     "markers": ["The Insolvency Administrator was not an observer", "His office controlled indispensable gates"],
     "kind": "administrator_gatekeeper_en", "min_bytes": 5000},
    {"path": "es/administrador-concursal-puerta-credito-titulo/",
     "markers": ["El Administrador concursal no fue un observador", "Su cargo controló compuertas indispensables"],
     "kind": "administrator_gatekeeper_es", "min_bytes": 5000},
    {"path": "en/lender-of-record/liability/",
     "markers": ["A creditor chain is not a clean slate", "indirect credit-to-control-to-title appropriation architecture"],
     "kind": "lender_liability_en", "min_bytes": 5000},
    {"path": "es/acreedor-de-registro/responsabilidad/",
     "markers": ["Una cadena de acreedores no es una tabla rasa", "arquitectura indirecta crédito-control-título de apropiación"],
     "kind": "lender_liability_es", "min_bytes": 5000},
    {"path": "sitemap-lender-liability.xml",
     "markers": ["pacto-comisorio-credit-to-title-architecture", "perimetro-ph122-cerberus-haya-bankia-externo", "administrador-concursal-puerta-credito-titulo"],
     "kind": "lender_liability_sitemap", "min_bytes": 500},
    {"path": "assets/site.js", "markers": ["site-pre-intervencion-highlight-20260820.js?v=20260824e", "intervencion-protected-assets-highlight-20260820.js?v=20260820a"],
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
