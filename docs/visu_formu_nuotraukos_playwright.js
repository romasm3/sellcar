/* VISOS ĮKĖLIMO FORMOS — NUOTRAUKŲ VALDYMAS TIKROJE NARŠYKLĖJE.
 *
 * docs/nuotrauku_valdymas_playwright.js tikrina VIENĄ formą giliai.
 * Šitas pereina VISAS kategorijas ir kiekvienoje reikalauja to paties:
 *
 *   1. ◀ ▶ perstūmimo mygtukai ir tikras jų veikimas;
 *   2. žalias „PAGRINDINĖ" ženklas ant pirmos nuotraukos;
 *   3. matomas trynimo mygtukas telefone (`hover: none`);
 *   4. įkėlimas po vieną — miniatiūros atsiranda ir be perkrovimo.
 *
 * Selektorių čia nerašom: imam juos iš to paties nustatymų bloko,
 * kurį skaito ir pats kodas (`[data-al-nuotraukos]`). Jei forma
 * prisijungė neteisingai, testas tai ir parodo.
 *
 * Paleidimas:
 *   SP=<scratchpad> PATIKRA_SLAPTAZODIS=… node docs/visu_formu_nuotraukos_playwright.js
 *   FORMOS=/create/wheels/,/create/trucks/  — tik pasirinktos
 */
const path = require('path');
const { execFileSync } = require('child_process');
const { paleisk } = require(path.join(__dirname, 'patikra', 'nuotrauka.js'));
const { prisijunk, puslapis, A } = require(path.join(__dirname, 'patikra', 'pk2.js'));

// „parts" formai reikia potipio adrese — be jo ji nukreipia į rinkiklį.
const VISOS = [
  '/create/agriculture/', '/create/bicycles/', '/create/boats/',
  '/create/camping-houses/', '/create/car-for-parts/', '/create/cars/quick/',
  '/create/construction/', '/create/construction/attachment/',
  '/create/electronics/', '/create/forestry/', '/create/loading-equipment/',
  '/create/moto-for-parts/', '/create/moto-part/', '/create/motogear/',
  '/create/motorcycle/', '/create/parts/form/?sub=engine',
  '/create/rental/car/',
  '/create/rental/heavy/', '/create/rental/minibus/', '/create/rental/moto/',
  '/create/rims/', '/create/services/', '/create/trailers/',
  '/create/truck-for-parts/', '/create/trucks/', '/create/tyres/',
  '/create/wheels/',
];
const FORMOS = (process.env.FORMOS || '').trim()
  ? process.env.FORMOS.split(',').map(s => s.trim()).filter(Boolean)
  : VISOS;

// CDN naršyklei per agentų tarpinį nepasiekiamas — parsiunčiam curl'u.
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

// Ta pati kortelių paieška, kaip bendrame JS: tinklelis iš nustatymų,
// kortelė — arba nurodytu selektoriumi, arba tiesioginis vaikas.
const KORTOS = `(function () {
  var el = document.querySelector('[data-al-nuotraukos]');
  if (!el) return null;
  var d = el.dataset;
  var t = document.querySelector(d.tinklelis || '#existing-photos');
  if (!t) return [];
  if (d.kortele) return [].slice.call(t.querySelectorAll(d.kortele));
  return [].filter.call(t.children, function (e) { return e.nodeType === 1; });
})()`;

(async () => {
  const b = await paleisk();
  const SP = process.env.SP || '/tmp';

  for (const kelias of FORMOS) {
    const ctx = await b.newContext({
      viewport: { width: 390, height: 844 },
      isMobile: true, hasTouch: true, deviceScaleFactor: 2,
    });
    const p = await ctx.newPage();
    await p.route('**/*', (route) => {
      const url = route.request().url();
      if (url.startsWith(A) || url.startsWith('file://')) return route.continue();
      const body = imk(url);
      if (!body) return route.abort();
      route.fulfill({ status: 200, contentType: tipas(url), body });
    });
    p.on('dialog', d => d.accept());

    try {
      await prisijunk(p);
      const r = await p.goto(A + kelias,
                             { waitUntil: 'domcontentloaded', timeout: 90000 });
      await p.waitForTimeout(2500);
      if (!r || r.status() >= 400) {
        tikrink(false, `${kelias}: puslapis grąžino ${r && r.status()}`);
        await ctx.close(); continue;
      }

      // Nustatymų blokas — be jo forma liko su savo kodu
      const n = await p.evaluate(() => {
        const el = document.querySelector('[data-al-nuotraukos]');
        return el ? Object.assign({}, el.dataset) : null;
      });
      if (!n) {
        tikrink(false, `${kelias}: nėra bendro nuotraukų bloko`);
        await ctx.close(); continue;
      }

      // Įkeliam dvi nuotraukas per tikrą formos lauką
      const ivestis = n.ivestis || '#imageInput';
      const yra = await p.evaluate(s => !!document.querySelector(s), ivestis);
      if (!yra) {
        tikrink(false, `${kelias}: nėra failų lauko ${ivestis}`);
        await ctx.close(); continue;
      }
      await p.setInputFiles(ivestis, [SP + '/foto1.jpg', SP + '/foto2.jpg']);
      await p.waitForTimeout(7000);

      const b1 = await p.evaluate(`(function () {
        var kort = ${KORTOS};
        if (!kort || !kort.length) return { nera: true };
        var pirma = kort[0];
        var zyme = pirma.querySelector('.foto-zyme');
        var trinti = pirma.querySelector('.foto-trinti, button');
        var kaire = pirma.querySelector('.foto-perstumti-kaire');
        var desine = pirma.querySelector('.foto-perstumti-desine');
        var st = function (e) { return e ? getComputedStyle(e) : null; };
        return {
          kiek: kort.length,
          zymeYra: !!zyme,
          zymeTekstas: zyme ? zyme.textContent.trim() : null,
          zymeFonas: zyme ? st(zyme).backgroundColor : null,
          trintiOpacity: trinti ? st(trinti).opacity : null,
          kaireYra: !!kaire, desineYra: !!desine,
          kaireIsjungta: kaire ? kaire.disabled : null,
          desineOpacity: desine ? st(desine).opacity : null
        };
      })()`);

      if (b1.nera) {
        tikrink(false, `${kelias}: po įkėlimo nėra nė vienos miniatiūros`);
        await ctx.close(); continue;
      }
      console.log(`  ${kelias}: ${JSON.stringify(b1)}`);

      tikrink(b1.kiek >= 2, `${kelias}: įkėlimas po vieną davė ${b1.kiek} iš 2`);
      tikrink(b1.kaireYra && b1.desineYra, `${kelias}: nėra ◀ ▶ mygtukų`);
      tikrink(b1.kaireIsjungta === true,
              `${kelias}: pirmos nuotraukos „kairėn" turi būti neaktyvus`);
      tikrink(b1.desineOpacity === '1',
              `${kelias}: ◀ ▶ nematomi telefone (opacity ${b1.desineOpacity})`);
      tikrink(b1.trintiOpacity === '1',
              `${kelias}: trynimas nematomas telefone (opacity ${b1.trintiOpacity})`);
      tikrink(b1.zymeYra, `${kelias}: nėra „PAGRINDINĖ" ženklo`);
      // Žalia — standartinė sėkmės spalva (#16a34a), ne akcentas
      tikrink(b1.zymeFonas === 'rgb(22, 163, 74)',
              `${kelias}: „PAGRINDINĖ" ne žalia (${b1.zymeFonas})`);

      // Perstūmimas TIKRU paspaudimu: antra į pirmą vietą
      if (b1.kiek >= 2) {
        const pries = await p.evaluate(`${KORTOS}.map(function (e) {
          return e.dataset.imgId || e.dataset.existingImgId || e.dataset.imageId
              || e.dataset.id || e.querySelector('img') && e.querySelector('img').src; })`);
        await p.evaluate(`${KORTOS}[1].querySelector('.foto-perstumti-kaire').click()`);
        await p.waitForTimeout(2500);
        const po = await p.evaluate(`${KORTOS}.map(function (e) {
          return e.dataset.imgId || e.dataset.existingImgId || e.dataset.imageId
              || e.dataset.id || e.querySelector('img') && e.querySelector('img').src; })`);
        tikrink(JSON.stringify(pries) !== JSON.stringify(po),
                `${kelias}: ◀ nieko nepakeitė (${pries} → ${po})`);
      }

      // Trynimas — kortelių turi sumažėti
      const kiekPries = await p.evaluate(`${KORTOS}.length`);
      await p.evaluate(`(function () {
        var k = ${KORTOS}[0];
        var b = k.querySelector('.foto-trinti')
             || k.querySelector('button[onclick*="elete"], .photo-action-btn.delete')
             || k.querySelector('button');
        if (b) b.click();
      })()`);
      await p.waitForTimeout(4000);
      const kiekPo = await p.evaluate(`(${KORTOS} || []).length`);
      tikrink(kiekPo < kiekPries,
              `${kelias}: trynimas nesumažino (${kiekPries} → ${kiekPo})`);
    } catch (e) {
      tikrink(false, `${kelias}: ${e.message.split('\n')[0]}`);
    }
    await ctx.close();
  }

  await b.close();
  console.log('\n' + '='.repeat(60));
  console.log(`formų: ${FORMOS.length}   gerai: ${gerai}, nepavyko: ${blogai}`);
  process.exit(blogai ? 1 : 0);
})();
