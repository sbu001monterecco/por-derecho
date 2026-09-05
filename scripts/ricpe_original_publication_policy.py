"""Exactly one explicitly authorised original; never a general privacy bypass."""
import hashlib
import json
from pathlib import Path

PATH = 'evidence/ricpe-cnmv/2026-08-27/original-authorised-20260905/RICPE_Canal_Etico_Certificado_Resolucion_27AGO2026.pdf'
HASH = 'db9979715cac4aeb8ded81a998227cfd894144dcd0a50fe81d4b1369904c9bb4'
AUTH = 'operations/preservation-authorizations/RICPE_ORIGINAL_EXACT_PUBLICATION_05SEP2026.json'

def authorised_original(root: Path, relative: str, data: bytes) -> bool:
    if relative != PATH or len(data) != 444759 or hashlib.sha256(data).hexdigest() != HASH:
        return False
    try:
        record = json.loads((root / AUTH).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return False
    return all((record.get('authorization_id') == 'PD-RICPE-ORIGINAL-20260905', record.get('date') == '2026-09-05', record.get('path') == PATH, record.get('sha256') == HASH, record.get('bytes') == 444759, record.get('pages') == 6, record.get('unaltered_original') is True, record.get('no_outbound_action') is True))
