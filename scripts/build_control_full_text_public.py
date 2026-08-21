#!/usr/bin/env python3
"""Build page-traceable, redacted public text editions for Controls 21/22/24.

The source PDFs are deliberately kept outside the public repository.  This script
records the exact source binary and page range used, extracts one page at a time
with pdftotext, applies the narrow public redactions below, and writes searchable
Markdown without modifying the source files.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    output: str
    title: str
    source: str
    source_sha256: str
    source_pages: int
    first_page: int
    last_page: int
    filing_note: str


DOCUMENTS = (
    Document(
        output="control-21/2026-06-25-complaint-full-text-public.md",
        title="Control 21 — denuncia de 25 de junio de 2026 — texto íntegro público",
        source="FINAL-IMPRIMIR_DENUNCIA_PENAL_DOCUMENTADA_Y_ANEXOS_25JUN2026_FINAL_CORREGIDO.pdf",
        source_sha256="ad3f6aea269649a46212967ddb05225fa160b6e93393e8896e001aa3570e5c08",
        source_pages=199,
        first_page=1,
        last_page=85,
        filing_note=(
            "Incluye la portada y el índice del paquete (páginas fuente 1–2) y el texto "
            "completo de la denuncia (páginas fuente 3–85). Los anexos comienzan en la "
            "página fuente 86 y se controlan por inventario, sin reproducirse aquí."
        ),
    ),
    Document(
        output="control-21/2026-07-09-filing-guide-full-text-public.md",
        title="Control 21 — guía judicial presentada el 9 de julio de 2026 — texto íntegro público",
        source="CONTROL21_FILE_THIS_DECANATO_09JUL2026_FINAL_FIRMA.pdf",
        source_sha256="2ef7366966178bab4848c77067c21170f0a3316639d30962201cd28a8172abe8",
        source_pages=492,
        first_page=1,
        last_page=6,
        filing_note=(
            "Guía de lectura que precede al escrito de ampliación dentro del paquete presentado. "
            "El escrito de ampliación comienza en la página fuente 7."
        ),
    ),
    Document(
        output="control-21/2026-07-09-ampliacion-full-text-public.md",
        title="Control 21 — ampliación de 9 de julio de 2026 — texto íntegro público",
        source="CONTROL21_FILE_THIS_DECANATO_09JUL2026_FINAL_FIRMA.pdf",
        source_sha256="2ef7366966178bab4848c77067c21170f0a3316639d30962201cd28a8172abe8",
        source_pages=492,
        first_page=7,
        last_page=25,
        filing_note=(
            "Texto completo del escrito de ampliación contenido en el paquete presentado; "
            "la página fuente 26 inicia el índice de anexos."
        ),
    ),
    Document(
        output="control-22/2026-06-18-complaint-full-text-public.md",
        title="Control 22 — denuncia presentada el 18 de junio de 2026 — texto íntegro público",
        source="01_Denuncia_Penal_AC_LPB_Sun_Park_AC-FINAL_17JUN2026.pdf",
        source_sha256="b11f10e7410f922a8cd1796ea462ea7ea20d555b7308e4481f2cb23732b1002b",
        source_pages=55,
        first_page=1,
        last_page=55,
        filing_note="Texto completo de las 55 páginas del escrito fuente.",
    ),
    Document(
        output="control-24/2026-06-18-complaint-full-text-public.md",
        title="Control 24 — denuncia presentada el 18 de junio de 2026 — texto íntegro público",
        source="02_Paquete_Unificado_Para_Presentacion_JUEZ_ FINAL 17JUNE2026 (signed).pdf",
        source_sha256="1cae1912a20202c5f5779db07e77c7e1d3f0ae514676e07d3ace4dd56f6f76a0",
        source_pages=79,
        first_page=1,
        last_page=30,
        filing_note=(
            "Incluye la hoja de presentación (páginas fuente 1–3) y el texto completo de "
            "la denuncia de 27 páginas (páginas fuente 4–30). Los anexos comienzan en la "
            "página fuente 31 y se controlan por inventario, sin reproducirse aquí."
        ),
    ),
    Document(
        output="control-24/2026-06-25-complement-full-text-public.md",
        title="Control 24 — aportación complementaria de 25 de junio de 2026 — texto íntegro público",
        source="APORTACION_COMPLEMENTARIA_CONTROL_24_25JUN2026.pdf",
        source_sha256="a552c10094a3bdbf21132f7083689d79bee39b8d51ed96de19090a3d638b7c48",
        source_pages=10,
        first_page=1,
        last_page=10,
        filing_note="Texto completo de las 10 páginas del escrito fuente.",
    ),
)


HEADER = """# {title}

> **Naturaleza:** transcripción pública, pesquisable y página por página de un escrito de parte.
> **Cautela:** contiene alegaciones y solicitudes de investigación; no expresa hechos probados ni una conclusión judicial o fiscal. Se preservan la presunción de inocencia, la contradicción y el derecho de rectificación.
> **Edición pública:** se han sustituido NIE/DNI, domicilios personales, correos, teléfonos y datos de firma por marcadores explícitos. El PDF fuente firmado o presentado no se publica y conserva su integridad fuera de Git.

## Control de fuente

- Archivo fuente privado: `{source}`
- SHA-256 del PDF fuente: `{source_sha256}`
- Extensión del PDF fuente: {source_pages} páginas
- Rango transcrito: páginas fuente {first_page}–{last_page}
- Nota de alcance: {filing_note}
- Método: extracción página por página con `pdftotext -layout`; redacción determinista; sin paráfrasis ni reordenación.

Los marcadores `[... REDACTADO ...]` son intervenciones editoriales. Los saltos de línea y caracteres proceden de la capa de texto del PDF y pueden reflejar artefactos de extracción; la numeración de página fuente permite cotejar cada pasaje con el original bajo custodia.
"""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def redact(text: str) -> str:
    # Personal service addresses identified by their procedural context.  The
    # literal address is intentionally not embedded in this public script.
    text = re.sub(
        r"(efectos de (?:comunicaciones|notificaciones) en )Calle[^\n]*"
        r"(?:\n\s*[^\n]*(?=\by correo electrónico))?",
        r"\1[DOMICILIO PERSONAL REDACTADO] ",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"(domicilio a efectos de (?:comunicaciones|notificaciones)(?: en|:)\s*)Calle[^\n]*",
        r"\1[DOMICILIO PERSONAL REDACTADO]",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"(?m)^(\s*)Calle[^\n]*(?=\n(?:[^\n]*correo electrónico|[^\n]*\[CORREO))",
        "[DOMICILIO PERSONAL REDACTADO]",
        text,
        flags=re.IGNORECASE,
    )

    # Contact and identifying data, including the identifiers of named respondents.
    text = re.sub(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        "[CORREO ELECTRÓNICO REDACTADO]",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\b(?:[XYZ][0-9]{7}[A-Z]|[0-9]{8}[A-Z])\b",
        "[NIE/DNI REDACTADO]",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"(?<!\d)(?:\+34[ -]?)?[6-9][0-9]{2}[ .-]?[0-9]{3}[ .-]?[0-9]{3}(?!\d)",
        "[TELÉFONO REDACTADO]",
        text,
    )

    # The extracted layer does not contain the handwritten image.  Mark its omission.
    text = re.sub(
        r"(Firma manuscrita del compareciente:\s*)",
        r"\1\n[FIRMA REDACTADA EN LA EDICIÓN PÚBLICA]\n",
        text,
        flags=re.IGNORECASE,
    )
    return text.rstrip()


def extract_page(source: Path, page_number: int) -> str:
    result = subprocess.run(
        [
            "pdftotext",
            "-layout",
            "-f",
            str(page_number),
            "-l",
            str(page_number),
            str(source),
            "-",
        ],
        check=True,
        capture_output=True,
    )
    return result.stdout.decode("utf-8", errors="replace").replace("\f", "")


def build(document: Document, source_dir: Path, output_dir: Path) -> None:
    source = source_dir / document.source
    if not source.is_file():
        raise FileNotFoundError(source)
    actual_hash = sha256(source)
    if actual_hash != document.source_sha256:
        raise RuntimeError(
            f"hash mismatch for {document.source}: {actual_hash} != {document.source_sha256}"
        )

    target = output_dir / document.output
    target.parent.mkdir(parents=True, exist_ok=True)
    parts = [
        HEADER.format(
            title=document.title,
            source=document.source,
            source_sha256=document.source_sha256,
            source_pages=document.source_pages,
            first_page=document.first_page,
            last_page=document.last_page,
            filing_note=document.filing_note,
        ).rstrip(),
    ]
    for page in range(document.first_page, document.last_page + 1):
        extracted = redact(extract_page(source, page))
        parts.append(
            f"## Página fuente {page} de {document.source_pages}\n\n"
            f"```text\n{extracted}\n```"
        )
    target.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("archive/controls"),
    )
    args = parser.parse_args()
    for document in DOCUMENTS:
        build(document, args.source_dir, args.output_dir)


if __name__ == "__main__":
    main()
