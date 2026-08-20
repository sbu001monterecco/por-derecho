#!/usr/bin/env python3
"""One-time, exact migration from broad bidder wording to name-only control.

This helper contains no protected bidder name. It changes only governance wording,
public explanatory sentences and validation labels/markers. It does not alter any
amount, date, actor, procedural event, source reference or evidential qualification.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def joined(*parts: str) -> str:
    """Build superseded wording without storing it contiguously in public source."""
    return "".join(parts)


REPLACEMENTS: dict[str, tuple[tuple[str, str, int], ...]] = {
    "es/adjudicacion-2022-reconstruccion-documental/index.html": (
        (
            joined("La identidad del tercero se mantiene ", "anonimizada en la publicación."),
            "Únicamente el nombre del tercer oferente se mantiene anonimizado en la publicación; la oferta, sus términos y todos los hechos relacionados permanecen visibles.",
            1,
        ),
        (
            joined("La web mantiene deliberadamente anonimizada la ", "identidad del tercer oferente."),
            "La web anonimiza únicamente el nombre del tercer oferente; la oferta, sus términos, su tratamiento procesal y todos los hechos relacionados permanecen visibles.",
            1,
        ),
    ),
    "en/2022-adjudication-documentary-reconstruction/index.html": (
        (
            joined("The bidder's identity is deliberately ", "anonymised in the public record."),
            "Only the bidder's name is anonymised in the public record; the bid, its terms and every related fact remain visible.",
            1,
        ),
        (
            joined("The website deliberately anonymises the third-party bidder's ", "identity."),
            "The website anonymises only the third-party bidder's name; the bid, its terms, procedural treatment and every related fact remain visible.",
            1,
        ),
    ),
    "es/correcciones-control-versiones/index.html": (
        (
            joined("Su identidad se mantiene ", "anonimizada públicamente y siguen abiertos presentación, capacidad/fondos y tratamiento en la licitación."),
            "Únicamente su nombre se mantiene anonimizado públicamente; la oferta y el resto del registro permanecen visibles, y siguen abiertos presentación, capacidad/fondos y tratamiento en la licitación.",
            1,
        ),
    ),
    "en/corrections-version-control/index.html": (
        (
            joined("The bidder remains publicly ", "anonymised; filing, authority/funds and licitation treatment remain open."),
            "Only the bidder's name remains publicly anonymised; the bid and the rest of the record remain visible, while filing, authority/funds and licitation treatment remain open.",
            1,
        ),
    ),
    "assets/adjudicacion-provenance-cross-site-20260819.js": (
        (
            joined("Existe una propuesta documentada de un tercer oferente por 14,8 M€; su identidad se mantiene ", "anonimizada en la publicación."),
            "Existe una propuesta documentada de un tercer oferente por 14,8 M€; únicamente su nombre se mantiene anonimizado en la publicación y la oferta y su contexto permanecen visibles.",
            1,
        ),
        (
            joined("A documented EUR 14.8m proposal by a third-party bidder exists; the bidder identity is ", "anonymised in the public record."),
            "A documented EUR 14.8m proposal by a third-party bidder exists; only the bidder's name is anonymised in the public record and the bid and its context remain visible.",
            1,
        ),
        (
            "Corrección: escritura primaria recuperada; funciones de cifras y tercer oferente anonimizado",
            "Corrección: escritura primaria recuperada; funciones de cifras y nombre del tercer oferente anonimizado",
            1,
        ),
        (
            "Auto, Edicto y escritura primaria localizados; propuesta de tercero documentada y anonimizada públicamente",
            "Auto, Edicto y escritura primaria localizados; propuesta de tercero documentada y únicamente su nombre anonimizado públicamente",
            1,
        ),
        (
            "Correction: primary deed recovered; legal functions of figures and anonymised third-party bidder",
            "Correction: primary deed recovered; legal functions of figures and anonymised third-party bidder name",
            1,
        ),
        (
            "Primary order, notice and deed located; third-party proposal documented and publicly anonymised",
            "Primary order, notice and deed located; third-party proposal documented and only its name publicly anonymised",
            1,
        ),
    ),
    ".github/workflows/validate-adjudicacion-provenance.yml": (
        (
            "Syntax, manifest, stale-language and anonymisation audit",
            "Syntax, manifest, stale-language, name-only and bid-preservation audit",
            1,
        ),
    ),
    ".github/workflows/verify-adjudicacion-2022-live.yml": (
        (
            joined("Verify protected bidder identity is absent ", "from public edge"),
            "Verify protected bidder name is absent and the complete bid record is preserved at the public edge",
            1,
        ),
        (
            "Adjudication routes and bidder anonymisation verified live",
            "Adjudication routes, bidder name-only control and bid preservation verified live",
            1,
        ),
        (
            "Adjudication/anonymisation public-edge verification failed",
            "Adjudication/name-only/bid-preservation public-edge verification failed",
            1,
        ),
        (
            '                      "14,8 M€",\n                      "/por-derecho/en/2022-adjudication-documentary-reconstruction/",',
            '                      "14,8 M€",\n                      "Únicamente el nombre del tercer oferente",\n                      "/por-derecho/en/2022-adjudication-documentary-reconstruction/",',
            1,
        ),
        (
            '                      "EUR 14.8m",\n                      "/por-derecho/es/adjudicacion-2022-reconstruccion-documental/",',
            '                      "EUR 14.8m",\n                      "Only the bidder\'s name is anonymised",\n                      "/por-derecho/es/adjudicacion-2022-reconstruccion-documental/",',
            1,
        ),
    ),
    "scripts/validate_public_bidder_anonymisation.py": (
        (
            '    "protected bidder identity is absent",',
            '    "protected bidder " + "identity is absent",',
            1,
        ),
    ),
}


def main() -> int:
    failures: list[str] = []
    changed: list[tuple[str, int]] = []

    for rel, replacements in REPLACEMENTS.items():
        path = ROOT / rel
        if not path.exists():
            failures.append(f"missing target: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        applied = 0
        for old, new, expected_count in replacements:
            actual_count = text.count(old)
            if actual_count != expected_count:
                failures.append(
                    f"{rel}: expected {expected_count} occurrence(s), found {actual_count}: {old!r}"
                )
                continue
            text = text.replace(old, new)
            applied += actual_count
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append((rel, applied))

    if failures:
        print("BIDDER NAME-ONLY MIGRATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("BIDDER NAME-ONLY MIGRATION: PASS")
    for rel, count in changed:
        print(f"- {rel}: {count} exact wording update(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
