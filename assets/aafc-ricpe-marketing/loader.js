(function () {
  "use strict";
  const baseUrl = new URL("./", document.currentScript.src);
  let manifestPromise;

  function getManifest() {
    if (!manifestPromise) {
      manifestPromise = fetch(new URL("manifest.json", baseUrl), { cache: "no-cache" }).then(response => {
        if (!response.ok) throw new Error(`manifest HTTP ${response.status}`);
        return response.json();
      });
    }
    return manifestPromise;
  }

  function decodeBase64(value) {
    const binary = atob(value.replace(/\s+/g, ""));
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
    return bytes;
  }

  async function sha256Hex(bytes) {
    if (!window.crypto || !window.crypto.subtle) return null;
    const digest = await window.crypto.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, "0")).join("");
  }

  async function hydrate(key) {
    const images = Array.from(document.querySelectorAll(`[data-aafc-image="${key}"]`));
    const links = Array.from(document.querySelectorAll(`[data-aafc-link="${key}"]`));
    if (!images.length) return;

    try {
      const manifest = await getManifest();
      const entry = manifest.images && manifest.images[key];
      if (!entry) throw new Error(`manifest entry missing for ${key}`);
      const partNames = entry.base64_parts || (entry.base64_path ? [entry.base64_path] : []);
      if (!partNames.length) throw new Error(`image data paths missing for ${key}`);
      const partTexts = await Promise.all(partNames.map(async partName => {
        const response = await fetch(new URL(`chunks/${partName}`, baseUrl), { cache: "force-cache" });
        if (!response.ok) throw new Error(`image data HTTP ${response.status} for ${key}/${partName}`);
        return response.text();
      }));
      const bytes = decodeBase64(partTexts.join(""));
      if (bytes.byteLength !== entry.bytes) throw new Error(`byte-length mismatch for ${key}`);
      const actualHash = await sha256Hex(bytes);
      if (actualHash && actualHash !== entry.sha256) throw new Error(`SHA-256 mismatch for ${key}`);
      const url = URL.createObjectURL(new Blob([bytes], { type: entry.mime || "image/webp" }));
      images.forEach(img => {
        img.src = url;
        img.dataset.aafcIntegrity = actualHash ? "verified" : "length-verified";
        img.removeAttribute("aria-busy");
      });
      links.forEach(link => {
        link.href = url;
        link.download = entry.filename;
      });
    } catch (error) {
      console.error("AAFC image hydration failed", key, error);
      images.forEach(img => {
        img.alt = `${img.alt || key} — image unavailable; consult the captioned source and hash`;
        img.dataset.aafcIntegrity = "failed";
        img.removeAttribute("aria-busy");
      });
      links.forEach(link => link.removeAttribute("href"));
    }
  }

  function start() {
    const keys = new Set(Array.from(document.querySelectorAll("[data-aafc-image]"), el => el.dataset.aafcImage));
    keys.forEach(key => hydrate(key));
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, { once: true });
  else start();
}());
