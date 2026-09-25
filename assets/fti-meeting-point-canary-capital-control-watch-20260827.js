(function () {
  "use strict";

  const root = document.querySelector("[data-fmr-watch]");
  if (!root) return;

  const lang = document.body.dataset.fmrLanguage || root.dataset.language || "en";
  const supportedLang = ["es", "en", "de"].includes(lang) ? lang : "en";
  const source = root.dataset.watchSrc;

  const ui = {
    es: {
      snapshot: "Corte público",
      lanes: "Líneas de vigilancia",
      runtime: "Estado operativo",
      runtimeValue: "Contrato de datos preparado; ejecución/cadencia no probadas",
      scope: "Activo, empresa o derecho",
      current: "Último estado documentado",
      test: "Inferencia, límite y producción",
      identity: "Identidad ^ y fuentes",
      inference: "Límite de inferencia",
      production: "Siguiente producción",
      sources: "Fuentes",
      dossier: "Abrir dossier",
      tableCaption: "Estado al corte; no es una certificación en tiempo real ni un registro exhaustivo de transmisiones.",
      rule: "Regla de actualización",
      caret: "Regla ^",
      loading: "Cargando el registro público de vigilancia…",
      error: "El registro dinámico no pudo cargarse. Consulte el JSON controlado directamente.",
      data: "Abrir vista derivada",
      canonical: "Abrir registro canónico"
    },
    en: {
      snapshot: "Public snapshot",
      lanes: "Watch lanes",
      runtime: "Operational state",
      runtimeValue: "Data contract ready; execution/cadence not proved",
      scope: "Asset, business or right",
      current: "Latest documented state",
      test: "Inference, boundary and production",
      identity: "^ identity and sources",
      inference: "Inference boundary",
      production: "Next production",
      sources: "Sources",
      dossier: "Open dossier",
      tableCaption: "State at the snapshot date; not real-time certification or an exhaustive transfer register.",
      rule: "Update rule",
      caret: "^ rule",
      loading: "Loading the public watch register…",
      error: "The dynamic register could not be loaded. Open the controlled JSON directly.",
      data: "Open derived view",
      canonical: "Open canonical register"
    },
    de: {
      snapshot: "Öffentlicher Stichtag",
      lanes: "Prüflinien",
      runtime: "Betriebsstatus",
      runtimeValue: "Datenvertrag vorbereitet; Ausführung/Taktung nicht belegt",
      scope: "Vermögenswert, Geschäft oder Recht",
      current: "Letzter dokumentierter Stand",
      test: "Schlussfolgerung, Grenze und Vorlage",
      identity: "^-Identität und Quellen",
      inference: "Schlussfolgerungsgrenze",
      production: "Nächste vorzulegende Unterlage",
      sources: "Quellen",
      dossier: "Dossier öffnen",
      tableCaption: "Stand zum Stichtag; keine Echtzeit-Zertifizierung und kein vollständiges Übertragungsregister.",
      rule: "Aktualisierungsregel",
      caret: "^-Regel",
      loading: "Öffentliches Prüfregister wird geladen…",
      error: "Das dynamische Register konnte nicht geladen werden. Öffnen Sie die kontrollierte JSON-Datei direkt.",
      data: "Abgeleitete Ansicht öffnen",
      canonical: "Kanonisches Register öffnen"
    }
  }[supportedLang];

  function addText(parent, tag, text, className) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    node.textContent = text;
    parent.appendChild(node);
    return node;
  }

  function localized(value) {
    if (!value || typeof value !== "object") return "";
    return value[supportedLang] || value.en || "";
  }

  function friendlyEvent(value) {
    return String(value || "").toLowerCase().replaceAll("_", " ");
  }

  function appendLinks(parent, item, canonical) {
    const links = document.createElement("div");
    links.className = "fm-watch__links";

    const sourceMap = new Map((canonical.sources || []).map(function (sourceItem) {
      return [sourceItem.source_id, sourceItem];
    }));
    (item.canonical_source_refs || []).map(function (sourceRef) {
      return sourceMap.get(sourceRef);
    }).filter(Boolean).forEach(function (sourceItem) {
      const anchor = document.createElement("a");
      anchor.href = sourceItem.url;
      anchor.textContent = sourceItem.title;
      if (/^https?:\/\//.test(sourceItem.url)) {
        anchor.target = "_blank";
        anchor.rel = "noopener";
      }
      links.appendChild(anchor);
    });

    const dossierPath = item.dossier_paths && (item.dossier_paths[supportedLang] || item.dossier_paths.en);
    if (dossierPath) {
      const dossier = document.createElement("a");
      dossier.href = dossierPath;
      dossier.textContent = ui.dossier + " →";
      links.appendChild(dossier);
    }

    parent.appendChild(links);
  }

  function render(data, canonical, canonicalURL) {
    if (!data || data.schema !== "por-derecho.fti-meeting-point-canary-capital-control-watch-derived-public-view.v1" || !Array.isArray(data.presentation_lanes)) {
      throw new Error("Invalid derived watch-view schema");
    }
    if (!canonical || canonical.schema !== data.canonical_register.schema || canonical.control_id !== data.canonical_register.control_id) {
      throw new Error("Canonical watch-register mismatch");
    }

    root.replaceChildren();

    const meta = document.createElement("div");
    meta.className = "fm-watch__meta";
    [
      [ui.snapshot, data.snapshot_date],
      [ui.lanes, String(data.presentation_lanes.length)],
      [ui.runtime, ui.runtimeValue]
    ].forEach(function (entry) {
      const box = document.createElement("div");
      addText(box, "span", entry[0]);
      addText(box, "strong", entry[1]);
      meta.appendChild(box);
    });
    root.appendChild(meta);

    const rule = document.createElement("div");
    rule.className = "fm-watch__rule";
    const scopeBox = document.createElement("div");
    addText(scopeBox, "strong", ui.rule);
    addText(scopeBox, "p", localized(data.monitoring_rule));
    rule.appendChild(scopeBox);
    const caretBox = document.createElement("div");
    addText(caretBox, "strong", ui.caret);
    addText(caretBox, "p", localized(data.caret_boundary));
    rule.appendChild(caretBox);
    root.appendChild(rule);

    const wrapper = document.createElement("div");
    wrapper.className = "fm-watch__table-wrap";
    const table = document.createElement("table");
    table.className = "fm-watch__table";
    const caption = document.createElement("caption");
    caption.textContent = ui.tableCaption;
    table.appendChild(caption);

    const head = document.createElement("thead");
    const headRow = document.createElement("tr");
    [ui.scope, ui.current, ui.test, ui.identity].forEach(function (label) {
      addText(headRow, "th", label);
    });
    head.appendChild(headRow);
    table.appendChild(head);

    const body = document.createElement("tbody");
    data.presentation_lanes.forEach(function (item) {
      const row = document.createElement("tr");
      row.dataset.watchId = item.id;
      row.dataset.watchState = item.state;

      const scopeCell = document.createElement("td");
      scopeCell.dataset.column = ui.scope;
      addText(scopeCell, "span", [item.id].concat(item.canonical_refs || []).join(" · "), "fm-watch__id");
      addText(scopeCell, "strong", localized(item.scope));
      const eventList = document.createElement("div");
      eventList.className = "fm-watch__event-list";
      (item.event_classes || []).forEach(function (eventClass) {
        addText(eventList, "span", friendlyEvent(eventClass), "fm-watch__event");
      });
      scopeCell.appendChild(eventList);
      row.appendChild(scopeCell);

      const currentCell = document.createElement("td");
      currentCell.dataset.column = ui.current;
      const status = addText(currentCell, "span", localized(data.evidence_states[item.state]), "fm-watch__status");
      status.dataset.state = item.state;
      addText(currentCell, "p", localized(item.latest_state));
      row.appendChild(currentCell);

      const testCell = document.createElement("td");
      testCell.dataset.column = ui.test;
      addText(testCell, "strong", ui.inference, "fm-watch__label");
      addText(testCell, "p", localized(item.inference_boundary));
      addText(testCell, "strong", ui.production, "fm-watch__label");
      addText(testCell, "p", localized(item.next_production));
      row.appendChild(testCell);

      const identityCell = document.createElement("td");
      identityCell.dataset.column = ui.identity;
      addText(identityCell, "p", localized(item.identity_state), "fm-watch__identity");
      addText(identityCell, "strong", ui.sources, "fm-watch__label");
      appendLinks(identityCell, item, canonical);
      row.appendChild(identityCell);

      body.appendChild(row);
    });
    table.appendChild(body);
    wrapper.appendChild(table);
    root.appendChild(wrapper);

    const linkRow = document.createElement("div");
    linkRow.className = "fm-watch__links";
    const canonicalLink = document.createElement("a");
    canonicalLink.href = canonicalURL;
    canonicalLink.textContent = ui.canonical + " →";
    canonicalLink.className = "button";
    linkRow.appendChild(canonicalLink);
    const dataLink = document.createElement("a");
    dataLink.href = source;
    dataLink.textContent = ui.data + " →";
    dataLink.className = "button secondary";
    linkRow.appendChild(dataLink);
    root.appendChild(linkRow);
  }

  function showError() {
    root.replaceChildren();
    const error = addText(root, "p", ui.error + " ", "fm-watch__error");
    const dataLink = document.createElement("a");
    dataLink.href = source;
    dataLink.textContent = ui.data + " →";
    error.appendChild(dataLink);
  }

  addText(root, "p", ui.loading, "fm-watch__loading");
  if (!source) {
    showError();
    return;
  }

  fetch(source, { cache: "no-store" })
    .then(function (response) {
      if (!response.ok) throw new Error("Derived watch view unavailable");
      return response.json();
    })
    .then(function (view) {
      const viewURL = new URL(source, document.baseURI);
      const canonicalURL = new URL(view.canonical_register.path_relative_to_this_view, viewURL);
      return fetch(canonicalURL, { cache: "no-store" })
        .then(function (response) {
          if (!response.ok) throw new Error("Canonical watch register unavailable");
          return response.json();
        })
        .then(function (canonical) {
          render(view, canonical, canonicalURL.href);
        });
    })
    .catch(showError);
}());
