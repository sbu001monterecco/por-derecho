#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required = {
    "assets/site.js": [
        "san-telmo-attribution-correction-20260819.js?v=20260819a",
    ],
    "assets/san-telmo-attribution-correction-20260819.js": [
        "Speaker correction.",
        "Corrección de atribución.",
        "Eduardo Sánchez · 08:08–08:12",
        "The programme title identifies Enrique Guerra as the guest",
        "El título del programa identifica a Enrique Guerra como invitado",
        "/por-derecho/en/san-telmo-ricpe-sun-park/",
        "/por-derecho/es/san-telmo-ricpe-sun-park/",
    ],
    "en/san-telmo-ricpe-sun-park/index.html": [
        "The direct public source",
        "Proposition-by-proposition evidence map",
        "Same hotel complex and connected project perimeter—not one undivided legal asset.",
        "https://www.youtube.com/watch?v=mHn9IJU0qI4&t=488s",
        "og:title",
        "Silence is not treated as proof.",
    ],
    "es/san-telmo-ricpe-sun-park/index.html": [
        "La fuente pública directa",
        "Mapa probatorio, proposición por proposición",
        "El mismo complejo hotelero y perímetro de proyecto conectado; no un único activo jurídico indivisible.",
        "https://www.youtube.com/watch?v=mHn9IJU0qI4&t=488s",
        "og:title",
        "El silencio no se trata como prueba.",
    ],
    "sitemap-san-telmo.xml": [
        "/en/san-telmo-ricpe-sun-park/",
        "/es/san-telmo-ricpe-sun-park/",
    ],
    "robots.txt": [
        "Sitemap: https://sbu001monterecco.github.io/por-derecho/sitemap-san-telmo.xml",
    ],
    "assets/san-telmo-source-stamp-20260819.js": [
        "San Telmo partner Eduardo Sánchez stated that",
        "08:08 → 08:12",
    ],
}

forbidden = {
    "en/san-telmo-ricpe-sun-park/index.html": [
        "https://aweswell.com/en/san-telmo-ricpe-sun-park/",
    ],
    "es/san-telmo-ricpe-sun-park/index.html": [
        "https://aweswell.com/es/san-telmo-ricpe-sun-park/",
    ],
}

failures = []
for path, markers in required.items():
    text = (ROOT / path).read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            failures.append(f"{path}: missing {marker!r}")
    for marker in forbidden.get(path, []):
        if marker in text:
            failures.append(f"{path}: forbidden stale marker remains {marker!r}")

if failures:
    raise SystemExit("SAN TELMO RENDERED ATTRIBUTION VALIDATION: FAIL\n" + "\n".join(f" - {failure}" for failure in failures))

print("SAN TELMO RENDERED ATTRIBUTION VALIDATION: PASS")
