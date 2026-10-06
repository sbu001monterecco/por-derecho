# Cross-host and public-site omission audit — 26 September 2026

**Control:** PD-CROSSHOST-OMISSION-AUDIT-20260926-01  
**Status:** ACTIVE — omission-first — no exhaustion certification

## Purpose

Critically compare GitHub main, GitLab main and the public website/projection for omissions, silent relocations, stale publication controls, missing actors/images/evidence routes, host-specific newer work and provenance drift. Neither repository is presumed complete or subordinate to the other.

## Initial full-tree census

- GitHub main: **6,724 blobs** (8,247 total tree entries; tree not truncated).
- GitLab main: **5,239 blobs** (6,656 total tree entries).
- Shared blob paths: **2,178**.
- Shared paths with identical Git object IDs: **1,076**.
- Shared paths with different blobs: **1,102**.
- GitHub-only blob paths: **4,546**.
- GitLab-only blob paths: **3,061**.

These raw counts include intentionally host-specific CI, recovery history and archive material. They are a discovery signal, not a direction to mass-copy.

## Public-page asymmetry

For bilingual `en/**/index.html` and `es/**/index.html` routes:

- GitHub-only public pages: **402**.
- GitLab-only public pages: **90**.
- Shared public routes whose bytes differ: **617**.

High-value GitHub-only clusters include: ONA funded-exit subroutes; Community acta document rooms; Concurso 36/2012 judicial-spine/decision-continuity routes; Cuatrecasas contemporaneous/gap/DP748 routes; DP1901/EG745 cross-institutional routes; Ministerio Fiscal directories; RICPE/CNMV; CaixaBank unitary subroutes; and actor/platform provenance routes.

High-value GitLab-only clusters include: newer Cuatrecasas primary-record/invoices/WIP/Matkator routes; Acosta Matos 2018 offer/liquidation-plan routes; CEXP operation-chain routes; CaixaBank NPL/recovery/overview routes; symposium routes; and newer professional-conduct material.

Shared-but-different high-value routes include the main actor dossiers, actor/party registry, AC/Judge accountability, ONA exit, pre-7-June funded exit, 7-June takeover, Cuatrecasas, PwC, Fiscalía, DP1901/DP1956, RICPE, Meeting Point and recovery-command-centre families.

## Confirmed publication regression and root cause

The public GitLab Pages homepage remained on the compact 25-Sep orientation version after GitLab repository main had been restored. The deeper publication defect was a stale scoped-release manifest that still pinned the compact ~11 KB EN/ES homepage bytes.

The 26-Sep repair now:
1. restores GitLab main EN/ES homepages byte-identically to reviewed GitHub main;
2. restores the actor CSS, reader-priority JS and FMMM/Shaila/Antonio image;
3. restores the live-homepage preservation lock;
4. supersedes the 25-Sep archive-only relocation for the live actor presentation; and
5. pins the restored ~226 KB EN / ~236 KB ES homepages in the actual GitLab Pages scoped-release manifest.

## Omission policy

Do **not** bulk-copy GitHub-only material into GitLab or GitLab-only material into GitHub. Every asymmetry must be classified first as one of:
- canonical omission requiring synchronization;
- legitimate host-specific CI/recovery/governance implementation;
- newer successor not yet mirrored;
- historical/superseded material that must remain non-controlling;
- public-safe page/asset omission;
- private/evidential material not suitable for public projection;
- duplicate/renamed route requiring redirect or provenance mapping;
- unresolved conflict requiring source-level review.

## Priority closure order

P0 — Public first-read continuity: homepage actors/images/main matter; ONA funded exit; 7 June takeover; AC/Judge boundaries; actor registry.

P1 — Canonical evidence and governance omissions: source registers, proceedings controls, counsel/work-product controls, Fiscalía/judicial registers, contrary-evidence and negative-search ledgers.

P2 — High-value public-route asymmetry: determine whether each GitHub-only/GitLab-only page is canonical, superseded, renamed or intentionally host-specific; preserve ES/EN parity.

P3 — Asset/image parity: verify every live page dependency and prevent missing images/CSS/JS from surviving release checks.

P4 — CI/release controls: prevent a stale release manifest, archive relocation or old tested-build pin from silently reverting live public content.

P5 — Full evidence corpus parity: compare evidence/assets by provenance and canonical status, not filename count.

## Non-negotiable controls

- GitHub and GitLab are independent preservation surfaces; neither is assumed complete.
- Public website state is a third surface and must be read back independently after deployment.
- A merge is not proof of publication.
- A public page is not the source of truth.
- No allegation is upgraded merely because a route is restored or mirrored.
- Contrary evidence, open proof and right-of-reply controls travel with any synchronized public proposition.
- No exhaustion certification until all material pagination/version/attachment/route lanes are closed or expressly bounded.
