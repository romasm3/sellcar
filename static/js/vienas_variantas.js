/* Telefono ir darbalaukio laukų sąrašai gyvena TOJE PAČIOJE formoje
 * (vienas paslėptas per CSS). Naršyklė siunčia ir paslėptus laukus,
 * todėl adrese atsirasdavo dublikatai: „?q=&q=&transmission=6&…".
 *
 * Todėl nematomo varianto laukus laikom išjungtus (disabled) — nuo pat
 * įkėlimo, o ne tik prieš siuntimą: dalis panelių formą siunčia per
 * form.submit(), o tada „submit" įvykis NEKYLA ir tvarkyti būtų vėlu.
 *
 * Ribą imam tą pačią kaip Tailwind lg (1024 px), o ne offsetParent:
 * multiselect'ų žymimieji langeliai guli suskleistame sąraše
 * (display:none), bet juos siųsti BŪTINA.
 */
(function () {
    'use strict';

    function tvarkyti() {
        var darbalaukis = window.matchMedia('(min-width: 1024px)').matches;
        document.querySelectorAll('[data-laukai]').forEach(function (blokas) {
            var aktyvus = blokas.dataset.laukai === (darbalaukis ? 'darbalaukis' : 'mobilus');
            blokas.querySelectorAll('input, select, textarea').forEach(function (el) {
                el.disabled = !aktyvus;
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', tvarkyti);
    } else {
        tvarkyti();
    }

    var laikmatis = null;
    window.addEventListener('resize', function () {
        clearTimeout(laikmatis);
        laikmatis = setTimeout(tvarkyti, 150);
    });

    // Paskutinė apsauga tiems atvejams, kai laukai atsiranda vėliau (AJAX)
    document.addEventListener('submit', tvarkyti, true);
})();
