/* ═══════════════════════════════════════════════════════════════════
   static/js/unit_toggle.js testai.

   Paleidimas:   npm i jsdom && node docs/unit_toggle_tests.js

   Svarbiausia, ką tikrina: kad ir kokį vienetą vartotojas matytų,
   POST'e visada guli kanoninė (metrinė) reikšmė po teisingu lauko vardu.
   ═══════════════════════════════════════════════════════════════════ */
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const JS = fs.readFileSync(path.join(__dirname, '..', 'static', 'js', 'unit_toggle.js'), 'utf8');

const HTML = `<!doctype html><html><body><form id="f">
 <div><label class="l">Galia (kW)</label>
   <input type="number" name="power" data-unit-field="power" min="0" step="1" value="150"></div>
 <div><label class="l">Rida (km) <span class="req">*</span></label>
   <input type="number" name="mileage" data-unit-field="mileage" min="0" step="1" value="150000"></div>
 <div><label class="l">Svoris, kg</label>
   <input type="number" name="curb_weight" data-unit-field="curb_weight" min="0" step="1" value=""></div>
 <div><label class="l">Ilgis (m)</label>
   <input type="number" name="length_m" data-unit-field="length_m" min="0" step="0.01" value="12.5"></div>
 <div><label class="l">Darbinis tūris (l)</label>
   <input type="number" name="engine_capacity" data-unit-field="engine_capacity" step="0.1" value="2.0"></div>
 <div><label class="l">Kuro sąnaudos (l/100 km)</label>
   <input type="number" name="fuel_consumption_combined" data-unit-field="fuel_consumption_combined" step="0.1" value="6.0"></div>
 <div><label class="l">Degalų bako talpa (l)</label>
   <input type="number" name="fuel_tank_capacity_l" data-unit-field="fuel_tank_capacity_l" step="1" value="70"></div>
 <div><label class="l">Engine displacement (cm³)</label>
   <input type="number" name="engine_capacity" data-unit-field="engine_capacity_cc" step="1" value="1300"></div>
 <div><label class="l">Bendra masė (kg)</label>
   <input type="number" name="gross_weight_kg" data-unit-field="gross_weight_kg" max="40000" step="1" value="18000"></div>
 <p>Galia: <span id="v-power" data-unit-show="power" data-unit-raw="150">150 kW</span></p>
 <p>Rida: <span id="v-mileage" data-unit-show="mileage" data-unit-raw="150000">150 000 km</span></p>
 <p>Matmenys: <span id="v-dims" data-unit-show="truck_length_mm" data-unit-raw="1200|800|600">1200 × 800 × 600 mm</span></p>
 <p>Nėra: <span id="v-empty" data-unit-show="payload_kg" data-unit-raw="">—</span></p>
</form></body></html>`;

let failures = 0;
function chk(name, got, want) {
  const ok = String(got) === String(want);
  if (!ok) failures++;
  console.log((ok ? '  ok   ' : '  FAIL ') + name + '  got=' + JSON.stringify(String(got)) +
              (ok ? '' : ' want=' + JSON.stringify(String(want))));
}

function boot(storage) {
  return new Promise(res => {
    const dom = new JSDOM(HTML, { runScripts: 'outside-only', url: 'https://x.test/' });
    if (storage) dom.window.localStorage.setItem('autoleft_units', JSON.stringify(storage));
    dom.window.eval(JS);
    dom.window.addEventListener('load', () => setTimeout(() => res(dom), 0));
  });
}
const posted = (dom) => {
  const o = {};
  dom.window.document.querySelectorAll('#f [name]').forEach(e => { o[e.name] = e.value; });
  return o;
};
// Ką realiai išsiųs BŪTENT šis laukas (fixture'e yra du 'engine_capacity')
const postedFor = (dom, key) => {
  const vis = dom.window.document.querySelector(`[data-unit-field="${key}"]`);
  if (vis.hasAttribute('name')) return vis.value;
  return dom.window.document.querySelector(`[data-canonical-for="${key}"]`).value;
};
const F = (dom, n) => dom.window.document.querySelector(`[data-unit-field="${n}"]`);
const lab = (dom, n) => F(dom, n).parentNode.querySelector('label');
// etiketės tekstas be mygtukų
const labText = (dom, n) => [...lab(dom, n).childNodes]
    .filter(x => x.nodeType === 3).map(x => x.nodeValue).join('').trim();
const btns = (dom, n) => lab(dom, n).querySelectorAll('.unit-switch button');
const hint = (dom, n) => F(dom, n).parentNode.querySelector('.unit-hint').textContent;
function type(dom, n, v) {
  const i = F(dom, n);
  i.value = String(v);
  i.dispatchEvent(new dom.window.Event('input'));
}
const nb = s => s.replace(/ | /g, ' ');

(async () => {

console.log('\n── 1. Etiketės ir mygtukai ──');
{
  const d = await boot();
  chk('"Galia (kW)" -> vienetas nuimtas', labText(d,'power'), 'Galia');
  chk('"Svoris, kg" -> vienetas nuimtas', labText(d,'curb_weight'), 'Svoris');
  chk('"(l/100 km)" su tarpu nuimtas', labText(d,'fuel_consumption_combined'), 'Kuro sąnaudos');
  chk('privalomumo * islieka', lab(d,'mileage').querySelector('.req').textContent, '*');
  chk('mygtuku kiekis', btns(d,'power').length, 2);
  chk('mygtuku uzrasai', [...btns(d,'power')].map(b=>b.textContent).join('/'), 'kW/HP');
}

console.log('\n── 2. Pradinė būsena = kanoninė ──');
{
  const d = await boot();
  chk('power value', F(d,'power').value, '150');
  chk('power name vietoje', F(d,'power').getAttribute('name'), 'power');
  chk('power hint', hint(d,'power'), '≈ 201 HP');
  chk('mileage hint', nb(hint(d,'mileage')), '≈ 93,206 mi');
  chk('tuscias laukas be hint', hint(d,'curb_weight'), '');
  chk('POST power', posted(d).power, '150');
}

console.log('\n── 3. Perjungimas į alternatyvų vienetą ──');
{
  const d = await boot();
  btns(d,'power')[1].click();
  chk('rodo HP', F(d,'power').value, '201');
  chk('name nuimtas nuo matomo', F(d,'power').getAttribute('name'), null);
  chk('POST vis tiek kW', posted(d).power, '150');
  chk('hint rodo kW', hint(d,'power'), '≈ 150 kW');
  btns(d,'power')[0].click();
  chk('grizus i kW nera nuokrypio', F(d,'power').value, '150');
  chk('POST po grizimo', posted(d).power, '150');
  chk('hidden pasalintas', d.window.document.querySelectorAll('[data-canonical-for="power"]').length, 0);
}

console.log('\n── 4. Įvestis alternatyviais vienetais ──');
{
  const d = await boot();
  btns(d,'mileage')[1].click();
  type(d, 'mileage', 60000);
  chk('POST km', posted(d).mileage, String(Math.round(60000/0.62137)));
  chk('hint', nb(hint(d,'mileage')), '≈ 96,561 km');
  type(d, 'mileage', '');
  chk('tuscia -> tuscias POST', posted(d).mileage, '');
  chk('tuscia -> nera hint', hint(d,'mileage'), '');
}

console.log('\n── 5. Šeima persijungia kartu, kitos – ne ──');
{
  const d = await boot();
  btns(d,'length_m')[1].click();
  chk('length_m -> ft', F(d,'length_m').value, '41');
  chk('step pritaikytas', F(d,'length_m').getAttribute('step'), 'any');
  chk('power liko kW', F(d,'power').value, '150');
  chk('curb_weight liko kg', [...btns(d,'curb_weight')][0].getAttribute('style').includes('#374151'), 'true');
  chk('POST length_m metrais', posted(d).length_m, '12.5');
}

console.log('\n── 6. Atvirkštinė konversija (l/100km ↔ mpg) ──');
{
  const d = await boot();
  btns(d,'fuel_consumption_combined')[1].click();
  chk('6 l/100km -> mpg', F(d,'fuel_consumption_combined').value, '39.2');
  type(d, 'fuel_consumption_combined', 30);
  chk('POST l/100km', posted(d).fuel_consumption_combined, '7.8');
}

console.log('\n── 7. Sveikaskaitis laukas negauna trupmenos ──');
{
  const d = await boot();
  btns(d,'fuel_tank_capacity_l')[1].click();
  chk('70 L -> gal', F(d,'fuel_tank_capacity_l').value, '18.5');
  type(d, 'fuel_tank_capacity_l', 20);
  chk('POST sveikas L', posted(d).fuel_tank_capacity_l, '76');
  chk('be kablelio', /^\d+$/.test(posted(d).fuel_tank_capacity_l), 'true');
}

console.log('\n── 8. Įsimintas pasirinkimas pritaikomas pakrovus ──');
{
  const d = await boot({ distance: 'alt', weight: 'alt' });
  chk('mileage is karto mi', F(d,'mileage').value, '93206');
  chk('POST vis tiek km', posted(d).mileage, '150000');
  chk('power liko kW', F(d,'power').value, '150');
}

console.log('\n── 9. L ↔ cm³ ──');
{
  const d = await boot();
  btns(d,'engine_capacity')[1].click();
  chk('2.0 L -> cm3', F(d,'engine_capacity').value, '2000');
  type(d, 'engine_capacity', 1598);
  chk('POST litrais', postedFor(d,'engine_capacity'), '1.6');
}

console.log('\n── 10. name ≠ spec raktas (moto_part: cm³ po vardu engine_capacity) ──');
{
  const d = await boot();
  const inp = d.window.document.querySelector('[data-unit-field="engine_capacity_cc"]');
  chk('etiketes vienetas nuimtas', labText(d,'engine_capacity_cc'), 'Engine displacement');
  chk('POST po teisingu vardu', postedFor(d,'engine_capacity_cc'), '1300');
  lab(d,'engine_capacity_cc').querySelectorAll('.unit-switch button')[1].click();
  chk('1300 cm3 -> ci', inp.value, '79.3');
  chk('POST vis tiek cm3', postedFor(d,'engine_capacity_cc'), '1300');
  chk('hidden vardas = name atributas', d.window.document.querySelector('[data-canonical-for="engine_capacity_cc"]').name, 'engine_capacity');
  chk('vardas nepakeistas i spec rakta', d.window.document.querySelectorAll('[name="engine_capacity_cc"]').length, 0);
}

console.log('\n── 11. max atributas perskaiciuojamas ──');
{
  const d = await boot();
  chk('pradinis max', F(d,'gross_weight_kg').getAttribute('max'), '40000');
  btns(d,'gross_weight_kg')[1].click();
  chk('max lbs', F(d,'gross_weight_kg').getAttribute('max'), '88185');
  chk('reiksme lbs', F(d,'gross_weight_kg').value, '39683');
  btns(d,'gross_weight_kg')[0].click();
  chk('max atstatytas', F(d,'gross_weight_kg').getAttribute('max'), '40000');
  chk('reiksme atstatyta', F(d,'gross_weight_kg').value, '18000');
}

console.log('\n── 12. Peržiūra: užuomina ir paspaudimas ──');
{
  const d = await boot();
  const V = id => d.window.document.getElementById(id);
  const main = el => [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue).join('').trim();
  chk('pagrindine reiksme', nb(main(V('v-power'))), '150 kW');
  chk('uzuomina', V('v-power').querySelector('.unit-hint').textContent, '≈ 201 HP');
  chk('paspaudziamas', V('v-power').style.cursor, 'pointer');
  V('v-power').click();
  chk('po paspaudimo rodo HP', nb(main(V('v-power'))), '201 HP');
  chk('uzuomina apsivertė', V('v-power').querySelector('.unit-hint').textContent, '≈ 150 kW');
}

console.log('\n── 13. Peržiūra: matmenys viena eilute ir tuščios reikšmės ──');
{
  const d = await boot();
  const V = id => d.window.document.getElementById(id);
  const main = el => [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue).join('').trim();
  chk('metrais', nb(main(V('v-dims'))), '1,200 × 800 × 600 mm');
  V('v-dims').click();
  chk('coliais', nb(main(V('v-dims'))), '47.2 × 31.5 × 23.6 in');
  chk('tuscias neliestas', V('v-empty').textContent, '—');
  chk('tuscias nepaspaudziamas', V('v-empty').style.cursor || '(nėra)', '(nėra)');
}

console.log('\n── 14. Forma ir peržiūra dalijasi ta pačia nuostata ──');
{
  const d = await boot();
  const V = id => d.window.document.getElementById(id);
  const main = el => [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue).join('').trim();
  // paspaudžiam peržiūros reikšmę → turi persijungti ir formos laukas
  V('v-mileage').click();
  chk('formos laukas persijunge i mi', F(d,'mileage').value, '93206');
  chk('formos POST vis tiek km', posted(d).mileage, '150000');
  chk('kitos seimos rodinys nepajudejo', nb(main(V('v-power'))), '150 kW');
  // atgal per formos mygtuka → persijungia ir rodinys
  btns(d,'mileage')[0].click();
  chk('rodinys grizo i km', nb(main(V('v-mileage'))), '150,000 km');
}

console.log(failures ? `\n✗ ${failures} nesėkmė(s)\n` : '\n✓ visi testai praėjo\n');
process.exit(failures ? 1 : 0);
})();
