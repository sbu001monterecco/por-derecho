# Lender-of-record liability implementation register

**Activated:** 19 August 2026  
**Canonical research path:** `research/lender-of-record-liability/`  
**Public routes:** `/en/lender-of-record/liability/` · `/es/acreedor-de-registro/responsabilidad/`

## Why this register exists

The lender chain cuts across the banking-origin, insolvency-credit, Article 1535, valuation, CAM/HNT, criminal-restoration and damages lanes. This register prevents a later page or pleading from collapsing distinct actors, capacities or remedies.

## Mandatory maintenance cycle

| Trigger | Required update |
|---|---|
| new transfer instrument or schedule | update `data/transfers.json`, credit genealogy, P0 register and public page if public-safe |
| new servicing/authority evidence | update actor, knowledge and conduct records; reassess mandate/Art. 1903 route |
| new judgment/order | add source; mark adverse/favourable/mixed; update appeal/finality and limitation |
| new valuation/account ledger | update instrument genealogy, conduct matrix, causation/damages and double-count control |
| new CAM/HNT corporate document | update succession record and liability allocation |
| new demand/filing | update actor-specific limitation/preservation ledger |
| correction | enter repository correction register and propagate to ES/EN pages |

## Proposition gates

No material proposition is promoted unless it is:

1. actor-specific;
2. capacity-specific;
3. dated from a reliable source;
4. linked to conduct;
5. linked to a proceeding/remedy;
6. causally bounded;
7. contradicted where necessary;
8. public-safe.

## Public publication controls

- no automatic inherited-liability language;
- no group-wide liability from perimeter labels;
- no criminal conclusion;
- no suppression of the 15 February 2018 adverse/mixed order;
- no publication of raw privileged advice, personal contact information or confidential transaction material;
- no use of the €350,000 commissions line as proof of payment, recipient or illegality;
- no Ring 2/3 damages figure without counterfactual evidence and counsel/expert review.

## P0 owner matrix

| Gap | Primary target | Secondary route |
|---|---|---|
| Bankia→SAREB instrument/schedule | native lender/SAREB files | court/AC/adviser copies |
| SAREB→PH122 LSAP/price | notarial/transaction/PH122/SAREB files | DP 1041/2017 and adviser archives |
| Haya servicing/authority | Haya/PH122/Cerberus records | committee, PoA, litigation and employment evidence |
| PH122→CAM full file | notarial/CAM/PH122 files | AC/court/adviser/valuer records |
| CAM→HNT passive schedule | corporate/notarial/registry file | accounts, tax, financing and litigation disclosures |
| end-to-end ledger | native bank/servicer/AC/CAM accounting | expert reconstruction |

## Validation

The repository CI runs:

`python research/lender-of-record-liability/validate.py`

A passing validator confirms structural consistency only. It is not legal validation or proof of any proposition.
