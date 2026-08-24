#!/usr/bin/env python3
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

required = {
    "assets/site.js": [
        "san-telmo-attribution-correction-20260819.js?v=20260819a",
        "data-san-telmo-attribution-loader",
    ],
    "assets/san-telmo-attribution-correction-20260819.js": [
        "Speaker correction.",
        "Corrección de atribución.",
        "Eduardo Sánchez · 08:08–08:12",
        "The programme title identifies Enrique Guerra as the guest",
        "El título del programa identifica a Enrique Guerra como invitado",
        "section.interview-evidence",
        "pdSanTelmoAttribution",
        "pd:san-telmo-attribution-ready",
        "/por-derecho/en/san-telmo-ricpe-sun-park/",
        "/por-derecho/es/san-telmo-ricpe-sun-park/",
    ],
    "assets/audience-experience-order-20260823.js": [
        "section.interview-evidence[data-pd-san-telmo-attribution=",
        "audienceProtectedSanTelmo",
        "sanTelmoAttributionVisible",
        "sanTelmo.classList.add('shell')",
        "placeAfter(sanTelmo, sourceFunds || fullRecord)",
        "pd:san-telmo-attribution-ready",
    ],
    "en/index.html": [
        '<section class="interview-evidence"',
    ],
    "es/index.html": [
        '<section class="interview-evidence"',
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
    "scripts/render_san_telmo_attribution_live.mjs": [
        'section.interview-evidence[data-pd-san-telmo-attribution="20260819"]',
        "Speaker correction.",
        "Corrección de atribución.",
        "staleTextAbsent",
        "primarySourceLink",
        "RENDERED_DOM_LIVE_VERIFIED",
        "visibleOutsideCollapsedRecord",
        "directChildOfMain",
    ],
    ".github/workflows/verify-san-telmo-rendered-attribution-live.yml": [
        "Verify rendered English and Spanish homepage attribution",
        "scripts/render_san_telmo_attribution_live.mjs",
        "SOURCE_OUTCOME",
        "DOM_OUTCOME",
        "pages-propagation/san-telmo-attribution",
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

unwanted_domain = "awe" + "swell.com"

forbidden = {
    "en/san-telmo-ricpe-sun-park/index.html": [
        f"https://{unwanted_domain}/en/san-telmo-ricpe-sun-park/",
    ],
    "es/san-telmo-ricpe-sun-park/index.html": [
        f"https://{unwanted_domain}/es/san-telmo-ricpe-sun-park/",
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

# Keep the unwanted domain out of every tracked file, not only the San Telmo
# pages that originally carried stale canonical metadata.  The domain string is
# assembled above so this guard does not need to store the forbidden URL itself.
tracked_files = subprocess.run(
    ["git", "ls-files", "-z"],
    cwd=ROOT,
    check=True,
    capture_output=True,
).stdout.split(b"\0")
unwanted_domain_bytes = unwanted_domain.encode("ascii")
for tracked_file in tracked_files:
    if not tracked_file:
        continue
    relative_path = tracked_file.decode("utf-8")
    if unwanted_domain_bytes in (ROOT / relative_path).read_bytes().lower():
        failures.append(f"{relative_path}: unwanted domain reference remains")

if failures:
    raise SystemExit("SAN TELMO RENDERED ATTRIBUTION VALIDATION: FAIL\n" + "\n".join(f" - {failure}" for failure in failures))

print("SAN TELMO RENDERED ATTRIBUTION VALIDATION: PASS")
