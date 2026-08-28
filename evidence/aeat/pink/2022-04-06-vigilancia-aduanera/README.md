# AEAT / Vigilancia Aduanera - Sun Park diligence of 6 April 2022

**Evidence ID:** `EVID-AEAT-PINK-VA-20220406-001`

**Source date:** 6 April 2022

**Underlying visit:** 22 March 2022

**Issuing office on the face of the copy:** Agencia Tributaria - Administracion de Aduanas de Lanzarote

**Public status:** five-page official-record copy digitised as a neutral, public-safe derivative; complete substantive text and all four photographs retained; later editorial highlighting, direct contact data, officer NUMA identifiers and handwritten signatures removed

## Controlling evidential reading

The diligence records that two Vigilancia Aduanera officers attended Sun Park on
22 March 2022, following instructions from the Financial and Tax Inspection in
Santa Cruz de Tenerife to obtain information about ownership and operation. It
records the officers' direct observation that the complex was then undergoing
works and closed to the public, four photographs, statements attributed to
people encountered at or contacted through the Acosta Matos business channel,
and a four-entry tourism-registration history said to derive from a Cabildo de
Lanzarote certification.

The document proves that those observations and statements were recorded in an
AEAT diligence. It does **not** by itself prove the truth of every third-party
statement, the identity of the unnamed male corporate interlocutor, the contents
of police reports that are not annexed, the identity of the Booking account, who
received 2017-2018 hotel income, or the complete legal distinction among owner,
operator, creditor, Community and individual shareholder.

## Source and attribution map

| Source inside the diligence | What the document records | Evidential limit |
|---|---|---|
| Vigilancia Aduanera officers | Visit on 22 March 2022; works; public closure; people supervising; photographs | Direct evidence of the observed March 2022 condition only; not direct evidence of 2017-2018 operation |
| Unnamed on-site person | Association with the Acosta Matos business channel; corporate contact route | Person is not named; exact employer, authority and knowledge are not proved |
| Unnamed male corporate interlocutor | Credit purchase, judicial award, additional acquisitions, claimed 2017-2018 Booking activity, alleged complaints and access incidents | The diligence uses masculine references but supplies no name; the statements are neither annexed title evidence nor police/Booking proof |
| Laura Acosta Matos, as described in the source | Request of 24 November 2021 for tourism-history clarification; statements about Gil Marer, Monterecco/Pink, LPB and the 2014 operator change | Her name is express; accuracy, authority, knowledge, purpose and independent corroboration remain separate questions |
| Cabildo history as recited in the diligence | 1991 Sun Park S.A.; 1996 Monte Lanza, S.L.; 2012 Monterecco Sun Park, S.L.; 2014 Owners' Community | The underlying Cabildo certificate is not appended to this five-page diligence and must control when produced |
| Four photographs | Entrance, signage, an interior view and external works | Show the conditions photographed during the 2022 visit; do not establish earlier operation, title, revenue or fault |

## Material controls and contradictions

1. Pink entered the inspection plan in July 2020 and inspection commenced in
   late 2020. The supplementary action was ordered/notified on 4/15 March 2022.
   The located 22 March/6 April contact therefore did not originate the 2020
   inspection and, absent evidence of earlier contact, did not originate the
   already ordered supplementary action. It could still have affected later
   fact attribution or evidential assessment.
2. The source literal describes the prior proprietor as “una empresa llamada
   GIL MARER”. Gil Marer is a natural person, not the name of the company that
   owned the 159 LPB units. The same page later names Luchy Playa Blanca, S.L.U.
   This is a concrete entity/person conflation requiring correction rather than
   silent adoption.
3. The document moves among ownership, exploitation, credit ownership,
   judicial award, Community status and personal/company control. Those are
   legally distinct capacities. The narrative does not itself prove that Pink
   was the comprehensive taxable operator or recipient of all hotel revenue in
   2017-2018.
4. The figures 220 units, 159 awarded units, 49 reportedly acquired units and
   the wider property-title denominator cannot be reconciled without the
   property schedule, deeds and Registry records. Different tourism, physical
   and land-registry denominators must not be collapsed.
5. The claims about Booking, tourist complaints, assault, threats and denied
   access are recorded third-party allegations. No Booking export, reservation
   ledger, complaint, police report, witness statement or judicial outcome is
   annexed.
6. The recited 2014 tourism-registration change is important formal evidence,
   but registration alone does not determine actual 2017-2018 contractual
   authority, services, account control, invoicing or receipt of taxable income.

## Procedural relevance

For the Pink / AEAT dispute, the diligence is material to the provenance and
quality of the 2022 operator narrative. The controlled question is not whether
AEAT was permitted to investigate, but whether later acts correctly separated
entity, function, property/unit, period, contractual authority and revenue, and
whether AEAT independently verified the recorded statements before attributing
taxable activity or culpable conduct.

The precise statement-by-statement use and counterfactual effect remain open
until the complete inspection index, internal reliance record, assessment and
sanction reasoning, Booking/payment data, bank accounts, invoices, PMS records,
police files and underlying Cabildo certification are reconciled.

## Public evidence inventory

| File | Purpose | Pages / status |
|---|---|---|
| `public-pdfs/diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022-public-redacted.pdf` | Neutral raster facsimile | 5 pages; no text layer, annotations, forms or signatures |
| `public-pages/diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022-page1-public.png` | Public page-one preview | Raster; same redactions as public PDF |
| `full-text/diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022-public-transcription.md` | Searchable Spanish transcription | Page-accounted; Spanish source controls |
| `full-text/diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022-english-translation.md` | Complete working English translation | Not a certified legal translation |
| `redaction-log.md` | Public/private and annotation-removal record | All five pages accounted for |

## Source custody and hashes

The received native copy remains outside public Git history. Its private file
name and custody locator are not published. The public derivative is pinned to
the received source by hash and page count.

| Source or derivative | SHA-256 |
|---|---|
| Received native copy | `b6ffc7cf29928a41bac7a466d16e513cc5e2f1c8d8db5069ae86ba64e117bb16` |
| Public redacted PDF | `1698a0800c477b526c3b1f1f5ca8ab55fc07a1248a0cc112fe2d42f175dbf2c9` |
| Public page-one preview | `b321db0392cf9f5bda97bc4f629f018a127c368881a43d26b716be95d5d25843` |

## Reproduction

Run:

```bash
python3 scripts/build_aeat_pink_diligence_public_evidence.py --source /path/to/native-copy.pdf
```

The builder verifies the source hash and five-page count, suppresses 27 later
highlight annotations and their 27 popup objects, rasterises all pages at 140
DPI, burns the limited redactions into the pixels, canonicalises metadata for
byte-stable rebuilds, strips forms/text/metadata exposure and fails if an
annotation, form or hidden text layer remains. The complete transcription and
translation provide the accessible searchable text.
