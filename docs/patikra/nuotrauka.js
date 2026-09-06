/* Ekrano nuotraukos vietiniam serveriui — BENDRA dalis visiems
 * docs/*_playwright.js testams.
 *
 * Anksčiau šitas failas gyveno tik laikinajame kataloge ($SP), o repo
 * gulėjo 13 testų, kurie be jo nepasileidžia. Sesijai pasibaigus jie
 * tapdavo nebepaleidžiami. Dabar jis čia, o $SP lieka atsarginiu keliu.
 *
 * CDN (tailwind, flag-icons, font-awesome) naršyklei per agentų tarpinį
 * nepasiekiami, todėl juos parsiunčiam curl'u ir atiduodam patys.
 */
const { execFileSync } = require('child_process');
const path = require('path');

// Playwright gyvena arba projekte, arba laikinajame kataloge.
function imkPlaywright() {
  const keliai = [];
  if (process.env.SP) keliai.push(path.join(process.env.SP, 'node_modules', 'playwright'));
  keliai.push('playwright');
  for (const k of keliai) {
    try { return require(k); } catch (e) { /* bandom kitą */ }
  }
  throw new Error('Playwright nerastas. Įdiek jį arba nurodyk SP katalogą, '
                  + 'kuriame yra node_modules/playwright.');
}
const { chromium } = imkPlaywright();

// Konteineryje naršyklė guli čia; kitur — kaip Playwright pats randa.
const NARSYKLE = process.env.CHROMIUM
  || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const kesas = new Map();
function parsiusti(url) {
  if (kesas.has(url)) return kesas.get(url);
  try {
    const buf = execFileSync('curl', ['-sSL', '--max-time', '30', url], { maxBuffer: 64e6 });
    kesas.set(url, buf);
    return buf;
  } catch (e) { kesas.set(url, null); return null; }
}
function tipas(url) {
  if (/\.css(\?|$)/.test(url)) return 'text/css';
  if (/\.js(\?|$)/.test(url) || url.includes('cdn.tailwindcss.com')) return 'application/javascript';
  if (/\.svg(\?|$)/.test(url)) return 'image/svg+xml';
  if (/\.woff2(\?|$)/.test(url)) return 'font/woff2';
  if (/\.woff(\?|$)/.test(url)) return 'font/woff';
  if (/\.png(\?|$)/.test(url)) return 'image/png';
  if (/\.jpe?g(\?|$)/.test(url)) return 'image/jpeg';
  return 'application/octet-stream';
}

async function paruosti(b, w, h) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  await p.route('**/*', async (route) => {
    const url = route.request().url();
    if (url.startsWith('http://127.0.0.1:8899') || url.startsWith('file://')) return route.continue();
    const body = parsiusti(url);
    if (!body) return route.abort();
    route.fulfill({ status: 200, contentType: tipas(url), body });
  });
  return p;
}

/* Paleidžia naršyklę vienoda tvarka visiems testams. */
async function paleisk() {
  return chromium.launch({ executablePath: NARSYKLE, args: ['--no-sandbox'] });
}

module.exports = { chromium, paruosti, paleisk, NARSYKLE };
