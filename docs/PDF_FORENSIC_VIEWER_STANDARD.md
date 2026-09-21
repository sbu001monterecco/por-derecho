# Por Derecho Canonical PDF + Forensic Sidecar Standard

## Purpose

Use one reusable public reader whenever a Por Derecho page needs to let a visitor inspect a PDF **and** understand source-controlled commentary beside it.

The reference implementation is the RPL 3304/2025 AC-opposition page released in PR #1732. The private/local `tools/forensic-reader` remains the deeper working environment; this standard governs the reviewed public projection.

## Architecture

### 1. Source custody

Keep two concepts separate:

- **native source** — exact received/signed binary, immutable and hash-controlled;
- **public viewer binary** — either that same binary when disclosure review permits, or a reviewed visually equivalent public-safe derivative.

Never alter the native binary merely to make the website viewer easier.

Each public record should state:
- document ID/title/date;
- native SHA-256;
- public binary SHA-256;
- page count;
- relationship between native and public binary;
- any redactions/flattening/removal and why.

### 2. Viewer shell

Default public viewer is zero-network and static-host compatible:

- embedded PDF at left;
- page controls;
- open-in-new-tab fallback;
- sticky forensic sidecar at right on desktop;
- stacked responsive layout on mobile.

Shared assets:
- `assets/pdf-forensic-viewer.css`
- `assets/pdf-forensic-viewer.js`

The page root uses:

```html
<section
  data-pd-pdf-forensic-viewer
  data-case-global="MY_CASE_GLOBAL"
  data-lang="es">
  ...
</section>
```

The case-specific data object supplies the PDF URL, pages, categories and notes.

### 3. Sidecar data

Minimum case object:

```js
window.MY_CASE_GLOBAL = {
  version: "1.0.0",
  documentId: "DOC-ID",
  pages: 22,
  pdf: "/por-derecho/evidence/.../document.pdf",
  categories: {
    CONTEXT: { color:"#c18119", es:"Contexto", en:"Context" }
  },
  notes: [{
    id:"stable-note-id",
    page:3,
    category:"CONTEXT",
    status:"PARTIAL",
    title:{es:"...",en:"..."},
    quote:{es:"...",en:"..."},
    commentary:{es:"...",en:"..."},
    boundary:{es:"...",en:"..."},
    links:[{es:"...",en:"...",hrefEs:"/por-derecho/es/...",hrefEn:"/por-derecho/en/..."}]
  }]
};
```

Stable annotation IDs make direct links such as `#note-stable-note-id` possible.

### 4. Evidential semantics

Colours are review categories, not a truth score.

Recommended categories:
- `RHETORIC`
- `CONTEXT`
- `NOTICE`
- `VERIFY`
- `NARROWING`
- `SUPPORTED`

Rules:
- NARROWING/CONTRADICTED does not by itself establish lying or intent.
- NOTICE requires evidence of receipt/knowledge, not merely source existence.
- Preserve lawful/contrary explanations on the same record.
- Preserve open proof explicitly.
- Do not publish private working annotations simply because the public viewer can display them.

### 5. Interconnectivity

Every commentary node may link to:
- the precise proceeding page;
- actor dossier;
- chronology/event;
- source room;
- valuation/accounting analysis;
- related document reader;
- correction/right-of-reply route.

The sidecar is therefore part of the site evidence graph, not an isolated annotation panel.

### 6. Public/private workflow

`native source → hash/custody → extraction/review → private forensic case → disclosure review → public-safe binary → curated sidecar → bilingual reader → CI/browser checks → Pages deployment → live byte readback`

The private `pd.forensic.v1` case can be much richer than the public sidecar. Public projection must be separately reviewed.

## Rendering tiers

### Tier A — default / current standard

Browser-native PDF iframe plus shared sidecar.

Advantages:
- zero external network;
- no third-party runtime;
- works on GitHub Pages;
- preserves the PDF as the central document;
- page-linked navigation, search, filters, visual category summary and deep links.

Limitation:
- browser PDF plugins do not expose internal scroll/word geometry to page JavaScript, so automatic scroll synchronization and rectangle/word overlays are not reliable.

### Tier B — precise forensic rendering

For documents requiring automatic page-scroll synchronization, text/rectangle highlights or clickable coordinates, use a **locally vendored** PDF.js build, not an external CDN.

Tier B must:
- be stored inside the repository;
- make no external network requests;
- keep the same sidecar schema and source hashes;
- fall back to Tier A/open-original when PDF.js cannot render;
- preserve accessibility and mobile behavior;
- pass dependency/license and browser acceptance before deployment.

No PDF.js bundle was present in the repository at the 22 Sep 2026 audit, so Tier B is an explicit future enhancement, not something to fake with screenshots.

## Acceptance contract for every new public PDF

A new public PDF page is not complete until it has:
1. native/public hash relationship;
2. page count and extraction/OCR status;
3. disclosure/redaction decision;
4. embedded bilingual viewer or justified single-language exception;
5. what the document is;
6. what it establishes;
7. what it does not establish;
8. page-linked commentary where analysis is material;
9. reciprocal evidence-graph links;
10. deterministic route/link/privacy checks;
11. desktop/mobile browser rendering;
12. post-merge Pages/live readback.

This incorporates the stronger parts of the Fiscalía PDF-room contract (#1621), the RICPE multi-route viewer work (#1479), JSP evidence-reader work (#1477), the historical Puzzle hybrid viewer branch, and the deployed R33 split forensic viewer (#1732).

## Non-regression rule

Do not replace existing native/public binaries, URLs or source provenance merely to migrate a page to this standard. Add the shared viewer around the already-controlled source, and preserve old links.

