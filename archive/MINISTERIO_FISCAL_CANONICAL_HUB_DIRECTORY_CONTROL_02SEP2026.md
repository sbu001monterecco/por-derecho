# Ministerio Fiscal canonical hub and directory control — 2 September 2026

## Controlling architecture

The public Ministerio Fiscal layer is organised as one canonical institutional hub with a subordinate office/event directory and links to the existing communications ↔ proceedings graph.

The identity layers must never be collapsed:

1. **Office / route directory identity:** `PD-MF-OFF-####` plus `^` when the office identity is source-locked. This is a Por Derecho directory identity, not an official Ministerio Fiscal reference.
2. **Expediente identity:** the existing Master Register ID (`GC-FIS-*`, `TF-FIS-*`, `LZ-FIS-*`, `NAT-FIS-*`, or a controlled unresolved reference). Existing IDs are never renumbered merely to fit this directory.
3. **Communication / act event:** `PD-SP-EVT-####`. Every source-proved filing, receipt, response, decree, notice, acknowledgement, routing act or transport row has one stable event identity.
4. **External official identifiers:** REGAGE/RedSARA registration, DIR3, NIG, DI, DIP, EG, ST, CC/CA and judicial references remain separate fields and never replace the Por Derecho event/master identity.

## Office/event rendering rule

The office page may allocate an event to a directory office only from the controlled `office` field using a finite normalisation vocabulary. Unmatched events remain visibly unallocated to the directory view while retaining their canonical `PD-SP-EVT-####` identity. No office association may be inferred from subject matter, alleged competence or a related proceeding.

## Proof boundary

A REGAGE/RedSARA receipt proves formal presentation at the stated registration destination and time. It does not by itself prove downstream delivery, internal allocation, joinder, examination, admission, investigation or merits. An official notice or acknowledgement proves only what that act states. A signed decree proves issuance and stated reasoning/outcome, not completeness of the file, correctness, motive or wrongdoing.

## Baseline integrity

The directory validator reconciles against the canonical communication and proceeding datasets. It requires unique `PD-MF-OFF-####` directory identities; every directory expediente Master_ID to exist in the Master Register; globally unique `PD-SP-EVT-####` communication-event identities; exactly the controlled 75 detailed RedSARA baseline receipt events with separate `REGAGE...` and `PD-SP-EVT-####` identities; every located inbound institutional communication row to carry its own event ID; and no universal historical-completeness claim.

## Historical lane

The requested historical audit extends to the beginning of the Ministerio Fiscal/Fiscalía perimeter. The 2011/2012 traceability scope is an audit instruction, not proof that a Fiscalía filing occurred in those years. The earliest direct Fiscalía file presently locked in the Master Register is `GC-FIS-011 — DI 273/2013`. Earlier source-controlled proceedings, denuncias and correspondence are appended only when an individual primary or controlled source establishes the event.

## Explicit gaps preserved

The directory continues to display, rather than hide or silently fill, at least these live gaps: the 22 later aggregate-only RedSARA/AGE records; EG 19/2026 Valencia → Arrecife master reconciliation; OC/2024/0532 / EPPO file bridge; the DP 1901/2026 Fiscal report and later judicial act; receiving-office proof after referrals; and the 2011–2012 historical source lane.

## Public routes

- Spanish hub: `/es/ministerio-fiscal/`
- Spanish offices/events: `/es/ministerio-fiscal/oficinas/`
- English hub: `/en/ministerio-fiscal/`
- English offices/events: `/en/ministerio-fiscal/offices/`
- Existing event/proceeding graph remains at `/es/fiscalia-comunicaciones-procedimientos/` and `/en/public-prosecution-communications-proceedings/`.

The hub is a navigation and control layer. It does not alter the evidential ceilings of the underlying sources.
