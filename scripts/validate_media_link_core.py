#!/usr/bin/env python3
"""Offline check of an actual .eml, NOT a send/authorization/live-link verifier.

Never store private .eml or reports in the public repository.  Usage:
  python validate_media_link_core.py message.eml --language es \
    --landing-url https://sbu001monterecco.github.io/por-derecho/es/ric-private-equity-sun-park/ \
    --institutional
A pass is only a mechanical content pass. History, privacy, truth, rendered
layout, fresh public access and exact user authorization remain separate gates.
"""
from __future__ import annotations
import argparse
from email import policy
from email.parser import BytesParser
import hashlib
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

BASE = 'https://sbu001monterecco.github.io/por-derecho/'
WEBINAR = 'https://www.youtube.com/watch?v=mHn9IJU0qI4&t=488s'
PNG_NAMES = {
    'es': ('pwc-five-actors-plus-ac-2016-knowledge-checkpoint-ES.png',
           'san-telmo-ricpe-sun-park-stamp-v1-ES.png'),
    'en': ('pwc-five-actors-plus-ac-2016-knowledge-checkpoint-EN.png',
           'san-telmo-ricpe-sun-park-stamp-v1.png'),
    'de': ('Anlage-2A-PwC-Kenntnispunkt-2016-DE.png',
           'Anlage-1A-RICPE-Sun-Park-Rollen-DE.png'),
}

class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(); self.links: set[str] = set(); self.text: list[str] = []; self.ignored = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.ignored += 1
        if tag == 'a' and not self.ignored:
            self.links.update(unescape(v) for k, v in attrs if k == 'href' and v)
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.ignored = max(0, self.ignored - 1)
    def handle_data(self, data):
        if not self.ignored: self.text.append(data)

def project_route(value: str) -> bool:
    p = urlsplit(value)
    return (p.scheme == 'https' and p.netloc == 'sbu001monterecco.github.io'
            and p.path.startswith('/por-derecho/') and not p.query)

def extract_links(text: str, kind: str) -> set[str]:
    if kind == 'text/html':
        parser = LinkParser(); parser.feed(text)
        return parser.links | set(re.findall(r'https://[^\s<>"\)]+', ''.join(parser.text)))
    return {u.rstrip('.,;') for u in re.findall(r'https://[^\s<>"\)]+', text)}

def inspect_eml(raw: bytes, language: str, landing_url: str,
                institutional: bool = False, expected: dict[str, str] | None = None) -> dict:
    """Check decoded MIME bodies/attachments; do not accept filenames in body as attachments."""
    errors: list[str] = []
    msg = BytesParser(policy=policy.default).parsebytes(raw)
    body_parts: list[tuple[str, set[str]]] = []
    attachments: dict[str, list[dict]] = {}
    def visit(part, inside_attachment=False):
        attached = inside_attachment or part.get_content_disposition() == 'attachment' or part.get_filename() is not None
        if attached:
            if not inside_attachment and part.get_filename():
                payload = part.get_payload(decode=True) or b''
                record = {'mime_type': part.get_content_type(), 'size_bytes': len(payload),
                          'sha256': hashlib.sha256(payload).hexdigest(),
                          'png_signature': payload.startswith(b'\x89PNG\r\n\x1a\n')}
                attachments.setdefault(part.get_filename(), []).append(record)
            return  # No links from forwarded .eml, PDF, attachment metadata, etc.
        if part.is_multipart():
            for child in part.iter_parts(): visit(child)
        elif part.get_content_type() in ('text/plain', 'text/html'):
            body_parts.append((part.get_content_type(), extract_links(part.get_content(), part.get_content_type())))
    visit(msg)
    if not body_parts: errors.append('MISSING_EMAIL_BODY')
    # German has no assumed published hub; an explicit, verified ES/EN hub must be selected by the operator.
    hub_language = language if language in ('es', 'en') else 'es'
    hub = BASE + hub_language + '/'
    if not project_route(landing_url) or landing_url.rstrip('/') in (BASE.rstrip('/'), hub.rstrip('/')):
        errors.append('INVALID_OR_NON_SPECIFIC_LANDING_URL')
    required = {hub: 'WEBSITE_HUB', landing_url: 'SPECIFIC_LANDING', WEBINAR: 'WEBINAR'}
    if institutional:
        required[BASE + hub_language + '/reconstruccion-unitaria-autoridades-publicas/'] = 'COURT_AUTHORITY_CONTEXT'
        required[BASE + hub_language + '/registros-institucionales/'] = 'INSTITUTIONAL_RECORDS'
    for index, (kind, links) in enumerate(body_parts, 1):
        for url, label in required.items():
            if url not in links: errors.append(f'BODY_{index}_{kind}:MISSING_{label}')
    for filename in PNG_NAMES[language]:
        records = attachments.get(filename, [])
        if len(records) != 1: errors.append(f'REQUIRED_PNG_COUNT_{len(records)}:{filename}')
        elif records[0]['mime_type'] != 'image/png' or not records[0]['png_signature']:
            errors.append(f'INVALID_PNG_PAYLOAD:{filename}')
    for filename, digest in (expected or {}).items():
        records = attachments.get(filename, [])
        if len(records) != 1 or records[0]['sha256'] != digest:
            errors.append(f'ATTACHMENT_HASH_MISMATCH_OR_MISSING:{filename}')
    return {'status': 'CONTENT_GATE_BLOCKED' if errors else 'CONTENT_GATE_PASS_ONLY',
            'errors': errors, 'attachments': attachments,
            'live_links_verified': False, 'history_gate_verified': False,
            'authorization_verified': False, 'sent_verified': False,
            'note': 'Offline structural check only. Inspect visible rendering and source limits separately.'}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('eml', type=Path)
    parser.add_argument('--language', choices=tuple(PNG_NAMES), default='es')
    parser.add_argument('--landing-url', required=True)
    parser.add_argument('--institutional', action='store_true')
    parser.add_argument('--attachment-hashes', type=Path,
                        help='Private JSON object mapping every approved filename to SHA-256.')
    args = parser.parse_args()
    try:
        expected = json.loads(args.attachment_hashes.read_text()) if args.attachment_hashes else None
        if expected is not None and (not isinstance(expected, dict) or
                any(not isinstance(k, str) or not isinstance(v, str) or not re.fullmatch(r'[0-9a-f]{64}', v)
                    for k, v in expected.items())):
            raise ValueError('Invalid attachment hash manifest')
        result = inspect_eml(args.eml.read_bytes(), args.language, args.landing_url, args.institutional, expected)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result['errors'] else 0
    except (OSError, ValueError, TypeError, KeyError, UnicodeError) as exc:
        print(json.dumps({'status': 'CONTENT_GATE_BLOCKED', 'error': str(exc)})); return 2

if __name__ == '__main__':
    sys.exit(main())
