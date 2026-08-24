(() => {
  const current = document.currentScript;
  if (!current) return;

  const load = (filename, onload) => {
    const script = document.createElement('script');
    script.src = new URL(filename, current.src).href;
    script.async = false;
    if (onload) script.addEventListener('load', onload, { once: true });
    document.head.appendChild(script);
  };

  load('justice-map-navigation-20260815.js?v=20260815d', () => {
    load('concursal-accountability-navigation-20260815.js?v=20260815a', () => {
      load('site-accountability-20260814.js?v=20260815a', () => {
        load('accountability-evidence-grammar-20260815.js?v=20260815a', () => {
          load('institutional-accountability-spotlights-20260815.js?v=20260815a', () => {
            load('institutional-accountability-backlog-20260815.js?v=20260815a', () => {
              load('media-accountability-navigation-20260815.js?v=20260815a', () => {
                load('media-followup-pressrelease-fiscal-20260815.js?v=20260815a', () => {
                  load('canarias7-preview-fix-20260815.js?v=20260815a');
                });
              });
            });
          });
        });
        load('ricpe-identity-correction-20260815.js?v=20260824a', () => {
          load('police-evidence-preservation-20260815.js?v=20260815a', () => {
            load('police-regage-drilldown-20260815.js?v=20260815a', () => {
              load('police-context-explainer-20260815.js?v=20260815a', () => {
                load('book-foundation-20260815.js?v=20260815b', () => {
                  load('books-portfolio-20260815.js?v=20260815c');
                  // Book pages now carry the authoritative locked JPG cover in their HTML.
                  // Do not load the legacy SVG router here: it overwrites the correct cover after first paint.
                });
              });
            });
          });
        });
      });
    });
  });

  // Independent media-mark loader: do not make this depend on any other helper chain.
  load('media-publication-marks-20260815.js?v=20260815a');

  // Canary Council of Bar Associations institutional mark and source-controlled status record.
  load('ccca-institutional-mark-20260816.js?v=20260816a');

  // Canonical RICPE routing, chronology, legacy-dossier banner, SNCA boundary and reviewed 17-Aug V6 status.
  load('canonical-routing-chronology-20260815.js?v=20260817b');
  // Post-filing correction: native platform email + contemporaneous signed-PDF provenance supersede the pre-filing status card.
  load('ricpe-filed-status-20260817.js?v=20260817a');

  // Banking-origin, direct-market and extraconcursal-perimeter bridge for the Community dossiers.
  load('origin-direct-market-context-20260816.js?v=20260816b');

  // Current banking-recovery publication routes plus the 2011-2012 default/enforcement evidence boundary.
  load('banking-recovery-publication-20260816.js?v=20260816b');

  // Dedicated Valencia banking-recovery page links across lender-of-record, possession/convergence and PH122→CAM chain pages.
  load('caixabank-valencia-claim-navigation-20260816.js?v=20260816a');

  // Source-controlled CaixaBank→Aweswell adhesion sequence for Borja, propagated to Valencia, lender, AC, Calificación and AP pages.
  load('caixabank-borja-witness-context-20260816.js?v=20260816a');

  // Companies House continuity: UK Monterecco Sun Park Limited renamed Aweswell Limited, same company no. 07716847.
  load('aweswell-monterecco-name-continuity-20260816.js?v=20260816a', () => {
    // Separate Spanish-company continuity: Monterecco Sun Park, S.L. renamed Pink Canary Services, S.L., same NIF B76564517.
    load('pink-canary-monterecco-spanish-continuity-20260816.js?v=20260816a');
  });

  // Controlled direct invitation naming Rosa María Dorta Perdomo as a historical identification lead only.
  load('rosa-dorta-direct-open-letter-20260816.js?v=20260816a');

  // LinkedIn professional-profile capture for Lourdes Castillejo on her ES/EN open-letter pages.
  load('lourdes-linkedin-profile-20260816.js?v=20260816a');

  // Verified 28-Jul-2026 AGE/RedSARA presentation in CGPJ Alzada 286/2026; presentation is not examination or merits.
  load('cgpj-alzada-regage-20260816.js?v=20260816a');

  // Source-complete LPAM–Magistrado appearance-of-impartiality control: contemporaneous 2018/2020 sources,
  // 18-May-2021 court-record limits and timing anomaly, 28-Jul filing, and verified 30-Jul CGPJ General Registry routing.
  load('lpam-magistrado-source-control-20260816.js?v=20260816a');

  // Integrated 2018→2021→2023→CGPJ knowledge chain: formal CNMV/AEAT alerts, 918/2021 RICPE/CAM court filing,
  // LPAM reported-testimony boundary, Gil's stated credibility position, and corrected Alzada chronology.
  load('lpam-cgpj169-calificacion-unitary-20260817.js?v=20260817a');

  // Calificacion: current appellate status and first-person accountability opening, followed by a 90-second
  // professional evidence gateway and the user-approved strong-form Judge Alberto accusation.
  load('calificacion-opening-accountability-20260816.js?v=20260816b', () => {
    load('calificacion-professional-read-20260816.js?v=20260816a');
    load('judge-alberto-approved-accusation-20260816.js?v=20260816a');
    load('calificacion-report-radical-transparency-20260816.js?v=20260816a', () => {
      load('calificacion-allegation01-collaboration-audit-20260816.js?v=20260816a', () => {
        load('calificacion-allegation02-thirdparty-credits-audit-20260816.js?v=20260816a', () => {
          load('calificacion-allegation03-pink-rent-operating-audit-20260816.js?v=20260816a', () => {
            load('calificacion-allegation03-unitary-community-ac-causation-20260816.js?v=20260816a', () => {
              load('calificacion-allegation04-accounting-audit-20260816.js?v=20260816a', () => {
                load('calificacion-allegation04-cls-bdo-correction-20260816.js?v=20260816a', () => {
                  load('calificacion-3032010-fabrication-allegation-20260816.js?v=20260816a', () => {
                    load('calificacion-judicial-adoption-private-actor-bridge-20260816.js?v=20260816a', () => {
                      load('calificacion-fiscal-eg49-response-20260816.js?v=20260816a');
                    });
                  });
                });
              });
            });
          });
        });
      });
    });
  });

  // Community dossier cross-link into the non-fragmented Allegation-03 causation analysis.
  load('calificacion-a03-community-bridge-20260816.js?v=20260816a');

  // Calificacion: 2018 recognised secured-credit holder plus de facto material-control threshold;
  // separates creditor status, physical control, later adjudication and pre/post-control causation.
  // Loaded after the AC crosswalk so its insertion after that module becomes the causal baseline before serial allegation audits.
  load('calificacion-2018-creditor-material-control-20260816.js?v=20260816a');

  // Cross-cutting first-person allegation: alleged forcible/clandestine extraconcursal control, AC authority overreach,
  // Fiscal circularity and later judicial legitimisation. Appears only on relevant Calificación/takeover/AC/Judge/Fiscal/DP1901/accountability routes.
  load('extraconcursal-force-authority-laundering-20260816.js?v=20260816a');

  // Source-completion addendum: 25-Jun-2018 counsel report that the opposing side relied on Borja's security email;
  // preserves the contrary AC account and the unproved literal key-handover boundary.
  load('extraconcursal-borja-security-source-upgrade-20260816.js?v=20260816a');

  // Calificacion/recovery: documented positive-agency chronology and reciprocal recovery-through-adversity bridge.
  load('calificacion-recovery-through-adversity-20260816.js?v=20260816a');

  // Calificacion/recovery: unitary commercial normalisation / refinancing / hotel-operation / exit counter-record.
  // Preserves ONA↔Clubotel entity separation, VSO conditionality and the actor-specific causation boundary.
  load('calificacion-documentary-counter-record-20260816.js?v=20260817a');

  // Calificacion: surface the verified 2017 court-record rescue filing and the 2018 reported direct judicial notice on the ES/EN landing pages and detail routes.
  load('calificacion-prior-judicial-knowledge-20260816.js?v=20260816b');

  // Calificacion: supersede stale static wording that still described the now-complete 47-page AC report as outstanding.
  load('calificacion-source-status-correction-20260816.js?v=20260816a');

  // Calificacion: canonical person-specific AC → Fiscalía → judgment → appeal map.
  load('calificacion-canonical-allegations-outcomes-20260817.js?v=20260817a');

  // Cross-cutting documentary bridge: pre-concurso minority litigation, 2019 DI248/unitary-liquidation record,
  // and the Jan-Feb-2026 Fiscalía complaint family. Complaints remain allegations; reproduced Plan language is source-qualified.
  load('calificacion-fiscal-2012-2019-2026-bridge-20260816.js?v=20260816b', () => {
    // Primary-source closure layer: original AC Plan, signed 24-Oct-2019 non-convalidation Auto,
    // signed Tenerife Diligencias 20/2026 decree and signed Valencia EG 19/2026 inhibition.
    load('calificacion-primary-source-closures-20260816.js?v=20260816a');
  });

  // Calificación × elEconomista: collateral use, scope mismatch, provenance alternatives and finite sender/header evidence requests.
  load('calificacion-eleconomista-collateral-use-20260816.js?v=20260816a');

  // Cross-site unitary allegation: the same Sun Park/MYND hotel, assets, works, value and employment
  // across Concurso, Comunidad, RICPE/RIC, HNT, GC/836/P06, FEDER and current operation.
  // States the allegation strongly while preserving its status as a substantiated allegation rather than an adjudicated finding.
  load('same-asset-multiple-financial-lives-20260816.js?v=20260816a');

  // Cross-site accountability layer: repeated CAM-favourable direction of effect across retracto, control,
  // liquidation/adjudication and later continuity. Separates repeated effects, possible duty breach and
  // higher-threshold influence/conspiracy hypotheses rather than converting optics into criminal findings.
  load('cam-favourable-pattern-20260819.js?v=20260819a');

  // ONA exit pages: unitary actor/property/exploitation map. Preserves LPB as principal property owner rather than whole hotel,
  // Clubotel/ONA Hotels as operating anchor, Daniel Irigoyen's legal-coordinator role and Cuatrecasas' broader transaction work.
  load('ona-unitary-actor-map-20260817.js?v=20260817a');

  // Calificación landing pages: stable guided reader journey, serial navigation, evidence-before-actor matrix,
  // progressive disclosure of connected dossiers, correction/right-of-reply controls and deterministic final ordering.
  // The module waits for the earlier dynamic sections to settle before applying the bilingual composition.
  load('calificacion-reader-experience-20260817.js?v=20260817a', () => {
    load('calificacion-reader-experience-finish-20260817.js?v=20260817a');
  });

  // 7 June 2018: bilingual convergence-hub reader architecture plus a high homepage hinge module.
  // This is a presentation layer over the controlled dossier; it does not create new primary findings.
  load('sun-park-7june-convergence-20260817.js?v=20260817a');

  // 2008→2022 Community/CEXP ACTA authority provenance: Alimarket baseline, entity corrections,
  // disputed 22-Jun-2011 provenance node, source-safe 2016/2018 primary findings and downstream context bridges.
  load('community-actas-authority-provenance-20260817.js?v=20260817b');

  // Public-authority / independent-review unitary case reconstruction gateway.
  // Reuses source-controlled canonical propositions while keeping clean-room and criminal-forensic boundaries explicit.
  load('public-authority-case-reconstruction-20260817.js?v=20260817a');

  // Flagship/test case: JV 1260/2011 → AP Las Palmas 89/2014. Gives the pre-concurso operator litigation
  // a high-visibility Spotlight while keeping the procedural-fraud theory explicitly non-adjudicated.
  load('flagship-case-1260-2011-20260817.js?v=20260817a');

  // Canonical sharing/deep-link capability. Book pages retain their established markup and load this through
  // the legacy compatibility bridge; other substantive ES/EN pages receive the compact page-share control.
  if (!document.querySelector('script[src*="book-page-share-20260815.js"]')) {
    load('share-controls-20260817.js?v=20260817a');
  }
})();
