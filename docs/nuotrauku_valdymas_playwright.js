/* NUOTRAUKŲ VALDYMAS SKELBIMO FORMOJE — TELEFONE IRGI.
 *
 * Trynimo „×" ir kiti mygtukai buvo paslėpti per
 * `opacity-0 group-hover:opacity-100`. Telefone `:hover` neįvyksta, tad
 * žmogus matė tik numerius ir negalėjo nei ištrinti, nei pakeisti
 * pagrindinės nuotraukos. Tvarkos keitimas rėmėsi HTML5 „drag and drop",
 * kurio liesti ekranai nekelia visai.
 *
 * Tikrinam TIKRĄ apskaičiuotą matomumą telefono dydžio lange su
 * `hover: none`, o perstūmimą — tikru paspaudimu.
 *
 * Paleidimas: SP=<scratchpad> node docs/nuotrauku_valdymas_playwright.js
 */
const path = require('path');
const { paleisk } = require(path.join(__dirname, 'patikra', 'nuotrauka.js'));
const { execFileSync } = require('child_process');

// CDN (tailwind, font-awesome) naršyklei per agentų tarpinį nepasiekiami —
// parsiunčiam curl'u, kad nuotrauka atrodytų kaip tikras puslapis.
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
const { prisijunk } = require(path.join(__dirname, 'patikra', 'pk2.js'));
const A = process.env.ADRESAS || 'http://127.0.0.1:8899';

let gerai = 0, blogai = 0;
const tikrink = (s, k) => { if (s) gerai++; else { blogai++; console.log('  NEPAVYKO: ' + k); } };

(async () => {
  const b = await paleisk();

  for (const [vardas, w, h, telefonas] of [['telefonas', 390, 844, true],
                                           ['darbalaukis', 1400, 1000, false]]) {
    const ctx = await b.newContext({
      viewport: { width: w, height: h },
      hasTouch: telefonas, isMobile: telefonas,
      // hover:none — būtent tai lemia, ar group-hover suveiks
      ...(telefonas ? { reducedMotion: 'reduce' } : {}),
    });
    const p = await ctx.newPage();
    // Trynimas klausia patvirtinimo (confirm). Playwright be šito
    // dialogus tyliai atmeta — ir testas „ištrina" nieko.
    p.on('dialog', function (d) { d.accept(); });
    await p.route('**/*', (route) => {
      const url = route.request().url();
      if (url.startsWith(A) || url.startsWith('file://')) return route.continue();
      const body = imk(url);
      if (!body) return route.abort();
      route.fulfill({ status: 200, contentType: tipas(url), body });
    });
    await prisijunk(p);
    await p.goto(A + (process.env.FORMA || '/create/cars/quick/'),
                 { waitUntil: 'domcontentloaded', timeout: 90000 });
    await p.waitForTimeout(3000);

    // Įkeliam per TIKRĄ formos lauką — tuo pačiu patikrinam ir nuoseklų
    // siuntimą: jei jis lūžtų, miniatiūrų neatsirastų.
    const SP = process.env.SP || '/tmp';
    const jau = await p.evaluate(() =>
      document.querySelectorAll('#draft-photos > div[data-img-id], '
        + '#existing-photos > div[data-existing-img-id]').length);
    if (jau < 2) {
      await p.setInputFiles('#imageInput', [SP + '/foto1.jpg', SP + '/foto2.jpg']);
      await p.waitForTimeout(9000);
    }

    const b1 = await p.evaluate(() => {
      const sel = '#draft-photos > div[data-img-id], '
                + '#existing-photos > div[data-existing-img-id]';
      const kort = [...document.querySelectorAll(sel)];
      if (!kort.length) return { nera: true };
      const pirma = kort[0];
      const trinti = pirma.querySelector('button[title], button');
      const kaire = pirma.querySelector('.foto-perstumti-kaire');
      const desine = pirma.querySelector('.foto-perstumti-desine');
      const st = (el) => el ? getComputedStyle(el) : null;
      return {
        kiek: kort.length,
        trintiYra: !!trinti,
        trintiOpacity: trinti ? st(trinti).opacity : null,
        kaireYra: !!kaire, desineYra: !!desine,
        // Pirmos kortelės „kairėn" yra IŠJUNGTAS (nėra kur stumti), o
        // išjungtas mygtukas sąmoningai blankus. Matomumą tikrinam ant
        // veikiančio „dešinėn".
        desineOpacity: desine ? st(desine).opacity : null,
        kaireIsjungta: kaire ? kaire.disabled : null,
        desineIsjungta: desine ? desine.disabled : null,
        hoverNone: window.matchMedia('(hover: none)').matches,
      };
    });
    console.log(`  ${vardas}: ${JSON.stringify(b1)}`);
    if (b1.nera) { tikrink(false, `${vardas}: juodraštyje nėra nuotraukų — nėra ko tikrinti`); await ctx.close(); continue; }

    tikrink(b1.kaireYra && b1.desineYra, `${vardas}: nėra perstūmimo mygtukų`);
    tikrink(b1.kaireIsjungta === true, `${vardas}: pirmos nuotraukos „kairėn" turi būti neaktyvus`);
    if (b1.hoverNone) {
      tikrink(b1.trintiOpacity === '1',
        `${vardas}: trynimo mygtukas nematomas (opacity ${b1.trintiOpacity})`);
      tikrink(b1.desineOpacity === '1', `${vardas}: perstūmimo mygtukas nematomas`);
    }

    // Perstūmimas TIKRU paspaudimu: antra nuotrauka į pirmą vietą
    if (b1.kiek >= 2) {
      const pries = await p.evaluate(() =>
        [...document.querySelectorAll('#draft-photos > div[data-img-id], '
          + '#existing-photos > div[data-existing-img-id]')]
          .map(e => e.dataset.imgId || e.dataset.existingImgId));
      await p.evaluate(() => {
        const kort = [...document.querySelectorAll('#draft-photos > div[data-img-id], '
          + '#existing-photos > div[data-existing-img-id]')];
        kort[1].querySelector('.foto-perstumti-kaire').click();
      });
      await p.waitForTimeout(1200);
      const po = await p.evaluate(() =>
        [...document.querySelectorAll('#draft-photos > div[data-img-id], '
          + '#existing-photos > div[data-existing-img-id]')]
          .map(e => e.dataset.imgId || e.dataset.existingImgId));
      tikrink(po[0] === pries[1] && po[1] === pries[0],
        `${vardas}: perstūmimas nesuveikė: ${pries} → ${po}`);
      const naujaPagrindine = await p.evaluate(() => {
        const pirma = document.querySelector('#draft-photos > div[data-img-id], '
          + '#existing-photos > div[data-existing-img-id]');
        return pirma.className.indexOf('border-green-500') !== -1;
      });
      tikrink(naujaPagrindine, `${vardas}: pirma nuotrauka nepažymėta kaip pagrindinė`);
      console.log(`  ${vardas}: tvarka ${pries} → ${po}`);
    }

    if (telefonas) {
      const el0 = await p.$('#draft-photos-wrapper');
      if (el0) {
        await el0.scrollIntoViewIfNeeded();
        await p.waitForTimeout(400);
        await el0.screenshot({ path: (process.env.SP || '/tmp') + '/nuotrauku-valdymas.png' });
      }
    }

    // Trynimas — tikru paspaudimu
    const priesTrinant = await p.evaluate(() =>
      document.querySelectorAll('#draft-photos > div[data-img-id], '
        + '#existing-photos > div[data-existing-img-id]').length);
    await p.evaluate(() => {
      const k = document.querySelector('#draft-photos > div[data-img-id], '
        + '#existing-photos > div[data-existing-img-id]');
      [...k.querySelectorAll('button')]
        .find(b => b.textContent.trim() === '×').click();
    });
    // Dalis formų po trynimo perkrauna puslapį. Kad neskaičiuotume
    // vidury navigacijos, palaukiam ir atsidarom puslapį iš naujo —
    // taip matome tikrą serverio būklę, ne pusiau nugriautą DOM.
    await p.waitForTimeout(3000);
    await p.goto(A + (process.env.FORMA || '/create/cars/quick/'),
                 { waitUntil: 'domcontentloaded', timeout: 90000 });
    await p.waitForTimeout(2500);
    const poTrynimo = await p.evaluate(() => ({
      kiek: document.querySelectorAll('#draft-photos > div[data-img-id]').length,
      skaitiklis: (document.getElementById('draft-photos-count') || {}).textContent,
    }));
    // Tikslų likutį tikrina docs/ikelimo_keliai_test.py prie DB; čia
    // svarbu, kad paspaudimas TIKRAI ką nors pašalino (o ne tik
    // paslėpė). Perkraunančiose formose skaičius po navigacijos gali
    // būti ir mažesnis — svarbu, kad ne toks pat.
    tikrink(poTrynimo.kiek < priesTrinant,
      `${vardas}: po trynimo liko ${poTrynimo.kiek}, buvo ${priesTrinant}`);
    // Skaitiklį turi ne visos formos — tikrinam tik ten, kur jis yra.
    if (poTrynimo.skaitiklis) {
      tikrink(poTrynimo.skaitiklis.indexOf('(' + poTrynimo.kiek + ' /') === 0,
        `${vardas}: skaitiklis neatsinaujino: ${poTrynimo.skaitiklis}`);
    }
    console.log(`  ${vardas}: trynimas ${priesTrinant} → ${poTrynimo.kiek}, skaitiklis ${poTrynimo.skaitiklis}`);

    // Išėjimo sargas: kol siuntimo nėra, jokio įspėjimo
    const sargas = await p.evaluate(() => typeof window.alIkelimuVyksta === 'function'
      ? { yra: true, vyksta: window.alIkelimuVyksta() } : { yra: false });
    tikrink(sargas.yra, `${vardas}: išėjimo sargo nėra`);
    tikrink(sargas.vyksta === 0, `${vardas}: sargas mano, kad siuntimas vyksta`);

    await ctx.close();
  }

  await b.close();
  console.log('\n' + '='.repeat(60));
  console.log(`gerai: ${gerai}, nepavyko: ${blogai}`);
  process.exit(blogai ? 1 : 0);
})();
