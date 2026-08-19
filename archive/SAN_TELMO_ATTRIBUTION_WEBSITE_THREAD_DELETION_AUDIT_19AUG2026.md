# Thread deletion audit — San Telmo / RICPE / Sun Park attribution and website correction

**Date:** 19 August 2026  
**Project:** Por Derecho / Project Sun Rock  
**Status at source commit:** MERGE AND PUBLIC-EDGE VERIFICATION REQUIRED BEFORE DELETION

## Material correction

The bilingual homepage interview section had attributed the statement “nosotros en el despacho … metimos unos cuantos clientes” to Enrique Guerra and described Eduardo Sánchez only as interviewer/recipient.

The source-controlled attribution is now locked as follows:

- **Eduardo Sánchez** is the speaker of the client-introduction statement at **08:08–08:12**;
- **“Enrique Guerra, en #UnCaféenSanTelmo”** is the programme title and identifies Guerra as guest;
- the wider project statements by Guerra remain separate from Sánchez’s quotation;
- the video establishes the quotation; the RICPE–Sun Park identification relies on separately cited records;
- the material does not by itself establish client allocation specifically to Sun Park, coordination, transfer or misuse of insolvency information, unlawfulness or liability.

## Website changes preserved

- rendered English and Spanish homepage correction loaded through `assets/site.js`;
- dedicated bilingual correction asset: `assets/san-telmo-attribution-correction-20260819.js`;
- rebuilt English and Spanish San Telmo–RICPE–Sun Park dossier pages;
- proposition-by-proposition evidence ledger;
- explicit clarification that the image’s “same asset” wording means the same hotel complex / connected project perimeter, not one undivided legal asset or the whole LPB insolvency estate;
- preservation of Matkator and third-party perimeter distinctions;
- primary-source timecodes and transcript-page references;
- GitHub Pages canonical and social-sharing metadata;
- dedicated bilingual sitemap and `robots.txt` registration;
- repository regression validation and post-merge public-edge verification;
- right-of-reply and equal-prominence correction route.

## Deliberate implementation choice

The large pre-existing homepages are corrected at render time through the common site loader rather than being rewritten wholesale in this change. This reduces collision risk with concurrent homepage work while ensuring that public readers receive the corrected attribution. The correction asset replaces the complete visible interview section, not merely a footnote.

## Deletion gate

This thread becomes safe to delete only after:

1. the correction PR is merged into current `main`;
2. repository validation passes;
3. public GitHub Pages read-back confirms the site loader, correction asset, both dossier routes, sitemap and robots registration;
4. this audit is updated with the PR number, merge SHA and successful verification run.
