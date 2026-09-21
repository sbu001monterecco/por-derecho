#!/usr/bin/env node

import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(scriptDir, '..');
const base = (process.env.PSR_BASE_URL || 'https://sbu001monterecco.github.io/por-derecho').replace(/\/$/, '');
const concurrency = Number.parseInt(process.env.PSR_READBACK_CONCURRENCY || '8', 10);

const readJson = relative => JSON.parse(fs.readFileSync(path.join(repo, relative), 'utf8'));
const lineage = readJson('evidence/community/actas/meeting-lineage-index-v1.json');
const publicIndex = readJson('evidence/community/actas/public-index.json');
const resources = [];

function add(relative, category, publicPath = relative) {
  const body = fs.readFileSync(path.join(repo, relative));
  resources.push({
    path: relative,
    category,
    url: `${base}/${publicPath.replace(/^\/+/, '').replace(/index\.html$/, '')}`,
    bytes: body.length,
    sha256: crypto.createHash('sha256').update(body).digest('hex'),
  });
}

for (const event of lineage.events) {
  add(event.detail_page_es, 'event');
  add(event.detail_page_en, 'event');
}

add('es/comunidad-instrumentalizacion/sala-documental-actas/index.html', 'room');
add('en/community-instrumentalisation/acta-document-room/index.html', 'room');

for (const item of publicIndex.items) {
  add(item.public_pdf_path, 'text_pdf');
  add(item.redacted_source_facsimile, 'source_pdf');
  add(item.manifest_path, 'package_manifest');
  add(item.preview_pages[0], 'text_image');
  add(item.source_preview_pages[0], 'source_image');
}

for (const control of [
  'evidence/community/actas/meeting-lineage-index-v1.json',
  'evidence/community/actas/public-index.json',
  'evidence/community/actas/event-family-continuity-v1.json',
  'evidence/community/actas/source-family-reconciliation-v2.json',
  'publication-manifests/community-acta-document-room-20260823.json',
  'sitemap.xml',
  'assets/acta-document-room-20260822.css',
  'assets/acta-document-room-20260822.js',
  'es/comunidad-instrumentalizacion/actas-2011-2022/index.html',
  'en/community-instrumentalisation/minutes-2011-2022/index.html',
]) add(control, 'control');

if (resources.length !== 158) throw new Error(`expected 158 resources; found ${resources.length}`);

const expectedTypes = {
  event: 'text/html',
  room: 'text/html',
  text_pdf: 'application/pdf',
  source_pdf: 'application/pdf',
  package_manifest: 'application/json',
  text_image: 'image/jpeg',
  source_image: 'image/jpeg',
};

async function verify(item) {
  const response = await fetch(item.url, { cache: 'no-store', redirect: 'follow' });
  const body = Buffer.from(await response.arrayBuffer());
  const contentType = response.headers.get('content-type') || '';
  const expectedType = expectedTypes[item.category]
    || (item.path.endsWith('.json') ? 'application/json'
      : item.path.endsWith('.xml') ? 'application/xml'
        : item.path.endsWith('.css') ? 'text/css'
          : item.path.endsWith('.js') ? 'text/javascript'
            : 'text/html');
  const typeMatches = item.path.endsWith('.js')
    ? /^(?:application|text)\/javascript\b/i.test(contentType)
    : contentType.toLowerCase().includes(expectedType);
  const result = {
    ...item,
    status: response.status,
    response_url: response.url,
    response_bytes: body.length,
    response_sha256: crypto.createHash('sha256').update(body).digest('hex'),
    content_type: contentType,
  };
  result.ok = result.status === 200
    && result.response_bytes === item.bytes
    && result.response_sha256 === item.sha256
    && typeMatches;
  return result;
}

const results = new Array(resources.length);
let cursor = 0;
async function worker() {
  while (cursor < resources.length) {
    const index = cursor++;
    try {
      results[index] = await verify(resources[index]);
    } catch (error) {
      results[index] = { ...resources[index], ok: false, error: String(error) };
    }
  }
}

await Promise.all(Array.from({ length: Math.max(1, concurrency) }, () => worker()));
const categories = Object.fromEntries([...new Set(results.map(item => item.category))].map(category => [category, {
  total: results.filter(item => item.category === category).length,
  ok: results.filter(item => item.category === category && item.ok).length,
}]));
const failures = results.filter(item => !item.ok);
const summary = {
  verified_at_utc: new Date().toISOString(),
  base,
  total: results.length,
  ok: results.length - failures.length,
  categories,
  failures,
};
process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
if (failures.length) process.exitCode = 1;
