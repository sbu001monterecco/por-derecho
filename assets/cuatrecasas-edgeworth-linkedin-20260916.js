(() => {
  'use strict';

  const cleanPath = location.pathname.replace(/index\.html$/, '').replace(/\/+$/, '/');
  const routes = new Set([
    '/por-derecho/en/',
    '/por-derecho/en/cuatrecasas-sun-park/'
  ]);
  if (!routes.has(cleanPath)) return;
  if (document.getElementById('cuatrecasas-edgeworth-publication')) return;

  const styleId = 'pd-cuatrecasas-edgeworth-publication-style';
  if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
      .pd-edgeworth-publication{background:#f4f1ea;border-top:1px solid rgba(19,37,45,.10);border-bottom:1px solid rgba(19,37,45,.10)}
      .pd-edgeworth-publication .pd-edgeworth-head{max-width:70rem;margin:0 0 1.25rem}
      .pd-edgeworth-publication .pd-edgeworth-kicker{margin:0 0 .4rem;text-transform:uppercase;letter-spacing:.11em;font-size:.74rem;font-weight:800;color:#80621d}
      .pd-edgeworth-publication h2{margin:.15rem 0 .65rem;font-family:Georgia,'Times New Roman',serif;font-size:clamp(2rem,4vw,3.5rem);line-height:1.05;color:#13252d}
      .pd-edgeworth-publication .pd-edgeworth-deck{max-width:62rem;margin:0;color:#46555b;font-size:1.05rem;line-height:1.65}
      .pd-edgeworth-figure{margin:1.35rem 0 1.2rem;background:#0f252c;border-radius:20px;overflow:hidden;box-shadow:0 20px 50px rgba(15,37,44,.16)}
      .pd-edgeworth-figure img{display:block;width:100%;height:auto}
      .pd-edgeworth-figure figcaption{padding:.85rem 1rem;color:#dbe5e6;font-size:.82rem;line-height:1.55}
      .pd-edgeworth-post{max-width:66rem;background:#fff;border:1px solid #dfe3e3;border-radius:18px;padding:clamp(1rem,2.4vw,1.6rem);box-shadow:0 12px 32px rgba(19,37,45,.06)}
      .pd-edgeworth-post .pd-edgeworth-label{display:block;margin-bottom:.8rem;text-transform:uppercase;letter-spacing:.09em;font-size:.72rem;font-weight:800;color:#8c2f2c}
      .pd-edgeworth-post p{margin:.75rem 0;line-height:1.7;color:#27373d}
      .pd-edgeworth-post .pd-edgeworth-question{font-family:Georgia,'Times New Roman',serif;font-size:1.35rem;line-height:1.45;color:#13252d}
      .pd-edgeworth-post .pd-edgeworth-headline{font-weight:900;letter-spacing:.025em;color:#8c2f2c}
      .pd-edgeworth-actions{display:flex;gap:.7rem;flex-wrap:wrap;margin:1rem 0}
      .pd-edgeworth-boundary{max-width:66rem;margin:.8rem 0 0;padding-left:1rem;border-left:4px solid #80621d;color:#56656b;font-size:.88rem;line-height:1.6}
      @media(max-width:650px){.pd-edgeworth-publication h2{font-size:2rem}.pd-edgeworth-post .pd-edgeworth-question{font-size:1.15rem}.pd-edgeworth-figure{border-radius:12px}}
    `;
    document.head.appendChild(style);
  }

  const section = document.createElement('section');
  section.className = 'section pd-edgeworth-publication';
  section.id = 'cuatrecasas-edgeworth-publication';
  section.setAttribute('aria-labelledby', 'cuatrecasas-edgeworth-publication-title');
  section.innerHTML = `
    <div class="shell">
      <header class="pd-edgeworth-head">
        <p class="pd-edgeworth-kicker">Current professional-accountability publication · 16 September 2026</p>
        <h2 id="cuatrecasas-edgeworth-publication-title">One firm. Two high-value clients. One repeated question.</h2>
        <p class="pd-edgeworth-deck">A documentary comparison between the public Edgeworth Capital proceedings and the independently preserved Aweswell / Sun Rock record concerning the handling of 2019 Spanish Supreme Court insolvency jurisprudence.</p>
      </header>

      <figure class="pd-edgeworth-figure">
        <img src="/por-derecho/assets/cuatrecasas-edgeworth-one-repeated-question-20260916.webp" width="800" height="450" loading="eager" decoding="async" alt="Editorial comparison graphic: Robert Tchenguiz and Edgeworth Capital on the left, Gil Marer and Aweswell / Sun Rock on the right, with Cuatrecasas, its Madrid and London offices, and STS 112/2019 connecting the two matters.">
        <figcaption><strong>Editorial graphic.</strong> It summarises the comparison; it is not primary evidence. The underlying judgments, correspondence and procedural sources are controlled separately.</figcaption>
      </figure>

      <article class="pd-edgeworth-post" aria-label="LinkedIn post text">
        <span class="pd-edgeworth-label">LinkedIn post text</span>
        <p>Robert Tchenguiz and Edgeworth Capital have put a €213m professional-negligence claim before the English High Court. Cuatrecasas denies the claim and liability has not been determined.</p>
        <p>Our independent documentary record does not prove Edgeworth's case. But it reveals a striking overlap.</p>
        <p>The public Edgeworth claim concerns, among other things, an alleged failure to advise on the effect of two 2019 Spanish Supreme Court decisions: <strong>STS 112/2019</strong> and <strong>STS 227/2019</strong>.</p>
        <p>In the Sun Rock record, Aweswell itself sent <strong>STS 112/2019</strong> directly to Cuatrecasas on <strong>31 May 2019</strong>, explained the insolvency-interest consequence, and Cuatrecasas acknowledged that the clarification was important.</p>
        <p>So the comparison is precise: Edgeworth alleges that critical Supreme Court law was not properly advised before a decisive transaction. Sun Rock alleges that one of those same judgments was actually put into Cuatrecasas's hands, its economic significance explained, but the protection still did not follow through effectively.</p>
        <p class="pd-edgeworth-question"><strong>When critical Spanish Supreme Court law was available, did Cuatrecasas repeatedly fail to convert that knowledge into effective protection of client value?</strong></p>
        <p class="pd-edgeworth-headline">ONE FIRM. TWO HIGH-VALUE CLIENTS. ONE REPEATED QUESTION.</p>
        <p>The two matters are separate and contested. The Edgeworth claim remains unadjudicated on the merits. The Sun Rock / Aweswell allegations remain subject to forensic and judicial determination. Evidence and right of reply remain open.</p>
      </article>

      <div class="pd-edgeworth-actions">
        <a class="button" href="/por-derecho/en/cuatrecasas-edgeworth-comparator/">Open the Edgeworth comparator and sources →</a>
        <a class="button secondary" href="/por-derecho/en/cuatrecasas-sun-park/">Open the Cuatrecasas / Sun Park record →</a>
      </div>
      <p class="pd-edgeworth-boundary"><strong>Website evidence boundary:</strong> this section preserves the publication text and its underlying comparison without converting either claimant's allegations into a finding. Cuatrecasas denies the Edgeworth claim; no merits determination is asserted. The Sun Rock / Aweswell position remains an attributed allegation. The graphic is editorial and the source record remains controlling.</p>
    </div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector(':scope > section.hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();
