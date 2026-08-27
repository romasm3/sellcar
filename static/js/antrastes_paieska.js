/**
 * ANTRAŠTĖS PAIEŠKA — trys laukai vienoje juostoje (Alpine komponentas).
 *
 * Siunčiami parametrai yra TIE PATYS, kuriuos naudoja paieškos panelė ir
 * detali paieška (apps/listings/search_params.py + filter_listings):
 *
 *   category=<slug>   kategorija
 *   city=<tekstas>    vieta (+ country_filter=<XX>, jei siūlymas turi šalį)
 *   brand=<id>        markė, kai pasirinkta iš siūlymų (kartu nustatoma
 *                     ir kategorija, nes markių id yra kategorijos viduje)
 *   q=<tekstas>       kai markė tiesiog įrašyta ranka
 *
 * Todėl rezultatų puslapyje pasirinkimai jau būna pažymėti — jokio antro
 * filtrų rinkinio.
 */
function antrastesPaieska() {
    const p = (() => {
        try { return JSON.parse(document.getElementById('apPradine').textContent); }
        catch (e) { return {}; }
    })();

    return {
        atverta: false,
        kategorija: p.kategorija || 'all',   // 'all' = visos kategorijos
        vieta: p.vieta || '',
        salis: p.salis || '',
        marke: p.marke || '',
        markeId: p.markeId || '',
        vietos: [], rodykVietas: false,
        markesSarasas: [], rodykMarkes: false,

        /** Telefono mygtuko tekstas — kad matytųsi, kas jau pasirinkta. */
        santrauka() {
            const d = [this.vieta, this.marke].filter(Boolean);
            return d.length ? d.join(' · ') : (window.AP_TEKSTAI || {}).ieskoti || 'Ieškoti';
        },

        atidaryk() { this.atverta = true; document.body.style.overflow = 'hidden'; },
        uzdaryk() { this.atverta = false; document.body.style.overflow = ''; },

        // ── Vieta (Photon per /ajax/adresai/) ──────────────────────
        ieskokVietos() {
            this.salis = '';                     // rankinis tekstas — šalies nebežinom
            const q = this.vieta.trim();
            if (q.length < 3) { this.vietos = []; return; }
            fetch('/ajax/adresai/?q=' + encodeURIComponent(q))
                .then(r => r.ok ? r.json() : { siulymai: [] })
                .then(a => { this.vietos = a.siulymai || []; this.rodykVietas = true; })
                .catch(() => { this.vietos = []; });
        },

        pasirinkVieta(v) {
            // Filtruojam pagal miestą — tai tas pats `city`, kurį naudoja
            // panelė; adresas su namo numeriu čia nieko nepridėtų.
            // Vietovei imam jos pačios vardą („Kaunas"), o adresui —
            // miestą, kuriame ji yra.
            const vietove = ['city', 'town', 'village', 'district',
                             'locality', 'hamlet'].indexOf(v.tipas) !== -1;
            this.vieta = (vietove ? v.vardas : v.miestas) || v.vardas
                         || v.miestas || v.tekstas;
            this.salis = v.salies_kodas || '';
            this.vietos = []; this.rodykVietas = false;
        },

        // ── Markė (/ajax/markes/) ──────────────────────────────────
        ieskokMarkiu() {
            this.markeId = '';                   // rašant rankomis id nebegalioja
            const q = this.marke.trim();
            if (q.length < 2) { this.markesSarasas = []; return; }
            const kat = this.kategorija === 'all' ? '' : this.kategorija;
            const adr = '/ajax/markes/?q=' + encodeURIComponent(q) +
                        (kat ? '&kategorija=' + encodeURIComponent(kat) : '');
            fetch(adr)
                .then(r => r.ok ? r.json() : { markes: [] })
                .then(a => {
                    const vardai = window.AP_KATEGORIJOS || {};
                    this.markesSarasas = (a.markes || []).slice(0, 8).map(m => ({
                        ...m, kn: (!kat && m.k) ? (vardai[m.k] || '') : '',
                    }));
                    this.rodykMarkes = true;
                })
                .catch(() => { this.markesSarasas = []; });
        },

        pasirinkMarke(m) {
            this.marke = m.n;
            this.markeId = m.v;
            // Markės id gyvena kategorijos viduje, todėl kartu pažymim ir ją
            if ((!this.kategorija || this.kategorija === 'all') && m.k) this.kategorija = m.k;
            this.markesSarasas = []; this.rodykMarkes = false;
        },

        /** Prieš siunčiant sudedam reikšmes; tuščius laukus paliekam
         *  išjungtus, kad į adresą nepatektų `?city=&brand=`. */
        paruosk() {
            const dek = (ref, reiksme) => {
                const el = this.$refs[ref];
                el.value = reiksme || '';
                el.disabled = !reiksme;
            };
            dek('pCategory', this.kategorija);
            dek('pCity', this.vieta.trim());
            dek('pCountry', this.vieta.trim() ? this.salis : '');
            dek('pBrand', this.markeId);
            dek('pQ', this.markeId ? '' : this.marke.trim());
            document.body.style.overflow = '';
        },
    };
}
