/* KALBOS PERJUNGIKLIS MATOMAS VISUOSE PLOČIUOSE.
 *
 * Iki 2026-09-02 ties ≤360 px antraštės vėliavėlė buvo slepiama. 360 CSS
 * px (720 fizinių, DPR 2) yra dažniausias Android plotis, tad kalbos
 * nematydavo didelė dalis žmonių. Dabar vietoj apskritimo — siauras
 * tekstinis „lt ▾", telpantis ir 320 px ekrane.
 *
 * Testas krenta, jei bent viename plotyje perjungiklio nėra, jis
 * nepaspaudžiamas arba antraštė išsiplečia už ekrano.
 *
 * Paleidimas:  SP=<scratchpad> node docs/kalbos_perjungiklis_playwright.js
 *              SP=<scratchpad> GYVAI=1 node docs/kalbos_perjungiklis_playwright.js
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
    const p = await paruosti(b, w, 780);
    await p.goto(A + '/', { waitUntil: 'domcontentloaded', timeout: 90000 });
    await p.waitForTimeout(GYVAI ? 2500 : 1800);

    const m = await p.evaluate(() => {
      const el = document.querySelector('.kalbos-mygtukas');
      if (!el) return { yra: false };
      const cs = getComputedStyle(el), r = el.getBoundingClientRect();
      const kodas = el.querySelector('.kalbos-kodas');
      const svg = el.querySelector('svg');
      return {
        yra: true,
        matomas: r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none',
        plotis: Math.round(r.width), aukstis: Math.round(r.height),
        kairys: Math.round(r.left), desinys: Math.round(r.right),
        tekstas: kodas ? kodas.textContent.trim() : null,
        rodykle: svg ? Math.round(svg.getBoundingClientRect().width) : null,
        fonas: cs.backgroundColor, remelis: cs.borderTopWidth,
        langas: window.innerWidth,
        puslapioPlotis: document.documentElement.scrollWidth,
      };
    });

    console.log('  ' + String(w).padStart(3) + ' px: ' + JSON.stringify(m));
    tik(m.yra && m.matomas, w + ' px — perjungiklio NĖRA arba jis paslėptas');
    tik(m.tekstas && /^[a-z]{2}$/.test(m.tekstas), w + ' px — nėra kalbos kodo („' + m.tekstas + '")');
    tik(m.rodykle && m.rodykle <= 14, w + ' px — rodyklė ne 12 px (' + m.rodykle + ')');
    tik(m.desinys <= m.langas + 1 && m.kairys >= -1, w + ' px — perjungiklis išlipęs už ekrano');
    tik(m.puslapioPlotis <= m.langas + 1,
        w + ' px — antraštė plečia puslapį (' + m.puslapioPlotis + ' > ' + m.langas + ')');

    // Paspaudžiamas ir atidaro sąrašą
    await p.evaluate(() => document.querySelector('.kalbos-mygtukas').click());
    await p.waitForTimeout(600);
    const kalbos = await p.evaluate(() =>
      [...document.querySelectorAll('.kalbos-lakstas .kalbos-eilute')]
        .filter(e => e.getClientRects().length).length);
    tik(kalbos > 1, w + ' px — sąrašas neatsidaro (eilučių ' + kalbos + ')');

    await p.screenshot({ path: EKRANAI + '/kalba-' + (GYVAI ? 'gyva-' : '') + w + '.png' });
    await p.close();
  }

  console.log('\nGerai: ' + gerai + ', blogai: ' + blogai);
  await b.close();
  process.exit(blogai ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
