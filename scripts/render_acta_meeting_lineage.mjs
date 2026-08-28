import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const { chromium } = await import(process.env.PSR_PLAYWRIGHT_MODULE || 'playwright');

const base = (process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho').replace(/\/$/, '');
const out = process.env.PSR_SCREENSHOT_DIR || 'artifacts/acta-meeting-lineage';
const browserPath = process.env.PSR_BROWSER_PATH || undefined;
const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const manifestPath = path.resolve(scriptDir, '../evidence/community/actas/meeting-lineage-index-v1.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const expectedEventCount = 23;
const requiredRicpeIds = new Set([
  'SP-RECITAL-2021-12-29-RICPE',
  'SP-MEETING-2022-03-11-RICPE',
]);

if (!Array.isArray(manifest.events) || manifest.events.length !== expectedEventCount) {
  throw new Error(`meeting-lineage index must contain exactly ${expectedEventCount} events; found ${manifest.events?.length ?? 'no event array'}`);
}
if (manifest.controlled_event_family_count !== expectedEventCount) {
  throw new Error(`controlled_event_family_count ${manifest.controlled_event_family_count} != ${expectedEventCount}`);
}
if (!manifest.perimeters || Object.keys(manifest.perimeters).length !== 6) {
  throw new Error(`meeting-lineage index must define exactly six perimeters; found ${Object.keys(manifest.perimeters || {}).length}`);
}

const eventIds = manifest.events.map(event => event.id);
if (eventIds.some(id => typeof id !== 'string' || !id) || new Set(eventIds).size !== expectedEventCount) {
  throw new Error('meeting-lineage index event IDs must be non-empty and unique');
}
for (const id of requiredRicpeIds) {
  if (!eventIds.includes(id)) throw new Error(`meeting-lineage index is missing required RICPE event ${id}`);
}

const expectedPerimeters = Object.entries(manifest.perimeters).map(([key, value]) => ({
  key,
  code: value.code,
  label_es: value.label_es,
  label_en: value.label_en,
}));
const expectedPerimeterKeys = new Set(expectedPerimeters.map(item => item.key));
const expectedPerimeterCodes = new Set(expectedPerimeters.map(item => item.code));
if (expectedPerimeterKeys.size !== 6 || expectedPerimeterCodes.size !== 6 || expectedPerimeters.some(item => !item.code || !item.label_es || !item.label_en)) {
  throw new Error('all six perimeter definitions must have unique codes and bilingual labels');
}
if (manifest.events.some(event => !expectedPerimeterKeys.has(event.perimeter))) {
  throw new Error('one or more meeting-lineage events use an undefined perimeter');
}
if (new Set(manifest.events.map(event => event.perimeter)).size !== 6) {
  throw new Error('the controlled event corpus must exercise all six perimeter classifications');
}

function publicRoute(value, eventId, locale) {
  if (typeof value !== 'string' || !value.trim()) throw new Error(`${eventId} has no ${locale} detail route`);
  const route = value.trim().replace(/^\/+/, '').replace(/index\.html$/, '');
  return `/${route}`;
}

const roomCases = [
  {
    name: 'es-overview',
    route: '/es/comunidad-instrumentalizacion/sala-documental-actas/',
    kind: 'room',
    locale: 'es',
  },
  {
    name: 'en-overview',
    route: '/en/community-instrumentalisation/acta-document-room/',
    kind: 'room',
    locale: 'en',
  },
];

const eventCases = manifest.events.flatMap(event => ['es', 'en'].map(locale => ({
  name: `${locale}-${event.slug || event.id.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`,
  route: publicRoute(event[`detail_page_${locale}`], event.id, locale),
  kind: 'event',
  locale,
  eventId: event.id,
  perimeter: event.perimeter,
  perimeterCode: event.perimeter_code || manifest.perimeters[event.perimeter].code,
  fullSource: event.digitisation_complete_for_located_copy === true,
})));

if (eventCases.length !== expectedEventCount * 2 || new Set(eventCases.map(item => item.route)).size !== expectedEventCount * 2) {
  throw new Error(`expected ${expectedEventCount * 2} unique bilingual event routes; found ${eventCases.length}`);
}

const cases = [...roomCases, ...eventCases];
const viewports = {
  desktop: { width: 1440, height: 1000 },
  mobile: { width: 390, height: 844 },
};

fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ headless: true, ...(browserPath ? { executablePath: browserPath } : {}) });
const results = [];
const colourPairs = new Map(expectedPerimeters.map(item => [item.key, new Set()]));
let failed = false;

try {
  for (const testCase of cases) {
    for (const [device, viewport] of Object.entries(viewports)) {
      const page = await browser.newPage({ viewportSize: viewport });
      const errors = [];
      page.on('pageerror', error => errors.push(`pageerror: ${error.message}`));
      page.on('console', message => {
        if (message.type() === 'error') errors.push(`console: ${message.text()}`);
      });
      const response = await page.goto(`${base}${testCase.route}`, { waitUntil: 'networkidle' });
      if (!response || !response.ok()) errors.push(`HTTP ${response?.status() || 'no response'}`);

      if (testCase.kind === 'room') {
        try {
          await page.waitForFunction(() => {
            const state = document.querySelector('[data-acta-room]')?.dataset.manifestState;
            return state === 'ready' || state === 'unavailable';
          }, null, { timeout: 15000 });
        } catch (error) {
          errors.push(`manifest state did not settle: ${error.message}`);
        }
      }

      const metrics = testCase.kind === 'room'
        ? await page.evaluate(({ perimeterDefinitions }) => {
          const body = document.body;
          const room = document.querySelector('[data-acta-room]');
          const cards = [...(room?.querySelectorAll('[data-acta-list] .acta-record') || [])];
          const isVisible = node => {
            if (!node) return false;
            const style = getComputedStyle(node);
            const rect = node.getBoundingClientRect();
            return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
          };
          const perimeterDisplay = perimeterDefinitions.map(({ key, code }) => {
            const matchingCards = cards.filter(card => card.dataset.perimeter === key);
            const cardDisplays = matchingCards.map(card => {
              const ribbon = card.querySelector('.acta-perimeter-ribbon');
              const codeNode = ribbon?.querySelector('.acta-perimeter-code');
              const heading = ribbon?.querySelector('strong');
              const headingText = heading?.textContent?.replace(/\s+/g, ' ').trim() || '';
              const displayedCode = codeNode?.textContent?.trim() || '';
              const label = headingText.startsWith(displayedCode)
                ? headingText.slice(displayedCode.length).trim()
                : headingText;
              return {
                cardCode: card.dataset.perimeterCode || '',
                ribbonCode: ribbon?.dataset.perimeterCode || '',
                displayedCode,
                label,
                visible: isVisible(ribbon) && isVisible(codeNode) && isVisible(heading),
              };
            });
            const legendLabel = room?.querySelector(`.acta-perimeter-legend [data-perimeter="${key}"] strong`);
            return {
              key,
              expectedCode: code,
              cardCount: matchingCards.length,
              cardDisplays,
              legendLabel: legendLabel?.textContent?.replace(/\s+/g, ' ').trim() || '',
              legendVisible: isVisible(legendLabel),
            };
          });
          return {
            title: document.title,
            lang: document.documentElement.lang,
            manifestState: room?.dataset.manifestState || null,
            manifestUrl: room?.dataset.manifest || null,
            cards: cards.length,
            cardIds: cards.map(card => card.querySelector('.acta-record-id')?.textContent?.trim() || ''),
            statTotal: room?.querySelector('[data-stat-total]')?.textContent?.trim() || '',
            perimeterDisplay,
            overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
            bodyPerimeter: body.dataset.perimeter || null,
          };
        }, { perimeterDefinitions: expectedPerimeters })
        : await page.evaluate(({ expected, expectedCode, full, expectedId }) => {
          const body = document.body;
          const ribbon = document.querySelector('.acta-event-hero .acta-perimeter-ribbon');
          const codeNode = ribbon?.querySelector('.acta-perimeter-code');
          const heading = ribbon?.querySelector('strong');
          const fullText = document.querySelector('.acta-full-ocr');
          const sourcePages = document.querySelectorAll('.acta-source-gallery .acta-source-page');
          const style = ribbon ? getComputedStyle(ribbon) : null;
          const headingText = heading?.textContent?.replace(/\s+/g, ' ').trim() || '';
          const displayedCode = codeNode?.textContent?.trim() || '';
          return {
            title: document.title,
            bodyPerimeter: body.dataset.perimeter || null,
            expected,
            expectedCode,
            eventIdVisible: document.querySelector('.acta-event-hero .eyebrow')?.textContent?.includes(expectedId) || false,
            ribbon: Boolean(ribbon),
            ribbonCode: displayedCode,
            ribbonLabel: headingText.startsWith(displayedCode) ? headingText.slice(displayedCode.length).trim() : headingText,
            ribbonColour: style?.borderLeftColor || null,
            ribbonBackground: style?.backgroundColor || null,
            ocrChars: fullText?.textContent?.length || 0,
            sourcePages: sourcePages.length,
            full,
            overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
            previousNext: document.querySelectorAll('.acta-event-nav a').length,
          };
        }, {
          expected: testCase.perimeter,
          expectedCode: testCase.perimeterCode,
          full: testCase.fullSource,
          expectedId: testCase.eventId,
        });

      if (testCase.kind === 'room') {
        if (metrics.manifestState !== 'ready') errors.push(`manifest state ${metrics.manifestState || 'missing'} != ready`);
        if (!metrics.manifestUrl?.endsWith('evidence/community/actas/meeting-lineage-index-v1.json')) errors.push(`unexpected manifest URL ${metrics.manifestUrl || 'missing'}`);
        if (metrics.cards !== expectedEventCount) errors.push(`rendered cards ${metrics.cards} != ${expectedEventCount}`);
        if (metrics.statTotal !== String(expectedEventCount)) errors.push(`displayed total ${metrics.statTotal || 'missing'} != ${expectedEventCount}`);
        if (JSON.stringify(metrics.cardIds) !== JSON.stringify(eventIds)) errors.push('rendered card IDs/order do not match the meeting-lineage manifest');
        if (new Set(metrics.perimeterDisplay.map(perimeter => perimeter.legendLabel)).size !== expectedPerimeters.length) {
          errors.push('the room does not display six distinct written perimeter legend labels');
        }
        for (const perimeter of metrics.perimeterDisplay) {
          if (!perimeter.cardCount) errors.push(`perimeter ${perimeter.key} has no rendered card`);
          if (!perimeter.legendLabel || !perimeter.legendVisible) errors.push(`perimeter ${perimeter.key} has no visible written legend label`);
          for (const display of perimeter.cardDisplays) {
            if (display.cardCode !== perimeter.expectedCode) errors.push(`${perimeter.key} card code ${display.cardCode || 'missing'} != ${perimeter.expectedCode}`);
            if (display.ribbonCode !== perimeter.expectedCode) errors.push(`${perimeter.key} ribbon data code ${display.ribbonCode || 'missing'} != ${perimeter.expectedCode}`);
            if (display.displayedCode !== perimeter.expectedCode) errors.push(`${perimeter.key} visible code ${display.displayedCode || 'missing'} != ${perimeter.expectedCode}`);
            if (!display.label) errors.push(`${perimeter.key} has no written card label`);
            if (!display.visible) errors.push(`${perimeter.key} code/label is not visibly rendered`);
          }
        }
      } else {
        if (metrics.bodyPerimeter !== testCase.perimeter) errors.push(`perimeter ${metrics.bodyPerimeter} != ${testCase.perimeter}`);
        if (!metrics.ribbon) errors.push('missing perimeter ribbon');
        if (metrics.ribbonCode !== testCase.perimeterCode) errors.push(`visible code ${metrics.ribbonCode || 'missing'} != ${testCase.perimeterCode}`);
        if (!metrics.ribbonLabel) errors.push('missing written perimeter label');
        if (!metrics.eventIdVisible) errors.push(`event ID ${testCase.eventId} not displayed in hero`);
        if (!metrics.ribbonColour || !metrics.ribbonBackground) errors.push('missing computed perimeter colour');
        if (metrics.ribbonColour && metrics.ribbonBackground) colourPairs.get(testCase.perimeter).add(`${metrics.ribbonColour}|${metrics.ribbonBackground}`);
        if (testCase.fullSource && (metrics.ocrChars < 100 || metrics.sourcePages < 1)) {
          errors.push(`incomplete embedded source layer: text ${metrics.ocrChars}; pages ${metrics.sourcePages}`);
        }
      }
      if (metrics.overflow > 2) errors.push(`horizontal overflow ${metrics.overflow}px`);

      const target = testCase.kind === 'event' ? page.locator('.acta-event-hero') : page.locator('main').first();
      await target.screenshot({ path: path.join(out, `${testCase.name}-${device}.png`) });
      results.push({ name: testCase.name, route: testCase.route, device, metrics, errors });
      if (errors.length) failed = true;
      await page.close();
    }
  }
} finally {
  await browser.close();
}

const canonicalColours = new Map();
for (const [perimeter, pairs] of colourPairs) {
  if (pairs.size !== 1) {
    failed = true;
    results.push({ name: 'colour-consistency', errors: [`${perimeter} rendered with ${pairs.size} colour pairs instead of one`] });
  } else canonicalColours.set(perimeter, [...pairs][0]);
}
if (new Set(canonicalColours.values()).size !== expectedPerimeters.length) {
  failed = true;
  results.push({ name: 'colour-distinction', errors: ['two or more perimeter lanes share the same rendered colour pair'] });
}

fs.writeFileSync(path.join(out, 'result.json'), JSON.stringify({
  base,
  manifest: 'evidence/community/actas/meeting-lineage-index-v1.json',
  controlledEvents: expectedEventCount,
  bilingualEventRoutes: eventCases.length,
  roomRoutes: roomCases.length,
  colours: Object.fromEntries(canonicalColours),
  results,
}, null, 2));
if (failed) {
  console.error('ACTA rendered lineage validation failed');
  for (const item of results.filter(item => item.errors?.length)) console.error(item.name, item.device || '', item.errors.join('; '));
  process.exit(1);
}
console.log(`ACTA rendered lineage validation: PASS (${results.length} route/viewport checks; ${eventCases.length} bilingual event routes; ${canonicalColours.size} distinct lanes)`);
