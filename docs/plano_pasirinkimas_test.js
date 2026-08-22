/* ═══════════════════════════════════════════════════════════════════
   Aktyvavimo plano puslapio (listing_select_plan.html) mobilaus vaizdo
   testai — tikras atrenderintas šablonas ir tikras jo inline JS.

   Paleidimas:
       python docs/plano_pasirinkimas_render.py   # atrenderina į /tmp
       node    docs/plano_pasirinkimas_test.js

   Svarbiausia, ką tikrina: mobilios kortelės naudoja TUOS PAČIUS radio
   mygtukus per <label for>, todėl formoje nėra dublikatų — kitaip
   mokėjimo forma pasiųstų du plan_code arba dvi renew_count reikšmes.
   ═══════════════════════════════════════════════════════════════════ */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { JSDOM } = require('jsdom');
const FIXTURE = process.env.PLAN_HTML ||
      path.join(os.tmpdir(), 'plan_rendered.html');
if (!fs.existsSync(FIXTURE)) {
  console.error('Nerastas ' + FIXTURE + ' — pirma paleisk:\n' +
                '  python docs/plano_pasirinkimas_render.py');
  process.exit(2);
}
const HTML = fs.readFileSync(FIXTURE, 'utf8');

let bad = 0;
const chk = (name, got, want) => {
  const ok = String(got) === String(want);
  if (!ok) bad++;
  console.log((ok ? '  ok   ' : '  FAIL ') + name + '  got=' + JSON.stringify(String(got)) +
              (ok ? '' : ' want=' + JSON.stringify(String(want))));
};

new Promise(res => {
  const dom = new JSDOM(HTML, { runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true });
  dom.window.addEventListener('load', () => setTimeout(() => res(dom), 0));
}).then(dom => {
  const doc = dom.window.document;
  const radios = doc.querySelectorAll('.plan-radio');
  const mcards = doc.querySelectorAll('[data-mplan]');
  const mincl = doc.querySelectorAll('[data-mincl]');

  console.log('\n── Struktūra ──');
  chk('radio mygtukų', radios.length, 3);
  chk('mobilių kortelių', mcards.length, 3);
  chk('„Į planą įeina" blokų', mincl.length, 3);
  chk('formoje vienas plan_code rinkinys', doc.querySelectorAll('[name="plan_code"]').length, 3);
  chk('renew_count nesudubliuotas', doc.querySelectorAll('[name="renew_count"]').length, 1);
  chk('featured_days nesudubliuotas', doc.querySelectorAll('[name="featured_days"]').length, 1);
  chk('submitBtn vienas', doc.querySelectorAll('#submitBtn').length, 1);
  chk('totalPrice vienas', doc.querySelectorAll('#totalPrice').length, 1);

  console.log('\n── Etiketės rodo į tikrus radio ──');
  [...mcards].forEach((el, i) => {
    const target = doc.getElementById(el.getAttribute('for'));
    chk('kortelė ' + i + ' -> radio', target ? target.dataset.idx : '(nėra)', String(i));
  });

  console.log('\n── Pradinė būsena: rekomenduojamas pažymėtas ──');
  chk('pažymėtas radio', doc.querySelector('.plan-radio:checked').dataset.idx, '0');
  chk('kortelė 0 pažymėta', mcards[0].className.includes('border-gray-800'), 'true');
  chk('kortelė 1 nepažymėta', mcards[1].className.includes('border-gray-800'), 'false');
  chk('varnelė matoma tik pirmoje',
      [...doc.querySelectorAll('.m-plan-check')].filter(c => !c.classList.contains('hidden')).length, 1);
  chk('rodomas 1 „įeina" blokas',
      [...mincl].filter(b => !b.classList.contains('hidden')).length, 1);
  chk('rodomas BŪTENT pirmo plano', [...mincl].find(b => !b.classList.contains('hidden')).dataset.mincl, '0');
  chk('jame yra 3★', [...mincl][0].textContent.includes('3 ★'), 'true');

  console.log('\n── Paspaudus antrą kortelę ──');
  mcards[1].click();                       // <label for=...> — natūralus elgesys
  chk('persijungė radio', doc.querySelector('.plan-radio:checked').dataset.idx, '1');
  chk('kortelė 1 pažymėta', mcards[1].className.includes('border-gray-800'), 'true');
  chk('kortelė 0 nebe', mcards[0].className.includes('border-gray-800'), 'false');
  chk('„įeina" blokas persijungė', [...mincl].find(b => !b.classList.contains('hidden')).dataset.mincl, '1');
  chk('suma perskaičiuota', doc.getElementById('totalPrice').textContent, '35.99');

  console.log('\n── Grįžus į pirmą ──');
  mcards[0].click();
  chk('suma', doc.getElementById('totalPrice').textContent, '39.99');
  chk('„įeina" blokas', [...mincl].find(b => !b.classList.contains('hidden')).dataset.mincl, '0');

  console.log('\n── Darbalaukio lentelė telefone paslėpta ──');
  const desk = doc.querySelector('.hidden.md\\:flex');
  chk('lentelė turi hidden md:flex', !!desk, 'true');
  chk('mobilus blokas turi md:hidden', mcards[0].closest('.md\\:hidden') !== null, 'true');

  console.log(bad ? `\n✗ ${bad} nesėkmė(s)` : '\n✓ visi testai praėjo');
  process.exit(bad ? 1 : 0);
});
