/* ═══════════════════════════════════════════════════════════════════
   ŠALIES JUOSTA virš paieškos panelės — Playwright patikra.

   Paleidimas (reikia vietinio serverio ties 127.0.0.1:8899):
       SP=<katalogas su node_modules> node docs/salies_juosta_playwright.js

   Tikrina matmenis (56 px eilutė, 610 px plotis, 16 px tarpas iki
   panelės, 420 px langas / apatinis lakštas telefone), angliškus
   pavadinimus, rikiavimą pagal kiekį, paiešką, Escape, ir kad
   pasirinkus šalį adresas tampa ?salis=de, o seni filtrai lieka.
   ═══════════════════════════════════════════════════════════════════ */
const { chromium, paruosti } = require(process.env.SP + '/nuotrauka.js');
const S = process.env.SP;
let gerai=0, blogai=0;
const tik=(s,k)=>{ s?gerai++:(blogai++,console.log('  NEPAVYKO: '+k)); };
(async () => {
  const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args:['--no-sandbox'] });
  for (const [vardas, w, h] of [['1600', 1600, 1000], ['390', 390, 844]]) {
    console.log('\n══ ' + vardas + 'px ══');
    const p = await paruosti(b, w, h);
    await p.goto('http://127.0.0.1:8899/?section=cars', {waitUntil:'domcontentloaded', timeout:60000});
    await p.waitForTimeout(2500);

    const juosta = await p.$('.salies-juosta');
    tik(juosta && await juosta.isVisible(), 'juosta matoma');
    const dj = await juosta.boundingBox();
    const eil = await (await p.$('.salies-eilute')).boundingBox();
    tik(Math.round(eil.height) === 56, `eilutė 56px (${Math.round(eil.height)})`);
    tik(Math.round(dj.width) <= 610, `plotis ≤610px (${Math.round(dj.width)})`);

    // Tas pats plotis ir ta pati kairė kaip panelės
    const panele = await (await p.$('.sp-shell')).boundingBox();
    tik(Math.abs(dj.width - panele.width) < 2,
        `plotis kaip panelės (juosta ${Math.round(dj.width)}, panelė ${Math.round(panele.width)})`);
    tik(Math.abs(dj.x - panele.x) < 2, 'sulygiuota su panele');
    const tarpas = panele.y - (dj.y + dj.height);
    tik(Math.abs(tarpas - 16) < 1.5, `tarpas iki panelės 16px (${Math.round(tarpas)})`);
    await p.screenshot({ path: `${S}/salis-${vardas}-uzdaryta.png`,
                         clip: { x:0, y:Math.max(0,dj.y-90), width:w, height:Math.min(h, 420) } });

    // Atidarom
    await p.click('.salies-keisti');
    await p.waitForTimeout(500);
    const langas = await p.$('.salies-langas');
    tik(langas && await langas.isVisible(), 'langas atsidaro');
    const dl = await langas.boundingBox();
    if (w >= 640) {
      tik(Math.round(dl.width) === 420, `darbalaukyje 420px (${Math.round(dl.width)})`);
      tik(Math.abs((dl.x + dl.width) - (dj.x + dj.width)) < 2, 'lygiuotas dešinėje');
    } else {
      tik(Math.round(dl.width) === w, `telefone per visą plotį (${Math.round(dl.width)} iš ${w})`);
      tik(Math.round(dl.y + dl.height) === h, 'prilipęs prie apačios (apatinis lakštas)');
    }
    const rodykle = await p.$eval('.salies-keisti svg', e => getComputedStyle(e).transform);
    tik(rodykle.includes('-1') || rodykle === 'matrix(-1, 0, 0, -1, 0, 0)',
        `rodyklė apsivertė (${rodykle})`);
    const punktai = await p.$$('.salies-punktas');
    tik(punktai.length === 4, `4 šalys su skelbimais (${punktai.length})`);
    const tekstai = await p.$$eval('.salies-punkto-vardas', e => e.map(x => x.textContent.trim()));
    tik(JSON.stringify(tekstai) === JSON.stringify(['Lithuania','Germany','Poland','Latvia']),
        'angliškai ir pagal kiekį: ' + JSON.stringify(tekstai));
    const svoris = await p.$eval('.salies-punktas.is-on .salies-punkto-vardas',
                                 e => getComputedStyle(e).fontWeight);
    tik(svoris === '700', `dabartinė 700 (${svoris})`);
    tik(await p.$('.salies-punktas.is-on .salies-varnele'), 'dabartinė su varnele');
    await p.screenshot({ path: `${S}/salis-${vardas}-atidaryta.png`,
                         clip: w >= 640 ? { x:0, y:Math.max(0,dj.y-90), width:w, height:Math.min(h, 640) } : undefined,
                         fullPage: false });

    // Paieška sąraše
    await p.fill('.salies-paieska input', 'ger');
    await p.waitForTimeout(350);
    const matomi = await p.$$eval('.salies-punktas',
      els => els.filter(e => getComputedStyle(e).display !== 'none')
                .map(e => e.querySelector('.salies-punkto-vardas').textContent.trim()));
    tik(JSON.stringify(matomi) === '["Germany"]', 'paieška filtruoja: ' + JSON.stringify(matomi));
    await p.fill('.salies-paieska input', '');

    // Escape uždaro
    await p.keyboard.press('Escape'); await p.waitForTimeout(400);
    tik(!(await (await p.$('.salies-langas')).isVisible()), 'Escape uždaro');

    // Pasirinkus šalį — perkraunama ir adresas ?salis=de
    await p.click('.salies-keisti'); await p.waitForTimeout(400);
    await Promise.all([p.waitForNavigation({waitUntil:'domcontentloaded', timeout:30000}),
                       p.click('.salies-punktas:not(.is-on)')]);
    await p.waitForTimeout(1500);
    const u = new URL(p.url());
    tik(u.searchParams.get('salis') === 'de', `adresas ?salis=de (${p.url()})`);
    tik(u.searchParams.get('section') === 'cars', 'senas filtras liko');
    const dabar = await p.$eval('.salies-vardas', e => e.textContent.trim());
    tik(dabar === 'Germany', `juosta rodo Germany (${dabar})`);
    const kiek = await p.$eval('.salies-kiekis', e => e.textContent.trim());
    tik(kiek.includes('4'), `skaičius atsinaujino (${kiek})`);
    await p.screenshot({ path: `${S}/salis-${vardas}-pasirinkta-de.png`,
                         clip: { x:0, y:Math.max(0,dj.y-90), width:w, height:Math.min(h, 420) } });
    await p.close();
  }
  await b.close();
  console.log('\n' + '═'.repeat(50));
  console.log(`gerai: ${gerai}, nepavyko: ${blogai}`);
  process.exit(blogai ? 1 : 0);
})();
