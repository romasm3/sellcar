/* Telefono filtrai: eilutės, reikšmių ekranai, žymos ir apačios blokas.
 *
 * Reikšmės rašomos į tuos pačius formos laukus, kuriuos renderina
 * fields/_*.html (telefone jie tik paslėpti). Antra ir tolesnės to paties
 * lauko reikšmės — paslėpti įvedimai tuo pačiu vardu; variklis juos ima
 * per getlist ir filtruoja kaip „arba".
 */
window.mobileFilters = function () {
    return {
        sheet: '',
        q: '',
        picked: {},

        init() {
            /* Iš URL atkeliavusios reikšmės iškart virsta žymomis. */
            var self = this;
            var form = this.$el.closest('form');
            if (!form) { return; }
            form.querySelectorAll('[name]').forEach(function (el) {
                if (!el.value || el.type === 'hidden' && el.dataset.extra) { return; }
                if (['category', 'sidebar', 'subcategory', 'sort'].indexOf(el.name) !== -1) { return; }
                var label = el.tagName === 'SELECT' && el.selectedOptions.length
                    ? el.selectedOptions[0].textContent.trim() : el.value;
                if (label) { self.picked[el.name] = [{ v: el.value, l: label }]; }
            });
        },

        control(param) {
            var form = this.$el.closest('form');
            return form ? form.querySelector('[name="' + param + '"]:not([data-extra])') : null;
        },

        value(param) {
            var el = this.control(param);
            return el ? el.value : '';
        },

        has(param) {
            return (this.picked[param] || []).length > 0;
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

        /* Tiesioginis rašymas be žymos (paieškos laukas, žymimieji langeliai) */
        write(param, value) {
            var el = this.control(param);
            if (el) {
                if (el.type === 'checkbox') { el.checked = !!value; }
                else { el.value = value; }
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
            this.recount();
        },

        pick(param, value, label) {
            var list = this.picked[param] || [];
            if (list.length === 0) {
                this.write(param, value);
            } else {
                /* Antra reikšmė tam pačiam laukui — paslėptas įvedimas */
                var form = this.$el.closest('form');
                var extra = document.createElement('input');
                extra.type = 'hidden';
                extra.name = param;
                extra.value = value;
                extra.dataset.extra = String(list.length);
                form.appendChild(extra);
            }
            list.push({ v: value, l: label });
            this.picked[param] = list;
            this.closeSheet();
            this.recount();
        },

        /* × šalina TIK šitą filtrą: eilutė su „›" grįžta, kiti lieka. */
        clear(param, index) {
            var list = this.picked[param] || [];
            var removed = list.splice(index, 1)[0];
            this.picked[param] = list;

            var form = this.$el.closest('form');
            if (index === 0) {
                var main = this.control(param);
                if (main) {
                    if (main.type === 'checkbox') { main.checked = false; }
                    else { main.value = list.length ? list[0].v : ''; }
                    main.dispatchEvent(new Event('change', { bubbles: true }));
                }
                var first = form.querySelector('[name="' + param + '"][data-extra]');
                if (list.length && first) { first.remove(); }
            } else if (removed) {
                var extras = form.querySelectorAll('[name="' + param + '"][data-extra]');
                if (extras[index - 1]) { extras[index - 1].remove(); }
            }
            this.recount();
        },

        recount() {
            if (typeof refreshCount === 'function') { refreshCount(0); }
        },
    };
};
