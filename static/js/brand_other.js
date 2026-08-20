/* „Kita" markė — bendras elgesys visoms kategorijoms.
 *
 * Kai markės sąraše nėra, žmogus renkasi „Kita" ir įrašo pavadinimą
 * ranka. Įvestas tekstas keliauja į admin'ą kaip pasiūlymas
 * (BrandSuggestion), todėl sąrašas pildosi pagal realų poreikį.
 *
 * Prisikabina prie bet kurio <select>, kurio vardas baigiasi
 * „_brand_text" ir kuris turi porą <input name="<vardas>_other">.
 */
(function () {
    function bind(select) {
        var input = document.querySelector(
            '[name="' + select.name + '_other"]');
        if (!input) { return; }

        function toggle() {
            var other = select.value === '__other__';
            input.style.display = other ? '' : 'none';
            if (other) {
                input.setAttribute('required', 'required');
                input.focus();
            } else {
                input.removeAttribute('required');
            }
        }

        select.addEventListener('change', toggle);
        toggle();
    }

    document.addEventListener('DOMContentLoaded', function () {
        var selects = document.querySelectorAll('select[name$="_brand_text"]');
        Array.prototype.forEach.call(selects, bind);
    });
})();
