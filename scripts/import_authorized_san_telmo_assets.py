#!/usr/bin/env python3
"""One-time, source-controlled import of the user-authorized San Telmo visual assets.

This script does not identify anyone from facial appearance. It decodes the exact
base64 staging files authorized by the user, verifies their SHA-256 values, keeps
the existing canonical Borja asset, and creates a portable self-contained SVG.
"""

from __future__ import annotations

import base64
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / ".asset-import"
EDUARDO_OUT = ROOT / "assets/actors/eduardo-sanchez-san-telmo.webp"
SUNPARK_OUT = ROOT / "assets/places/sun-park-mynd-yaiza--user-authorized-20260819.jpg"
BORJA = ROOT / "assets/actors/francisco-de-borja-rodriguez-batllori.jpg"
SVG_OUT = ROOT / "assets/composites/san-telmo-ricpe-sun-park-stamp-v1.svg"

EXPECTED = {
    EDUARDO_OUT: "a46afb994e6fa0fb309d43fff45b72923a75db39680abc01e10a0c13a52af7d6",
    SUNPARK_OUT: "91fb8e8bff10b76296d2abdb27f2733bd6faa99666941d0c22a2d631c369110d",
}


def decode_chunks(pattern: str, destination: Path) -> None:
    chunks = sorted(STAGING.glob(pattern))
    if not chunks:
        raise RuntimeError(f"No staging chunks matched {pattern!r}")
    encoded = "".join(chunk.read_text(encoding="ascii") for chunk in chunks)
    encoded = "".join(encoded.split())
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(base64.b64decode(encoded, validate=True))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def make_svg() -> str:
    eduardo = data_uri(EDUARDO_OUT, "image/webp")
    sunpark = data_uri(SUNPARK_OUT, "image/jpeg")
    borja = data_uri(BORJA, "image/jpeg")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 2400 1600" role="img" aria-labelledby="title desc">
<title id="title">San Telmo, RIC Private Equity and Sun Park documentary collision</title>
<desc id="desc">Eduardo Sánchez on the left, Sun Park in the centre and Francisco de Borja Rodríguez-Batllori Laffitte, Insolvency Administrator, on the right. The source-controlled statement records that Eduardo Sánchez stated the firm put clients into the RICPE investment connected to Sun Park. It does not by itself prove coordination, information transfer, unlawfulness or liability.</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fffdf8"/><stop offset="1" stop-color="#efe5d4"/></linearGradient>
  <linearGradient id="red" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7e1013"/><stop offset="1" stop-color="#bd2026"/></linearGradient>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#24090a" flood-opacity=".24"/></filter>
  <clipPath id="e"><rect x="62" y="500" width="524" height="390" rx="3"/></clipPath>
  <clipPath id="s"><rect x="860" y="500" width="680" height="390" rx="3"/></clipPath>
  <clipPath id="b"><rect x="1814" y="500" width="524" height="390" rx="3"/></clipPath>
</defs>
<rect width="2400" height="1600" fill="url(#bg)"/>
<rect width="2400" height="250" fill="#0c1116"/>
<text x="1200" y="68" text-anchor="middle" fill="#fff" font-family="Inter,Arial,sans-serif" font-size="53" font-weight="900">San Telmo partner Eduardo Sánchez stated that “el despacho”</text>
<text x="1200" y="132" text-anchor="middle" fill="#fff" font-family="Inter,Arial,sans-serif" font-size="53" font-weight="900">put clients into the RICPE investment connected to Sun Park.</text>
<text x="1200" y="190" text-anchor="middle" fill="#d7aa52" font-family="Inter,Arial,sans-serif" font-size="35" font-weight="800">El socio de San Telmo Eduardo Sánchez manifestó que «el despacho»</text>
<text x="1200" y="232" text-anchor="middle" fill="#d7aa52" font-family="Inter,Arial,sans-serif" font-size="35" font-weight="800">metió clientes en la inversión RICPE conectada con Sun Park.</text>
<rect y="250" width="2400" height="105" fill="url(#red)"/>
<text x="1200" y="295" text-anchor="middle" fill="#fff" font-family="Inter,Arial,sans-serif" font-size="34" font-weight="900">ONE HOTEL. ONE SAN TELMO PROFESSIONAL PERIMETER. TWO PARALLEL PROFESSIONAL LIVES.</text>
<text x="1200" y="337" text-anchor="middle" fill="#f0cf91" font-family="Inter,Arial,sans-serif" font-size="27" font-weight="800">UN MISMO HOTEL. UN MISMO PERÍMETRO PROFESIONAL SAN TELMO. DOS VIDAS PROFESIONALES EN PARALELO.</text>

<g filter="url(#shadow)"><rect x="50" y="385" width="548" height="520" rx="14" fill="#fffaf2" stroke="#0c1116" stroke-width="5"/><rect x="50" y="385" width="548" height="115" rx="14" fill="#0c1116"/><rect x="50" y="486" width="548" height="14" fill="#0c1116"/><text x="324" y="430" text-anchor="middle" fill="#fff" font-family="Inter,Arial,sans-serif" font-size="31" font-weight="900">EDUARDO SÁNCHEZ</text><text x="324" y="470" text-anchor="middle" fill="#d7aa52" font-family="Inter,Arial,sans-serif" font-size="23" font-weight="800">SAN TELMO PARTNER / SOCIO DE SAN TELMO</text><image x="62" y="500" width="524" height="390" preserveAspectRatio="xMidYMid slice" clip-path="url(#e)" href="{eduardo}" xlink:href="{eduardo}"/><rect x="62" y="500" width="524" height="390" fill="none" stroke="#d7aa52" stroke-width="5"/></g>
<g filter="url(#shadow)"><rect x="848" y="385" width="704" height="520" rx="14" fill="#fffaf2" stroke="#0c1116" stroke-width="5"/><rect x="848" y="385" width="704" height="115" rx="14" fill="#0c1116"/><rect x="848" y="486" width="704" height="14" fill="#0c1116"/><text x="1200" y="430" text-anchor="middle" fill="#fff" font-family="Inter,Arial,sans-serif" font-size="31" font-weight="900">SUN PARK / MYND YAIZA</text><text x="1200" y="470" text-anchor="middle" fill="#d7aa52" font-family="Inter,Arial,sans-serif" font-size="23" font-weight="800">THE SAME HOTEL / EL MISMO HOTEL</text><image x="860" y="500" width="680" height="390" preserveAspectRatio="xMidYMid slice" clip-path="url(#s)" href="{sunpark}" xlink:href="{sunpark}"/><rect x="860" y="500" width="680" height="390" fill="none" stroke="#d7aa52" stroke-width="5"/></g>
<g filter="url(#shadow)"><rect x="1802" y="385" width="548" height="520" rx="14" fill="#fffaf2" stroke="#0c1116" stroke-width="5"/><rect x="1802" y="385" width="548" height="115" rx="14" fill="#0c1116"/><rect x="1802" y="486" width="548" height="14" fill="#0c1116"/><text x="2076" y="417" text-anchor="middle" fill="#fff" font-family="Inter,Arial,sans-serif" font-size="25" font-weight="900">FRANCISCO DE BORJA</text><text x="2076" y="449" text-anchor="middle" fill="#fff" font-family="Inter,Arial,sans-serif" font-size="25" font-weight="900">RODRÍGUEZ-BATLLORI LAFFITTE</text><text x="2076" y="480" text-anchor="middle" fill="#d7aa52" font-family="Inter,Arial,sans-serif" font-size="19" font-weight="800">ADMINISTRADOR CONCURSAL / INSOLVENCY ADMINISTRATOR</text><image x="1814" y="500" width="524" height="390" preserveAspectRatio="xMidYMid meet" clip-path="url(#b)" href="{borja}" xlink:href="{borja}"/><rect x="1814" y="500" width="524" height="390" fill="none" stroke="#d7aa52" stroke-width="5"/></g>

<path d="M620 600 H785 V548 L840 645 L785 742 V690 H620 Z" fill="#bd2026"/><text x="718" y="618" text-anchor="middle" fill="#fff" font-family="Inter,Arial,sans-serif" font-size="27" font-weight="900">RICPE</text><text x="718" y="654" text-anchor="middle" fill="#fff" font-family="Inter,Arial,sans-serif" font-size="24" font-weight="800">investment /</text><text x="718" y="688" text-anchor="middle" fill="#fff" font-family="Inter,Arial,sans-serif" font-size="24" font-weight="800">inversión RICPE</text>
<line x1="1575" y1="645" x2="1760" y2="645" stroke="#0c1116" stroke-width="14" stroke-dasharray="22 14"/><path d="M1760 615 L1800 645 L1760 675 Z" fill="#0c1116"/><text x="1680" y="718" text-anchor="middle" fill="#0c1116" font-family="Inter,Arial,sans-serif" font-size="24" font-weight="900">CONCURSO 36/2012</text><text x="1680" y="752" text-anchor="middle" fill="#0c1116" font-family="Inter,Arial,sans-serif" font-size="22" font-weight="800">insolvency / concurso</text>

<rect x="120" y="930" width="2160" height="190" rx="18" fill="#fff" stroke="#9f1518" stroke-width="6"/><text x="1200" y="1010" text-anchor="middle" fill="#9f1518" font-family="Inter,Arial,sans-serif" font-size="65" font-weight="900">“EL DESPACHO” / “THE FIRM”</text><text x="1200" y="1078" text-anchor="middle" fill="#0c1116" font-family="Inter,Arial,sans-serif" font-size="35" font-weight="800">put clients into the RICPE investment / metió clientes en la inversión RICPE</text>
<rect y="1130" width="2400" height="170" fill="#0c1116"/><circle cx="120" cy="1215" r="56" fill="none" stroke="#d7aa52" stroke-width="8"/><text x="120" y="1245" text-anchor="middle" fill="#d7aa52" font-family="Inter,Arial,sans-serif" font-size="80" font-weight="900">?</text><text x="210" y="1195" fill="#fff" font-family="Inter,Arial,sans-serif" font-size="34" font-weight="900">What conflict, file-separation, KYC, access and information controls existed — and where are the records?</text><text x="210" y="1255" fill="#d7aa52" font-family="Inter,Arial,sans-serif" font-size="29" font-weight="800">¿Qué controles de conflicto, separación de expedientes, KYC, acceso e información existían — y dónde están los registros?</text>
<rect y="1300" width="2400" height="300" fill="#d7aa52"/><rect y="1300" width="2400" height="12" fill="#0c1116"/><text x="105" y="1370" fill="#0c1116" font-family="Inter,Arial,sans-serif" font-size="30" font-weight="900">SOURCE-CONTROLLED DIRECT STATEMENT. This establishes the contemporaneous San Telmo–RICPE–Sun Park connection</text><text x="105" y="1412" fill="#0c1116" font-family="Inter,Arial,sans-serif" font-size="30" font-weight="900">and the need to reconcile the records.</text><text x="105" y="1462" fill="#0c1116" font-family="Inter,Arial,sans-serif" font-size="27" font-weight="800">It does not by itself establish Borja–Eduardo coordination, transfer of insolvency information, unlawfulness or liability.</text><text x="105" y="1512" fill="#2d2417" font-family="Inter,Arial,sans-serif" font-size="26" font-weight="800">MANIFESTACIÓN DIRECTA CONTROLADA POR FUENTES. Acredita la conexión contemporánea San Telmo–RICPE–Sun Park</text><text x="105" y="1550" fill="#2d2417" font-family="Inter,Arial,sans-serif" font-size="26" font-weight="700">y exige conciliar los registros. No acredita por sí sola coordinación, transmisión de información, ilicitud ni responsabilidad.</text><rect y="1570" width="2400" height="30" fill="#0c1116"/>
</svg>'''


def main() -> int:
    trigger = STAGING / "trigger.txt"
    if not trigger.exists():
        print("Authorized asset trigger already consumed; nothing to import.")
        return 0
    if not BORJA.is_file():
        raise RuntimeError(f"Canonical Borja asset is missing: {BORJA.relative_to(ROOT)}")

    decode_chunks("eduardo.*.b64", EDUARDO_OUT)
    decode_chunks("sunpark.*.b64", SUNPARK_OUT)
    for path, expected in EXPECTED.items():
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"SHA-256 mismatch for {path.relative_to(ROOT)}: {actual} != {expected}")

    SVG_OUT.parent.mkdir(parents=True, exist_ok=True)
    SVG_OUT.write_text(make_svg(), encoding="utf-8")
    if SVG_OUT.stat().st_size < 50_000:
        raise RuntimeError("Generated SVG is unexpectedly small; embedded image data may be missing.")

    print(f"Imported {EDUARDO_OUT.relative_to(ROOT)}: {sha256(EDUARDO_OUT)}")
    print(f"Imported {SUNPARK_OUT.relative_to(ROOT)}: {sha256(SUNPARK_OUT)}")
    print(f"Generated {SVG_OUT.relative_to(ROOT)}: {sha256(SVG_OUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
