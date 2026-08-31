(() => {
  const root = document.querySelector('[data-pdf-viewer]');
  if (!root) return;
  const docs = JSON.parse(root.dataset.documents || '{}');
  const key = new URLSearchParams(location.search).get('doc');
  const record = docs[key];
  const status = root.querySelector('[data-status]');
  const frame = root.querySelector('iframe');
  const download = root.querySelector('[data-download]');
  const title = root.querySelector('[data-title]');
  const details = root.querySelector('[data-details]');
  if (!record) {
    status.textContent = root.dataset.unknown;
    return;
  }
  document.title = record.title + ' | Por Derecho';
  title.textContent = record.title;
  const manifestPath = key === 'exhibit-access' ? record.manifest.replace('pdf-transport-v1.json', 'pdf-transport-exhibit-v1.json') : record.manifest;
  const absolute = new URL(manifestPath, location.href);
  const base = new URL('.', absolute);

  async function decodeChunk(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`${response.status} ${url}`);
    const payload = await response.json();
    if (payload.encoding !== 'base64-tilde-segments-16' || typeof payload.data !== 'string') throw new Error(`invalid chunk ${url}`);
    const encoded = payload.data.replaceAll('~', '');
    const binary = atob(encoded);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
    return bytes;
  }

  async function run() {
    status.textContent = root.dataset.loading;
    const response = await fetch(absolute);
    if (!response.ok) throw new Error(`${response.status} manifest`);
    const manifest = await response.json();
    const parts = [];
    for (let i = 0; i < manifest.chunks.length; i += 6) {
      const batch = manifest.chunks.slice(i, i + 6);
      const decoded = await Promise.all(batch.map((path) => decodeChunk(new URL(path, base))));
      parts.push(...decoded);
      status.textContent = `${root.dataset.loading} ${Math.min(i + 6, manifest.chunks.length)}/${manifest.chunks.length}`;
    }
    const blob = new Blob(parts, {type: 'application/pdf'});
    if (blob.size !== manifest.source_pdf_size_bytes) throw new Error('size mismatch');
    const bytes = await blob.arrayBuffer();
    const digest = [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map((b) => b.toString(16).padStart(2, '0')).join('');
    if (digest !== manifest.source_pdf_sha256) throw new Error('hash mismatch');
    const url = URL.createObjectURL(blob);
    frame.src = url;
    frame.hidden = false;
    download.href = url;
    download.download = manifest.source_pdf_filename;
    download.hidden = false;
    details.textContent = `${manifest.source_pdf_filename} · ${manifest.source_pdf_size_bytes.toLocaleString()} bytes · SHA-256 ${digest}`;
    status.textContent = root.dataset.ready;
  }
  run().catch((error) => {
    status.textContent = `${root.dataset.failed} (${error.message})`;
  });
})();
