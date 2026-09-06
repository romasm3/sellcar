/* Vietinio serverio puslapis su prisijungimu — bendra dalis testams.
 *
 * Slaptažodžio faile NĖRA: imamas iš aplinkos (PATIKRA_SLAPTAZODIS).
 * Testinė paskyra aprašyta CLAUDE.md; adresą irgi galima perrašyti.
 */
const path = require('path');
const { chromium, paruosti, paleisk } = require(path.join(__dirname, 'nuotrauka.js'));

const A = process.env.ADRESAS || 'http://127.0.0.1:8899';
const PASKYRA = process.env.PATIKRA_PASKYRA || 'romasm333@gmail.com';
const SLAPTAZODIS = process.env.PATIKRA_SLAPTAZODIS || '';

module.exports.puslapis = async (b, w, h) => {
  const p = await paruosti(b, w, h);
  await p.setExtraHTTPHeaders({ 'Accept-Language': 'lt,en;q=0.5' });
  await p.context().addCookies([{ name: 'django_language', value: 'lt', url: A }]);
  return p;
};

module.exports.prisijunk = async (p) => {
  if (!SLAPTAZODIS) {
    throw new Error('Nėra PATIKRA_SLAPTAZODIS aplinkoje — prisijungimo testai '
                    + 'be jo nepasileis (slaptažodžio repo nelaikom).');
  }
  await p.goto(A + '/accounts/login/', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(1200);
  await p.evaluate(([paskyra, slaptazodis]) => {
    const f = [...document.querySelectorAll('form')]
      .find(f => f.querySelector('input[name=email]'));
    f.querySelector('input[name=email]').value = paskyra;
    const pw = f.querySelector('input[type=password]');
    if (pw) pw.value = slaptazodis;
    f.submit();
  }, [PASKYRA, SLAPTAZODIS]);
  await p.waitForTimeout(2500);
};

module.exports.A = A;
module.exports.chromium = chromium;
module.exports.paleisk = paleisk;
