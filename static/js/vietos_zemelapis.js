/**
 * VIETOS ŽEMĖLAPIS kūrimo formoje (Leaflet + OpenStreetMap plytelės).
 *
 * Elgsena:
 *   • rašant adresą — siūlymai iš /ajax/adresai/ (Photon), 300 ms atidėjimas;
 *   • pasirinkus siūlymą — žemėlapis nuslenka ir pastato žymeklį;
 *   • žymeklį galima tempti (pele ar pirštu); PALEIDUS jį kviečiamas
 *     /ajax/vieta/ (Nominatim) ir adreso laukas atsinaujina;
 *   • mastelis — ratuku arba + / − mygtukais.
 *
 * Nepavykus geokodavimui viskas veikia toliau: laukas lieka paprastu
 * tekstu, žymeklį galima statyti ranka. Skelbimo kūrimas nesustoja.
 */
function vietosZemelapis(pradiniai) {
    return {
        uzklausa: '',
        siulymai: [],
        lat: pradiniai.lat,
        lon: pradiniai.lon,
        miestas: '',
        salis: '',
        tiksliaiStr: pradiniai.tiksliai ? '' : 'on',
        _zem: null,
        _zymeklis: null,

        paruosk() {
            // Leaflet įkeliamas tik ten, kur žemėlapio tikrai reikia
            ikelkLeaflet(() => this.pieskZemelapi());
        },

        pieskZemelapi() {
            const L = window.L;
            if (!L || !this.$refs.zemelapis) return;
            const centras = (this.lat && this.lon) ? [this.lat, this.lon] : [54.6872, 25.2797];
            const priartinimas = (this.lat && this.lon) ? 16 : 6;

            this._zem = L.map(this.$refs.zemelapis, { zoomControl: false, scrollWheelZoom: true })
                         .setView(centras, priartinimas);
            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19, attribution: '' // nuoroda rodoma savo elemente (.vt-nuoroda)
            }).addTo(this._zem);

            if (this.lat && this.lon) this.pastatyk(this.lat, this.lon, false);

            // Paspaudus žemėlapį — žymeklis atsiranda toje vietoje
            this._zem.on('click', (e) => this.pastatyk(e.latlng.lat, e.latlng.lng, true));
        },

        pastatyk(lat, lon, klausk) {
            const L = window.L;
            this.lat = Number(lat).toFixed(6);
            this.lon = Number(lon).toFixed(6);
            if (!this._zem) return;
            if (!this._zymeklis) {
                this._zymeklis = L.marker([lat, lon], { draggable: true }).addTo(this._zem);
                // TIK paleidus — taip laikomės Nominatim „1 užklausa/sek." taisyklės
                this._zymeklis.on('dragend', () => {
                    const p = this._zymeklis.getLatLng();
                    this.lat = p.lat.toFixed(6);
                    this.lon = p.lng.toFixed(6);
                    setTimeout(() => this.atvirkstinis(), 300);
                });
            } else {
                this._zymeklis.setLatLng([lat, lon]);
            }
            if (klausk) setTimeout(() => this.atvirkstinis(), 300);
        },

        ieskok() {
            const q = (this.uzklausa || '').trim();
            if (q.length < 3) { this.siulymai = []; return; }
            fetch('/ajax/adresai/?q=' + encodeURIComponent(q), {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(r => r.ok ? r.json() : { siulymai: [] })
            .then(a => { this.siulymai = a.siulymai || []; })
            .catch(() => { this.siulymai = []; });   // be siūlymų, bet laukas veikia
        },

        pasirink(s) {
            this.uzklausa = s.tekstas;
            this.siulymai = [];
            this.miestas = s.miestas || '';
            this.salis = s.salis || '';
            if (this._zem && s.lat && s.lon) {
                this._zem.setView([s.lat, s.lon], 16);
                this.pastatyk(s.lat, s.lon, false);
            }
            this.irasykAdresa(s.tekstas, s.miestas);
        },

        atvirkstinis() {
            if (!this.lat || !this.lon) return;
            fetch('/ajax/vieta/?lat=' + this.lat + '&lon=' + this.lon, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(r => r.ok ? r.json() : { vieta: {} })
            .then(a => {
                const v = a.vieta || {};
                if (!v.tekstas) return;            // tyliai: žymeklis lieka, adresas — kaip įvestas
                this.uzklausa = v.tekstas;
                this.miestas = v.miestas || this.miestas;
                this.salis = v.salis || this.salis;
                this.irasykAdresa(v.gatve || v.tekstas, v.miestas);
            })
            .catch(() => {});
        },

        /** Įrašo reikšmes į kontaktų bloko laukus (adresas, miestas). */
        irasykAdresa(gatve, miestas) {
            const a = document.getElementById('id_address');
            if (a && gatve) { a.value = gatve; a.dispatchEvent(new Event('change', { bubbles: true })); }
            const m = document.getElementById('id_city');
            if (m && miestas) { m.value = miestas; m.dispatchEvent(new Event('change', { bubbles: true })); }
        },

        mastelis(kryptis) {
            if (!this._zem) return;
            this._zem.setZoom(this._zem.getZoom() + kryptis);
        }
    };
}

/** Leaflet įkeliamas kartą ir tik pareikalavus. */
function ikelkLeaflet(kai) {
    if (window.L) { kai(); return; }
    if (window.__leafletKraunamas) {
        document.addEventListener('leaflet:ok', kai, { once: true });
        return;
    }
    window.__leafletKraunamas = true;
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    document.head.appendChild(css);
    const js = document.createElement('script');
    js.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    js.onload = () => { document.dispatchEvent(new Event('leaflet:ok')); kai(); };
    js.onerror = () => { /* be žemėlapio — laukas vis tiek veikia */ };
    document.head.appendChild(js);
}
