# REG/RedSARA canonical reconciliation — 21 September 2026

## Current-main denominator

The supplied REG/RedSARA status export contains **398 distinct REGAGE references** covering **7 December 2025 through 21 September 2026**.

- Literal `Recibido`: **336**
- Literal `Enviado`: **36**
- Literal `Rechazado`: **26**
- Existing dedicated formal-registration events reused from current main: **92**
- Status events added to current main: **306**
- Of those additions, REGAGE identities already reserved in the pending DP1901/E.G.745 mapping are preserved: **22**
- Remaining generic status additions: **284**, allocated `PD-SP-EVT-0213` through `PD-SP-EVT-0496`
- Canonical event total after reconciliation: **641**

Two separately reserved DP1901 A02 identifiers are S-references rather than REGAGE registrations and therefore are outside this 398-row REGAGE reconciliation.

The raw CSV is not committed because it contains personal identity fields. Its controlled SHA-256 is `5cc7eaa867b248b0bff7e9cd19e5093dfe2df494fae8ca84c8f12c15382016a3`. The committed public-safe derivative is `ops/regage-status-export-input-20260921.json`.

## Proof boundary

The export is treated strictly as a registry-status source. `Recibido`, `Enviado` and `Rechazado` are preserved literally. No status is upgraded into a claim of onward delivery, internal routing, incorporation, admission, substantive examination, merits acceptance, requested relief or criminal responsibility.

The historical 75-receipt baseline and earlier 22-record aggregate remain provenance. The 398-row source supplies the current individual status census; no unsupported one-to-one mapping of the old aggregate is inferred.

The 22 preassigned REGAGE IDs preserve identity continuity only. Richer native-receipt/hash proof, where separately controlled, is not inferred from this CSV.

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
