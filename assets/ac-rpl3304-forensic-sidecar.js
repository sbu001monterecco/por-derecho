(function(){
  "use strict";
  const data=window.PD_RPL3304_PUBLIC_SIDECAR;
  if(!data) return;
  const root=document.querySelector("[data-rpl3304-forensic-reader]");
  if(!root) return;
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
  let currentPage=1, category="", query="";

  const t=(obj)=>obj && (obj[lang]||obj.es||obj.en||"");
  const label=(k)=>data.categories[k] ? (data.categories[k][lang]||data.categories[k].es) : k;
  const statusLabels={
    SUPPORTED:{es:"Apoyado",en:"Supported"},
    PARTIAL:{es:"Parcial",en:"Partial"},
    UNRESOLVED:{es:"No resuelto",en:"Unresolved"},
    RHETORICAL_OR_LEGAL:{es:"Retórico / jurídico",en:"Rhetorical / legal"}
  };

  function pdfUrl(page){
    return data.pdf+"#page="+page+"&view=FitH";
  }
  function goPage(page,noteId){
    currentPage=Math.max(1,Math.min(data.pages,Number(page)||1));
    frame.src=pdfUrl(currentPage);
    pageSelect.value=String(currentPage);
    root.querySelectorAll(".forensic-card.active").forEach(x=>x.classList.remove("active"));
    if(noteId){
      const card=root.querySelector("#note-"+CSS.escape(noteId));
      if(card){card.classList.add("active");card.scrollIntoView({block:"nearest",behavior:"smooth"});}
      history.replaceState(null,"","#note-"+noteId);
    }
  }
  for(let p=1;p<=data.pages;p++){
    const o=document.createElement("option");o.value=String(p);o.textContent=(lang==="es"?"Página ":"Page ")+p;pageSelect.appendChild(o);
  }
  pageSelect.addEventListener("change",()=>goPage(pageSelect.value));
  prev.addEventListener("click",()=>goPage(currentPage-1));
  next.addEventListener("click",()=>goPage(currentPage+1));

  const cats=["",...Object.keys(data.categories)];
  cats.forEach(k=>{
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
    return data.notes.filter(n=>{
      if(category && n.category!==category) return false;
      if(!query) return true;
      const hay=[t(n.title),t(n.quote),t(n.commentary),t(n.boundary),n.status,label(n.category)].join(" ").toLowerCase();
      return hay.includes(query);
    });
  }
  function renderViz(notes){
    vizBox.innerHTML="";
    const max=Math.max(1,...Object.keys(data.categories).map(c=>notes.filter(n=>n.category===c).length));
    Object.keys(data.categories).forEach(c=>{
      const n=notes.filter(x=>x.category===c).length;
      if(!n) return;
      const box=document.createElement("div");box.className="forensic-viz-item";box.style.setProperty("--viz",data.categories[c].color);
      box.innerHTML="<strong>"+label(c)+"</strong><small>"+n+" "+(lang==="es"?(n===1?"punto":"puntos"):(n===1?"item":"items"))+"</small><div class=\"forensic-viz-bar\"><div class=\"forensic-viz-fill\" style=\"width:"+Math.round((n/max)*100)+"%\"></div></div>";
      vizBox.appendChild(box);
    });
  }
  function render(){
    const notes=filtered();
    cardsBox.innerHTML="";
    renderViz(notes);
    count.textContent=notes.length+" / "+data.notes.length;
    if(!notes.length){cardsBox.innerHTML="<div class=\"forensic-empty\">"+(lang==="es"?"No hay comentarios con este filtro.":"No commentary matches this filter.")+"</div>";return;}
    notes.forEach(n=>{
      const card=document.createElement("article");
      card.className="forensic-card forensic-tone-"+n.category;
      card.id="note-"+n.id;
      const status=statusLabels[n.status] ? statusLabels[n.status][lang] : n.status;
      const links=(n.links||[]).map(l=>'<a href="'+(lang==="es"?l.hrefEs:l.hrefEn)+'">'+(lang==="es"?l.es:l.en)+" →</a>").join("");
      card.innerHTML=
        '<div class="forensic-card-head"><div><div class="forensic-tag-row"><span class="forensic-tag">'+label(n.category)+'</span><span class="forensic-tag">'+status+'</span></div><h4>'+t(n.title)+'</h4></div><button type="button" class="forensic-page-chip">'+(lang==="es"?"p. ":"p. ")+n.page+'</button></div>'+
        '<div class="forensic-quote">'+t(n.quote)+'</div>'+
        '<p class="forensic-comment">'+t(n.commentary)+'</p>'+
        '<div class="forensic-boundary"><strong>'+(lang==="es"?"Límite probatorio: ":"Evidence boundary: ")+'</strong>'+t(n.boundary)+'</div>'+
        (links?'<div class="forensic-links">'+links+'</div>':"");
      card.querySelector(".forensic-page-chip").addEventListener("click",()=>goPage(n.page,n.id));
      card.addEventListener("dblclick",()=>goPage(n.page,n.id));
      cardsBox.appendChild(card);
    });
  }
  search.addEventListener("input",()=>{query=search.value.trim().toLowerCase();render();});
  render();

  const hash=location.hash||"";
  if(hash.startsWith("#note-")){
    const id=hash.slice(6);
    const note=data.notes.find(n=>n.id===id);
    if(note) setTimeout(()=>goPage(note.page,note.id),50);
  }
})();