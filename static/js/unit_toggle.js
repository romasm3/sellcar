/* ═══════════════════════════════════════════════════════════════════════
   AutoLeft — BENDRA MATAVIMO VIENETŲ PERJUNGIMO SISTEMA
   ═══════════════════════════════════════════════════════════════════════

   Naudojimas šablone — vienas atributas ant esamo input'o:

       <input type="number" name="power" data-unit-field="power" ...>

   Viskas kita (mygtukai, konvertavimas, paslėptas laukas, etiketės
   sutvarkymas) padaroma automatiškai. Šablone JS rašyti NEREIKIA.

   TAISYKLĖ: į DB VISADA keliauja kanoninė (metrinė) reikšmė.
   Vienetas DB nesaugomas — perjungiklis yra tik atvaizdavimui.

   Kaip veikia name-swap:
     • rodomas kanoninis vienetas → name lieka ant matomo input'o;
     • rodomas alternatyvus       → name nuimamas nuo matomo input'o ir
       perkeliamas į sugeneruotą <input type="hidden">, kuriame guli
       kanoninė reikšmė.
   Todėl serveris visada gauna tą patį lauko vardą su metrine reikšme.

   Naujas laukas = viena eilutė SPECS lentelėje + data-unit-field šablone.
   ═══════════════════════════════════════════════════════════════════════ */
(function () {
    'use strict';

    // ───────────────────────────────────────────────────────────────────
    // SPECIFIKACIJOS — raktas sutampa su lauko name atributu.
    //   canonical / alt — vienetų ženklai
    //   mul             — kanoninis × mul = alternatyvus
    //   inv             — atvirkštinė konversija: alt = mul / kanoninis
    //                     (l/100km ↔ mpg)
    //   dec / altDec    — po kablelio skaitmenys kiekvienoje pusėje.
    //                     dec PRIVALO atitikti modelio lauko tipą:
    //                     IntegerField → 0, DecimalField → decimal_places.
    //   family          — vienos šeimos laukai persijungia kartu ir
    //                     pasirinkimas įsimenamas localStorage'e.
    // ───────────────────────────────────────────────────────────────────
    var SPECS = {
        // — galia —
        power:            { canonical: 'kW',      alt: 'HP',   mul: 1.34102,   dec: 0, altDec: 0, family: 'power' },

        // — rida ir greitis —
        mileage:          { canonical: 'km',      alt: 'mi',   mul: 0.62137,   dec: 0, altDec: 0, family: 'distance' },
        mileage_km:       { canonical: 'km',      alt: 'mi',   mul: 0.62137,   dec: 0, altDec: 0, family: 'distance' },
        range_km:         { canonical: 'km',      alt: 'mi',   mul: 0.62137,   dec: 0, altDec: 0, family: 'distance' },
        max_speed_kmh:    { canonical: 'km/h',    alt: 'mph',  mul: 0.62137,   dec: 0, altDec: 0, family: 'distance' },

        // — variklio tūris (abu metriniai, atskira šeima) —
        engine_capacity:    { canonical: 'L',     alt: 'cm³',  mul: 1000,      dec: 1, altDec: 0, family: 'engine' },
        engine_capacity_cc: { canonical: 'cm³',   alt: 'ci',   mul: 0.0610237, dec: 0, altDec: 1, family: 'engine' },

        // — masė —
        curb_weight:      { canonical: 'kg',      alt: 'lbs',  mul: 2.20462,   dec: 0, altDec: 0, family: 'weight' },
        gross_weight_kg:  { canonical: 'kg',      alt: 'lbs',  mul: 2.20462,   dec: 0, altDec: 0, family: 'weight' },
        payload_kg:       { canonical: 'kg',      alt: 'lbs',  mul: 2.20462,   dec: 0, altDec: 0, family: 'weight' },

        // — matmenys —
        truck_length_mm:  { canonical: 'mm',      alt: 'in',   mul: 0.0393701, dec: 0, altDec: 1, family: 'dimension' },
        truck_width_mm:   { canonical: 'mm',      alt: 'in',   mul: 0.0393701, dec: 0, altDec: 1, family: 'dimension' },
        truck_height_mm:  { canonical: 'mm',      alt: 'in',   mul: 0.0393701, dec: 0, altDec: 1, family: 'dimension' },
        length_m:         { canonical: 'm',       alt: 'ft',   mul: 3.28084,   dec: 2, altDec: 1, family: 'dimension' },
        width_m:          { canonical: 'm',       alt: 'ft',   mul: 3.28084,   dec: 2, altDec: 1, family: 'dimension' },
        height_m:         { canonical: 'm',       alt: 'ft',   mul: 3.28084,   dec: 2, altDec: 1, family: 'dimension' },
        boat_length_m:    { canonical: 'm',       alt: 'ft',   mul: 3.28084,   dec: 2, altDec: 1, family: 'dimension' },
        boat_width_m:     { canonical: 'm',       alt: 'ft',   mul: 3.28084,   dec: 2, altDec: 1, family: 'dimension' },
        working_width_m:  { canonical: 'm',       alt: 'ft',   mul: 3.28084,   dec: 2, altDec: 1, family: 'dimension' },
        lift_height_m:    { canonical: 'm',       alt: 'ft',   mul: 3.28084,   dec: 2, altDec: 1, family: 'dimension' },
        fork_length_m:    { canonical: 'm',       alt: 'ft',   mul: 3.28084,   dec: 2, altDec: 1, family: 'dimension' },
        aisle_width_m2:   { canonical: 'm²',      alt: 'ft²',  mul: 10.7639,   dec: 2, altDec: 1, family: 'dimension' },

        // — talpa —
        truck_volume_m3:      { canonical: 'm³',  alt: 'ft³',  mul: 35.3147,   dec: 2, altDec: 1, family: 'dimension' },
        fuel_tank_capacity_l: { canonical: 'L',   alt: 'gal',  mul: 0.264172,  dec: 0, altDec: 1, family: 'volume' },
        boat_fuel_tank_l:     { canonical: 'L',   alt: 'gal',  mul: 0.264172,  dec: 1, altDec: 1, family: 'volume' },

        // — sąnaudos (atvirkštinė konversija) —
        fuel_consumption_combined: { canonical: 'l/100km', alt: 'mpg', mul: 235.215, inv: true, dec: 1, altDec: 1, family: 'consumption' }
    };

    var STORAGE_KEY = 'autoleft_units';

    // ───────────────────────────────────────────────────────────────────
    // ĮSIMINTAS PASIRINKIMAS
    // ───────────────────────────────────────────────────────────────────
    function loadPrefs() {
        try { return JSON.parse(window.localStorage.getItem(STORAGE_KEY) || '{}') || {}; }
        catch (e) { return {}; }
    }
    function savePref(family, unit) {
        try {
            var p = loadPrefs();
            p[family] = unit;
            window.localStorage.setItem(STORAGE_KEY, JSON.stringify(p));
        } catch (e) { /* private mode — tiesiog neįsimename */ }
    }

    // ───────────────────────────────────────────────────────────────────
    // SKAIČIAI
    // ───────────────────────────────────────────────────────────────────
    function roundTo(v, dec) {
        var f = Math.pow(10, dec);
        return Math.round(v * f) / f;
    }
    // Reikšmė į input.value — be tūkstančių skirtukų (type=number to nepriima)
    function forInput(v, dec) {
        if (v === null || isNaN(v)) return '';
        return String(roundTo(v, dec));
    }
    // Reikšmė į užuominą — su skirtukais, kad 150 000 būtų skaitoma
    function forHint(v, dec) {
        if (v === null || isNaN(v)) return '';
        try {
            return new Intl.NumberFormat(undefined, {
                minimumFractionDigits: 0, maximumFractionDigits: dec
            }).format(roundTo(v, dec));
        } catch (e) { return String(roundTo(v, dec)); }
    }
    function toAlt(spec, canon) {
        if (canon === null || isNaN(canon)) return null;
        if (spec.inv) return canon === 0 ? null : spec.mul / canon;
        return canon * spec.mul;
    }
    function toCanon(spec, alt) {
        if (alt === null || isNaN(alt)) return null;
        if (spec.inv) return alt === 0 ? null : spec.mul / alt;
        return alt / spec.mul;
    }

    // ───────────────────────────────────────────────────────────────────
    // ETIKETĖ — nuimam vienetą iš teksto, nes jį dabar rodo mygtukai.
    // "Galia (kW)" → "Galia"; "Rida su vienu įkrovimu, km" → "Rida su ..."
    // Keičiam tik paskutinį teksto mazgą, kad išliktų <span>*</span> ir pan.
    // ───────────────────────────────────────────────────────────────────
    function stripUnitFromLabel(label, spec) {
        if (!label) return;
        var units = [spec.canonical, spec.alt];
        var node = null;
        for (var i = label.childNodes.length - 1; i >= 0; i--) {
            var n = label.childNodes[i];
            if (n.nodeType === 3 && n.nodeValue.trim() !== '') { node = n; break; }
        }
        if (!node) return;
        var t = node.nodeValue.replace(/\s+$/, '');
        for (var j = 0; j < units.length; j++) {
            var u = units[j].replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            var paren = new RegExp('\\s*\\(\\s*' + u + '\\s*\\)$', 'i');
            var comma = new RegExp('\\s*,\\s*' + u + '$', 'i');
            if (paren.test(t)) { node.nodeValue = t.replace(paren, ''); return; }
            if (comma.test(t)) { node.nodeValue = t.replace(comma, ''); return; }
        }
    }

    // ───────────────────────────────────────────────────────────────────
    // MYGTUKŲ STILIUS — inline, kad veiktų ir be Tailwind rebuild'o
    // (žr. templates/listings/_design_patterns.md).
    // ───────────────────────────────────────────────────────────────────
    var BTN_BASE = 'padding:.2rem .45rem;font-size:.68rem;font-weight:600;line-height:1.35;' +
                   'cursor:pointer;background:#fff;color:#6b7280;border:1px solid #d1d5db;' +
                   'white-space:nowrap;';
    function paintBtn(btn, active, isFirst) {
        var s = BTN_BASE +
            (isFirst ? 'border-radius:.25rem 0 0 .25rem;' : 'border-radius:0 .25rem .25rem 0;margin-left:-1px;');
        if (active) s += 'background:#374151;border-color:#374151;color:#fff;position:relative;z-index:1;';
        btn.setAttribute('style', s);
    }

    // ───────────────────────────────────────────────────────────────────
    var fields = [];

    function build(input) {
        var key = input.dataset.unitField;
        var spec = SPECS[key];
        if (!spec) {
            if (window.console) console.warn('[unit_toggle] nežinomas data-unit-field:', key);
            return;
        }

        var f = {
            input: input,
            spec: spec,
            key: key,
            form: input.closest('form'),
            origName: input.getAttribute('name') || key,
            origStep: input.getAttribute('step'),
            origMax: input.getAttribute('max'),
            unit: spec.canonical,
            canon: null,
            hidden: null
        };

        // Pradinė reikšmė šablone visada kanoninė (iš DB / draft'o)
        var v0 = parseFloat(input.value);
        f.canon = isNaN(v0) ? null : v0;

        // ── Mygtukai — dedami į etiketės eilutę, kad input'o plotis nesikeistų
        var wrap = document.createElement('span');
        wrap.className = 'unit-switch';
        wrap.setAttribute('style', 'display:inline-flex;flex:0 0 auto;margin-left:auto;');

        f.btnCanon = document.createElement('button');
        f.btnCanon.type = 'button';
        f.btnCanon.textContent = spec.canonical;
        f.btnAlt = document.createElement('button');
        f.btnAlt.type = 'button';
        f.btnAlt.textContent = spec.alt;
        wrap.appendChild(f.btnCanon);
        wrap.appendChild(f.btnAlt);

        var label = input.parentNode ? input.parentNode.querySelector('label') : null;
        if (label) {
            stripUnitFromLabel(label, spec);
            var ls = label.getAttribute('style') || '';
            label.setAttribute('style', ls + ';display:flex;align-items:center;gap:.4rem;');
            label.appendChild(wrap);
        } else {
            // Atsarginis variantas — šalia input'o
            var row = document.createElement('span');
            row.setAttribute('style', 'display:inline-flex;align-items:center;gap:.4rem;width:100%;');
            input.parentNode.insertBefore(row, input);
            input.style.flex = '1';
            input.style.minWidth = '0';
            row.appendChild(input);
            row.appendChild(wrap);
        }

        // ── Užuomina po lauku
        f.hint = document.createElement('span');
        f.hint.className = 'unit-hint';
        f.hint.setAttribute('style', 'display:block;font-size:.68rem;color:#9ca3af;margin-top:.15rem;min-height:.9rem;');
        if (input.parentNode) input.parentNode.insertBefore(f.hint, input.nextSibling);

        f.btnCanon.addEventListener('click', function () { switchFamily(spec.family, spec.canonical, f); });
        f.btnAlt.addEventListener('click', function () { switchFamily(spec.family, spec.alt, f); });

        input.addEventListener('input', function () {
            var v = parseFloat(input.value);
            if (isNaN(v)) {
                f.canon = null;
            } else if (f.unit === spec.canonical) {
                f.canon = v;
            } else {
                f.canon = toCanon(spec, v);
            }
            syncName(f);
            updateHint(f);
        });

        fields.push(f);
        paintBtn(f.btnCanon, true, true);
        paintBtn(f.btnAlt, false, false);
        updateHint(f);
        return f;
    }

    // Perjungiam visus tos pačios šeimos laukus puslapyje + įsimenam
    function switchFamily(family, unit, origin) {
        var changed = false;
        for (var i = 0; i < fields.length; i++) {
            var f = fields[i];
            if (f.spec.family !== family) continue;
            // Šeimoje gali būti skirtingų vienetų porų (mm/in ir m/ft) —
            // renkamės pagal tai, ar prašoma kanoninio, ar alternatyvaus.
            var target = (unit === origin.spec.canonical) ? f.spec.canonical : f.spec.alt;
            if (f.unit === target) continue;
            f.unit = target;
            render(f);
            changed = true;
        }
        if (changed) savePref(family, (unit === origin.spec.canonical) ? 'canonical' : 'alt');
    }

    function render(f) {
        var spec = f.spec, input = f.input;
        var isCanon = (f.unit === spec.canonical);
        var dec = isCanon ? spec.dec : spec.altDec;

        input.value = (f.canon === null)
            ? ''
            : forInput(isCanon ? f.canon : toAlt(spec, f.canon), dec);

        // step/max turi atitikti rodomą vienetą, kitaip naršyklė blokuoja įvestį
        if (isCanon) {
            if (f.origStep === null) input.removeAttribute('step'); else input.setAttribute('step', f.origStep);
            if (f.origMax === null) input.removeAttribute('max'); else input.setAttribute('max', f.origMax);
        } else {
            input.setAttribute('step', spec.altDec > 0 ? 'any' : '1');
            if (f.origMax !== null) {
                var m = parseFloat(f.origMax);
                if (!isNaN(m)) input.setAttribute('max', forInput(toAlt(spec, m), spec.altDec));
            }
        }

        paintBtn(f.btnCanon, isCanon, true);
        paintBtn(f.btnAlt, !isCanon, false);
        syncName(f);
        updateHint(f);
    }

    // name visada ten, kur kanoninė reikšmė
    function syncName(f) {
        var isCanon = (f.unit === f.spec.canonical);
        if (isCanon) {
            f.input.setAttribute('name', f.origName);
            if (f.hidden) { f.hidden.parentNode.removeChild(f.hidden); f.hidden = null; }
            return;
        }
        f.input.removeAttribute('name');
        if (!f.hidden) {
            f.hidden = document.createElement('input');
            f.hidden.type = 'hidden';
            f.hidden.name = f.origName;
            f.hidden.setAttribute('data-canonical-for', f.key);
            (f.form || f.input.parentNode).appendChild(f.hidden);
        }
        f.hidden.value = (f.canon === null) ? '' : forInput(f.canon, f.spec.dec);
    }

    function updateHint(f) {
        var spec = f.spec;
        if (f.canon === null || isNaN(f.canon)) { f.hint.textContent = ''; return; }
        if (f.unit === spec.canonical) {
            var a = toAlt(spec, f.canon);
            f.hint.textContent = (a === null) ? '' : '≈ ' + forHint(a, spec.altDec) + ' ' + spec.alt;
        } else {
            f.hint.textContent = '≈ ' + forHint(f.canon, spec.dec) + ' ' + spec.canonical;
        }
    }

    function init() {
        var inputs = document.querySelectorAll('input[data-unit-field]');
        if (!inputs.length) return;
        for (var i = 0; i < inputs.length; i++) build(inputs[i]);

        // Pritaikom įsimintus pasirinkimus
        var prefs = loadPrefs();
        for (var j = 0; j < fields.length; j++) {
            var f = fields[j];
            if (prefs[f.spec.family] === 'alt' && f.unit !== f.spec.alt) {
                f.unit = f.spec.alt;
                render(f);
            }
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    window.AutoLeftUnits = { specs: SPECS, fields: fields };
})();
