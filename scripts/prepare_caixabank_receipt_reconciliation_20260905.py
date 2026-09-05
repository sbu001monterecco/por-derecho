#!/usr/bin/env python3
"""Worker-only preparation from the independently read native receipt. No raw intake."""
import json
import os
from pathlib import Path

ROOT = Path.cwd()
if os.getenv('GITHUB_REF') != 'refs/heads/worker/caixabank-360-audit-20260905':
    raise SystemExit('Restricted to the named preparation worker')

components = [
 ('principal','Demanda_00 - Aweswell.pdf','d41a44712020991475a5f3e9df5a524d262d08d5e72e680a3b2e941b29a9d91d'),
 ('annex-0','Poder pleitos','25f40cb5da75fdb2f0a0642804f2a8f3ca0311f41ad96bc87f6db8f82e4a04df'),
 ('annex-1','Auto aprobacion','42111bd5e8a000bbe21e26121e1bb7b96a01f54cf028c422fd948849b1f57b93'),
 ('annex-2','Autorizacion','b7f1ea811dcc70b2fa303927b3af3faa499049ff93bfad654d7422158313a355'),
 ('annex-3','Escritura primer prestamo','edfe20ac61ac14e90cdaca6c02b1bb54abf84d3a3da1a31786d86c6b89e4e441'),
 ('annex-4','Contrato gestion riesgos financieros','45ec32cfee70cb6e372ad1ecbb7040d4034a7759d2ebb3ae70adb3e96d9154b6'),
 ('annex-5','Modificacion primer prestamo','06ee04b65175f0aadff5c01309bccdce2fbce3b8bff2acc4f1bbed32af9166fa'),
 ('annex-6','Escritura segundo prestamo','486ed98dd4c688a1c1ee749fd0f0d3db464208ebe9b2580f8a02c0d78d369d02'),
 ('annex-7','Poliza pignoracion','c76dfda1ed51d71d2a77bf37fb5c1f3a7b530aff87b709ac7467ddbd6ed4b58a'),
 ('annex-8','Contrato servicios inversion','468a715b698daad2e9fe39468c1622d139384c56a82d8592ef0ba8453a5710f1'),
 ('annex-9','Cuadros economicos','5bb3d326d94ae3a3b2cbdfec196f65f06b8fa50e1fe7c5b39cb57dba5602e017'),
 ('annex-10','Movimiento cuentas','825085411eac4047fbffc11b8b22b41e908b8f02070f35a43f4c4fc428825019'),
 ('annex-11','Comunicaciones','f7e0e33f8b5951188f5755ac2ab4dff412053ab18b84e19dad9584f3604ae414')
]
assert len(components)==13 and len({r[0] for r in components})==13
assert all(len(fp)==64 and all(c in '0123456789abcdef' for c in fp) for _,_,fp in components)
manifest_path=ROOT/'data/audits/caixabank-public-derivatives-20260905.json'
m=json.loads(manifest_path.read_text())
m['claim_filing_reconciliation']={
 'status':'RECEIPT_RECOVERED_EXACT_FILE_RECONCILIATION_OPEN',
 'receipt':{'sha256':'a522daa528c345f4ef31963e3ded6a674a5376b56bead7495cc837fb013e2312','pages':4,'bytes':194989,'native_publication':'WITHHELD_PRIVATE','dispatch_local':'2023-10-11T19:39:57','timezone':'NOT_STATED_IN_RECEIPT','generation_local':'2023-10-11T19:45','generation_precision':'minute'},
 'denominator':{'principal_pdf':1,'accompanying_pdfs':12,'total':13,'annex_labels':'0 through 11'},
 'components':[{'component':i,'receipt_label':label,'receipt_declared_fingerprint':fp,'fingerprint_algorithm':'NOT_EXPRESSLY_STATED_IN_REVIEWED_RECEIPT','exact_native_match':'OPEN'} for i,label,fp in components],
 'recovered_claim_sha256':'f44121b7ac9026d2478d82974641c9da11fe497aacd999188ada3d495fe34a77',
 'public_claim_status':'COUNSEL_SOURCE_DERIVED_REDACTED_READING_COPY_NOT_CERTIFIED_BYTE_IDENTICAL_TO_FILED_PRINCIPAL',
 'interpretation':'The receipt establishes dispatch and the thirteen-component inventory. Its principal fingerprint has not been reconciled with the recovered claim PDF. Different fingerprints alone do not prove substantive alteration or wrongdoing. The receipt labels annex9 as economic tables, not the Administrator filing. No exact annex attribution is invented from a filename.',
 'date_boundary':'Legacy 13-Oct references, 11-Oct dispatch, receipt generation and any later court registration are separate events.',
 'custodian':'Filing procurador, counsel and complete court file',
 'closure_test':'Recover all receipt-listed files; establish fingerprint algorithm and signing/conversion history; compare bytes and content; reconcile later court registration separately; review each annex for privacy, privilege and licensed material.',
 'no_claims':['All annexes publicly available','Every native annex fully reviewed','Exact filed-version identity proved','Court admission proved by dispatch alone','Fingerprint mismatch proves misconduct'],
 'preparation_correction':'An earlier unexecuted preparation draft contained incorrect receipt metadata and annex labels. It was replaced after independent extraction and hashing of the mounted source, before generation, merge or site deployment.'
}
manifest_path.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
notes={
'es/reclamacion-caixabank-valencia/documentos/index.html':'''<aside class="note" id="control-presentacion-11oct2023"><h3>Presentación y versión exacta: controles distintos</h3><p>El justificante LexNET recuperado registra el envío el <strong>11 de octubre de 2023 a las 19:39:57</strong> (zona horaria no indicada) y enumera <strong>un PDF principal y doce anexos, numerados 0–11</strong>. Esto documenta el envío, no por sí solo admisión, reparto ni identidad íntegra de cada archivo.</p><p>La demanda remitida por los profesionales se ofrece como <strong>copia de lectura disociada</strong>. Su archivo fuente recuperado no está reconciliado con la huella declarada para el principal en el justificante. No se certifica identidad byte a byte con ese adjunto presentado. Una diferencia de huella no demuestra alteración sustantiva ni irregularidad. La referencia histórica al 13-Oct debe mantenerse separada del envío del 11-Oct y de cualquier registro posterior.</p><p><a href="/por-derecho/data/audits/caixabank-public-derivatives-20260905.json">Ver inventario de trece componentes, procedencia y prueba pendiente</a>. El justificante nativo queda en custodia privada; los anexos aún no cotejados no se presentan como íntegramente publicados.</p></aside>''',
'en/caixabank-valencia-claim/documents/index.html':'''<aside class="note" id="control-presentacion-11oct2023"><h3>Submission and exact-file identity are separate controls</h3><p>The recovered LexNET receipt records dispatch on <strong>11 October 2023 at 19:39:57</strong> (timezone not stated) and lists <strong>one principal PDF and twelve annexes, labelled 0–11</strong>. It documents dispatch, not by itself court admission, allocation or the exact identity of each attachment.</p><p>The claim supplied by the legal professionals is provided as a <strong>public-redacted reading copy</strong>. Its recovered source file has not been reconciled with the receipt-declared fingerprint for the principal. Byte-for-byte identity with that submitted attachment is not certified. Different fingerprints alone do not prove substantive alteration or wrongdoing. The legacy 13-Oct reference remains separate from the observed 11-Oct dispatch and any later registration.</p><p><a href="/por-derecho/data/audits/caixabank-public-derivatives-20260905.json">See the thirteen-component inventory, provenance and open proof test</a>. The native receipt remains private; unreconciled annexes are not described as fully published.</p></aside>'''
}
changed=[str(manifest_path.relative_to(ROOT))]
for rel,note in notes.items():
 p=ROOT/rel;s=p.read_text()
 if 'id="control-presentacion-11oct2023"' not in s:
  anchor='<section class="section" id="copias-publicas-verificadas"><div class="shell record">'
  assert s.count(anchor)==1,rel
  p.write_text(s.replace(anchor,anchor+note,1))
 changed.append(rel)
control=ROOT/'CAIXABANK_360_READER_REPAIR_CONTROL_05SEP2026.md'
s=control.read_text();heading='## Recovered 11 October 2023 receipt: exact-file identity still open'
if heading not in s:
 s+='\n\n'+heading+'\n\nIndependently read four-page receipt: dispatch11-Oct-2023 at19:39:57; generation19:45, timezone unstated; principal plus twelve annexes0–11. Source SHA-256 a522daa528c345f4ef31963e3ded6a674a5376b56bead7495cc837fb013e2312. The receipt-declared principal fingerprint is not reconciled with the recovered counsel PDF. Annex9 is economic tables; no AC attachment attribution is inferred. Source readers and the existing derivative manifest preserve the limitation; the native receipt and private verification data remain private. An incorrect unexecuted preparation draft was corrected against actual bytes before generation.\n\nThe first final-reader regression incorrectly expected one total homepage component, although the source deliberately creates one navigation rail and one case-map section. The corrected test checks one of each on homepages and none on either CaixaBank landing page, retaining contrast/tap-size checks and failure artifacts. The worker was also fast-forwarded through GitHub’s conflict-free merge tree a50462a54fb3cdbaff542d41d1a48df1a94aa85a, whose parents preserve ADC8 current main and the complete worker. Main was not merged or rewritten.\n'
 control.write_text(s)
changed.append(str(control.relative_to(ROOT)))
Path('/tmp/caixabank-receipt-prepared-paths.json').write_text(json.dumps(changed))
print('RECEIPT_STATUS_PREPARED',len(changed),'native receipt not published')
