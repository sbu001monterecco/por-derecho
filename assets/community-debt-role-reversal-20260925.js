(() => {
  const p=location.pathname.replace(/\/index\.html$/i,'').replace(/\/+$/,'');
  const es=/\/es\//.test(p);
  const ok=[
    /\/en\/community-instrumentalisation$/,
    /\/es\/comunidad-instrumentalizacion$/,
    /\/en\/community-instrumentalisation\/minutes-2011-2022$/,
    /\/es\/comunidad-instrumentalizacion\/actas-2011-2022$/,
    /\/en\/insolvency-classification-parallel-lives$/,
    /\/es\/calificacion-concurso-36-2012-vidas-paralelas$/
  ].some(r=>r.test(p));
  if(!ok||document.querySelector('[data-community-role-reversal]'))return;
  const t=es?{
    k:'INVERSIÓN DE ROLES · MECANISMO DOCUMENTADO · RESPONSABILIDAD ABIERTA',
    h:'La deuda que excluyó el voto mayoritario debe auditarse antes de asignar culpabilidad.',
    a:'El registro obliga a reconstruir primero la validez económica y jurídica de la deuda/morosidad utilizada para filtrar el voto de LPB y sus efectos posteriores.',
    f:'ACTA 26-04-2016: LPB 72,976% de participación; sólo 11,039% tratado como voto habilitado; cuentas 2010–2015 incompletas y no aprobadas; reducción de cuota aprox. €171,89→€22,26 con efecto retroactivo; la morosidad cae considerablemente antes de nuevas decisiones de certificación/cobro y gobierno.',
    n:'El escrito del AC de septiembre de 2026 reproduce el email de Gil de 29-04-2016 y fija aviso directo de una controversia concreta sobre deuda, morosidad, contabilidad y gastos comunes pagados por explotadoras. Aviso no equivale a prueba de falsedad.',
    r:'La posición atribuida de Gil/AWESWELL es que la causalidad debe examinarse en sentido inverso: si la contabilidad transacción por transacción demuestra que la deuda o el filtro de morosidad carecían de base o fueron incorrectamente aplicados, la investigación debe seguir a quienes crearon, certificaron, utilizaron, habilitaron o adoptaron conscientemente el mecanismo, sin detenerse automáticamente en LPB por ser la concursada.',
    l:'Límite: la validez de la deuda, el conocimiento de cada actor, la intención y cualquier responsabilidad civil, profesional, concursal, penal o judicial requieren prueba separada. La calificación culpable formal no se traslada automáticamente a terceros.',
    test:'coste real → obligado correcto → pagador real → cargo → imputación LPB → cálculo → vencimiento → impugnación/consignación → morosidad → exclusión de voto → acuerdo/certificado → uso posterior → conocimiento → efecto → beneficiario/perjuicio → explicación contraria'
  }:{
    k:'ROLE REVERSAL · DOCUMENTED MECHANISM · ACCOUNTABILITY OPEN',
    h:'The debt that excluded the majority vote must be audited before culpability is assigned.',
    a:'The record requires reconstruction of the economic and legal validity of the debt/arrears used to filter LPB’s voting rights and its later effects before assigning causation.',
    f:'26-Apr-2016 ACTA: LPB 72.976% participation; only 11.039% treated as vote-eligible; 2010–2015 accounts incomplete and unapproved; quota reduced about €171.89→€22.26 retroactively; arrears then fall considerably before further certification/recovery and governance decisions.',
    n:'The AC’s September-2026 opposition reproduces Gil’s 29-Apr-2016 email and fixes direct notice of a concrete dispute over debt, arrears, accounting and operator-paid common costs. Notice is not proof that the debt was false.',
    r:'Gil/AWESWELL’s attributed position is that causation must also be tested in reverse: if transaction-level accounting establishes that the debt or arrears filter lacked a valid basis or was wrongly applied, the inquiry should follow those who created, certified, used, enabled or knowingly adopted the mechanism, rather than stopping automatically with LPB merely because it was the insolvency debtor.',
    l:'Boundary: debt validity, each actor’s knowledge, intent and any civil, professional, insolvency, criminal or judicial responsibility require separate proof. Formal culpable classification is not automatically transferred to third parties.',
    test:'actual cost → proper payer → actual payer → charge → LPB allocation → calculation → due date → challenge/consignation → arrears → vote exclusion → resolution/certificate → later use → knowledge → effect → beneficiary/harm → contrary explanation'
  };
  const st=document.createElement('style');
  st.textContent='.pd-role-reversal{padding:42px 0;background:#f4efe6;border-block:1px solid rgba(19,37,45,.16)}.pd-role-reversal .rrb{width:min(1120px,calc(100% - 36px));margin:auto;background:#fff;border:2px solid #13252d;border-radius:20px;padding:clamp(20px,3vw,34px)}.rrb-k{font-size:.76rem;letter-spacing:.08em;text-transform:uppercase;font-weight:900;color:#8a5b22}.rrb h2{font:clamp(1.65rem,3vw,2.65rem)/1.08 Georgia,serif;margin:.35rem 0 1rem}.rrb-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.rrb-card{border:1px solid rgba(19,37,45,.18);border-radius:14px;padding:16px;background:#fafafa}.rrb-thesis{margin:16px 0;border-left:6px solid #8a5b22;background:#f8f2e7;border-radius:12px;padding:16px}.rrb-limit{border-left:5px solid #315c7b;background:#eef4f7;padding:13px 15px;border-radius:10px}.rrb-test{background:#13252d;color:#fff;border-radius:12px;padding:14px;font:13px/1.55 ui-monospace,monospace;overflow-wrap:anywhere}@media(max-width:760px){.rrb-grid{grid-template-columns:1fr}}';
  document.head.appendChild(st);
  const s=document.createElement('section');
  s.className='pd-role-reversal';
  s.dataset.communityRoleReversal='PD-COMMUNITY-DEBT-ROLE-REVERSAL-20260925-01';
  s.innerHTML='<div class="rrb"><p class="rrb-k">'+t.k+'</p><h2>'+t.h+'</h2><p>'+t.a+'</p><div class="rrb-grid"><article class="rrb-card"><h3>'+(es?'Mecanismo documentado':'Documented mechanism')+'</h3><p>'+t.f+'</p></article><article class="rrb-card"><h3>'+(es?'Aviso directo al AC':'Direct notice to the AC')+'</h3><p>'+t.n+'</p></article></div><div class="rrb-thesis"><h3>'+(es?'Pregunta de inversión causal':'Causal role-reversal question')+'</h3><p>'+t.r+'</p></div><p class="rrb-limit">'+t.l+'</p><h3>'+(es?'Prueba decisiva':'Decisive test')+'</h3><div class="rrb-test">'+t.test+'</div></div>';
  const m=document.querySelector('main');if(!m)return;const first=m.querySelector(':scope > section');if(first)first.insertAdjacentElement('afterend',s);else m.prepend(s);
})();
