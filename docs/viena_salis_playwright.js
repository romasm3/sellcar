/* VIENA ŠALIS VISAI SVETAINEI — tikra naršyklė, tikras serveris.
 *
 * Trys srautai, kurių prašyta:
 *   1. pakeisti šalį per juostą virš panelės  → patikrinti šoninę juostą
 *   2. pakeisti per šoninę juostą             → patikrinti juostą ir /imones/
 *   3. atidaryti vokišką skelbimą su pasirinkta Lietuva → vokiška vėliava
 *      kontaktų bloke ir tyli eilutė virš jo
 *
 * Nuotraukos: 1600px ir 390px į docs/ekranai/.
 *
 * Paleidimas (serveris turi suktis ties 127.0.0.1:8899):
 *   SP=<scratchpad> node docs/viena_salis_playwright.js
 */
const { chromium, paruosti } = require(process.env.SP + '/nuotrauka.js');
const EKRANAI = __dirname + '/ekranai';
const A = 'http://127.0.0.1:8899';
const VOKISKAS = '/11/';                 // „DE auto 3", Berlin

let gerai = 0, blogai = 0;
const tik = (s, k) => { s ? gerai++ : (blogai++, console.log('  NEPAVYKO: ' + k)); };
const antraste = (t) => console.log('\n── ' + t + ' ' + '─'.repeat(Math.max(0, 52 - t.length)));

// Kuri šalis rodoma — juostoje arba šoninėje juostoje.
const rodoma = (p) => p.evaluate(() => {
  const j = document.querySelector('.salies-vardas');
  const s = document.querySelector('.salis-cur-vardas');
  return (j && j.textContent.trim()) || (s && s.textContent.trim()) || null;
});

const eik = async (p, kelias) => {
  await p.goto(A + kelias, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(1200);
};

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox'] });

  for (const [vardas, w, h] of [['1600', 1600, 1000], ['390', 390, 844]]) {
    console.log('\n══════ ' + vardas + 'px ══════');
    const p = await paruosti(b, w, h);
    const telefonas = w < 1024;

    // ── 1. Pakeičiam per JUOSTĄ virš panelės ─────────────────────
    antraste('1. Juosta virš panelės');
    await eik(p, '/');
    tik(await p.$('.salies-juosta'), 'juosta yra');
    tik(await rodoma(p) === 'Lithuania', 'pradžioje Lithuania (' + await rodoma(p) + ')');
    await p.screenshot({ path: `${EKRANAI}/viena-salis-${vardas}-pradzia-lt.png`,
                         fullPage: false });

    await p.click('.salies-keisti');
    await p.waitForTimeout(400);
    await p.screenshot({ path: `${EKRANAI}/viena-salis-${vardas}-sarasas.png`,
                         fullPage: false });
    // Vėliava PO pavadinimo — tikrinam tikras koordinates naršyklėje
    const tvarka = await p.evaluate(() => {
      const eil = document.querySelector('.salies-punktas');
      if (!eil) return null;
      const v = eil.querySelector('.salies-punkto-vardas').getBoundingClientRect();
      const f = eil.querySelector('img.veliava');
      const k = eil.querySelector('.salies-punkto-kiekis').getBoundingClientRect();
      return f ? { vardas: v.right, veliava: f.getBoundingClientRect().left,
                   kiekis: k.left } : { begVeliavos: true };
    });
    if (tvarka && !tvarka.begVeliavos) {
      tik(tvarka.veliava >= tvarka.vardas - 1, 'vėliava PO pavadinimo');
      tik(tvarka.veliava < tvarka.kiekis, 'vėliava prieš skaičių');
    }
    await p.click('a[href*="salis=de"]');
    await p.waitForTimeout(1500);
    tik(await rodoma(p) === 'Germany', 'juosta rodo Germany (' + await rodoma(p) + ')');

    // ── ir ta pati šalis kitur ───────────────────────────────────
    if (!telefonas) {
      await eik(p, '/?section=cars&sidebar=1');
      tik(await rodoma(p) === 'Germany',
          'ŠONINĖ JUOSTA rodo Germany (' + await rodoma(p) + ')');
      await p.screenshot({ path: `${EKRANAI}/viena-salis-${vardas}-sonine-de.png`,
                           fullPage: false });
      // Kortelės vieta — ta pati vėliava, ir ji eina PO pavadinimo
      const kortele = await p.evaluate(() => {
        // Vietos eilutė dabar ateina iš bendros dalies (_kort_vieta.html)
        const loc = document.querySelector('.kv-zalia');
        if (!loc) return null;
        const f = loc.querySelector('img.veliava');
        if (!f) return { beVeliavos: true, tekstas: loc.textContent.trim() };
        const fr = f.getBoundingClientRect();
        return { src: f.getAttribute('src'), tekstas: loc.textContent.trim(),
                 veliava: fr.left, kaire: loc.getBoundingClientRect().left };
      });
      tik(kortele && !kortele.beVeliavos, 'kortelėje yra vėliava');
      if (kortele && !kortele.beVeliavos) {
        tik(/flags\/de\.svg/.test(kortele.src), 'kortelės vėliava vokiška');
        tik(kortele.veliava > kortele.kaire, 'kortelėje vėliava PO vietos teksto');
        tik(/Germany/.test(kortele.tekstas),
            'kortelėje pilnas angliškas šalies vardas: ' + kortele.tekstas);
      }
    }
    await eik(p, '/imones/');
    tik(await rodoma(p) === 'Germany', '/imones/ rodo Germany (' + await rodoma(p) + ')');
    await p.screenshot({ path: `${EKRANAI}/viena-salis-${vardas}-imones-de.png`,
                         fullPage: false });

    // ── 2. Pakeičiam per ŠONINĘ JUOSTĄ ───────────────────────────
    if (!telefonas) {
      antraste('2. Šoninė juosta');
      await eik(p, '/?section=cars&sidebar=1');
      await p.click('.salis-keisti-mazas');
      await p.waitForTimeout(400);
      await p.screenshot({ path: `${EKRANAI}/viena-salis-${vardas}-sonine-sarasas.png`,
                           fullPage: false });
      const t2 = await p.evaluate(() => {
        const eil = document.querySelector('.salis-eil');
        const v = eil.querySelector('.salis-eil-vardas').getBoundingClientRect();
        const f = eil.querySelector('img.veliava');
        const k = eil.querySelector('.salis-eil-kiekis').getBoundingClientRect();
        return f ? { vardas: v.right, veliava: f.getBoundingClientRect().left, kiekis: k.left } : null;
      });
      if (t2) {
        tik(t2.veliava >= t2.vardas - 1, 'šoninėje: vėliava PO pavadinimo');
        tik(t2.veliava < t2.kiekis, 'šoninėje: vėliava prieš skaičių');
      }
      await p.click('.salis-list a[href*="salis=pl"]');
      await p.waitForTimeout(1500);
      tik(await rodoma(p) === 'Poland', 'šoninė juosta rodo Poland');

      await eik(p, '/');
      tik(await rodoma(p) === 'Poland', 'JUOSTA rodo Poland (' + await rodoma(p) + ')');
      await eik(p, '/imones/');
      tik(await rodoma(p) === 'Poland', '/imones/ rodo Poland (' + await rodoma(p) + ')');
    }

    // ── 3. Vokiškas skelbimas, kai pasirinkta Lietuva ────────────
    antraste('3. Vokiškas skelbimas su pasirinkta Lietuva');
    await eik(p, '/?salis=lt');
    tik(await rodoma(p) === 'Lithuania', 'svetainėje vėl Lietuva');
    await eik(p, VOKISKAS);
    const blokas = await p.$('.pard-blokas, .pard-vieta');
    tik(!!blokas, 'kontaktų blokas yra');
    const kita = await p.$('.pard-kita-salis');
    tik(!!kita, 'tyli eilutė „Šis skelbimas yra Vokietijoje" yra');
    if (kita) {
      const tekstas = (await kita.innerText()).replace(/\s+/g, ' ').trim();
      tik(/Vokietijoje/.test(tekstas), 'eilutėje vietininkas: ' + tekstas);
      tik(/Rodyti visus/.test(tekstas), 'yra nuoroda į visus tos šalies skelbimus');
    }
    const veliava = await p.$('.pard-vieta img.veliava');
    tik(!!veliava, 'kontaktų bloke yra vėliava');
    if (veliava) {
      const src = await veliava.getAttribute('src');
      tik(/flags\/de\.svg/.test(src), 'vėliava VOKIŠKA, ne pagal pasirinktą šalį (' + src + ')');
      const t3 = await p.evaluate(() => {
        const v = document.querySelector('.pard-vieta');
        const f = v.querySelector('img.veliava').getBoundingClientRect();
        // Tekstas eina prieš vėliavą: paskutinis teksto taškas kairiau
        const r = document.createRange();
        r.selectNodeContents(v);
        return { veliava: f.left, blokas: v.getBoundingClientRect().left };
      });
      tik(t3.veliava > t3.blokas, 'vėliava dešinėje nuo teksto (po pavadinimo)');
    }
    // Blokas gali būti žemiau lango — pirma prisukam, tada kerpam.
    await p.$eval('.pard-vieta', el => el.scrollIntoView({ block: 'center' }));
    await p.waitForTimeout(400);
    const dv = await (await p.$('.pard-vieta')).boundingBox();
    const virs = Math.max(0, Math.min(dv.y - 240, h - 420));
    await p.screenshot({ path: `${EKRANAI}/viena-salis-${vardas}-kontaktai-de.png`,
                         clip: { x: 0, y: virs, width: w,
                                 height: Math.min(420, h - virs) } });
    await p.close();
  }

  await b.close();
  console.log('\n' + '═'.repeat(56));
  console.log('gerai: ' + gerai + ', nepavyko: ' + blogai);
  process.exit(blogai ? 1 : 0);
})();
