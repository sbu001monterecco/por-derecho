# CALIFICACIÓN VISTA — SPEAKER REGISTER

**Status:** visual/interface identities partly resolved; spoken attribution pending diarisation + aural/context verification.

Diarisation labels and named identities are separate layers. A named person may be shown on screen without being the person speaking at every instant.

| Stable ID | Current identity | Evidence basis | Current status | Prohibited inference |
|---|---|---|---|---|
| `SPEAKER_01` / `WITNESS_DAVID_ESPEJO` | David Espejo Navarro | visible videoconference label in VIDEO_01 opening; sampled VIDEO_02 display; pre-hearing witness material and Drive expert-report family identify David Espejo as perito/expert witness | NAME CANDIDATE STRONGLY SUPPORTED; exact speech boundaries pending | do not assign all audio during his displayed window to him automatically |
| `SPEAKER_02` / `PARTY_GIL` | Gil Marer | visible videoconference label/display state in VIDEO_01, VIDEO_02 and VIDEO_03; party identity controlled by Calificación record | NAME/ROLE SUPPORTED; exact speech boundaries pending | display tile ≠ proof of speaking; no merits proposition yet |
| `SPEAKER_03` / `WITNESS_JONATHAN_SIMO` | Jonathan Simó Morales | visible label near end VIDEO_01 and opening VIDEO_02; pre-hearing witness material; separate 2012/2016 accounting/PwC source family | NAME CANDIDATE STRONGLY SUPPORTED; exact oath/examination boundaries pending | 2016 statements cannot be substituted for 2023 testimony |
| `SPEAKER_JUDGE` | judicial role | courtroom configuration + official proceeding; exact identity controlled elsewhere | ROLE RESERVED; speech attribution pending | court setting alone does not identify each spoken intervention |
| `SPEAKER_FISCAL` | Ministerio Fiscal participant | procedural record establishes Fiscalía participation | ROLE RESERVED; audio/official attendance mapping pending | do not identify by face |
| `SPEAKER_AC` | Administrador Concursal / counsel as applicable | procedural record establishes AC side participation | ROLE RESERVED; exact person/intervention pending | do not merge AC, AC counsel and witnesses |
| `SPEAKER_COUNSEL_LPB` | unresolved | official attendance + audio required | UNRESOLVED | do not infer from seating only |
| `SPEAKER_COUNSEL_GIL` | unresolved | official attendance + audio required | UNRESOLVED | do not infer from seating only |
| `SPEAKER_COUNSEL_PINK` | unresolved | official attendance + audio required | UNRESOLVED | do not infer from seating only |
| `SPEAKER_XX` | neutral diarisation labels to be created by STT | raw diarised output | PENDING | never silently convert `SPEAKER_XX` to a person without evidence |

## Identity-resolution hierarchy

Prefer, in order:

1. explicit introduction/oath/name in the recording;
2. question expressly addressed by name and coherent response;
3. official hearing minute/attendance/witness order;
4. stable videoconference label plus matching documentary role;
5. contextual inference, clearly marked and not promoted to verified identity without confirmation.

Facial recognition is not part of this workflow.
