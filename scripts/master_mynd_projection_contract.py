"""Separate two exact approved discovery projections from earlier owned content.

Only the byte-fingerprinted, standalone bilingual MASTER MYND backlink can be
removed from a legacy generator's comparison view. The public source is never
modified. All other content remains subject to the generator's exact comparison.
The new reader's independent source/identity/link/browser acceptance remains required.
"""
import hashlib
import re

MARKER = 'id="sun-park-canonical-site"'
PREFIX = '<section class="section master-supplement" '+MARKER+'>'
DIGESTS = {'en':'3fa952a13ea8ad3c429a999e90b089080896635cae904028ea4af19ae2d97ecf', 'es':'7116005bf858b822d9e37b7112a79be338c56536f7be49142dde6e2cb4340b20'}
# Only paths actually shared with the CNMV and Orion historical generators.
ALLOWED = {'en/authorities-duties-asset-recovery/index.html','es/autoridades-deberes-recuperacion-activos/index.html','en/acosta-matos-perimeter/index.html','es/acosta-matos-perimetro/index.html','en/ric-private-equity-sun-park/index.html','es/ric-private-equity-sun-park/index.html','en/lava-verde-club-sei-meeting-point/index.html','es/lava-verde-club-sei-meeting-point/index.html'}

def without_master_mynd_discovery(text: str, path: str) -> str:
    if MARKER not in text:
        return text
    if path not in ALLOWED:
        raise AssertionError('Unregistered discovery projection in legacy comparison: '+path)
    if text.count(MARKER)!=1:
        raise AssertionError('Duplicated discovery projection: '+path)
    matches=list(re.finditer(re.escape(PREFIX)+r'.*?</section>\n',text,re.S))
    if len(matches)!=1:
        raise AssertionError('Malformed discovery projection: '+path)
    match=matches[0]
    if hashlib.sha256(match[0].encode()).hexdigest()!=DIGESTS[path.split('/')[0]]:
        raise AssertionError('Discovery projection differs from approved source: '+path)
    if not text[match.end():].startswith('</main>'):
        raise AssertionError('Discovery projection is not the isolated final main section: '+path)
    return text[:match.start()]+text[match.end():]
