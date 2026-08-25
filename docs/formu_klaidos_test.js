/* ═══════════════════════════════════════════════════════════════════
   static/js/form_validation.js testai.

   Paleidimas:  npm i jsdom && node docs/formu_klaidos_test.js

   Ką tikrina: kad pateikiant tuščią privalomą lauką forma NEIŠSIUNČIAMA,
   laukas pažymimas, po juo atsiranda žinutė, o užpildžius žymė dingsta.
   Ir kad grįžus iš serverio su klaidomis vaizdas toks pat.
   ═══════════════════════════════════════════════════════════════════ */
const fs = require('fs');
const path = require('path');
const { JSDOM } = require(process.env.JSDOM_PATH || 'jsdom');
const JS = fs.readFileSync(path.join(__dirname, '..', 'static', 'js', 'form_validation.js'), 'utf8');

let gerai = 0, blogai = 0;
function tikrink(salyga, ka) {
    if (salyga) { gerai++; }
    else { blogai++; console.log('  NEPAVYKO: ' + ka); }
}
function antraste(t) { console.log('\n── ' + t + ' ' + '─'.repeat(Math.max(0, 56 - t.length))); }

const FORMA = `
<form id="f" method="post" data-validate action="/create/">
  <div data-field-wrap>
    <label for="id_phone">Telefonas</label>
    <input type="text" id="id_phone" name="phone" required>
  </div>
  <div data-field-wrap>
    <label for="id_city">Miestas</label>
    <input type="text" id="id_city" name="city" required>
  </div>
  <div data-field-wrap>
    <label for="id_price">Kaina</label>
    <input type="number" id="id_price" name="price" min="1" value="500">
  </div>
  <div data-field-wrap>
    <label for="id_email">El. paštas</label>
    <input type="email" id="id_email" name="email" required value="ne-pastas">
  </div>
  <label><input type="checkbox" id="id_agree_terms" name="agree_terms" required> Sutinku</label>
  <button type="submit">Skelbti</button>
</form>`;

/* Skriptas laukia DOMContentLoaded, todėl vykdom jį TIK dokumentui
   užsikrovus — kitaip nieko neprijungtų ir testai „praeitų" tuščiai. */
function kurti(kunas, priesEval) {
    const dom = new JSDOM(`<!doctype html><html><body>${kunas}</body></html>`,
        { runScripts: 'outside-only', pretendToBeVisual: true });
    // jsdom neturi išdėstymo — offsetWidth visada 0, todėl „matomas" sakytų NE.
    Object.defineProperty(dom.window.HTMLElement.prototype, 'getClientRects', {
        value: function () { return this.hidden ? [] : [{ width: 10, height: 10 }]; },
        configurable: true,
    });
    return new Promise(function (baigta) {
        function paleisti() {
            if (priesEval) { priesEval(dom); }
            dom.window.eval(JS);
            baigta(dom);
        }
        if (dom.window.document.readyState === 'complete') { paleisti(); }
        else { dom.window.addEventListener('load', paleisti); }
    });
}

function puslapis(papildomai, priesEval) {
    return kurti(`${FORMA}${papildomai || ''}`, priesEval);
}

/* Lauko žinutė guli iškart po jo bloku. Bendra paieška per tėvą
   (formą) rastų PIRMO lauko žinutę — tada testas tikrintų ne tą. */
function zinuteSalia(el) {
    const vieta = el.closest('[data-field-wrap]') || el.closest('label') || el;
    const kitas = vieta.nextElementSibling;
    return (kitas && kitas.hasAttribute('data-klaidos-zinute')) ? kitas : null;
}

function pateikti(dom) {
    const f = dom.window.document.getElementById('f');
    const ivykis = new dom.window.Event('submit', { bubbles: true, cancelable: true });
    f.dispatchEvent(ivykis);
    return ivykis;
}

async function testai() {

antraste('1. Tuščias privalomas laukas stabdo pateikimą');
{
    const dom = await puslapis();
    const d = dom.window.document;
    const e = pateikti(dom);
    tikrink(e.defaultPrevented, 'submit atšauktas (preventDefault)');
    tikrink(d.querySelector('[data-field-wrap] input#id_phone')
             .closest('[data-field-wrap]').classList.contains('field-invalid'),
            'telefonas pažymėtas .field-invalid');
    tikrink(d.querySelector('label[for="id_phone"]').classList.contains('label-invalid'),
            'telefono etiketė .label-invalid');
    const zin = d.querySelectorAll('.field-error-msg');
    tikrink(zin.length >= 3, 'žinutės po laukais (rasta ' + zin.length + ')');
    tikrink([...zin].some(z => z.textContent === 'Privalomas laukas'),
            'tekstas „Privalomas laukas"');
    tikrink([...zin].some(z => z.textContent === 'Turite sutikti su taisyklėmis'),
            'taisyklių langeliui — „Turite sutikti su taisyklėmis"');
    tikrink(d.getElementById('id_price').closest('[data-field-wrap]')
             .classList.contains('field-invalid') === false,
            'neprivalomas užpildytas laukas nepažymėtas');
}

antraste('2. Nuslinkimas ir fokusas į PIRMĄ klaidą');
{
    const dom = await puslapis();
    const d = dom.window.document;
    let nuslinkta = null, parametrai = null;
    dom.window.HTMLElement.prototype.scrollIntoView = function (o) {
        if (!nuslinkta) { nuslinkta = this; parametrai = o; }
    };
    pateikti(dom);
    tikrink(nuslinkta === d.getElementById('id_phone').closest('[data-field-wrap]'),
            'nuslinkta prie pirmos klaidos (telefono)');
    tikrink(parametrai && parametrai.behavior === 'smooth' && parametrai.block === 'center',
            'scrollIntoView({behavior:smooth, block:center})');
}

antraste('3. Užpildžius žymė nusiima');
{
    const dom = await puslapis();
    const d = dom.window.document;
    pateikti(dom);
    const laukas = d.getElementById('id_phone');
    tikrink(laukas.closest('[data-field-wrap]').classList.contains('field-invalid'), 'prieš: pažymėta');

    laukas.value = '+37060000000';
    laukas.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
    tikrink(!laukas.closest('[data-field-wrap]').classList.contains('field-invalid'),
            'po įvedimo: .field-invalid nuimta');
    tikrink(!d.querySelector('label[for="id_phone"]').classList.contains('label-invalid'),
            'po įvedimo: etiketė švari');
    tikrink(zinuteSalia(laukas) === null, 'po įvedimo: žinutė pašalinta');

    const dezute = d.getElementById('id_agree_terms');
    dezute.checked = true;
    dezute.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
    tikrink(!dezute.classList.contains('field-invalid'), 'pažymėjus langelį žymė nuimta');
}

antraste('4. Užpildyta, bet netinkama reikšmė');
{
    const dom = await puslapis();
    const d = dom.window.document;
    pateikti(dom);
    const zin = zinuteSalia(d.getElementById('id_email'));
    tikrink(zin !== null, 'blogam el. paštui yra žinutė');
    tikrink(zin && zin.textContent === 'Netinkama reikšmė',
            'tekstas „Netinkama reikšmė", ne „Privalomas laukas": ' +
            (zin ? JSON.stringify(zin.textContent) : '—'));
}

antraste('5. Visi užpildyti — forma išsiunčiama');
{
    const dom = await puslapis();
    const d = dom.window.document;
    d.getElementById('id_phone').value = '+37060000000';
    d.getElementById('id_city').value = 'Vilnius';
    d.getElementById('id_email').value = 'a@b.lt';
    d.getElementById('id_agree_terms').checked = true;
    const e = pateikti(dom);
    tikrink(!e.defaultPrevented, 'submit NEatšauktas');
    tikrink(d.querySelectorAll('.field-invalid').length === 0, 'nė vieno pažymėto lauko');
}

antraste('6. Serverio klaidos puslapiui užsikrovus');
{
    const JSON_BLOKAS = `<script type="application/json" id="serverio-klaidos">
      {"laukai":["city","agree_terms"],
       "zinutes":{"city":"Miestas yra privalomas","agree_terms":"Turite sutikti su taisyklėmis"},
       "tekstai":{"privalomas":"Privalomas laukas","taisykles":"Turite sutikti su taisyklėmis"}}
    </script>`;
    let nuslinkta = null;
    const dom = await puslapis(JSON_BLOKAS, function (dm) {
        dm.window.HTMLElement.prototype.scrollIntoView =
            function () { if (!nuslinkta) { nuslinkta = this; } };
    });
    const d = dom.window.document;
    tikrink(d.getElementById('id_city').closest('[data-field-wrap]')
             .classList.contains('field-invalid'), 'serverio laukas pažymėtas');
    tikrink(!d.getElementById('id_phone').closest('[data-field-wrap]')
              .classList.contains('field-invalid'), 'nenurodytas laukas nepažymėtas');
    const zin = zinuteSalia(d.getElementById('id_city'));
    tikrink(zin && zin.textContent === 'Miestas yra privalomas',
            'serverio tekstas po lauku: ' + (zin ? zin.textContent : '—'));
    tikrink(nuslinkta === d.getElementById('id_city').closest('[data-field-wrap]'),
            'automatiškai nuslinkta į pirmą .field-invalid');
}

antraste('7. Dėžutės nuoroda nušoka į lauką');
{
    const DEZUTE = `<div class="form-error-box"><ul>
       <li><a href="#id_city">Miestas yra privalomas</a></li></ul></div>`;
    let nuslinkta = null;
    const dom = await kurti(`${DEZUTE}${FORMA}`, function (dm) {
        dm.window.HTMLElement.prototype.scrollIntoView = function () { nuslinkta = this; };
    });
    const d = dom.window.document;
    const a = d.querySelector('.form-error-box a');
    const e = new dom.window.MouseEvent('click', { bubbles: true, cancelable: true });
    a.dispatchEvent(e);
    tikrink(e.defaultPrevented, 'naršyklės šuolis atšauktas (kad neliktų po antrašte)');
    tikrink(nuslinkta === d.getElementById('id_city').closest('[data-field-wrap]'),
            'nuslinkta prie lauko');
}

antraste('8. Forma be data-validate neliečiama');
{
    const dom = await kurti('<form id="paieska" method="get">'
                            + '<input name="q" required></form>');
    const f = dom.window.document.getElementById('paieska');
    const e = new dom.window.Event('submit', { bubbles: true, cancelable: true });
    f.dispatchEvent(e);
    tikrink(!e.defaultPrevented, 'paieškos forma neblokuojama');
    tikrink(!f.hasAttribute('novalidate'), 'paieškos formai novalidate nepridėtas');
}

antraste('9. Paslėpti laukai netikrinami');
{
    const dom = await puslapis();
    const d = dom.window.document;
    const miestas = d.getElementById('id_city');
    miestas.hidden = true;                       // pvz. „valstija" ne JAV atveju
    d.getElementById('id_phone').value = '+3706';
    d.getElementById('id_email').value = 'a@b.lt';
    d.getElementById('id_agree_terms').checked = true;
    const e = pateikti(dom);
    tikrink(!e.defaultPrevented, 'paslėptas privalomas laukas nestabdo pateikimo');
}

console.log('\n' + '═'.repeat(62));
console.log(`gerai: ${gerai}, nepavyko: ${blogai}`);
process.exit(blogai ? 1 : 0);

}   // testai()

testai().catch(function (e) { console.error(e); process.exit(1); });
