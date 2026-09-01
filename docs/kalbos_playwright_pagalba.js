/* Ekrano nuotraukos vietiniam serveriui.
   CDN (tailwind, flag-icons, font-awesome) naršyklei per agentų tarpinį
   nepasiekiami, todėl juos parsiunčiam curl'u ir atiduodam patys. */
const { chromium } = require(process.env.SP + '/node_modules/playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');

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
  return 'application/octet-stream';
}

async function paruosti(b, w, h) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  await p.route('**/*', async (route) => {
    const url = route.request().url();
    if (url.startsWith('http://127.0.0.1:8899')) return route.continue();
    const body = parsiusti(url);
    if (!body) return route.abort();
    route.fulfill({ status: 200, contentType: tipas(url), body });
  });
  return p;
}

module.exports = { chromium, paruosti };
