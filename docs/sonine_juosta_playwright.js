/* ŠONINĖS JUOSTOS IŠVAIZDA — docs/demo/grozio-demo.html.
 *
 * Matuoja tikrus matmenis naršyklėje. Turinio NETIKRINA — tam yra
 * docs/sonines_juostos_sarasas.py (išrašas prieš/po turi sutapti).
 *
 * Paleidimas:  SP=<scratchpad> node docs/sonine_juosta_playwright.js
 */
const { chromium, paruosti } = require(process.env.SP + '/nuotrauka.js');
const EKRANAI = __dirname + '/ekranai';
const A = 'http://127.0.0.1:8899';

let gerai = 0, blogai = 0;
const tik = (s, k) => { s ? gerai++ : (blogai++, console.log('  NEPAVYKO: ' + k)); };
const antraste = (t) => console.log('\n── ' + t + ' ' + '─'.repeat(Math.max(0, 50 - t.length)));

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox'] });
  const p = await paruosti(b, 1600, 1100);
  await p.goto(A + '/?section=cars&sidebar=1', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(2500);

  const m = await p.evaluate(() => {
    const s = document.querySelector('.sp-side-card');
    if (!s) return null;
    const st = getComputedStyle(s);
    const blokai = [...s.querySelectorAll('[data-laukai="darbalaukis"] > div:not(.sb-apply)')]
      .filter(e => e.getBoundingClientRect().height > 0);
    const b1 = getComputedStyle(blokai[0]);
    const ant = s.querySelector('[data-laukai="darbalaukis"] label.block');
    const a = getComputedStyle(ant);
    const fld = [...s.querySelectorAll('select.sp-fld, input.sp-fld, button.sp-fld')]
      .find(e => e.getBoundingClientRect().height > 0);
    const eil = [...s.querySelectorAll('[data-laukai="darbalaukis"] label:not(.block)')]
      .find(e => e.getBoundingClientRect().height > 0);
    const go = s.querySelector('.sb-apply button[type=submit]');
    const cl = s.querySelector('.sb-clear');
    const keisti = s.querySelector('.salis-keisti-mazas');
    const salis = s.querySelector('.salis-blk');
    const gr = go.getBoundingClientRect();
    return {
      kortRadius: st.borderRadius, kortPad: st.padding,
      bloku: blokai.length, blokPad: b1.padding,
      linija: b1.borderBottomWidth, linijaSpalva: b1.borderBottomColor,
      antDydis: a.fontSize, antSvoris: a.fontWeight, antSpalva: a.color,
      antDidz: a.textTransform, antTarpas: a.letterSpacing,
      fldA: Math.round(fld.getBoundingClientRect().height),
      fldR: getComputedStyle(fld).borderRadius,
      eilA: eil ? Math.round(eil.getBoundingClientRect().height) : null,
      eilDidz: eil ? getComputedStyle(eil).textTransform : null,
      goA: Math.round(gr.height), goW: Math.round(gr.width),
      goFonas: getComputedStyle(go).backgroundColor,
      juosta: Math.round(s.getBoundingClientRect().width),
      clFonas: getComputedStyle(cl).backgroundColor,
      clSpalva: getComputedStyle(cl).color,
      keisti: keisti ? getComputedStyle(keisti).color : null,
      keistiDydis: keisti ? getComputedStyle(keisti).fontSize : null,
      salisFonas: salis ? getComputedStyle(salis).backgroundColor : null,
      // Paieškos panelė NETURI pasikeisti — jos laukai lieka kaip buvo
      panelesFld: (() => {
        const f = document.querySelector('.sp-shell .sp-fld');
        return f ? Math.round(f.getBoundingClientRect().height) : null;
      })(),
    };
  });
  if (!m) { console.log('NEPAVYKO: juostos nėra'); process.exit(1); }

  antraste('Blokai');
  tik(m.kortRadius === '12px', 'kortelė radius 12px (' + m.kortRadius + ')');
  tik(m.kortPad === '0px', 'kortelės vidų duoda blokai (' + m.kortPad + ')');
  tik(m.bloku > 10, 'blokų yra (' + m.bloku + ')');
  tik(m.blokPad === '16px', 'bloko vidus 16px (' + m.blokPad + ')');
  tik(m.linija === '1px' && m.linijaSpalva === 'rgb(229, 231, 235)',
      'linija 1px #E5E7EB (' + m.linija + ' ' + m.linijaSpalva + ')');

  antraste('Antraštės');
  tik(m.antDydis === '12px', '12px (' + m.antDydis + ')');
  tik(m.antSvoris === '700', '700 (' + m.antSvoris + ')');
  tik(m.antSpalva === 'rgb(107, 114, 128)', 'pilka #6B7280 (' + m.antSpalva + ')');
  tik(m.antDidz === 'uppercase', 'DIDŽIOSIOMIS (' + m.antDidz + ')');
  tik(m.antTarpas === '0.5px', 'tarpas 0.5px (' + m.antTarpas + ')');

  antraste('Laukai ir eilutės');
  tik(m.fldA === 44, 'laukas 44px (' + m.fldA + ')');
  tik(m.fldR === '8px', 'radius 8px (' + m.fldR + ')');
  tik(m.eilA === null || m.eilA >= 34, 'varnelės eilutė ≥34px (' + m.eilA + ')');
  tik(m.eilDidz !== 'uppercase', 'varnelės eilutė NE didžiosiomis (' + m.eilDidz + ')');

  antraste('Nuorodos ir mygtukai');
  tik(m.keisti === 'rgb(210, 65, 29)', '„Keisti" #D2411D (' + m.keisti + ')');
  tik(parseFloat(m.keistiDydis) >= 13 && parseFloat(m.keistiDydis) <= 14,
      '„Keisti" 13–14px (' + m.keistiDydis + ')');
  tik(m.goA === 48, '„Filtruoti" 48px (' + m.goA + ')');
  tik(m.goFonas === 'rgb(24, 27, 31)', '„Filtruoti" juodas (' + m.goFonas + ')');
  tik(m.goW >= m.juosta - 36, '„Filtruoti" per visą plotį (' + m.goW + ' iš ' + m.juosta + ')');
  tik(m.clFonas === 'rgba(0, 0, 0, 0)', '„Išvalyti" be fono (' + m.clFonas + ')');
  tik(m.clSpalva === 'rgb(107, 114, 128)', '„Išvalyti" pilkas (' + m.clSpalva + ')');
  tik(m.salisFonas === 'rgba(0, 0, 0, 0)',
      'šalies blokas be atskiro fono (' + m.salisFonas + ')');

  antraste('Paieškos panelė nepaliesta');
  tik(m.panelesFld === null || m.panelesFld !== 44,
      'panelės laukas liko savo aukščio (' + m.panelesFld + ')');

  const bb = await (await p.$('.sp-side-card')).boundingBox();
  await p.screenshot({ path: `${EKRANAI}/sonine-juosta-virsus.png`, fullPage: true,
    clip: { x: Math.max(0, bb.x - 12), y: Math.max(0, bb.y - 12),
            width: bb.width + 24, height: Math.min(bb.height + 24, 1500) } });
  const r = await p.evaluate(() => {
    const a = document.querySelector('.sp-side-card .sb-apply').getBoundingClientRect();
    return { x: a.x + scrollX, y: a.y + scrollY, w: a.width, h: a.height };
  });
  await p.screenshot({ path: `${EKRANAI}/sonine-juosta-apacia.png`, fullPage: true,
    clip: { x: Math.max(0, r.x - 30), y: Math.max(0, r.y - 340),
            width: r.w + 60, height: r.h + 380 } });

  await b.close();
  console.log('\n' + '═'.repeat(54));
  console.log('gerai: ' + gerai + ', nepavyko: ' + blogai);
  process.exit(blogai ? 1 : 0);
})();
