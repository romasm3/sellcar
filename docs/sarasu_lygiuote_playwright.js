/* SĄRAŠŲ TEKSTAS VISADA KAIRĖJE (docs/taisykles.md 10).
 *
 * Matuoja TIKRĄ atstumą nuo eilutės kairio krašto iki teksto pradžios
 * kiekviename sąraše: iškrentančiame (markės, modeliai, reikšmės),
 * šalių sąraše, telefono eilutėse ir /pasirinkti/ puslapyje.
 *
 * Riba — 38 px. Į ją telpa eilutės vidus (14 px) ir žymimasis langelis
 * ar radijo mygtukas su tarpu (16 + 10 px). Daugiau reiškia, kad tekstas
 * nustumtas.
 *
 * Paleidimas:  SP=<scratchpad> node docs/sarasu_lygiuote_playwright.js
 *              SP=<scratchpad> GYVAI=1 node docs/sarasu_lygiuote_playwright.js
 */
const GYVAI = !!process.env.GYVAI;
const { chromium, paruosti } = require(process.env.SP +
  (GYVAI ? '/nuotrauka_gyva.js' : '/nuotrauka.js'));
const A = GYVAI ? 'https://autoleft.com' : 'http://127.0.0.1:8899';
const RIBA = 38;

let gerai = 0, blogai = 0;
const tik = (s, k) => { s ? gerai++ : (blogai++, console.log('  NEPAVYKO: ' + k)); };

// Tekstas eilutėje — pirmas span, kuris nėra skaičius.
const MATUOK = (sel) => {
  const eil = [...document.querySelectorAll(sel)]
    .filter(e => e.getClientRects().length && e.textContent.trim());
  return eil.slice(0, 6).map(e => {
    const r = e.getBoundingClientRect();
    const t = [...e.querySelectorAll('span')]
      .find(s => !s.className.includes('count') && !s.className.includes('cnt')
                 && !s.className.includes('kiekis') && s.textContent.trim());
    const cs = getComputedStyle(e);
    return { tekstas: (t || e).textContent.trim().slice(0, 18),
             offsetLeft: Math.round(((t || e).getBoundingClientRect().left) - r.left),
             justify: cs.justifyContent, textAlign: cs.textAlign };
  });
};

async function tirk(p, kelias, atidaryk, sarasai) {
  await p.goto(A + kelias, { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(GYVAI ? 3000 : 2000);
  if (atidaryk) { await p.evaluate(atidaryk); await p.waitForTimeout(1500); }
  for (const [sel, vardas] of sarasai) {
    const eil = await p.evaluate(MATUOK, sel);
    if (!eil.length) { console.log('  (praleista, nėra: ' + vardas + ')'); continue; }
    const bloga = eil.filter(e => e.offsetLeft > RIBA);
    tik(bloga.length === 0, vardas + ' — tekstas nustumtas: ' + JSON.stringify(bloga));
    tik(eil.every(e => e.justify !== 'space-between'),
        vardas + ' — eilutėje liko justify-content:space-between');
    console.log('  ' + vardas.padEnd(34) + ' offsetLeft: '
                + eil.map(e => e.offsetLeft).join(', ') + '  (' + eil[0].justify + ')');
  }
}

// Atidarom viską, kas turi sąrašą: pirmą lauką ir šalių bloką.
const ATIDARYK_DD = () => {
  const dd = [...document.querySelectorAll('.sp-dd-btn')].filter(x => x.getClientRects().length)[0];
  if (dd) dd.click();
  ['.salis-keisti-mazas', '.salies-keisti'].forEach(sel => {
    const k = [...document.querySelectorAll(sel)].filter(x => x.getClientRects().length)[0];
    if (k) k.click();
  });
};

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });

  console.log('\n── Šoninė juosta (1600) ' + '─'.repeat(26));
  let p = await paruosti(b, 1600, 1100);
  await tirk(p, '/?section=cars&sidebar=1', ATIDARYK_DD,
    [['.sp-dd-item', 'iškrentantis sąrašas'], ['.salis-eil', 'šalių sąrašas']]);
  await p.close();

  console.log('\n── Išplėstinė paieška (1600) ' + '─'.repeat(21));
  p = await paruosti(b, 1600, 1100);
  await tirk(p, '/paieska/cars/', ATIDARYK_DD,
    [['.sp-dd-item', 'iškrentantis sąrašas'], ['.salis-eil', 'šalių sąrašas']]);
  await p.close();

  console.log('\n── Greitoji panelė, pradžia (1600) ' + '─'.repeat(15));
  p = await paruosti(b, 1600, 1100);
  await tirk(p, '/', ATIDARYK_DD,
    [['.sp-dd-item', 'iškrentantis sąrašas'], ['.salies-punktas', 'juostos šalių sąrašas']]);
  await p.close();

  console.log('\n── Telefonas (390) ' + '─'.repeat(31));
  p = await paruosti(b, 390, 844);
  await tirk(p, '/?section=cars&sidebar=1', null, [['.sp-mrow', 'telefono eilutės']]);
  await tirk(p, '/pasirinkti/?laukas=body_type&kategorija=cars&grizti=/', null,
    [['.sp-sheet-item', '/pasirinkti/ reikšmės']]);
  await p.close();

  console.log('\nGerai: ' + gerai + ', blogai: ' + blogai);
  await b.close();
  process.exit(blogai ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
