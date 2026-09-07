/* FORMŲ VAIZDO PALYGINIMAS — „prieš" ir „po".
 *
 * Bendrinama tik logika, ne išvaizda: iškėlus bloką į partial'ą arba
 * pakeitus kainos sufiksą, forma privalo atrodyti taip pat. Šitas
 * daro ekrano nuotraukas keturių kategorijų ir jas palygina baitas į
 * baitą su ankstesnėmis.
 *
 * Paleidimas:
 *   SP=<scratchpad> ETIKETE=pries node docs/formu_vaizdo_palyginimas.js
 *   ... pakeitimai ...
 *   SP=<scratchpad> ETIKETE=po PALYGINTI=pries node docs/formu_vaizdo_palyginimas.js
 */
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const { execFileSync } = require('child_process');
const { paleisk } = require(path.join(__dirname, 'patikra', 'nuotrauka.js'));
const { prisijunk, A } = require(path.join(__dirname, 'patikra', 'pk2.js'));

const FORMOS = {
  cars: '/create/cars/quick/',
  trucks: '/create/trucks/',
  agriculture: '/create/agriculture/',
  parts: '/create/parts/form/?sub=engine',
};

const SP = process.env.SP || '/tmp';
const ETIKETE = process.env.ETIKETE || 'pries';
const PALYGINTI = process.env.PALYGINTI || '';
const KATALOGAS = path.join(SP, 'vaizdai');

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

(async () => {
  fs.mkdirSync(KATALOGAS, { recursive: true });
  const b = await paleisk();
  const rezultatai = [];

  for (const [vardas, kelias] of Object.entries(FORMOS)) {
    for (const [irenginys, matmenys] of Object.entries({
      telefonas: { width: 390, height: 844, isMobile: true, hasTouch: true },
      darbalaukis: { width: 1280, height: 900 },
    })) {
      const ctx = await b.newContext({ viewport: matmenys, isMobile: !!matmenys.isMobile });
      const p = await ctx.newPage();
      await p.route('**/*', (route) => {
        const url = route.request().url();
        if (url.startsWith(A)) return route.continue();
        const body = imk(url);
        if (!body) return route.abort();
        route.fulfill({ status: 200, contentType: tipas(url), body });
      });
      await prisijunk(p);
      await p.goto(A + kelias, { waitUntil: 'domcontentloaded', timeout: 90000 });
      await p.waitForTimeout(2500);
      // Animacijos ir „nauja" ženklai laiko nefiksuoja — išjungiam
      await p.addStyleTag({ content: '*{animation:none!important;transition:none!important;caret-color:transparent!important}' });
      const failas = path.join(KATALOGAS, `${vardas}-${irenginys}-${ETIKETE}.png`);
      await p.screenshot({ path: failas, fullPage: true });
      const suma = crypto.createHash('sha256').update(fs.readFileSync(failas)).digest('hex').slice(0, 12);
      rezultatai.push({ vardas, irenginys, failas, suma });
      console.log(`  ${vardas} / ${irenginys}: ${suma}`);
      await ctx.close();
    }
  }
  await b.close();

  if (!PALYGINTI) {
    console.log(`\nIšsaugota kaip „${ETIKETE}". Po pakeitimų paleisk su ` +
                `ETIKETE=po PALYGINTI=${ETIKETE}`);
    return;
  }

  let skiriasi = 0;
  console.log('\n── Palyginimas su „' + PALYGINTI + '" ──');
  for (const r of rezultatai) {
    const senas = path.join(KATALOGAS, `${r.vardas}-${r.irenginys}-${PALYGINTI}.png`);
    if (!fs.existsSync(senas)) { console.log(`  ${r.vardas}/${r.irenginys}: nėra „prieš"`); continue; }
    const senaSuma = crypto.createHash('sha256').update(fs.readFileSync(senas)).digest('hex').slice(0, 12);
    const vienoda = senaSuma === r.suma;
    if (!vienoda) skiriasi++;
    console.log(`  ${vienoda ? 'VIENODA' : 'SKIRIASI'}  ${r.vardas}/${r.irenginys}` +
                (vienoda ? '' : `  (${senaSuma} → ${r.suma})`));
  }
  console.log('\n' + '='.repeat(60));
  console.log(skiriasi ? `SKIRIASI: ${skiriasi} vaizdai — peržiūrėk juos` : 'Vaizdas nepakito');
  process.exit(skiriasi ? 1 : 0);
})();
