"""Bounded canonical press-desk checks; not a full-site or deployment audit."""
import hashlib
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGES = {
    'es': ('es/medios-trazabilidad-relato-publico/index.html', 'da410d375b89dccf97b1c00a58135841a44900f7'),
    'en': ('en/media-public-narrative-traceability/index.html', '91bcb1f846ad12fe51c4eafa0c607078686f7956'),
}
BASE = 'https://sbu001monterecco.github.io/por-derecho/'
MARK = '<!-- PD-MEDIA-DESK-20260905-02:'
HEAD = '<!-- PD-MEDIA-DESK-HEAD:'


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def strip_additions(text):
    for marker in (MARK, HEAD):
        text, count = re.subn(re.escape(marker + 'START -->') + '.*?' +
                             re.escape(marker + 'END -->'), '', text, flags=re.S)
        if count != 1:
            raise ValueError('Expected one complete controlled block')
    return text


def section(text):
    return text.split(MARK + 'START -->', 1)[1].split(MARK + 'END -->', 1)[0]


class CanonicalMediaDeskTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {lang: (ROOT / path).read_text(encoding='utf-8')
                     for lang, (path, _) in PAGES.items()}

    def test_original_record_preserved_exactly(self):
        for lang, text in self.pages.items():
            raw = strip_additions(text).encode('utf-8')
            digest = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
            self.assertEqual(digest, PAGES[lang][1], lang)

    def test_h1_precedes_new_h2(self):
        for text in self.pages.values():
            self.assertEqual(text.count('<h1>'), 1)
            self.assertLess(text.index('<h1>'), text.index(MARK))

    def test_unique_ids(self):
        for text in self.pages.values():
            ids = [a['id'] for _, a in Tags(text).tags if 'id' in a]
            self.assertEqual(len(ids), len(set(ids)))

    def test_six_source_cards_in_both_languages(self):
        for text in self.pages.values():
            self.assertEqual(section(text).count('class="media-desk-card"'), 6)

    def test_canonical_routes_not_new_media_aliases(self):
        for lang, text in self.pages.items():
            canonical = [a['href'] for t, a in Tags(text).tags if t == 'link' and a.get('rel') == 'canonical']
            self.assertEqual(canonical, [BASE + PAGES[lang][0][:-10]])
            self.assertNotIn(BASE + 'es/medios/', text)
            self.assertNotIn(BASE + 'en/media/', text)

    def test_language_switch_targets_existing_pair(self):
        for lang, text in self.pages.items():
            other = 'en' if lang == 'es' else 'es'
            links = [a for t, a in Tags(text).tags if t == 'link' and a.get('hreflang') == other]
            self.assertEqual(len(links), 1)
            self.assertEqual(links[0]['href'], BASE + PAGES[other][0][:-10])

    def test_no_new_actions_or_scripts(self):
        forbidden = {'form', 'input', 'textarea', 'button', 'script', 'iframe', 'object', 'embed'}
        for text in self.pages.values():
            for tag, attrs in Tags(section(text)).tags:
                self.assertNotIn(tag, forbidden)
                self.assertFalse(any(k.lower().startswith('on') for k in attrs))
                self.assertFalse(any(str(v).lower().startswith(('javascript:', 'mailto:', 'data:')) for v in attrs.values()))

    def test_no_private_source_locators(self):
        for text in self.pages.values():
            added = section(text)
            for token in ('mail.google.com', '1drv.ms', 'drive.google.com', 'dropbox.com', 'gmail_id', 'thread_id', '/private/'):
                self.assertNotIn(token, added)
            self.assertIsNone(re.search(r'[\w.+-]+@[\w.-]+\.[a-z]{2,}', added, re.I))

    def test_required_documentary_routes(self):
        for text in self.pages.values():
            for route in ('ric-private-equity-sun-park/', 'reconstruccion-unitaria-autoridades-publicas/', 'registros-institucionales/'):
                self.assertIn(route, section(text))

    def test_webinar_literal_preserved_not_invented(self):
        for text in self.pages.values():
            self.assertIn('https://www.youtube.com/watch?v=mHn9IJU0qI4&amp;t=488s', section(text))

    def test_english_labels_spanish_sources(self):
        added = section(self.pages['en'])
        self.assertIn('thematic dossier · Spanish', added)
        self.assertIn('institutional reconstruction · Spanish', added)
        self.assertIn('institutional register · Spanish', added)
        self.assertIn('audiovisual source · Spanish', added)

    def test_scoped_styles_no_external_resources(self):
        css = (ROOT / 'assets/media-desk.css').read_text(encoding='utf-8')
        self.assertNotIn('url(', css.lower())
        self.assertNotIn('@import', css.lower())
        self.assertIn('.media-desk', css)
        self.assertIn('@media', css)
        self.assertIn(':focus-visible', css)

    def test_limits_preserved_in_both_languages(self):
        for text in self.pages.values():
            added = section(text)
            for name in ('LPB', 'CEXP', 'Matkator', 'Orion'):
                self.assertIn(name, added)
        self.assertIn('satire is not evidence', section(self.pages['en']))
        self.assertIn('la sátira no es prueba', section(self.pages['es']))


if __name__ == '__main__':
    unittest.main()
