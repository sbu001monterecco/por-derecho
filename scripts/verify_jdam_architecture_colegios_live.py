from urllib.request import Request, urlopen
import time

BASE = "https://sbu001monterecco.github.io/por-derecho"
CHECKS = {
    "/es/arquitectura-nodo-documental-jdam/": ["26/008230", "22/000036/7800", "artículo 262 LECrim"],
    "/en/architecture-documentary-node-jdam/": ["26/008230", "22/000036/7800", "Article 262 LECrim"],
    "/assets/jdam-architecture-colegios-20260820.js": ["jdam-architecture-gateway"],
    "/assets/jdam-pwc-conocimiento-2016-ES.svg": ["PUNTO DE CONOCIMIENTO PROFESIONAL"],
    "/assets/jdam-san-telmo-ricpe-sun-park-ES.svg": ["EL DESPACHO"],
    "/sitemap-jdam-architecture.xml": ["arquitectura-nodo-documental-jdam"],
}

for attempt in range(12):
    failures = []
    for path, needles in CHECKS.items():
        try:
            request = Request(BASE + path, headers={"User-Agent": "Project-Sun-Rock-live-verifier/1.0"})
            with urlopen(request, timeout=20) as response:
                text = response.read().decode("utf-8", "replace")
            for needle in needles:
                if needle not in text:
                    failures.append(f"{path}: missing {needle}")
        except Exception as exc:
            failures.append(f"{path}: {exc}")
    if not failures:
        print("JDAM architecture public edge verified")
        break
    if attempt == 11:
        raise SystemExit("\n".join(failures))
    time.sleep(20)
