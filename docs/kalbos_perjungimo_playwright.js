/* KALBOS PERJUNGIKLIS VEIKIA IR TEN, KUR ADRESE YRA ?next=
 *
 * Django `set_language` adreso priešdėlio nepersukdavo (`translate_url`
 * pirma bando `resolve`, o `LocalePrefixPattern` atpažįsta tik AKTYVIOS
 * kalbos priešdėlį — perjungimo POST'as ateina be jo). Žmogus grįždavo į
 * /ru/…, ir kelio priešdėlis nugalėdavo ką tik įrašytą slapuką.
 *
 * Tikrinam tikru pelės paspaudimu: po perjungimo (1) adresas gauna
 * teisingą kalbos priešdėlį, (2) `next` parametras irgi, (3) puslapis
 * TIKRAI kitos kalbos (<html lang>) — kritęs vertimas čia nepraeis.
 *
 * Paleidimas:  SP=<scratchpad> node docs/kalbos_perjungimo_playwright.js
 */
const { chromium } = require(process.env.SP + '/nuotrauka.js');
const A = process.env.ADRESAS || 'http://127.0.0.1:8899';

let gerai = 0, blogai = 0;
const tikrink = (s, k) => { if (s) gerai++; else { blogai++; console.log('  NEPAVYKO: ' + k); } };

// [pradinis adresas, kalba, laukiamas kelio pavidalas, laukiamas next]
const ATVEJAI = [
  ['/ru/accounts/login/?next=/ru/%3Fcategory%3Dcars',  'en', '/en/accounts/login/', '/en/?category=cars'],
  ['/ru/accounts/login/?next=/ru/%3Fcategory%3Dcars',  'lt', '/accounts/login/',    '/?category=cars'],
  ['/accounts/login/?next=/%3Fcategory%3Dcars',        'ru', '/ru/accounts/login/', '/ru/?category=cars'],
  ['/ru/accounts/register/?next=/ru/imones/',          'lt', '/accounts/register/', '/imones/'],
  ['/accounts/register/?next=/imones/',                'ru', '/ru/accounts/register/', '/ru/imones/'],
  ['/ru/imones/',                                      'en', '/en/imones/',         null],
  ['/ru/',                                             'lt', '/',                   null],
  ['/imones/',                                         'ru', '/ru/imones/',         null],
];

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox'] });

  for (const [pradzia, kalba, laukiamasKelias, laukiamasNext] of ATVEJAI) {
    const ctx = await b.newContext({ viewport: { width: 1400, height: 1000 } });
    const p = await ctx.newPage();
    await p.goto(A + pradzia, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await p.waitForTimeout(1200);

    // Perjungiam kaip žmogus: paspaudžiam kalbos mygtuką jo formoje.
    const paspausta = await p.evaluate((k) => {
      const btn = [...document.querySelectorAll('form button[name=language]')]
        .find(x => x.value === k && x.form.action.includes('setlang'));
      if (!btn) return false;
      btn.click();
      return true;
    }, kalba);
    tikrink(paspausta, `${pradzia} → ${kalba}: kalbos mygtuko nėra`);
    if (!paspausta) { await ctx.close(); continue; }

    await p.waitForTimeout(2500);
    const url = new URL(p.url());
    const next = url.searchParams.get('next');
    const htmlLang = await p.evaluate(() =>
      document.documentElement.getAttribute('lang'));

    tikrink(url.pathname === laukiamasKelias,
      `${pradzia} → ${kalba}: kelias ${url.pathname}, laukta ${laukiamasKelias}`);
    if (laukiamasNext !== null) {
      tikrink(next === laukiamasNext,
        `${pradzia} → ${kalba}: next „${next}", laukta „${laukiamasNext}"`);
    }
    tikrink((htmlLang || '').split('-')[0] === kalba,
      `${pradzia} → ${kalba}: puslapis liko „${htmlLang}" — kalba nepasikeitė`);

    console.log(`  ${kalba}  ${pradzia}\n     → ${url.pathname}${url.search}  lang=${htmlLang}`);
    await ctx.close();
  }

  // Antraštės mygtukai keičiasi kartu
  console.log('\n── Antraštė abiem kalbom ─────────────────────────');
  const LAUKIAMA = {
    lt: ['Prisijungti', 'Registruotis', 'Įkelti'],
    ru: ['Регистрация', 'Разместить'],
  };
  for (const [kalba, tekstai] of Object.entries(LAUKIAMA)) {
    const ctx = await b.newContext({ viewport: { width: 1400, height: 1000 } });
    const p = await ctx.newPage();
    await p.goto(A + (kalba === 'lt' ? '/' : '/' + kalba + '/'),
                 { waitUntil: 'domcontentloaded', timeout: 60000 });
    await p.waitForTimeout(1500);
    const antraste = await p.evaluate(() => {
      const h = document.querySelector('header') || document.body;
      return h.innerText.replace(/\s+/g, ' ');
    });
    for (const t of tekstai) {
      tikrink(antraste.includes(t), `antraštė (${kalba}): nėra „${t}"`);
    }
    // Rusiškoje antraštėje lietuviškų mygtukų likti negali
    if (kalba === 'ru') {
      for (const t of ['Registruotis', 'Įkelti']) {
        tikrink(!antraste.includes(t),
          `antraštė (ru): likęs lietuviškas „${t}"`);
      }
    }
    console.log(`  ${kalba}: ${antraste.slice(0, 130)}`);
    await ctx.close();
  }

  await b.close();
  console.log('\n' + '='.repeat(60));
  console.log(`gerai: ${gerai}, nepavyko: ${blogai}`);
  process.exit(blogai ? 1 : 0);
})();
