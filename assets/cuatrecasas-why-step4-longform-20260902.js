(() => {
  const path = window.location.pathname.replace(/\/+$/, '');
  if (!path.includes('/en/cuatrecasas-sun-park')) return;
  if (document.querySelector('[data-cuatrecasas-why-step4="20260902"]')) return;

  const section = document.createElement('section');
  section.className = 'section alt';
  section.setAttribute('data-cuatrecasas-why-step4', '20260902');
  section.innerHTML = `
  <div class="shell" style="max-width:1160px">
    <div style="background:#fff;border:1px solid #d9dfdf;border-radius:22px;padding:clamp(1.1rem,3vw,2rem);box-shadow:0 16px 36px rgba(16,39,47,.09)">
      <p style="margin:0 0 .35rem;color:#80621d;font-size:.78rem;font-weight:900;letter-spacing:.06em;text-transform:uppercase">MANDATE → PAYMENT ROUTES → ENFORCEMENT</p>
      <h2 style="font-size:clamp(2rem,5vw,4rem);line-height:1;margin:.25rem 0 .55rem;color:#13252d">Why go straight to Step 4?</h2>
      <p style="font-size:1.08rem;line-height:1.6;max-width:960px">Cuatrecasas publicly presents itself as a leading adviser in restructuring, insolvency and special situations, including distressed M&amp;A, NPL/REO, credit bidding, loan-to-own strategies and enforcement. Against that market positioning, the controlled Sun Park record raises a simple evidential question about the route used to recover professional fees.</p>

      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:.8rem;margin:1.25rem 0">
        <article style="border:1px solid #d9dfdf;border-radius:16px;padding:1rem;background:#f7f8f8;opacity:.82"><strong style="display:block;font-size:1.2rem">1 · Demand payment from the mandating client?</strong><p>Aweswell / UK client.</p><span style="display:inline-block;background:#e5e7e8;border-radius:999px;padding:.3rem .55rem;font-size:.78rem;font-weight:800">Not evidenced in the record presently located</span></article>
        <article style="border:1px solid #d9dfdf;border-radius:16px;padding:1rem;background:#f7f8f8;opacity:.82"><strong style="display:block;font-size:1.2rem">2 · Seek payment through LPB Concurso 36/2012?</strong><p>Las Palmas insolvency route.</p><span style="display:inline-block;background:#e5e7e8;border-radius:999px;padding:.3rem .55rem;font-size:.78rem;font-weight:800">Not evidenced as the payment route used</span></article>
        <article style="border:1px solid #d9dfdf;border-radius:16px;padding:1rem;background:#f7f8f8;opacity:.82"><strong style="display:block;font-size:1.2rem">3 · Seek payment through the open hotel?</strong><p>Operating hotel / recovery structure.</p><span style="display:inline-block;background:#e5e7e8;border-radius:999px;padding:.3rem .55rem;font-size:.78rem;font-weight:800">Not evidenced in the record presently located</span></article>
        <article style="border:2px solid #8c2f2c;border-radius:16px;padding:1rem;background:#fff7f5"><strong style="display:block;font-size:1.2rem;color:#8c2f2c">4 · Execute against Matkator?</strong><p>ETJ 163/2020 → remate / adjudication request.</p><span style="display:inline-block;background:#8c2f2c;color:#fff;border-radius:999px;padding:.3rem .55rem;font-size:.78rem;font-weight:800">Route actually used</span></article>
      </div>

      <div style="background:#13252d;color:#fff;border-radius:17px;padding:1rem 1.1rem;margin:1.1rem 0"><strong style="display:block;color:#f1d37e;margin-bottom:.35rem">The visual question</strong><span style="font-size:1.08rem;line-height:1.55">Why jump straight to Step 4? The client-side theory is that fee instruments appear to have been treated more like a first-demand enforcement route than a last-resort guarantee. That is an analytical proposition, not an adjudicated fact.</span></div>

      <p>The fees arose from the wider Sun Park mandate. The mandating UK client was Aweswell. The controlled record shows Cuatrecasas understanding Aweswell as the 100% owner of Luchy and Matkator. A November 2018 Cuatrecasas email records that the promissory notes were delivered to cover pending invoices and existing incurred costs while the firm continued assisting as financing and the insolvency position were being resolved.</p>

      <p>The current remate concerns <strong>one property only: finca registral 8,584</strong>. But the executed debtor is <strong>Matkator, S.L.</strong> That distinction matters. Subject always to the execution order, the outstanding balance, proportionality and the rules governing attachment, a monetary enforcement against Matkator may potentially reach other legally attachable patrimonial assets or rights of Matkator. It does not automatically expose Aweswell's separate assets.</p>

      <p>Matkator is nevertheless the wholly owned subsidiary of the UK client whose wider hotel position Cuatrecasas had been retained to assist. Depletion of Matkator can therefore diminish the value, security pool, claims and recovery capacity within Aweswell's investment perimeter even without any automatic veil-piercing.</p>

      <h3 style="margin-top:1.4rem">That is why the repository uses the term <em>mandate inversion</em>.</h3>
      <p>A firm retained and paid to help protect, finance and recover a client's hotel position later used fee-derived instruments in an enforcement capable of removing value from a subsidiary forming part of that same recovery perimeter. In June 2019, Cuatrecasas itself identified Matkator's free assets as assets potentially capable of supporting the rescue financing.</p>

      <p>The question is therefore not simply: <strong>“Was Cuatrecasas entitled to collect unpaid fees?”</strong></p>
      <p style="font-size:1.18rem;font-weight:800;line-height:1.45;color:#13252d">The question is: how did instruments delivered in the context of paying professional fees become the route by which the professional adviser could attack the patrimonial base it had previously understood as part of the client's rescue architecture?</p>

      <p><strong>And why Step 4 first?</strong></p>

      <p>If Steps 1, 2 or 3 did in fact occur, the documentary questions are finite:</p>
      <ul style="columns:2;column-gap:2rem;line-height:1.6">
        <li>Show the demand to Aweswell.</li>
        <li>Show the invoice-by-invoice client allocation.</li>
        <li>Show the reconciliation between Aweswell, LPB and Matkator.</li>
        <li>Show the payment demands.</li>
        <li>Show the complete pagaré accounting.</li>
        <li>Show the current ETJ balance.</li>
        <li>Explain why Matkator was selected as debtor.</li>
        <li>Explain the decision to seek adjudication at 70%.</li>
        <li>Explain the reservation of the right to cede the remate to a third party.</li>
      </ul>

      <p>This does not exist in isolation. By March 2021 Cuatrecasas had also been directly supplied with Sun Park / RIC Private Equity / CNMV warning material. Further institutional warnings followed. The resulting question is therefore one of <strong>mandate, knowledge, professional responsibility, enforcement, conflicts, asset preservation and who ultimately bears the economic consequences</strong>.</p>

      <p>Cuatrecasas knows the distressed, restructuring and special-situations market exceptionally well. Its own public marketing makes that clear. That is precisely why <strong>“Why did you go straight to Step 4?”</strong> deserves a documented answer.</p>

      <div style="border-left:6px solid #80621d;background:#fff8e8;border-radius:14px;padding:1rem 1.1rem;margin-top:1.15rem"><strong>Publication boundary.</strong> Facts, inferences and allegations remain separate. The present record does not prove that Cuatrecasas acted for CAM/HNT, does not prove a completed cession of the remate to any identified third party, and does not convert Aweswell automatically into an executed debtor. Useful historical legal work is not erased merely because later conduct is disputed; equally, useful work does not immunise later conduct from separate contractual, professional or deontological scrutiny.</div>

      <p style="margin:1.1rem 0 0"><a href="../cuatrecasas-mandate-ric-continuity/" style="display:inline-block;background:#13252d;color:#fff;text-decoration:none;font-weight:800;border-radius:999px;padding:.65rem .95rem">Open the mandate → Matkator → RIC/CNMV bridge →</a></p>
    </div>
  </div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const anchor = main.querySelector('[data-cuatrecasas-mandate-ric-inbound="20260902"]');
  if (anchor && anchor.nextSibling) main.insertBefore(section, anchor.nextSibling);
  else {
    const first = main.querySelector('section');
    if (first && first.nextSibling) main.insertBefore(section, first.nextSibling);
    else main.prepend(section);
  }
})();
