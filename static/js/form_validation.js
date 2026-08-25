/* ═══════════════════════════════════════════════════════════════════
 * PRIVALOMŲ LAUKŲ TIKRINIMAS — vienas failas visoms /create/ formoms.
 *
 * Iki šiol kiekvienas šablonas turėjo savo validaciją inline: vienur
 * tik viršutinė dėžutė, kitur tik rėmelis, kai kur nieko. Nuo šiol —
 * viena elgsena:
 *
 *   · pateikiant: pereinam per [required] ir tikrinam checkValidity()
 *   · nevalidiems — .field-invalid + .field-error-msg po lauku
 *   · bent viena klaida → preventDefault(), nuslenkam ir fokusuojam pirmą
 *   · užpildžius lauką (input/change) žymė nusiimama iškart
 *   · atsidarius puslapiui su serverio klaidomis — tas pats vaizdas ir
 *     tas pats nuslinkimas (serveris paduoda error_fields per
 *     _form_errors.html)
 *
 * Kabinasi prie <form data-validate> — žr. listings/partials/_form_errors.html.
 * Neliečia paieškos formų ir nieko, kas šio atributo neturi.
 * ═══════════════════════════════════════════════════════════════════ */
(function () {
    'use strict';

    var NEVALIDUS = 'field-invalid';
    var ETIKETE = 'label-invalid';
    var ZINUTE = 'field-error-msg';
    var ZYME = 'data-klaidos-zinute';   // mūsų įterptos žinutės žymė

    /* Tekstai. Kalba ateina iš serverio (žr. _form_errors.html); be jo —
       lietuviškai, nes tai šaltinio kalba. */
    function tekstai() {
        var t = (window.AutoLeftFormTekstai || {});
        return {
            privalomas: t.privalomas || 'Privalomas laukas',
            taisykles: t.taisykles || 'Turite sutikti su taisyklėmis',
            netinkamas: t.netinkamas || 'Netinkama reikšmė',
        };
    }

    /* Ar tai sutikimo su taisyklėmis langelis */
    function arTaisykles(el) {
        var n = (el.getAttribute('name') || '').toLowerCase();
        return el.type === 'checkbox' &&
            (n.indexOf('terms') !== -1 || n.indexOf('agree') !== -1 ||
             n.indexOf('taisykl') !== -1);
    }

    function pranesimoTekstas(el) {
        var t = tekstai();
        if (arTaisykles(el)) { return t.taisykles; }
        if (el.value && el.validity && !el.validity.valueMissing) {
            /* Užpildyta, bet netinka (type=email, pattern, min/max).
               Naršyklės validationMessage yra jos kalba ir mūsų sąsajoje
               atrodytų svetimas, todėl rodom savo tekstą. */
            return t.netinkamas;
        }
        return t.privalomas;
    }

    /* Kur dėti rėmelį. Pasirinkimo laukai dažnai suvynioti į apvalkalą
       su savo rėmeliu — tada dažom apvalkalą, kitaip rėmelis atsidurtų
       po juo ir nesimatytų. */
    function dazomas(el) {
        var wrap = el.closest('[data-field-wrap]');
        if (wrap && el.type !== 'checkbox' && el.type !== 'radio') { return wrap; }
        return el;
    }

    /* Kur dėti žinutę — po visu lauko bloku, ne viduryje apvalkalo */
    function zinutesVieta(el) {
        return el.closest('[data-field-wrap]') ||
               el.closest('label') ||
               el;
    }

    function etikete(el) {
        var id = el.getAttribute('id');
        if (id) {
            var lbl = document.querySelector('label[for="' + CSS.escape(id) + '"]');
            if (lbl) { return lbl; }
        }
        var wrap = el.closest('[data-field-wrap]');
        return wrap ? wrap.querySelector('label') : null;
    }

    /* Žinutė yra IŠKART po lauko bloku. Ieškom jos būtent taip, o ne
       per parentNode.querySelector: visų laukų blokai turi tą patį tėvą
       (formą), tad bendra paieška rasdavo pirmo lauko žinutę ir visi
       laukai perrašinėdavo tą pačią — matėsi viena klaida vietoj visų. */
    function esamaZinute(vieta) {
        var kitas = vieta.nextElementSibling;
        return (kitas && kitas.hasAttribute && kitas.hasAttribute(ZYME)) ? kitas : null;
    }

    function pazymeti(el, tekstas) {
        dazomas(el).classList.add(NEVALIDUS);
        var lbl = etikete(el);
        if (lbl) { lbl.classList.add(ETIKETE); }

        var vieta = zinutesVieta(el);
        var zin = esamaZinute(vieta);
        if (!zin) {
            zin = document.createElement('span');
            zin.className = ZINUTE;
            zin.setAttribute(ZYME, el.getAttribute('name') || '1');
            if (vieta.parentNode) {
                vieta.parentNode.insertBefore(zin, vieta.nextSibling);
            }
        }
        zin.textContent = tekstas;
        el.setAttribute('aria-invalid', 'true');
    }

    function nuimti(el) {
        dazomas(el).classList.remove(NEVALIDUS);
        el.classList.remove(NEVALIDUS);
        var lbl = etikete(el);
        if (lbl) { lbl.classList.remove(ETIKETE); }
        var zin = esamaZinute(zinutesVieta(el));
        if (zin) { zin.remove(); }
        el.removeAttribute('aria-invalid');
    }

    function uzpildytas(el) {
        if (el.type === 'checkbox' || el.type === 'radio') { return el.checked; }
        return String(el.value || '').trim() !== '';
    }

    function priePirmo(el) {
        var taikinys = dazomas(el);
        if (taikinys.scrollIntoView) {
            taikinys.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        /* Fokusas iškart nuslinktų be animacijos, todėl truputį palaukiam.
           preventScroll palieka mūsų sklandų nuslinkimą. */
        setTimeout(function () {
            try { el.focus({ preventScroll: true }); } catch (e) { el.focus(); }
        }, 300);
    }

    /* Paslėptų laukų netikrinam: forma dažnai turi neaktyvių sekcijų
       (pvz. „valstija" tik JAV), o naršyklė pati ant jų užstrigtų. */
    function matomas(el) {
        if (el.disabled) { return false; }
        return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    }

    function laukai(forma) {
        return Array.prototype.filter.call(
            forma.querySelectorAll('[required]'), matomas);
    }

    function tikrinti(forma) {
        var blogi = [];
        laukai(forma).forEach(function (el) {
            if (el.checkValidity()) { nuimti(el); return; }
            pazymeti(el, pranesimoTekstas(el));
            blogi.push(el);
        });
        return blogi;
    }

    function prijungti(forma) {
        if (forma.__validacijaPrijungta) { return; }
        forma.__validacijaPrijungta = true;

        /* Naršyklės burbulai išjungiami — rodom savo žymėjimą. */
        forma.setAttribute('novalidate', 'novalidate');

        forma.addEventListener('submit', function (e) {
            var blogi = tikrinti(forma);
            if (!blogi.length) { return; }
            e.preventDefault();
            e.stopPropagation();
            priePirmo(blogi[0]);
        });

        /* Užpildo — žymė nusiima iškart, nelaukiant kito pateikimo */
        ['input', 'change'].forEach(function (ivykis) {
            forma.addEventListener(ivykis, function (e) {
                var el = e.target;
                if (!el || !el.hasAttribute || !el.hasAttribute('required')) { return; }
                if (uzpildytas(el) && el.checkValidity()) { nuimti(el); }
            }, true);
        });
    }

    /* ── Serverio klaidos ────────────────────────────────────────────
       Puslapis grįžo su klaidomis: pažymim tuos pačius laukus ir
       nuslenkam į pirmą — kad elgsena būtų tokia pat kaip naršyklėje. */
    function serverioKlaidos() {
        var blokas = document.getElementById('serverio-klaidos');
        if (!blokas) { return null; }
        try { return JSON.parse(blokas.textContent || '{}'); }
        catch (e) { return null; }
    }

    function taikytiServerio() {
        var duomenys = serverioKlaidos();
        if (!duomenys) { return; }
        if (duomenys.tekstai) { window.AutoLeftFormTekstai = duomenys.tekstai; }

        var pirmas = null;
        (duomenys.laukai || []).forEach(function (vardas) {
            var el = document.querySelector('[name="' + CSS.escape(vardas) + '"]');
            if (!el || !matomas(el)) { return; }
            pazymeti(el, (duomenys.zinutes || {})[vardas] || tekstai().privalomas);
            if (!pirmas) { pirmas = el; }
        });

        /* Šablonas galėjo pažymėti pats ({% if 'x' in error_fields %}) —
           tada JSON sąrašo gali ir nebūti, bet klasė jau yra. */
        if (!pirmas) {
            var jau = document.querySelector('.' + NEVALIDUS);
            if (jau) {
                pirmas = jau.matches('input, select, textarea')
                    ? jau : jau.querySelector('input, select, textarea');
            }
        }
        if (pirmas) { priePirmo(pirmas); }
    }

    /* ── Viršutinės dėžutės nuorodos ─────────────────────────────────
       <a href="#id_laukas"> — naršyklė nušoktų be animacijos ir po
       lipnia antrašte, todėl perimam. */
    function dezutesNuorodos() {
        document.addEventListener('click', function (e) {
            var a = e.target.closest && e.target.closest('.form-error-box a[href^="#"]');
            if (!a) { return; }
            var id = a.getAttribute('href').slice(1);
            var el = document.getElementById(id) ||
                     document.querySelector('[name="' + CSS.escape(id) + '"]');
            if (!el) { return; }
            e.preventDefault();
            priePirmo(el);
        });
    }

    function paleisti() {
        document.querySelectorAll('form[data-validate]').forEach(prijungti);
        dezutesNuorodos();
        taikytiServerio();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', paleisti);
    } else {
        paleisti();
    }

    window.AutoLeftForma = {
        prijungti: prijungti,
        tikrinti: tikrinti,
        pazymeti: pazymeti,
        nuimti: nuimti,
    };
})();
