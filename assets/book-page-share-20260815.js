(()=>{
  if(window.PorDerechoShare){
    window.PorDerechoShare.init(document);
    return;
  }
  if(document.querySelector('script[src*="share-controls-20260817.js"]')) return;
  const current=document.currentScript;
  if(!current) return;
  const script=document.createElement('script');
  script.src=new URL('share-controls-20260817.js?v=20260817a',current.src).href;
  script.defer=true;
  document.head.appendChild(script);
})();
