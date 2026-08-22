from __future__ import annotations

from pathlib import Path
from textwrap import dedent
import os

ROOT = Path(__file__).resolve().parents[1]
STAMP = "2026-08-20"
MARKER = "SOURCE-OF-FUNDS-NOTICE-20260820"

LOADER_JS = dedent(r'''

/* SOURCE-OF-FUNDS-NOTICE-20260820 */
(() => {
  const current = document.currentScript;
  const base = current && current.src ? new URL('.', current.src) : new URL('/assets/', location.href);
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const exact = new Map([
    ['/es/', ['full', '#historia-reconstruida', 'after']],
    ['/en/', ['full', null, 'append']],
    ['/es/ric-private-equity-sun-park/', ['full', '#respuesta', 'before']],
    ['/en/ric-private-equity-sun-park/', ['full', '#response', 'before']],
    ['/es/mismo-hotel-multiples-vidas-financieras/', ['full', null, 'append']],
    ['/en/same-hotel-multiple-financial-lives/', ['full', null, 'append']],
    ['/es/acosta-matos-perimetro/', ['full', null, 'append']],
    ['/en/acosta-matos-perimeter/', ['full', null, 'append']],
    ['/es/objetivos-recuperacion-restitucion/', ['full', '#vias', 'before']],
    ['/en/recovery-restitution-objectives/', ['full', null, 'append']],
    ['/es/cadena-instrumentalizacion-ric-fondos-incentivos/', ['full', null, 'append']],
    ['/en/institutionalisation-chain-ric-eu-incentives/', ['full', null, 'append']],
    ['/es/ricpe-responsabilidad-documental/', ['compact', null, 'append']],
    ['/en/ricpe-documentary-accountability/', ['compact', null, 'append']],
    ['/es/pwc-canarias-carlos-saavedra-sun-park/', ['compact', null, 'append']],
    ['/en/pwc-canarias-carlos-saavedra-sun-park/', ['compact', null, 'append']],
    ['/es/rsm/nnr4-1025c2f66/', ['compact', null, 'append']],
    ['/en/rsm/nnr4-1025c2f66/', ['compact', null, 'append']],
    ['/es/grant-thornton/cuyas-canarias/', ['compact', null, 'append']],
    ['/en/grant-thornton/cuyas-canarias/', ['compact', null, 'append']],
    ['/es/grant-thornton/2024-04/', ['compact', null, 'append']],
    ['/en/grant-thornton/2024-04/', ['compact', null, 'append']],
    ['/es/actores-partes-abogados-representantes/', ['compact', null, 'append']],
    ['/en/actors-parties-lawyers-representatives/', ['compact', null, 'append']],
    ['/es/san-telmo-ricpe-sun-park/', ['compact', null, 'append']],
    ['/en/san-telmo-ricpe-sun-park/', ['compact', null, 'append']]
  ]);
  const match = [...exact.entries()].find(([suffix]) => path.endsWith(suffix));
  if (!match || document.querySelector('[data-source-of-funds-notice]')) return;

  const [variant, selector, position] = match[1];
  const section = document.createElement('section');
  section.className = 'section source-funds-notice-section';
  section.setAttribute('aria-label', document.documentElement.lang === 'en'
    ? 'Source of funds and professional services notice'
    : 'Aviso sobre procedencia de fondos y servicios profesionales');
  const shell = document.createElement('div');
  shell.className = 'shell';
  const mount = document.createElement('div');
  mount.dataset.sourceOfFundsNotice = variant;
  shell.append(mount);
  section.append(shell);

  const anchor = selector ? document.querySelector(selector) : null;
  const main = document.querySelector('main');
  if (!main) return;
  if (anchor && position === 'before') anchor.insertAdjacentElement('beforebegin', section);
  else if (anchor && position === 'after') anchor.insertAdjacentElement('afterend', section);
  else main.append(section);

  const component = document.createElement('script');
  component.src = new URL('source-of-funds-notice-20260820.js?v=20260822b', base).href;
  component.dataset.sourceFundsComponent = '20260820';
  document.head.append(component);
})();
''')

TARGETS = [
    'es/index.html', 'en/index.html',
    'es/ric-private-equity-sun-park/index.html', 'en/ric-private-equity-sun-park/index.html',
    'es/mismo-hotel-multiples-vidas-financieras/index.html', 'en/same-hotel-multiple-financial-lives/index.html',
    'es/acosta-matos-perimetro/index.html', 'en/acosta-matos-perimeter/index.html',
    'es/objetivos-recuperacion-restitucion/index.html', 'en/recovery-restitution-objectives/index.html',
    'es/cadena-instrumentalizacion-ric-fondos-incentivos/index.html', 'en/institutionalisation-chain-ric-eu-incentives/index.html',
    'es/ricpe-responsabilidad-documental/index.html', 'en/ricpe-documentary-accountability/index.html',
    'es/pwc-canarias-carlos-saavedra-sun-park/index.html', 'en/pwc-canarias-carlos-saavedra-sun-park/index.html',
    'es/rsm/nnr4-1025c2f66/index.html', 'en/rsm/nnr4-1025c2f66/index.html',
    'es/grant-thornton/cuyas-canarias/index.html', 'en/grant-thornton/cuyas-canarias/index.html',
    'es/grant-thornton/2024-04/index.html', 'en/grant-thornton/2024-04/index.html',
    'es/actores-partes-abogados-representantes/index.html', 'en/actors-parties-lawyers-representatives/index.html',
    'es/san-telmo-ricpe-sun-park/index.html', 'en/san-telmo-ricpe-sun-park/index.html',
]


def relative_site_js(path: Path) -> str:
    return os.path.relpath(ROOT / 'assets/site.js', path.parent).replace(os.sep, '/')


def ensure_target_loader(relative: str) -> None:
    path = ROOT / relative
    if not path.exists():
        raise FileNotFoundError(relative)
    content = path.read_text(encoding='utf-8')
    if '<main' not in content.lower():
        raise RuntimeError(f'{relative}: missing <main>')
    if 'site.js' not in content:
        tag = f'<script src="{relative_site_js(path)}" defer></script>'
        if '</head>' not in content:
            raise RuntimeError(f'{relative}: missing </head>')
        path.write_text(content.replace('</head>', f'  {tag}\n</head>', 1), encoding='utf-8')


def update_sitemap() -> None:
    path = ROOT / 'sitemap.xml'
    if not path.exists():
        return
    content = path.read_text(encoding='utf-8')
    urls = [
        'https://sbu001monterecco.github.io/por-derecho/es/aviso-procedencia-fondos-servicios-profesionales/',
        'https://sbu001monterecco.github.io/por-derecho/en/source-of-funds-professional-services-notice/',
    ]
    additions = [f'  <url><loc>{url}</loc><lastmod>{STAMP}</lastmod></url>' for url in urls if url not in content]
    if additions:
        if '</urlset>' not in content:
            raise RuntimeError('sitemap.xml: missing </urlset>')
        path.write_text(content.replace('</urlset>', '\n'.join(additions) + '\n</urlset>', 1), encoding='utf-8')


def validate() -> None:
    site = (ROOT / 'assets/site.js').read_text(encoding='utf-8')
    assert site.count(MARKER) == 1
    assert site.count('source-of-funds-notice-20260820.js') == 1
    assert len(TARGETS) == 26
    for relative in TARGETS:
        assert 'site.js' in (ROOT / relative).read_text(encoding='utf-8'), relative
    required = [
        'assets/source-of-funds-notice-20260820.css',
        'assets/source-of-funds-notice-20260820.js',
        'es/aviso-procedencia-fondos-servicios-profesionales/index.html',
        'en/source-of-funds-professional-services-notice/index.html',
        'assets/por-derecho/second-pair-eyes.svg',
    ]
    for relative in required:
        assert (ROOT / relative).exists(), relative
    component = (ROOT / 'assets/source-of-funds-notice-20260820.js').read_text(encoding='utf-8')
    assert 'not an allegation of wrongdoing' in component
    assert 'no una acusación de irregularidad' in component
    assert "scopeAnchor: 'scope'" in component


def main() -> None:
    site_path = ROOT / 'assets/site.js'
    site = site_path.read_text(encoding='utf-8')
    if MARKER not in site:
        site_path.write_text(site.rstrip() + '\n' + LOADER_JS, encoding='utf-8')
    for target in TARGETS:
        ensure_target_loader(target)
    update_sitemap()
    validate()
    print(f'Applied {MARKER} to {len(TARGETS)} target pages plus two canonical notice pages.')


if __name__ == '__main__':
    main()
