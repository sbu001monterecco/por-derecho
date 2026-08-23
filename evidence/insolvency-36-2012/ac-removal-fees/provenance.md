# AC removal, remuneration and judicial-order provenance

Control date: 23 August 2026
Public route: `es/concurso-36-2012-separacion-ac-honorarios/` and English counterpart
Canonical analysis: `archive/AC_SEPARATION_FEES_AUTOS_DP1901_REFERENCE22_UNITARY_DIGEST_23AUG2026.md`

## Primary-source inventory

| Source | Date / extent | Source anchor | Original SHA-256 | Public treatment |
|---|---:|---|---|---|
| Aweswell application to remove the Insolvency Administrator | 23 Apr 2025 · 58 pages | Gmail message `19663da50d6eb73e`, attachment `1. Demanda.pdf` | `5665ec05ae42f18fc64b1209ed7984c39ece015933bdfc9dd8bcf1a8ece6bf26` | Complete structured digest. Raw pleading withheld because it contains unnecessary personal/professional data and annex references. |
| Professional-liability / remuneration claim | 1 Sep 2024 · 21 pages | Gmail message `193a8015d8eee373`, attachment `Demanda Honorarios AC 1SEP2024.pdf` | `6f44c28781f56a46eb5df12b54f33eebd0848a05167eac2dc4f3fe19a5d90430` | Complete structured digest. Raw pleading withheld on data-minimisation grounds. |
| Auto 1377/2025 | 12 Sep 2025 · 3 pages | Gmail message `19952646b51e374b`, attachment `Adjunto1(201).pdf` | `bcb7a0fb242949ca20d2b9ad85a1113d6b84e834bd716cbe90a0bd8ce15f2bfd` | Image-only public copy after irreversible removal of the administrative header, identifiers, unrelated professional/third-party names and verification metadata. |
| Auto resolving reconsideration | 11 Nov 2025 · 4 pages | Gmail message `19a7d06c03e1c731`, attachment `Adjunto1(210).pdf` | `271b72e5c05fbcb46270b945c0489b562454dc135fbd49e38586a4166e628e84` | Same irreversible public-copy process. |
| Criminal complaint concerning the Insolvency Administrator | 18 Jun 2026 · 48 pages | Gmail message `19ed19724709f79b`, attachment `01_Denuncia_Penal_AC_LPB_Sun_Park_FINAL_18JUN2026.pdf` | `5f2925609563caec6c82f4e95fa16abb660f372a34051133fe0f01aa785483f7` | Structured digest only. The raw filing contains identification, address, email and telephone data. Controlled intake materials associate it with handwritten daily intake/reference `22`; that number is not represented as an official proceeding number. |

## Generated public copies

| File | Pages | SHA-256 | Hidden-text / form control |
|---|---:|---|---|
| `auto-1377-2025-removal-public-redacted.pdf` | 3 | `2286dc7ae2321106f82e2ed9aa6ea0a2cfde10b7844111ead766cd5723eac11a` | Image-only; no AcroForm; no JavaScript; no inherited metadata stream; `pdftotext` returns no substantive text layer. |
| `auto-11nov2025-reconsideration-public-redacted.pdf` | 4 | `a2ae1143c2d4dd5c5f8539b58a46eb0af9e6876cadf62f69abfcfabe3ecab8a1` | Image-only; no AcroForm; no JavaScript; no inherited metadata stream; `pdftotext` returns no substantive text layer. |

The builder is `scripts/build_public_ac_orders.py`. It rasterises all pages and reconstructs the PDF, so removed header and verification data do not survive as searchable, form, annotation or metadata content. The substantive judicial pages were visually checked after conversion.

## Publication rule

The public site publishes the two judicial orders in full substantive form, with only the privacy/administrative layer removed. It publishes comprehensive structured summaries—not raw copies—of the party pleadings and the 18 June complaint. A pleading records an allegation and requested relief; it is not proof that the pleaded facts were judicially established.
