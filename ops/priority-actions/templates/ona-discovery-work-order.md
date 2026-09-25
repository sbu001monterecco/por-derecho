# ONA funded-exit discovery work order

**Task:** `P1-ONA-01`

## Route pair

- English: `/en/pre-7-june-2018-funded-ona-exit/`
- Spanish: `/es/salida-financiada-ona-antes-7-junio-2018/`

## Controlled source

- `research/pre-7-june-2018-funded-ona-exit-source-map.md`
- `research/financing-history-since-2016-wave-map.md`

The public proposition must remain bounded: the record supports multiple signed or active conditional operating, acquisition, bridge, security, due-diligence and court-exit routes by the close of 6 June 2018. It does not establish an unconditional cash drawdown, completed sale or completed judicial exit by that date.

## Preparation checklist

### Current-state refresh

- [ ] Fetch current `main` and record SHA.
- [ ] Confirm both route files exist and inspect their canonical and hreflang tags.
- [ ] Inspect `sitemap.xml` and any generated search/discovery index.
- [ ] Inspect current links from the established ONA pages.
- [ ] Inspect current links from the 7 June and multiple-financial-lives pages.
- [ ] Inspect sent-link and preservation controls before changing routes or fragments.

### Sitemap pair

Add two reciprocal entries with a current `lastmod` and:

- ES alternate;
- EN alternate;
- `x-default` pointing to the controlled default language route.

Do not duplicate an existing route entry.

### Internal gateways

Use one concise bilingual gateway on each of the following relevant route families, unless an equivalent current link already exists:

- `en/ona-hotels-insolvency-exit-36-2012/`
- `es/ona-hotels-salida-concurso-36-2012/`
- `en/sun-park-takeover-7-june-2018/`
- `es/toma-control-sun-park-7-junio-2018/`
- `en/same-hotel-multiple-financial-lives/`
- `es/mismo-hotel-multiples-vidas-financieras/`

The gateway must not:

- add a new large homepage module;
- imply unconditional financing;
- backdate the 12 June or later documents;
- republish private emails or native transaction documents.

### Discovery/index review

- [ ] Identify whether search index data is generated or hand-maintained.
- [ ] Add both routes through the current canonical process rather than creating a parallel index.
- [ ] Preserve bilingual parity and route labels.

## Required checks

Before PR:

- [ ] sitemap is valid XML;
- [ ] each route appears exactly once;
- [ ] reciprocal canonical/hreflang values match;
- [ ] all new internal links resolve in source;
- [ ] repository preservation and sent-link checks pass;
- [ ] audience/reader checks pass on affected pages;
- [ ] no private-source body or locator is introduced.

After merge/deployment:

- [ ] exact merge SHA is identified;
- [ ] both direct routes return HTTP 200;
- [ ] both canonical tags are correct;
- [ ] reciprocal hreflang links are present;
- [ ] each gateway resolves;
- [ ] source/live or settled-DOM parity is recorded;
- [ ] the result is preserved in a publication/verification record.

## Completion statement

Use only:

`ONA_DISCOVERY_COMPLETE` — all checks and live readback passed.

or

`ONA_DISCOVERY_PARTIAL` — state precisely which discovery or deployment check remains open.
