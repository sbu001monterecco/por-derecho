import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import test from 'node:test';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const modules = [
  ['matkator-8584-hotel-title-multitrack-20260903.js', 'data-matkator-8584-critical-update'],
  ['hotel-finca-title-system-interlink-20260903.js', 'data-hotel-finca-system-control'],
];

// A small DOM fixture enforces insertBefore's real direct-child requirement.
// The legacy Club SEI pages wrap their first section in main > article.
class Element {
  constructor(tag) { this.tagName = tag; this.children = []; this.parentNode = null; this.dataset = {}; this.attributes = {}; }
  get nextSibling() { return this.parentNode?.children[this.parentNode.children.indexOf(this) + 1] || null; }
  insertBefore(node, before) {
    if (before !== null && before.parentNode !== this) throw new Error('The reference node is not a child of this node');
    if (node.parentNode) node.parentNode.children.splice(node.parentNode.children.indexOf(node), 1);
    const index = before === null ? this.children.length : this.children.indexOf(before);
    this.children.splice(index, 0, node); node.parentNode = this; return node;
  }
  appendChild(node) { return this.insertBefore(node, null); }
  prepend(node) { return this.insertBefore(node, this.children[0] || null); }
  setAttribute(name, value) { this.attributes[name] = value; }
  querySelector(selector) {
    for (const child of this.children) {
      if (selector === child.tagName) return child;
      const found = child.querySelector(selector); if (found) return found;
    }
    return null;
  }
}

function fixture(lang, nested, withSection = true, withNext = true) {
  const main = new Element('main');
  const parent = nested ? main.appendChild(new Element('article')) : main;
  const hero = withSection ? parent.appendChild(new Element('section')) : null;
  if (hero) hero.innerHTML = '<a href="#preserved-evidence">Existing evidence</a>';
  const tail = withNext ? parent.appendChild(new Element('section')) : null;
  if (tail) tail.innerHTML = '<a href="#preserved-next">Existing next section</a>';
  // For the no-section branch use a non-section placeholder.
  if (!withSection) tail.tagName = 'div';
  const created = [];
  const document = {
    body: new Element('body'), head: new Element('head'), readyState: 'complete',
    documentElement: { lang },
    getElementById: () => null,
    querySelector: selector => selector === 'main' ? main : null,
    createElement: tag => { const node = new Element(tag); created.push(node); return node; },
  };
  const location = { pathname: `/por-derecho/${lang}/lava-verde-club-sei-meeting-point/` };
  return { main, parent, hero, tail, created, document, location };
}

for (const [name, marker] of modules) {
  const source = fs.readFileSync(path.join(root, 'assets', name), 'utf8');
  for (const lang of ['en', 'es']) {
    for (const nested of [false, true]) {
      test(`${name}: ${lang} ${nested ? 'article-wrapped' : 'direct'} first section`, () => {
        const f = fixture(lang, nested);
        const heroContent = f.hero.innerHTML, tailContent = f.tail.innerHTML;
        vm.runInNewContext(source, { document: f.document, location: f.location, window: { location: f.location } }, { filename: name });
        const inserted = f.created.find(node => node.attributes[marker]);
        assert.ok(inserted, 'the existing panel is retained');
        assert.deepEqual(f.parent.children, [f.hero, inserted, f.tail]);
        assert.equal(f.hero.innerHTML, heroContent);
        assert.equal(f.tail.innerHTML, tailContent);
        assert.equal((inserted.innerHTML.match(/<a href=/g) || []).length, 6, 'all existing panel links remain');
        if (nested) assert.deepEqual(f.main.children, [f.parent]);
      });
    }
    test(`${name}: ${lang} no first section preserves prepend fallback`, () => {
      const f = fixture(lang, false, false);
      vm.runInNewContext(source, { document: f.document, location: f.location, window: { location: f.location } }, { filename: name });
      const inserted = f.created.find(node => node.attributes[marker]);
      assert.deepEqual(f.main.children, [inserted, f.tail]);
    });
    for (const nested of [false, true]) {
      test(`${name}: ${lang} ${nested ? 'nested' : 'direct'} last section preserves prepend fallback`, () => {
        const f = fixture(lang, nested, true, false);
        vm.runInNewContext(source, { document: f.document, location: f.location, window: { location: f.location } }, { filename: name });
        const panels = f.created.filter(node => node.attributes[marker]);
        assert.equal(panels.length, 1);
        assert.deepEqual(f.main.children, [panels[0], nested ? f.parent : f.hero]);
        if (nested) assert.deepEqual(f.parent.children, [f.hero]);
      });
    }
    if (name.startsWith('hotel-finca')) {
      test(`${name}: ${lang} non-home nested section uses its actual parent`, () => {
        const f = fixture(lang, true);
        f.location.pathname = `/por-derecho/${lang}/dp-748-2026/nested-detail`;
        vm.runInNewContext(source, { document: f.document, location: f.location, window: { location: f.location } }, { filename: name });
        const panels = f.created.filter(node => node.attributes[marker]);
        assert.equal(panels.length, 1);
        assert.deepEqual(f.parent.children, [f.hero, panels[0], f.tail]);
        assert.deepEqual(f.main.children, [f.parent]);
      });
    }
  }
}
