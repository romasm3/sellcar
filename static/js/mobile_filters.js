/* Telefono filtrų eilutės ir reikšmių ekranai.
 *
 * Reikšmes rašo į tuos pačius formos laukus, kuriuos renderina
 * fields/_*.html — jie telefone tik paslėpti. Todėl forma siunčia
 * lygiai tą patį, ką ir darbalaukyje, o dublikatų su tais pačiais
 * vardais nėra.
 */
window.mobileFilters = function () {
    return {
        sheet: '',
        q: '',
        labels: {},

        control(param) {
            var form = this.$el.closest('form');
            return form ? form.querySelector('[name="' + param + '"]') : null;
        },

        value(param) {
            var el = this.control(param);
            return el ? el.value : '';
        },

        /* Ką rodyti eilutės dešinėje: pasirinkto varianto tekstą. */
        label(param) {
            if (this.labels[param] !== undefined) { return this.labels[param]; }
            var el = this.control(param);
            if (!el || !el.value) { return ''; }
            if (el.tagName === 'SELECT' && el.selectedOptions.length) {
                return el.selectedOptions[0].textContent.trim();
            }
            return el.value;
        },

        openSheet(param) {
            this.sheet = param;
            this.q = '';
            document.body.style.overflow = 'hidden';
        },

        closeSheet() {
            this.sheet = '';
            document.body.style.overflow = '';
        },

        match(text) {
            if (!this.q) { return true; }
            return String(text).toLowerCase().indexOf(this.q.toLowerCase()) !== -1;
        },

        pick(param, value, label) {
            var el = this.control(param);
            if (el) {
                el.value = value;
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
            this.labels[param] = label;
            if (typeof refreshCount === 'function') { refreshCount(0); }
            if (arguments.length < 4) { this.closeSheet(); }
        },
    };
};
