/* MOBILI ANTRAŠTĖ IR ŠALIES JUOSTA — 320 / 360 / 390 / 414 / 768 px.
 *
 * Tikrina keturis dalykus kiekviename plotyje:
 *   1. kalbos mygtukas matomas (getBoundingClientRect plotis > 0);
 *   2. antraštės elementai vienoje eilutėje ir nepersidengia;
 *   3. šalies juostos eilutė 52 px, ne daugiau (t. y. nesilaužo);
 *   4. document.scrollWidth <= window.innerWidth.
 *
 * Paleidimas:  SP=<scratchpad> node docs/mob_antrastes_playwright.js
 *              SP=<scratchpad> GYVAI=1 node docs/mob_antrastes_playwright.js
 */
const GYVAI = !!process.env.GYVAI;
const { chromium, paruosti } = require(process.env.SP +
  (GYVAI ? '/nuotrauka_gyva.js' : '/nuotrauka.js'));
const A = GYVAI ? 'https://autoleft.com' : 'http://127.0.0.1:8899';
const PLOCIAI = [320, 360, 390, 414, 768];
const EKRANAI = __dirname + '/ekranai';

let gerai = 0, blogai = 0;
const tik = (s, k) => { s ? gerai++ : (blogai++, console.log('  NEPAVYKO: ' + k)); };

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });

  for (const w of PLOCIAI) {
    const p = await paruosti(b, w, 800);
    await p.goto(A + '/', { waitUntil: 'domcontentloaded', timeout: 90000 });
    await p.waitForTimeout(GYVAI ? 2500 : 1800);

    const m = await p.evaluate(() => {
      const r = e => e.getBoundingClientRect();
      const k = document.querySelector('.kalbos-mygtukas');
      const kr = k ? r(k) : null;
      const kcs = k ? getComputedStyle(k) : null;

      // Antraštės veiksmai: matomi tiesioginiai vaikai
      const juosta = document.querySelector('.hdr-veiksmai');
      const vaikai = juosta ? [...juosta.children].filter(e => r(e).width > 0) : [];
      const dez = vaikai.map(e => ({ k: (e.className || '').toString().slice(0, 22),
                                     l: Math.round(r(e).left), d: Math.round(r(e).right),
                                     v: Math.round(r(e).top), a: Math.round(r(e).bottom) }));
      let persidengia = 0, eilutes = new Set();
      for (let i = 0; i < dez.length; i++) {
        eilutes.add(Math.round(dez[i].v / 8));
        for (let j = i + 1; j < dez.length; j++) {
          if (dez[i].l < dez[j].d - 1 && dez[j].l < dez[i].d - 1
              && dez[i].v < dez[j].a - 1 && dez[j].v < dez[i].a - 1) persidengia++;
        }
      }

      const se = document.querySelector('.salies-eilute');
      const vard = document.querySelector('.salies-vardas');
      const kiek = document.querySelector('.salies-kiekis');
      const nav = document.querySelector('.sec-nav-in');

      return {
        kalba: k ? { plotis: Math.round(kr.width), aukstis: Math.round(kr.height),
                     kodas: (k.querySelector('.kalbos-kodas') || {}).textContent,
                     didziosios: k.querySelector('.kalbos-kodas')
                                 ? getComputedStyle(k.querySelector('.kalbos-kodas')).textTransform : null,
                     veliava: k.querySelector('.fi')
                              ? Math.round(r(k.querySelector('.fi')).width) + '×'
                                + Math.round(r(k.querySelector('.fi')).height) : null,
                     rodykle: k.querySelector('svg') ? Math.round(r(k.querySelector('svg')).width) : null,
                     fonas: kcs.backgroundColor, remelis: kcs.borderTopWidth } : null,
        antraste: { elementu: dez.length, eiluciu: eilutes.size, persidengia },
        juosta: se ? { aukstis: Math.round(r(se).height),
                       vardas: vard ? vard.textContent.trim() : null,
                       vardoEilutes: vard ? Math.round(r(vard).height / 22) : null,
                       kiekis: kiek ? kiek.textContent.trim() : null,
                       kiekioOverflow: kiek ? getComputedStyle(kiek).textOverflow : null } : null,
        nav: nav ? { slenka: getComputedStyle(nav).overflowX,
                     plotis: Math.round(r(nav).width),
                     turinys: nav.scrollWidth } : null,
        langas: window.innerWidth, puslapis: document.documentElement.scrollWidth,
      };
    });

    console.log('\n  ' + w + ' px');
    console.log('    kalba:    ' + JSON.stringify(m.kalba));
    console.log('    antraštė: ' + JSON.stringify(m.antraste));
    console.log('    juosta:   ' + JSON.stringify(m.juosta));
    console.log('    nuorodos: ' + JSON.stringify(m.nav));

    tik(m.kalba && m.kalba.plotis > 0, w + ' — kalbos mygtuko nesimato');
    tik(m.kalba && m.kalba.didziosios === 'uppercase', w + ' — kodas ne DIDŽIOSIOMIS');
    tik(m.kalba && m.kalba.veliava === '20×15', w + ' — vėliava ne 20×15 (' + (m.kalba||{}).veliava + ')');
    tik(m.kalba && m.kalba.rodykle === 11, w + ' — rodyklė ne 11 px (' + (m.kalba||{}).rodykle + ')');
    tik(m.kalba && m.kalba.fonas === 'rgba(0, 0, 0, 0)' && m.kalba.remelis === '0px',
        w + ' — mygtukas su fonu arba rėmeliu');
    tik(m.antraste.eiluciu === 1, w + ' — antraštė ne vienoje eilutėje (' + m.antraste.eiluciu + ')');
    tik(m.antraste.persidengia === 0, w + ' — antraštės elementai persidengia (' + m.antraste.persidengia + ')');
    if (m.juosta) {
      tik(m.juosta.aukstis <= 52, w + ' — šalies juosta ' + m.juosta.aukstis + ' px (turi būti <= 52)');
      tik(m.juosta.vardoEilutes <= 1, w + ' — šalies pavadinimas dviem eilutėm');
      tik(!/…|\.\.\./.test(m.juosta.kiekis || ''), w + ' — skaičius trumpinamas: „' + m.juosta.kiekis + '"');
    }
    if (m.nav) tik(m.nav.slenka === 'auto' || m.nav.slenka === 'scroll',
                   w + ' — nuorodų juosta neslenka (' + m.nav.slenka + ')');
    tik(m.puslapis <= m.langas + 1,
        w + ' — puslapis platesnis už ekraną (' + m.puslapis + ' > ' + m.langas + ')');

    // Lakštas — atidarom ir palyginam su etalonu (demo .sh / .krow)
    await p.evaluate(() => document.querySelector('.kalbos-mygtukas').click());
    await p.waitForTimeout(600);
    const l = await p.evaluate(() => {
      const r = e => e.getBoundingClientRect();
      const sh = document.querySelector('.kalbos-lakstas');
      if (!sh) return null;
      const cs = getComputedStyle(sh);
      const eil = [...sh.querySelectorAll('.kalbos-eilute')].filter(e => r(e).width > 0);
      const e0 = eil[0], f = e0 && e0.querySelector('.fi');
      const ant = sh.querySelector('.kalbos-antraste');
      const rank = sh.querySelector('.kalbos-lakstas-rankena');
      const akt = sh.querySelector('.kalbos-eilute.is-on');
      return { radius: cs.borderTopLeftRadius,
               rankena: rank ? Math.round(r(rank).width) + '×' + Math.round(r(rank).height) : null,
               antraste: ant ? ant.textContent.trim() : null,
               antrastesDydis: ant ? getComputedStyle(ant).fontSize : null,
               eiluciu: eil.length,
               eilutesAukstis: e0 ? Math.round(r(e0).height) : null,
               veliava: f ? Math.round(r(f).width) + '×' + Math.round(r(f).height) : null,
               lygiuote: e0 ? getComputedStyle(e0).textAlign : null,
               vardas: e0 ? (e0.querySelector('.kalbos-vardas') || {}).textContent : null,
               varnele: !!(akt && akt.querySelector('.kalbos-varnele')) };
    });
    console.log('    lakštas:  ' + JSON.stringify(l));
    tik(l && l.radius === '20px', w + ' — lakšto apvalinimas ne 20 px (' + (l||{}).radius + ')');
    tik(l && l.rankena === '40×4', w + ' — rankenėlė ne 40×4 (' + (l||{}).rankena + ')');
    tik(l && l.antraste === 'Kalba', w + ' — lakšto antraštė ne „Kalba"');
    tik(l && l.eilutesAukstis === 48, w + ' — eilutė ne 48 px (' + (l||{}).eilutesAukstis + ')');
    tik(l && l.veliava === '24×18', w + ' — lakšto vėliava ne 24×18 (' + (l||{}).veliava + ')');
    tik(l && l.lygiuote === 'left', w + ' — lakšto tekstas ne kairėje (' + (l||{}).lygiuote + ')');
    tik(l && l.varnele, w + ' — aktyvi kalba be varnelės');

    await p.screenshot({ path: EKRANAI + '/mob-antraste-' + (GYVAI ? 'gyva-' : '') + w + '.png' });
    await p.close();
  }

  console.log('\nGerai: ' + gerai + ', blogai: ' + blogai);
  await b.close();
  process.exit(blogai ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
