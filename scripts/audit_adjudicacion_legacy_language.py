#!/usr/bin/env python3
"""Fail on stale public formulations superseded by the 2022-adjudication reconstruction.

The audit is deliberately narrow. It scans public HTML and runtime JavaScript, not private
working papers, archival controls or evidence registers. A hit means the public wording needs
human review; it does not decide the underlying legal question.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {
    ROOT / "assets" / "adjudicacion-provenance-cross-site-20260819.js",
}

RULES: list[tuple[str, re.Pattern[str]]] = [
    (
        "no-fourth-option-es",
        re.compile(r"\bno\s+(?:hay|existe)\s+(?:una\s+)?cuarta\s+(?:opci[oó]n|posibilidad)\b", re.I),
    ),
    (
        "no-fourth-option-en",
        re.compile(r"\bthere\s+is\s+no\s+fourth\s+(?:option|possibility)\b", re.I),
    ),
    (
        "amount-has-no-calculation-es",
        re.compile(
            r"13[.]168[.]082,02.{0,100}(?:carece|no\s+tiene|sin).{0,55}(?:c[aá]lculo|puente\s+aritm[eé]tico|explicaci[oó]n\s+aritm[eé]tica)",
            re.I | re.S,
        ),
    ),
    (
        "amount-has-no-calculation-en",
        re.compile(
            r"13,168,082[.]02.{0,100}(?:has\s+no|lacks|without).{0,55}(?:calculation|arithmetic\s+bridge|arithmetic\s+explanation)",
            re.I | re.S,
        ),
    ),
    (
        "automatic-waiver-surplus-es",
        re.compile(
            r"(?:condonaci[oó]n|deuda\s+condonada).{0,110}(?:autom[aá]ticamente|por\s+s[ií]\s+sola).{0,80}(?:sobrante|remanente|masa\s+activa)",
            re.I | re.S,
        ),
    ),
    (
        "automatic-waiver-surplus-en",
        re.compile(
            r"(?:waiver|waived\s+debt).{0,110}(?:automatically|by\s+itself).{0,80}(?:surplus|estate\s+proceeds)",
            re.I | re.S,
        ),
    ),
    (
        "automatic-downstream-collapse-es",
        re.compile(
            r"(?:todos|cada\s+uno\s+de)\s+los\s+actos\s+(?:posteriores|derivados).{0,70}(?:caen|desaparecen|son\s+nulos)\s+autom[aá]ticamente",
            re.I | re.S,
        ),
    ),
    (
        "automatic-downstream-collapse-en",
        re.compile(
            r"(?:all|every)\s+downstream\s+acts?.{0,70}(?:fall|disappear|are\s+void)\s+automatically",
            re.I | re.S,
        ),
    ),
    (
        "continuing-effects-no-timebar-es",
        re.compile(
            r"(?:no\s+(?:hay|existe)|sin)\s+(?:caducidad|prescripci[oó]n|plazo).{0,100}(?:efectos?\s+contin[uú]an|tracto\s+sucesivo)",
            re.I | re.S,
        ),
    ),
    (
        "continuing-effects-no-timebar-en",
        re.compile(
            r"(?:no\s+time\s+limit|cannot\s+expire|no\s+limitation).{0,100}(?:effects?\s+continue|continuing\s+effects)",
            re.I | re.S,
        ),
    ),
    (
        "protocol-457-retransferred-premises-es",
        re.compile(r"protocolo\s+457.{0,120}(?:volvi[oó]\s+a\s+transmitir|retransmiti[oó]).{0,70}locales", re.I | re.S),
    ),
    (
        "protocol-457-retransferred-premises-en",
        re.compile(r"protocol\s+457.{0,120}(?:retransferred|transferred\s+again).{0,70}premises", re.I | re.S),
    ),
]


def public_files() -> list[Path]:
    files: list[Path] = []
    for base, suffixes in ((ROOT / "es", {".html"}), (ROOT / "en", {".html"}), (ROOT / "assets", {".js"})):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix in suffixes and path not in EXCLUDED:
                files.append(path)
    return sorted(files)


def contextual_exception(rule_id: str, context: str) -> bool:
    lowered = context.lower()
    if rule_id.startswith("automatic-") and any(
        marker in lowered
        for marker in (
            "no se afirma",
            "no implica",
            "no nace",
            "no es",
            "does not claim",
            "does not imply",
            "does not arise",
            "not automatically",
        )
    ):
        return True
    if rule_id.startswith("protocol-457-") and any(
        marker in lowered
        for marker in (
            "no queda acreditada",
            "no se acredita",
            "no prueba",
            "is not established",
            "does not establish",
            "does not prove",
        )
    ):
        return True
    return False


def main() -> int:
    hits: list[dict[str, str | int]] = []
    scanned = 0
    for path in public_files():
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for rule_id, pattern in RULES:
            for match in pattern.finditer(text):
                start = max(0, match.start() - 180)
                end = min(len(text), match.end() + 180)
                context = re.sub(r"\s+", " ", text[start:end]).strip()
                if contextual_exception(rule_id, context):
                    continue
                hits.append(
                    {
                        "rule": rule_id,
                        "path": str(path.relative_to(ROOT)),
                        "offset": match.start(),
                        "match": re.sub(r"\s+", " ", match.group(0)).strip(),
                        "context": context,
                    }
                )

    report = {
        "audit": "adjudicacion-2022-legacy-language",
        "scanned_files": scanned,
        "status": "FAIL" if hits else "PASS",
        "hits": hits,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
