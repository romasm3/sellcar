/* ATIDARYTI SĄRAŠAI šoninėje juostoje — ar langas telpa ir nekerpa teksto.
 *
 * Iki 2026-09-02 juostos kortelė turėjo overflow:hidden, o .sp-dd —
 * min-width:250px prie 230px juostos. Sąrašai išlipdavo ir tekstas
 * virsdavo „Lietu…", „Vokie…".
 *
 * Paleidimas:  SP=<scratchpad> node docs/sonines_sarasu_playwright.js
 */
const { chromium, paruosti } = require(require('path').join(__dirname, 'patikra', 'nuotrauka.js'));
const A = process.env.ADRESAS || 'http://127.0.0.1:8899';
let blogai = 0;

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox'] });
  const p = await paruosti(b, 1600, 1100);
  await p.goto(A + '/?section=cars&sidebar=1', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(2500);

  const mygtukai = await p.$$('.sp-side-card .sp-dd-btn');
  console.log('Sąrašų (mūsų) rasta: ' + mygtukai.length + '\n');
  console.log('laukas                          | plotis OK | neišlipa | tekstas matomas');
  console.log('-'.repeat(78));

  for (let i = 0; i < mygtukai.length; i++) {
    // Antra ir trečia markės/modelio pora paslėptos (x-show="poros > N"),
    // kol jų nepridedi — tai ne klaida, tad neskaičiuojam.
    const matomas = await p.evaluate((idx) => {
      const mg = document.querySelectorAll('.sp-side-card .sp-dd-btn')[idx];
      return mg.getBoundingClientRect().width > 0;
    }, i);
    if (!matomas) continue;
    // „Modelis" be pasirinktos markės yra sąmoningai neaktyvus
    // (opacity-60, toggle() neatidaro) — tai ne klaida.
    const neaktyvus = await p.evaluate((idx) => {
      const mg = document.querySelectorAll('.sp-side-card .sp-dd-btn')[idx];
      return mg.className.includes('opacity-60');
    }, i);
    if (neaktyvus) {
      const v = await p.evaluate((idx) => {
        const mg = document.querySelectorAll('.sp-side-card .sp-dd-btn')[idx];
        const et = mg.closest('div').querySelector('label');
        return et ? et.textContent.trim() : '?';
      }, i);
      console.log(`${v.slice(0,31).padEnd(31)} | (neaktyvus, kol nepasirinkta markė)`);
      continue;
    }
    // Spaudžiam PROGRAMIŠKAI: tikras paspaudimas nepraeina — lipni
    // antraštė ir jau atidarytas langas perima pelę. Alpine DOM atnaujina
    // kitame cikle, tad matuojam ATSKIRAI, po pauzės.
    await p.evaluate(() => document.body.dispatchEvent(
      new KeyboardEvent('keydown', { key: 'Escape', bubbles: true })));
    await p.evaluate((idx) => {
      for (const d of document.querySelectorAll('.sp-side-card [data-ms]')) {
        if (d.__x && d.__x.$data) d.__x.$data.open = false;
      }
      document.querySelectorAll('.sp-side-card .sp-dd-btn')[idx].click();
    }, i);
    await p.waitForTimeout(300);

    const r = await p.evaluate((idx) => {
      const s = document.querySelector('.sp-side-card');
      const mg = s.querySelectorAll('.sp-dd-btn')[idx];
      const blk = mg.closest('div');
      const et = blk.querySelector('label');
      const pan = blk.querySelector('.sp-dd');
      if (!pan || pan.getBoundingClientRect().width === 0)
        return { vardas: et ? et.textContent.trim() : '?', nera: true };
      const f = mg.getBoundingClientRect();
      const d = pan.getBoundingClientRect();
      const j = s.getBoundingClientRect();
      let kirpta = [];
      for (const e of pan.querySelectorAll('.sp-dd-item, .sp-dd-item span, .sp-dd-group')) {
        if (e.scrollWidth > e.clientWidth + 1)
          kirpta.push((e.textContent || '').trim().slice(0, 24));
      }
      return {
        vardas: et ? et.textContent.trim() : '?',
        dKaire: Math.abs(d.left - f.left), dDesine: Math.abs(d.right - f.right),
        islipa: Math.max(0, Math.round(j.left - d.left)) + Math.max(0, Math.round(d.right - j.right)),
        z: getComputedStyle(pan).zIndex,
        aukstis: Math.round(d.height),
        kirpta,
      };
    }, i);
    if (r.nera) { console.log(`${r.vardas.padEnd(31)} | (neatsidarė)`); blogai++; continue; }
    const pl = r.dKaire <= 1 && r.dDesine <= 1;
    const ne = r.islipa === 0;
    const tk = r.kirpta.length === 0;
    if (!pl || !ne || !tk) blogai++;
    console.log(
      `${r.vardas.slice(0,31).padEnd(31)} | ${(pl?'✔':'✘ '+Math.round(r.dKaire)+'/'+Math.round(r.dDesine)+'px').padEnd(9)} | ` +
      `${(ne?'✔':'✘ '+r.islipa+'px').padEnd(8)} | ${tk?'✔':'✘ '+r.kirpta.join(', ')}`);
  }

  // Native <select> — jų turi nebūti visai
  const native = await p.$$eval('.sp-side-card [data-laukai] select',
    e => e.map(x => x.name));
  console.log('\nNative <select> juostoje: ' + (native.length ? native.join(', ') : 'nėra'));

  await b.close();
  console.log('\n' + '═'.repeat(60));
  console.log(blogai ? 'NEATITIKIMŲ: ' + blogai : 'VISI SĄRAŠAI TVARKOJE');
  process.exit(blogai ? 1 : 0);
})();
