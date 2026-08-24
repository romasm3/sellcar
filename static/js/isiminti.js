/**
 * ĮSIMINTŲ SKELBIMŲ SKAITIKLIS — vienas šaltinis visoms antraštėms.
 *
 * Prisijungusiam skaičių atiduoda serveris (context_processors.
 * saved_listings_count, įrašytas į data-serverio-kiekis), svečiui —
 * localStorage sąrašas „isiminti". Ekrane gali būti kelios ikonos
 * (darbalaukio ir telefono antraštės, meniu) — visos atsinaujina kartu,
 * nes piešiamos iš tos pačios reikšmės.
 *
 * Naudojimas iš kortelių:
 *     window.isiminti.nustatyk(atsakymas.kiek);   // prisijungęs
 *     window.isiminti.perjunk(listingId);         // svečias (localStorage)
 */
(function () {
    'use strict';

    var RAKTAS = 'isiminti';

    function svecioSarasas() {
        try {
            var v = JSON.parse(window.localStorage.getItem(RAKTAS) || '[]');
            return Array.isArray(v) ? v : [];
        } catch (e) { return []; }
    }

    function irasykSveciui(sarasas) {
        try { window.localStorage.setItem(RAKTAS, JSON.stringify(sarasas)); }
        catch (e) { /* privatus režimas — tyliai praleidžiam */ }
    }

    // Šaltinis — vienintelis elementas su serverio reikšme (antraštės
    // ikona). Kitos ikonos (meniu, avataro sąrašas) tik atkartoja skaičių.
    function saltinis() {
        var el = document.querySelector('[data-serverio-kiekis]');
        return (el && el.getAttribute('data-serverio-kiekis') !== '') ? el : null;
    }

    function kiek() {
        var el = saltinis();
        if (el) return parseInt(el.getAttribute('data-serverio-kiekis'), 10) || 0;
        return svecioSarasas().length;
    }

    function nustatyk(n) {
        n = parseInt(n, 10);
        if (isNaN(n) || n < 0) n = 0;
        var sal = saltinis();
        if (sal) sal.setAttribute('data-serverio-kiekis', String(n));
        document.querySelectorAll('[data-isiminti-skaitiklis]').forEach(function (el) {
            el.textContent = n;
            el.style.display = n > 0 ? '' : 'none';
        });
        return n;
    }

    function perjunk(id) {
        var sarasas = svecioSarasas();
        var i = sarasas.indexOf(String(id));
        if (i >= 0) sarasas.splice(i, 1);
        else sarasas.push(String(id));
        irasykSveciui(sarasas);
        nustatyk(sarasas.length);
        return i < 0;
    }

    function perpiesti() { nustatyk(kiek()); }

    window.isiminti = {
        kiek: kiek,
        nustatyk: nustatyk,
        perjunk: perjunk,
        sarasas: svecioSarasas,
        perpiesti: perpiesti
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', perpiesti);
    } else {
        perpiesti();
    }
})();
