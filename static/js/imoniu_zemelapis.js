/**
 * ĮMONIŲ ŽEMĖLAPIS — /imones/map/
 *
 * Elgsena tokia pat kaip skelbimų žemėlapyje, tik duomenys savi:
 *   • sąrašas ir skaičius persikrauna, kai žemėlapis nurimsta (idle),
 *     400 ms atidėjimas, sena užklausa nutraukiama (AbortController);
 *   • postūmiai, keičiantys plotą mažiau nei 2 %, praleidžiami;
 *   • paspaudus žymeklį — įmonės kortelė, antrą kartą — jos puslapis;
 *   • krovimo metu sąrašas pritemdomas, ne išvalomas.
 *
 * Žymekliai piešiami bendru imoniuZymekliai() — tuo pačiu, kurį naudoja
 * skelbimų žemėlapis.
 */
const IMZ = { zem: null, zymekliai: [], burbulas: null, atidarytas: null };
const IMZ_MAKS_MASTELIS = 15;

function imoniuZemelapis() {
    let pradine = { lat: 55.17, lng: 23.88, z: 7, is_url: false };
    try { pradine = JSON.parse(document.getElementById('imzPradine').textContent); }
    catch (e) {}

    return {
        kiek: 0,
        kraunama: false,
        pajudinta: false,
        zemelapisMatomas: true,
        _pakrauta: false,
        _ribos: null,
        _ctrl: null,
        _atidarytoUrl: '',

        paruosk() {
            this.laukZemelapio();
            // Atsarginis krovimas: jei „idle" neįvyktų (paslėptas žemėlapis),
            // sąrašas vis tiek atsiranda.
            setTimeout(() => { if (!this._pakrauta) this.uzkrauk(); }, 1500);
            document.addEventListener('click', e => {
                if (e.target.closest('[data-uzdaryti]')) this.uzdarykBurbula();
                if (e.target.closest('[data-atitolinti]')) this.atitolink();
            });
            document.addEventListener('keydown', e => {
                if (e.key === 'Escape') this.uzdarykBurbula();
            });
        },

        laukZemelapio() {
            if (!window.google || !google.maps) {
                setTimeout(() => this.laukZemelapio(), 200);
                return;
            }
            IMZ.zem = new google.maps.Map(this.$refs.zemelapis, {
                center: { lat: pradine.lat, lng: pradine.lng },
                zoom: pradine.z,
                gestureHandling: 'greedy',   // be Ctrl — kaip ir skelbimų žemėlapy
                mapTypeControl: false,
                streetViewControl: false,
                fullscreenControl: false,
            });
            IMZ.zem.addListener('idle', () => {
                this.irasykURL();
                if (!this._pakrauta) { this.uzkrauk(); return; }
                if (!this.ribosPasikeite()) return;
                clearTimeout(this._atidejimas);
                this._atidejimas = setTimeout(() => this.uzkrauk(), 400);
            });
            IMZ.zem.addListener('click', () => this.uzdarykBurbula());
            IMZ.zem.addListener('dragend', () => { this.pajudinta = true; });
        },

        zemelapisRodomas() {
            const el = this.$refs.zemelapis;
            return !!(el && el.offsetWidth > 0 && el.offsetHeight > 0);
        },

        ribosPasikeite() {
            const b = this.zemelapisRodomas() && IMZ.zem && IMZ.zem.getBounds();
            if (!b) return false;
            const d = { s: b.getSouthWest().lat(), n: b.getNorthEast().lat(),
                        v: b.getSouthWest().lng(), r: b.getNorthEast().lng() };
            const sen = this._ribos;
            if (!sen) return true;
            const a = Math.abs(sen.n - sen.s) || 1, pl = Math.abs(sen.r - sen.v) || 1;
            return Math.max(Math.abs(d.s - sen.s) / a, Math.abs(d.n - sen.n) / a,
                            Math.abs(d.v - sen.v) / pl, Math.abs(d.r - sen.r) / pl) > 0.02;
        },

        uzkrauk() {
            this._pakrauta = true;
            this.kraunama = true;
            if (this._ctrl) this._ctrl.abort();
            this._ctrl = ('AbortController' in window) ? new AbortController() : null;

            // Filtrai imami iš adreso — jie ateina iš paieškos juostos
            const p = new URLSearchParams(location.search);
            ['lat', 'lng', 'z'].forEach(k => p.delete(k));
            const b = this.zemelapisRodomas() && IMZ.zem && IMZ.zem.getBounds();
            if (b) {
                p.set('s', b.getSouthWest().lat()); p.set('n', b.getNorthEast().lat());
                p.set('v', b.getSouthWest().lng()); p.set('r', b.getNorthEast().lng());
                this._ribos = { s: b.getSouthWest().lat(), n: b.getNorthEast().lat(),
                                v: b.getSouthWest().lng(), r: b.getNorthEast().lng() };
            }
            fetch('/imones/duomenys/?' + p.toString(), {
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                signal: this._ctrl ? this._ctrl.signal : undefined,
            })
                .then(r => r.ok ? r.json() : null)
                .then(a => {
                    this.kraunama = false;
                    if (!a) return;
                    this.kiek = a.kiek;
                    this.$refs.sarasas.innerHTML = a.html;
                    IMZ.zymekliai = window.imoniuZymekliai(
                        IMZ.zem, a.imones || [], IMZ.zymekliai);
                    this.rikPaspaudimus(a.imones || []);
                    this.pajudinta = false;
                })
                .catch(e => {
                    if (e && e.name === 'AbortError') return;
                    this.kraunama = false;
                });
        },

        /** Žymeklius piešia OverlayView, todėl jų dar gali nebūti, kai
         *  ateina duomenys — paspaudimą gaudom deleguotai. */
        rikPaspaudimus(sarasas) {
            this._pagalUrl = {};
            sarasas.forEach(i => { this._pagalUrl[i.url] = i; });
            if (this._klausom) return;
            this._klausom = true;
            // Gaudymo fazė (true): Google žemėlapio „click" klausytojas
            // kabo ant žemėlapio konteinerio ir suveiktų anksčiau —
            // uždarytų ką tik atidarytą burbulą, o antras paspaudimas
            // vėl atrodytų kaip pirmas.
            document.addEventListener('click', e => {
                const el = e.target.closest('.zp-imone');
                if (!el) return;
                const i = (this._pagalUrl || {})[el.getAttribute('href')];
                if (!i) return;                     // nežinom — leidžiam nuorodai
                e.preventDefault();
                // Be šito paspaudimas nukeliauja iki žemėlapio ir tas pats
                // mygtukas iškart uždaro ką tik atidarytą burbulą.
                e.stopPropagation();
                this.zymeklioPaspaudimas(i);
            }, true);
        },

        /** Pirmas paspaudimas — kortelė, antras — įmonės puslapis. */
        zymeklioPaspaudimas(i) {
            if (IMZ.atidarytas === i.id) { window.location = i.url; return; }
            IMZ.atidarytas = i.id;
            fetch('/imones/kortele/' + i.id + '/',
                  { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.ok ? r.json() : null)
                .then(a => {
                    if (!a) return;
                    if (!IMZ.burbulas) {
                        IMZ.burbulas = new google.maps.InfoWindow({ maxWidth: 268 });
                        IMZ.burbulas.addListener('closeclick',
                            () => { IMZ.atidarytas = null; });
                    }
                    IMZ.burbulas.setContent(a.html);
                    IMZ.burbulas.setPosition({ lat: a.lat, lng: a.lng });
                    IMZ.burbulas.open({ map: IMZ.zem });
                })
                .catch(() => {});
        },

        uzdarykBurbula() {
            if (IMZ.burbulas) IMZ.burbulas.close();
            IMZ.atidarytas = null;
        },

        atitolink() {
            if (!IMZ.zem) return;
            IMZ.zem.setZoom(Math.max(1, IMZ.zem.getZoom() - 2));
            setTimeout(() => this.uzkrauk(), 300);
        },

        /** Filtrai ir padėtis adrese — nuorodą galima dalintis. */
        irasykURL() {
            if (!IMZ.zem) return;
            const c = IMZ.zem.getCenter();
            if (!c) return;
            const p = new URLSearchParams(location.search);
            p.set('lat', c.lat().toFixed(5));
            p.set('lng', c.lng().toFixed(5));
            p.set('z', Math.min(IMZ.zem.getZoom(), IMZ_MAKS_MASTELIS));
            history.replaceState(null, '', location.pathname + '?' + p.toString());
        },

        zenklas(kiek) {
            const f = (window.IMZ_TEKSTAI || {}).imoniu || ['įmonė', 'įmonės', 'įmonių'];
            const d = kiek % 10, dd = kiek % 100;
            return (d === 0 || (dd >= 11 && dd <= 19)) ? f[2] : (d === 1 ? f[0] : f[1]);
        },
    };
}
