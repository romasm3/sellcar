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

   ── RODYMO PUSĖ (skelbimo peržiūra) ──

       <span data-unit-show="power" data-unit-raw="150">150 kW</span>

   Serveris atiduoda metrinę reikšmę tekste (veikia ir be JS), o skriptas
   prirašo užuominą „≈ 201 HP" ir padaro elementą paspaudžiamą. Paspaudus
   pagrindinė ir antrinė reikšmės susikeičia vietomis.

   data-unit-raw gali turėti kelias reikšmes per „|" — tada rodoma
   „1200 × 800 × 600 mm" (matmenys viena eilute).

   ── DIAPAZONAI „nuo–iki" ──

   Antram poros laukui dedam data-unit-quiet: jis konvertuojasi kartu,
   bet mygtukų ir užuominos nekartoja — vienai porai užtenka vieno
   perjungiklio prie bendros etiketės.

   SVARBU: data-unit-raw reikšmė TURI būti nelokalizuota (|unlocalize),
   nes LT lokalėje {{ 12.5 }} atsiduoda kaip „12,5" ir parseFloat luš.

   Rodymo ir įvedimo pusės dalijasi ta pačia įsiminta nuostata: pardavėjas,
   perjungęs formą į mylias, ir skelbimuose matys mylias.

   Naujas laukas = viena eilutė SPECS lentelėje + data-unit-field / -show.
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
    function savePref(family, mode) {
        try {
            var p = loadPrefs();
            p[family] = mode;
            window.localStorage.setItem(STORAGE_KEY, JSON.stringify(p));
        } catch (e) { /* private mode — tiesiog neįsimename */ }
    }

    // Kurį vienetą šiuo metu rodo kiekviena šeima: 'canonical' | 'alt'.
    // Vienintelis tiesos šaltinis ir įvedimo laukams, ir rodymo elementams.
    var familyMode = {};
    function modeOf(spec) { return familyMode[spec.family] === 'alt' ? 'alt' : 'canonical'; }
    function isAlt(spec) { return modeOf(spec) === 'alt'; }
    function unitOf(spec) { return isAlt(spec) ? spec.alt : spec.canonical; }
    function decOf(spec) { return isAlt(spec) ? spec.altDec : spec.dec; }

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
    // Etiketė gali būti <label> arba <span class="sp-label"> / .field-label /
    // .form-label — projekte naudojami visi trys.
    function isLabelish(n) {
        if (n.tagName === 'LABEL') return true;
        var c = (typeof n.className === 'string') ? n.className : '';
        return /(^|\s|-)label(\s|$|-)/i.test(c);
    }

    // Paieškos tvarka: ankstesni broliai, tada tas pats vienu lygiu aukščiau
    // (diapazonuose „nuo–iki" abu input'ai guli atskirame flex konteineryje),
    // ir tik tada tėvinis mazgas — jei jame vienintelis input.
    function findLabel(input) {
        for (var el = input, up = 0; el && up < 2; el = el.parentNode, up++) {
            var n = el.previousElementSibling;
            while (n) {
                if (isLabelish(n)) return n;
                if (n.tagName === 'INPUT' || n.tagName === 'SELECT') break;
                n = n.previousElementSibling;
            }
        }
        var p = input.parentNode;
        if (!p) return null;
        if (p.querySelectorAll('input, select, textarea').length > 1) return null;
        return p.querySelector('label');
    }

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
            // Tarpai vienete lankstūs: "l/100km" turi sutapti su "(l/100 km)"
            var u = units[j].split('').map(function (c) {
                return c.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            }).join('\\s*');
            var paren = new RegExp('\\s*\\(\\s*' + u + '\\s*\\)$', 'i');
            var comma = new RegExp('\\s*,\\s*' + u + '$', 'i');
            // „Bendroji masė kg" — vienetas be skliaustų ir be kablelio
            var bare = new RegExp('\\s+' + u + '$', 'i');
            if (paren.test(t)) { node.nodeValue = t.replace(paren, ''); return; }
            if (comma.test(t)) { node.nodeValue = t.replace(comma, ''); return; }
            if (bare.test(t)) { node.nodeValue = t.replace(bare, ''); return; }
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

    function onUserInput(f) {
        return function () {
            var v = parseFloat(f.input.value);
            if (isNaN(v)) {
                f.canon = null;
            } else if (isAlt(f.spec)) {
                f.canon = toCanon(f.spec, v);
            } else {
                f.canon = v;
            }
            syncName(f);
            updateHint(f);
        };
    }

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
            canon: null,
            hidden: null
        };

        // Pradinė reikšmė šablone visada kanoninė (iš DB / draft'o)
        var v0 = parseFloat(input.value);
        f.canon = isNaN(v0) ? null : v0;

        // ── Mygtukai — dedami į etiketės eilutę, kad input'o plotis nesikeistų
        var wrap = document.createElement('span');
        wrap.className = 'unit-switch';
        wrap.dataset.unitFor = f.origName;      // kuriam laukui priklauso
        wrap.setAttribute('style', 'display:inline-flex;flex:0 0 auto;margin-left:auto;');

        f.btnCanon = document.createElement('button');
        f.btnCanon.type = 'button';
        f.btnCanon.textContent = spec.canonical;
        f.btnAlt = document.createElement('button');
        f.btnAlt.type = 'button';
        f.btnAlt.textContent = spec.alt;
        wrap.appendChild(f.btnCanon);
        wrap.appendChild(f.btnAlt);

        // Diapazono antras laukas („iki") — jokių savo mygtukų ir užuominos
        f.quiet = input.hasAttribute('data-unit-quiet');
        if (f.quiet) {
            input.addEventListener('input', onUserInput(f));
            fields.push(f);
            return f;
        }

        // Įsimenam, kur dėti užuominą, PRIEŠ galimą input'o perkėlimą.
        // Diapazonuose („nuo" ir „iki" viename grid-cols-2 konteineryje)
        // užuomina turi atsidurti PO visu konteineriu — kitaip ji užimtų
        // tinklelio langelį ir nustumtų „iki" į kitą eilutę.
        var hintParent = input.parentNode;
        var hintRef = input.nextSibling;
        if (hintParent && hintParent.querySelectorAll('[data-unit-field]').length > 1
                && hintParent.parentNode) {
            hintRef = hintParent.nextSibling;
            hintParent = hintParent.parentNode;
        }

        var label = findLabel(input);
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
        if (hintParent) hintParent.insertBefore(f.hint, hintRef);

        f.btnCanon.addEventListener('click', function () { setFamilyMode(spec.family, 'canonical'); });
        f.btnAlt.addEventListener('click', function () { setFamilyMode(spec.family, 'alt'); });

        input.addEventListener('input', onUserInput(f));

        fields.push(f);
        paintBtn(f.btnCanon, !isAlt(spec), true);
        paintBtn(f.btnAlt, isAlt(spec), false);
        updateHint(f);
        return f;
    }

    // Perjungiam VISĄ šeimą — ir įvedimo laukus, ir peržiūros reikšmes.
    // Visi svoriai persijungia kartu; kitos šeimos nepajuda.
    function setFamilyMode(family, mode) {
        if (modeOf({ family: family }) === mode) return;
        familyMode[family] = mode;
        savePref(family, mode);
        repaintFamily(family);
    }

    function repaintFamily(family) {
        var i;
        for (i = 0; i < fields.length; i++) {
            if (fields[i].spec.family === family) render(fields[i]);
        }
        for (i = 0; i < views.length; i++) {
            if (views[i].spec.family === family) renderView(views[i]);
        }
    }

    function render(f) {
        var spec = f.spec, input = f.input;
        var isCanon = !isAlt(spec);
        var dec = decOf(spec);

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

        if (!f.quiet) {
            paintBtn(f.btnCanon, isCanon, true);
            paintBtn(f.btnAlt, !isCanon, false);
        }
        syncName(f);
        updateHint(f);
    }

    // name visada ten, kur kanoninė reikšmė
    function syncName(f) {
        var isCanon = !isAlt(f.spec);
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
            // Kai kurios formos renka juodraštį pagal [data-autosave="true"],
            // ne pagal visą formą. Be šito laukas dingtų iš juodraščio, kol
            // vartotojas žiūri alternatyviais vienetais.
            if (f.input.hasAttribute('data-autosave')) {
                f.hidden.setAttribute('data-autosave', f.input.getAttribute('data-autosave'));
            }
            (f.form || f.input.parentNode).appendChild(f.hidden);
        }
        f.hidden.value = (f.canon === null) ? '' : forInput(f.canon, f.spec.dec);
    }

    function updateHint(f) {
        var spec = f.spec;
        if (f.quiet || !f.hint) return;
        if (f.canon === null || isNaN(f.canon)) { f.hint.textContent = ''; return; }
        if (!isAlt(spec)) {
            var a = toAlt(spec, f.canon);
            f.hint.textContent = (a === null) ? '' : '≈ ' + forHint(a, spec.altDec) + ' ' + spec.alt;
        } else {
            f.hint.textContent = '≈ ' + forHint(f.canon, spec.dec) + ' ' + spec.canonical;
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // RODYMO PUSĖ — skelbimo peržiūros reikšmės
    // ═══════════════════════════════════════════════════════════════
    var views = [];

    var HINT_STYLE = 'color:#9ca3af;font-size:.85em;margin-left:.35rem;white-space:nowrap;' +
                     'border-bottom:1px dashed #d1d5db;';

    function buildView(el) {
        var key = el.dataset.unitShow;
        var spec = SPECS[key];
        if (!spec) {
            if (window.console) console.warn('[unit_toggle] nežinomas data-unit-show:', key);
            return;
        }
        // Kelios reikšmės per „|" = matmenys vienoje eilutėje (1200 × 800 × 600 mm)
        var raw = String(el.dataset.unitRaw || '').split('|').map(function (x) {
            var n = parseFloat(x);
            return isNaN(n) ? null : n;
        });
        if (!raw.some(function (n) { return n !== null; })) return;   // nėra ką rodyti

        var v = { el: el, spec: spec, raw: raw, hint: null };
        v.hint = document.createElement('span');
        v.hint.className = 'unit-hint';
        v.hint.setAttribute('style', HINT_STYLE);

        el.style.cursor = 'pointer';
        if (window.UNIT_TOGGLE_TITLE) el.title = window.UNIT_TOGGLE_TITLE;
        el.addEventListener('click', function () {
            setFamilyMode(spec.family, isAlt(spec) ? 'canonical' : 'alt');
        });

        views.push(v);
        renderView(v);
    }

    function joinValues(spec, values, toUnit) {
        var dec = (toUnit === 'alt') ? spec.altDec : spec.dec;
        return values.map(function (n) {
            if (n === null) return '—';
            var out = (toUnit === 'alt') ? toAlt(spec, n) : n;
            return (out === null) ? '—' : forHint(out, dec);
        }).join(' × ');
    }

    function renderView(v) {
        var spec = v.spec, alt = isAlt(spec);
        v.el.textContent = joinValues(spec, v.raw, alt ? 'alt' : 'canon') + ' ' + unitOf(spec);
        v.hint.textContent = '≈ ' + joinValues(spec, v.raw, alt ? 'canon' : 'alt') + ' ' +
                             (alt ? spec.canonical : spec.alt);
        v.el.appendChild(v.hint);
    }

    function init() {
        var prefs = loadPrefs();
        Object.keys(prefs).forEach(function (fam) {
            if (prefs[fam] === 'alt') familyMode[fam] = 'alt';
        });

        var inputs = document.querySelectorAll('input[data-unit-field]');
        var i;
        for (i = 0; i < inputs.length; i++) build(inputs[i]);
        // Pirmas piešimas jau įvertina įsimintą nuostatą
        for (i = 0; i < fields.length; i++) {
            if (isAlt(fields[i].spec)) render(fields[i]);
        }

        var shows = document.querySelectorAll('[data-unit-show]');
        for (i = 0; i < shows.length; i++) buildView(shows[i]);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // ═══════════════════════════════════════════════════════════════
    // VIEŠAS API — formoms, kurios turi savo autosave / validaciją.
    // Visada dirba KANONINĖMIS reikšmėmis, nesvarbu ką mato vartotojas.
    // ═══════════════════════════════════════════════════════════════
    function byName(name) {
        for (var i = 0; i < fields.length; i++) {
            if (fields[i].origName === name) return fields[i];
        }
        return null;
    }

    // Kanoninė reikšmė kaip eilutė ('' jei tuščia) — tinka tiesiai į JSON/POST
    function getCanonical(name) {
        var f = byName(name);
        if (!f || f.canon === null || isNaN(f.canon)) return '';
        return forInput(f.canon, f.spec.dec);
    }

    // Įrašom kanoninę reikšmę (pvz. atkuriant juodraštį) ir perpiešiam
    function setCanonical(name, value) {
        var f = byName(name);
        if (!f) return false;
        var v = parseFloat(value);
        f.canon = isNaN(v) ? null : v;
        render(f);
        return true;
    }

    window.AutoLeftUnits = {
        specs: SPECS, fields: fields, views: views,
        setFamilyMode: setFamilyMode,
        get: getCanonical,
        set: setCanonical
    };
})();
