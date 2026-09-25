
(function(){
  const root = document.documentElement;
  root.setAttribute('data-lang', 'es');
  const buttons = document.querySelectorAll('[data-lang]');
  function setLang(lang){
    root.setAttribute('data-lang', lang);
    root.setAttribute('lang', lang);
    buttons.forEach(btn => btn.classList.toggle('active', btn.getAttribute('data-lang') === lang));
  }
  buttons.forEach(btn => btn.addEventListener('click', () => setLang(btn.getAttribute('data-lang'))));
})();
