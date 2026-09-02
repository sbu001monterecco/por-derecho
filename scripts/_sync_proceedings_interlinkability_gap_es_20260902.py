#!/usr/bin/env python3
"""Add the source-bounded Spanish gap texts for the 2-Sep historic exact-file backfill.

The legacy interlinkability builder intentionally requires GAP_ES to cover every
public exact proceeding with an open source gap.  These entries are translations
of the canonical Master Open_Reference_Gap fields for the newly recovered files;
no authority identity, relationship, merits finding or outcome is inferred here.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
BUILDER = ROOT / "scripts/build_proceedings_interlinkability_v1.py"

GAPS = {
    "LZ-APP-046": "Identidad del LAJ; rollo certificado completo; registro de notificación y firmeza.",
    "LZ-APP-054": "NIG; resolución final firmada exacta; identidades del panel o Juez cuando proceda por el acto judicial; LAJ; notificación y firmeza.",
    "LZ-CIV-045": "Identidad del LAJ; expediente completo; recurso, firmeza y registro de notificación.",
    "LZ-FIS-049": "Extracción del Fiscal asignado o firmante; destino judicial y NIG; expediente completo de investigación; disposición y firmeza.",
    "LZ-FIS-051": "Clase exacta del expediente de Fiscalía; Fiscal asignado o firmante; decretos de incoación y archivo; anexos; notificación y firmeza.",
    "LZ-JUD-047": "Auto inicial o denuncia firmados; Juez; LAJ; Fiscal; acto de acumulación con DP 168/2015; disposición final, notificación y firmeza.",
    "LZ-JUD-048": "NIG; querella o denuncia; partes y capacidades exactas; Juez; LAJ; Fiscal; auto de archivo y firmeza.",
    "LZ-REF-038": "NIG; denuncia o querella; acto firmado de acumulación o ampliación de 15 de julio de 2017; Juez; LAJ; Fiscal; disposición final y notificación.",
    "LZ-REF-039": "NIG; sentencia firmada; Juez; LAJ; escritos de las partes; notificación y firmeza.",
}


def main() -> int:
    with MASTER.open(encoding="utf-8", newline="") as fh:
        rows = {row["Master_ID"]: row for row in csv.DictReader(fh)}

    for master_id in GAPS:
        row = rows.get(master_id)
        if not row:
            raise SystemExit(f"missing canonical Master row for {master_id}")
        if row.get("Is_Proceeding", "").strip().upper() != "TRUE":
            raise SystemExit(f"{master_id} is no longer an exact proceeding; review GAP_ES patch")
        if not row.get("Open_Reference_Gap", "").strip():
            raise SystemExit(f"{master_id} no longer has an open source gap; review GAP_ES patch")

    path = BUILDER
    text = path.read_text(encoding="utf-8")
    original = text
    start = text.find("GAP_ES = {")
    if start < 0:
        raise SystemExit("GAP_ES block not found")
    end_marker = "\n}\n\n\ndef is_public"
    end = text.find(end_marker, start)
    if end < 0:
        raise SystemExit("GAP_ES closing anchor not found")

    block = text[start:end]
    additions = []
    for master_id, gap in GAPS.items():
        if re.search(rf'^\s*"{re.escape(master_id)}"\s*:', block, flags=re.M):
            continue
        escaped = gap.replace('\\', '\\\\').replace('"', '\\"')
        additions.append(f'    "{master_id}": "{escaped}",')
    if additions:
        text = text[:end] + "\n" + "\n".join(additions) + text[end:]

    path.write_text(text, encoding="utf-8")
    state = "IDEMPOTENT" if text == original else "UPDATED"
    print("PROCEEDINGS_INTERLINKABILITY_GAP_ES_SYNCED", len(GAPS), state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
