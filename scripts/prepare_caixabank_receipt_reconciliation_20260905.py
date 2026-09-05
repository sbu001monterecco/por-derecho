#!/usr/bin/env python3
"""Idempotent, worker-only source-status preparation. No native receipt or private data."""
import json
import os
from pathlib import Path

ROOT = Path.cwd()
if os.getenv('GITHUB_REF') != 'refs/heads/worker/caixabank-360-audit-20260905':
    raise SystemExit('Preparation is restricted to the named worker branch')

manifest_path = ROOT/'data/audits/caixabank-public-derivatives-20260905.json'
m = json.loads(manifest_path.read_text())
components = [
 ('principal','Claim','d41a44712020991475a5f3e9df5a3e524d262d08d5e72e680a3b2e941b29a9d91d'),
 ('annex-0','Documentary index','46b2becc7c0f4fbc372129c115bef801a329a961c785877bad49d1b66018b6adf'),
 ('annex-1','Liquidation-plan approval order','8d6b535e726e2233449862b78d7d0f3ffbe116bab4c4faf2a2e56d48506193f67'),
 ('annex-2','Inflation coverage contract','59d1968df8c43e2c8989405ec24cc897c8508a8f28d6e8e10729e46203626321'),
 ('annex-3','Options contract','9a8e3a2e3cd8f48cd30d6d9e1089fd5c05cfe1c5695cc7c249906772d7f013f2'),
 ('annex-4','Swaps','e91dfe0e6487dd3b354603e370e77226599a2f0ca35c4e8f08d2cc9593314c52'),
 ('annex-5','2008 CIRBE','4b05fcd9f1dce2acca20f425b150a2c9a406e44607b8f070ccbf1c434a8b8bb2'),
 ('annex-6','Bank account ledger','98b40d694faef9013735b69703d5d6874bc41b33fd0927ad932d7d96bdb5ff3a5'),
 ('annex-7','17 June 2008 loan','a9b008746f1ea3d26a4b197399794d25d23fde4cd4fcb7f9fac8432c2bf614e8e'),
 ('annex-8','27 May 2010 mortgage','6414fe7859cdb0aa5708cbcd07c95bdf7766cfc8bb60e7494750aab89225cf6b7'),
 ('annex-9','AC filing of 25 January 2021','d6ba42ba889bb3fdba8f0bda6a6b02f002eac273330198a06510fb8a7b4d05c7'),
 ('annex-10','Bank guarantee information','5b365f8730a1119b0cfc4777a7d8cd0b3ecfd7f825458aeba6e94715247a5c6d'),
 ('annex-11','LexNET invoice','b2f6aa222c117d184798237825e2deddee4f21c9f14e3c5041a74c6cd86c0b20')
]
# Principal fingerprint is copied from the inspected receipt, not from a same-named PDF.
components[0] = ('principal','Claim','d41a44712020991475a5f3e9df5a524d262d08d5e72e680a3b2e941b29a9d91d')
reconciliation = {
 'status':'RECEIPT_RECOVERED_EXACT_FILE_RECONCILIATION_OPEN',
 'receipt':{'sha256':'a41d6aba8a6e65878ed384c3ecb0115c00e21e287d453402849f438041884c360','pages':4,'bytes':194989,'native_publication':'WITHHELD_PRIVATE','submission_local':'2023-10-11T19:39:45','timezone':'NOT_STATED_IN_RECEIPT','receipt_generation_local':'2023-10-11T19:44:10'},
 'denominator':{'principal_pdf':1,'accompanying_pdfs':12,'total':13,'annex_labels':'0 through 11'},
 'components':[{'component':i,'label':label,'receipt_declared_fingerprint':fp,'fingerprint_algorithm':'NOT_EXPRESSLY_STATED_IN_REVIEWED_RECEIPT','exact_native_match':'OPEN'} for i,label,fp in components],
 'recovered_claim_sha256':'f44121b7ac9026d2478d82974641c9da11fe497aacd999188ada3d495fe34a77',
 'recovered_ac_20210125_sha256':'eda97315e94bb6db549bec7d30914d70a0cb2bf08a89ff405a3937c0562ac990',
 'public_claim_status':'COUNSEL_SOURCE_DERIVED_REDACTED_READING_COPY_NOT_CERTIFIED_BYTE_IDENTICAL_TO_FILED_PRINCIPAL',
 'public_ac_status':'SOURCE_DERIVED_REDACTED_READING_COPY_NOT_CERTIFIED_BYTE_IDENTICAL_TO_ANNEX_9',
 'interpretation':'The receipt establishes dispatch and a finite package inventory. Its declared claim/annex9 fingerprints have not been reconciled with recovered PDFs. Different hashes alone do not establish substantive alteration or wrongdoing. Legacy 13-Oct labels and later characterisations do not replace the observed 11-Oct dispatch date; later court registration is a separate event.',
 'custodian':'Filing procurador, counsel and complete court file',
 'closure_test':'Recover the receipt-listed principal and all twelve annexes; establish fingerprint algorithm; compare bytes and signing/conversion history; reconcile court registration separately; review each source for privacy, privilege and licensed material.',
 'no_claims':['All annexes publicly available','Every annex fully reviewed','Exact filed-version identity proved','Court admission proved by dispatch alone','Fingerprint mismatch proves misconduct']
}
assert len(components)==13 and len({r[0] for r in components})==13
m['claim_filing_reconciliation'] = reconciliation
manifest_path.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
notes = {
 'es/reclamacion-caixabank-valencia/documentos/index.html':'''<aside class="note" id="control-presentacion-11oct2023"><h3>Presentación y versión exacta: dos controles distintos</h3><p>El justificante LexNET recuperado registra la presentación el <strong>11 de octubre de 2023 a las 19:39:45</strong> (sin zona horaria indicada) y enumera <strong>un PDF principal y doce anexos, numerados 0–11</strong>. Esto acredita el envío documentado, no por sí solo admisión, reparto o identidad íntegra de cada archivo.</p><p>La copia de la demanda remitida por los profesionales y el escrito del AC de 25-Ene-2021 se ofrecen como <strong>copias de lectura disociadas</strong>. Sus archivos fuente recuperados no están reconciliados con las huellas declaradas para el principal y el anexo 9 en el justificante. No se certifica identidad byte a byte con esos adjuntos presentados. Una diferencia de huella no demuestra alteración sustantiva ni irregularidad. La referencia histórica al 13-Oct debe mantenerse separada de este envío del 11-Oct y de cualquier registro posterior.</p><p><a href="/por-derecho/data/audits/caixabank-public-derivatives-20260905.json">Ver inventario de 13 componentes, procedencia y prueba pendiente</a>. El justificante nativo queda en custodia privada; los anexos aún no cotejados no se presentan como íntegramente publicados.</p></aside>''',
 'en/caixabank-valencia-claim/documents/index.html':'''<aside class="note" id="control-presentacion-11oct2023"><h3>Submission and exact-file identity are separate controls</h3><p>The recovered LexNET receipt records dispatch on <strong>11 October 2023 at 19:39:45</strong> (timezone not stated) and lists <strong>one principal PDF and twelve annexes, labelled 0–11</strong>. It establishes the documented dispatch, not by itself court admission, allocation or the exact identity of every attachment.</p><p>The claim supplied by the legal professionals and the Administrator’s 25-Jan-2021 filing are provided as <strong>public-redacted reading copies</strong>. Their recovered source files have not been reconciled with the receipt-declared fingerprints for the principal and annex 9. Byte-for-byte identity with those submitted attachments is not certified. Different fingerprints alone do not prove substantive alteration or wrongdoing. The legacy 13-Oct reference remains separate from the observed 11-Oct dispatch and any later registration.</p><p><a href="/por-derecho/data/audits/caixabank-public-derivatives-20260905.json">See the 13-component inventory, provenance and open proof test</a>. The native receipt remains private; unreconciled annexes are not described as fully published.</p></aside>'''
}
changed=[str(manifest_path.relative_to(ROOT))]
for rel,note in notes.items():
    p=ROOT/rel;s=p.read_text()
    if 'id="control-presentacion-11oct2023"' not in s:
        anchor='<section class="section" id="copias-publicas-verificadas"><div class="shell record">'
        assert s.count(anchor)==1,rel
        s=s.replace(anchor,anchor+note,1)
        p.write_text(s)
    changed.append(rel)
control=ROOT/'CAIXABANK_360_READER_REPAIR_CONTROL_05SEP2026.md'
s=control.read_text()
heading='## Recovered 11 October 2023 receipt: exact-file identity still open'
if heading not in s:
    s+='\n\n'+heading+'\n\nThe recovered four-page receipt establishes dispatch on 11-Oct-2023 at19:39:45 and one principal plus twelve annexes(0–11). Receipt fingerprint algorithm is not expressly stated in the reviewed text. The receipt-declared principal and annex9 fingerprints differ from the respective recovered source SHA-256 values. The public derivative manifest and both source readers now preserve this limitation without implying substantive alteration, fraud or court admission. Native receipt identifiers remain private. Exact thirteen-component matching and later registration remain open.\n\nThe first final-reader regression failed because it counted the deliberately separate navigation rail and case-map section together and expected one element. The successor asserts one of each on each homepage and none on either CaixaBank landing page; it also retains contrast/tap-size checks and failure artifacts. No production acceptance threshold was relaxed.\n'
    control.write_text(s)
changed.append(str(control.relative_to(ROOT)))
Path('/tmp/caixabank-receipt-prepared-paths.json').write_text(json.dumps(changed))
print('RECEIPT_STATUS_PREPARED',len(changed),'native receipt not published')
