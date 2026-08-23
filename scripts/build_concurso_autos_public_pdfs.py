#!/usr/bin/env python3
"""Build the ten public, image-only Judge/LAJ decision PDFs."""

from __future__ import annotations

import argparse
from pathlib import Path

from build_public_ac_orders import build


ROOT = Path(__file__).resolve().parents[1]


SPECS = (
    (
        "auto-1377-source.pdf",
        "evidence/insolvency-36-2012/ac-removal-fees/auto-1377-2025-removal-public-redacted.pdf",
        310,
        "Auto 1377/2025 - copia publica redactada",
    ),
    (
        "auto-reconsideration-source.pdf",
        "evidence/insolvency-36-2012/ac-removal-fees/auto-11nov2025-reconsideration-public-redacted.pdf",
        265,
        "Auto de 11 noviembre 2025 - copia publica redactada",
    ),
    (
        "gmail/removal-laj-transfer-2025-04-28.pdf",
        "evidence/insolvency-36-2012/concurso-autos/public-pdfs/laj-28abr2025-traslado-separacion-public-redacted.pdf",
        288,
        "Diligencia LAJ 28 abril 2025 - copia publica redactada",
    ),
    (
        "gmail/removal-laj-table-for-decision-2025-05-20.pdf",
        "evidence/insolvency-36-2012/concurso-autos/public-pdfs/laj-20may2025-puesta-a-resolver-public-redacted.pdf",
        265,
        "Diligencia LAJ 20 mayo 2025 - copia publica redactada",
    ),
    (
        "auto-clarification-source.pdf",
        "evidence/insolvency-36-2012/concurso-autos/public-pdfs/auto-12sep2025-aclaracion-providencia-public-redacted.pdf",
        295,
        "Auto 12 septiembre 2025 sobre aclaracion - copia publica redactada",
    ),
    (
        "gmail/removal-ap-auto-223-2026-07-15.pdf",
        "evidence/insolvency-36-2012/concurso-autos/public-pdfs/auto-223-2026-acumulacion-public-redacted.pdf",
        274,
        "Auto 223/2026 de acumulacion - copia publica redactada",
    ),
    (
        "gmail/fees-auto-inhibition-2024-10-08.pdf",
        "evidence/insolvency-36-2012/concurso-autos/public-pdfs/decreto-113-2024-inhibicion-public-redacted.pdf",
        230,
        "Decreto 113/2024 de inhibicion - copia publica redactada",
    ),
    (
        "gmail/fees-admission-2-2024-11-28.pdf",
        "evidence/insolvency-36-2012/concurso-autos/public-pdfs/decreto-28nov2024-admision-honorarios-public-redacted.pdf",
        228,
        "Decreto 28 noviembre 2024 de admision - copia publica redactada",
    ),
    (
        "fee-judgment-source.pdf",
        "evidence/insolvency-36-2012/concurso-autos/public-pdfs/sentencia-4-2026-honorarios-public-redacted.pdf",
        233,
        "Sentencia 4/2026 - copia publica redactada",
    ),
    (
        "gmail/fees-laj-decree-no-clarification-2026-01.pdf",
        "evidence/insolvency-36-2012/concurso-autos/public-pdfs/decreto-21ene2026-no-aclaracion-public-redacted.pdf",
        216,
        "Decreto 21 enero 2026 sobre aclaracion - copia publica redactada",
    ),
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=ROOT / "tmp/pdfs/ac-core")
    parser.add_argument("--dpi", type=int, default=200)
    args = parser.parse_args()
    for source_rel, output_rel, cutoff, title in SPECS:
        source = args.source_root / source_rel
        output = ROOT / output_rel
        if not source.is_file():
            raise FileNotFoundError(source)
        build(source, output, dpi=args.dpi, header_cutoff=cutoff, title=title)
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
