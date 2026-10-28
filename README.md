# Sun Rock banking briefing — isolated Render deployment

Deployment-only branch. Do not merge this branch into the main public documentary website.

This serves the preserved, password-encrypted bank-facing briefing. The complete bank letter, five-role graphic and two PDF files remain inside the original AES-256-GCM/PBKDF2 encrypted payload. No password, decryption key, personal banking information, counsel email, seller letter or private data-room link is committed or published.

Build: `python3 build.py`; publish only `_site`. The source zip is SHA-256 pinned. The initial import URL is supplied privately to Render and is not required once encrypted-source.zip has been versioned. The deployment includes robots exclusion and a hash-based script Content Security Policy. Shared-password recipients may retain downloaded documents.

Reference: SRLN-2026-WEB-SANTANDER-20261022-001/RENDER-002. Content preparation remains preliminary; publication does not create a bank appointment or capital commitment.


## 28 October 2026 — independently encrypted pre-NDA route

The scoped pre-NDA relationship brief is staged at \`/intro/\` on this **same Render host**.
It presents AWESWELL / Sun Rock's prospective **programme-wide coordinating
and receiving-bank** request for externally sourced capital, with Montaña Roja
as an anchor transaction, not the whole mandate. It separates Santander UK,
European CIB, conditional US coordination, and Santander Alternative
Investments' independently managed capital.

The new reader uses an independently generated passphrase and authenticated
AES-256-GCM ciphertext; neither passphrase nor plaintext is included in
GitHub. It does **not** unlock, replace, embed, or link to the original V5.2
confidential full-pack reader at the root URL. No Santander approval,
financing, onboarding, agency appointment, NDA, delivery or bank receipt
is represented. Initial recipient access and sharing remain owner-controlled.

Canonical scope: SRLN-2026-WEB-SANTANDER-PRENDA-20261028-001/INTRO-V1.
