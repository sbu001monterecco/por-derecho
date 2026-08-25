# Person-perimeter start gate

**Control date:** 25 August 2026  
**Status:** governance approved; person-by-person classification and public-display decisions remain authorization-controlled

Before adding, retaining, reclassifying, anonymising, pseudonymising, withdrawing or publicly displaying a natural person in the Por Derecho identity system, read:

1. `AGENTS.md`;
2. `.github/governance/PERSON_PERIMETER_SEPARATION_AND_PUBLICATION_PROTOCOL.md`;
3. `.github/governance/person-perimeter-classification-policy-v1.json`;
4. `.github/governance/TRANSACTION_DEVELOPMENT_SEPARATION_AND_PUBLICATION_PROTOCOL.md`;
5. the current immutable identity registry and operational-control files.

## Mandatory presentation rule

The public identity architecture must not use one undifferentiated people list. It must present, in visibly separate sections or views:

1. **Our perimeter / Perímetro propio**;
2. **Adverse private parties and documented opposing interests / Partes privadas adversas e intereses opuestos documentados**;
3. **Professionals and representatives / Profesionales y representantes**;
4. **Institutions and officeholders / Instituciones y cargos**; and
5. **Witnesses, experts and document custodians / Testigos, peritos y custodios documentales**.

Transaction-development contacts use `TRANSACTION_DEVELOPMENT_PRIVATE`; unresolved candidates use `UNRESOLVED_PRIVATE_CANDIDATE`. Both remain outside the public legal-matter lists by default.

## Professional completeness gate

Before claiming that the lawyers, firms or procuradores/as list is complete, load:

- `assets/data/legal-professionals-representatives-register-v1.json`;
- `assets/data/legal-professionals-representatives-register-v1.people.json`;
- `assets/data/legal-professionals-representatives-register-v1.organisations.json`; and
- `archive/LEGAL_PROFESSIONALS_REPRESENTATIVES_MASTER_CENSUS_25AUG2026.md`.

`PD-SP-PROF-REG-001` is the controlled completeness layer. It does not itself create an immutable matter ID, profile-page authority, allegation or principal-perimeter assignment. Proposal-only, copied-recipient, administrative and review-candidate records must retain their limits.

## No automatic assignment

Discovery of a name, inclusion in an email, meeting attendance, employment, family relationship, company-group connection, professional representation, chronology or earlier registry inclusion does not by itself authorize placement in either principal perimeter.

Every natural-person assignment and display mode requires a recorded, person-specific decision by Gil Marer. A blank, general or ambiguous instruction means `PRIVATE_ONLY`.

The immutable identity registry remains the neutral identity-resolution layer. Perimeter classification is a separate, dated, capacity-specific overlay and never establishes guilt, liability, knowledge, intent, control or collective responsibility.
