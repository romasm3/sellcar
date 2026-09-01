/* ═══════════════════════════════════════════════════════════════════
   ŠALIES VĖLIAVĖLĖS — Playwright patikra (docs/taisykles.md 5).

   Paleidimas (reikia vietinio serverio ties 127.0.0.1:8899):
       SP=<katalogas su node_modules> node docs/veliavos_playwright.js

   Tikrina matmenis (16×12, tarpas 6 px, apvalinimas 2 px), kad tai
   <img> su SVG (ne emoji), ir surenka palyginimą: kontaktų blokas bei
   žemėlapio burbulas su lietuvišku ir vokišku skelbimu greta.
   ═══════════════════════════════════════════════════════════════════ */
const { chromium, paruosti } = require(process.env.SP + '/nuotrauka.js');
const S = process.env.SP;
let gerai=0, blogai=0;
const tik=(s,k)=>{ s?gerai++:(blogai++,console.log('  NEPAVYKO: '+k)); };

(async () => {
  const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args:['--no-sandbox'] });

  // ── 1. Kortelės sąraše (LT ir DE greta) ──
  // .card-params rodomas tik siaurame rodinyje (darbalaukyje display:none),
  // tad korteles fotografuojam 390 px — ten ir gyvena vietos eilutė.
  let p = await paruosti(b, 390, 900);
  await p.goto('http://127.0.0.1:8899/browse/?category=cars&sidebar=1', {waitUntil:'domcontentloaded', timeout:60000});
  await p.waitForTimeout(2500);
  const vel = await p.$$('.veliava');
  tik(vel.length >= 2, `kortelėse vėliavėlių: ${vel.length}`);
  // Matuojam būtent VIETOS EILUTĖS vėliavą: šoninės juostos šalies bloke
  // vėliavos didesnės (20×15) ir jos čia netinka. Sąraše yra du kortelių
  // išdėstymai — vienas paslėptas, tad imam matomą.
  let dydis = null, matoma = null;
  for (const v of await p.$$('.kv .veliava, .card-params .veliava')) {
    const d = await v.boundingBox();
    if (d && d.width) { dydis = d; matoma = v; break; }
  }
  tik(dydis, 'yra matoma vietos eilutės vėliavėlė');
  if (!dydis) { await b.close(); console.log('gerai: '+gerai+', nepavyko: '+(blogai+1)); process.exit(1); }
  tik(Math.round(dydis.width) === 16 && Math.round(dydis.height) === 12,
      `16×12 (${Math.round(dydis.width)}×${Math.round(dydis.height)})`);
  const stilius = await matoma.evaluate(e => { const c = getComputedStyle(e);
    // Tarpą iki teksto duoda arba pačios vėliavos margin (tekstinėje
    // eilutėje), arba tėvo flex gap (naujoje .kv eilutėje) — abu 6px.
    const t = getComputedStyle(e.parentElement);
    const tarpas = c.marginLeft !== '0px' ? c.marginLeft
                 : (t.display.includes('flex') ? (t.columnGap || t.gap) : c.marginLeft);
    return { tarpas, apval: c.borderRadius, tipas: e.tagName }; });
  tik(stilius.tarpas === '6px', `tarpas 6px (${stilius.tarpas})`);
  tik(stilius.apval === '2px', `apvalinimas 2px (${stilius.apval})`);
  tik(stilius.tipas === 'IMG', 'SVG per <img>, ne emoji');
  await matoma.evaluate(e => { const k = e.closest('article, .card, li, .kortele, div[class*=card]');
    if (k) k.scrollIntoView({block:'center'}); });
  await p.waitForTimeout(600);
  await p.screenshot({ path: `${S}/veliavos-korteles.png`, fullPage: false });
  await p.close();

  // ── 2 ir 3. Kontaktų blokas ir žemėlapio burbulas — LT ir DE greta ──
  const fragmentai = {};
  p = await paruosti(b, 1280, 900);
  for (const [zyma, pk] of [['lt', 7], ['de', 11]]) {
    await p.goto(`http://127.0.0.1:8899/listings/${pk}/`, {waitUntil:'domcontentloaded', timeout:60000});
    await p.waitForTimeout(1800);
    // Imam TIK vietos eilutę su pardavėjo vardu — visas .pard-bl kartais
    // apima pusę puslapio ir palyginime lieka nesuprantamas.
    fragmentai['kont_' + zyma] = await p.$eval('.pard-vieta', e => e.outerHTML)
      .catch(() => '');
    const burb = await p.evaluate(async (id) => {
      const r = await fetch('/map/kortele/' + id + '/');
      return (await r.json()).html;
    }, pk);
    fragmentai['burb_' + zyma] = burb;
  }
  const css = await (await fetch('http://127.0.0.1:8899/static/css/style.css')).text().catch(()=>'')
    || '';
  await p.close();

  // <base> būtinas: fragmentuose src="/static/flags/lt.svg" yra ABSOLIUTUS
  // kelias, o file:// puslapyje jis rodytų į failų sistemos šaknį.
  const pardCss = (await (await fetch('http://127.0.0.1:8899/listings/7/')).text())
    // Tingus [\s\S]*? peršoka per </style> ir įtraukia tarp jų buvusį HTML —
    // todėl aiškiai draudžiam uždarymo žymę viduje.
    .match(/<style>(?:(?!<\/style>)[\s\S])*?\.pard-vieta(?:(?!<\/style>)[\s\S])*?<\/style>/)?.[0] || '';
  const puslapis = `<!doctype html><meta charset="utf-8">
  <base href="http://127.0.0.1:8899/">
  <link rel="stylesheet" href="/static/css/style.css">
  ${pardCss}
  <style>body{font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#F5F5F7;margin:0;padding:24px}
   h2{font-size:15px;color:#6B7280;margin:0 0 10px;font-weight:600}
   .por{display:grid;grid-template-columns:1fr 1fr;gap:24px;max-width:1100px;margin:0 auto 28px}
   .kort{background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:16px}
   .zb-vieta{display:flex;align-items:center;gap:4px;color:#6B7280;font-size:13px;margin-top:6px}
   .zb-pav{font-weight:600;text-decoration:none;color:#1A1A1A}
   .zb-kaina{font-weight:700;margin:4px 0}</style>
  <div class="por"><div><h2>Kontaktų blokas — lietuviškas skelbimas</h2><div class="kort">${fragmentai.kont_lt}</div></div>
   <div><h2>Kontaktų blokas — vokiškas skelbimas</h2><div class="kort">${fragmentai.kont_de}</div></div></div>
  <div class="por"><div><h2>Žemėlapio burbulas — LT</h2><div class="kort">${fragmentai.burb_lt}</div></div>
   <div><h2>Žemėlapio burbulas — DE</h2><div class="kort">${fragmentai.burb_de}</div></div></div>`;
  require('fs').writeFileSync(S + '/palyginimas.html', puslapis);

  p = await paruosti(b, 1200, 900);
  await p.goto('file://' + S + '/palyginimas.html', {waitUntil:'domcontentloaded'});
  await p.waitForTimeout(2000);
  // Tikrinam PAGAL VIETOS EILUTES, ne bendrą vėliavų kiekį: kontaktų bloke
  // gali būti ir kitų vėliavų (pvz. pardavėjo kalbos), o mums rūpi ta, kuri
  // stovi prie miesto.
  const eilutes = await p.$$eval('.pard-vieta, .zb-vieta', els => els.map(e => ({
    tekstas: e.textContent.replace(/\s+/g, ' ').trim(),
    alt: e.querySelector('.veliava') ? e.querySelector('.veliava').alt : null,
    tagas: e.querySelector('.veliava') ? e.querySelector('.veliava').tagName : null,
  })));
  tik(eilutes.length >= 4, `bent keturios vietos eilutės (${eilutes.length})`);
  tik(eilutes.every(e => e.tagas === 'IMG'), 'kiekvienoje — <img> vėliavėlė');
  const poros = eilutes.map(e => e.alt + '|' + e.tekstas);
  tik(poros.some(x => x === 'Lietuva|Vilnius, Lietuva'), 'LT: ' + JSON.stringify(poros));
  tik(poros.some(x => x === 'Vokietija|Berlin, Vokietija'), 'DE: ' + JSON.stringify(poros));
  const tekstai = await p.$$eval('.pard-vieta, .zb-vieta', e => e.map(x => x.textContent.replace(/\s+/g,' ').trim()));
  tik(tekstai.some(t => t.includes('Vilnius, Lietuva')) && tekstai.some(t => t.includes('Berlin, Vokietija')),
      'formatas „Miestas, Šalis": ' + JSON.stringify(tekstai));
  await p.screenshot({ path: `${S}/veliavos-palyginimas.png`, fullPage: true });
  await p.close();

  await b.close();
  console.log(`\ngerai: ${gerai}, nepavyko: ${blogai}`);
  process.exit(blogai ? 1 : 0);
})();
