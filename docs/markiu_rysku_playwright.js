/* MARKĖS BE SKELBIMŲ RODOMOS TOKIU PAT RYŠKIU TEKSTU KAIP IR SU SKELBIMAIS.
 *
 * Anksčiau eilutė su „(0)" gaudavo .is-tuscia ir pilkėdavo — atrodė
 * neaktyvi, nors ją paspausti galima (autogidas jas rodo ryškias).
 * Tikrinam ne klasės buvimą, o TIKRĄ apskaičiuotą spalvą: jei kas nors
 * blankinimą grąžins kitu keliu, testas vis tiek kris.
 *
 * Paleidimas: node docs/markiu_rysku_playwright.js
 */
const path = require('path');
const { paruosti, paleisk } = require(path.join(__dirname, 'patikra', 'nuotrauka.js'));
const A = process.env.ADRESAS || 'http://127.0.0.1:8899';

let gerai = 0, blogai = 0;
const tikrink = (s, k) => { if (s) gerai++; else { blogai++; console.log('  NEPAVYKO: ' + k); } };

(async () => {
  const b = await paleisk();
  const p = await paruosti(b, 1400, 1000);

  // Markių sąrašą atiduodam patys: vietinėje DB visos markės turi
  // skelbimų, o tikrinti reikia būtent eilutę su „(0)". Šitaip patikra
  // nepriklauso nuo duomenų ir tikrina tai, kas pakeista — šabloną ir CSS.
  await p.route('**/ajax/markes/**', (route) => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      kategorija: 'cars', param: 'brand', viso: 3,
      // Visų varduose yra „a" — paieška „a" parodys ir turinčias
      // skelbimų, ir tuščias, tad bus ką lyginti.
      markes: [{ v: '1', n: 'Mazda', c: 1 },
               { v: '2', n: 'Audi', c: 0 },
               { v: '3', n: 'Skoda', c: 0 }],
    }),
  }));

  await p.goto(A + '/?section=cars&sidebar=1', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(2500);

  // Atidarom markių sąrašą
  const atidaryta = await p.evaluate(() => {
    const btn = [...document.querySelectorAll('.sp-dd-btn, [x-data] .sp-fld')]
      .find(e => /mark/i.test(e.textContent) || /mark/i.test(e.placeholder || ''));
    if (!btn) return false;
    btn.click();
    return true;
  });
  tikrink(atidaryta, 'markių lauko nerasta');
  await p.waitForTimeout(2000);

  // Markės be skelbimų sąraše slepiamos, kol neieškai (onlyWithAds) —
  // tos elgsenos nekeitėm. Įvedam ir ištrinam raidę: po to sąraše lieka
  // visos, įskaitant nulines.
  await p.evaluate(() => {
    const inp = document.querySelector('.sp-dd-search input');
    if (!inp) return;
    inp.value = 'a';
    inp.dispatchEvent(new Event('input', { bubbles: true }));
  });
  await p.waitForTimeout(1200);

  const eilutes = await p.evaluate(() => {
    const out = [];
    for (const el of document.querySelectorAll('.sp-dd-item')) {
      const r = el.getBoundingClientRect();
      if (!r.width) continue;
      const cnt = el.querySelector('.sp-dd-count');
      if (!cnt) continue;                       // „Visos markės" — be skaičiaus
      const st = getComputedStyle(el);
      out.push({
        vardas: (el.querySelector('span:not(.sp-dd-count)') || {}).textContent || '',
        skaicius: cnt.textContent.trim(),
        spalva: st.color,
        permatomumas: st.opacity,
        klases: el.className,
      });
    }
    return out;
  });

  console.log('  rasta eilučių su skaičiumi:', eilutes.length);
  tikrink(eilutes.length >= 2, 'per mažai markių sąraše, nėra ką lyginti');

  const nuliniai = eilutes.filter(e => /\(0\)/.test(e.skaicius));
  const neNuliniai = eilutes.filter(e => !/\(0\)/.test(e.skaicius));
  console.log('  su (0):', nuliniai.length, '| su skelbimais:', neNuliniai.length);
  tikrink(nuliniai.length >= 1, 'nėra nė vienos markės su (0) — patikra beprasmė');
  tikrink(neNuliniai.length >= 1, 'nėra nė vienos markės su skelbimais');

  if (nuliniai.length && neNuliniai.length) {
    const etalonas = neNuliniai[0];
    for (const e of nuliniai) {
      tikrink(e.spalva === etalonas.spalva,
        `„${e.vardas.trim()} ${e.skaicius}" spalva ${e.spalva}, o „${etalonas.vardas.trim()} ${etalonas.skaicius}" ${etalonas.spalva}`);
      tikrink(e.permatomumas === etalonas.permatomumas,
        `„${e.vardas.trim()}" opacity ${e.permatomumas} vs ${etalonas.permatomumas}`);
      tikrink(!/is-tuscia|opacity|muted|disabled/.test(e.klases),
        `„${e.vardas.trim()}" turi blankinimo klasę: ${e.klases}`);
    }
    console.log(`  etalonas: ${etalonas.vardas.trim()} ${etalonas.skaicius} → ${etalonas.spalva}`);
    for (const e of nuliniai) console.log(`  su (0):   ${e.vardas.trim()} ${e.skaicius} → ${e.spalva}`);
  }

  // Skaičius skliaustuose privalo likti
  tikrink(eilutes.every(e => /^\(\d+\)$/.test(e.skaicius)),
    'skaičius skliaustuose dingo arba pasikeitė pavidalas');

  await p.screenshot({ path: (process.env.SP || '/tmp') + '/markes-sarasas.png' });
  await b.close();
  console.log('\n' + '='.repeat(60));
  console.log(`gerai: ${gerai}, nepavyko: ${blogai}`);
  process.exit(blogai ? 1 : 0);
})();
