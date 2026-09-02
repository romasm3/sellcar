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
 *
 * VIENA IŠIMTIS bendrai taisyklei — suskleista markės/modelio poros
 * eilutė. Paspaudus „✕" ji dingsta iš akių, bet jos laukai lieka
 * formoje ir siųsdavo tuščias reikšmes: adrese atsirasdavo
 * „?brand=1&brand=&brand=", o iš jo šoninė juosta atsistatydavo su
 * DAUGIAU tuščių eilučių, nei buvo — atrodė, kad × neveikia. Tikrinam
 * tik šitą vieną atvejį (`[data-pair-row]`), o ne bendrą matomumą, kad
 * suskleisti multiselect'ai ir toliau keliautų.
 */
(function () {
    'use strict';

    function suskleista_pora(el) {
        var eilute = el.closest ? el.closest('[data-pair-row]') : null;
        return !!eilute && eilute.getClientRects().length === 0;
    }

    function tvarkyti() {
        var darbalaukis = window.matchMedia('(min-width: 1024px)').matches;
        document.querySelectorAll('[data-laukai]').forEach(function (blokas) {
            var aktyvus = blokas.dataset.laukai === (darbalaukis ? 'darbalaukis' : 'mobilus');
            blokas.querySelectorAll('input, select, textarea').forEach(function (el) {
                el.disabled = !aktyvus || suskleista_pora(el);
            });
        });
    }

    // Gyvas skaičius ant „Filtruoti" turi skaičiuoti TUOS PAČIUS laukus,
    // kuriuos pasiųs mygtukas, todėl sąrašų skriptai kviečia šitą prieš
    // rinkdami FormData.
    window.spTvarkykLaukus = tvarkyti;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', tvarkyti);
    } else {
        tvarkyti();
    }
    // Iki Alpine paleidimo poros eilutės dar paslėptos per x-cloak, tad
    // po jo perskaičiuojam — kitaip iš adreso atėjusi antra markė liktų
    // išjungta.
    document.addEventListener('alpine:initialized', tvarkyti);

    var laikmatis = null;
    window.addEventListener('resize', function () {
        clearTimeout(laikmatis);
        laikmatis = setTimeout(tvarkyti, 150);
    });

    // Paskutinė apsauga tiems atvejams, kai laukai atsiranda vėliau (AJAX)
    document.addEventListener('submit', tvarkyti, true);
})();
