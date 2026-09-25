(() => {
  const p = location.pathname;
  const map = [
    [/\/(en\/book|es\/libro)\/?$/, 'reason-to-believe.svg', 'Reason to Believe'],
    [/\/law-mower-man\/?$/, 'law-mower-man.svg', 'Law-mower Man'],
    [/\/the-sunrockers\/?$/, 'the-sunrockers.svg', 'The SunRockers'],
    [/\/(justice-in-pieces|justicia-en-fragmentos)\/?$/, 'justice-in-pieces.svg', 'Justice in Pieces'],
    [/\/(special-situations|situaciones-especiales)\/?$/, 'special-situations.svg', 'Special Situations'],
    [/\/four-green-houses-one-red-hotel\/?$/, 'four-green-houses-one-red-hotel.svg', '4 Green Houses, One Red Hotel']
  ];
  const hit = map.find(([re]) => re.test(p));
  if (!hit) return;
  const [, file, title] = hit;
  const depth = p.split('/').filter(Boolean).length;
  const prefix = '../'.repeat(Math.max(1, depth - 1));
  const src = `${prefix}assets/book-covers/${file}`;
  document.querySelectorAll('.book-cover img').forEach(img => { img.src = src; img.alt = `${title} book cover`; });
  const og = document.querySelector('meta[property="og:image"]');
  if (og) og.content = new URL(src, location.href).href;
})();
