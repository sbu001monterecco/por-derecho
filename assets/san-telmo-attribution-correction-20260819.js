(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEnglish = /(?:\/por-derecho)?\/en\/$/.test(path);
  const isSpanish = /(?:\/por-derecho)?\/es\/$/.test(path);
  if (!isEnglish && !isSpanish) return;

  const source = 'https://www.youtube.com/watch?v=mHn9IJU0qI4&t=488s';
  const githubHosted = path.includes('/por-derecho/');
  const dossier = isSpanish
    ? (githubHosted ? '/por-derecho/es/san-telmo-ricpe-sun-park/' : '/es/san-telmo-ricpe-sun-park/')
    : (githubHosted ? '/por-derecho/en/san-telmo-ricpe-sun-park/' : '/en/san-telmo-ricpe-sun-park/');

  const copy = isSpanish ? {
    badge: 'Registro audiovisual conectado · 30 nov 2021',
    title: 'El programa de San Telmo contiene una manifestación directa sobre introducción de clientes y una conversación más amplia sobre proyectos RICPE.',
    p1: '<strong>Corrección de atribución.</strong> En 08:08–08:12, el socio de San Telmo <strong>Eduardo Sánchez</strong> manifiesta: «bueno, nosotros en el despacho… en esa primera inversión… metimos unos cuantos clientes». El título del programa identifica a Enrique Guerra como invitado; no lo convierte en autor de esta manifestación concreta.',
    p2: 'En el pasaje más amplio y en la conversación posterior, Enrique Guerra aborda proyectos de RICPE, el perímetro promotor Acosta Matos, inmuebles de Lanzarote afectados por cuestiones judiciales de propiedad, «un complejo abandonado en Lanzarote» y la liberación de fondos de inversores contra certificaciones técnicas. Son manifestaciones separadas y no deben fundirse con la cita de cuatro segundos de Eduardo Sánchez.',
    p3: '<strong>Límite probatorio.</strong> El vídeo acredita que Eduardo Sánchez pronunció la manifestación citada. La identificación de «esa primera inversión» con la inversión RICPE asociada a Sun Park se apoya en la cronología RICPE/Sun Park citada separadamente. El conjunto no acredita por sí solo que los clientes mencionados invirtieran específicamente en Sun Park, que se transmitiera o utilizara indebidamente información concursal, que los profesionales coordinaran sus funciones ni que ninguna persona actuara ilícitamente.',
    p4: 'La cuestión resultante es documental: qué registros de encargo, conflictos, separación de expedientes, accesos, referral, remuneración, incorporación de inversores y KYC existían, qué entidad era responsable de cada control y dónde se conservan hoy.',
    button: 'Leer el expediente documental completo',
    context: 'Contexto más amplio del programa',
    contextText: 'Proyectos RICPE · Acosta Matos · propiedad e inversión en Lanzarote',
    cite: '«Enrique Guerra, en #UnCaféenSanTelmo» · San Telmo Abogados y Economistas · 30 nov 2021 · manifestación 08:08–08:12 · contexto 07:57–08:27 · transcripción pp. 29–30 de 85'
  } : {
    badge: 'Connected audiovisual record · 30 Nov 2021',
    title: 'The San Telmo programme contains a direct client-introduction statement and a wider RICPE project discussion.',
    p1: '<strong>Speaker correction.</strong> At 08:08–08:12, San Telmo partner <strong>Eduardo Sánchez</strong> states: <span lang="es">“bueno, nosotros en el despacho… en esa primera inversión… metimos unos cuantos clientes”</span>. A working English translation is: “well, we at the firm… in that first investment… brought in several clients.” The programme title identifies Enrique Guerra as the guest; it does not make him the speaker of this particular statement.',
    p2: 'In the wider passage and later discussion, Enrique Guerra addresses RICPE projects, the Acosta Matos promoter perimeter, Lanzarote property affected by judicial ownership issues, an “abandoned complex in Lanzarote” and release of investor money against technical certificates. Those are separate statements and must not be collapsed into Eduardo Sánchez’s four-second quotation.',
    p3: '<strong>Evidential boundary.</strong> The video proves that Eduardo Sánchez made the quoted statement. The identification of “that first investment” with the RICPE investment associated with Sun Park relies on the separately cited RICPE/Sun Park chronology. The combined material does not by itself prove that the clients mentioned invested specifically in Sun Park, that insolvency information was transferred or misused, that professionals coordinated their roles, or that any person acted unlawfully.',
    p4: 'The resulting question is documentary: what engagement, conflict, file-separation, access, referral, remuneration, investor-onboarding and KYC records existed, which entity was responsible for each control, and where are those records now?',
    button: 'Read the complete source-led dossier',
    context: 'Wider programme context',
    contextText: 'RICPE projects · Acosta Matos · Lanzarote property and investment discussion',
    cite: '“Enrique Guerra, en #UnCaféenSanTelmo” · San Telmo Abogados y Economistas · 30 Nov 2021 · statement 08:08–08:12 · context 07:57–08:27 · transcript pp. 29–30 of 85'
  };

  const apply = () => {
    const section = document.querySelector('section.interview-evidence');
    if (!section || section.dataset.pdSanTelmoAttribution === '20260819') return;

    section.setAttribute('aria-labelledby', 'interview-title');
    section.dataset.pdSanTelmoAttribution = '20260819';
    section.innerHTML = `
      <div class="interview-copy">
        <span class="evidence-badge allegation-badge">${copy.badge}</span>
        <h4 id="interview-title">${copy.title}</h4>
        <p>${copy.p1}</p>
        <p>${copy.p2}</p>
        <p>${copy.p3}</p>
        <p>${copy.p4}</p>
        <p class="actions"><a class="button secondary" href="${dossier}">${copy.button}</a></p>
      </div>
      <blockquote class="interview-quote" lang="es">
        <p><strong>Eduardo Sánchez · 08:08–08:12</strong><br>«bueno, nosotros en el despacho… en esa primera inversión… metimos unos cuantos clientes»</p>
        <p><strong>${copy.context}</strong><br>${copy.contextText}</p>
        <cite><a href="${source}" rel="external noopener" target="_blank">${copy.cite}</a></cite>
      </blockquote>`;
    document.dispatchEvent(new CustomEvent('pd:san-telmo-attribution-ready', {
      detail: { version: '20260819' }
    }));
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', apply, { once: true });
  } else {
    apply();
  }
})();
