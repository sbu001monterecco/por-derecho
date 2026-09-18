"""Finite additive-preservation and late-scroll delegation regression contracts."""
import json, os, re, subprocess, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
BASE = os.environ.get('GITHUB_BASE_SHA', '65d56cec10e11f5a5c0861bb087ee87e64f5effa')
MARK = 'PD-MEDIA-DASHBOARD-20260905-01'
GUARD = "    // The media desk owns this new fragment and cancels restoration on reader input.\n    if (target.id === 'media-desk' && document.body.classList.contains('media-desk-page')) return;\n"

def prior(path):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT, text=True)

def strip(text):
    text = re.sub(r'<!-- ' + MARK + r':(?:head|desk|nav):START -->.*?<!-- ' + MARK + r':(?:head|desk|nav):END -->\n?', '', text, flags=re.S)
    return text.replace('class="dossier-page media-desk-page"', 'class="dossier-page"')

class Preservation(unittest.TestCase):
    def test_html_inherited_content_exact(self):
        for route in ('es/medios-trazabilidad-relato-publico/', 'en/media-public-narrative-traceability/'):
            p = route + 'index.html'
            self.assertEqual(strip(prior(p)), strip((ROOT / p).read_text()), p)
    def test_shared_script_only_delegates_new_fragment(self):
        p = 'assets/optimum-reader-journey-finish-20260818.js'
        text = (ROOT / p).read_text(); self.assertEqual(text.count(GUARD), 1)
        self.assertEqual(prior(p).replace(GUARD, ''), text.replace(GUARD, ''))
    def test_search_rows_preserved(self):
        p = 'assets/data/unitary-route-registry-sync-20260819.json'
        old = json.loads(prior(p)); new = json.loads((ROOT / p).read_text())
        self.assertEqual(new[:len(old)], old)
    def test_sitemap_original_bytes_preserved(self):
        p = 'sitemap-discovery-navigation.xml'
        def strip_entries(text):
            return re.sub(r'<url><loc>https://sbu001monterecco.github.io/por-derecho/(?:es/medios-trazabilidad-relato-publico|en/media-public-narrative-traceability)/</loc>.*?</url>\n?', '', text)
        self.assertEqual(strip_entries(prior(p)), strip_entries((ROOT / p).read_text()))
    def test_cached_legacy_script_cannot_duplicate(self):
        for lang in ('es', 'en'):
            p = ROOT / 'ops/media-dashboard/build_release.py'
            self.assertIn('data-optimum-reader-journey-finish="20260905media"', p.read_text())
        js = (ROOT / 'assets/media-desk.js').read_text()
        for event in ('wheel', 'touchstart', 'pointerdown', 'keydown', 'hashchange'):
            self.assertIn(event, js)
    def test_new_section_not_legacy_insertion_target(self):
        for lang in ('es', 'en'):
            s = (ROOT / f'ops/media-dashboard/section-{lang}.html').read_text()
            self.assertIn('class="media-desk-section"', s)
            self.assertNotIn('class="section', s)
if __name__ == '__main__': unittest.main()
