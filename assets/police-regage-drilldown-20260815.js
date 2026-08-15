(() => {
  const run = () => {
    const lang = document.documentElement.lang === 'en' ? 'en' : 'es';
    if (document.getElementById('police-regage-drilldown-20260815')) return;

    const parent = document.getElementById('police-evidence-preservation-20260815');
    if (!parent) return;

    const gc = [
      ['REGAGE26e00004131045','17/01/2026 21:39:58','AMPLIACIÓN DENUNCIA – PRESERVACIÓN PROBATORIA Y DELITOS ECONÓMICOS SUN PARK','Received'],
      ['REGAGE26e00003979568','16/01/2026 16:33:06','Solicitud urgente de aseguramiento probatorio – Hotel Sun Park / RIC','Received'],
      ['REGAGE26e00003912926','16/01/2026 12:44:45','Solicitud urgente de actuaciones y preservación probatoria – Operación “Sun Park”','Received'],
      ['REGAGE26e00003640214','15/01/2026 21:19:29','Preservación probatoria por contradicciones económicas – Concurso 36/2012','Received'],
      ['REGAGE26e00003630632','15/01/2026 20:13:50','Solicitud de preservación probatoria – comercialización Sun Park / Club Sei','Received'],
      ['REGAGE26e00003610147','15/01/2026 18:16:23','Preservación probatoria urgente – conversación marzo 2018 / Sun Park','Received'],
      ['REGAGE26e00003497566','15/01/2026 12:38:34','Solicitud urgente de preservacion probatoria – comercializacion Sun Park','Received'],
      ['REGAGE26e00003039101','14/01/2026 10:18:30','Denuncia penal y preservación probatoria – delitos económicos complejos','Received'],
      ['REGAGE26e00000915939','06/01/2026 21:06:22','Denuncia penal – Explotación económica continuada sin título jurídico (delito económico…)','Received'],
      ['REGAGE26e00000559233','04/01/2026 22:12:23','Denuncia penal – Acta 2022 Sun Park (posible falsedad documental y estafa)','Received']
    ];

    const pn = [
      ['REGAGE26e00003914995','16/01/2026 12:48:15','Solicitud urgente de actuaciones policiales y preservación probatoria – Operación…','Received'],
      ['REGAGE26e00003640595','15/01/2026 21:23:21','Preservación probatoria por indicios económicos graves – Hotel Sun Park','Rejected'],
      ['REGAGE26e00003632107','15/01/2026 20:23:16','Solicitud de aseguramiento probatorio – explotación hotelera Sun Park / Club Sei…','Rejected'],
      ['REGAGE26e00003610577','15/01/2026 18:19:12','Preservación probatoria urgente – conversación marzo 2018 / Sun Park','Rejected'],
      ['REGAGE26e00003499270','15/01/2026 12:42:29','Solicitud urgente de preservacion probatoria – Sun Park / Club Sei','Rejected'],
      ['REGAGE26e00003042124','14/01/2026 10:24:47','Denuncia penal y preservación probatoria – delitos económicos complejos','Received'],
      ['REGAGE26e00000916504','06/01/2026 21:13:49','Denuncia penal – Explotación económica continuada sin título habilitante','Received'],
      ['REGAGE26e00000559552','04/01/2026 22:21:15','Puesta en conocimiento – indicios de falsedad documental y fraude económico (ACT…)','Received']
    ];

    const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    const status = (s) => lang === 'es' ? (s === 'Received' ? 'Recibido' : 'Rechazado') : s;
    const rows = (items) => items.map(([id,date,subject,state]) => `
      <tr>
        <td><code>${esc(id)}</code></td>
        <td>${esc(date)}</td>
        <td>${esc(subject)}</td>
        <td><strong>${esc(status(state))}</strong></td>
      </tr>`).join('');

    const section = document.createElement('section');
    section.id = 'police-regage-drilldown-20260815';
    section.style.marginTop = '1.5rem';
    section.innerHTML = lang === 'es' ? `
      <details open>
        <summary><strong>Rastro REGAGE individual · 18 registros</strong></summary>
        <div class="source-policy" style="margin:1rem 0">La tabla reproduce los números, fechas, asuntos y estados mostrados en el listado registral facilitado. Cuando el asunto aparecía truncado en el listado, se conserva la elipsis en vez de completar texto no verificado. «Recibido» describe únicamente el estado registral.</div>
        <h4>Guardia Civil — Comandancia de Las Palmas · 10/10 recibidos</h4>
        <div style="overflow-x:auto"><table class="evidence-table"><thead><tr><th>Registro</th><th>Presentación</th><th>Asunto</th><th>Estado</th></tr></thead><tbody>${rows(gc)}</tbody></table></div>
        <h4 style="margin-top:1.5rem">Policía Nacional — Comisaría Provincial de Las Palmas · 4 recibidos / 4 rechazados</h4>
        <div style="overflow-x:auto"><table class="evidence-table"><thead><tr><th>Registro</th><th>Presentación</th><th>Asunto</th><th>Estado</th></tr></thead><tbody>${rows(pn)}</tbody></table></div>
        <p class="source-policy" style="margin-top:1rem"><strong>Límite probatorio:</strong> estos asientos acreditan presentación y estado registral; por sí solos no acreditan investigación, diligencias policiales, preservación efectiva, remisión, archivo ni aceptación de los hechos denunciados.</p>
      </details>` : `
      <details open>
        <summary><strong>Individual REGAGE trail · 18 records</strong></summary>
        <div class="source-policy" style="margin:1rem 0">The table reproduces the registration numbers, dates, subjects and statuses shown in the supplied registry listing. Where a subject was truncated in that listing, the ellipsis is preserved rather than completing unverified wording. “Received” describes registration status only.</div>
        <h4>Guardia Civil — Las Palmas Command · 10/10 received</h4>
        <div style="overflow-x:auto"><table class="evidence-table"><thead><tr><th>Registration</th><th>Presented</th><th>Official subject</th><th>Status</th></tr></thead><tbody>${rows(gc)}</tbody></table></div>
        <h4 style="margin-top:1.5rem">Policía Nacional — Las Palmas Provincial Police Station · 4 received / 4 rejected</h4>
        <div style="overflow-x:auto"><table class="evidence-table"><thead><tr><th>Registration</th><th>Presented</th><th>Official subject</th><th>Status</th></tr></thead><tbody>${rows(pn)}</tbody></table></div>
        <p class="source-policy" style="margin-top:1rem"><strong>Evidential limit:</strong> these entries establish submission and registration status only; standing alone they do not establish an investigation, police proceedings, actual evidence preservation, referral, closure or acceptance of the allegations.</p>
      </details>`;

    parent.appendChild(section);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
})();
