#!/usr/bin/env python3
"""One-shot, assertion-led patch for the 29 August 2026 continuity truth repair."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if new in text:
        return
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one old fragment, found {count}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


EN_STATE = '''<section class="boundary" data-c36-continuity-truth="20260829"><h2>Operational control and evidential record are distinct</h2><p><strong>This route controls restart, release lineage, deployment and readback.</strong> The substantive evidential record remains in the <a href="../insolvency-36-2012-orders-decisions/">decisions and orders dossier</a>. A green deployment does not close an evidential gap, and an open evidence gate does not mean publication failed.</p><div class="table-wrap" style="margin-top:18px"><table><thead><tr><th>State field</th><th>Controlled value</th></tr></thead><tbody><tr><td>CURRENT_MAIN</td><td>Resolve afresh at runtime; last observed before this repair: <code>0b0423820942cb95f7a98e8d6fc519f6a9482a04</code></td></tr><tr><td>RELEASE_SHA</td><td><code>0b0423820942cb95f7a98e8d6fc519f6a9482a04</code> (PR #1190)</td></tr><tr><td>SCOPED_VALIDATION</td><td>Must pass on the exact proposed source</td></tr><tr><td>GLOBAL_INTEGRITY</td><td>Must be evaluated independently from evidential closure</td></tr><tr><td>PAGES_DEPLOYMENT</td><td>Release deployment passed: run 33233442563</td></tr><tr><td>EXACT_ROUTE_READBACK</td><td>Required for the bilingual routes and machine register</td></tr><tr><td>EVIDENCE_CLOSURE</td><td>OPEN — P0/P1 gates remain controlled below</td></tr><tr><td>DELETION_SAFE</td><td>NO until the deletion audit records every release gate</td></tr></tbody></table></div></section>'''

ES_STATE = '''<section class="boundary" data-c36-continuity-truth="20260829"><h2>El control operativo y el expediente probatorio son distintos</h2><p><strong>Esta ruta controla la reanudación, el linaje de publicación, el despliegue y la lectura externa.</strong> El expediente probatorio sustantivo permanece en el <a href="../concurso-36-2012-autos-resoluciones/">dossier de autos y resoluciones</a>. Un despliegue correcto no cierra una laguna probatoria, y una laguna abierta no significa que la publicación haya fallado.</p><div class="table-wrap" style="margin-top:18px"><table><thead><tr><th>Campo de estado</th><th>Valor controlado</th></tr></thead><tbody><tr><td>CURRENT_MAIN</td><td>Resolver de nuevo en cada ejecución; último main observado antes de esta reparación: <code>0b0423820942cb95f7a98e8d6fc519f6a9482a04</code></td></tr><tr><td>RELEASE_SHA</td><td><code>0b0423820942cb95f7a98e8d6fc519f6a9482a04</code> (PR #1190)</td></tr><tr><td>SCOPED_VALIDATION</td><td>Debe aprobar sobre la fuente exacta propuesta</td></tr><tr><td>GLOBAL_INTEGRITY</td><td>Debe evaluarse separadamente del cierre probatorio</td></tr><tr><td>PAGES_DEPLOYMENT</td><td>Despliegue de la publicación aprobado: ejecución 33233442563</td></tr><tr><td>EXACT_ROUTE_READBACK</td><td>Obligatoria para las dos rutas y el registro máquina</td></tr><tr><td>EVIDENCE_CLOSURE</td><td>ABIERTO — se conservan los controles P0/P1 siguientes</td></tr><tr><td>DELETION_SAFE</td><td>NO hasta que la auditoría de borrado registre todos los controles</td></tr></tbody></table></div></section>'''

replace_once(
    "en/insolvency-36-2012-continuity-control/index.html",
    "<h1>Continuity closed. Evidence gaps remain open.</h1>",
    "<h1>Continuation control reconciled; evidential closure remains open.</h1>",
)
replace_once(
    "en/insolvency-36-2012-continuity-control/index.html",
    '<main class="wrap">',
    '<main class="wrap">\n' + EN_STATE,
)
replace_once(
    "es/concurso-36-2012-control-continuidad/index.html",
    "<h1>Continuidad cerrada. Las lagunas probatorias siguen abiertas.</h1>",
    "<h1>Control de continuidad conciliado; el cierre probatorio sigue abierto.</h1>",
)
replace_once(
    "es/concurso-36-2012-control-continuidad/index.html",
    '<main class="wrap">',
    '<main class="wrap">\n' + ES_STATE,
)

replace_once(
    "scripts/production_smoke_check.py",
    '''    {"path": "assets/site.js", "markers": ["site-pre-intervencion-highlight-20260820.js?v=20260824e", "intervencion-protected-assets-highlight-20260820.js?v=20260820a"],
     "kind": "global_loader", "min_bytes": 1000},''',
    '''    {"path": "assets/site.js", "markers": ["site-pre-treasury-154-hq-20260828.js?v=20260828a", "treasury-154-hq-visual-20260828.js?v=20260828c", "data-pre-treasury-154-site-loader"],
     "kind": "global_loader", "min_bytes": 700},''',
)

print("continuity truth repair patch applied")
