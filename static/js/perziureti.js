/**
 * PERŽIŪRĖTI SKELBIMAI — vienas šaltinis naršyklės pusėje.
 *
 * Ką daro:
 *   1. skelbimo puslapyje įrašo peržiūrą (svečiui — į localStorage;
 *      prisijungusiam tai jau padarė serveris);
 *   2. prisijungus perkelia svečio sąrašą į paskyrą (/perziureti/sujungti/)
 *      ir naršyklės sąrašą išvalo;
 *   3. rezultatų kortelėse pažymi jau matytus skelbimus ženkliuku
 *      „Žiūrėjote";
 *   4. /perziureti/ puslapyje: svečiui užkrauna korteles, tvarko filtrą,
 *      rūšiavimą, ✕ ir „Dalintis".
 *
 * Sąrašas laikomas kaip [{id, kada}] — naujausias priekyje, ne daugiau
 * kaip RIBA įrašų (tiek pat, kiek saugo serveris).
 */
(function () {
    'use strict';

    var RAKTAS = 'perziureti';
    var RIBA = 100;
    var T = window.PERZIURETI_TEKSTAI || {};

    // ── Naršyklės sąrašas ───────────────────────────────────────────
    function skaityk() {
        try {
            var v = JSON.parse(window.localStorage.getItem(RAKTAS) || '[]');
            return Array.isArray(v) ? v.filter(function (x) { return x && x.id; }) : [];
        } catch (e) { return []; }
    }

    function rasyk(sarasas) {
        try { window.localStorage.setItem(RAKTAS, JSON.stringify(sarasas.slice(0, RIBA))); }
        catch (e) { /* privatus režimas */ }
    }

    function zymeti(id) {
        id = parseInt(id, 10);
        if (!id) return;
        var sarasas = skaityk().filter(function (x) { return parseInt(x.id, 10) !== id; });
        sarasas.unshift({ id: id, kada: new Date().toISOString() });
        rasyk(sarasas);
    }

    function idSarasas() {
        return skaityk().map(function (x) { return parseInt(x.id, 10); });
    }

    function laikai() {
        var m = {};
        skaityk().forEach(function (x) { m[x.id] = x.kada; });
        return m;
    }

    function csrf() {
        var v = ('; ' + document.cookie).split('; csrftoken=');
        return v.length === 2 ? v.pop().split(';').shift() : '';
    }

    function postJSON(url, duom) {
        return fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf(),
                       'X-Requested-With': 'XMLHttpRequest' },
            body: JSON.stringify(duom || {})
        }).then(function (r) { return r.ok ? r.json() : null; });
    }

    // ── 1. Įrašom peržiūrą ──────────────────────────────────────────
    function irasykSiaPerziura() {
        var el = document.querySelector('[data-perziurimas-skelbimas]');
        if (!el) return;
        var id = el.getAttribute('data-perziurimas-skelbimas');
        // Prisijungusiam sąrašą tvarko serveris — dubliuoti nereikia.
        if (el.getAttribute('data-prisijunges') === '1') return;
        zymeti(id);
    }

    // ── 2. Svečio sąrašas → paskyra ─────────────────────────────────
    function sujunkSuPaskyra() {
        var kunas = document.body;
        if (!kunas || kunas.getAttribute('data-prisijunges') !== '1') return;
        var ids = idSarasas();
        if (!ids.length) return;
        postJSON('/perziureti/sujungti/', { ids: ids, laikai: laikai() })
            .then(function (a) {
                if (a && a.ok) {
                    rasyk([]);                      // perkelta — naršyklėje nebereikia
                    if (window.location.pathname.indexOf('/perziureti/') === 0) {
                        window.location.reload();
                    }
                }
            }).catch(function () {});
    }

    // ── 3. Ženkliukas „Žiūrėjote" kortelėse ─────────────────────────
    function zymekKorteles(ids) {
        if (!ids || !ids.length) return;
        var matyti = {};
        ids.forEach(function (i) { matyti[parseInt(i, 10)] = true; });

        document.querySelectorAll('[data-skelbimas]').forEach(function (kort) {
            if (kort.querySelector('.card-ziurejote')) return;
            if (!matyti[parseInt(kort.getAttribute('data-skelbimas'), 10)]) return;
            if (kort.classList.contains('pz-kort')) return;   // pačiame sąraše nereikia

            var vieta = kort.querySelector('.card-bottom-left');
            if (!vieta) {
                var nuotr = kort.querySelector('.h-img-side, .home-tab-img, .pz-nuotrauka');
                if (!nuotr) return;
                vieta = document.createElement('div');
                vieta.className = 'card-bottom-left';
                nuotr.appendChild(vieta);
            }
            var z = document.createElement('span');
            z.className = 'card-mini-badge card-ziurejote';
            z.textContent = T.ziurejote || 'Žiūrėjote';
            vieta.appendChild(z);
        });
    }

    function pazymekMatytus() {
        if (!document.querySelector('[data-skelbimas]')) return;
        if (document.body.getAttribute('data-prisijunges') === '1') {
            fetch('/perziureti/id/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(function (r) { return r.json(); })
                .then(function (a) { zymekKorteles(a.ids); })
                .catch(function () {});
        } else {
            zymekKorteles(idSarasas());
        }
    }

    // ── 4. /perziureti/ puslapis ────────────────────────────────────
    function puslapis() {
        var sarasas = document.querySelector('[data-pz-sarasas]');
        if (!sarasas) return;

        var kat = document.querySelector('[data-pz-kategorija]');
        var sort = document.querySelector('[data-pz-sort]');
        var kiekis = document.querySelector('[data-pz-kiekis]');

        function svecias() { return sarasas.getAttribute('data-svecias') === '1'; }

        function uzkraukSveciui() {
            postJSON('/perziureti/duomenys/', {
                ids: idSarasas(), laikai: laikai(),
                kategorija: kat ? kat.value : '', sort: sort ? sort.value : 'naujausi'
            }).then(function (a) {
                if (!a) return;
                sarasas.innerHTML = a.html;
                if (kiekis) kiekis.textContent = a.kiek ? '(' + a.kiek + ')' : '';
                if (kat && kat.options.length <= 1 && a.kategorijos) {
                    a.kategorijos.forEach(function (k) {
                        var o = document.createElement('option');
                        o.value = k.slug; o.textContent = k.label;
                        kat.appendChild(o);
                    });
                }
                if (window.laikoZyma) window.laikoZyma.perpiesti(sarasas);
            }).catch(function () {});
        }

        function keitimas() {
            if (svecias()) { uzkraukSveciui(); return; }
            var u = new URL(window.location.href);
            if (kat && kat.value) u.searchParams.set('kategorija', kat.value);
            else u.searchParams.delete('kategorija');
            if (sort && sort.value) u.searchParams.set('sort', sort.value);
            window.location = u.toString();
        }

        if (kat) kat.addEventListener('change', keitimas);
        if (sort) sort.addEventListener('change', keitimas);

        sarasas.addEventListener('click', function (e) {
            var salinti = e.target.closest('[data-salinti]');
            if (salinti) {
                e.preventDefault();
                var id = parseInt(salinti.getAttribute('data-salinti'), 10);
                var kort = salinti.closest('.pz-kort');
                if (svecias()) {
                    rasyk(skaityk().filter(function (x) { return parseInt(x.id, 10) !== id; }));
                    if (kort) kort.remove();
                    uzkraukSveciui();
                } else {
                    postJSON('/perziureti/' + id + '/pasalinti/', {}).then(function (a) {
                        if (kort) kort.remove();
                        if (a && kiekis) kiekis.textContent = a.kiek ? '(' + a.kiek + ')' : '';
                        if (a && !a.kiek) window.location.reload();
                    }).catch(function () {});
                }
                return;
            }

            var dalintis = e.target.closest('[data-dalintis]');
            if (dalintis) {
                e.preventDefault();
                var nuoroda = dalintis.getAttribute('data-nuoroda');
                var pav = dalintis.getAttribute('data-pavadinimas') || '';
                if (navigator.share) {
                    navigator.share({ title: pav, url: nuoroda }).catch(function () {});
                } else if (navigator.clipboard) {
                    navigator.clipboard.writeText(nuoroda).then(function () {
                        var t = dalintis.querySelector('span');
                        if (!t) return;
                        var senas = t.textContent;
                        t.textContent = T.nukopijuota || 'Nukopijuota';
                        setTimeout(function () { t.textContent = senas; }, 2000);
                    }).catch(function () {});
                }
            }
        });

        if (svecias()) uzkraukSveciui();
    }

    function startas() {
        irasykSiaPerziura();
        sujunkSuPaskyra();
        pazymekMatytus();
        puslapis();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', startas);
    } else {
        startas();
    }

    window.perziureti = { zymeti: zymeti, idSarasas: idSarasas, skaityk: skaityk };
})();
