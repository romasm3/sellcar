/**
 * ĮMONĖS PUSLAPIS — „Įsiminti".
 *
 * Čia buvo ir mažas Leaflet žemėlapis su OSM viešomis plytelėmis
 * (#imMap). Jo elemento nė viename šablone nebėra, o OSM
 * viešų plytelių taip naudoti negalima — kodas pašalintas. Įmonių
 * žemėlapiai (/imones/ sąrašas ir žemėlapis) eina per Google Maps.
 *
 * „Įsiminti įmonę" 1 etape gyvena naršyklėje (localStorage), kaip ir
 * peržiūrėti skelbimai — paskyros sąrašas ateis su 2 etapu.
 */
(function () {
    'use strict';

    var RAKTAS = 'isimintos_imones';

    function skaityk() {
        try { return JSON.parse(localStorage.getItem(RAKTAS) || '[]') || []; }
        catch (e) { return []; }
    }

    function perjunk(id, mygtukas) {
        var sarasas = skaityk();
        var yra = sarasas.indexOf(id) !== -1;
        sarasas = yra ? sarasas.filter(function (x) { return x !== id; })
                      : sarasas.concat([id]);
        try { localStorage.setItem(RAKTAS, JSON.stringify(sarasas)); }
        catch (e) { /* privatus režimas — mygtukas tiesiog nieko neįsimena */ }
        pazymek(mygtukas, !yra);
    }

    function pazymek(mygtukas, yra) {
        var t = mygtukas.querySelector('.im-isiminti-txt');
        if (t) {                       // šoninės kortelės mygtukas su tekstu
            t.textContent = yra ? mygtukas.dataset.yra || 'Įsiminta'
                                : mygtukas.dataset.nera || 'Įsiminti įmonę';
            mygtukas.style.borderColor = yra ? 'var(--accent)' : '';
        } else {                       // širdis kortelėje sąraše
            mygtukas.textContent = yra ? '♥' : '♡';
            mygtukas.classList.toggle('is-on', yra);
        }
    }

    function paruosk() {
        // Mygtukų gali būti daug: šoninė kortelė puslapyje ir širdys sąraše
        var sarasas = skaityk();
        [].forEach.call(document.querySelectorAll('[data-isiminti]'), function (m) {
            var t = m.querySelector('.im-isiminti-txt');
            if (t) { m.dataset.nera = t.textContent; m.dataset.yra = 'Įsiminta'; }
            pazymek(m, sarasas.indexOf(m.dataset.isiminti) !== -1);
            m.addEventListener('click', function (e) {
                e.preventDefault(); e.stopPropagation();   // kortelė yra nuoroda
                perjunk(m.dataset.isiminti, m);
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', paruosk);
    } else { paruosk(); }
})();
