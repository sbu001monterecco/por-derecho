(() => {
  const d = document;

  const render = () => {
    if (d.querySelector('[data-alertador-notice]')) return;
    const en = (d.documentElement.lang || '').toLowerCase().startsWith('en');
    const notice = d.createElement('aside');
    notice.className = 'alertador-notice';
    notice.dataset.alertadorNotice = '20260823';
    notice.setAttribute('aria-labelledby', 'alertador-notice-title');

    const eu = 'https://eur-lex.europa.eu/eli/dir/2019/1937/oj';
    const germany = 'https://www.gesetze-im-internet.de/hinschg/';

    notice.innerHTML = en ? `
      <div class="shell alertador-notice__inner">
        <p class="alertador-notice__kicker">AUTHORSHIP · PUBLIC-INTEREST REPORTING</p>
        <h2 id="alertador-notice-title">Author's reporting-person / whistleblowing position</h2>
        <p>Gil Marer states that he has acted and continues to act as a reporting person/whistleblower, communicating to authorities, regulators, professional bodies and other competent recipients information and allegations that he considers grounded and in the public interest. He invokes—where materially, personally, temporally and territorially applicable—<a href="${eu}" target="_blank" rel="noopener">Directive (EU) 2019/1937</a>, <a href="https://www.boe.es/buscar/act.php?id=BOE-A-2023-4513" target="_blank" rel="noopener">Spain's Law 2/2023</a>, Germany's <a href="${germany}" target="_blank" rel="noopener">Hinweisgeberschutzgesetz (HinSchG)</a>, and the protected-disclosure regimes of <a href="https://www.legislation.gov.uk/ukpga/1996/18/part/IVA" target="_blank" rel="noopener">Great Britain</a> and <a href="https://www.legislation.gov.uk/nisi/1996/1919/contents" target="_blank" rel="noopener">Northern Ireland</a>.</p>
        <p class="alertador-notice__limit">This statement records the capacity in which the author says he acts. It does not itself confer or establish protected-reporting-person status or retrospectively turn earlier facts into infringements of later rules. In Spain, the <a href="https://www.boe.es/buscar/act.php?id=BOE-A-2023-4513#da-6" target="_blank" rel="noopener">Sixth Additional Provision of Law 2/2023</a> may extend protective measures to people who reported acts or omissions within Article 2 that occurred after Directive (EU) 2019/1937 entered into force, even where the communication preceded the Law. That timing rule does not remove the remaining requirements. Protection in each instance depends on the facts, subject matter, reasonable belief, channel and recipient, work-related or professional context, personal, material, temporal and territorial scope, time limits and statutory exclusions. The application of the Great Britain and Northern Ireland regimes is not automatic either. No court, regulator or competent authority is presented here as having determined that status for every communication.</p>
        <p class="alertador-notice__sources"><strong>Official sources:</strong> <a href="https://www.legislation.gov.uk/ukpga/1998/23/contents" target="_blank" rel="noopener">Public Interest Disclosure Act 1998</a> · <a href="https://www.legislation.gov.uk/nisi/1998/1763/contents" target="_blank" rel="noopener">Public Interest Disclosure (Northern Ireland) Order 1998</a>.</p>
      </div>` : `
      <div class="shell alertador-notice__inner">
        <p class="alertador-notice__kicker">AUTORÍA · COMUNICACIÓN DE INTERÉS PÚBLICO</p>
        <h2 id="alertador-notice-title">Posición del autor como persona informante / alertador</h2>
        <p>Gil Marer declara que ha actuado y continúa actuando como persona informante/alertador, comunicando a autoridades, reguladores, órganos profesionales y otros destinatarios competentes información y alegaciones que considera fundadas y de interés público. Invoca —cuando resulten material, personal, temporal y territorialmente aplicables— la <a href="${eu}" target="_blank" rel="noopener">Directiva (UE) 2019/1937</a>, la <a href="https://www.boe.es/buscar/act.php?id=BOE-A-2023-4513" target="_blank" rel="noopener">Ley 2/2023 española</a>, la <a href="${germany}" target="_blank" rel="noopener">Hinweisgeberschutzgesetz (HinSchG) alemana</a> y los regímenes de divulgaciones protegidas de <a href="https://www.legislation.gov.uk/ukpga/1996/18/part/IVA" target="_blank" rel="noopener">Gran Bretaña</a> y de <a href="https://www.legislation.gov.uk/nisi/1996/1919/contents" target="_blank" rel="noopener">Irlanda del Norte</a>.</p>
        <p class="alertador-notice__limit">Esta declaración registra la capacidad en la que el autor afirma actuar. No confiere ni acredita por sí sola la condición jurídica de informante protegido, ni convierte retroactivamente hechos anteriores en infracciones de normas posteriores. Respecto de España, la <a href="https://www.boe.es/buscar/act.php?id=BOE-A-2023-4513#da-6" target="_blank" rel="noopener">disposición adicional sexta de la Ley 2/2023</a> puede extender las medidas de protección a personas que comunicaron acciones u omisiones comprendidas en su artículo 2 y ocurridas desde la entrada en vigor de la Directiva (UE) 2019/1937, aunque la comunicación precediera a la Ley. Esa regla temporal no elimina los restantes requisitos. En cada caso, la protección depende de los hechos, la materia comunicada, la creencia razonable, el canal y destinatario, el contexto laboral o profesional, los ámbitos personal, material, temporal y territorial, los plazos y las exclusiones legales. La aplicación de los regímenes de Gran Bretaña e Irlanda del Norte tampoco es automática. Ningún tribunal, regulador o autoridad competente se presenta aquí como si hubiera determinado esa condición para todas las comunicaciones.</p>
        <p class="alertador-notice__sources"><strong>Fuentes oficiales:</strong> <a href="https://www.legislation.gov.uk/ukpga/1998/23/contents" target="_blank" rel="noopener">Public Interest Disclosure Act 1998</a> · <a href="https://www.legislation.gov.uk/nisi/1998/1763/contents" target="_blank" rel="noopener">Public Interest Disclosure (Northern Ireland) Order 1998</a>.</p>
      </div>`;

    const style = d.createElement('style');
    style.textContent = `
      .alertador-notice{border-top:7px solid #d1a13a;background:#10242d;color:#f7fafb;padding:1.4rem 0 1.6rem}
      .alertador-notice__inner{box-sizing:border-box;width:min(1180px,calc(100% - 2rem));max-width:none;margin-inline:auto}.alertador-notice__kicker{margin:0 0 .35rem;color:#f0c76c;font-size:.75rem;font-weight:950;letter-spacing:.11em}.alertador-notice h2{margin:.15rem 0 .75rem;color:#fff;font-size:clamp(1.35rem,2.6vw,2.1rem)}.alertador-notice p{max-width:105ch;margin:.6rem 0;line-height:1.55}.alertador-notice a{color:#ffe099;text-decoration-thickness:2px;text-underline-offset:3px}.alertador-notice a:hover,.alertador-notice a:focus-visible{color:#fff}.alertador-notice__limit{box-sizing:border-box;padding:.8rem 1rem;border-left:5px solid #d1a13a;background:rgba(255,255,255,.07);font-size:.9rem}.alertador-notice__sources{font-size:.82rem;color:#dce5e8}
    `;
    d.head.append(style);

    const footer = d.querySelector('footer.site-footer, .site-footer');
    const main = d.querySelector('main');
    if (footer) footer.insertAdjacentElement('beforebegin', notice);
    else if (main) main.insertAdjacentElement('afterend', notice);
    else d.body.append(notice);
  };

  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', render, { once: true });
  else render();
})();
