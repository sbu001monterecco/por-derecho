(function(){
  "use strict";
  const roots=[...document.querySelectorAll("[data-pd-pdf-forensic-viewer]")];
  if(!roots.length) return;

  const statusLabels={
    SUPPORTED:{es:"Apoyado",en:"Supported"},
    PARTIAL:{es:"Parcial",en:"Partial"},
    UNRESOLVED:{es:"No resuelto",en:"Unresolved"},
    RHETORICAL_OR_LEGAL:{es:"Retórico / jurídico",en:"Rhetorical / legal"},
    UNTESTED:{es:"No probado",en:"Untested"},
    CONTRADICTED:{es:"Contradicho",en:"Contradicted"}
  };

  function resolveCase(root){
    const globalName=root.dataset.caseGlobal;
    const key=root.dataset.caseKey;
    if(key && window.PD_PDF_FORENSIC_CASES && window.PD_PDF_FORENSIC_CASES[key]) return window.PD_PDF_FORENSIC_CASES[key];
    if(globalName && window[globalName]) return window[globalName];
    return null;
  }

  function mount(root){
    if(root.dataset.pdPdfForensicMounted==="true") return;
    const data=resolveCase(root);
    if(!data){root.dataset.pdPdfForensicState="missing-case";return;}
    root.dataset.pdPdfForensicMounted="true";
    root.dataset.pdPdfForensicState="ready";

    const lang=(root.dataset.lang||document.documentElement.lang||"es").toLowerCase().startsWith("en")?"en":"es";
    const $=(s)=>root.querySelector(s);
    const frame=$("[data-pdf-frame]");
    const pageSelect=$("[data-page-select]");
    const prev=$("[data-prev-page]");
    const next=$("[data-next-page]");
    const cardsBox=$("[data-forensic-cards]");
    const filtersBox=$("[data-forensic-filters]");
    const vizBox=$("[data-forensic-viz]");
    const search=$("[data-forensic-search]");
    const count=$("[data-forensic-count]");
    if(!frame||!pageSelect||!cardsBox||!filtersBox||!vizBox||!search||!count) return;

    let currentPage=1, category="", query="";
    const t=(obj)=>obj && (obj[lang]||obj.es||obj.en||"");
    const label=(k)=>data.categories && data.categories[k] ? (data.categories[k][lang]||data.categories[k].es||k) : k;
    const totalPages=Number(data.pages||root.dataset.pages||1);
    const pdf=data.pdf||root.dataset.pdfSrc||"";

    function pdfUrl(page){
      if(!pdf) return "";
      return pdf+"#page="+page+"&view=FitH&pagemode=none";
    }
    function goPage(page,noteId){
      currentPage=Math.max(1,Math.min(totalPages,Number(page)||1));
      if(pdf) frame.src=pdfUrl(currentPage);
      pageSelect.value=String(currentPage);
      root.querySelectorAll(".forensic-card.active").forEach(x=>x.classList.remove("active"));
      if(noteId){
        const card=root.querySelector("#note-"+CSS.escape(noteId));
        if(card){card.classList.add("active");card.scrollIntoView({block:"nearest",behavior:"smooth"});}
        try{history.replaceState(null,"","#note-"+noteId);}catch(_){}
      }
    }

    for(let p=1;p<=totalPages;p++){
      const o=document.createElement("option");
      o.value=String(p);o.textContent=(lang==="es"?"Página ":"Page ")+p;
      pageSelect.appendChild(o);
    }
    pageSelect.addEventListener("change",()=>goPage(pageSelect.value));
    prev&&prev.addEventListener("click",()=>goPage(currentPage-1));
    next&&next.addEventListener("click",()=>goPage(currentPage+1));

    const categories=data.categories||{};
    ["",...Object.keys(categories)].forEach(k=>{
      const b=document.createElement("button");
      b.type="button";b.className="forensic-filter";b.dataset.category=k;
      b.setAttribute("aria-pressed",k===""?"true":"false");
      b.textContent=k===""?(lang==="es"?"Todo":"All"):label(k);
      b.addEventListener("click",()=>{
        category=k;
        filtersBox.querySelectorAll(".forensic-filter").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));
        render();
      });
      filtersBox.appendChild(b);
    });

    function filtered(){
      const notes=Array.isArray(data.notes)?data.notes:[];
      return notes.filter(n=>{
        if(category && n.category!==category) return false;
        if(!query) return true;
        const hay=[t(n.title),t(n.quote),t(n.commentary),t(n.boundary),n.status,label(n.category),(n.issue||"")].join(" ").toLowerCase();
        return hay.includes(query);
      });
    }
    function renderViz(notes){
      vizBox.innerHTML="";
      const keys=Object.keys(categories);
      const max=Math.max(1,...keys.map(c=>notes.filter(n=>n.category===c).length));
      keys.forEach(c=>{
        const n=notes.filter(x=>x.category===c).length;
        if(!n) return;
        const box=document.createElement("div");
        box.className="forensic-viz-item";
        box.style.setProperty("--viz",categories[c].color||"#315c7b");
        box.innerHTML="<strong>"+label(c)+"</strong><small>"+n+" "+(lang==="es"?(n===1?"punto":"puntos"):(n===1?"item":"items"))+"</small><div class=\"forensic-viz-bar\"><div class=\"forensic-viz-fill\" style=\"width:"+Math.round((n/max)*100)+"%\"></div></div>";
        vizBox.appendChild(box);
      });
    }
    function render(){
      const notes=filtered();
      cardsBox.innerHTML="";
      renderViz(notes);
      const all=Array.isArray(data.notes)?data.notes:[];
      count.textContent=notes.length+" / "+all.length;
      if(!notes.length){
        cardsBox.innerHTML="<div class=\"forensic-empty\">"+(lang==="es"?"No hay comentarios con este filtro.":"No commentary matches this filter.")+"</div>";
        return;
      }
      notes.forEach(n=>{
        const card=document.createElement("article");
        card.className="forensic-card forensic-tone-"+(n.category||"CONTEXT");
        card.id="note-"+n.id;
        const status=statusLabels[n.status] ? statusLabels[n.status][lang] : (n.status||"");
        const links=(n.links||[]).map(l=>{
          const href=lang==="es"?(l.hrefEs||l.href):(l.hrefEn||l.href);
          const text=lang==="es"?(l.es||l.en):(l.en||l.es);
          return href?'<a href="'+href+'">'+text+" →</a>":"";
        }).join("");
        card.innerHTML=
          '<div class="forensic-card-head"><div><div class="forensic-tag-row"><span class="forensic-tag">'+label(n.category)+'</span>'+(status?'<span class="forensic-tag">'+status+'</span>':"")+'</div><h4>'+t(n.title)+'</h4></div><button type="button" class="forensic-page-chip">p. '+n.page+'</button></div>'+
          (t(n.quote)?'<div class="forensic-quote">'+t(n.quote)+'</div>':"")+
          '<p class="forensic-comment">'+t(n.commentary)+'</p>'+
          (t(n.boundary)?'<div class="forensic-boundary"><strong>'+(lang==="es"?"Límite probatorio: ":"Evidence boundary: ")+'</strong>'+t(n.boundary)+'</div>':"")+
          (links?'<div class="forensic-links">'+links+'</div>':"");
        card.querySelector(".forensic-page-chip").addEventListener("click",()=>goPage(n.page,n.id));
        card.addEventListener("dblclick",()=>goPage(n.page,n.id));
        cardsBox.appendChild(card);
      });
    }

    search.addEventListener("input",()=>{query=search.value.trim().toLowerCase();render();});
    root.addEventListener("keydown",e=>{
      if(["INPUT","TEXTAREA","SELECT"].includes(e.target.tagName)) return;
      if(e.key==="ArrowLeft"){e.preventDefault();goPage(currentPage-1);}
      if(e.key==="ArrowRight"){e.preventDefault();goPage(currentPage+1);}
    });
    render();
    if(pdf) frame.src=pdfUrl(1);

    const hash=location.hash||"";
    if(hash.startsWith("#note-")){
      const id=hash.slice(6);
      const note=(data.notes||[]).find(n=>n.id===id);
      if(note) setTimeout(()=>goPage(note.page,note.id),50);
    }
  }

  roots.forEach(mount);
})();