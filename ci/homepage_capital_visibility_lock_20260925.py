from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HOME_EN = ROOT / "en/index.html"
HOME_ES = ROOT / "es/index.html"
FUTURE_EN = ROOT / "en/future/index.html"
FUTURE_ES = ROOT / "es/futuro/index.html"

errors = []

for path in (HOME_EN, HOME_ES, FUTURE_EN, FUTURE_ES):
    if not path.exists():
        errors.append(f"missing required route: {path.relative_to(ROOT)}")

if not errors:
    en = HOME_EN.read_text(encoding="utf-8")
    es = HOME_ES.read_text(encoding="utf-8")
    future_en = FUTURE_EN.read_text(encoding="utf-8")
    future_es = FUTURE_ES.read_text(encoding="utf-8")

    if 'href="#future"' in en or 'href="#futuro"' in es:
        errors.append("Future/Futuro must navigate to standalone pages, not homepage anchors")
    if 'institutional-capital/' in en:
        errors.append("en/index.html must not link directly to institutional capital")
    if 'capital-institucional/' in es:
        errors.append("es/index.html must not link directly to capital institucional")
    if 'href="future/"' not in en:
        errors.append("en/index.html missing standalone Future route")
    if 'href="futuro/"' not in es:
        errors.append("es/index.html missing standalone Futuro route")
    if '../institutional-capital/' not in future_en:
        errors.append("en/future/index.html missing controlled onward institutional-capital route")
    if '../capital-institucional/' not in future_es:
        errors.append("es/futuro/index.html missing controlled onward capital-institucional route")

if errors:
    print("HOMEPAGE CAPITAL VISIBILITY LOCK: FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("HOMEPAGE CAPITAL VISIBILITY LOCK: PASS")
