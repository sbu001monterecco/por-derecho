# Clarification session prompt

Use control `PD-CLAR-GLOBAL-20260923-01` and `assets/data/clarification-registry-v1.json`.

1. Identify the current speaker before recording an answer.
2. Select the highest-priority materially useful OPEN/CONFLICTED clarification.
3. Present one compact A/B/C/D gate; always permit free text.
4. Do not reveal a preferred answer.
5. After the answer, capture the minimum follow-up needed to distinguish firsthand fact, recollection, inference and legal characterisation.
6. Create/update an answer object using `assets/data/clarification-answer-schema-v1.json`.
7. Compare with existing primary/adverse evidence when available.
8. If conflict exists, mark CONFLICTED and create a child clarification rather than overwriting.
9. Feed reconciled results into relevant Truth Machine ledgers and dependency nodes.
10. Periodically offer a short batch session (normally 3–5 high-priority questions), but never force testimony into multiple choice.
11. For Patricia voice-to-text statements, also generate: proposition → interpretation → corroboration → tension/contrary evidence → numerical/date conflict → implications → questions for Miguel → questions for Gil → open proof → canonical formulation.
12. No email, filing, publication or external action is authorised by this prompt.
