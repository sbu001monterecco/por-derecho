#!/usr/bin/env python3
"""Validate the bilingual Cuatrecasas DP 748 / civil-action publication."""
from __future__ import annotations

import json
import hashlib
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "cuatrecasas-dp748-civil-action-20260824"
ACCOUNTABILITY_MARKER = "CUATRECASAS-INSTITUTIONAL-ACCOUNTABILITY-20260824"
COMPARATOR_MARKER = "cuatrecasas-edgeworth-partial-overlap-20260824"

ROUTES = {
    "es/cuatrecasas-dp748-accion-civil/index.html": [
        MARKER,
        "La tesis causal, sin sustitución de responsables",
        "DP 748/2026 no es la acción civil",
        "hipótesis principal y concreta",
        "Alcance público de la vía civil contemplada",
        "estimación parcial por insuficiencia de la motivación concreta",
        "No se persigue acción judicial británica",
        "no tiene actualmente contratado a ningún despacho británico para tales acciones",
        "omite deliberadamente los nombres",
        ACCOUNTABILITY_MARKER,
        "Un requerimiento institucional contestable mediante documentos",
        "registrará únicamente como <em>no contestado</em>",
        "Vías de responsabilidad con eje en España",
    ],
    "en/cuatrecasas-dp748-civil-action/index.html": [
        MARKER,
        "The causal thesis, without substituting defendants",
        "DP 748/2026 is not the civil action",
        "leading concrete hypothesis",
        "Public scope of the contemplated civil route",
        "partial allowance because the dismissal’s specific reasoning was insufficient",
        "No UK court action is being pursued",
        "no UK firm is currently instructed for such proceedings",
        "deliberately omits the names",
        ACCOUNTABILITY_MARKER,
        "A document-answerable institutional challenge",
        "recorded only as <em>unanswered</em>",
        "Spain-led accountability routes",
    ],
}

# One-way digests keep the controlled identities out of the public repository
# while preserving a negative publication test for two- and three-word phrases.
CONTROLLED_IDENTITY_HASHES = {
    "bf109170a1c97237d2200966e955202ec47e8dbb84774c47c4d2398b6e662c78",
    "8116237652d0a8381e13b2fc0d41f791dbefcb1b7677f0d4a35903db9772abe9",
    "24303b19997972677adfac4dcd37840f26d3564c30a3295477746ed94be25d42",
    "d43cff9be035963ce976a8fb2cd14abfede3627d19c7f7c7e9d32e02ecf1dfae",
    "75c5af18e9497cb198a0716cdb1671b69f88f352f348db6e7d3415fbaadc9278",
    "19d0f2cb66ed83896c14267ad0d692fd70a5fc79a637aafa148463be0232c9a0",
}


def leaks_controlled_identity(text: str) -> bool:
    tokens = re.findall(r"[^\W\d_]+", html.unescape(text).casefold(), flags=re.UNICODE)
    for width in (2, 3):
        for offset in range(len(tokens) - width + 1):
            phrase = " ".join(tokens[offset : offset + width])
            digest = hashlib.sha256(phrase.encode("utf-8")).hexdigest()
            if digest in CONTROLLED_IDENTITY_HASHES:
                return True
    return False

errors: list[str] = []
texts: dict[str, str] = {}
for rel, markers in ROUTES.items():
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing route: {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    texts[rel] = text
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel}: missing marker {marker!r}")
    if leaks_controlled_identity(text):
        errors.append(f"{rel}: controlled current-team identity leaked")

COMPARATOR_ROUTES = {
    "en/cuatrecasas-edgeworth-comparator/index.html": (
        COMPARATOR_MARKER,
        "A comparator is not evidence. It can identify the questions that deserve an answer",
        "What the UK judgment establishes—and what it does not",
        "Similar professional-liability questions; different cases",
        "No pattern or propensity inference",
        "Two independent proof chains",
        "Separate records stay separate",
        "Edgeworth's evidence is not relied upon as evidence of the Sun Rock/Aweswell case",
        "The UK legal route is not being pursued",
        "no UK firm is currently instructed for such proceedings",
        "Any SRA consideration is a distinct, secondary and jurisdiction-dependent regulatory question",
        "What we are asking Cuatrecasas to do now",
        "independent proof · open resolution lane",
    ),
    "es/comparador-cuatrecasas-edgeworth/index.html": (
        COMPARATOR_MARKER,
        "Un comparador no es prueba. Puede identificar las preguntas que merecen respuesta",
        "Qué establece la resolución británica y qué no",
        "Preguntas similares de responsabilidad profesional; asuntos distintos",
        "Sin inferencia de patrón o propensión",
        "Dos cadenas probatorias independientes",
        "Los expedientes separados permanecen separados",
        "La prueba de Edgeworth no se utiliza como prueba del asunto Sun Rock/Aweswell",
        "La vía judicial británica no se persigue",
        "no tiene actualmente contratado a ningún despacho británico para tales acciones",
        "Cualquier consideración sobre la SRA es una cuestión regulatoria distinta, secundaria y dependiente de jurisdicción",
        "Qué estamos pidiendo ahora a Cuatrecasas",
        "prueba independiente · vía abierta para resolver",
    ),
}
for rel, markers in COMPARATOR_ROUTES.items():
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing comparator route: {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel}: missing comparator marker {marker!r}")
    if leaks_controlled_identity(text):
        errors.append(f"{rel}: controlled current-team identity leaked")
    if text.count("BL-2024-000237") < 2 or text.count("[2025] EWHC 1014 (Ch)") < 2:
        errors.append(f"{rel}: comparator case identity is not repeated in route and source record")

UK_STATUS_ROUTES = {
    "en/cuatrecasas-edgeworth-comparator/index.html": (
        "Sun Rock/Aweswell is not pursuing UK legal proceedings",
        "No UK court action is being pursued",
    ),
    "es/comparador-cuatrecasas-edgeworth/index.html": (
        "Sun Rock/Aweswell no persigue acciones judiciales en el Reino Unido",
        "No se persigue acción judicial británica",
    ),
    "en/cuatrecasas-dp748-civil-action/index.html": (
        "Sun Rock/Aweswell is not pursuing UK legal proceedings",
        "No UK court action is being pursued",
    ),
    "es/cuatrecasas-dp748-accion-civil/index.html": (
        "Sun Rock/Aweswell no persigue acciones judiciales en el Reino Unido",
        "No se persigue acción judicial británica",
    ),
    "en/why-the-uk-should-care/index.html": (
        "UK public-interest, evidence and investment relevance does not mean UK litigation",
        "Sun Rock/Aweswell is not pursuing UK court proceedings",
    ),
    "es/por-que-debe-importar-al-reino-unido/index.html": (
        "el interés público, probatorio e inversor británico no significa litigio británico",
        "Sun Rock/Aweswell no persigue procedimientos judiciales en el Reino Unido",
    ),
    "en/recovery-restitution-objectives/index.html": (
        "no UK legal action is being pursued",
    ),
    "es/objetivos-recuperacion-restitucion/index.html": (
        "no se persigue acción judicial en el Reino Unido",
    ),
}
STALE_UK_STATUS_PHRASES = (
    "our contemplated UK route",
    "contemplated UK route",
    "contemplated UK legal action",
    "no issued UK claim is asserted",
    "no issued UK claim",
    "potential UK litigation",
    "UK litigation remains under consideration",
    "UK claim remains under consideration",
    "nuestra vía británica contemplada",
    "vía judicial británica contemplada",
    "acción judicial británica contemplada",
    "no se afirma la presentación de una demanda británica",
    "posible litigio británico",
    "el litigio británico sigue bajo consideración",
    "la demanda británica sigue bajo consideración",
    "The UK case is strongest",
    "El caso británico es más sólido",
)
for rel, current_markers in UK_STATUS_ROUTES.items():
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing UK-status route: {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    for current_marker in current_markers:
        if current_marker not in text:
            errors.append(f"{rel}: missing definitive UK-route status {current_marker!r}")
    folded_text = text.casefold()
    for stale_phrase in STALE_UK_STATUS_PHRASES:
        if stale_phrase.casefold() in folded_text:
            errors.append(f"{rel}: stale UK-route wording remains {stale_phrase!r}")

UNITARY_ROUTES = {
    "en/cuatrecasas-sun-park/index.html": (
        "real and substantial opportunity",
        "2017 denominator",
        "What “proper performance could have avoided this” can responsibly mean",
    ),
    "es/cuatrecasas-sun-park/index.html": (
        "oportunidad real y sustancial",
        "Denominador 2017",
        "Qué puede significar responsablemente «una actuación correcta pudo evitarlo»",
    ),
}
for rel, markers in UNITARY_ROUTES.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel}: missing unitary causation marker {marker!r}")
    if leaks_controlled_identity(text):
        errors.append(f"{rel}: controlled current-team identity leaked")

GAP_ROUTES = {
    "en/cuatrecasas-critical-gaps/index.html": (
        "Critical · CG-010",
        "Silence or non-response is recorded only as unanswered",
    ),
    "es/cuatrecasas-brechas-criticas/index.html": (
        "Crítica · CG-010",
        "El silencio o falta de respuesta se registra solo como no contestado",
    ),
}
for rel, markers in GAP_ROUTES.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel}: missing pressure-control marker {marker!r}")
    if leaks_controlled_identity(text):
        errors.append(f"{rel}: controlled current-team identity leaked")

pressure_control = ROOT / "archive/CUATRECASAS_MAXIMUM_PERMISSIBLE_INSTITUTIONAL_ACCOUNTABILITY_24AUG2026.md"
if not pressure_control.is_file():
    errors.append("missing institutional-accountability control")
else:
    pressure_text = pressure_control.read_text(encoding="utf-8")
    for marker in (
        "cuatrecasas-institutional-accountability-20260824",
        "Silence, refusal or absence of a public answer",
        "The civil and professional-liability strategy is Spain-led",
    ):
        if marker not in pressure_text:
            errors.append(f"institutional-accountability control missing {marker!r}")

comparator_control = ROOT / "archive/CUATRECASAS_EDGEWORTH_PARTIAL_OVERLAP_CONTROL_24AUG2026.md"
if not comparator_control.is_file():
    errors.append("missing Edgeworth partial-overlap control")
else:
    comparator_text = comparator_control.read_text(encoding="utf-8")
    for marker in (
        COMPARATOR_MARKER,
        "Parallel questions may exist; duty, evidence, causation, loss and procedural control remain independent",
        "does not establish an executed claimant-to-claimant cooperation",
        "No new cross-matter exchange or communication is authorised",
        "No proposition may use the Edgeworth case to prove pattern",
    ):
        if marker not in comparator_text:
            errors.append(f"Edgeworth comparator control missing {marker!r}")

required_shared = (
    "Acosta Matos",
    "DP 748/2026",
    "ETJ 163/2020",
    "KYC/AML",
    "SRA",
)
for marker in required_shared:
    for rel, text in texts.items():
        if marker not in text:
            errors.append(f"{rel}: missing shared proposition {marker!r}")

for rel in (
    "sitemap.xml",
    "sitemap-legal-advisers.xml",
    "README.md",
    "assets/data/unitary-route-registry-v1.json",
    "assets/data/unitary-route-registry-sync-20260819.json",
):
    text = (ROOT / rel).read_text(encoding="utf-8")
    for slug in (
        "cuatrecasas-dp748-accion-civil",
        "cuatrecasas-dp748-civil-action",
        "comparador-cuatrecasas-edgeworth",
        "cuatrecasas-edgeworth-comparator",
    ):
        if slug not in text:
            errors.append(f"{rel}: missing route {slug}")

manifest_path = ROOT / "publication-manifests/cuatrecasas-dp748-civil-action-20260824.json"
try:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("control_marker") != MARKER:
        errors.append("publication manifest marker mismatch")
    expected_routes = {
        route
        for language_routes in manifest.get("expected_routes", {}).values()
        for route in language_routes
    }
    for rel in (*ROUTES, *UNITARY_ROUTES, *GAP_ROUTES, *COMPARATOR_ROUTES):
        if rel not in expected_routes:
            errors.append(f"publication manifest omits affected route {rel}")
except Exception as exc:
    errors.append(f"invalid publication manifest: {exc}")

if errors:
    print("CUATRECASAS DP748 / CIVIL ACTION: FAIL")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print("CUATRECASAS DP748 / CIVIL ACTION: PASS (8 public routes across 4 bilingual pairs; comparator and privacy locks active)")
