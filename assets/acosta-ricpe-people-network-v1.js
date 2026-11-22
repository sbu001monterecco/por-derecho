/* PD-AM-RICPE-PEOPLE-GRAPH-20261120-001: public projection, no telemetry. */
(() => {
  "use strict";
  const root = document.querySelector("[data-people-graph]");
  if (!root) return;
  const es = root.dataset.lang === "es";
  const q = selector => root.querySelector(selector);
  const words = es ? {
    founder: "Fundador", child: "Hijo/a documentado/a", all: "Todas las áreas",
    none: "Sin coincidencias", named: "personas observadas", roles: "vínculos fechados",
    date: "Fecha o periodo", source: "Fuente y alcance", observed: "Observación pública",
    approved: "Asiento oficial", historical: "Histórico / fechado", profile: "Perfil declarado",
    qualified: "Fuente delimitada", primaryPending: "Acto primario pendiente", unknown: "Identidad candidata", boardLimit:
      "Último asiento de nombramiento localizado, no certificado de titularidad, voto ni control. Quedan por comprobar actos posteriores y actas del consejo.",
    oldBoard: "Panorama del ejercicio 2025: sus nombramientos fueron cancelados de oficio en el asiento de 29 octubre 2026.",
    link: "Abrir fuente", bridge: "La financiación no convierte al prestamista en propietario.",
    relation: "Tipo de relación", noSource: "Referencia interna; comprobar fuente pública.",
    familyLimit: "No se ha verificado parentesco entre los perfiles Aguiar Acosta y una persona concreta de esta familia."
  } : {
    founder: "Founder", child: "Documented child", all: "All sections",
    none: "No matches", named: "named people", roles: "dated role records",
    date: "Date or period", source: "Source and scope", observed: "Public observation",
    approved: "Official registered act", historical: "Historical / dated", profile: "Profile report",
    qualified: "Qualified source", primaryPending: "Primary company act pending", unknown: "Candidate identity", boardLimit:
      "Latest located appointment act, not a certificate of ownership, voting power or control. Later acts and board minutes remain to be checked.",
    oldBoard: "FY2025 snapshot: those appointments were cancelled ex officio in the 29 October 2026 act.",
    link: "Open source", bridge: "Financing does not make a lender an equity owner.",
    relation: "Relationship type", noSource: "Internal reference; public source recheck needed.",
    familyLimit: "No kinship is verified between the Aguiar Acosta profiles and a named member of this family."
  };
  const lanes = es ? {
    founder:"Fundador",family:"Familia / gobierno",cross_perimeter:"Trayectorias",
    ricpe_board:"Consejo RICPE",ricpe_officer:"Órganos no consejeros",
    ricpe_management:"Equipo gestor",ricpe_historical:"Equipo histórico",
    ch_management:"Canarian Hospitality",ch_historical:"Hospitality histórico",
    hotel_historical:"Hoteles históricos",external_professional:"Profesional externo",
    historical_governance:"Gobierno histórico"
  } : {
    founder:"Founder",family:"Family / governance",cross_perimeter:"Careers",
    ricpe_board:"RICPE board",ricpe_officer:"Non-director officers",
    ricpe_management:"RICPE management",ricpe_historical:"Historic RICPE team",
    ch_management:"Canarian Hospitality",ch_historical:"Historic hospitality",
    hotel_historical:"Historic hotel roles",external_professional:"Outside professional",
    historical_governance:"Historical governance"
  };
  const roleEs = Object.freeze({"Accounting & administration":"Contabilidad y administración","Administration director":"Director de administración","Board member (published as José Acosta)":"Consejero (publicado como José Acosta)","CEO / managing partner":"Director general / «managing partner» (denominación publicada)","Chairman (published as José Acosta Matos)":"Presidente del consejo (publicado como José Acosta Matos)","Chief commercial officer / managing partner":"Director comercial / «managing partner» (denominación publicada)","Chief development officer / managing partner":"Director de desarrollo / «managing partner» (denominación publicada)","Corporate executive chef":"Chef ejecutivo corporativo","Debt Advisory":"Asesoramiento en deuda","Director":"Miembro del consejo de administración","Director and secretary":"Consejera y secretaria","Director of own-brand operations":"Directora de operaciones de marcas propias","E-commerce director":"Director de comercio electrónico","External investment professional":"Profesional externo de inversiones","Finance & administration director":"Director de finanzas y administración","Finance director":"Directora financiera","First deputy secretary":"Vicesecretario primero","First vice-president":"Vicepresidente primero","Founder; former president":"Fundador; antiguo presidente","General director; secretary & legal adviser":"Director general; secretario y asesor jurídico","HR senior adviser":"Asesora sénior de recursos humanos","Head of purchasing":"Responsable de compras","Historic company administrator; relationship to founder unverified":"Administradora societaria histórica; parentesco con el fundador no verificado","IT & business intelligence":"Tecnologías de la información e inteligencia empresarial","Investments & administration":"Inversiones y administración","Investments director":"Director de inversiones","Investor relations":"Relaciones con inversores","MYND Adeje director":"Director de MYND Adeje","MYND Yaiza director":"Director de MYND Yaiza","Marketing manager":"Responsable de marketing","Operations, HR & compliance director":"Director de operaciones, recursos humanos y cumplimiento","President":"Presidente","President / director":"Presidente / consejero","Processes, organisation and planning director":"Director de procesos, organización y planificación","Provisional Management & Guest Relations at LACASA Cotillo; name incomplete":"Gestión y relaciones con huéspedes en LACASA Cotillo (provisional); nombre incompleto","Radisson Blu Lanzarote director":"Director del Radisson Blu Lanzarote","Reported corporate law placement":"Estancia profesional declarada en derecho mercantil","Reported hotel-sector legal advisory":"Asesoramiento jurídico declarado en el sector hotelero","Reported investments/structuring placement":"Estancia profesional declarada en inversiones y estructuración","Reported summer internship including MYND Yaiza/Radisson Blu Lanzarote controllers and legal department":"Prácticas de verano declaradas, incluidos los departamentos de control de MYND Yaiza y Radisson Blu Lanzarote y el departamento jurídico","Revenue management director":"Directora de gestión de ingresos","Sales director":"Director de ventas","Second deputy secretary":"Vicesecretario segundo","Second vice-president":"Vicepresidente segundo","Secretary / delegated director / director":"Secretaria / consejera delegada / consejera","Sholeo Los Gigantes director":"Director de Sholeo Los Gigantes","Third deputy secretary":"Vicesecretario tercero","Vice-president":"Vicepresidente","Vice-president / director":"Vicepresidente / consejero","Vice-secretary / director":"Vicesecretario / consejero"});
  const whenEs = Object.freeze({"02 Feb 2024":"2 feb 2024","2022–2023":"2022–2023","2023":"2023","2024":"2024","2025":"2025","2026":"2026","FY2025 board; previous appointments cancelled 29 Oct 2026":"Consejo del ejercicio 2025; nombramientos previos cancelados el 29 oct 2026","Jul–Aug 2024":"jul–ago 2024","historic":"histórico","observed 20 Nov 2026":"observado el 20 nov 2026","registered 2 Apr 2024; published 9 Apr 2024":"inscrito el 2 abr 2024; publicado el 9 abr 2024","registered 29 Oct 2026; published 6 Nov 2026":"inscrito el 29 oct 2026; publicado el 6 nov 2026","registered 5 Aug 2021; published 16 Aug 2021":"inscrito el 5 ago 2021; publicado el 16 ago 2021","through 2020":"hasta 2020"});
  const kindEs = Object.freeze({"company_board":"consejo de administración","company_published_management":"dirección publicada por la empresa","executive_and_non_director_secretary":"dirección y secretaría no consejera","external_professional":"relación profesional externa","historic_governance":"gobierno histórico","historical_company_board":"consejo histórico de la sociedad","historical_company_people":"personal histórico de la sociedad","historical_governance":"gobierno histórico","historical_team":"equipo histórico","non_director_officer":"cargo no consejero","profile_reported_placement":"estancia declarada en perfil","registered_board":"consejo inscrito","registered_office":"cargo societario inscrito"});
  const edgeEs = Object.freeze({"2024_demerge_beneficiary":"beneficiaria de escisión de 2024","equity":"participación social","financing":"financiación","project_or_brand":"proyecto o marca","demerger":"escisión"});
  const edgeWhenEs = Object.freeze({"post 2022":"después de 2022","registered 02 Feb 2024":"inscrito el 2 feb 2024","sole shareholder registered 19 Jun 2024; FY2025 accounts report 100%":"socio único inscrito el 19 jun 2024; cuentas de 2025 indican el 100 %","two loan lines, 2022 and 2023; reported 31 Dec 2025":"dos partidas de préstamo, de 2022 y 2023; consignadas a 31 dic 2025"});
  const sourceEs = Object.freeze({"BORME30":"BORME Las Palmas, 12 feb 2024","BORME32":"BORME Las Palmas, 14 feb 2024","BORME72":"Corrección BORME, 12 abr 2024","RICBOARD":"RIC Private Equity — página del consejo de administración","RICTEAM":"RIC Private Equity — página del equipo gestor","RIC2022":"Presentación histórica de RICPE de 2022","RICFOUND":"Historia fundacional de RICPE","CHTEAM":"Canarian Hospitality — directorio de personas «Sobre nosotros»","FAMILY":"Expediente familiar bilingüe de Por Derecho","PROFILE_FAG":"Perfil público de Fernando Aguiar; conservado el 28 ago 2026","PROFILE_LAA":"Experiencia profesional de Laura Aguiar; conservada el 28 ago 2026","ARCHIVE_CH24":"Perfil corporativo de Canarian Hospitality, junio de 2024","ACTOR":"Registro controlado de identidades de Por Derecho","CNMV2025":"CNMV: cuentas auditadas de RICPE de 2025, certificación del consejo y plantilla","BORME2026":"BORME 6 nov 2026, asiento 497012 de Las Palmas (inscrito el 29 oct)","BORME122":"BORME 26 jun 2024, asiento 287289 de Las Palmas","CNMV2025LOANS":"Cuentas auditadas de RICPE de 2025, nota 7, préstamos participativos","BORME2021CH":"BORME 16 ago 2021, asiento 383950 de Canarian Hospitality","BORME2024ORION":"BORME 9 abr 2024, asiento 168456 de Orion Rental SOCIMI"});
  const roleLabel = role => es ? roleEs[role.role] || role.role : role.role;
  const whenLabel = value => es ? whenEs[value] || value : value;
  const kindLabel = value => es ? kindEs[value] || value : value.replaceAll("_", " ");
  const edgeLabel = value => es ? edgeEs[value] || value : value.replaceAll("_", " ");
  const edgeDate = value => es ? edgeWhenEs[value] || value : value;
  const el = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text !== null) node.textContent = String(text);
    if (className) node.className = className;
    return node;
  };
  const sourceLink = (data, key) => {
    const source = data.sources[key];
    if (!source) return el("span", words.noSource);
    if (!source.url) return el("span", (es ? sourceEs[key] || source.title : source.title) + " · " + words.noSource);
    const a = el("a", es ? sourceEs[key] || source.title : source.title);
    a.href = es && key === "FAMILY" ?
      source.url.replace("/en/acosta-matos-family/", "/es/acosta-matos-familia/") : source.url;
    if (/^https:\/\//.test(a.href)) {
      a.target = "_blank";
      a.rel = "noopener noreferrer";
    }
    return a;
  };
  const sourceList = (data, keys) => {
    const span = el("span", null, "sources");
    for (const key of keys) span.append(sourceLink(data, key));
    return span;
  };
  const roleState = role => {
    if (role.status === "needs_primary_company_act") return words.primaryPending;
    if (role.relation_kind === "registered_board" || role.status === "official" || (role.relation_kind === "registered_office" && role.status === "source_supported")) return words.approved;
    if (/historical|historic|superseded/.test(role.status + " " + role.relation_kind)) return words.historical;
    if (/profile/.test(role.status + " " + role.relation_kind)) return words.profile;
    return words.qualified;
  };
  function family(data, people) {
    const area = q("#family-diagram");
    const founder = people.get("p0013");
    const parent = el("div", null, "family-parent");
    parent.append(el("span", words.founder, "eyebrow"), el("strong", founder.name));
    area.replaceChildren(parent, el("div", null, "family-connector"));
    const children = el("div", null, "family-children");
    for (const edge of data.documented_family_edges) {
      const person = people.get(edge.to);
      const card = el("div", null, "family-child");
      const a = el("a", person.name); a.href = "#person-" + person.id;
      card.append(a, el("small", words.child), sourceList(data, edge.sources));
      children.append(card);
    }
    area.append(children);
    q("#aguiar-warning").textContent = words.familyLimit;
  }
  function board(data, people) {
    const select = q("#board-view");
    const area = q("#board-grid");
    function render() {
      const view = data.board_views.find(item => item.id === select.value);
      const rows = data.roles.filter(item =>
        item.organization_id === "RICPE" && item.relation_kind === view.relation_kind);
      if (rows.length !== view.expected_people) throw Error("Board view count mismatch");
      area.classList.toggle("historical", view.id === "historical_2025");
      area.replaceChildren();
      q("#board-context").textContent = view.id === "registered_2026" ? words.boardLimit : words.oldBoard;
      for (const role of rows) {
        const person = people.get(role.person_id), card = el("article", null, "board-card");
        const anchor = el("a", person.name); anchor.href = "#person-" + person.id;
        card.append(el("small", roleState(role)), anchor,
          el("strong", roleLabel(role)), el("small", whenLabel(role.when)), sourceList(data, role.sources));
        area.append(card);
      }
    }
    select.addEventListener("change", render);
    render();
  }
  function organisations(data) {
    const area = q("#institution-strip");
    for (const id of ["GAM", "GPAM", "RICPE", "CH"]) {
      const org = data.organisations.find(item => item.id === id);
      const n = data.roles.filter(item => item.organization_id === id).length;
      const card = el("div", null, "inst-card");
      card.append(el("strong", org.name), el("span", n + " " + (es ? "observaciones fechadas" : "dated observations")));
      area.append(card);
    }
    const edges = q("#org-links");
    for (const edge of data.organisation_edges) {
      const from = data.organisations.find(item => item.id === edge.from);
      const to = data.organisations.find(item => item.id === edge.to);
      const box = el("article", null, "org-link " + (edge.relation_type || ""));
      const type = edge.relation_type || (edge.kind.includes("demerge") ? "demerger" : "project / brand");
      box.append(el("small", edgeLabel(type)), el("strong", from.name + " → " + to.name),
        el("small", edgeDate(edge.when)), sourceList(data, edge.sources));
      if (edge.relation_type === "financing") box.append(el("small", words.bridge));
      edges.append(box);
    }
  }
  function careers(data, people) {
    const area = q("#career-timelines");
    for (const id of ["p0088", "p0095"]) {
      const card = el("article", null, "career-path");
      const person = people.get(id), name = el("a", person.name);
      name.href = "#person-" + id;
      card.append(name);
      const list = el("ol", null);
      for (const role of data.roles.filter(item => item.person_id === id)) {
        const org = data.organisations.find(item => item.id === role.organization_id);
        const item = el("li", null);
        item.append(el("strong", whenLabel(role.when) + " · " + org.name), el("small", roleLabel(role)),
          el("small", words.profile), sourceList(data, role.sources));
        list.append(item);
      }
      card.append(list); area.append(card);
    }
  }
  function personCard(data, person, roles) {
    const card = el("article", null, "person-card");
    card.id = "person-" + person.id;
    card.append(el("span", lanes[person.lane] || person.lane, "lane"), el("h3", person.name),
      el("code", person.canonical_actor_id || words.unknown, "person-id"));
    for (const role of roles) {
      const org = data.organisations.find(item => item.id === role.organization_id);
      const row = el("div", null, "role-row");
      row.append(el("strong", org.name), el("div", roleLabel(role), "role-name"));
      const meta = el("div", null, "role-meta");
      meta.append(el("span", whenLabel(role.when)), el("span", kindLabel(role.relation_kind)),
        el("span", roleState(role), "role-state"));
      const detail = el("details", null, "source-drawer");
      detail.append(el("summary", words.source), el("p", words.date + ": " + whenLabel(role.when)),
        sourceList(data, role.sources));
      row.append(meta, detail); card.append(row);
    }
    return card;
  }
  function directory(data, people) {
    const search = q("#person-search"), lane = q("#lane-filter");
    lane.append(el("option", words.all)); lane.lastChild.value = "";
    for (const [key, label] of Object.entries(lanes)) {
      lane.append(el("option", label)); lane.lastChild.value = key;
    }
    const params = new URLSearchParams(location.search);
    search.value = params.get("q") || "";
    function render() {
      const needle = search.value.normalize("NFKD").toLocaleLowerCase();
      const area = q("#people-cards");
      area.replaceChildren();
      const matches = data.people.filter(person => {
        if (lane.value && person.lane !== lane.value) return false;
        const roles = data.roles.filter(role => role.person_id === person.id);
        const text = [person.name, person.canonical_actor_id || "", person.short_name_on_company_page || "",
          ...roles.flatMap(role => {
            const org = data.organisations.find(item => item.id === role.organization_id);
            return [role.role, roleLabel(role), role.when, whenLabel(role.when), role.relation_kind, kindLabel(role.relation_kind), org.name, org.category];
          })].join(" ").normalize("NFKD").toLocaleLowerCase();
        return text.includes(needle);
      });
      matches.sort((a,b) => a.lane.localeCompare(b.lane) || a.name.localeCompare(b.name));
      for (const person of matches) area.append(personCard(data, person,
        data.roles.filter(role => role.person_id === person.id)));
      if (!matches.length) area.append(el("p", words.none));
      q("#match-count").textContent = matches.length + " / " + data.people.length;
      const url = new URL(location.href);
      if (needle) url.searchParams.set("q", search.value);
      else url.searchParams.delete("q");
      history.replaceState(null, "", url);
    }
    search.addEventListener("input", render);
    lane.addEventListener("change", render);
    render();
  }
  function validate(data) {
    if (data.control_id !== "PD-AM-RICPE-PEOPLE-GRAPH-20261120-001") throw Error("Control mismatch");
    const ids = new Set(data.people.map(person => person.id));
    const orgs = new Set(data.organisations.map(org => org.id));
    if (ids.size !== data.people.length || orgs.size !== data.organisations.length) throw Error("Duplicate identity");
    for (const role of data.roles) {
      if (!ids.has(role.person_id) || !orgs.has(role.organization_id) ||
          !role.when || !role.sources.every(key => data.sources[key])) throw Error("Incomplete sourced role");
    }
    for (const edge of [...data.documented_family_edges, ...data.organisation_edges]) {
      if (!(ids.has(edge.from) && ids.has(edge.to)) &&
          !(orgs.has(edge.from) && orgs.has(edge.to))) throw Error("Dangling graph edge");
      if (!edge.sources.every(key => data.sources[key])) throw Error("Unsourced graph edge");
    }
    if (data.documented_family_edges.some(edge => ["p0088","p0095"].includes(edge.from) ||
        ["p0088","p0095"].includes(edge.to))) throw Error("Unverified kinship");
  }
  fetch("../../assets/data/acosta-ricpe-people-network-20261120-v1.json", {credentials: "same-origin"})
    .then(response => {if (!response.ok) throw Error("HTTP " + response.status); return response.json();})
    .then(data => {
      validate(data);
      const people = new Map(data.people.map(person => [person.id, person]));
      q("#count-people").textContent = data.people.length;
      q("#count-roles").textContent = data.roles.length;
      q("#count-orgs").textContent = data.organisations.length;
      q("#count-people-label").textContent = words.named;
      q("#count-roles-label").textContent = words.roles;
      q("#source-date").textContent = es ? "Proyección pública actualizada 21 nov 2026" : "Public projection updated 21 Nov 2026";
      family(data, people); board(data, people); organisations(data);
      careers(data, people); directory(data, people);
      q("#loading").hidden = true;
    })
    .catch(error => {
      q("#loading").textContent = (es ? "No se pudo cargar el índice: " : "Could not load the index: ") + error.message;
    });
})();
