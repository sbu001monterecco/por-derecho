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

  const visualCapture = `
    <figure style="margin:1rem 0 1.1rem;">
      <a href="${profileUrl}" rel="external noopener" style="display:block;text-decoration:none;color:inherit;" aria-label="${isEs ? 'Abrir perfil público de Lourdes Castillejo Trenas en LinkedIn' : 'Open Lourdes Castillejo Trenas public LinkedIn profile'}">
        <svg viewBox="0 0 1200 760" role="img" aria-label="${isEs ? 'Captura visual del perfil público indexado de LinkedIn de Lourdes Castillejo Trenas' : 'Visual capture of Lourdes Castillejo Trenas indexed public LinkedIn profile'}" style="width:100%;height:auto;display:block;border-radius:14px;background:#fff;">
          <rect x="4" y="4" width="1192" height="752" rx="24" fill="#fbfbfb" stroke="#c9c9c9" stroke-width="3"/>
          <text x="40" y="58" font-family="Arial,Helvetica,sans-serif" font-size="19" font-weight="700" fill="#333">${isEs ? 'CAPTURA VISUAL · PERFIL PÚBLICO LINKEDIN' : 'VISUAL CAPTURE · PUBLIC LINKEDIN PROFILE'}</text>
          <circle cx="100" cy="160" r="58" fill="#f0f0f0" stroke="#999" stroke-width="3"/>
          <text x="100" y="177" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="46" font-weight="700" fill="#555">LC</text>
          <text x="205" y="140" font-family="Arial,Helvetica,sans-serif" font-size="46" font-weight="700" fill="#111">Lourdes Castillejo Trenas</text>
          <text x="205" y="185" font-family="Arial,Helvetica,sans-serif" font-size="27" font-weight="700" fill="#222">Canarian Hospitality</text>
          <text x="205" y="224" font-family="Arial,Helvetica,sans-serif" font-size="24" fill="#444">${isEs ? 'Málaga, Andalucía, España' : 'Málaga, Andalusia, Spain'}</text>
          <text x="40" y="305" font-family="Arial,Helvetica,sans-serif" font-size="25" fill="#333">${isEs ? '5 mil seguidores · Más de 500 contactos' : '5K followers · 500+ connections'}</text>
          <text x="40" y="360" font-family="Arial,Helvetica,sans-serif" font-size="23" fill="#333">${isEs ? 'Formación mostrada: Les Roches Crans-Montana Global Hospitality' : 'Education shown: Les Roches Crans-Montana Global Hospitality'}</text>
          <text x="40" y="405" font-family="Arial,Helvetica,sans-serif" font-size="23" fill="#333">${isEs ? 'Sitios enlazados: canarianhospitality.com · myndhotels.com' : 'Linked websites: canarianhospitality.com · myndhotels.com'}</text>
          <rect x="40" y="455" width="1120" height="68" rx="13" fill="#fff" stroke="#b8b8b8" stroke-width="2"/>
          <text x="62" y="499" font-family="Arial,Helvetica,sans-serif" font-size="25" font-weight="700" fill="#222">es.linkedin.com/in/lourdescastillejotrenas</text>
          <text x="40" y="575" font-family="Arial,Helvetica,sans-serif" font-size="19" fill="#555">${isEs ? 'Fuente verificada el 16/08/2026 mediante el perfil público indexado de LinkedIn y búsqueda exacta.' : 'Source verified on 16 Aug 2026 through LinkedIn’s indexed public profile and exact-name search.'}</text>
          <text x="40" y="608" font-family="Arial,Helvetica,sans-serif" font-size="19" fill="#555">${isEs ? 'Esta imagen es una captura visual preparada por Por Derecho a partir del contenido público indexado.' : 'This image is a visual capture prepared by Por Derecho from publicly indexed profile content.'}</text>
          <text x="40" y="641" font-family="Arial,Helvetica,sans-serif" font-size="19" fill="#555">${isEs ? 'No es una exportación forense ni una captura nativa del navegador.' : 'It is not a forensic export or a native browser screenshot.'}</text>
          <text x="40" y="710" font-family="Arial,Helvetica,sans-serif" font-size="19" font-weight="700" fill="#333">${isEs ? 'Uso: identificación profesional y contexto · sujeto a corrección y derecho de respuesta' : 'Use: professional identification and context · subject to correction and right of reply'}</text>
        </svg>
      </a>
      <figcaption class="small" style="margin-top:.55rem;">${isEs ? 'Captura visual de referencia del contenido público indexado. No se republica una fotografía personal de LinkedIn.' : 'Reference visual capture of the publicly indexed content. No personal LinkedIn photograph is republished.'}</figcaption>
    </figure>`;

  wrap.innerHTML = isEs ? `
    <p style="margin:0 0 .35rem;font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;">Captura de perfil profesional · LinkedIn</p>
    <h2 style="margin:.15rem 0 .65rem;">Lourdes Castillejo en LinkedIn</h2>
    <p>En una búsqueda realizada el <strong>16 de agosto de 2026</strong> por <strong>Lourdes Castillejo</strong> y <strong>Canarian Hospitality</strong>, LinkedIn devolvió un único perfil profesional coincidente:</p>
    ${visualCapture}
    <p><a href="${profileUrl}" rel="external noopener"><strong>Abrir el perfil público de Lourdes Castillejo en LinkedIn ↗</strong></a></p>
    <p class="small">Esta localización se publica como <strong>identificador profesional y fuente de contexto</strong>. No demuestra por sí sola que Lourdes realizara personalmente las solicitudes de Google Business, controlara <code>mynd.hotels@gmail.com</code>, conociera el episodio de 2019 o incurriera en conducta irregular. Esas cuestiones siguen sujetas a los registros nativos y a su derecho de respuesta.</p>
  ` : `
    <p style="margin:0 0 .35rem;font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;">Professional-profile capture · LinkedIn</p>
    <h2 style="margin:.15rem 0 .65rem;">Lourdes Castillejo on LinkedIn</h2>
    <p>In a search performed on <strong>16 August 2026</strong> for <strong>Lourdes Castillejo</strong> and <strong>Canarian Hospitality</strong>, LinkedIn returned a single matching professional profile:</p>
    ${visualCapture}
    <p><a href="${profileUrl}" rel="external noopener"><strong>Open Lourdes Castillejo's public LinkedIn profile ↗</strong></a></p>
    <p class="small">This is published as a <strong>professional identifier and contextual source</strong>. It does not by itself prove that Lourdes personally submitted the Google Business requests, controlled <code>mynd.hotels@gmail.com</code>, knew of the 2019 episode, or engaged in wrongdoing. Those questions remain subject to native records and her right of reply.</p>
  `;

  facts.insertAdjacentElement('afterend', wrap);
})();
