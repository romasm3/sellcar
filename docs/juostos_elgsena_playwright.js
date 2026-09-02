/* ŠONINĖ JUOSTA RENKA REIKŠMES, O NE PERKRAUNA PUSLAPĮ.
 *
 * Viena taisyklė visiems juostos laukams: pasirinkimas keičia tik
 * vietinę būseną ir lauko užrašą, adresas NEPASIKEIČIA, o skaičius ant
 * „Filtruoti" atsinaujina gyvai. Adresą keičia tik „Filtruoti".
 *
 * Scenarijus (žmogaus prašymas 2026-09-02):
 *   pasirenku šalį, kurą ir markę  →  adresas nepasikeičia,
 *                                     skaičius pasikeičia tris kartus;
 *   spaudžiu „Filtruoti"           →  adresas atnaujinamas VIENU kartu
 *                                     su visais trimis.
 * Plius trys konkrečios klaidos, dėl kurių šitas testas atsirado:
 *   1. markės/modelio × neišsitrindavo (grįždavo iš paslėptų kopijų);
 *   2. šalis persikraudavo iškart (punktas buvo nuoroda);
 *   3. „Galia, kW" nerodydavo pasirinkimo (datalist reikšmės tekstinės).
 *
 * Paleidimas:  SP=<scratchpad> node docs/juostos_elgsena_playwright.js
 */
const { chromium, paruosti } = require(process.env.SP + '/nuotrauka.js');
const A = 'http://127.0.0.1:8899';
const KELIAS = '/?section=cars&sidebar=1';

let gerai = 0, blogai = 0;
const tik = (s, k) => { s ? gerai++ : (blogai++, console.log('  NEPAVYKO: ' + k)); };
const antraste = (t) => console.log('\n── ' + t + ' ' + '─'.repeat(Math.max(0, 52 - t.length)));

const skaicius = (p) => p.evaluate(() => (document.getElementById('sidebarCount') || {}).textContent);
const adresas = (p) => p.evaluate(() => location.href);

// Lipnus antraštės sluoksnis perima tikrus paspaudimus, todėl spaudžiam
// programiškai — matomumą tikrinam atskirai.
const spusk = (p, sel, nr) => p.evaluate(([s, n]) => {
  const e = [...document.querySelectorAll(s)].filter(el => el.getClientRects().length)[n || 0];
  if (!e) return false;
  e.click(); return true;
}, [sel, nr || 0]);

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox'] });
  const p = await paruosti(b, 1600, 1100);

  antraste('1. Trys pasirinkimai — adresas nejuda, skaičius juda');
  await p.goto(A + KELIAS, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(2500);
  const pradinis = await adresas(p);
  const sk = [await skaicius(p)];

  // ŠALIS
  await spusk(p, '.sp-side-card .salis-keisti-mazas');
  await p.waitForTimeout(300);
  const salisMatosi = await p.evaluate(() =>
    [...document.querySelectorAll('.sp-side-card .salis-eil')].filter(e => e.getClientRects().length).length);
  tik(salisMatosi > 1, 'šalių sąrašas atsidaro juostoje (matomų eilučių ' + salisMatosi + ')');
  // Antra eilutė — ne dabartinė šalis
  await p.evaluate(() => {
    const e = [...document.querySelectorAll('.sp-side-card .salis-eil')]
      .filter(el => el.getClientRects().length && !el.classList.contains('is-on'))[0];
    if (e) e.click();
  });
  await p.waitForTimeout(900);
  tik(await adresas(p) === pradinis, 'pasirinkus šalį adresas NEPASIKEITĖ');
  sk.push(await skaicius(p));

  // KURAS — pirmas checkbox „Kuro tipas" bloke
  await p.evaluate(() => {
    const cb = document.querySelector('.sp-side-card input[type=checkbox][name="fuel_type"], '
                                    + '.sp-side-card input[type=checkbox][name="fuel_type_chk"]');
    if (cb) { cb.click(); }
  });
  await p.waitForTimeout(900);
  tik(await adresas(p) === pradinis, 'pasirinkus kurą adresas NEPASIKEITĖ');
  sk.push(await skaicius(p));

  // MARKĖ — atidarom pirmą markių sąrašą ir renkam pirmą įrašą
  await spusk(p, '.sp-side-card .sp-dd-btn');
  await p.waitForTimeout(1200);
  await p.evaluate(() => {
    const it = [...document.querySelectorAll('.sp-side-card .sp-dd-item')]
      .filter(e => e.getClientRects().length && !e.classList.contains('font-semibold'))[0];
    if (it) it.click();
  });
  await p.waitForTimeout(900);
  tik(await adresas(p) === pradinis, 'pasirinkus markę adresas NEPASIKEITĖ');
  sk.push(await skaicius(p));

  console.log('  skaičius ant „Filtruoti": ' + sk.join(' → '));
  console.log('  adresas per visus tris pasirinkimus: ' + (await adresas(p)));
  const unik = [...new Set(sk)];
  tik(sk.length === 4 && unik.length >= 2, 'skaičius ant mygtuko keitėsi: ' + sk.join(' → '));
  const markesUzrasas = await p.evaluate(() =>
    (document.querySelector('.sp-side-card .sp-dd-btn span') || {}).textContent.trim());
  tik(markesUzrasas && !/Visos markės/.test(markesUzrasas), 'markės laukas rodo pasirinkimą: ' + markesUzrasas);

  antraste('2. „Filtruoti" — adresas atnaujinamas vienu kartu');
  const laukiam = p.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 });
  await spusk(p, '.sp-side-card .sb-apply button[type=submit]');
  await laukiam;
  await p.waitForTimeout(1200);
  const naujas = new URL(await adresas(p));
  const q = naujas.searchParams;
  console.log('  adresas po „Filtruoti": ' + naujas.search.slice(0, 160));
  tik(q.get('salis'), 'adrese yra šalis: salis=' + q.get('salis'));
  tik(q.get('fuel_type') || q.get('fuel_type_chk'), 'adrese yra kuras: ' + (q.get('fuel_type') || q.get('fuel_type_chk')));
  tik(q.getAll('brand').filter(Boolean).length === 1,
      'adrese lygiai viena markė: ' + JSON.stringify(q.getAll('brand')));
  tik(q.getAll('brand').length === 1,
      'tuščios markės kopijos nesiunčiamos: brand × ' + q.getAll('brand').length);

  antraste('3. Markės/modelio × išvalo ir NEPERKRAUNA');
  await p.goto(A + KELIAS + '&brand=1&brand=2', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(2500);
  const priesX = await adresas(p);
  const siunciamos = () => p.evaluate(() =>
    [...document.querySelectorAll('#sidebarForm input[name="brand"]')]
      .filter(i => !i.disabled).map(i => i.value).filter(Boolean));
  const markesPries = await siunciamos();
  tik(markesPries.length === 2, 'pradžioje dvi markės: ' + JSON.stringify(markesPries));

  await spusk(p, '.sp-side-card [data-pair-row] .pair-x-sm');
  await p.waitForTimeout(900);
  tik(await adresas(p) === priesX, '× NEPERKROVĖ puslapio');
  const markesPo = await siunciamos();
  tik(markesPo.length === 1 && markesPo[0] === markesPries[0],
      'liko viena markė: ' + JSON.stringify(markesPo));

  const laukiam2 = p.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 });
  await spusk(p, '.sp-side-card .sb-apply button[type=submit]');
  await laukiam2;
  await p.waitForTimeout(800);
  const poX = new URL(await adresas(p)).searchParams.getAll('brand');
  console.log('  adresas po × + „Filtruoti": ' + (await adresas(p)).replace(/^[^?]*/, '').slice(0, 160));
  tik(poX.length === 1 && poX[0] === markesPries[0],
      'po „Filtruoti" markė NEGRĮŽO: brand=' + JSON.stringify(poX));

  antraste('4. „Galia, kW" priima pasiūlytą reikšmę');
  await p.goto(A + KELIAS, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(2000);
  const dl = await p.evaluate(() => {
    const d = document.getElementById('dl-power_min');
    if (!d) return null;
    return [...d.options].map(o => ({ v: o.value, l: o.label }));
  });
  tik(dl && dl.length > 0, 'pasiūlymų sąrašas yra (' + (dl ? dl.length : 0) + ')');
  tik(dl && dl.every(o => /^-?\d+(\.\d+)?$/.test(o.v)),
      'visos reikšmės skaitinės, pvz. ' + JSON.stringify(dl && dl[0]));
  tik(dl && dl.some(o => /kW/.test(o.l)), 'žmogui matomas užrašas išliko: ' + (dl && dl[0] && dl[0].l));

  // Įrašytą reikšmę laukas priima ir laiko
  const laiko = await p.evaluate((v) => {
    const el = document.querySelector('.sp-side-card input[name="power_min"]');
    if (!el) return null;
    el.value = v; el.dispatchEvent(new Event('input', { bubbles: true }));
    return el.value;
  }, dl && dl[2] ? dl[2].v : '35');
  tik(laiko && laiko !== '', 'laukas išlaiko reikšmę: „' + laiko + '"');

  antraste('5. Naršyklės „atgal" grąžina ankstesnį rinkinį');
  await p.goBack({ waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(1200);
  const atgal = new URL(await adresas(p)).searchParams.getAll('brand');
  tik(atgal.length >= 1, 'grįžus filtrai vietoje: brand=' + JSON.stringify(atgal));

  console.log('\nGerai: ' + gerai + ', blogai: ' + blogai);
  await b.close();
  process.exit(blogai ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
