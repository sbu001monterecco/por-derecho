from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
JS_PATH = ROOT / "assets/jdam-architecture-colegios-20260820.js"
CONTROL_DATE = "2026-08-20"


def extract_template(source: str, name: str) -> str:
    pattern = rf"const {re.escape(name)} = \(\) => `(.*?)`;"
    match = re.search(pattern, source, flags=re.S)
    if not match:
        raise RuntimeError(f"Template {name!r} not found in {JS_PATH}")
    template = match.group(1).strip()
    if "${" in template:
        raise RuntimeError(f"Template {name!r} contains runtime interpolation and cannot be used statically")
    return template


def article(inner: str, element_id: str) -> str:
    return (
        f'<article class="ir-record jdam-ir-current" id="{element_id}" '
        f'data-jdam-institutional-parity="{CONTROL_DATE}">{inner}</article>'
    )


def replace_article(source: str, element_id: str, replacement: str) -> str:
    pattern = (
        rf'<article class="ir-record(?: jdam-ir-current)?" id="{re.escape(element_id)}"'
        rf'(?: data-jdam-institutional-parity="[^"]+")?>.*?</article>'
    )
    updated, count = re.subn(pattern, replacement, source, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"Expected one #{element_id} article; replaced {count}")
    return updated


def synchronise(path: Path, coagc_template: str, coalz_template: str) -> None:
    source = path.read_text(encoding="utf-8")
    source = replace_article(source, "coagc", article(coagc_template, "coagc"))
    source = replace_article(source, "coa-lanzarote", article(coalz_template, "coa-lanzarote"))

    required = [
        'data-jdam-institutional-parity="2026-08-20"',
        "26/008230",
        "26/008474",
        "26/008476",
        "21428",
        "2315",
        "262 LECrim",
    ]
    for token in required:
        if token not in source:
            raise RuntimeError(f"{token!r} missing after synchronising {path}")
    if source.count('data-jdam-institutional-parity="2026-08-20"') != 2:
        raise RuntimeError(f"Unexpected parity-marker count in {path}")

    path.write_text(source, encoding="utf-8")


def main() -> None:
    js = JS_PATH.read_text(encoding="utf-8")
    synchronise(
        ROOT / "es/registros-institucionales/index.html",
        extract_template(js, "spanishCoagc"),
        extract_template(js, "spanishCoalz"),
    )
    synchronise(
        ROOT / "en/institutional-records/index.html",
        extract_template(js, "englishCoagc"),
        extract_template(js, "englishCoalz"),
    )
    print("Static COAGC/COALZ institutional records synchronised")


if __name__ == "__main__":
    main()
