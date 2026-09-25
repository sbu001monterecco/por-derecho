# Actor / PwC shared visualization and mobile control — 19 Aug 2026

Status: mandatory front-end/back-end continuity control

## Purpose
The FMMM / Antonio Cogolludo / Shaila Cogolludo + PwC 2016 knowledge-checkpoint visualization is a single controlled component reused across three public surfaces:
1. bilingual homepage actor cluster;
2. canonical PwC / Carlos Saavedra page;
3. canonical RIC Private Equity / Sun Park page.

The canonical implementation is `assets/homepage-actor-family-pwc-note-20260819.js`. Do not fork the relationship facts or the PwC quotation into independently maintained copies unless there is a compelling technical reason. Page-specific explanatory text may differ, but canonical identities, relationships, chronology labels, quote attribution and evidential boundary must remain synchronized.

## Canonical relationships
- Francisco Mario Matos Matas (FMMM) — husband of Shaila María Cogolludo Ramos.
- Shaila María Cogolludo Ramos — wife of Francisco Mario Matos Matas and daughter of Antonio Cogolludo Rojas.
- Antonio Cogolludo Rojas — father of Shaila María Cogolludo Ramos.
- Laura Patricia Acosta Matos — full name on first public mention; then Laura Acosta Matos / Laura.
- Never use `Tuco` for Antonio Cogolludo Rojas without new primary evidence.

## Canonical chronology labels
- FMMM: 2011 → at least 2022 documented.
- Antonio Cogolludo: 2018 → later documented business-perimeter continuity.
- Shaila Cogolludo: 2017 → later documented business-perimeter continuity.
- José Daniel Acosta Matos: 2017–2018 entry into perimeter → 2022 control → later continuity.
- Laura Patricia Acosta Matos: 2017–2018 legal/insolvency and access role → 2022 CAM representation → later continuity.

## PwC knowledge checkpoint
Dominant quotation: `LA VÍA PENAL CONTRA ESTA GENTE`.

Mandatory boundary: this is a contemporaneous client penal-route instruction and PwC knowledge record. It is not a PwC criminal finding against FMMM, Antonio Cogolludo, Shaila Cogolludo or any other person.

PwC's later confirmed direct contact with the Administrador Concursal may be stated, but the full content of the client criminal allegations must not be imputed to the AC unless proved by a source.

## Surface-specific purpose
### Homepage
Attach the PwC checkpoint visually to the actor cluster so readers see contemporaneous professional notice in the same place as the named Community/control actors.

### PwC page
Surface the shared actor/context visualization immediately after the hero. Purpose: show which historical Community/control perimeter gives context to PwC's 2016 knowledge, prior-client position and later conflict/convergence questions.

### RICPE page
Surface the shared actor/context visualization immediately after the hero. Purpose: show why PwC's asset-specific prior knowledge is relevant to later RICPE audit / legal-fiscal due-diligence / conflict / information-governance questions.

## Mobile acceptance criteria
The shared component must be readable at 320–390 CSS px without horizontal page overflow.
- Homepage actor grid: one column at <=760px; two columns at <=980px.
- Replica actor cards: three desktop, two tablet, one mobile.
- PwC quote/body: two columns desktop, one mobile.
- Use `overflow-wrap:anywhere` for long relationship labels.
- Reduce borders/padding and quote size on narrow mobile screens.
- Links stack naturally and remain tap-sized/readable.

## Backend / cache rule
The shared component is loaded through `assets/ricpe-identity-correction-20260815.js`, itself loaded by the central site loader. When the shared component changes materially, bump its query-string cache version in the loader so deployed browsers do not retain an older homepage-only implementation.

## Verification rule
Repository/main read-back confirms source deployment. External rendered GitHub Pages verification is a separate status and must not be claimed if the environment cannot resolve or fetch the public `github.io` host.
