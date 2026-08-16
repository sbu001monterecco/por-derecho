(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEs = path.endsWith('/es/carta-abierta-lourdes-castillejo/');
  const isEn = path.endsWith('/en/open-letter-lourdes-castillejo/');
  if (!isEs && !isEn) return;
  if (document.getElementById('lourdes-linkedin-profile-20260816')) return;

  const facts = document.querySelector('.facts');
  if (!facts) return;

  const profileUrl = 'https://es.linkedin.com/in/lourdescastillejotrenas/en';
  const wrap = document.createElement('section');
  wrap.id = 'lourdes-linkedin-profile-20260816';
  wrap.setAttribute('aria-label', isEs ? 'Perfil LinkedIn de Lourdes Castillejo' : 'Lourdes Castillejo LinkedIn profile');
  wrap.style.cssText = 'border:1px solid #d8d3c8;border-radius:16px;padding:1.2rem 1.3rem;margin:1.35rem 0;background:#fff;';

  wrap.innerHTML = isEs ? `
    <p style="margin:0 0 .35rem;font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;">Captura de perfil profesional · LinkedIn</p>
    <h2 style="margin:.15rem 0 .65rem;">Lourdes Castillejo en LinkedIn</h2>
    <p>En una búsqueda realizada el <strong>16 de agosto de 2026</strong> por <strong>Lourdes Castillejo</strong> y <strong>Canarian Hospitality</strong>, LinkedIn devolvió un único perfil profesional coincidente:</p>
    <p><a href="${profileUrl}" rel="external noopener"><strong>Abrir el perfil público de Lourdes Castillejo en LinkedIn ↗</strong></a></p>
    <p class="small">Esta localización se publica como <strong>identificador profesional y fuente de contexto</strong>. No demuestra por sí sola que Lourdes realizara personalmente las solicitudes de Google Business, controlara <code>mynd.hotels@gmail.com</code>, conociera el episodio de 2019 o incurriera en conducta irregular. Esas cuestiones siguen sujetas a los registros nativos y a su derecho de respuesta.</p>
  ` : `
    <p style="margin:0 0 .35rem;font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;">Professional-profile capture · LinkedIn</p>
    <h2 style="margin:.15rem 0 .65rem;">Lourdes Castillejo on LinkedIn</h2>
    <p>In a search performed on <strong>16 August 2026</strong> for <strong>Lourdes Castillejo</strong> and <strong>Canarian Hospitality</strong>, LinkedIn returned a single matching professional profile:</p>
    <p><a href="${profileUrl}" rel="external noopener"><strong>Open Lourdes Castillejo's public LinkedIn profile ↗</strong></a></p>
    <p class="small">This is published as a <strong>professional identifier and contextual source</strong>. It does not by itself prove that Lourdes personally submitted the Google Business requests, controlled <code>mynd.hotels@gmail.com</code>, knew of the 2019 episode, or engaged in wrongdoing. Those questions remain subject to native records and her right of reply.</p>
  `;

  facts.insertAdjacentElement('afterend', wrap);
})();
