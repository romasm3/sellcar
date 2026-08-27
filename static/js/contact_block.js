/* ═══════════════════════════════════════════════════════════════════
 * Contact block behaviour — shared by every create/edit form.
 * Loaded by templates/listings/partials/contact_block.html.
 *
 * State is only meaningful for US addresses, so it is hidden (and its
 * asterisk dropped) for every other country. City is always visible.
 *
 * Forms must NOT define their own onCountryChange — a later inline
 * definition would override this one.
 * ═══════════════════════════════════════════════════════════════════ */
(function () {
    'use strict';

    function onCountryChange() {
        var country = document.getElementById('id_country');
        var stateWrap = document.getElementById('stateFieldWrapper');
        if (!country || !stateWrap) return;

        // Kurios šalys turi valstijas — sąrašą duoda serveris
        // (salys.VALSTIJOS per contact_block.html). Savo sąrašo čia nėra.
        var suValstijomis = window.VALSTIJU_SALYS || ['US'];
        var isUS = suValstijomis.indexOf(country.value) !== -1;
        var stateInput = stateWrap.querySelector('select[name="state"]');
        var star = document.getElementById('state-required');

        stateWrap.classList.toggle('hidden', !isUS);
        // Some forms style wrappers with inline display rather than a class.
        stateWrap.style.display = isUS ? '' : 'none';

        if (star) star.style.display = isUS ? '' : 'none';
        if (stateInput) {
            if (isUS) {
                stateInput.setAttribute('data-required', 'true');
            } else {
                stateInput.removeAttribute('data-required');
                stateWrap.removeAttribute('data-required');
            }
        }
    }

    // Forms call onCountryChange() from an inline onchange handler.
    window.onCountryChange = onCountryChange;

    function init() {
        var country = document.getElementById('id_country');
        if (!country) return;
        country.addEventListener('change', onCountryChange);
        onCountryChange();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
