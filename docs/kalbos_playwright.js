/* ═══════════════════════════════════════════════════════════════════
   KALBŲ PERJUNGIKLIS telefone ir planšetėje — Playwright patikra.

   Paleidimas (reikia vietinio serverio ties 127.0.0.1:8899):
       SP=<katalogas su node_modules> node docs/kalbos_playwright.js

   Tikrina: antraštės vėliavėlė, apatinis lakštas, mėsainio meniu
   skyrelis (48 px eilutės, 24 px vėliavos, 13 px antraštė, varnelė),
   poraštė, ir svarbiausia — kad po perjungimo lieki TAME PAČIAME
   puslapyje su visais GET filtrais.
   ═══════════════════════════════════════════════════════════════════ */
const { chromium, paruosti } = require(require('path').join(__dirname, 'patikra', 'nuotrauka.js'));
const S = process.env.SP;
const ADRESAS = 'http://127.0.0.1:8899/?section=cars&price_min=5000&fuel_type=2';
let gerai = 0, blogai = 0;
const tikrink = (s, k) => { if (s) gerai++; else { blogai++; console.log('  NEPAVYKO: ' + k); } };

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });

  for (const [vardas, w, h] of [['telefonas', 390, 844], ['plansete', 768, 1024]]) {
    console.log('\n══ ' + vardas + ' ' + w + '×' + h + ' ══');
    const p = await paruosti(b, w, h);
    await p.goto(ADRESAS, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await p.waitForTimeout(2200);

    // ── 1. Antraštės vėliavėlė ──
    const mygtukas = await p.$('.kalbos-mygtukas');
    const matomas = mygtukas && await mygtukas.isVisible();
    tikrink(matomas, 'antraštėje matoma kalbos vėliavėlė');
    if (matomas) {
      const d = await mygtukas.boundingBox();
      tikrink(Math.round(d.width) === 32 && Math.round(d.height) === 32,
              `vėliavėlė 32×32 (gauta ${Math.round(d.width)}×${Math.round(d.height)})`);
      tikrink(d.x + d.width < w, 'vėliavėlė telpa į ekraną');
    }
    // horizontalaus slinkimo neatsirado
    const persislinko = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
    tikrink(!persislinko, 'antraštė nepraplėtė puslapio į šoną');
    await p.screenshot({ path: `${S}/po-${vardas}-antraste.png` });

    // ── 2. Apatinis lakštas ──
    if (matomas) {
      await mygtukas.click();
      await p.waitForTimeout(500);
      const lakstas = await p.$('.kalbos-lakstas');
      tikrink(lakstas && await lakstas.isVisible(), 'paspaudus atsidaro apatinis lakštas');
      const eilutes = await p.$$('.kalbos-lakstas .kalbos-eilute');
      tikrink(eilutes.length === 13, `lakšte 13 kalbų (rasta ${eilutes.length})`);
      await p.screenshot({ path: `${S}/po-${vardas}-lakstas.png` });
      // Uždangos vidurį dengia pats lakštas — spaudžiam viršuje,
      // ten, kur žmogus ir bakstelėtų norėdamas uždaryti.
      await p.click('.kalbos-uzdanga', { position: { x: 40, y: 40 } });
      await p.waitForTimeout(400);
      tikrink(!(await (await p.$('.kalbos-lakstas')).isVisible()), 'uždanga uždaro lakštą');
    }

    // ── 3. Mėsainio meniu ──
    await p.click('button.lg\\:hidden.p-2');
    await p.waitForTimeout(600);
    const antraste = await p.$('.mm-kalbos .kalbos-antraste');
    tikrink(antraste, 'meniu apačioje yra skyrelis „Kalba"');
    if (antraste) {
      const t = (await antraste.textContent()).trim();
      tikrink(t === 'Kalba', `antraštės tekstas „Kalba" (gauta „${t}")`);
      const st = await antraste.evaluate(e => getComputedStyle(e));
      const stilius = await antraste.evaluate(e => {
        const c = getComputedStyle(e);
        return { dydis: c.fontSize, svoris: c.fontWeight, didz: c.textTransform, tarpas: c.letterSpacing };
      });
      tikrink(stilius.dydis === '13px', `antraštė 13px (gauta ${stilius.dydis})`);
      tikrink(stilius.svoris === '700', `antraštė 700 (gauta ${stilius.svoris})`);
      tikrink(stilius.didz === 'uppercase', 'antraštė didžiosiomis');
      tikrink(parseFloat(stilius.tarpas).toFixed(1) === '0.4', `tarpas 0.4px (gauta ${stilius.tarpas})`);
      // matosi be papildomo scrollinimo
      const r = await antraste.evaluate(e => { const b = e.getBoundingClientRect();
        return { virsus: b.top, langas: window.innerHeight }; });
      tikrink(r.virsus < r.langas, `skyrelis matosi be scrollo (y=${Math.round(r.virsus)} < ${r.langas})`);
    }
    const eil = await p.$$('.mm-kalbos .kalbos-eilute');
    tikrink(eil.length === 13, `meniu 13 kalbų (rasta ${eil.length})`);
    if (eil.length) {
      const d = await eil[0].boundingBox();
      tikrink(Math.round(d.height) === 48, `eilutė 48px (gauta ${Math.round(d.height)})`);
      const vel = await eil[0].$('.fi');
      const dv = await vel.boundingBox();
      tikrink(Math.round(dv.width) === 24 && Math.round(dv.height) === 24,
              `vėliavėlė 24×24 (gauta ${Math.round(dv.width)}×${Math.round(dv.height)})`);
      const vardStil = await eil[0].$eval('.kalbos-vardas', e => getComputedStyle(e).fontSize);
      tikrink(vardStil === '16px', `pavadinimas 16px (gauta ${vardStil})`);
      // aktyvi — varnelė ir 600
      const aktyvi = await p.$('.mm-kalbos .kalbos-eilute.is-on');
      tikrink(aktyvi, 'aktyvi kalba pažymėta');
      if (aktyvi) {
        tikrink(await aktyvi.$('.kalbos-varnele'), 'aktyvi turi varnelę');
        const sp = await aktyvi.$eval('.kalbos-varnele', e => getComputedStyle(e).color);
        tikrink(sp === 'rgb(0, 0, 0)', `varnelė juoda (gauta ${sp})`);
        const sv = await aktyvi.$eval('.kalbos-vardas', e => getComputedStyle(e).fontWeight);
        tikrink(sv === '600', `aktyvios svoris 600 (gauta ${sv})`);
      }
    }
    await p.screenshot({ path: `${S}/po-${vardas}-meniu.png` });

    // ── 4. Perjungimas — lieka tas pats puslapis su filtrais ──
    const enMygtukas = await p.$('.mm-kalbos button[value="en"]');
    tikrink(enMygtukas, 'meniu yra „English" mygtukas');
    if (enMygtukas) {
      await Promise.all([p.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }), enMygtukas.click()]);
      await p.waitForTimeout(1500);
      const u = new URL(p.url());
      console.log('   po perjungimo:', p.url());
      tikrink(u.pathname === '/en/', `kelias /en/ (gauta ${u.pathname})`);
      tikrink(u.searchParams.get('section') === 'cars', 'išliko ?section=cars');
      tikrink(u.searchParams.get('price_min') === '5000', 'išliko ?price_min=5000');
      tikrink(u.searchParams.get('fuel_type') === '2', 'išliko ?fuel_type=2');
      const html = await p.content();
      tikrink(html.includes('Found') || html.includes('listings'), 'puslapis angliškas');
      await p.screenshot({ path: `${S}/po-${vardas}-perjungta-en.png` });
    }

    // ── 5. Poraštė ──
    await p.goto(ADRESAS, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await p.waitForTimeout(1800);
    const por = await p.$('.kalbos-porastes-btn');
    tikrink(por, 'poraštėje yra kalbos mygtukas');
    if (por) {
      const t = (await por.textContent()).replace(/\s+/g, ' ').trim();
      tikrink(t.includes('Kalba: Lietuvių'), `poraštėje „Kalba: Lietuvių" (gauta „${t}")`);
      await por.scrollIntoViewIfNeeded();
      await por.click();
      await p.waitForTimeout(400);
      const sar = await p.$('.kalbos-porastes-sarasas');
      tikrink(sar && await sar.isVisible(), 'poraštės sąrašas atsidaro');
      await p.screenshot({ path: `${S}/po-${vardas}-porastes.png` });
    }
    await p.close();
  }
  await b.close();
  console.log('\n' + '═'.repeat(50));
  console.log(`gerai: ${gerai}, nepavyko: ${blogai}`);
  process.exit(blogai ? 1 : 0);
})();
