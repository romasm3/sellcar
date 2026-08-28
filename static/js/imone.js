/**
 * ĮMONĖS PUSLAPIS — mažas žemėlapis šoninėje kortelėje ir „Įsiminti".
 *
 * Žemėlapis — Leaflet su OpenStreetMap plytelėmis, tas pats šaltinis
 * kaip kūrimo formos vietos bloke (ODbL nuoroda rodoma prie žemėlapio).
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
        if (t) t.textContent = yra ? mygtukas.dataset.yra || 'Įsiminta'
                                   : mygtukas.dataset.nera || 'Įsiminti įmonę';
        mygtukas.style.borderColor = yra ? 'var(--accent)' : '';
    }

    function ikelkLeaflet(kai) {
        if (window.L) return kai();
        var css = document.createElement('link');
        css.rel = 'stylesheet';
        css.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
        document.head.appendChild(css);
        var js = document.createElement('script');
        js.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
        js.onload = kai;
        js.onerror = function () { /* be žemėlapio puslapis veikia toliau */ };
        document.head.appendChild(js);
    }

    function paruosk() {
        var m = document.querySelector('[data-isiminti]');
        if (m) {
            m.dataset.nera = m.querySelector('.im-isiminti-txt').textContent;
            m.dataset.yra = 'Įsiminta';
            pazymek(m, skaityk().indexOf(m.dataset.isiminti) !== -1);
            m.addEventListener('click', function () { perjunk(m.dataset.isiminti, m); });
        }

        var el = document.getElementById('imMap');
        if (!el) return;
        ikelkLeaflet(function () {
            var lat = parseFloat(el.dataset.lat), lng = parseFloat(el.dataset.lng);
            if (isNaN(lat) || isNaN(lng)) return;
            var zem = L.map(el, { zoomControl: false, scrollWheelZoom: false,
                                  dragging: false, attributionControl: false })
                       .setView([lat, lng], 15);
            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 })
                .addTo(zem);
            L.marker([lat, lng]).addTo(zem).bindTooltip(el.dataset.vardas || '');
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', paruosk);
    } else { paruosk(); }
})();
