/* SKELBIMO GALERIJA — BRAUKYMAS PIRŠTU.
 *
 * Telefone rodyklės mažos ir dengia pačią nuotrauką; braukymas yra tai,
 * ko žmogus tikisi. Tikrinam TIKRAIS pirštų įvykiais (pointer su
 * pointerType 'touch'), ne funkcijos iškvietimu:
 *
 *   1. braukimas kairėn → kita nuotrauka;
 *   2. braukimas dešinėn → grįžta atgal;
 *   3. po braukymo NEATSIVERIA peržiūra (kitaip kiekvienas braukymas
 *      mestų žmogų į lightbox'ą);
 *   4. paspaudimas (be judesio) peržiūrą atidaro;
 *   5. vertikalus judesys nuotraukos nekeičia — kitaip slenkant
 *      puslapį galerija „šokinėtų";
 *   6. rodyklės darbalaukyje veikia kaip veikė.
 *
 * Paleidimas: SKELBIMAS=<pk> node docs/skelbimo_galerija_playwright.js
 */
const path = require('path');
const { execFileSync } = require('child_process');
const { paleisk } = require(path.join(__dirname, 'patikra', 'nuotrauka.js'));
const { prisijunk, A } = require(path.join(__dirname, 'patikra', 'pk2.js'));

const PK = process.env.SKELBIMAS || '1';
const kesas = new Map();
function imk(url) {
  if (kesas.has(url)) return kesas.get(url);
  let r = null;
  try { r = execFileSync('curl', ['-sSL', '--max-time', '30', url], { maxBuffer: 64e6 }); }
  catch (e) { r = null; }
  kesas.set(url, r); return r;
}
const tipas = (u) =>
  /\.css(\?|$)/.test(u) ? 'text/css' :
  /\.js(\?|$)/.test(u) || u.includes('cdn.tailwindcss.com') ? 'application/javascript' :
  /\.woff2(\?|$)/.test(u) ? 'font/woff2' : 'application/octet-stream';

let gerai = 0, blogai = 0;
const tikrink = (s, k) => { if (s) gerai++; else { blogai++; console.log('  NEPAVYKO: ' + k); } };

// Pirštas: pointerdown → keli pointermove → pointerup. Playwright touch
// API galerijai nepakanka, nes komponentas klauso pointer įvykių.
async function braukk(p, nuoX, ikiX, y, veiksmai = 6) {
  await p.evaluate(([x0, x1, yy, n]) => {
    const el = document.querySelector('.ld-stage');
    const ivykis = (tipas, x, y) => el.dispatchEvent(new PointerEvent(tipas, {
      clientX: x, clientY: y, bubbles: true, cancelable: true,
      pointerId: 1, pointerType: 'touch', isPrimary: true,
    }));
    ivykis('pointerdown', x0, yy);
    for (let i = 1; i <= n; i++) ivykis('pointermove', x0 + (x1 - x0) * i / n, yy);
    ivykis('pointerup', x1, yy);
  }, [nuoX, ikiX, y, veiksmai]);
  await p.waitForTimeout(400);
}

const dabartine = (p) => p.evaluate(() => {
  const el = document.querySelector('[x-data^="galerijosJuosta"]');
  return el && el._x_dataStack ? el._x_dataStack[0].currentImage : null;
});
const perziuraAtidaryta = (p) => p.evaluate(() => {
  const lb = document.getElementById('lb');
  return !!lb && getComputedStyle(lb).display !== 'none';
});

(async () => {
  const b = await paleisk();
  const ctx = await b.newContext({
    viewport: { width: 390, height: 844 },
    isMobile: true, hasTouch: true, deviceScaleFactor: 2,
  });
  const p = await ctx.newPage();
  await p.route('**/*', (route) => {
    const url = route.request().url();
    if (url.startsWith(A)) return route.continue();
    const body = imk(url);
    if (!body) return route.abort();
    route.fulfill({ status: 200, contentType: tipas(url), body });
  });
  await prisijunk(p);
  await p.goto(A + '/' + PK + '/', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(2500);

  const kiek = await p.evaluate(() => document.querySelectorAll('.ld-slide').length);
  tikrink(kiek >= 2, `skelbime tik ${kiek} nuotrauka — nėra ko braukti`);
  if (kiek < 2) { await b.close(); process.exit(1); }

  tikrink(await dabartine(p) === 0, 'pradžioje turi būti rodoma pirma nuotrauka');

  // 1. Kairėn → kita
  await braukk(p, 320, 90, 250);
  const po1 = await dabartine(p);
  tikrink(po1 === 1, `braukimas kairėn nepakeitė nuotraukos (${po1})`);
  tikrink(!(await perziuraAtidaryta(p)), 'po braukymo atsidarė peržiūra');

  // 2. Dešinėn → atgal
  await braukk(p, 90, 320, 250);
  const po2 = await dabartine(p);
  tikrink(po2 === 0, `braukimas dešinėn negrąžino atgal (${po2})`);

  // 3. Vertikalus judesys nieko nekeičia
  await p.evaluate(() => {
    const el = document.querySelector('.ld-stage');
    const ivykis = (t, x, y) => el.dispatchEvent(new PointerEvent(t, {
      clientX: x, clientY: y, bubbles: true, cancelable: true,
      pointerId: 2, pointerType: 'touch', isPrimary: true }));
    ivykis('pointerdown', 200, 120);
    ivykis('pointermove', 205, 320);
    ivykis('pointerup', 205, 330);
  });
  await p.waitForTimeout(300);
  tikrink(await dabartine(p) === 0, 'vertikalus judesys pakeitė nuotrauką');

  // 4. Trumpas paspaudimas be judesio — peržiūra atsidaro
  await p.evaluate(() => {
    const a = document.querySelector('.ld-slide .ld-link');
    const ivykis = (t) => a.dispatchEvent(new PointerEvent(t, {
      clientX: 200, clientY: 200, bubbles: true, cancelable: true,
      pointerId: 3, pointerType: 'touch', isPrimary: true }));
    ivykis('pointerdown'); ivykis('pointerup');
    a.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
  });
  await p.waitForTimeout(600);
  tikrink(await perziuraAtidaryta(p), 'paspaudus nuotrauką peržiūra neatsidarė');
  await p.keyboard.press('Escape');
  await p.waitForTimeout(400);

  // 5. Rodyklės — darbalaukyje
  const ctx2 = await b.newContext({ viewport: { width: 1280, height: 900 } });
  const d = await ctx2.newPage();
  await d.route('**/*', (route) => {
    const url = route.request().url();
    if (url.startsWith(A)) return route.continue();
    const body = imk(url);
    if (!body) return route.abort();
    route.fulfill({ status: 200, contentType: tipas(url), body });
  });
  await prisijunk(d);
  await d.goto(A + '/' + PK + '/', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await d.waitForTimeout(2000);
  await d.evaluate(() => document.querySelector('.ld-stage button:last-of-type').click());
  await d.waitForTimeout(400);
  const poRodykles = await dabartine(d);
  tikrink(poRodykles === 1, `rodyklė nustojo veikti darbalaukyje (${poRodykles})`);

  await b.close();
  console.log('\n' + '='.repeat(60));
  console.log(`gerai: ${gerai}, nepavyko: ${blogai}`);
  process.exit(blogai ? 1 : 0);
})();
