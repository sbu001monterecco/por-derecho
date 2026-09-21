# Search methodology and reproducibility

## Corpus searched

- Six accessible top-level archive packages and six nested archives.
- 303 recursively extracted files, totalling 218,438,331 bytes.
- PDF, DOCX, DOC, XLS/XLSX, CSV, JSON, HTML, text and available database/metadata content.
- Exact, accent-insensitive and spelling-variant searches for Laborý, Labory, Labori, CATRUDE, Juan Carlos Cabrera, report/audit terminology, Sun Park, LPB, Community, exploitation, concurso and Arrecife terms.

## Identification threshold

A document is not the target unless authorship or transmission is supported by at least one primary indicator such as:

1. Laborý/CATRUDE letterhead;
2. Juan Carlos Cabrera's verified name or signature;
3. a verified transmitting email;
4. author/creator metadata;
5. an engagement letter, invoice or covering correspondence;
6. a judicial filing expressly attributing the report; or
7. direct confirmation from the firm or another reliable custodian.

## Archive limitation

The 18 unresolved archives are historical Gmail attachments for which only metadata is accessible. They have not been opened internally. A zero result from public filename or text search is not evidence that the report is absent from those ZIPs.

## Privacy boundary

The public register uses aliases. Exact Gmail message IDs, attachment IDs, private email bodies, personal addresses and confidential source packages remain outside the public repository.

## Re-run rule

Whenever an archive is recovered:

1. preserve the original unchanged;
2. calculate SHA-256;
3. extract recursively with path-traversal protection;
4. calculate hashes for all extracted files;
5. deduplicate exact copies and map versions;
6. search text, images where necessary, metadata, letterheads, signatures and embedded objects;
7. update all three registers and the bilingual pages;
8. rerun the deletion-safety audit.
