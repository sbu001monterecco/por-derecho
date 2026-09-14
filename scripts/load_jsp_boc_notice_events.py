#!/usr/bin/env python3
"""Source-controlled BOC cohort for the existing canonical event builder.

The input is the reviewed notice specification, not the output register. This
loader allocates no IDs and claims no delivery, final decision or new filing.
"""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path

EXPECTED=[('2006-09-20','inspection-20754'),('2007-01-24','inspection-21200'),('2007-02-13','inspection-21016'),('2007-04-11','inspection-21417'),('2007-07-04','inspection-21878'),('2008-02-14','inspection-22715'),('2008-08-04','initiation'),('2008-08-17','defence-date'),('2008-08-28','defence-receipt'),('2008-10-16','proposal'),('2008-11-25','publication-resolution'),('2008-12-09','publication')]
PDF='assets/evidence/jsp-2017/BOC-2008-245-4927.pdf'
SHA='21d92223ac38b894054cc4ef70d7073df7d81de8da8ed2d53cc813e159041fc0'

def pretty(s):
    s=re.sub(r'(?<=[a-záéíóúñ])(?=(?:19|20)\d{2})',' ',s,flags=re.I)
    s=re.sub(r'((?:19|20)\d{2})(?=[a-záéíóúñ])',r'\1 ',s,flags=re.I)
    s=re.sub(r',(?=[A-Za-zÁÉÍÓÚñ])',', ',s)
    return re.sub(r'(?<=%)(?=[a-zA-Z])',' ',s)

def load_boc_notice_events(root:Path)->list[dict]:
    spec=json.loads((root/'archive/jsp-boc-execution-spec-20260905.json').read_text())
    if spec['control_id']!='PD-JSP-BOC-SIX-20260905' or spec['source_id']!='JSP-DOC-017':raise ValueError('Wrong BOC source identity')
    if [(r[0],r[1])for r in spec['events']]!=EXPECTED:raise ValueError('BOC dated event input changed')
    data=(root/PDF).read_bytes()
    if len(data)!=49291 or hashlib.sha256(data).hexdigest()!=SHA:raise ValueError('Native BOC source changed')
    rows=[]
    for index,(date,key,es,en)in enumerate(spec['events'],179):
        eid=f'PD-SP-EVT-{index:04d}'
        rows.append({'event_id':eid,'cohort':'CURATED_SOURCE_PROVED_EVENT','layer':'OFFICIAL_ACT_OR_CORRESPONDENCE','source_key':'BOC:2008/245/4927:'+key,'record_type':'OFFICIAL_NOTIFICATION'if key=='publication'else'OFFICIAL_ACT_UNCLASSIFIED','event_date':date,'direction':'OUTBOUND_TO_INSTITUTION'if key.startswith('defence')else'INBOUND_FROM_INSTITUTION','channel':'HISTORICAL_OFFICIAL_GAZETTE_RECITAL_NOT_DELIVERY_TO_GIL','office':'Historical Dirección General de Ordenación y Promoción Turística — Canarias','official_reference':'BOC245/2008 notice4927; expediente308/07; '+key,'matter_references':['PD-JSP-INC-2017-01','JSP-DOC-017','308/07'],'source_integrity':{'status':'NATIVE_OFFICIAL_GAZETTE_CAPTURE_WITH_REPORTED_UNDERLYING_ACTS','repository_anchor':PDF,'sha256':SHA},'evidence_state':{'transmission':'OFFICIAL_PUBLICATION_LOCATED; UNDERLYING ACT AS REPORTED','registration':'1140075 ONLY FOR THE REPORTED DEFENCE RECEIPT'if key=='defence-receipt'else'NO_SEPARATE_RECEIPT_INFERRED','filing':'HISTORICAL_SOURCE_RECITAL_NOT_A_NEW_FILING','destination':'HISTORICAL_TOURISM_FILE_AND_MONTE_LANZA; NOT_GIL','delivery':'NO_SERVICE_ON_GIL_OR_NEW_SERVICE_CLAIM','internal_association':'ONLY_THE_308_07_ASSOCIATION_IN_THE_NOTICE','substantive_examination':'ONLY_AS_RECORDED_IN_THE_PROPOSAL','merits':'PROPOSED_SANCTION_NOT_FINAL_OUTCOME'},'proves':['The official notice records this dated act; original inspection/representation records remain separately recoverable.'],'does_not_prove':['Final sanction, service on Gil, guilt, complete source dossier, current office, later ownership or responsibility of related people.'],'public_summary':pretty(en),'public_summary_es':pretty(es),'attribution_state':'INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED','linked_transport_event_ids':[],'transport_link_state':'HISTORICAL_RECITAL_NOT_MAILBOX_TRANSPORT','proof_level':'OFFICIAL_NOTICE_DIRECT; UNDERLYING_RECORD_NOT_NEWLY_OBTAINED','canonical_anchor_es':'es/jsp-montelanza-concurso-liquidacion/#communication-'+eid,'canonical_anchor_en':'en/jsp-montelanza-insolvency-liquidation/#communication-'+eid})
    return rows
