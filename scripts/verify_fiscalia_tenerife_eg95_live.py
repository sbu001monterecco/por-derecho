from pathlib import Path
from urllib.request import Request, urlopen
import json
import time

BASE = "https://sbu001monterecco.github.io/por-derecho"
ARTIFACT_DIR = Path("artifacts/fiscalia-tenerife-eg95-live")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

CHECKS = {
    "/es/fiscalia-tenerife-eg95-2026/": [
        "Expediente Gubernativo 95/2026",
        "archivo procedimental",
        "No acredita incorporación judicial",
    ],
    "/en/fiscalia-tenerife-eg95-2026/": [
        "Administrative File 95/2026",
        "procedural closure",
        "No proof of judicial incorporation",
    ],
    "/assets/fiscalia-eg95-propagation-20260823.js": [
        "data-eg95-dp748-update",
        "data-eg95-institutional-record",
        "data-eg95-update",
    ],
    "/assets/site-pre-intervencion-highlight-20260820.js": [
        "fiscalia-eg95-propagation-20260823.js",
        "site-pre-intervencion-highlight-before-eg95-20260823.js",
    ],
    "/sitemap-fiscalia-tenerife.xml": [
        "/es/fiscalia-tenerife-eg95-2026/",
        "/en/fiscalia-tenerife-eg95-2026/",
        "/es/fiscalia-tenerife-dp748/",
    ],
    "/robots.txt": ["sitemap-fiscalia-tenerife.xml"],
}

result = {"base": BASE, "attempts": [], "verified": False}

for attempt in range(36):
    failures = []
    observations = []
    cache_buster = f"eg95-live-{int(time.time())}-{attempt}"
    for path, needles in CHECKS.items():
        separator = "&" if "?" in path else "?"
        url = BASE + path + separator + cache_buster
        try:
            request = Request(
                url,
                headers={
                    "User-Agent": "Project-Sun-Rock-EG95-live-verifier/1.0",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                },
            )
            with urlopen(request, timeout=30) as response:
                status = response.status
                text = response.read().decode("utf-8", "replace")
            missing = [needle for needle in needles if needle not in text]
            observations.append(
                {"path": path, "status": status, "bytes": len(text.encode("utf-8")), "missing": missing}
            )
            for needle in missing:
                failures.append(f"{path}: missing {needle}")
        except Exception as exc:
            observations.append({"path": path, "error": str(exc)})
            failures.append(f"{path}: {exc}")

    result["attempts"].append({"attempt": attempt + 1, "failures": failures, "observations": observations})
    if not failures:
        result["verified"] = True
        result["successful_attempt"] = attempt + 1
        break
    if attempt < 35:
        time.sleep(15)

(ARTIFACT_DIR / "static-public-edge.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
)

if not result["verified"]:
    latest = result["attempts"][-1]["failures"]
    raise SystemExit("\n".join(latest))

print("Fiscalía Tenerife EG 95/2026 static public edge verified")
