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
    ? `<strong>Actualización documental · 28 julio 2026.</strong> El justificante oficial AGE/RedSARA <code>REGAGE26e00069061338</code> acredita la presentación ante la Unidad de Registro y Archivo del CGPJ de una aportación dirigida a la <strong>Comisión Permanente / Sección de Recursos</strong>, identificando expresamente la <strong>Alzada 286/2026</strong> y la <strong>DI 169/2026</strong>, con cinco archivos PDF. El propio escrito precisa que el módulo específico LPAM–Magistrado <strong>no</strong> había quedado incorporado al escrito firmado de 18 de junio. <strong>Presentación ≠ incorporación al expediente ≠ examen ≠ aceptación ≠ veracidad de las alegaciones.</strong> La pregunta ahora es qué tratamiento motivado recibió esa aportación antes de resolverse la alzada.`
    : `<strong>Documentary update · 28 July 2026.</strong> Official AGE/RedSARA receipt <code>REGAGE26e00069061338</code> verifies presentation to the CGPJ Registry and Archive Unit of a supplementary filing addressed to the <strong>Permanent Commission / Appeals Section</strong>, expressly identifying <strong>Appeal 286/2026</strong> and <strong>DI 169/2026</strong>, with five PDF files. The filing itself corrects the chronology by stating that the specific LPAM–Judge module had <strong>not</strong> been incorporated into the signed 18 June filing. <strong>Presentation ≠ incorporation into the file ≠ examination ≠ acceptance ≠ truth of the allegations.</strong> The remaining question is what reasoned treatment that filing received before the appeal is decided.`;

  const shell = target.querySelector('.shell');
  if (shell) shell.appendChild(box);
})();
