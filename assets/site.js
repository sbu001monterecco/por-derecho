(() => {
  const current = document.currentScript;
  const legacy = document.createElement('script');
  legacy.src = new URL('site-base-1728fcf.js', current.src).href;
  legacy.onload = () => {
    const isSpanish = document.documentElement.lang === 'es';

    const title = isSpanish
      ? 'Límite del concurso: LPB sí; Matkator y la Explotadora, no por arrastre.'
      : 'Insolvency boundary: LPB was in the proceeding; Matkator and the Operating Community were not pulled in automatically.';

    const text = isSpanish
      ? 'El Concurso 36/2012 era de Luchy Playa Blanca, S.L.U. El propio expediente trata a la Comunidad de Explotación del Complejo Sun Park (CESP / Explotadora) como una estructura separada —incluso como deudora de un dividendo frente a LPB— y a Matkator como titular extraconcursal. Por ello, la condición de Administrador Concursal de LPB y la supervisión del Juzgado del concurso no conferían, por sí solas, poder directo para sustituir la autoridad de la Explotadora ni disponer de bienes de Matkator: cualquier efecto sobre esos planos exigía un título jurídico independiente y contemporáneo.<br><br>El puente de 2018 es verificable documentalmente. El Administrador Concursal escribió que entendía recibida la posesión al recibir las claves de acceso y anunció que daría instrucciones al administrador de la Comunidad para que accediera al complejo para mantenimiento y vigilancia; Gil respondió que mantenimiento, vigilancia y explotación correspondían a la Explotadora. Esta web no presenta ese intercambio como una sentencia de extralimitación. Lo presenta como la pregunta jurídica que debe cerrarse: <b>¿qué poder concreto permitió que facultades concursales sobre LPB produjeran efectos materiales sobre la Explotadora, Matkator, terceros y el negocio hotelero?</b><br><br>Gil Marer alega que éste fue un mecanismo recurrente: actores privados generaban o ejecutaban el acto operativo; la Administración Concursal lo habilitaba, transmitía o no lo impedía; y las actuaciones u omisiones judiciales permitían que la posición resultante persistiera. Si existió coordinación ilícita o responsabilidad individual es una cuestión para prueba y decisión por los órganos competentes, no una conclusión judicial que esta página dé por establecida.'
      : 'Insolvency Proceeding 36/2012 concerned Luchy Playa Blanca, S.L.U. The record itself treats the Comunidad de Explotación del Complejo Sun Park (CESP / Operating Community) as a separate structure —including as owing a dividend to LPB— and Matkator as an owner outside the insolvency estate. Accordingly, the Insolvency Administrator’s office over LPB and the insolvency court’s supervision did not, by themselves, confer direct power to replace the Operating Community’s authority or dispose of Matkator property: any effect on those separate planes required an independent, contemporaneous legal basis.<br><br>The 2018 bridge is document-verifiable. The Insolvency Administrator wrote that he understood possession to have been given to him when he received the access codes and said he would instruct the Owners’ Community administrator to enter the complex for maintenance and security; Gil replied that maintenance, security and operation belonged to the Operating Community. This site does not present that exchange as a judicial finding of excess of power. It presents the legal question that must be closed: <b>what specific authority allowed insolvency powers over LPB to produce material effects on the Operating Community, Matkator, third parties and the hotel business?</b><br><br>Gil Marer alleges that this became a recurring mechanism: private actors generated or executed the operative act; the Insolvency Administration enabled, transmitted or failed to stop it; and judicial acts or omissions allowed the resulting position to persist. Whether unlawful coordination or individual liability existed is a matter for evidence and determination by competent authorities, not a judicial conclusion asserted by this page.';

    const dossierSection = document.querySelector('#actor-accountability-12aug .shell');
    if (dossierSection && !document.getElementById('insolvency-boundary-12aug')) {
      const box = document.createElement('div');
      box.className = 'pressure-maxim';
      box.id = 'insolvency-boundary-12aug';
      box.style.marginTop = '1.5rem';
      box.innerHTML = `<strong>${title}</strong><span>${text}</span>`;
      const responsibility = dossierSection.querySelector('.responsibility-grid');
      if (responsibility) dossierSection.insertBefore(box, responsibility);
      else dossierSection.appendChild(box);
    }

    const mainUpdate = document.querySelector('#actor-update-12aug2026 .shell');
    if (mainUpdate && !document.getElementById('insolvency-boundary-main-12aug')) {
      const box = document.createElement('div');
      box.className = 'pressure-maxim';
      box.id = 'insolvency-boundary-main-12aug';
      box.style.marginTop = '1.5rem';
      box.innerHTML = `<strong>${title}</strong><span>${text}</span>`;
      mainUpdate.appendChild(box);
    }
  };
  legacy.onerror = () => console.error('Project Sun Rock base script failed to load.');
  document.head.appendChild(legacy);
})();