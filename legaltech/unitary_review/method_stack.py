"""Reusable multi-method forensic review stack for pd.forensic.v1 case packages.

The stack implements source-bound candidate generation and evidence-structure
mapping. It is deliberately NOT a lie detector. It never promotes a proposition
to false, knowingly false, dishonest, criminal, guilty or liable automatically.

Implemented lenses:
- ACH competing hypotheses
- SUE-style statement/evidence consistency
- Verifiability Approach candidate detail mapping
- Wigmore-style proposition/evidence graph
- FATF-style parallel financial rail
- FCA-style expected-control evidence rail
- PSFA intelligence/source-quality discipline
- PEACE-inspired account/context preservation
- FBI-style linguistic probe cues (probe only)
- NIST/ENFSI validation/competing-proposition firewall
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

CONTROL = "PD-TRUTH-METHOD-STACK-20260925-01"
SCHEMA = "por-derecho.truth-machine.method-stack.v1"
METHODS = (
    "ACH_COMPETING_HYPOTHESES",
    "SUE_STATEMENT_EVIDENCE_CONSISTENCY",
    "VERIFIABILITY_APPROACH",
    "WIGMORE_EVIDENCE_GRAPH",
    "FATF_PARALLEL_FINANCIAL_RAIL",
    "FCA_EXPECTED_CONTROL_EVIDENCE",
    "PSFA_INTELLIGENCE_DISCIPLINE",
    "PEACE_ACCOUNT_INTEGRITY",
    "FBI_LINGUISTIC_PROBE",
    "NIST_ENFSI_VALIDATION_FIREWALL",
)
HYPOTHESES = (
    "H1_ACCURATE_AS_USED",
    "H2_CORE_FACT_TRUE_SCOPE_OVERSTATED",
    "H3_CONTEXT_CHANGES_MEANING",
    "H4_DIRECTLY_CONTRADICTED",
    "H5_INSUFFICIENT_EVIDENCE",
)
FORBIDDEN_SCORES = (
    "truth_score","lie_probability","credibility_score","guilt_score",
    "linguistic_deception_score","automated_veracity_score",
)

DATE = re.compile(r"\b(?:\d{1,2}\s+de\s+[a-záéíóúñ]+\s+de\s+\d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4})\b", re.I)
AMOUNT = re.compile(r"(?:€|\beuros?\b|\bmillones?\b|\b\d[\d\.\s]*(?:,\d+)?\s*(?:€|euros?|%))", re.I)
ARTICLE = re.compile(r"\b(?:art(?:í|i)?culo|art\.?|arts\.?)\s*\d+", re.I)
PROCEDURAL = re.compile(r"\b(?:RPL|DP|DIP|PO|P\.O\.|Autos?|Sentencia|Providencia|escrito|informe|recurso|apelaci[oó]n|Juzgado|Audiencia|Fiscal[ií]a)\b", re.I)
DOCUMENT = re.compile(r"\b(?:correo|email|e-mail|escrito|informe|factura|cuentas|documentaci[oó]n|contrato|certificado|acta|transferencia|pago|extracto|registro|resoluci[oó]n|sentencia|auto)\b", re.I)
NAMED = re.compile(r"\b(?:Marer|Aweswell|Luchy|Acosta|Matos|Rodríguez-Batllori|Clubotel|ONA|Grant Thornton|PwC|RSM|CaixaBank|ACTÚA|CEXP)\b", re.I)

FINANCIAL = {
    "AMOUNT": AMOUNT,
    "PAYMENT": re.compile(r"\b(?:pago|pagad[oa]|abon[oa]|transferencia|ingreso|desembolso|cobro|cobr[oa])\w*\b", re.I),
    "DEBT_CREDIT": re.compile(r"\b(?:deuda|cr[eé]dito|acreedor|pr[eé]stamo|saldo|financiaci[oó]n|financiado|hipoteca)\w*\b", re.I),
    "INVOICE": re.compile(r"\b(?:factura|honorarios|presupuesto)\w*\b", re.I),
    "ACCOUNT": re.compile(r"\b(?:cuenta|bancari[oa]|extracto|contabilidad|contable|libro mayor)\w*\b", re.I),
}
CONTROL_CUES = {
    "AUTHORITY_APPROVAL": re.compile(r"\b(?:autoriza|autorizaci[oó]n|aprobaci[oó]n|acuerdo|consentimiento|mandato|facultad|permiso)\w*\b", re.I),
    "FILING_NOTICE": re.compile(r"\b(?:present[oó]|presentado|escrito|notificaci[oó]n|comunicaci[oó]n|requerimiento|solicitud|informe|certificaci[oó]n)\w*\b", re.I),
    "ACCOUNTING_RECORD": re.compile(r"\b(?:cuentas anuales|contabilidad|documentaci[oó]n contable|libros?|asiento|factura|extracto|balance)\b", re.I),
    "VALUATION_TRANSACTION": re.compile(r"\b(?:tasaci[oó]n|valoraci[oó]n|adjudicaci[oó]n|daci[oó]n|compraventa|transmisi[oó]n|cesi[oó]n|precio)\b", re.I),
}
LINGUISTIC = {
    "HEDGE_MODAL": re.compile(r"\b(?:podr[ií]a|puede|pudiera|cabe razonablemente|razonable pensar|presumiblemente|aparentemente|parece|probablemente|quiz[aá]|posiblemente)\b", re.I),
    "ABSOLUTE_QUANTIFIER": re.compile(r"\b(?:todos?|todas?|ning[uú]n|ninguna|nunca|siempre|exclusivamente|[uú]nicamente|totalmente)\b", re.I),
    "CAUSAL_LANGUAGE": re.compile(r"\b(?:porque|por tanto|consecuentemente|como consecuencia|debido a|refuerza la conclusi[oó]n|demuestra|acredita|resultado de)\b", re.I),
    "RHETORIC_ATTACK": re.compile(r"\b(?:delirante|obsesiv[oa]|absurd[oa]|difamatori[oa]|fabulos[oa]|frustraci[oó]n|torpedear|ret[oó]rica vac[ií]a)\b", re.I),
    "NEGATION_DENIAL": re.compile(r"\b(?:no|nunca|ning[uú]n|ninguna|jam[aá]s)\b", re.I),
    "PROCEDURAL_STATE": re.compile(r"\b(?:borrador|presentad[oa]|recibid[oa]|admitid[oa]|resuelto|sentencia|auto|providencia|apelaci[oó]n|firme|archivo|sobreseimiento)\b", re.I),
}

class MethodStackError(ValueError):
    pass

def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",",":"), allow_nan=False).encode("utf-8")).hexdigest()

def _features(text: str) -> list[str]:
    out=[]
    if DATE.search(text): out.append("DATE_OR_YEAR")
    if AMOUNT.search(text): out.append("AMOUNT_OR_PERCENT")
    if ARTICLE.search(text): out.append("LEGAL_PROVISION")
    if PROCEDURAL.search(text): out.append("PROCEDURAL_OR_FILING_REF")
    if DOCUMENT.search(text): out.append("DOCUMENT_OR_TRANSACTION_REF")
    if NAMED.search(text): out.append("NAMED_ACTOR_OR_ENTITY")
    return out

def _matched(mapping: dict[str,re.Pattern], text: str) -> list[str]:
    return [name for name,pattern in mapping.items() if pattern.search(text)]

def _page(record: dict) -> int | None:
    m=re.search(r"-P(\d{2})-", str(record.get("id","")))
    return int(m.group(1)) if m else None

def _sue_state(status: str, contrary: bool) -> str:
    if status=="SUPPORTED": return "CURRENTLY_SUPPORTED_IN_INPUT"
    if status=="PARTIAL" and contrary: return "MIXED_WITH_CONTRARY_RELATION"
    if status=="PARTIAL": return "PARTIAL_OR_NARROWING"
    if status=="RHETORICAL_OR_LEGAL": return "NON_BINARY_RHETORIC_OR_LEGAL"
    return "OPEN_NOT_SOURCE_RESOLVED"

def _ach_state(status: str, contrary: bool) -> str:
    if status=="SUPPORTED": return "H1_ACCURATE_CURRENTLY_HAS_SUPPORT"
    if status=="PARTIAL" and contrary: return "H2_OR_H4_NARROWING_OR_CONTRADICTION_ACTIVE"
    if status=="PARTIAL": return "H2_NARROWER_THAN_USED_ACTIVE"
    if status=="RHETORICAL_OR_LEGAL": return "NON_BINARY_EXCLUDED_FROM_FACTUAL_ACH"
    return "H1_TO_H5_OPEN_INSUFFICIENT_CURRENT_REVIEW"

def _falsehood_state(status: str, contrary: bool) -> str:
    if contrary: return "CONTRADICTION_REVIEW_CANDIDATE"
    if status=="PARTIAL": return "NARROWING_OR_MISLEADING_USE_CANDIDATE"
    if status=="SUPPORTED": return "CURRENTLY_SUPPORTED"
    if status=="RHETORICAL_OR_LEGAL": return "NON_BINARY_RHETORIC_OR_LEGAL"
    return "OPEN_UNRESOLVED"

def analyse_case(case: dict) -> tuple[dict,dict]:
    if not isinstance(case,dict) or case.get("schema")!="pd.forensic.v1":
        raise MethodStackError("pd.forensic.v1 case required")
    document=case.get("document") or {}
    if not document.get("id") or not re.fullmatch(r"[0-9a-fA-F]{64}", str(document.get("sha256",""))):
        raise MethodStackError("document id and recorded SHA-256 required")
    annotations=case.get("annotations")
    blocks=case.get("blocks")
    if not isinstance(annotations,list) or not isinstance(blocks,list):
        raise MethodStackError("blocks and annotations required")
    statements=[a for a in annotations if a.get("origin")=="LIAR_LIAR_FULL_V3_STATEMENT"]
    ids=[a.get("id") for a in statements]
    if not statements or len(ids)!=len(set(ids)) or any(not x for x in ids):
        raise MethodStackError("nonempty unique statement records required")
    original=digest(case)
    records=[]
    counters=defaultdict(int)
    ver_types=Counter(); fin_types=Counter(); ctrl_types=Counter(); ling_types=Counter()
    sue=Counter(); ach=Counter(); false=Counter(); pages=defaultdict(Counter)
    all_evidence=[]
    false_candidates=[]
    for ann in statements:
        text=ann.get("quote")
        if not isinstance(text,str) or not text:
            raise MethodStackError("statement quote required")
        truth=ann.get("truth") or {}
        status=truth.get("status","UNRESOLVED")
        evidence=ann.get("evidence") or []
        contrary=[e for e in evidence if e.get("relation")=="CONTRADICTS"]
        all_evidence.extend(evidence)
        vf=_features(text); fin=_matched(FINANCIAL,text); ctrl=_matched(CONTROL_CUES,text); ling=_matched(LINGUISTIC,text)
        if vf:counters["verifiability"]+=1
        if fin:counters["financial"]+=1
        if ctrl:counters["control"]+=1
        if ling:counters["linguistic"]+=1
        ver_types.update(vf);fin_types.update(fin);ctrl_types.update(ctrl);ling_types.update(ling)
        ss=_sue_state(status,bool(contrary)); aa=_ach_state(status,bool(contrary)); ff=_falsehood_state(status,bool(contrary))
        sue[ss]+=1;ach[aa]+=1;false[ff]+=1
        page=_page(ann); pm=pages[page]; pm["statements"]+=1
        if vf:pm["verifiable"]+=1
        if fin:pm["financial"]+=1
        if ctrl:pm["control"]+=1
        if ling:pm["linguistic"]+=1
        if contrary:pm["contradiction_candidate"]+=1
        pm[status.lower()]+=1
        sources=sorted({e.get("source") for e in evidence if e.get("source")})
        rec={
            "id":ann["id"],"page":page,"block":ann.get("block"),"quote":text,
            "existing_input":{"status":status,"decision":truth.get("decision"),"knowledge":truth.get("knowledge","NOT_ASSESSED"),"causation":truth.get("causation","NOT_ASSESSED")},
            "source_lineage":{"evidence_links":len(evidence),"related_links":sum(e.get("relation")=="RELATED" for e in evidence),
                              "contradicts_links":len(contrary),"source_families":sources},
            "verifiability_approach":{"candidate":bool(vf),"detail_types":vf,"verification_result":"NOT_INFERRED_FROM_CUE"},
            "sue_statement_evidence":{"state":ss,"interview_strategy_simulated":False},
            "ach":{"state":aa,"hypotheses":list(HYPOTHESES),"probabilities_assigned":False},
            "wigmore":{"proposition_node":ann["id"],"evidence_source_nodes":sources,"contrary_edges":len(contrary)},
            "financial_rail":{"candidate":bool(fin),"cue_types":fin,"money_trace_complete":False},
            "expected_control_evidence":{"candidate":bool(ctrl),"cue_types":ctrl,"control_artifact_check_complete":False},
            "linguistic_probe":{"candidate":bool(ling),"cue_types":ling,"deception_inference_allowed":False},
            "falsehood_register":{"state":ff,"source_complete_signoff":False,"knowingly_false":False,
                                  "knowledge_evidence_established":truth.get("knowledge")=="SOURCE_REVIEW_RECORDED"}
        }
        for key in FORBIDDEN_SCORES:
            if key in rec:
                raise MethodStackError("forbidden score generated")
        records.append(rec)
        if contrary:
            false_candidates.append({"id":ann["id"],"page":page,"state":"CONTRADICTION_REVIEW_CANDIDATE_NOT_SIGNED_OFF",
                                     "contrary_sources":[{"source":e.get("source"),"locator":e.get("locator")} for e in contrary],
                                     "knowledge_state":truth.get("knowledge","NOT_ASSESSED"),
                                     "causation_state":truth.get("causation","NOT_ASSESSED")})
    source_families=sorted({e.get("source") for e in all_evidence if e.get("source")})
    private={
        "schema":SCHEMA+".private","control":CONTROL,
        "document":{"id":document["id"],"title":document.get("title"),"native_sha256":document["sha256"]},
        "methods":list(METHODS),"records":records,
        "input_sha256":original,"source_inputs_modified":False,
        "automatic_merits_promotions":0,
        "boundary":"Candidate generation and evidence-structure mapping only; no automatic lie/falsity/intent/guilt/liability finding."
    }
    public={
        "schema":SCHEMA+".aggregate","control":CONTROL,
        "document":{"id":document["id"],"title":document.get("title"),"native_sha256":document["sha256"]},
        "structure":{"blocks":len(blocks),"statement_propositions":len(statements),
                     "paragraph_composites":len(annotations)-len(statements),"review_records":len(annotations)},
        "method_coverage":{
            "ACH":{"processed":len(statements),"probabilities_assigned":0,"states":dict(ach)},
            "SUE":{"processed":len(statements),"states":dict(sue),"interview_strategy_simulated":False},
            "VERIFIABILITY":{"processed":len(statements),"candidate_statements":counters["verifiability"],"cue_types":dict(ver_types),"truth_inference_from_ratio":False},
            "WIGMORE":{"proposition_nodes":len(statements),"evidence_source_families":len(source_families),"statement_evidence_edges":len(all_evidence),"contrary_edges":sum(e.get("relation")=="CONTRADICTS" for e in all_evidence)},
            "FATF_FINANCIAL":{"processed":len(statements),"candidate_statements":counters["financial"],"cue_types":dict(fin_types),"completed_money_traces":0},
            "FCA_CONTROLS":{"processed":len(statements),"candidate_statements":counters["control"],"cue_types":dict(ctrl_types),"completed_control_artifact_reconciliations":0},
            "FBI_LINGUISTIC_PROBE":{"processed":len(statements),"candidate_statements":counters["linguistic"],"cue_types":dict(ling_types),"deception_findings":0},
        },
        "falsehood_register":{"states":dict(false),"contradiction_review_candidates":len(false_candidates),
                              "source_complete_falsehood_signoffs":0,"knowingly_false_signoffs":0,
                              "candidates":false_candidates},
        "knowledge_states":dict(Counter(a.get("truth",{}).get("knowledge","NOT_ASSESSED") for a in statements)),
        "causation_states":dict(Counter(a.get("truth",{}).get("causation","NOT_ASSESSED") for a in statements)),
        "page_metrics":{str(k):dict(v) for k,v in sorted(pages.items())},
        "validation":{"statement_records_processed":len(statements),"source_inputs_modified":False,"automatic_merits_promotions":0},
        "boundary":"Review workload and structured evidential states; not a truth, lie, credibility, intent, guilt or liability score."
    }
    if digest(case)!=original:
        raise MethodStackError("source case mutated")
    return private,public

def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument("case",type=Path)
    parser.add_argument("--private-out",type=Path,required=True)
    parser.add_argument("--public-out",type=Path,required=True)
    ns=parser.parse_args()
    data=json.loads(ns.case.read_text(encoding="utf-8"))
    private,public=analyse_case(data)
    for path,obj in ((ns.private_out,private),(ns.public_out,public)):
        if path.exists(): raise MethodStackError("refusing to overwrite existing output")
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()