/**
 * PAGRINDINĖ PAIEŠKA — Alpine komponentas.
 *
 * Du laukai (ko ieškote · vieta) ir mygtukas. Sąraše — filtro žymos ir
 * sugrupuoti rezultatai iš /ajax/paieska/. Užklausa siunčiama po 250 ms
 * pauzės, ne kas raidę; sena užklausa nutraukiama (AbortController).
 *
 * Nuorodos veda ten, kur parametrus supranta atrankos variklis:
 *   markė / modelis -> rezultatai su brand/model
 *   skelbimas       -> /<pk>/
 *   įmonė           -> /imone/<slug>/
 *   vieta           -> /map/?city=…
 *   „Ieškoti"       -> /map/ su q, city (+country_filter)
 *
 * Klaviatūra: ↑↓ vaikšto po eilutėmis, Enter atidaro pažymėtą (o jei
 * niekas nepažymėta — paprasčiausiai siunčia formą), Esc uždaro.
 */
function herojausPaieska() {
    const T = window.HP_TEKSTAI || {};
    const RAKTAS = 'paieskos_istorija';
    const RIBA = 4;

    return {
        atviras: false,
        sritis: 'visi',
        ko: '', vieta: '', salis: '',
        grupes: [], paskutines: [],
        vietos: [], rodykVietas: false,
        pazymeta: -1,
        arGalimaVieta: !!(navigator && navigator.geolocation),
        _ctrl: null,

        sritys: [
            { raktas: 'visi', vardas: T.visi || 'Visi' },
            { raktas: 'markes', vardas: T.markes || 'Markės' },
            { raktas: 'skelbimai', vardas: T.skelbimai || 'Skelbimai' },
            { raktas: 'imones', vardas: T.imones || 'Įmonės' },
        ],

        // ── Atidarymas ir uždarymas ────────────────────────────────
        atidaryk() {
            this.atviras = true;
            document.body.classList.toggle('hp-uzdengta', window.innerWidth <= 900);
            this.ieskok();
        },

        uzdaryk() {
            this.atviras = false;
            this.pazymeta = -1;
            document.body.classList.remove('hp-uzdengta');
        },

        // ── Siūlymai ───────────────────────────────────────────────
        ieskok() {
            if (this._ctrl) this._ctrl.abort();
            this._ctrl = ('AbortController' in window) ? new AbortController() : null;
            const adr = '/ajax/paieska/?q=' + encodeURIComponent(this.ko.trim()) +
                        '&sritis=' + encodeURIComponent(this.sritis);
            fetch(adr, { headers: { 'X-Requested-With': 'XMLHttpRequest' },
                         signal: this._ctrl ? this._ctrl.signal : undefined })
                .then(r => r.ok ? r.json() : null)
                .then(a => {
                    if (!a) return;
                    this.grupes = a.grupes || [];
                    // Paskutinės paieškos: serverio (sesija/paskyra) + naršyklės
                    this.paskutines = this.ko.trim()
                        ? [] : this.sujunk(a.paskutines || [], this.skaityk());
                    this.pazymeta = -1;
                })
                .catch(e => { if (!e || e.name !== 'AbortError') this.grupes = []; });
        },

        sujunk(serverio, narsykles) {
            const matyti = {}, isvestis = [];
            serverio.concat(narsykles).forEach(p => {
                if (!p.vardas || matyti[p.vardas]) return;
                matyti[p.vardas] = true;
                isvestis.push(p);
            });
            return isvestis.slice(0, RIBA);
        },

        ikona(tipas) {
            return { marke: 'fa-car', modelis: 'fa-car', skelbimas: 'fa-image',
                     imone: 'fa-building', vieta: 'fa-location-dot' }[tipas] || 'fa-magnifying-glass';
        },

        zenklas(kiek) {
            if (!kiek) return '';
            const f = T.skelbimu || ['skelbimas', 'skelbimai', 'skelbimų'];
            const d = kiek % 10, dd = kiek % 100;
            const v = (d === 0 || (dd >= 11 && dd <= 19)) ? f[2] : (d === 1 ? f[0] : f[1]);
            return kiek + ' ' + v;
        },

        // ── Klaviatūra ─────────────────────────────────────────────
        /** Bendras eilučių sąrašas — kad ↑↓ eitų per visas grupes iš eilės. */
        eilutes() {
            const visos = this.paskutines.map((p, i) => ({ raktas: this.indeksas('p', i), url: p.url }));
            this.grupes.forEach((g, gi) => g.eilutes.forEach((e, ei) =>
                visos.push({ raktas: this.indeksas(gi, ei), url: e.url })));
            return visos;
        },

        indeksas(grupe, eilute) { return grupe + ':' + eilute; },

        zemyn() {
            const v = this.eilutes(); if (!v.length) return;
            const dabar = v.findIndex(x => x.raktas === this.pazymeta);
            this.pazymeta = v[(dabar + 1) % v.length].raktas;
        },

        aukstyn() {
            const v = this.eilutes(); if (!v.length) return;
            const dabar = v.findIndex(x => x.raktas === this.pazymeta);
            this.pazymeta = v[(dabar - 1 + v.length) % v.length].raktas;
        },

        jeiPazymeta(e) {
            const v = this.eilutes().find(x => x.raktas === this.pazymeta);
            if (!v) return;                 // niekas nepažymėta — forma siunčiasi pati
            e.preventDefault();
            window.location = v.url;
        },

        // ── Paskutinės paieškos naršyklėje ─────────────────────────
        skaityk() {
            try { return JSON.parse(localStorage.getItem(RAKTAS) || '[]') || []; }
            catch (e) { return []; }
        },

        irasyk(irasas) {
            const be = this.skaityk().filter(x => x.vardas !== irasas.vardas);
            try {
                localStorage.setItem(RAKTAS, JSON.stringify([irasas].concat(be).slice(0, RIBA)));
            } catch (e) { /* privatus režimas */ }
        },

        isvalyk() {
            try { localStorage.removeItem(RAKTAS); } catch (e) {}
            this.paskutines = [];
        },

        // ── Vieta ──────────────────────────────────────────────────
        ieskokVietos() {
            this.salis = '';
            const q = this.vieta.trim();
            if (q.length < 3) { this.vietos = []; return; }
            fetch('/ajax/adresai/?q=' + encodeURIComponent(q))
                .then(r => r.ok ? r.json() : { siulymai: [] })
                .then(a => { this.vietos = a.siulymai || []; this.rodykVietas = true; })
                .catch(() => { this.vietos = []; });
        },

        pasirinkVieta(v) {
            const vietove = ['city', 'town', 'village', 'district',
                             'locality', 'hamlet'].indexOf(v.tipas) !== -1;
            this.vieta = (vietove ? v.vardas : v.miestas) || v.vardas
                         || v.miestas || v.tekstas;
            this.salis = v.salies_kodas || '';
            this.vietos = []; this.rodykVietas = false;
        },

        /** „Dabartinė vieta" — koordinatės paverčiamos miestu (Nominatim). */
        dabartineVieta() {
            if (!navigator.geolocation) return;
            navigator.geolocation.getCurrentPosition(p => {
                fetch('/ajax/vieta/?lat=' + p.coords.latitude + '&lon=' + p.coords.longitude)
                    .then(r => r.ok ? r.json() : { vieta: {} })
                    .then(a => {
                        const v = (a.vieta || {});
                        this.vieta = v.miestas || v.tekstas || '';
                        this.salis = v.salies_kodas || '';
                        this.rodykVietas = false;
                    })
                    .catch(() => { this.rodykVietas = false; });
            }, () => { this.rodykVietas = false; }, { timeout: 5000 });
        },

        /** Prieš siunčiant — reikšmės į paslėptus laukus, tuščios išjungtos. */
        paruosk() {
            const dek = (nuoroda, reiksme) => {
                const el = this.$refs[nuoroda];
                if (!el) return;
                el.value = reiksme || '';
                el.disabled = !reiksme;
            };
            dek('pQ', this.ko.trim());
            dek('pCity', this.vieta.trim());
            dek('pCountry', this.vieta.trim() ? this.salis : '');
            const vardas = [this.ko.trim(), this.vieta.trim() || (T.visaLietuva || 'Visa Lietuva')]
                .filter(Boolean).join(' · ');
            if (vardas) {
                this.irasyk({ vardas: vardas, url: '/map/?' + new URLSearchParams({
                    q: this.ko.trim(), city: this.vieta.trim() }).toString() });
            }
            document.body.classList.remove('hp-uzdengta');
        },
    };
}
