/**
 * ŽEMĖLAPIO PAIEŠKA — sąrašas ir žemėlapis viename ekrane.
 *
 * Elgsena:
 *   • sąrašas persirenka pagal MATOMĄ žemėlapio plotą (/map/duomenys/);
 *   • pastūmus žemėlapį atsiranda „Ieškoti šioje srityje" — automatiškai
 *     neperkraunam, kad ekranas nešokinėtų po kiekvieno judesio;
 *   • ratukas priartina iškart (gestureHandling: 'greedy'), be Ctrl;
 *   • persidengiantys žymekliai jungiami į sankaupas su skaičiais;
 *   • užvedus ant kortelės paryškėja žymeklis; paspaudus žymeklį sąrašas
 *     nuslenka prie kortelės, antras paspaudimas atidaro skelbimą;
 *   • vietos paieška — Photon per /ajax/adresai/ (tas pats galas kaip
 *     kūrimo formoje); šaliai mastelis mažesnis;
 *   • padėtis rašoma į URL (lat/lng/z), kad nuorodą būtų galima dalintis.
 */
/** 1 skelbimas · 2–9 skelbimai · 0, 10–20 skelbimų. */
function zpSkelbimu(n) {
    const T = (window.ZP_TEKSTAI || {}).skelbimu || ['skelbimas', 'skelbimai', 'skelbimų'];
    n = Math.abs(parseInt(n, 10) || 0);
    const d = n % 10, dd = n % 100;
    if (d === 1 && dd !== 11) return T[0];
    if (d >= 2 && d <= 9 && (dd < 10 || dd > 20)) return T[1];
    return T[2];
}

function zemelapioPaieska() {
    // Pradinė padėtis ateina per json_script — taip išvengiam HTML kabučių
    // vertimo (dėl jo anksčiau lūždavo visas skriptas).
    let pradine = { lat: 55.17, lng: 23.88, z: 7, is_url: false };
    try { pradine = JSON.parse(document.getElementById('zpPradine').textContent); } catch (e) {}

    return {
        // ── būsena ──
        kiek: 0,
        langoKiek: 0,
        pajudinta: false,
        zemelapisMatomas: true,
        mobZemelapis: false,
        filtraiAtidaryti: false,
        vietosQ: '',
        vietos: [],
        markesQ: '',
        f: {},            // juostos filtrai (taikomi iškart)
        l: {},            // lango filtrai (taikomi paspaudus „Rodyti")
        _zem: null,
        _sankaupos: null,
        _zymekliai: {},
        _pasirinktas: null,

        paruosk() {
            this.f = this.isURL();
            this.l = Object.assign({}, this.f);
            this.$watch('mobZemelapis', v => {
                const d = document.querySelector('.zp-desine');
                if (d) d.classList.toggle('mob-matomas', v);
                if (v && this._zem) setTimeout(() => google.maps.event.trigger(this._zem, 'resize'), 200);
            });
            this.laukZemelapio();
        },

        /** Filtrai iš adreso — tie patys raktai kaip visose paieškose. */
        isURL() {
            const p = new URLSearchParams(location.search), o = {};
            ['make', 'model', 'category', 'price_min', 'price_max', 'year_min', 'year_max',
             'mileage_min', 'mileage_max', 'fuel_type', 'transmission', 'sort',
             'vin', 'feat_warranty', 'tik_lietuvoje', 'su_nuotraukomis'].forEach(k => {
                const v = p.get(k); if (v) o[k] = v;
            });
            return o;
        },

        laukZemelapio() {
            if (!window.google || !window.google.maps) {
                setTimeout(() => this.laukZemelapio(), 150);
                return;
            }
            this.pieskZemelapi();
        },

        pieskZemelapi() {
            const el = this.$refs.zemelapis;
            this._zem = new google.maps.Map(el, {
                center: { lat: pradine.lat, lng: pradine.lng },
                zoom: pradine.z,
                // Ratukas priartina iškart, kai pelė virš žemėlapio —
                // be Ctrl ir be jokio užrašo. Nustatoma KURIANT žemėlapį:
                // per setOptions vėliau Google užrašo nebenuima.
                gestureHandling: 'greedy',
                mapTypeControl: false,
                streetViewControl: false,
                fullscreenControl: false,
            });

            this._zem.addListener('idle', () => { this.irasykURL(); });
            this._zem.addListener('dragend', () => { this.pajudinta = true; });
            this._zem.addListener('zoom_changed', () => { this.pajudinta = true; });

            if (!pradine.is_url && navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    p => { this._zem.setCenter({ lat: p.coords.latitude, lng: p.coords.longitude });
                           this._zem.setZoom(10); this.uzkrauk(); },
                    () => {}, { timeout: 3000 });
            }
            this.uzkrauk();
        },

        /** Duomenys pagal matomą plotą. */
        uzkrauk() {
            const p = new URLSearchParams(this.f);
            const b = this._zem && this._zem.getBounds();
            if (b) {
                p.set('s', b.getSouthWest().lat()); p.set('n', b.getNorthEast().lat());
                p.set('v', b.getSouthWest().lng()); p.set('r', b.getNorthEast().lng());
            }
            fetch('/map/duomenys/?' + p.toString(), { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.ok ? r.json() : null)
                .then(a => {
                    if (!a) return;
                    this.kiek = a.kiek;
                    this.$refs.sarasas.innerHTML = a.html;
                    if (window.laikoZyma) window.laikoZyma.perpiesti(this.$refs.sarasas);
                    this.pieskZymeklius(a.zymekliai);
                    this.pajudinta = false;
                })
                .catch(() => {});     // tinklo klaida — lieka tai, kas jau matoma
        },

        ieskokSrityje() { this.uzkrauk(); },

        pieskZymeklius(sarasas) {
            if (!this._zem) return;
            if (this._sankaupos) this._sankaupos.clearMarkers();
            this._zymekliai = {};
            const zym = (sarasas || []).map(z => {
                const m = new google.maps.Marker({
                    position: { lat: z.lat, lng: z.lng },
                    title: '#' + z.id,
                });
                m.addListener('click', () => this.zymeklioPaspaudimas(z.id));
                this._zymekliai[z.id] = m;
                return m;
            });
            if (window.markerClusterer && window.markerClusterer.MarkerClusterer) {
                this._sankaupos = new markerClusterer.MarkerClusterer({ map: this._zem, markers: zym });
            } else {
                zym.forEach(m => m.setMap(this._zem));   // be bibliotekos — tiesiog taškai
            }
        },

        /** Pirmas paspaudimas — nuslenka prie kortelės, antras — atidaro. */
        zymeklioPaspaudimas(id) {
            if (this._pasirinktas === id) { window.location = '/' + id + '/'; return; }
            this._pasirinktas = id;
            const kort = this.$refs.sarasas.querySelector('[data-kort="' + id + '"]');
            if (kort) {
                kort.scrollIntoView({ behavior: 'smooth', block: 'center' });
                this.$refs.sarasas.querySelectorAll('.is-pazymeta').forEach(e => e.classList.remove('is-pazymeta'));
                kort.classList.add('is-pazymeta');
            }
        },

        pazymek(e) {
            const kort = e.target.closest('[data-kort]');
            if (!kort) return;
            const m = this._zymekliai[kort.dataset.kort];
            if (m) m.setAnimation(google.maps.Animation.BOUNCE);
        },
        nupazymek() {
            Object.values(this._zymekliai).forEach(m => m.setAnimation(null));
        },

        // ── Vietos paieška (Photon) ──
        ieskokVietos() {
            const q = (this.vietosQ || '').trim();
            if (q.length < 3) { this.vietos = []; return; }
            fetch('/ajax/adresai/?q=' + encodeURIComponent(q), { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.ok ? r.json() : { siulymai: [] })
                .then(a => { this.vietos = a.siulymai || []; })
                .catch(() => { this.vietos = []; });
        },
        pasirinkVieta(v) {
            this.vietos = []; this.vietosQ = v.tekstas;
            if (!this._zem || !v.lat) return;
            // Šalis — mažesnis mastelis, adresas — didesnis
            const salis = !v.miestas || v.tekstas.split(',').length <= 1;
            this._zem.setCenter({ lat: v.lat, lng: v.lon });
            this._zem.setZoom(salis ? 6 : 12);
            setTimeout(() => this.uzkrauk(), 300);
        },

        // ── Filtrai ──
        atidarykFiltrus() { this.l = Object.assign({}, this.f); this.filtraiAtidaryti = true; this.perskaiciuok(); },
        uzdarykFiltrus() { this.filtraiAtidaryti = false; },
        pritaikykFiltrus() { this.f = Object.assign({}, this.valyk(this.l)); this.filtraiAtidaryti = false; this.taikyk(); },
        valyk(o) { const r = {}; Object.keys(o).forEach(k => { if (o[k]) r[k] = o[k]; }); return r; },

        perskaiciuok() {
            const p = new URLSearchParams(this.valyk(this.l));
            const b = this._zem && this._zem.getBounds();
            if (b) {   // skaičius toks pat, kokį pamatys pritaikęs
                p.set('s', b.getSouthWest().lat()); p.set('n', b.getNorthEast().lat());
                p.set('v', b.getSouthWest().lng()); p.set('r', b.getNorthEast().lng());
            }
            p.set('tik_skaicius', '1');
            fetch('/map/duomenys/?' + p.toString(), { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.ok ? r.json() : null)
                .then(a => { if (a) this.langoKiek = a.kiek; })
                .catch(() => {});
        },

        taikyk() { this.f = this.valyk(this.f); this.irasykURL(); this.uzkrauk(); },
        isvalyk(irJuosta) {
            this.l = {};
            if (irJuosta) { this.f = {}; this.taikyk(); }
            this.perskaiciuok();
        },
        nuimk(raktas) { delete this.f[raktas]; delete this.l[raktas]; this.taikyk(); },

        aktyvuKiek() { return Object.keys(this.valyk(this.f)).length; },
        /** Filtro reikšmė žmogui: kategorijos ir kuro vardai, ne raktai. */
        vardas(raktas, reiksme) {
            const V = window.ZP_VARDAI || {};
            if (raktas === 'category') return (V.kategorijos || {})[reiksme] || reiksme;
            if (raktas === 'fuel_type') return (V.kuras || {})[reiksme] || reiksme;
            if (raktas === 'sort') return (V.rusiavimas || {})[reiksme] || reiksme;
            return reiksme;
        },

        aktyvuSarasas() {
            const T = window.ZP_TEKSTAI || {};
            const vardai = { make: T.marke, price_min: T.kaina + ' ' + T.nuo, price_max: T.kaina + ' ' + T.iki,
                             year_min: T.metai + ' ' + T.nuo, year_max: T.metai + ' ' + T.iki,
                             mileage_min: T.rida + ' ' + T.nuo, mileage_max: T.rida + ' ' + T.iki,
                             fuel_type: T.kuras };
            return Object.keys(this.valyk(this.f)).map(k => ({
                raktas: k,
                tekstas: (vardai[k] ? vardai[k] + ': ' : '') + this.vardas(k, this.f[k])
            }));
        },

        /** Padėtis ir filtrai adrese — nuorodą galima dalintis. */
        irasykURL() {
            if (!this._zem) return;
            const c = this._zem.getCenter(); if (!c) return;
            const p = new URLSearchParams(this.valyk(this.f));
            p.set('lat', c.lat().toFixed(5)); p.set('lng', c.lng().toFixed(5));
            p.set('z', this._zem.getZoom());
            history.replaceState(null, '', location.pathname + '?' + p.toString());
        },
    };
}
