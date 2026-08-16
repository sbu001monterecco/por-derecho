(() => {
  const path = window.location.pathname;
  const es = path.includes('/es/mensaje-abierto-cgpj/');
  const en = path.includes('/en/open-message-cgpj/');
  if (!es && !en) return;
  if (document.querySelector('[data-cgpj-regage-28jul]')) return;

  const target = document.querySelector('#caso, #case');
  if (!target) return;

  const box = document.createElement('aside');
  box.dataset.cgpjRegage28jul = 'true';
  box.className = 'cg-note';
  box.style.marginTop = '1.25rem';
  box.innerHTML = es
    ? `<strong>Actualización documental · cronología verificada a 16 de agosto de 2026.</strong> El archivo original de DI 169/2026 fue acordado el <strong>14 de mayo</strong>. El recurso fue firmado y formalmente presentado por AGE/RedSARA el <strong>15 de junio de 2026</strong> bajo <code>REGAGE26e00056359487</code>, con cuatro archivos. La Sección de Recursos comunicó después que el recurso había tenido entrada en el CGPJ el <strong>18 de junio</strong>, que se tramitaba como <strong>Alzada 286/2026</strong> y que el escrito presentado el <strong>15 de julio</strong> quedaba unido al expediente. Por tanto, 15 de junio (presentación registral) y 18 de junio (entrada indicada por Recursos) son hitos distintos. Un acuerdo posterior del Promotor, de <strong>10 de julio</strong>, resolvió mantenerse en el archivo acordado el 14 de mayo; no cambia cuál es el acto recurrido. El módulo específico LPAM–Magistrado no figura entre los cuatro archivos del justificante de 15 de junio; su primera presentación formal actualmente verificada en la alzada es la aportación de <strong>28 de julio</strong>, <code>REGAGE26e00069061338</code>, con cinco PDF. <strong>Presentación ≠ incorporación al expediente ≠ examen ≠ aceptación ≠ veracidad de las alegaciones.</strong> La unión del escrito de 15 de julio sí fue expresamente confirmada por Recursos; no se ha localizado confirmación equivalente de examen sustantivo del paquete de 28 de julio. Hasta el 16 de agosto no se ha localizado en el correo revisado una resolución sustantiva posterior de la Alzada 286/2026.`
    : `<strong>Documentary update · chronology verified to 16 August 2026.</strong> The original DI 169/2026 archive was agreed on <strong>14 May</strong>. The appeal was signed and formally presented through AGE/RedSARA on <strong>15 June 2026</strong> under <code>REGAGE26e00056359487</code>, with four files. The CGPJ Appeals Section later stated that the appeal had entered the CGPJ on <strong>18 June</strong>, was being processed as <strong>Appeal 286/2026</strong>, and that the filing presented on <strong>15 July</strong> was joined to the appellate record. Thus 15 June (registry presentation) and 18 June (CGPJ entry reported by Appeals) are distinct events. A later Promotor agreement dated <strong>10 July</strong> resolved to remain with the archive agreed on 14 May; it does not change the identity of the appealed act. The specific LPAM–Judge module is not among the four files listed on the 15 June receipt; its first currently verified formal presentation in the appeal route is the <strong>28 July</strong> five-PDF supplement, <code>REGAGE26e00069061338</code>. <strong>Presentation ≠ incorporation into the file ≠ examination ≠ acceptance ≠ truth of the allegations.</strong> Joinder of the 15 July filing was expressly confirmed by Appeals; no equivalent confirmation of substantive examination of the 28 July package has been located. Through 16 August, no later substantive Appeal 286/2026 decision was located in the reviewed email.`;

  const shell = target.querySelector('.shell');
  if (shell) shell.appendChild(box);
})();
