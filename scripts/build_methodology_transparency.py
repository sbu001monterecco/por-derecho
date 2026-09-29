#!/usr/bin/env python3
"""Render/check the bilingual public methodology projection from one public model."""
import argparse, hashlib, html, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/"assets/data/methodology-transparency-v1.json"
EXPECTED=["observe","manifest","compare","classify","traverse","adversarial","reconcile","verify","deploy","readback","envelope"]
ORIGINS={
    "github":"https://sbu001monterecco.github.io/por-derecho",
    "gitlab":"https://por-derecho.gitlab.io/por-derecho-setup-or-gitlab-setup",
}

def load_model():
    return json.loads(MODEL.read_text(encoding="utf-8"))

def git_blob_sha(path):
    data=path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()

def validate_model(m):
    ids=[x["id"] for x in m["recursive_sequence"]]
    if ids!=EXPECTED: raise ValueError(f"stage order drift: observed={ids} expected={EXPECTED}")
    if m.get("public_release_approved") is not False or m.get("live_verified") is not False:
        raise ValueError("candidate model cannot claim publication approval or live verification")
    if m["constitutional"].get("safeguards_self_modify") is not False:
        raise ValueError("constitutional safeguards cannot self-modify")
    return m

def esc(x): return html.escape(str(x),quote=True)

def flow(items):
    return " ".join(("&rarr; " if i else "")+f"<span>{esc(x.replace('_',' '))}</span>" for i,x in enumerate(items))

def render(lang,host):
    m=validate_model(load_model()); origin=ORIGINS[host]; is_en=lang=="en"
    route="/en/methodology/" if is_en else "/es/metodologia/"
    alt="/es/metodologia/" if is_en else "/en/methodology/"
    blob=git_blob_sha(MODEL)
    title="Evidence before conclusion." if is_en else "Evidencia antes que conclusión."
    lead=("A recursive, adversarial and auditable method for deciding what we know, what we allege, what we publish—and what we change when new evidence appears."
          if is_en else "Un método recursivo, adversarial y auditable para decidir qué sabemos, qué alegamos, qué publicamos y qué cambiamos cuando aparece nueva evidencia.")
    stages=[]
    for s in m["recursive_sequence"]:
        t=s[lang]
        stages.append(f'<li class="method-stage" data-method-stage="{s["id"]}" data-method-order="{s["order"]}"><h3>{esc(t["title"])}</h3><p class="tagline">{esc(t["tagline"])}</p><p>{esc(t["body"])}</p><details><summary>{"What can stop this stage?" if is_en else "¿Qué puede detener esta etapa?"}</summary><p>{esc(t["stop"])}</p></details></li>')
    neq="".join(f"<tr><td>{esc(r[0] if is_en else r[1])}</td><td>{esc(r[2] if is_en else r[3])}</td></tr>" for r in m["non_equivalences"])
    roles="".join(f'<article class="role-card"><span>{esc(r["id"])}</span><h3>{esc(r[lang]["title"])}</h3><p>{esc(r[lang]["body"])}</p></article>' for r in m["supervised_roles"])
    hosts="".join(f'<article class="host-card"><span>{esc(r["id"])}</span><h3>{esc(r[lang])}</h3><p>{esc(r["body_"+lang])}</p></article>' for r in m["host_states"])
    hist="".join(f'<article class="arch-row"><time datetime="{r["date"]}">{r["date"]}</time><span class="arch-status">{esc(r["status"])}</span><div><strong>{esc(r["control"])}</strong><p>{esc(r[lang])}</p></div></article>' for r in m["architecture_history"])
    parity="".join(f'<article class="parity-card"><span>{esc(r["id"])}</span><h3>{esc(r[lang])}</h3><p>{esc(r["body_"+lang])}</p></article>' for r in m["parity_states"])
    controls="".join(f'<div class="machine-item"><code>{esc(r["id"])}</code><span>{esc(r["status"])}</span></div>' for r in m["source_controls"])
    key=m["two_key"][lang]
    return f'''<!doctype html>
<html lang="{lang}" data-methodology-control="{m["control_id"]}" data-methodology-model-blob="{blob}" data-projection-host="{host}" data-publication-status="PUBLIC_SAFE_CANDIDATE" data-private-boundary="true" data-live-verified="false">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Project Sun Rock</title><meta name="description" content="{esc(lead)}"><link rel="canonical" href="{origin}{route}"><link rel="alternate" hreflang="{lang}" href="{origin}{route}"><link rel="alternate" hreflang="{"es" if is_en else "en"}" href="{origin}{alt}"><link rel="stylesheet" href="../../assets/styles.css"><link rel="stylesheet" href="../../assets/methodology-transparency-20260922.css"><script src="../../assets/site.js" defer></script></head>
<body class="methodology-page"><main id="content">
<section class="method-hero"><div class="shell"><p class="eyebrow">{"PUBLIC METHODOLOGY · EVIDENCE CONTROL · RECURSIVE REVIEW" if is_en else "METODOLOGÍA PÚBLICA · CONTROL PROBATORIO · REVISIÓN RECURSIVA"}</p><h1>{esc(title)}</h1><p class="lead">{esc(lead)}</p></div></section>
<section class="method-section" id="loop"><div class="shell"><h2>{"The public operating loop" if is_en else "El ciclo operativo público"}</h2><ol class="method-loop">{"".join(stages)}</ol><div class="recurse-arrow"><b>↺</b><span>{"New evidence, correction, host change or failed check reopens the loop" if is_en else "Nueva evidencia, corrección, cambio de host o control fallido reabre el ciclo"}</span></div></div></section>
<section class="method-section alt"><div class="shell"><div class="constitution"><strong>{"The loop is recursive. The constitution is not." if is_en else "El ciclo es recursivo. La constitución no."}</strong><p>{esc(m["public_private"][lang])}</p></div><div class="two-key"><article class="key-card"><h3>{esc(key["a"]["title"])}</h3><p>{esc(key["a"]["body"])}</p></article><article class="key-card"><h3>{esc(key["b"]["title"])}</h3><p>{esc(key["b"]["body"])}</p></article><div class="two-key-rule">{esc(key["rule"])}</div></div></div></section>
<section class="method-section"><div class="shell"><h2>{"What one thing does not mean" if is_en else "Lo que una cosa no significa"}</h2><table class="non-eq"><tbody>{neq}</tbody></table></div></section>
<section class="method-section dark"><div class="shell"><h2>{"Supervised intelligence" if is_en else "Inteligencia supervisada"}</h2><div class="role-grid">{roles}</div></div></section>
<section class="method-section alt"><div class="shell"><h2>{"Interconnected tools, distinct authority" if is_en else "Herramientas interconectadas, autoridad distinta"}</h2><div class="host-grid">{hosts}</div></div></section>
<section class="method-section"><div class="shell"><h2>{"Architecture history is preserved" if is_en else "La historia de arquitectura se conserva"}</h2><div class="arch-history">{hist}</div><div class="parity-grid">{parity}</div></div></section>
<section class="method-section alt"><div class="shell"><h2>{"How we correct ourselves" if is_en else "Cómo nos corregimos"}</h2><div class="flow-strip">{flow(m["correction_flow"])}</div><h2>{"How the method improves" if is_en else "Cómo mejora el método"}</h2><div class="flow-strip">{flow(m["improvement_pipeline"])}</div></div></section>
<section class="method-section dark"><div class="shell"><h2>{"Inspect the machine-readable method" if is_en else "Inspeccione el método legible por máquina"}</h2><div class="machine-list">{controls}</div></div></section>
</main></body></html>'''

def check_current(lang,host):
    m=validate_model(load_model()); path=ROOT/m["routes"][lang]; text=path.read_text(encoding="utf-8")
    expected_blob=git_blob_sha(MODEL)
    for token in [f'data-methodology-model-blob="{expected_blob}"',f'data-projection-host="{host}"']:
        if token not in text: raise ValueError(f"render marker missing: {token}")
    last=-1
    for order,sid in enumerate(EXPECTED,1):
        pos=text.find(f'data-method-stage="{sid}" data-method-order="{order}"')
        if pos<0 or pos<=last: raise ValueError(f"stage missing/out of order: {sid}")
        last=pos
    return path

def main():
    p=argparse.ArgumentParser(); p.add_argument("--host",choices=ORIGINS,required=True); p.add_argument("--check",action="store_true"); p.add_argument("--write",action="store_true")
    args=p.parse_args(); m=validate_model(load_model())
    if args.write:
        for lang in ("en","es"):
            path=ROOT/m["routes"][lang]; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(render(lang,args.host),encoding="utf-8")
        print(json.dumps({"status":"WROTE","host":args.host,"model_blob":git_blob_sha(MODEL)},sort_keys=True)); return
    if args.check:
        for lang in ("en","es"): check_current(lang,args.host)
        print(json.dumps({"status":"PASS","host":args.host,"control_id":m["control_id"],"model_blob":git_blob_sha(MODEL)},sort_keys=True)); return
    raise SystemExit("Choose --write or --check")

if __name__=="__main__": main()
