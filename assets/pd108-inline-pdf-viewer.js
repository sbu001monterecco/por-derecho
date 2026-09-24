(() => {
  const roots = [...document.querySelectorAll('[data-pd108-pdf-viewer]')];
  if (!roots.length) return;

  async function decodeChunk(url) {
    const response = await fetch(url, {cache: 'no-store'});
    if (!response.ok) throw new Error(`${response.status} ${url}`);
    const payload = await response.json();
    if (payload.encoding !== 'base64-tilde-segments-16' || typeof payload.data !== 'string') throw new Error('invalid chunk');
    const encoded = payload.data.replaceAll('~', '');
    const binary = atob(encoded);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
    return bytes;
  }

  async function hydrate(root) {
    const status = root.querySelector('[data-pd108-status]');
    const frame = root.querySelector('iframe');
    const open = root.querySelector('[data-pd108-open]');
    const details = root.querySelector('[data-pd108-details]');
    const manifestUrl = new URL(root.dataset.manifest, location.href);
    const base = new URL('.', manifestUrl);
    status.textContent = root.dataset.loading || 'Preparing PDF…';
    const response = await fetch(manifestUrl, {cache: 'no-store'});
    if (!response.ok) throw new Error(`${response.status} manifest`);
    const manifest = await response.json();
    const parts = [];
    for (let i = 0; i < manifest.chunks.length; i += 1) {
      parts.push(await decodeChunk(new URL(manifest.chunks[i], base)));
      status.textContent = `${root.dataset.loading || 'Preparing PDF…'} ${i + 1}/${manifest.chunks.length}`;
    }
    const blob = new Blob(parts, {type: 'application/pdf'});
    if (blob.size !== manifest.source_pdf_size_bytes) throw new Error('size mismatch');
    const bytes = await blob.arrayBuffer();
    const digest = [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map((b) => b.toString(16).padStart(2, '0')).join('');
    if (digest !== manifest.source_pdf_sha256) throw new Error('hash mismatch');
    const url = URL.createObjectURL(blob);
    frame.src = `${url}#view=FitH&toolbar=1`;
    frame.hidden = false;
    open.href = url;
    open.target = '_blank';
    open.rel = 'noopener';
    open.hidden = false;
    details.textContent = `${manifest.source_pdf_filename} · ${manifest.source_pdf_size_bytes.toLocaleString()} bytes · SHA-256 ${digest}`;
    status.textContent = root.dataset.ready || 'Verified PDF ready';
    root.dataset.verified = 'true';
  }

  roots.forEach((root) => hydrate(root).catch((error) => {
    const status = root.querySelector('[data-pd108-status]');
    status.textContent = `${root.dataset.failed || 'PDF could not be prepared'} (${error.message})`;
    root.dataset.verified = 'false';
  }));
})();