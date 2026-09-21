# REG/RedSARA status-export reconciliation — 21 September 2026

## Canonical result

The user-supplied REG/RedSARA status export contains **398 distinct REGAGE references** from **7 December 2025 through 21 September 2026**.

- Literal status `Recibido`: **336**
- Literal status `Enviado`: **36**
- Literal status `Rechazado`: **26**
- Existing dedicated formal-registration events reused: **114**
- New formal-registration status events allocated: **284**
- New event-ID band: **PD-SP-EVT-0213 through PD-SP-EVT-0496**
- Canonical target: `assets/data/institutional-communications-register-v1.json`

The raw CSV is **not** committed because it contains personal identity fields. Its SHA-256 is controlled as `5cc7eaa867b248b0bff7e9cd19e5093dfe2df494fae8ca84c8f12c15382016a3`. The public-safe derivative is `ops/regage-status-export-input-20260921.json`.

## Proof boundary

The export is a registry-status source. Each row proves only that the supplied export records the stated REGAGE reference, stated destination, timestamp and literal status. `Recibido`, `Enviado` and `Rechazado` are preserved literally and are not upgraded into broader claims about onward delivery, routing, incorporation, admission, examination, merits, requested relief or criminal responsibility.

The prior 75-receipt baseline and the historical 22-record aggregate remain provenance. The 398-row export supersedes the old aggregate as the current individual-status denominator without inventing an unsupported one-to-one mapping between the old 22-record aggregate and particular rows.

## Largest stated destination groups

- Fiscalia Provincial de Las Palmas: **53**
- Comisionado de Transparencia y Acceso a la Información Pública: **18**
- Fiscalia de la Comunidad Autonoma de Canarias: **18**
- Fiscalía General del Estado: **17**
- Consejería de Presidencia, Administraciones Públicas, Justicia y Seguridad: **15**
- Unidad de Registro y Archivo del Consejo General del Poder Judicial (CGPJ): **14**
- Agencia Estatal de Administración Tributaria: **13**
- Ayuntamiento de Yaiza: **13**
- Cabildo Insular de Lanzarote: **12**
- Intervención General: **11**
- Comandancia de Las Palmas: **10**
- Comisión Nacional del Mercado de Valores: **10**
- Dirección General de Fondos Europeos: **9**
- Dirección General del Tesoro y Política Financiera: **9**
- Fiscalia Especial contra la Corrupcion y Criminalidad Organizada: **9**
- Comisaría Provincial de Las Palmas: **8**
- Agencia Tributaria Canaria: **7**
- Dirección General de Transparencia y Participación Ciudadana: **7**
- Fiscalia Provincial de Santa Cruz de Tenerife: **7**
- Gerencia Territorial del Ministerio de la Presidencia, Justicia y Relaciones con las Cortes de Canarias en Las Palmas de Gran Canaria: **7**

## Reconciliation controls

Existing formal-registration IDs are never renumbered. New IDs use the previously unused 0213–0496 band in chronological order. The mailbox transport band at 1001+ is untouched. The source derivative omits identity-document fields, names, representative fields and the free-text subject.
