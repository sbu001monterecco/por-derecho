# DEPLOYMENT LOG

Use after every merged public-site change. A merge to `main` is not itself proof that GitHub Pages has published the revision.

| Date (UTC) | PR | Merge commit | Pages build/status | Critical verification | Notes |
|---|---:|---|---|---|---|
| 2026-08-15 | #83 | `01fe71a82cd2f1e2be932378ca375d640416b1b4` | GitHub Pages run 31905715225 — **completed / success**; created 20:05:00Z, completed 20:05:26Z | six existing locked JPG paths replaced with clean square derivatives made from the approved locked masters; six versioned `-v2.jpg` recovery/cache-busting copies also present; no HTML/manuscript/evidential content changed | Corrects the defective tiny binaries deployed earlier. Existing EN/ES `<img>` and static OG URLs continue to resolve at the same filenames, now to the clean artwork. |
| 2026-08-15 | #82 | `3882780702b9df312a197706f4a4483360de6765` | GitHub Pages run 31904879003 — **completed / success**; completed 19:47:14Z | `assets/book-pages-20260815.css` verified on `main`: square aspect ratio, `object-fit: contain`, no desaturation/filter, no dark overlay, no duplicate title overlay on portfolio cards | Corrects rendering that had forced square approved artwork into 2:3 portrait crops and altered the locked visual appearance. |
| 2026-08-15 | #80 | `75b1e7b5e41a0746bce77991be50670c31742e8c` | GitHub Pages build 1153592223 — **built**, no error; created 19:37:07Z, completed 19:37:29Z | `main` ref verified at exact merge commit; source paths verified for new ES/EN recovery/restitution objectives hub, canonical recovery doctrine, recovery causation matrix and revised ES/EN institutional-accountability hubs | External route retrieval was unavailable in the execution environment immediately after deployment, so URL-level content retrieval was not independently completed. Pages API confirms successful build of the exact merge commit. Public framing is recovery first, accountability in service of recovery, and no new finding of corruption, collusion, prevaricación, falsification or criminal intent. |
| 2026-08-15 | #75 | `1571c80d83be6c078fee1459b95c49cdb39e6c9a` | GitHub Pages build 1153540993 — **built**, no error; created 19:01:25Z, completed 19:01:49Z | `main` ref verified at exact merge commit; source paths verified for new ES/EN RIC→regional-incentives→EU institutionalisation hub and upgraded RICPE/SNCA/accountability pages | External search/index retrieval had not yet discovered the newly created Pages routes immediately after deployment; Pages API independently confirms successful build of the exact content commit. Public content frames LPB concursal + Matkator/third-party extraconcursal + Aweswell cross-border consequences as ongoing/remediable, not merely historical; RIC/subsidy/EU layers remain distinct and no fraud/double-funding finding is made. |
| 2026-08-15 | #51 | `6ee7d2fe3400f26f721062eefcb76e5a9732d771` | GitHub Pages build 1153119307 — **built**, no error | fresh publish forced after CNMV primary-source update | deployment-marker only; no substantive public content change |
| 2026-08-15 | #50 | `b1fafe442e0f2795ad0ebe3ea21db28e5aef8e4d` | superseded by #51 forced refresh | CNMV source on `main` verified | primary-source chronology upgrade |

## Required deployment procedure
1. identify merged PR and exact merge commit;
2. verify the intended files on `main`;
3. inspect GitHub Pages latest-build endpoint/status;
4. require `built` and no error before calling deployment confirmed;
5. test high-value public URLs where external retrieval is available;
6. record any cache/deployment-marker action;
7. append this log.

If Pages status cannot be checked, say **source merged / public deployment not independently verified** rather than assuming success.