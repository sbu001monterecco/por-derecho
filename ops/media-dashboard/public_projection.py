#!/usr/bin/env python3
"""Build a source-directory projection, never a mailbox or contact export.

Only a finite list of reviewed resource IDs is accepted. This helper does not
read Gmail, perform live checks, prove approval, send mail or deploy anything.
Keep actual correspondence and operational datasets outside the public repo.
"""
from __future__ import annotations
import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

BASE = 'https://sbu001monterecco.github.io/por-derecho/'
RESOURCES = {
    'website_es': {'url': BASE + 'es/', 'source_language': 'es'},
    'website_en': {'url': BASE + 'en/', 'source_language': 'en'},
    'sunpark_ricpe': {'url': BASE + 'es/ric-private-equity-sun-park/', 'source_language': 'es'},
    'court_authority_context': {'url': BASE + 'es/reconstruccion-unitaria-autoridades-publicas/', 'source_language': 'es'},
    'institutional_records': {'url': BASE + 'es/registros-institucionales/', 'source_language': 'es'},
    'webinar': {'url': 'https://www.youtube.com/watch?v=mHn9IJU0qI4&t=488s', 'source_language': 'es'},
}
FIELDS = {'language', 'as_of', 'resource_ids', 'release_approved', 'approval_record'}


def build_projection(config: dict[str, Any], *, preview: bool = False) -> dict[str, Any]:
    """Fail closed on unknown input; approval fields are operator assertions."""
    if not isinstance(config, dict) or set(config) != FIELDS:
        raise ValueError('Expected only the five controlled configuration fields')
    if config['language'] not in ('es', 'en'):
        raise ValueError('Unsupported language')
    try:
        as_of = date.fromisoformat(config['as_of']).isoformat()
    except (ValueError, TypeError):
        raise ValueError('as_of must be an ISO calendar date') from None
    if not isinstance(config['release_approved'], bool):
        raise ValueError('release_approved must be Boolean')
    if not isinstance(config['approval_record'], str):
        raise ValueError('approval_record must be a string')
    ids = config['resource_ids']
    if not isinstance(ids, list) or not ids or any(not isinstance(i, str) or i not in RESOURCES for i in ids):
        raise ValueError('Unknown or missing reviewed source ID')
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate source ID')
    required = {'website_' + config['language'], 'sunpark_ricpe', 'court_authority_context', 'institutional_records'}
    if not required.issubset(ids):
        raise ValueError('Missing website, topic or court/institutional entry')
    if not preview and (not config['release_approved'] or not config['approval_record'].strip()):
        raise ValueError('Release is blocked without a separate recorded approval')
    return {
        'schema_version': 'PD-MEDIA-DASHBOARD-20260905-01',
        'mode': 'preview_not_deployed' if preview else 'approved_projection_not_deployment_proof',
        'as_of': as_of,
        'language': config['language'],
        'source_check_required_before_release': True,
        'resources': [{'id': i, **RESOURCES[i]} for i in ids],
        'has_correspondence_data': False,
        'has_forms': False,
        'can_send_email': False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--preview', action='store_true')
    args = parser.parse_args()
    try:
        out = build_projection(json.loads(args.config.read_text(encoding='utf-8')), preview=args.preview)
        if args.output.resolve() == args.config.resolve():
            raise ValueError('Output must not overwrite configuration')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return 0
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, f'BLOCKED: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
