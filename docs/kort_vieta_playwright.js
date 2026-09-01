/* KORTELĖS VIETOS EILUTĖ IR ŠONINĖS JUOSTOS ŠALIES BLOKAS.
 *
 * Etalonai: docs/demo/veliaveles-pagrindinis-demo.html (.card .l)
 *           docs/demo/veliaveles-sidebar-demo.html (.cloc, .salis-blk)
 *
 * Tikrinam tikrais matmenimis naršyklėje:
 *   1. pagrindinio „Pasiūlymų" tinklelio kortelėse yra vietos eilutė
 *      „📍 Kaunas, Lithuania [vėliava]" — vėliava IŠKART po šalies
 *   2. rezultatų kortelės žalioje eilutėje — tas pats, VIENA eilutė
 *   3. ilgas pavadinimas („Nordrhein-Westfalen, Germany") eilutės
 *      nelaužo: tekstas trumpinamas, vėliava lieka toje pačioje eilutėje
 *   4. šoninės juostos ŠALIS blokas pagal etaloną
 *
 * Paleidimas:  SP=<scratchpad> node docs/kort_vieta_playwright.js
 */
const { chromium, paruosti } = require(process.env.SP + '/nuotrauka.js');
const EKRANAI = __dirname + '/ekranai';
const A = 'http://127.0.0.1:8899';

let gerai = 0, blogai = 0;
const tik = (s, k) => { s ? gerai++ : (blogai++, console.log('  NEPAVYKO: ' + k)); };
const antraste = (t) => console.log('\n── ' + t + ' ' + '─'.repeat(Math.max(0, 52 - t.length)));

const eik = async (p, kelias) => {
  await p.goto(A + kelias, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(1200);
};

/* Viena vietos eilutė išmatuota naršyklėje. */
const matuok = (p, sel) => p.evaluate((s) => {
  const v = document.querySelector(s);
  if (!v) return null;
  const t = v.querySelector('.kv-txt');
  const f = v.querySelector('img.veliava');
  const pin = v.querySelector('.kv-pin');
  const st = getComputedStyle(v);
  const eil = v.getBoundingClientRect();
  const out = {
    tekstas: t ? t.textContent.trim() : null,
    aukstis: eil.height,
    dydis: parseFloat(st.fontSize),
    spalva: st.color,
    tarpas: parseFloat(st.columnGap || st.gap),
    laužymas: st.flexWrap,
    trumpinimas: t ? getComputedStyle(t).textOverflow : null,
    pinPlotis: pin ? pin.getBoundingClientRect().width : null,
    veliavos: !!f,
  };
  if (f) {
    const fr = f.getBoundingClientRect(), tr = t.getBoundingClientRect();
    Object.assign(out, {
      fW: fr.width, fH: fr.height,
      fRadius: getComputedStyle(f).borderRadius,
      fKontūras: getComputedStyle(f).outlineWidth,
      poTeksto: fr.left >= tr.right - 1,
      tojePacioje: Math.abs(fr.top - tr.top) < 6,
      tarpasIkiVeliavos: fr.left - tr.right,
    });
  }
  return out;
}, sel);

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox'] });

  for (const [vardas, w, h] of [['1600', 1600, 1000], ['390', 390, 844]]) {
    console.log('\n══════ ' + vardas + 'px ══════');
    const p = await paruosti(b, w, h);
    const telefonas = w < 1024;

    // ── 1. PAGRINDINIS — „Pasiūlymų" tinklelis ──────────────────
    antraste('1. Pagrindinis: kortelės vietos eilutė');
    await eik(p, '/?salis=lt');
    const kiek = await p.$$eval('.home-tab-card .kv', e => e.length);
    tik(kiek > 0, 'kortelėse yra vietos eilutė (' + kiek + ')');
    // Dalis skirtukų paslėpti, o paslėpto elemento matmenys — nuliai.
    // Žymim pirmą MATOMĄ ir matuojam būtent ją.
    const yraMatoma = await p.evaluate(() => {
      for (const v of document.querySelectorAll('.home-tab-card .kv')) {
        if (v.getBoundingClientRect().width > 0) { v.id = 'kv-matoma'; return true; }
      }
      return false;
    });
    tik(yraMatoma, 'bent viena vietos eilutė matoma');
    const m = await matuok(p, '#kv-matoma');
    if (m) {
      tik(/^Vilnius, Lithuania$|^X, Lithuania$/.test(m.tekstas),
          'formatas „Miestas, Lithuania": ' + m.tekstas);
      tik(m.veliavos, 'yra vėliava');
      tik(m.poTeksto, 'vėliava PO šalies pavadinimo');
      tik(m.tojePacioje, 'vėliava toje pačioje eilutėje');
      tik(Math.abs(m.dydis - 12.5) < 0.6, 'šriftas 12,5px (' + m.dydis + ')');
      tik(m.spalva === 'rgb(107, 114, 128)', 'spalva #6B7280 (' + m.spalva + ')');
      tik(Math.abs(m.tarpas - 6) < 0.6, 'tarpas 6px (' + m.tarpas + ')');
      tik(m.laužymas === 'nowrap', 'flex-wrap: nowrap');
      tik(m.trumpinimas === 'ellipsis', 'tekstas su daugtaškiu');
      tik(Math.abs(m.pinPlotis - 11) < 0.6, 'smeigtukas 11px (' + m.pinPlotis + ')');
      tik(Math.abs(m.fW - 16) < 0.6 && Math.abs(m.fH - 12) < 0.6,
          'vėliava 16×12 (' + Math.round(m.fW) + '×' + Math.round(m.fH) + ')');
      tik(m.fRadius === '2px', 'radius 2px (' + m.fRadius + ')');
      tik(m.fKontūras === '1px', 'rėmelis 1px (' + m.fKontūras + ')');
      tik(Math.abs(m.tarpasIkiVeliavos - 6) < 1.5,
          'vėliava iškart po teksto, 6px (' + Math.round(m.tarpasIkiVeliavos) + ')');
    }
    // Tinklelis yra žemiau lango — prisukam prie jo, kad nuotraukoje
    // matytųsi būtent kortelės su vietos eilute.
    await p.$eval('#kv-matoma', el => el.closest('.home-tab-grid')
                  .scrollIntoView({ block: 'center' }));
    await p.waitForTimeout(500);
    await p.screenshot({ path: `${EKRANAI}/kort-vieta-${vardas}-pagrindinis.png`,
                         fullPage: false });

    // ── 2. REZULTATAI su šonine juosta ──────────────────────────
    antraste('2. Rezultatai: žalia vietos eilutė');
    await eik(p, '/?section=cars&sidebar=1&salis=de');
    const z = await matuok(p, '.kv-zalia');
    if (z) {
      tik(z.tekstas === 'Berlin, Germany' || /, Germany$/.test(z.tekstas),
          'formatas „Berlin, Germany": ' + z.tekstas);
      tik(z.poTeksto && z.tojePacioje, 'vėliava po šalies, VIENA eilutė');
      tik(z.spalva === 'rgb(22, 163, 74)', 'žalia #16A34A (' + z.spalva + ')');
      tik(z.aukstis < 30, 'eilutė nesulaužyta į dvi (' + Math.round(z.aukstis) + 'px)');
      tik(Math.abs(z.pinPlotis - 14) < 0.6, 'smeigtukas 14px (' + z.pinPlotis + ')');
    } else {
      tik(false, 'rezultatų kortelėje yra vietos eilutė');
    }
    if (z) {
      await p.$eval('.kv-zalia', el => el.closest('article, .ap-card, div')
                    .scrollIntoView({ block: 'center' }));
      await p.waitForTimeout(400);
    }
    await p.screenshot({ path: `${EKRANAI}/kort-vieta-${vardas}-rezultatai.png`,
                         fullPage: false });

    // ── 3. ILGAS PAVADINIMAS ────────────────────────────────────
    antraste('3. Ilgas pavadinimas — viena eilutė');
    const ilgas = await p.evaluate(() => {
      const v = document.querySelector('.kv-zalia');
      if (!v) return null;
      const t = v.querySelector('.kv-txt'), f = v.querySelector('img.veliava');
      const priesA = v.getBoundingClientRect().height;
      t.textContent = 'Nordrhein-Westfalen, Germany';
      // Susiaurinam eilutę, kad tekstas TIKRAI netilptų — kitaip
      // plačiame lange patikra nieko neįrodo.
      v.style.width = '190px';
      const po = v.getBoundingClientRect();
      const tr = t.getBoundingClientRect(), fr = f.getBoundingClientRect();
      return { priesA, aukstis: po.height,
               tojePacioje: Math.abs(fr.top - tr.top) < 6,
               poTeksto: fr.left >= tr.right - 1,
               veliavaViduj: fr.right <= po.right + 1,
               trumpinta: t.scrollWidth > t.clientWidth + 1,
               fW: fr.width };
    });
    if (ilgas) {
      tik(Math.abs(ilgas.aukstis - ilgas.priesA) < 2,
          'eilutės aukštis nepasikeitė (' + Math.round(ilgas.priesA) + ' → '
          + Math.round(ilgas.aukstis) + ')');
      tik(ilgas.tojePacioje, 'vėliava liko toje pačioje eilutėje');
      tik(ilgas.poTeksto, 'vėliava vis dar po teksto');
      tik(ilgas.veliavaViduj, 'vėliava neišlindo iš kortelės');
      tik(Math.abs(ilgas.fW - 16) < 0.6,
          'vėliava nesusitraukė (' + Math.round(ilgas.fW) + 'px)');
      tik(ilgas.trumpinta, 'netelpantis tekstas trumpinamas daugtaškiu');
    }
    if (ilgas) {
      await p.$eval('.kv-zalia', el => el.scrollIntoView({ block: 'center' }));
      await p.waitForTimeout(400);
    }
    await p.screenshot({ path: `${EKRANAI}/kort-vieta-${vardas}-ilgas.png`,
                         fullPage: false });

    // ── 4. ŠONINĖS JUOSTOS ŠALIES BLOKAS ────────────────────────
    if (!telefonas) {
      antraste('4. Šoninė juosta: ŠALIS blokas');
      await eik(p, '/?section=cars&sidebar=1&salis=lt');
      const blk = await p.evaluate(() => {
        const b = document.querySelector('.salis-blk');
        if (!b) return null;
        const st = getComputedStyle(b), h = getComputedStyle(b.querySelector('h4'));
        const k = b.querySelector('.salis-keisti-mazas');
        const ks = getComputedStyle(k);
        const cur = b.querySelector('.salis-cur');
        const cn = cur.querySelector('.salis-cur-vardas').getBoundingClientRect();
        const cf = cur.querySelector('img.veliava').getBoundingClientRect();
        return { fonas: st.backgroundColor, radius: st.borderRadius,
                 padding: st.padding,
                 hDydis: h.fontSize, hSvoris: h.fontWeight,
                 hDidziosios: h.textTransform, hSpalva: h.color,
                 kSpalva: ks.color, kDydis: ks.fontSize, kSvoris: ks.fontWeight,
                 kFonas: ks.backgroundColor, kRemelis: ks.borderTopWidth,
                 curVeliavaPo: cf.left >= cn.right - 1,
                 curDešinėje: k.getBoundingClientRect().right
                              > cf.right };
      });
      if (blk) {
        tik(blk.fonas === 'rgb(244, 244, 245)', 'fonas #F4F4F5 (' + blk.fonas + ')');
        tik(blk.radius === '10px', 'radius 10px (' + blk.radius + ')');
        tik(blk.padding === '14px', 'padding 14px (' + blk.padding + ')');
        tik(blk.hDydis === '12px', 'antraštė 12px (' + blk.hDydis + ')');
        tik(blk.hSvoris === '700', 'antraštė 700 (' + blk.hSvoris + ')');
        tik(blk.hDidziosios === 'uppercase', 'antraštė didžiosiomis');
        tik(blk.hSpalva === 'rgb(107, 114, 128)', 'antraštė pilka (' + blk.hSpalva + ')');
        // Etalone „Keisti" oranžinis (#E14D28) — tai to maketo akcentas.
        // Svetainės akcentas yra antracitas #374151, o oranžinė pagal
        // docs/dizaino-sistema.md leidžiama TIK logotipe ir ikonoje.
        tik(blk.kSpalva === 'rgb(55, 65, 81)',
            '„Keisti" svetainės akcento spalva (' + blk.kSpalva + ')');
        tik(blk.kDydis === '13px', '„Keisti" 13px (' + blk.kDydis + ')');
        tik(blk.kSvoris === '600', '„Keisti" 600 (' + blk.kSvoris + ')');
        tik(blk.kFonas === 'rgba(0, 0, 0, 0)', '„Keisti" be fono');
        tik(blk.kRemelis === '0px', '„Keisti" be rėmelio');
        tik(blk.curVeliavaPo, 'dabartinės šalies vėliava po pavadinimo');
        tik(blk.curDešinėje, '„Keisti" dešinėje');
      } else {
        tik(false, 'šoninėje juostoje yra ŠALIS blokas');
      }

      await p.click('.salis-keisti-mazas');
      await p.waitForTimeout(400);
      const eil = await p.evaluate(() => {
        const l = document.querySelector('.salis-list');
        const e = l.querySelectorAll('.salis-eil');
        const pir = e[0], antra = e[1];
        const r = antra.getBoundingClientRect();
        const nm = antra.querySelector('.salis-eil-vardas').getBoundingClientRect();
        const fl = antra.querySelector('img.veliava').getBoundingClientRect();
        const kk = antra.querySelector('.salis-eil-kiekis').getBoundingClientRect();
        return { linija: getComputedStyle(l).borderTopWidth,
                 pirmas: pir.querySelector('.salis-eil-vardas').textContent.trim(),
                 pirmasGaublys: /visos\.svg/.test(
                   pir.querySelector('img.veliava').getAttribute('src') || ''),
                 aukstis: r.height,
                 radijas: !!antra.querySelector('.salis-radijo'),
                 veliavaPoVardo: fl.left >= nm.right - 1,
                 kiekisDesineje: kk.right > fl.right
                                 && Math.abs(kk.right - r.right) < 4,
                 fW: fl.width, fH: fl.height };
      });
      tik(eil.linija === '1px', 'sąrašas po 1px linija (' + eil.linija + ')');
      tik(/Visos/.test(eil.pirmas), 'pirmas — „Visos šalys" (' + eil.pirmas + ')');
      tik(eil.pirmasGaublys, 'su gaubliu');
      tik(Math.abs(eil.aukstis - 34) < 2, 'eilutė 34px (' + Math.round(eil.aukstis) + ')');
      tik(eil.radijas, 'yra radio mygtukas');
      tik(eil.veliavaPoVardo, 'vėliava iškart po pavadinimo');
      tik(eil.kiekisDesineje, 'kiekis dešiniame krašte');
      tik(Math.abs(eil.fW - 20) < 0.6 && Math.abs(eil.fH - 15) < 0.6,
          'eilutės vėliava 20×15 (' + Math.round(eil.fW) + '×' + Math.round(eil.fH) + ')');
      const sb = await (await p.$('.salis-blk')).boundingBox();
      await p.screenshot({ path: `${EKRANAI}/kort-vieta-${vardas}-salis-blokas.png`,
                           clip: { x: Math.max(0, sb.x - 20), y: Math.max(0, sb.y - 20),
                                   width: Math.min(w, sb.width + 40),
                                   height: Math.min(h - Math.max(0, sb.y - 20),
                                                    sb.height + 40) } });
    }
    await p.close();
  }

  await b.close();
  console.log('\n' + '═'.repeat(56));
  console.log('gerai: ' + gerai + ', nepavyko: ' + blogai);
  process.exit(blogai ? 1 : 0);
})();
