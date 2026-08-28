/**
 * PAGRINDINĖ PAIEŠKA (viena juosta) — Alpine komponentas.
 *
 * Skirtukas lemia tikslą: „Visi" ir „Skelbimai" veda į /map/ (sąrašas su
 * žemėlapiu šalia), „Įmonės" — į /imones/.
 *
 * Siunčiami parametrai yra TIE PATYS, kuriuos skaito filter_listings ir
 * įmonių sąrašas: q, city (+country_filter), category. Antro filtrų
 * rinkinio nėra.
 *
 * Paskutinės paieškos laikomos naršyklėje — kaip ir peržiūrėti skelbimai.
 */
function herojausPaieska() {
    const T = window.HP_TEKSTAI || {};
    const RAKTAS = 'paieskos_istorija';
    const RIBA = 5;

    return {
        atviras: false,
        skirtukas: 'visi',
        ko: '', vieta: '', salis: '', kategorija: '',
        vietos: [], rodykVietas: false,
        paskutines: [],

        skirtukai: [
            { raktas: 'visi', vardas: T.visi || 'Visi' },
            { raktas: 'skelbimai', vardas: T.skelbimai || 'Skelbimai' },
            { raktas: 'imones', vardas: T.imones || 'Įmonės' },
        ],

        init() { this.paskutines = this.skaityk(); },

        veiksmas() { return this.skirtukas === 'imones' ? '/imones/' : '/map/'; },

        // ── Paskutinės paieškos ────────────────────────────────────
        skaityk() {
            try { return JSON.parse(localStorage.getItem(RAKTAS) || '[]') || []; }
            catch (e) { return []; }
        },

        irasyk(irasas) {
            const be = this.skaityk().filter(x => x.aprasas !== irasas.aprasas
                                                 || x.ko !== irasas.ko);
            try {
                localStorage.setItem(RAKTAS,
                    JSON.stringify([irasas].concat(be).slice(0, RIBA)));
            } catch (e) { /* privatus režimas */ }
        },

        isvalyk() {
            try { localStorage.removeItem(RAKTAS); } catch (e) {}
            this.paskutines = [];
        },

        pasirink(p) {
            this.ko = p.ko || '';
            this.vieta = p.vieta || '';
            this.salis = p.salis || '';
            this.kategorija = p.kategorija || '';
            this.skirtukas = p.skirtukas || 'visi';
            this.atviras = false;
        },

        // ── Vieta (Photon per /ajax/adresai/) ──────────────────────
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
            // Vietovei imam jos vardą („Kaunas"), adresui — miestą
            const vietove = ['city', 'town', 'village', 'district',
                             'locality', 'hamlet'].indexOf(v.tipas) !== -1;
            this.vieta = (vietove ? v.vardas : v.miestas) || v.vardas
                         || v.miestas || v.tekstas;
            this.salis = v.salies_kodas || '';
            this.vietos = []; this.rodykVietas = false;
        },

        /** Prieš siunčiant — reikšmės į paslėptus laukus, tuščios išjungtos. */
        paruosk() {
            const dek = (nuoroda, reiksme) => {
                const el = this.$refs[nuoroda];
                if (!el) return;
                el.value = reiksme || '';
                el.disabled = !reiksme;
            };
            const kat = this.skirtukas === 'imones' ? '' : this.kategorija;
            dek('pQ', this.ko.trim());
            dek('pCity', this.vieta.trim());
            dek('pCountry', this.vieta.trim() ? this.salis : '');
            dek('pCategory', kat);

            const vardai = window.HP_KATEGORIJOS || {};
            this.irasyk({
                ko: this.ko.trim(), vieta: this.vieta.trim(), salis: this.salis,
                kategorija: kat, skirtukas: this.skirtukas,
                aprasas: [vardai[kat] || (T.visosKategorijos || 'Visos kategorijos'),
                          this.vieta.trim() || (T.visaLietuva || 'Visa Lietuva')]
                         .join(' · '),
            });
        },
    };
}
