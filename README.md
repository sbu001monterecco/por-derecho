# Sun Rock banking briefing — isolated Render deployment

Deployment-only branch. Do not merge this branch into the main public documentary website.

This serves the preserved, password-encrypted bank-facing briefing. The complete bank letter, five-role graphic and two PDF files remain inside the original AES-256-GCM/PBKDF2 encrypted payload. No password, decryption key, personal banking information, counsel email, seller letter or private data-room link is committed or published.

Build: `python3 build.py`; publish only `_site`. The source zip is SHA-256 pinned. The initial import URL is supplied privately to Render and is not required once encrypted-source.zip has been versioned. The deployment includes robots exclusion and a hash-based script Content Security Policy. Shared-password recipients may retain downloaded documents.

Reference: SRLN-2026-WEB-SANTANDER-20261022-001/RENDER-002. Content preparation remains preliminary; publication does not create a bank appointment or capital commitment.
