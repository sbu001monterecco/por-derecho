# Anexo 4 RedSARA complete transcript — reconstruction

This directory contains the complete public-safe text transcript of the 154-page source, compressed as bzip2 and encoded as base64 so the full transcript can be preserved in the public repository without repeatedly re-uploading the PDF.

- Original PDF SHA-256: `4636b0da487f9150cd8f229d36f9c44f1bd16c9005f6bfa1415bcbc84595e03f`
- Public-safe uncompressed transcript bytes: `710529`
- Public-safe transcript SHA-256: `18a5d1687234e18d9293a3563d51118ea7b16fb5611adac9b8b428876d875df1`
- bzip2 binary bytes: `72967`
- bzip2 SHA-256: `45ab844382cfa9926863334e6925f7cbb7d8927e76edaaf41b562727b80fa6c7`
- Redacted only in the derivative: NIE, street address, direct email, direct phone number.
- Source-page markers `===== SOURCE PDF PAGE NNN / 154 =====` are embedded in the reconstructed transcript.

## Reconstruct
Concatenate the five files in lexical order, remove line breaks, base64-decode, then bzip2-decompress.

```bash
cat ANEXO4_REDSARA_TRANSCRIPT.bz2.b64.part-*.txt | tr -d '\n' | base64 -d | bzip2 -d > ANEXO4_REDSARA_PUBLIC_SAFE_TRANSCRIPT.txt
sha256sum ANEXO4_REDSARA_PUBLIC_SAFE_TRANSCRIPT.txt
```

Expected SHA-256:
`18a5d1687234e18d9293a3563d51118ea7b16fb5611adac9b8b428876d875df1`

The reconstructed transcript is a derivative. The original PDF / best official source controls where layout, signatures, certification or exact visual presentation matters.
