# CaixaBank Valencia — unitary inbound interlink control

Date: 2026-09-04
Release: CAIXABANK-VALENCIA-UNITARY-INBOUND-20260904A
Status model: protected-main PR publication.

## Purpose

Make the new Valencia document room / FAQ / OB REM cluster reachable in both directions. The CaixaBank dossier already links outward to the insolvency-administrator, lender-chain, Acosta Matos, criminal-unitary and 2022 adjudication material. This release adds the reverse path so those dossiers do not present Valencia as an isolated product dispute.

## Inbound pages

- `es/administrador-concursal-puerta-credito-titulo/`
- `es/acreedor-de-registro/responsabilidad/`
- `es/acosta-matos-perimetro/`
- `es/ingenieria-inversa-criminal-unitaria/`
- `es/adjudicacion-2022-reconstruccion-documental/`

Each receives a controlled callout linking to:

- `es/reclamacion-caixabank-valencia/faq-contexto-unitario/`
- `es/reclamacion-caixabank-valencia/documentos/`
- `es/reclamacion-caixabank-valencia/ob-rem-ac-cam-28nov2018/`

## Evidential boundary

The inbound callouts distinguish documented connection and investigative pattern from proof of collusion, concert or criminal responsibility. The Acosta Matos and criminal-unitary callouts expressly attribute the functional-agent/enabling-gatekeeper theory to Por Derecho as an allegation requiring primary proof.

## Implementation

- `assets/caixabank-valencia-unitary-inbound-interlinks-20260904.js`
- loader entry in `assets/site.js`, release `20260904a`.
