#!/usr/bin/env node

import fs from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { SpreadsheetFile, Workbook } = require("@oai/artifact-tool");
const JSZip = require("jszip");

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(scriptDir, "..");
const dataPath = path.join(
  repoRoot,
  "assets/data/concurso36-decision-continuity-2014-2026-v1.json",
);
const outputPath = path.join(
  repoRoot,
  "assets/data/concurso36-decision-continuity-2014-2026-v1.xlsx",
);
const previewDir = process.env.C36_DECISION_CONTINUITY_PREVIEW_DIR || "";

const payload = JSON.parse(await fs.readFile(dataPath, "utf8"));
const rows = payload.rows;
const expected = {
  audited_rows: 51,
  core_primary_decisions_controlled: 28,
  earlier_in_case_anchor_decisions_controlled: 4,
  connected_or_contextual_primary_decisions_controlled: 2,
  controlled_court_office_acts: 2,
  unresolved_or_partial_family_rows: 15,
};
const classificationLabels = {
  core_primary_decision_controlled: {
    es: "Decisión central primaria controlada",
    en: "Core primary decision controlled",
  },
  earlier_in_case_anchor_decision_controlled: {
    es: "Ancla interna anterior controlada",
    en: "Earlier in-case anchor controlled",
  },
  connected_or_contextual_primary_decision_controlled: {
    es: "Decisión conexa o contextual controlada",
    en: "Connected or contextual decision controlled",
  },
  controlled_court_office_act: {
    es: "Acto de oficina judicial controlado",
    en: "Court-office act controlled",
  },
  unresolved_or_partial_family: {
    es: "Familia abierta o parcial",
    en: "Open or partial family",
  },
};

function requireCondition(condition, message) {
  if (!condition) throw new Error(message);
}

async function ensureFrozenPanes(xlsxPath) {
  const zip = await JSZip.loadAsync(await fs.readFile(xlsxPath));
  const paneMarkup = [
    '<x:pane xSplit="2" ySplit="3" topLeftCell="C4" activePane="bottomRight" state="frozen" />',
    '<x:selection pane="topRight" activeCell="C1" sqref="C1" />',
    '<x:selection pane="bottomLeft" activeCell="A4" sqref="A4" />',
    '<x:selection pane="bottomRight" activeCell="C4" sqref="C4" />',
  ].join("");

  for (let index = 1; index <= 3; index += 1) {
    const member = `xl/worksheets/sheet${index}.xml`;
    const entry = zip.file(member);
    requireCondition(entry, `Missing ${member} while applying freeze panes`);
    let xml = await entry.async("string");
    if (!xml.includes("<x:pane ")) {
      const selfClosingView = /<x:sheetView([^>]*)\s\/>/;
      requireCondition(selfClosingView.test(xml), `${member} has an unsupported sheetView shape`);
      xml = xml.replace(selfClosingView, `<x:sheetView$1>${paneMarkup}</x:sheetView>`);
      zip.file(member, xml);
    }
  }

  const patched = await zip.generateAsync({
    type: "nodebuffer",
    compression: "DEFLATE",
    compressionOptions: { level: 9 },
  });
  await fs.writeFile(xlsxPath, patched);
}

for (const [key, value] of Object.entries(expected)) {
  requireCondition(
    payload.result?.[key] === value,
    `JSON result ${key}=${payload.result?.[key]} (expected ${value})`,
  );
}
requireCondition(Array.isArray(rows) && rows.length === expected.audited_rows, "Expected 51 decision rows");

const stableIds = rows.map((row) => row.id);
requireCondition(new Set(stableIds).size === stableIds.length, "Decision row IDs must be unique");

const chronologyKeys = rows.map(
  (row) => `${row.sort_date}\u0000${String(row.same_date_sequence).padStart(4, "0")}`,
);
requireCondition(
  chronologyKeys.every((key, index) => index === 0 || chronologyKeys[index - 1] <= key),
  "Rows must be ordered by sort_date and same_date_sequence",
);

const classificationCounts = Object.fromEntries(
  Object.keys(classificationLabels).map((key) => [key, 0]),
);
for (const row of rows) {
  requireCondition(/^\d{4}-\d{2}-\d{2}$/.test(row.sort_date), `${row.id} lacks an ISO sort_date`);
  requireCondition(Number.isInteger(row.same_date_sequence), `${row.id} lacks an integer same_date_sequence`);
  requireCondition(payload.status_labels[row.coverage_state], `${row.id} has an unknown coverage state`);
  requireCondition(classificationLabels[row.classification], `${row.id} has an unknown classification`);
  classificationCounts[row.classification] += 1;
}

const expectedByClassification = {
  core_primary_decision_controlled: expected.core_primary_decisions_controlled,
  earlier_in_case_anchor_decision_controlled: expected.earlier_in_case_anchor_decisions_controlled,
  connected_or_contextual_primary_decision_controlled:
    expected.connected_or_contextual_primary_decisions_controlled,
  controlled_court_office_act: expected.controlled_court_office_acts,
  unresolved_or_partial_family: expected.unresolved_or_partial_family_rows,
};
for (const [classification, value] of Object.entries(expectedByClassification)) {
  requireCondition(
    classificationCounts[classification] === value,
    `${classification}=${classificationCounts[classification]} (expected ${value})`,
  );
}

const siteRoot = new URL("https://sbu001monterecco.github.io/por-derecho/");
const publicPageEs = new URL("es/concurso-36-2012-autos-resoluciones/", siteRoot);
const publicPageEn = new URL("en/insolvency-36-2012-orders-decisions/", siteRoot);

function publicUrl(row, language) {
  const page = language === "es" ? publicPageEs : publicPageEn;
  const href = language === "es" ? row.public_href_es : row.public_href_en;
  if (row.public_anchor) return new URL(`#${row.public_anchor}`, page).href;
  if (href) return new URL(href, page).href;
  return new URL(language === "es" ? "#continuidad-2014-2026" : "#continuity-2014-2026", page).href;
}

const workbook = Workbook.create();
const summary = workbook.worksheets.add("Summary");
const families = workbook.worksheets.add("Decision families");
const legend = workbook.worksheets.add("Status legend");

for (const sheet of [summary, families, legend]) {
  sheet.showGridLines = false;
  sheet.freezePanes.freezeRows(3);
  sheet.freezePanes.freezeColumns(2);
}

const familyHeaderRow = 3;
const familyDataStartRow = familyHeaderRow + 1;
const familyDataEndRow = familyHeaderRow + rows.length;
const familyHeaders = [
  "Sort date (ISO)",
  "Same-date seq",
  "Period / periodo",
  "Stable ID",
  "Family (ES)",
  "Family (EN)",
  "Proceeding / lane (ES)",
  "Proceeding / lane (EN)",
  "Coverage state",
  "Status (ES)",
  "Status (EN)",
  "Classification code",
  "Classification (ES)",
  "Classification (EN)",
  "Row type",
  "Date status",
  "Canonical record IDs",
  "Priority",
  "Copy control",
  "Public access",
  "Remaining gap (ES)",
  "Remaining gap (EN)",
  "Public ES",
  "Public EN",
];

families.getRange("A1:X1").merge();
families.getRange("A1").values = [["Concurso 36/2012 — 2014–2026 decision-family continuity"]];
families.getRange("A2:X2").merge();
families.getRange("A2").values = [[
  "51 public-safe control rows · sort by ISO date then sequence · same-date instruments remain separate · no private locators",
]];
families.getRange("A3:X3").values = [familyHeaders];

const familyValues = rows.map((row) => {
  const status = payload.status_labels[row.coverage_state];
  const classification = classificationLabels[row.classification];
  return [
    row.sort_date,
    row.same_date_sequence,
    row.period,
    row.id,
    row.family_es,
    row.family_en,
    row.proceeding_es ?? row.proceeding ?? "",
    row.proceeding_en ?? row.proceeding ?? "",
    row.coverage_state,
    status.es,
    status.en,
    row.classification,
    classification.es,
    classification.en,
    row.row_type,
    row.date_status,
    row.canonical_record_ids.join("; "),
    row.priority,
    row.copy_control_status ?? "",
    row.public_access_status,
    row.gap_es,
    row.gap_en,
    publicUrl(row, "es"),
    publicUrl(row, "en"),
  ];
});
families.getRange(`A${familyDataStartRow}:X${familyDataEndRow}`).values = familyValues;

const familyTable = families.tables.add(
  `A${familyHeaderRow}:X${familyDataEndRow}`,
  true,
  "DecisionContinuityTable",
);
familyTable.style = "TableStyleMedium2";
familyTable.showBandedRows = true;
familyTable.showFilterButton = true;

summary.getRange("A1:J1").merge();
summary.getRange("A1").values = [["Concurso 36/2012 — Decision continuity audit, 2014–2026"]];
summary.getRange("A2:J2").merge();
summary.getRange("A2").values = [[
  `Public-safe coverage matrix · control date ${payload.control_date} · certified docket denominator not obtained`,
]];

summary.getRange("A4:D4").values = [["Metric", "Calculated", "JSON", "Variance"]];
summary.getRange("A5:A10").values = [
  ["Audited control rows"],
  ["Core primary decisions controlled"],
  ["Earlier in-case anchors controlled"],
  ["Connected/contextual primary controls"],
  ["Controlled court-office acts"],
  ["Unresolved or partial family rows"],
];
summary.getRange("B5").formulas = [[`=COUNTA('Decision families'!$D$${familyDataStartRow}:$D$${familyDataEndRow})`]];
summary.getRange("B6").formulas = [[`=COUNTIF('Decision families'!$L$${familyDataStartRow}:$L$${familyDataEndRow},"core_primary_decision_controlled")`]];
summary.getRange("B7").formulas = [[`=COUNTIF('Decision families'!$L$${familyDataStartRow}:$L$${familyDataEndRow},"earlier_in_case_anchor_decision_controlled")`]];
summary.getRange("B8").formulas = [[`=COUNTIF('Decision families'!$L$${familyDataStartRow}:$L$${familyDataEndRow},"connected_or_contextual_primary_decision_controlled")`]];
summary.getRange("B9").formulas = [[`=COUNTIF('Decision families'!$L$${familyDataStartRow}:$L$${familyDataEndRow},"controlled_court_office_act")`]];
summary.getRange("B10").formulas = [[`=COUNTIF('Decision families'!$L$${familyDataStartRow}:$L$${familyDataEndRow},"unresolved_or_partial_family")`]];
summary.getRange("C5:C10").values = [
  [expected.audited_rows],
  [expected.core_primary_decisions_controlled],
  [expected.earlier_in_case_anchor_decisions_controlled],
  [expected.connected_or_contextual_primary_decisions_controlled],
  [expected.controlled_court_office_acts],
  [expected.unresolved_or_partial_family_rows],
];
summary.getRange("D5").formulas = [["=B5-C5"]];
summary.getRange("D5:D10").fillDown();

summary.getRange("A11").values = [["Partition total"]];
summary.getRange("B11").formulas = [["=SUM(B6:B10)"]];
summary.getRange("C11").formulas = [["=C5"]];
summary.getRange("D11").formulas = [["=B11-C11"]];

summary.getRange("F4:J4").merge();
summary.getRange("F4").values = [["Controlling conclusion / conclusión rectora"]];
summary.getRange("F5:J7").merge();
summary.getRange("F5").values = [[payload.result.status]];
summary.getRange("F8:J11").merge();
summary.getRange("F8").values = [[
  "A located copy closes only its copy node. Filing, opposition, service, review, appeal, finality and implementation/accounting remain separate.",
]];

summary.getRange("A13:J13").merge();
summary.getRange("A13").values = [["Scope / Alcance"]];
summary.getRange("A14:E16").merge();
summary.getRange("A14").values = [[payload.scope.included_es]];
summary.getRange("F14:J16").merge();
summary.getRange("F14").values = [[payload.scope.included_en]];
summary.getRange("A17:E19").merge();
summary.getRange("A17").values = [[payload.scope.excluded_es]];
summary.getRange("F17:J19").merge();
summary.getRange("F17").values = [[payload.scope.excluded_en]];
summary.getRange("A21:E21").merge();
summary.getRange("F21:J21").merge();
summary.getRange("A21").values = [[new URL("#continuidad-2014-2026", publicPageEs).href]];
summary.getRange("F21").values = [[new URL("#continuity-2014-2026", publicPageEn).href]];

const summaryTable = summary.tables.add("A4:D11", true, "DecisionContinuitySummaryTable");
summaryTable.style = "TableStyleMedium2";
summaryTable.showBandedRows = false;
summaryTable.showFilterButton = true;

const statusEntries = Object.entries(payload.status_labels);
const statusStartRow = 4;
const statusEndRow = statusStartRow + statusEntries.length - 1;
legend.getRange("A1:H1").merge();
legend.getRange("A1").values = [["Status legend / Leyenda de estados"]];
legend.getRange("A2:H2").merge();
legend.getRange("A2").values = [[
  "Bilingual labels are sourced directly from the public-safe JSON; counts are formula-driven from Decision families.",
]];
legend.getRange("A3:G3").values = [[
  "Coverage state", "Label (ES)", "Label (EN)", "Count", "Share", "Meaning (ES)", "Meaning (EN)",
]];

const statusMeaning = {
  PRIMARY_COPY_CONTROLLED: [
    "La copia primaria de la resolución está controlada; la familia procesal puede seguir abierta.",
    "The primary decision copy is controlled; its wider procedural family may remain open.",
  ],
  CONTEXTUAL_PRIMARY_COPY_CONTROLLED: [
    "Copia primaria controlada de una vía separada, conservada sólo como contexto.",
    "Controlled primary copy from a separate lane, retained only as context.",
  ],
  COURT_OFFICE_COPY_CONTROLLED_FAMILY_INCOMPLETE: [
    "Copia del acto de oficina judicial controlada; escritos, testimonios, notificación o uso siguen abiertos.",
    "Court-office act copy controlled; filings, testimonies, service or later use remain open.",
  ],
  REFERENCED_PRIMARY_FAMILY_INCOMPLETE: [
    "La existencia o identidad está referenciada, pero falta la copia primaria o parte esencial de la familia.",
    "Existence or identity is referenced, but the primary copy or an essential family component is missing.",
  ],
  UNCONFIRMED_SECONDARY_REFERENCE: [
    "Referencia secundaria sin copia oficial suficiente para afirmar fecha, identidad o resultado.",
    "Secondary reference without an official copy sufficient to establish date, identity or outcome.",
  ],
  SECONDARY_REFERENCE_CONFLICT: [
    "Referencias secundarias incompatibles que requieren reconciliación con la fuente primaria.",
    "Conflicting secondary references requiring reconciliation against the primary source.",
  ],
  IDENTITY_AND_OUTCOME_UNRESOLVED: [
    "La identidad exacta del acto y su resultado todavía no están resueltos.",
    "The act's exact identity and outcome remain unresolved.",
  ],
  PARTIAL_SOURCE_CHAIN: [
    "Sólo se controla parte de la cadena fuente y procesal.",
    "Only part of the source and procedural chain is controlled.",
  ],
  OPEN_FINAL_CHAIN: [
    "La rendición final, decisión, firmeza o conclusión siguen abiertas.",
    "Final accounts, decision, finality or conclusion remain open.",
  ],
};

legend.getRange(`A${statusStartRow}:G${statusEndRow}`).values = statusEntries.map(([state, labels]) => [
  state,
  labels.es,
  labels.en,
  null,
  null,
  statusMeaning[state][0],
  statusMeaning[state][1],
]);
legend.getRange(`D${statusStartRow}`).formulas = [[
  `=COUNTIF('Decision families'!$I$${familyDataStartRow}:$I$${familyDataEndRow},A${statusStartRow})`,
]];
legend.getRange(`D${statusStartRow}:D${statusEndRow}`).fillDown();
legend.getRange(`E${statusStartRow}`).formulas = [[`=D${statusStartRow}/${expected.audited_rows}`]];
legend.getRange(`E${statusStartRow}:E${statusEndRow}`).fillDown();
const statusTable = legend.tables.add(`A3:G${statusEndRow}`, true, "DecisionStatusLegendTable");
statusTable.style = "TableStyleMedium2";
statusTable.showBandedRows = true;
statusTable.showFilterButton = true;

const classificationTitleRow = statusEndRow + 3;
const classificationHeaderRow = classificationTitleRow + 1;
const classificationStartRow = classificationHeaderRow + 1;
const classificationEntries = Object.entries(classificationLabels);
const classificationEndRow = classificationStartRow + classificationEntries.length - 1;
legend.getRange(`A${classificationTitleRow}:G${classificationTitleRow}`).merge();
legend.getRange(`A${classificationTitleRow}`).values = [["Classification partition / Partición de clasificación"]];
legend.getRange(`A${classificationHeaderRow}:E${classificationHeaderRow}`).values = [[
  "Classification code", "Label (ES)", "Label (EN)", "Calculated", "JSON declared",
]];
legend.getRange(`A${classificationStartRow}:E${classificationEndRow}`).values = classificationEntries.map(
  ([code, labels]) => [code, labels.es, labels.en, null, expectedByClassification[code]],
);
legend.getRange(`D${classificationStartRow}`).formulas = [[
  `=COUNTIF('Decision families'!$L$${familyDataStartRow}:$L$${familyDataEndRow},A${classificationStartRow})`,
]];
legend.getRange(`D${classificationStartRow}:D${classificationEndRow}`).fillDown();
const classificationTable = legend.tables.add(
  `A${classificationHeaderRow}:E${classificationEndRow}`,
  true,
  "DecisionClassificationLegendTable",
);
classificationTable.style = "TableStyleMedium2";
classificationTable.showBandedRows = true;
classificationTable.showFilterButton = true;

const palette = {
  navy: "#102A35",
  green: "#245B49",
  greenSoft: "#DDEFE6",
  blue: "#315C7B",
  blueSoft: "#E8EDF5",
  sand: "#E5DCCB",
  cream: "#F8F6F1",
  amber: "#8A5A18",
  amberSoft: "#FFF0D8",
  red: "#8B3028",
  redSoft: "#F8DEDB",
  grey: "#EDF2F1",
  white: "#FFFFFF",
};

const titleFormat = {
  fill: palette.navy,
  font: { bold: true, color: palette.white, size: 18 },
  verticalAlignment: "center",
};
const subtitleFormat = {
  fill: palette.sand,
  font: { italic: true, color: palette.navy },
  wrapText: true,
  verticalAlignment: "center",
};
for (const [sheet, titleRange, subtitleRange] of [
  [summary, "A1:J1", "A2:J2"],
  [families, "A1:X1", "A2:X2"],
  [legend, "A1:H1", "A2:H2"],
]) {
  sheet.getRange(titleRange).format = titleFormat;
  sheet.getRange(titleRange).format.rowHeight = 34;
  sheet.getRange(subtitleRange).format = subtitleFormat;
  sheet.getRange(subtitleRange).format.rowHeight = 30;
}

summary.getRange("A4:D4").format = {
  fill: palette.green,
  font: { bold: true, color: palette.white },
  horizontalAlignment: "center",
};
summary.getRange("A5:A11").format = { fill: palette.cream, wrapText: true };
summary.getRange("B5:C11").format = {
  font: { bold: true, color: palette.navy, size: 13 },
  horizontalAlignment: "center",
  numberFormat: "0",
};
summary.getRange("D5:D11").format = {
  font: { bold: true },
  horizontalAlignment: "center",
  numberFormat: "0",
};
summary.getRange("D5:D11").conditionalFormats.add("cellIs", {
  operator: "equal",
  formula: 0,
  format: { fill: palette.greenSoft, font: { color: palette.green, bold: true } },
});
summary.getRange("D5:D11").conditionalFormats.add("cellIs", {
  operator: "notEqual",
  formula: 0,
  format: { fill: palette.redSoft, font: { color: palette.red, bold: true } },
});
summary.getRange("F4:J4").format = { fill: palette.red, font: { bold: true, color: palette.white } };
summary.getRange("F5:J7").format = {
  fill: "#FFF4E0",
  font: { bold: true, color: palette.red, size: 13 },
  wrapText: true,
  verticalAlignment: "center",
};
summary.getRange("F8:J11").format = {
  fill: "#F4F8FA",
  font: { color: palette.navy },
  wrapText: true,
  verticalAlignment: "center",
};
summary.getRange("A13:J13").format = { fill: palette.green, font: { bold: true, color: palette.white } };
summary.getRange("A14:E16").format = { fill: palette.cream, wrapText: true, verticalAlignment: "center" };
summary.getRange("F14:J16").format = { fill: palette.cream, wrapText: true, verticalAlignment: "center" };
summary.getRange("A17:E19").format = { fill: palette.grey, wrapText: true, verticalAlignment: "center" };
summary.getRange("F17:J19").format = { fill: palette.grey, wrapText: true, verticalAlignment: "center" };
summary.getRange("A21:J21").format = { fill: palette.grey, font: { color: palette.green }, wrapText: true };

families.getRange("A3:X3").format = {
  fill: palette.green,
  font: { bold: true, color: palette.white },
  wrapText: true,
  verticalAlignment: "center",
};
families.getRange(`A${familyDataStartRow}:X${familyDataEndRow}`).format = {
  wrapText: true,
  verticalAlignment: "top",
};
families.getRange(`A${familyDataStartRow}:D${familyDataEndRow}`).format.horizontalAlignment = "center";
families.getRange(`I${familyDataStartRow}:N${familyDataEndRow}`).format.horizontalAlignment = "center";
families.getRange(`P${familyDataStartRow}:T${familyDataEndRow}`).format.horizontalAlignment = "center";
families.getRange(`A${familyDataStartRow}:X${familyDataEndRow}`).format.rowHeight = 62;
families.getRange(`B${familyDataStartRow}:B${familyDataEndRow}`).format.numberFormat = "0";

const stateRange = families.getRange(`I${familyDataStartRow}:I${familyDataEndRow}`);
stateRange.conditionalFormats.add("containsText", {
  text: "PRIMARY_COPY_CONTROLLED",
  format: { fill: palette.greenSoft, font: { color: palette.green, bold: true } },
});
stateRange.conditionalFormats.add("containsText", {
  text: "CONTEXTUAL_PRIMARY_COPY_CONTROLLED",
  format: { fill: palette.blueSoft, font: { color: palette.blue, bold: true } },
});
stateRange.conditionalFormats.add("containsText", {
  text: "COURT_OFFICE_COPY_CONTROLLED",
  format: { fill: palette.amberSoft, font: { color: palette.amber, bold: true } },
});
stateRange.conditionalFormats.add("containsText", {
  text: "UNCONFIRMED",
  format: { fill: palette.redSoft, font: { color: palette.red, bold: true } },
});
stateRange.conditionalFormats.add("containsText", {
  text: "OPEN_FINAL_CHAIN",
  format: { fill: palette.redSoft, font: { color: palette.red, bold: true } },
});
const priorityRange = families.getRange(`R${familyDataStartRow}:R${familyDataEndRow}`);
priorityRange.conditionalFormats.add("containsText", {
  text: "CRITICAL",
  format: { fill: palette.redSoft, font: { color: palette.red, bold: true } },
});
priorityRange.conditionalFormats.add("containsText", {
  text: "HIGH",
  format: { fill: palette.amberSoft, font: { color: palette.amber, bold: true } },
});

legend.getRange("A3:G3").format = {
  fill: palette.green,
  font: { bold: true, color: palette.white },
  wrapText: true,
  verticalAlignment: "center",
};
legend.getRange(`A${statusStartRow}:G${statusEndRow}`).format = {
  wrapText: true,
  verticalAlignment: "top",
};
legend.getRange(`D${statusStartRow}:D${statusEndRow}`).format = {
  numberFormat: "0",
  horizontalAlignment: "center",
  font: { bold: true },
};
legend.getRange(`E${statusStartRow}:E${statusEndRow}`).format = {
  numberFormat: "0.0%",
  horizontalAlignment: "center",
};
legend.getRange(`A${classificationTitleRow}:G${classificationTitleRow}`).format = {
  fill: palette.green,
  font: { bold: true, color: palette.white },
};
legend.getRange(`A${classificationHeaderRow}:E${classificationHeaderRow}`).format = {
  fill: palette.green,
  font: { bold: true, color: palette.white },
  wrapText: true,
};
legend.getRange(`A${classificationStartRow}:E${classificationEndRow}`).format = {
  wrapText: true,
  verticalAlignment: "top",
};
legend.getRange(`D${classificationStartRow}:E${classificationEndRow}`).format = {
  numberFormat: "0",
  horizontalAlignment: "center",
  font: { bold: true },
};

for (let index = 0; index < statusEntries.length; index += 1) {
  const state = statusEntries[index][0];
  const rowNumber = statusStartRow + index;
  let fill = palette.cream;
  let color = palette.navy;
  if (state === "PRIMARY_COPY_CONTROLLED") [fill, color] = [palette.greenSoft, palette.green];
  else if (state === "CONTEXTUAL_PRIMARY_COPY_CONTROLLED") [fill, color] = [palette.blueSoft, palette.blue];
  else if (state === "COURT_OFFICE_COPY_CONTROLLED_FAMILY_INCOMPLETE") [fill, color] = [palette.amberSoft, palette.amber];
  else if (state === "UNCONFIRMED_SECONDARY_REFERENCE" || state === "OPEN_FINAL_CHAIN") [fill, color] = [palette.redSoft, palette.red];
  legend.getRange(`A${rowNumber}:C${rowNumber}`).format = {
    fill,
    font: { color, bold: true },
    wrapText: true,
  };
}

summary.getRange("A1:J21").format.columnWidth = 15;
summary.getRange("A1:A21").format.columnWidth = 31;
summary.getRange("B1:D21").format.columnWidth = 13;
summary.getRange("F1:J21").format.columnWidth = 17;
summary.getRange("A14:J19").format.rowHeight = 30;

const familyWidths = {
  A: 15, B: 12, C: 17, D: 31, E: 35, F: 35, G: 29, H: 29,
  I: 33, J: 31, K: 31, L: 38, M: 29, N: 29, O: 22, P: 22,
  Q: 30, R: 12, S: 20, T: 24, U: 42, V: 42, W: 40, X: 40,
};
for (const [column, width] of Object.entries(familyWidths)) {
  families.getRange(`${column}:${column}`).format.columnWidth = width;
}

legend.getRange("A:A").format.columnWidth = 42;
legend.getRange("B:C").format.columnWidth = 35;
legend.getRange("D:D").format.columnWidth = 12;
legend.getRange("E:E").format.columnWidth = 12;
legend.getRange("F:F").format.columnWidth = 52;
legend.getRange("G:G").format.columnWidth = 70;
legend.getRange("H:H").format.columnWidth = 3;
legend.getRange(`A${statusStartRow}:G${statusEndRow}`).format.rowHeight = 68;
legend.getRange(`A${classificationStartRow}:E${classificationEndRow}`).format.rowHeight = 42;

if (previewDir) {
  await fs.mkdir(previewDir, { recursive: true });
  for (const [sheetName, range, scale] of [
    ["Summary", "A1:J21", 1.1],
    ["Decision families", `A1:X${Math.min(familyDataEndRow, 15)}`, 0.7],
    ["Status legend", `A1:H${classificationEndRow}`, 0.9],
  ]) {
    const image = await workbook.render({ sheetName, range, scale, format: "png" });
    await fs.writeFile(
      path.join(previewDir, `${sheetName.toLowerCase().replaceAll(" ", "-")}.png`),
      new Uint8Array(await image.arrayBuffer()),
    );
  }
}

const summaryInspect = await workbook.inspect({
  kind: "table",
  range: "Summary!A4:J11",
  include: "values,formulas",
  tableMaxRows: 12,
  tableMaxCols: 10,
  maxChars: 8000,
});
const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 200 },
  summary: "final formula error scan",
  maxChars: 5000,
});
console.log(summaryInspect.ndjson);
console.log(formulaErrors.ndjson);

const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);
// The current artifact-tool exporter drops its in-memory freeze-pane state.
// Apply the equivalent OOXML view after export so Excel and Sheets preserve A:B and rows 1–3.
await ensureFrozenPanes(outputPath);
await fs.rm(`${outputPath}.inspect.ndjson`, { force: true });
console.log(`Saved ${outputPath}`);
