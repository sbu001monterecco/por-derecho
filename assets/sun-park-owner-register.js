(() => {
  "use strict";
  const isEs = document.documentElement.lang.toLowerCase().startsWith("es");
  const T = isEs ? {
    owner:"Titularidad de fuente · no adversa por defecto", ap89:"Vínculo AP89 separado",
    matkator:"Referencia Matkator de fuente", lpb:"Pista candidata LPB-12",
    open:"Fuente derivada · Registro pendiente", noResults:"No hay filas que coincidan con el filtro.",
    error:"No se pudo cargar el ledger. Abra el manifiesto controlado y la tabla TSV.",
    exact:"filas exactas", aggregate:"filas agregadas", direct:"DIRECT de fuente",
    bank:"BANCO de fuente", mat:"referencias Matkator", issues:"incidencias abiertas"
  } : {
    owner:"Source ownership · non-adverse by default", ap89:"Separate AP89 link",
    matkator:"Source Matkator reference", lpb:"LPB-12 candidate lead",
    open:"Derivative source · Registry open", noResults:"No rows match the filter.",
    error:"The ledger could not be loaded. Open the controlled manifest and TSV table.",
    exact:"exact rows", aggregate:"aggregate rows", direct:"source DIRECT",
    bank:"source BANCO", mat:"Matkator references", issues:"open issues"
  };
  const manifestUrl = "../../assets/data/sun-park-unit-owner-ledger-v1.precam-full-denominator.json";
  const tsvUrl = "../../assets/data/sun-park-unit-owner-ledger-v1.precam-full-denominator.tsv";
  const candidates = new Set(["109", "110", "801", "802", "805"]);
  const el = id => document.getElementById(id);
  const body = el("ledger-body"), aggregates = el("aggregate-body"), search = el("ledger-search");
  const filter = el("ledger-filter"), count = el("ledger-count"), summary = el("ledger-summary");
  let exactRows = [];

  const td = value => {
    const node = document.createElement("td");
    node.textContent = value === null || value === undefined || value === "" ? "—" : String(value);
    return node;
  };
  const badge = (text, cls) => {
    const node = document.createElement("span");
    node.className = `ledger-mini-badge ${cls}`;
    node.textContent = text;
    return node;
  };
  const parseTSV = text => {
    const lines = text.replace(/\r/g, "").trimEnd().split("\n");
    const headers = lines.shift().split("\t");
    return lines.filter(Boolean).map(line => {
      const values = line.split("\t");
      return Object.fromEntries(headers.map((header, index) => [header, values[index] || ""]));
    });
  };
  const layers = record => {
    const wrap = document.createElement("div");
    wrap.className = "ledger-badges";
    wrap.appendChild(badge(T.owner, "badge-owner"));
    if (record.cross_source_refs.includes("AP89:")) wrap.appendChild(badge(T.ap89, "badge-ap89"));
    if (record.association_codes.includes("MATKATOR_SOURCE_ASSOCIATION")) wrap.appendChild(badge(T.matkator, "badge-matkator"));
    if (candidates.has(record.unit_or_label)) wrap.appendChild(badge(T.lpb, "badge-lpb"));
    return wrap;
  };
  const status = record => {
    const wrap = document.createElement("div");
    wrap.appendChild(badge(T.open, "badge-open"));
    if (record.anomaly_flags) {
      const note = document.createElement("p");
      note.className = "ledger-source-note";
      note.textContent = record.anomaly_flags.split(";").join(" · ");
      wrap.appendChild(note);
    }
    return wrap;
  };
  const renderSummary = data => {
    const stats = [
      [data.exact_records, T.exact], [data.aggregate_rows, T.aggregate],
      [data.direct_classified_exact_records, T.direct], [data.bank_classified_exact_records, T.bank],
      [data.source_rows_referencing_matkator, T.mat], [8, T.issues]
    ];
    summary.replaceChildren(...stats.map(([number, label]) => {
      const box = document.createElement("div");
      box.className = "pd-ledger-stat";
      const strong = document.createElement("strong");
      strong.textContent = number;
      box.append(strong, document.createTextNode(label));
      return box;
    }));
  };
  const renderAggregates = rows => {
    aggregates.replaceChildren();
    rows.forEach(record => {
      const tr = document.createElement("tr");
      tr.append(td(record.finca_id), td(record.urbana_id), td(record.source_unit_count_or_expression),
        td(record.unit_or_label), td(`${record.quota_percent}%`), td(record.source_reported_owner_label));
      const state = document.createElement("td");
      state.appendChild(badge(T.open, "badge-open"));
      tr.appendChild(state);
      aggregates.appendChild(tr);
    });
  };
  const render = () => {
    const query = search.value.trim().toLocaleLowerCase();
    const classification = filter.value;
    const rows = exactRows.filter(record => {
      const haystack = [record.unit_or_label, record.finca_id, record.urbana_id, record.source_reported_owner_label]
        .join(" ").toLocaleLowerCase();
      return (!query || haystack.includes(query)) && (!classification || record.source_contact_classification === classification);
    });
    body.replaceChildren();
    if (!rows.length) {
      const tr = document.createElement("tr"), cell = td(T.noResults);
      cell.colSpan = 8; cell.className = "ledger-empty"; tr.appendChild(cell); body.appendChild(tr);
    }
    rows.forEach(record => {
      const tr = document.createElement("tr");
      tr.append(td(record.unit_or_label), td(record.finca_id), td(record.urbana_id), td(`${record.quota_percent}%`),
        td(record.source_contact_classification), td(record.source_reported_owner_label));
      const layerCell = document.createElement("td"); layerCell.appendChild(layers(record)); tr.appendChild(layerCell);
      const statusCell = document.createElement("td"); statusCell.appendChild(status(record)); tr.appendChild(statusCell);
      body.appendChild(tr);
    });
    count.textContent = `${rows.length} / ${exactRows.length}`;
  };
  Promise.all([
    fetch(manifestUrl, {cache:"no-store"}).then(r => { if (!r.ok) throw new Error(String(r.status)); return r.json(); }),
    fetch(tsvUrl, {cache:"no-store"}).then(r => { if (!r.ok) throw new Error(String(r.status)); return r.text(); })
  ]).then(([manifest, text]) => {
    const rows = parseTSV(text);
    exactRows = rows.filter(record => record.record_type === "EXACT");
    renderSummary(manifest.summary);
    renderAggregates(rows.filter(record => record.record_type === "AGGREGATE"));
    render();
    search.addEventListener("input", render);
    filter.addEventListener("change", render);
  }).catch(() => {
    body.replaceChildren();
    const tr = document.createElement("tr"), cell = td(T.error);
    cell.colSpan = 8; cell.className = "ledger-empty"; tr.appendChild(cell); body.appendChild(tr);
  });
})();
