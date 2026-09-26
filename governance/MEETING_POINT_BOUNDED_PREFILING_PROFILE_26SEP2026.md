# Meeting Point — bounded prefiling validation profile

Control date: 26 September 2026. Public-safe implementation/method only. No court PDFs, private manifests, private emails or confidential source attachments are published here.

This control succeeds the implementation state described in `docs/meeting-point-prefiling-v11-v5-public-control-20260925.md`, which remains preserved as history. It does not replace the substantive safeguards in `governance/MEETING_POINT_PREFILING_ADVERSE_ADMISSION_CONTROL_24SEP2026.md`.

## Explicit version selection, not deletion of safeguards

The original two-text-file invocation keeps the legacy markers. A deliberately bounded successor uses `--profile bounded-v13-v7 --manifest PRIVATE.json` with the exact two private PDFs. Its manifest is held outside public Git. It checks document/source hashes, byte counts, page counts, front version pairing, source-to-output page bindings, the closed PUZZLE selection and pixel identity of the reproduced PUZZLE source regions. Deliberately excluded collateral cannot be reintroduced without a separately reviewed successor profile.

Passing these technical checks does not establish source authenticity, legal sufficiency, standing, criminal intent, truth of each historical allegation, signature readiness, remote CI, submission or receipt. Shared images do not alone prove common knowledge, legal authority, completed economic execution or continuity of contract. Capture date, document date and first-publication date remain distinct; source qualifications and contrary evidence remain material.

## Regression run

`python3 -m unittest discover -s tests -p test_meeting_point_prefiling_controls.py -v`

The fixtures are synthetic and contain no private exhibits. The exact private-PDF invocation requires PyMuPDF; the ordinary regression suite and legacy text invocation use the Python standard library. The success label is `MACHINE_CONTROLS_PASS_HUMAN_REVIEW_REQUIRED`.

The new scoped workflow performs these synthetic tests only. It does not upload a private package as a CI artifact, publish a website, merge a branch or certify a court filing. Existing unrelated workflows are unchanged.
