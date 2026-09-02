/* ŽINUTĖS — etalonas docs/demo/zinutes-notification-demo.html (2 ir 3).
 *
 * Tikrina tai, ko prašyta A ir B dalyse:
 *   A1 el. pašto pokalbiuose nėra nė vieno; rodomi vardai
 *   A2 neperskaitytos matomos (fonas, paryškinimas, taškas, skaičius),
 *      vokas su žyme matomas IR telefone
 *   A3 skelbimo juostelė su nuotrauka 44 px, pavadinimu ir kaina
 *   A4 nuotraukos rodomos abiejuose ekranuose, atsidaro didinimo langas
 *   A5 žinutės prilipusios prie apačios, atidarius — nuslinkta žemyn
 *   A6 datų skirtukai
 *   A7 greiti atsakymai (tik su skelbimu)
 *   A8 telefone sąrašas ir pokalbis — atskiri ekranai su „atgal"
 *   B9 jokio location.reload(): nauja žinutė atsiranda pati, įrašytas
 *      tekstas nedingsta, slinkimas nenušoka
 *
 * Paleidimas:  SP=<scratchpad> node docs/zinutes_playwright.js
 */
const { chromium } = require(process.env.SP + '/nuotrauka.js');
const { puslapis, prisijunk, A } = require(process.env.SP + '/pk2.js');
const EKRANAI = __dirname + '/ekranai';

let gerai = 0, blogai = 0;
const tik = (s, k) => { s ? gerai++ : (blogai++, console.log('  NEPAVYKO: ' + k)); };
const antraste = t => console.log('\n── ' + t + ' ' + '─'.repeat(Math.max(0, 48 - t.length)));

// El. paštą tikrinam TIK pokalbių srityje: poraštėje yra svetainės
// pagalbos adresas ir jis ten lieka sąmoningai.
const PASTAS = /[\w.-]+@[\w.-]+\.\w{2,}/;

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const p = await puslapis(b, 360, 800);
  const klaidos = [];
  p.on('pageerror', e => klaidos.push(String(e).slice(0, 200)));
  await prisijunk(p);

  // Neperskaitytos būsenos testas turi ją ir sukurti — ankstesni
  // paleidimai viską pažymi perskaityta.
  function pasnekovasRaso(tekstas) {
    require('child_process').execSync(
      'SECRET_KEY=x EMAIL_USER=x@x.lt EMAIL_PASSWORD=x '
      + 'PYTHONPATH=' + process.env.SP + ' python3 -c "'
      + "import os,django;os.environ['DJANGO_SETTINGS_MODULE']='sqlite_settings';django.setup();"
      + "from apps.conversations.models import Conversation,Message;"
      + "c=Conversation.objects.filter(listing__isnull=False).first();"
      + "s=c.participants.exclude(email='romasm333@gmail.com').first();"
      + "Message.objects.create(conversation=c,sender=s,content='" + tekstas + "')\"");
  }
  pasnekovasRaso('Nauja neskaityta');

  antraste('Sąrašas (360 px)');
  await p.goto(A + '/conversations/', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(1500);
  const s = await p.evaluate(() => {
    const sr = document.querySelector('.pk-shell');
    return {
      eiluciu: document.querySelectorAll('.pk-eil').length,
      vardai: [...document.querySelectorAll('.pk-vardas')].map(e => e.textContent.trim()),
      tekstas: sr ? sr.innerText : '',
      nauju: document.querySelectorAll('.pk-eil.yra-nauju').length,
      taskai: document.querySelectorAll('.pk-taskas').length,
      kiekiai: [...document.querySelectorAll('.pk-kiek')].map(e => e.textContent.trim()),
      vokoPlotis: (() => { const a = document.querySelector('.fa-envelope');
        return a ? Math.round(a.getBoundingClientRect().width) : 0; })(),
      zyme: !!document.querySelector('[data-zinuciu-zyme]'),
    };
  });
  console.log('  vardai: ' + JSON.stringify(s.vardai));
  tik(s.eiluciu > 0, 'sąraše nėra pokalbių — testui reikia duomenų');
  tik(!PASTAS.test(s.tekstas), 'sąraše matyti el. paštas');
  tik(s.vardai.every(v => v && !v.includes('@')), 'vardas atrodo kaip el. paštas');
  tik(s.nauju > 0 && s.taskai > 0, 'neperskaityti nepažymėti (fonas/taškas)');
  tik(s.kiekiai.length > 0, 'nerodomas neperskaitytų skaičius');
  tik(s.vokoPlotis > 0, 'vokas antraštėje telefone nematomas');
  tik(s.zyme, 'voko žymė be data-zinuciu-zyme (JS jos neatnaujins)');

  antraste('Antraštė prisijungus — vokas neišplečia puslapio');
  for (var w of [320, 360, 390, 414]) {
    await p.setViewportSize({ width: w, height: 780 });
    await p.waitForTimeout(400);
    var h = await p.evaluate(() => {
      var j = document.querySelector('.hdr-veiksmai');
      var el = [...j.children].filter(e => e.getBoundingClientRect().width > 0);
      return { eiluciu: new Set(el.map(e => Math.round(e.getBoundingClientRect().top / 8))).size,
               vokas: !!document.querySelector('.fa-envelope'),
               puslapis: document.documentElement.scrollWidth, langas: window.innerWidth };
    });
    console.log('  ' + w + ' px: ' + JSON.stringify(h));
    tik(h.vokas, w + ' px — voko nesimato prisijungus');
    tik(h.eiluciu === 1, w + ' px — antraštė ne vienoje eilutėje');
    tik(h.puslapis <= h.langas + 1, w + ' px — puslapis platesnis už ekraną');
  }
  await p.setViewportSize({ width: 360, height: 800 });
  await p.waitForTimeout(400);

  antraste('Pokalbis su skelbimu (360 px)');
  const suSkelbimu = await p.evaluate(() => {
    const e = [...document.querySelectorAll('.pk-eil')]
      .find(x => x.querySelector('.pk-skelb') && /·/.test(x.querySelector('.pk-skelb').textContent));
    if (e) { e.click(); return true; } return false;
  });
  await p.waitForTimeout(2000);
  const c = await p.evaluate(() => {
    const sr = document.getElementById('pkSrautas');
    const j = document.querySelector('.pk-juostele');
    // Nuotrauka arba jos vietą užimantis ženklas — abu 44 px
    const img = j ? (j.querySelector('img') || j.querySelector('.pk-jz')) : null;
    return {
      juostele: !!j,
      juostelesFoto: img ? Math.round(img.getBoundingClientRect().height) : null,
      pavadinimas: (document.querySelector('.pk-juostele-n') || {}).textContent,
      kaina: (document.querySelector('.pk-juostele-k') || {}).textContent,
      juostelesNuoroda: j ? j.tagName : null,
      burbulu: document.querySelectorAll('.pk-burb').length,
      dienos: [...document.querySelectorAll('.pk-diena')].map(e => e.textContent.trim()),
      greiti: [...document.querySelectorAll('.pk-greiti button')].map(e => e.textContent.trim()),
      apacioje: sr ? (sr.scrollHeight - sr.scrollTop - sr.clientHeight) : null,
      sarasasPaslept: [...document.querySelectorAll('.pk-eil')].every(e => e.getClientRects().length === 0),
      atgal: !!document.querySelector('a[aria-label]'),
      tekstas: document.querySelector('.pk-shell') ? document.querySelector('.pk-shell').innerText : '',
    };
  });
  console.log('  juostelė: ' + c.pavadinimas + ' · ' + c.kaina + ' | greiti: ' + c.greiti.length);
  tik(suSkelbimu, 'nerastas pokalbis su skelbimu');
  tik(c.juostele && c.juostelesNuoroda === 'A', 'skelbimo juostelė ne nuoroda į skelbimą');
  tik(c.juostelesFoto === 44, 'juostelės nuotrauka ne 44 px (' + c.juostelesFoto + ')');
  tik(!!c.kaina && c.kaina.trim().length > 0, 'juostelėje nėra kainos');
  tik(c.dienos.length > 0, 'nėra datų skirtukų');
  tik(c.greiti.length === 4, 'greitų atsakymų ne 4 (' + c.greiti.length + ')');
  tik(c.apacioje !== null && c.apacioje < 40, 'srautas neprislinktas prie apačios (' + c.apacioje + ')');
  tik(c.sarasasPaslept, 'telefone sąrašas ir pokalbis rodomi kartu');
  tik(c.atgal, 'nėra „atgal" mygtuko');
  tik(!PASTAS.test(c.tekstas), 'pokalbyje matyti el. paštas');

  antraste('Greitas atsakymas ir tekstas nedingsta');
  await p.evaluate(() => document.querySelector('.pk-greiti button').click());
  await p.waitForTimeout(300);
  const irasyta = await p.evaluate(() => document.getElementById('messageContent').value);
  tik(irasyta.length > 0, 'greitas atsakymas neįrašo teksto į lauką');

  antraste('B9 — nauja žinutė be perkrovimo');
  const pries = await p.evaluate(() => ({
    burbulu: document.querySelectorAll('.pk-burb').length,
    tekstas: document.getElementById('messageContent').value,
    conv: document.getElementById('pkSrautas').dataset.conv,
  }));
  // Pašnekovas parašo žinutę tiesiai į DB (per antrą sesiją to nedarom)
  pasnekovasRaso('Testine nauja zinute');
  await p.waitForTimeout(12000);   // pollinimas — 10 s
  const po = await p.evaluate(() => ({
    burbulu: document.querySelectorAll('.pk-burb').length,
    tekstas: document.getElementById('messageContent').value,
    paskutine: (() => { const b = document.querySelectorAll('.pk-burb');
      return b.length ? b[b.length - 1].innerText : ''; })(),
  }));
  console.log('  burbulų ' + pries.burbulu + ' → ' + po.burbulu);
  tik(po.burbulu === pries.burbulu + 1, 'nauja žinutė neatsirado (be perkrovimo)');
  tik(/Testine nauja zinute/.test(po.paskutine), 'nauja žinutė ne apačioje');
  tik(po.tekstas === pries.tekstas, 'įrašytas tekstas dingo — vadinasi, buvo perkrovimas');
  tik(klaidos.length === 0, 'JS klaidos: ' + JSON.stringify(klaidos));

  antraste('Vertimas — jungiklis su išsaugoma būsena');
  const vBusena = () => p.evaluate(() => ({
    btn: (document.getElementById('pkVerstiTxt') || {}).textContent.trim(),
    bukle: (document.getElementById('pkVerstiBukle') || {}).textContent.trim(),
    ijungta: (document.getElementById('pkVerstiBtn') || {}).dataset.ijungta,
    savoSuKlaida: [...document.querySelectorAll('.pk-burb.as')]
      .filter(b => b.querySelector('.pk-vertimo-klaida:not([hidden])')).length,
  }));
  const v0 = await vBusena();
  tik(v0.btn === 'IŠVERSTI POKALBĮ' && v0.bukle === 'Rodomi originalūs pranešimai',
      'išjungto jungiklio užrašai: ' + JSON.stringify(v0));

  await p.evaluate(() => document.getElementById('pkVerstiBtn').click());
  await p.waitForTimeout(3000);
  const v1 = await vBusena();
  console.log('  įjungus: ' + JSON.stringify(v1));

  if (v1.bukle === 'Vertimas neįjungtas') {
    // Serveryje/konteineryje nėra nei JSON rakto, nei API rakto —
    // tikrinam BŪTENT tą kelią: aiškus užrašas, o ne tylus originalas.
    console.log('  (rakto nėra — tikrinam „Vertimas neįjungtas" kelią)');
    tik(v1.ijungta === '0', 'be rakto jungiklis vis tiek įsijungė');
    tik(v1.btn === 'IŠVERSTI POKALBĮ', 'mygtukas neatsistatė: ' + v1.btn);
    tik(await p.evaluate(() =>
          document.getElementById('pkVerstiBukle').classList.contains('klaida')),
        '„Vertimas neįjungtas" nepažymėtas kaip klaida');
    tik(await p.evaluate(() => !document.getElementById('pkVerstiBtn').disabled),
        'mygtukas liko neaktyvus');
  } else {
    tik(v1.btn === 'RODYTI ORIGINALIAS ŽINUTES'
        && v1.bukle === 'Pranešimai verčiami automatiškai',
        'įjungto jungiklio užrašai: ' + JSON.stringify(v1));
    tik(v1.ijungta === '1', 'jungiklis neįsijungė');
    tik(v1.savoSuKlaida === 0, 'savo žinutės verčiamos — turi likti originalios');

    await p.reload({ waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(2000);
    const v2 = await vBusena();
    tik(v2.ijungta === '1' && v2.btn === 'RODYTI ORIGINALIAS ŽINUTES',
        'būsena neišliko po perkrovimo: ' + JSON.stringify(v2));

    await p.evaluate(() => document.getElementById('pkVerstiBtn').click());
    await p.waitForTimeout(2500);
    const v3 = await vBusena();
    tik(v3.ijungta === '0' && v3.btn === 'IŠVERSTI POKALBĮ', 'jungiklis neišsijungė');
    tik(await p.evaluate(() =>
          document.querySelectorAll('.pk-vertimo-klaida:not([hidden])').length === 0),
        'išjungus liko vertimo klaidų prierašų');
  }

  antraste('Nuotraukos ir didinimo langas');
  const foto = await p.evaluate(() => {
    const i = document.querySelector('.pk-burb img.lightbox-trigger');
    if (!i) return null;
    i.click();
    return true;
  });
  if (foto) {
    await p.waitForTimeout(500);
    tik(await p.evaluate(() => { const l = document.getElementById('pkLangas'); return l && !l.hidden; }),
        'didinimo langas neatsidaro');
    await p.keyboard.press('Escape');
    await p.waitForTimeout(300);
    tik(await p.evaluate(() => { const l = document.getElementById('pkLangas'); return l.hidden; }),
        'Escape neuždaro didinimo lango');
    // Miniatiūra, ne visas burbulas
    var mm = await p.evaluate(() => {
      const i = document.querySelector('.pk-burb img.lightbox-trigger');
      const r = i.getBoundingClientRect(), bur = i.closest('.pk-burb').getBoundingClientRect();
      const cs = getComputedStyle(i);
      return { w: Math.round(r.width), h: Math.round(r.height),
               dalis: r.width / bur.width, radius: cs.borderRadius, cursor: cs.cursor };
    });
    console.log('  miniatiūra: ' + JSON.stringify(mm));
    tik(mm.w <= 220 && mm.h <= 220, 'miniatiūra didesnė nei 220 px');
    tik(mm.dalis <= 0.71, 'telefone miniatiūra platesnė nei 70 % burbulo');
    tik(mm.radius === '10px', 'miniatiūros apvalinimas ne 10 px');
    tik(mm.cursor === 'pointer', 'miniatiūra be cursor:pointer');
  } else {
    console.log('  (šitame pokalbyje nuotraukų nėra — praleista)');
  }

  await p.screenshot({ path: EKRANAI + '/zinutes-360.png' });
  await p.close();

  antraste('Darbalaukis (1600 px)');
  const d = await puslapis(b, 1600, 1000);
  await prisijunk(d);
  await d.goto(A + '/conversations/', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await d.waitForTimeout(1500);
  await d.evaluate(() => {
    const e = [...document.querySelectorAll('.pk-eil')]
      .find(x => x.querySelector('.pk-skelb') && /·/.test(x.querySelector('.pk-skelb').textContent));
    if (e) e.click();
  });
  await d.waitForTimeout(2000);
  const dd = await d.evaluate(() => ({
    sarasasMatyti: [...document.querySelectorAll('.pk-eil')].some(e => e.getClientRects().length > 0),
    juostele: !!document.querySelector('.pk-juostele'),
    tekstas: document.querySelector('.pk-shell').innerText,
  }));
  tik(dd.sarasasMatyti, 'darbalaukyje sąrašas turi likti matomas');
  tik(dd.juostele, 'darbalaukyje nėra skelbimo juostelės');
  var dm = await d.evaluate(() => {
    const i = document.querySelector('.pk-burb img.lightbox-trigger');
    if (!i) return null;
    const r = i.getBoundingClientRect();
    return { w: Math.round(r.width), h: Math.round(r.height) };
  });
  if (dm) {
    console.log('  miniatiūra darbalaukyje: ' + JSON.stringify(dm));
    tik(dm.w <= 220 && dm.h <= 220, 'darbalaukyje miniatiūra didesnė nei 220 px');
  }
  tik(!PASTAS.test(dd.tekstas), 'darbalaukyje matyti el. paštas');
  await d.screenshot({ path: EKRANAI + '/zinutes-1600.png' });

  console.log('\nGerai: ' + gerai + ', blogai: ' + blogai);
  await b.close();
  process.exit(blogai ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
