#!/usr/bin/env python3
"""Offline synthetic MIME regression tests. No accounts, network or mail transport.
Run: python3 -m unittest discover -s scripts -p 'test_media_link_core.py' -v
A successful run is not authorization, source verification or Gmail enforcement.
"""
from email.message import EmailMessage
import hashlib
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_media_link_core import BASE, PNG_NAMES, WEBINAR, inspect_eml

HUB = BASE + 'es/'
LANDING = HUB + 'ric-private-equity-sun-park/'
AUTHORITY = HUB + 'reconstruccion-unitaria-autoridades-publicas/'
RECORDS = HUB + 'registros-institucionales/'
URLS = (HUB, LANDING, AUTHORITY, RECORDS, WEBINAR)
# Signature fixture exercises only the documented signature gate, not image decoding.
PNG = b'\x89PNG\r\n\x1a\nsynthetic-offline-signature-fixture'
PDF = b'%PDF-1.4\nsynthetic-offline-hash-fixture\n%%EOF'
PAYLOADS = dict.fromkeys(PNG_NAMES['es'], PNG)
PAYLOADS['source-fixture.pdf'] = PDF
HASHES = {name: hashlib.sha256(data).hexdigest() for name, data in PAYLOADS.items()}
TEXT = 'Synthetic current body. No transmission.\n' + '\n'.join(URLS)
HTML = '<html><body><p>Current body.</p>' + ''.join(
    f'<p><a href="{u.replace("&", "&amp;")}">Source {i}</a></p>'
    for i, u in enumerate(URLS)) + '</body></html>'


def message(text=TEXT, html=None, payloads=None):
    msg = EmailMessage()
    msg['Subject'] = 'Offline structural fixture'
    msg.set_content(text)
    if html is not None:
        msg.add_alternative(html, subtype='html')
    for name, data in (PAYLOADS if payloads is None else payloads).items():
        kind, subtype = ('image', 'png') if name.endswith('.png') else ('application', 'pdf')
        msg.add_attachment(data, maintype=kind, subtype=subtype, filename=name)
    return msg


def check(msg, **kwargs):
    options = dict(language='es', landing_url=LANDING, institutional=True, expected=HASHES)
    options.update(kwargs)
    return inspect_eml(msg.as_bytes(), **options)


class MediaCoreTests(unittest.TestCase):
    def test_complete_plain_package(self):
        self.assertEqual(check(message())['status'], 'CONTENT_GATE_PASS_ONLY')

    def test_complete_both_body_formats(self):
        self.assertFalse(check(message(html=HTML))['errors'])

    def test_each_missing_required_link(self):
        for url in URLS:
            with self.subTest(url=url):
                self.assertTrue(check(message(text=TEXT.replace(url + '\n', '', 1)
                                              if url + '\n' in TEXT else TEXT.replace(url, '')))['errors'])

    def test_each_missing_map(self):
        for name in PNG_NAMES['es']:
            with self.subTest(name=name):
                self.assertTrue(check(message(payloads={k: v for k, v in PAYLOADS.items()
                                                       if k != name}))['errors'])

    def test_filenames_in_body_not_attachments(self):
        self.assertTrue(check(message(text=TEXT + '\n' + '\n'.join(PAYLOADS), payloads={}))['errors'])

    def test_wrong_png_type_or_signature(self):
        msg = message()
        next(msg.iter_attachments()).replace_header('Content-Type', 'application/octet-stream')
        self.assertTrue(check(msg)['errors'])
        changed = dict(PAYLOADS)
        changed[PNG_NAMES['es'][0]] = b'not a PNG'
        self.assertTrue(check(message(payloads=changed))['errors'])

    def test_changed_pdf_hash(self):
        changed = dict(PAYLOADS)
        changed['source-fixture.pdf'] += b'changed'
        self.assertTrue(any('HASH_MISMATCH' in e for e in check(message(payloads=changed))['errors']))

    def test_unexpected_attachment(self):
        changed = dict(PAYLOADS, **{'unapproved.pdf': PDF})
        self.assertIn('UNEXPECTED_ATTACHMENT:unapproved.pdf', check(message(payloads=changed))['errors'])

    def test_duplicate_attachment(self):
        msg = message()
        msg.add_attachment(PDF, maintype='application', subtype='pdf', filename='source-fixture.pdf')
        self.assertIn('DUPLICATE_ATTACHMENT:source-fixture.pdf', check(msg)['errors'])

    def test_plain_html_mismatch(self):
        self.assertTrue(check(message(html='<p>Missing sources</p>'))['errors'])
        self.assertTrue(check(message(text='Missing sources', html=HTML))['errors'])

    def test_quoted_plain_links_do_not_count(self):
        self.assertTrue(check(message(text='New body.\n' + '\n'.join('> ' + u for u in URLS)))['errors'])

    def test_history_delimiters_do_not_count(self):
        for delimiter in ('On a previous date Writer wrote:', 'El lunes alguien escribió:',
                          '---------- Forwarded message ---------'):
            with self.subTest(delimiter=delimiter):
                self.assertTrue(check(message(text='New body.\n' + delimiter + '\n' + TEXT))['errors'])

    def test_quoted_html_links_do_not_count(self):
        for wrapper in ('<blockquote>{}</blockquote>', '<div class="gmail_quote">{}</div>'):
            with self.subTest(wrapper=wrapper):
                self.assertTrue(check(message(html='<p>New body</p>' + wrapper.format(HTML)))['errors'])

    def test_hidden_or_empty_anchor_does_not_count(self):
        for wrapper in ('<div hidden>{}</div>', '<div style="display: none">{}</div>',
                        '<div aria-hidden="true">{}</div>', '<script>{}</script>'):
            with self.subTest(wrapper=wrapper):
                self.assertTrue(check(message(html=wrapper.format(HTML)))['errors'])
        empty = ''.join(f'<a href="{u}"></a>' for u in URLS)
        self.assertTrue(check(message(html=empty))['errors'])

    def test_links_only_in_pdf_or_forward_do_not_count(self):
        payloads = dict(PAYLOADS)
        payloads['source-fixture.pdf'] = TEXT.encode()
        self.assertTrue(check(message(text='No current links', payloads=payloads))['errors'])
        msg = message(text='No current links')
        forwarded = EmailMessage()
        forwarded.set_content(TEXT)
        msg.add_attachment(forwarded)
        self.assertTrue(check(msg)['errors'])

    def test_home_fragment_and_wrong_host_not_topic(self):
        for landing in (HUB, HUB + '#topic', BASE + 'assets/file.pdf',
                        'https://example.invalid/por-derecho/es/topic/'):
            with self.subTest(landing=landing):
                self.assertIn('INVALID_OR_NON_SPECIFIC_LANDING_URL',
                              check(message(text=TEXT + '\n' + landing), landing_url=landing)['errors'])

    def test_nonspanish_institutional_slugs_not_invented(self):
        result = check(message(), language='en', landing_url=BASE + 'en/topic/')
        self.assertIn('MISSING_EXPLICIT_INSTITUTIONAL_ROUTES', result['errors'])

    def test_official_links_only_regression(self):
        msg = message(text='https://www.boe.es/\nhttps://www.boe.es/borme/',
                      payloads={'source-fixture.pdf': PDF})
        result = check(msg)
        self.assertEqual(result['status'], 'CONTENT_GATE_BLOCKED')
        self.assertGreaterEqual(len(result['errors']), 7)

    def test_pass_never_certifies_other_gates(self):
        result = check(message())
        for name in ('live_links_verified', 'history_gate_verified', 'authorization_verified',
                     'sent_verified', 'rendered_visibility_verified', 'source_accuracy_verified'):
            self.assertIs(result[name], False)


if __name__ == '__main__':
    unittest.main()
