"""Offline structural check for this generic public package; no private files read."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


def main() -> int:
    root = Path(__file__).resolve().parent
    try:
        svg = ET.parse(root / 'visual-disclosure-key.svg').getroot()
        ns = {'s': 'http://www.w3.org/2000/svg'}
        for tag in ('title', 'desc'):
            element = svg.find(f's:{tag}', ns)
            if element is None or not ''.join(element.itertext()).strip():
                raise ValueError(f'SVG needs a nonempty {tag}')
        text = ' '.join(svg.itertext())
        for label in ('ACTUAL PHOTOGRAPH', 'HISTORICAL DRAWING', 'ILLUSTRATIVE CONCEPT', 'PROPOSED PROCESS'):
            if label not in text:
                raise ValueError('Missing visual-status label')
        css = (root / 'visual-disclosure.css').read_text(encoding='utf-8')
        if '.capital-disclosure' not in css or '@media print' not in css:
            raise ValueError('Missing opt-in or print treatment')
        for file in root.iterdir():
            if file.suffix not in ('.md', '.css', '.svg'):
                continue
            content = file.read_text(encoding='utf-8').lower()
            if any(x in content for x in ('docs.google.com/', 'drive.google.com/', 'data:image/', 'private/capital/')):
                raise ValueError('Private locator or embedded source-image payload in public package')
        print('PASS: generic labels, SVG descriptions, opt-in print style and bounded locator check')
        return 0
    except (OSError, ET.ParseError, ValueError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
