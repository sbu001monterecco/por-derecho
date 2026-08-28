#!/usr/bin/env python3
"""Build reciprocal backlinks from the nine satellite tracks to the two core routes."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_ID = "PD-SP-POST7J-20260828-01"
BEGIN = "<!-- POST7J-EVIDENCE-JUNCTION:BEGIN -->"
END = "<!-- POST7J-EVIDENCE-JUNCTION:END -->"

ROUTES = {
    "en": [
        ("community", "en/community-instrumentalisation/index.html"),
        ("acosta", "en/acosta-matos-perimeter/index.html"),
        ("estate", "en/insolvency-36-2012-active-estate-2018-2021/index.html"),
        ("ona", "en/ona-hotels-insolvency-exit-36-2012/index.html"),
        ("de-facto", "en/de-facto-administration-community-ac/index.html"),
        ("deed", "en/2022-adjudication-documentary-reconstruction/index.html"),
        ("funding", "en/ricpe-hnt-gc836-traceability/index.html"),
        ("club-sei", "en/lava-verde-club-sei-meeting-point/index.html"),
        ("financial-lives", "en/same-hotel-multiple-financial-lives/index.html"),
    ],
    "es": [
        ("community", "es/comunidad-instrumentalizacion/index.html"),
        ("acosta", "es/acosta-matos-perimetro/index.html"),
        ("estate", "es/concurso-36-2012-masa-activa-2018-2021/index.html"),
        ("ona", "es/ona-hotels-salida-concurso-36-2012/index.html"),
        ("de-facto", "es/administracion-de-hecho-comunidad-ac/index.html"),
        ("deed", "es/adjudicacion-2022-reconstruccion-documental/index.html"),
        ("funding", "es/ricpe-hnt-gc836-trazabilidad/index.html"),
        ("club-sei", "es/lava-verde-club-sei-meeting-point/index.html"),
        ("financial-lives", "es/mismo-hotel-multiples-vidas-financieras/index.html"),
    ],
}


def backlink(locale: str, route_id: str) -> str:
    if locale == "es":
        return (
            f'{BEGIN}<nav class="shell post7-evidence-backlink" '
            f'data-post7-evidence-backlink="{CONTROL_ID}" data-post7-route-id="{route_id}" '
            'aria-label="Volver al nudo probatorio unitario 2018–2022">'
            '<strong>Nudo probatorio unitario · carriles separados, prueba interconectada</strong>'
            '<a data-post7-core="takeover" href="../toma-control-sun-park-7-junio-2018/'
            '#mapa-omnidireccional-4feb2022">7 junio 2018 → mapa 2022</a>'
            '<a data-post7-core="meeting" href="../comunidad-instrumentalizacion/'
            'sala-documental-actas/2022-02-04/#lectura-unitaria-2018-2022">'
            'Junta / ACTA de 4 febrero 2022</a></nav>'
            f'{END}'
        )
    return (
        f'{BEGIN}<nav class="shell post7-evidence-backlink" '
        f'data-post7-evidence-backlink="{CONTROL_ID}" data-post7-route-id="{route_id}" '
        'aria-label="Return to the unitary 2018–2022 evidence junction">'
        '<strong>Unitary evidence junction · separate tracks, connected proof</strong>'
        '<a data-post7-core="takeover" href="../sun-park-takeover-7-june-2018/'
        '#omnidirectional-4feb2022-map">7 June 2018 → 2022 map</a>'
        '<a data-post7-core="meeting" href="../community-instrumentalisation/'
        'acta-document-room/2022-02-04/#unitary-reading-2018-2022">'
        '4 February 2022 meeting / ACTA</a></nav>'
        f'{END}'
    )


def main() -> int:
    pattern = re.compile(rf"\s*{re.escape(BEGIN)}.*?{re.escape(END)}", re.DOTALL)
    changed = 0
    for locale, routes in ROUTES.items():
        for route_id, relative in routes:
            path = ROOT / relative
            text = path.read_text(encoding="utf-8")
            text = pattern.sub("", text)
            if text.count("</main>") != 1:
                raise RuntimeError(f"{relative}: expected exactly one </main>")
            rendered = text.replace("</main>", f"\n{backlink(locale, route_id)}\n</main>")
            path.write_text(rendered, encoding="utf-8")
            changed += 1
    print(f"POST-7-JUNE RECIPROCAL ROUTE INTERLINKS: BUILT {changed} PAGES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
