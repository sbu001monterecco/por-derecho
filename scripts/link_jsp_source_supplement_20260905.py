#!/usr/bin/env python3
"""Add source-supplement crosslinks without reallocating canonical identities."""
from pathlib import Path
import json
from prepare_jsp_perimeter_worker_20260905 import append_section, PAGES, PROMPT, DELTA

root = Path(__file__).resolve().parents[1]
supplement = 'archive/JSP_SOURCE_SUPPLEMENT_05SEP2026.md'
assert (root/supplement).is_file()
changed = []
content = {
 'es': ('Ampliación documental: Celgán, juez y cuentas consolidadas', 'El asiento oficial 445948 de BORME-A-2021-194-38 identifica conjuntamente a JSP y Celgán en 440/2021 y da el nombre completo Guillermo Fernández García. Se localizan además depósitos de cuentas consolidadas JSP de 2008 y 2010 y una reelección de auditor de 2020. El suplemento distingue estas fuentes de los nombres de representantes y LAJ tomados de una reproducción de edicto todavía pendiente de cotejo original. No se acredita por ello consolidación de masas, mayoría Montelanza ni un cargo actual.'),
 'en': ('Source update: Celgán, judicial identity and consolidated accounts', 'Official BORME-A-2021-194-38 entry 445948 identifies JSP and Celgán together in 440/2021 and supplies the full judicial name Guillermo Fernández García. Further targets are JSP consolidated-account deposits for 2008 and 2010 and a 2020 auditor reappointment. The supplement distinguishes these sources from representative and LAJ names transcribed from an edict reproduction still requiring original verification. This does not establish pooled estates, Montelanza majority ownership or a current appointment.'),
}
for lang, relative in PAGES.items():
    title, body = content[lang]
    block = '<section id="jsp-source-supplement"><h2>'+title+'</h2><p>'+body+'</p><p><a href="../../'+supplement+'">S08–S11 / R05 · source supplement</a></p></section>'
    append_section(root/relative, 'jsp-source-supplement', block, changed, root)
p = root/PROMPT
text = p.read_text(encoding='utf-8')
if 'JSP_SOURCE_SUPPLEMENT_05SEP2026.md' not in text:
    text += '\n\n## Mandatory source update before execution\n\nRead [JSP_SOURCE_SUPPLEMENT_05SEP2026.md](JSP_SOURCE_SUPPLEMENT_05SEP2026.md). Official entry445948 now confirms Celgán in440/2021 and supplies the full judge name Guillermo Fernández García. Recover the exact2008 and2010 consolidated-account deposits and2020 auditor appointment identified there. Treat Rafael Franco Miranda, Fidel Blasco Miota, Román García-Varela Iglesias and the procurador/NIG details in the reproduced edict as original-document verification targets, not current certified roles. Reconcile this supplement with the earlier candidate-only passages and identity delta; no estate pooling, ownership majority or criminal participation follows automatically.\n'
    p.write_text(text,encoding='utf-8')
    changed.append(PROMPT)
p = root/DELTA
d = json.loads(p.read_text(encoding='utf-8'))
d['source_supplement'] = {
 'path':supplement,
 'source_keys':['S08','S09','S10','S11','R05'],
 'coverage':'Explicit expansion beyond the 11-source, 21-disposition-group, 17-event base intake; not a canonical-ID allocation.',
 'primary_updates':['Celgán co-debtor and full judge name','2008 and 2010 consolidated-account deposit targets','2020 KPMG appointment'],
 'reproduction_only_name_leads':['Rafael Franco Miranda','Fidel Blasco Miota','Román García-Varela Iglesias','Francisco Javier Pérez Almeida'],
 'current_roles_verified':False,
 'canonical_reconciliation_pending':True
}
for item in d['identity_dispositions']:
    if item['name'] == 'Guillermo Fernández García':
        item['state'] = 'FULL_NAME_NOW_SUPPLIED_BY_PRIMARY_S08_REUSE_EXISTING_ID_CURRENT_ROLE_NOT_VERIFIED'
    if item['name'].startswith('Celgán, Asemar,'):
        item['state'] = 'CELGAN_CO_DEBTOR_NOW_PRIMARY_S08_OTHER_MANDATES_REMAIN_PENDING_SEE_SUPPLEMENT'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'supplement_linked':True,'changed_paths':changed,'canonical_registration_complete':False},indent=2))
