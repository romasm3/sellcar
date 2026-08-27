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
        _atidarytas: null,
        _burbulas: null,
        _apskritimai: [],
        _musuVieta: null,
        _matytiServeryje: [],
        lapasAtidarytas: false,
        lapasPilnas: false,
        lapoHtml: '',

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
            this._zem.addListener('click', () => this.uzdarykBurbula());
            document.addEventListener('keydown', e => { if (e.key === 'Escape') this.uzdarykBurbula(); });
            document.addEventListener('click', e => {
                if (e.target.closest('[data-uzdaryti]')) this.uzdarykBurbula();
            });
            this._zem.addListener('dragend', () => { this.pajudinta = true; });
            this._zem.addListener('zoom_changed', () => { this.pajudinta = true; });

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(p => {
                    this._musuVieta = { lat: p.coords.latitude, lng: p.coords.longitude };
                    if (!pradine.is_url) {
                        this._zem.setCenter(this._musuVieta);
                        this._zem.setZoom(10);
                        this.uzkrauk();
                    }
                }, () => {}, { timeout: 3000 });
            }
            // Prisijungusio peržiūrėti skelbimai — kad žymekliai būtų pilki
            if (document.body.dataset.prisijunges === '1') {
                fetch('/perziureti/id/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                    .then(r => r.ok ? r.json() : { ids: [] })
                    .then(a => { this._matytiServeryje = a.ids || []; })
                    .catch(() => {});
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

        /** SVG žymeklis su kaina. Antracito nenaudojam — jis susilieja
         *  su žemėlapio pilkuma; pavienis yra beveik juodas #111827. */
        ikona(tekstas, busena, pakeltas) {
            const fonas = busena === 'pasirinktas' ? '#E14D28'
                        : busena === 'ziuretas' ? '#FFFFFF' : '#111827';
            const raide = busena === 'ziuretas' ? '#6B7280' : '#FFFFFF';
            const rem = busena === 'ziuretas' ? '#E5E7EB' : '#FFFFFF';
            const w = Math.max(56, tekstas.length * 8.4 + 24);
            const h = 30, r = 15;
            const k = pakeltas ? 1.06 : 1;   // užvedus — 6 % didesnis
            const kilst = pakeltas ? 3 : 0;  // ir 3 px aukščiau
            const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h + 8}" viewBox="0 0 ${w} ${h + 8}">
                <g filter="none">
                  <rect x="1" y="1" rx="${r}" ry="${r}" width="${w - 2}" height="${h - 2}"
                        fill="${fonas}" stroke="${rem}" stroke-width="2"/>
                  <path d="M${w / 2 - 6} ${h - 2} L${w / 2} ${h + 6} L${w / 2 + 6} ${h - 2} Z"
                        fill="${fonas}" stroke="${rem}" stroke-width="2"/>
                  <text x="${w / 2}" y="${h / 2 + 4}" text-anchor="middle"
                        font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
                        font-size="12.5" font-weight="700" fill="${raide}">${tekstas}</text>
                </g></svg>`;
            return { url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(svg),
                     scaledSize: new google.maps.Size(w * k, (h + 8) * k),
                     anchor: new google.maps.Point(w * k / 2, (h + 8) * k + kilst) };
        },

        pieskZymeklius(sarasas) {
            if (!this._zem) return;
            if (this._sankaupos) this._sankaupos.clearMarkers();
            (this._apskritimai || []).forEach(a => a.setMap(null));
            this._apskritimai = [];
            this._zymekliai = {};
            const matyti = this.matytiId();
            const zym = [];

            (sarasas || []).forEach(z => {
                if (z.tipas === 'pardavejas') {
                    const m = new google.maps.Marker({
                        position: { lat: z.lat, lng: z.lng },
                        icon: this.ikona(z.vardas + ' · ' + z.kiek, 'ziuretas'),
                        zIndex: 30,
                    });
                    m.__pardavejas = z.pardavejas;
                    m.addListener('click', () => this.rodykAikstele(z.pardavejas));
                    zym.push(m);
                    return;
                }

                const busena = matyti[z.id] ? 'ziuretas' : 'įprastas';
                const m = new google.maps.Marker({
                    position: { lat: z.lat, lng: z.lng },
                    icon: this.ikona(z.kaina, busena),
                    zIndex: matyti[z.id] ? 5 : 10,
                });
                m.__id = z.id; m.__busena = busena; m.__kaina = z.kaina;
                m.addListener('click', () => this.zymeklioPaspaudimas(z.id));
                m.addListener('mouseover', () => this.zymeklioUzvedimas(z.id, true));
                m.addListener('mouseout', () => this.zymeklioUzvedimas(z.id, false));
                this._zymekliai[z.id] = m;
                zym.push(m);

                // Apytikslė vieta — punktyrinis ~500 m apskritimas
                if (z.apytiksliai) {
                    this._apskritimai.push(new google.maps.Circle({
                        map: this._zem, center: { lat: z.lat, lng: z.lng }, radius: 500,
                        strokeColor: '#111827', strokeOpacity: .55, strokeWeight: 1.5,
                        fillColor: '#111827', fillOpacity: .07, clickable: false,
                    }));
                }
            });

            if (window.markerClusterer && window.markerClusterer.MarkerClusterer) {
                this._sankaupos = new markerClusterer.MarkerClusterer({
                    map: this._zem, markers: zym,
                    renderer: { render: ({ count, position }) => new google.maps.Marker({
                        position, zIndex: 50,
                        icon: this.ikona(String(count), 'įprastas'),
                    }) },
                    onClusterClick: (e, sankaupa, zem) => this.sankaupaPaspausta(sankaupa, zem),
                });
            } else {
                zym.forEach(m => m.setMap(this._zem));
            }
        },

        /** Sankaupa: priartinam. Jei jau arčiausiai — rodom sąrašą. */
        sankaupaPaspausta(sankaupa, zem) {
            const arciausiai = zem.getZoom() >= (zem.maxZoom || 20) - 1;
            if (!arciausiai) {
                zem.fitBounds(sankaupa.bounds);
                return;
            }
            const id = (sankaupa.markers || []).map(m => m.__id).filter(Boolean);
            this.rodykSarasa(id);
        },

        /** Keli skelbimai toje pačioje vietoje — slenkamas sąrašas. */
        rodykSarasa(id) {
            if (!id.length) return;
            this.$refs.sarasas.querySelectorAll('.is-pazymeta').forEach(e => e.classList.remove('is-pazymeta'));
            id.forEach(x => {
                const k = this.$refs.sarasas.querySelector('[data-kort="' + x + '"]');
                if (k) k.classList.add('is-pazymeta');
            });
            const pirmas = this.$refs.sarasas.querySelector('[data-kort="' + id[0] + '"]');
            if (pirmas) pirmas.scrollIntoView({ behavior: 'smooth', block: 'center' });
        },

        /** Apatinio lapo tempimas: aukštyn — pilna kortelė, žemyn — uždaro. */
        lapoPradzia(e) { this._lapoY = e.touches[0].clientY; },
        lapoPabaiga(e) {
            if (this._lapoY == null) return;
            const dy = e.changedTouches[0].clientY - this._lapoY;
            this._lapoY = null;
            if (dy < -40) this.lapasPilnas = true;
            else if (dy > 40) { if (this.lapasPilnas) this.lapasPilnas = false; else this.uzdarykBurbula(); }
        },

        uzdarykBurbula() {
            if (this._burbulas) this._burbulas.close();
            this.lapasAtidarytas = false;
            if (this._atidarytas !== null) { this._atidarytas = null; this.perpieskBusena(); }
        },

        rodykAikstele(pardavejas) {
            fetch('/map/pardavejas/' + pardavejas + '/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.ok ? r.json() : null)
                .then(a => { if (a) this.rodykTurini(a.html, null); })
                .catch(() => {});
        },

        /** Pirmas paspaudimas — kortelė, antras — atidaro skelbimą. */
        zymeklioPaspaudimas(id) {
            if (this._atidarytas === id) { window.location = '/' + id + '/'; return; }
            this._atidarytas = id;
            this.perpieskBusena();
            fetch('/map/kortele/' + id + '/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.ok ? r.json() : null)
                .then(a => { if (a) this.rodykTurini(a.html, this._zymekliai[id], a); })
                .catch(() => {});
        },

        /** Užvedus — paryškinam kortelę sąraše (paspaudimas daro kita). */
        zymeklioUzvedimas(id, ijungta) {
            const kort = this.$refs.sarasas.querySelector('[data-kort="' + id + '"]');
            if (kort) kort.classList.toggle('is-pazymeta', ijungta);
            const m = this._zymekliai[id];
            if (!m) return;
            m.setIcon(this.ikona(m.__kaina, this._atidarytas === id ? 'pasirinktas' : m.__busena,
                                 ijungta));
            m.setZIndex(ijungta ? 60 : (m.__busena === 'ziuretas' ? 5 : 10));
        },

        perpieskBusena() {
            Object.keys(this._zymekliai).forEach(id => {
                const m = this._zymekliai[id];
                const b = (String(this._atidarytas) === String(id)) ? 'pasirinktas' : m.__busena;
                m.setIcon(this.ikona(m.__kaina, b));
                m.setZIndex(b === 'pasirinktas' ? 70 : (m.__busena === 'ziuretas' ? 5 : 10));
            });
        },

        /** Darbalaukyje — burbulas virš žymeklio, telefone — apatinis lapas. */
        rodykTurini(html, zymeklis, duom) {
            if (window.innerWidth < 1024) {
                this.lapoHtml = html; this.lapasAtidarytas = true; this.lapasPilnas = false;
                this.$nextTick(() => this.paruoskAtstuma(duom));
                return;
            }
            if (!this._burbulas) {
                this._burbulas = new google.maps.InfoWindow({ maxWidth: 268 });
                this._burbulas.addListener('closeclick', () => { this._atidarytas = null; this.perpieskBusena(); });
            }
            this._burbulas.setContent(html);
            // Sankaupoje esantis žymeklis nėra žemėlapyje — tada rišam prie taško
            if (zymeklis && zymeklis.getMap()) {
                this._burbulas.open({ map: this._zem, anchor: zymeklis });
            } else if (duom && duom.lat != null) {
                this._burbulas.setPosition({ lat: duom.lat, lng: duom.lng });
                this._burbulas.open({ map: this._zem });
            }
            setTimeout(() => this.paruoskAtstuma(duom), 60);
        },

        /** Atstumas ir laikas — tik jei žinom vartotojo vietą. */
        paruoskAtstuma(duom) {
            const el = document.querySelector('.zb-vieta');
            if (!el) return;
            const nav = document.querySelector('[data-nav]');
            if (nav && duom) {
                nav.href = 'https://www.google.com/maps/dir/?api=1&destination=' + duom.lat + ',' + duom.lng;
            }
            if (!this._musuVieta || !duom) return;
            const R = 6371, dLat = (duom.lat - this._musuVieta.lat) * Math.PI / 180,
                  dLng = (duom.lng - this._musuVieta.lng) * Math.PI / 180;
            const a = Math.sin(dLat / 2) ** 2 + Math.cos(this._musuVieta.lat * Math.PI / 180) *
                      Math.cos(duom.lat * Math.PI / 180) * Math.sin(dLng / 2) ** 2;
            const km = Math.round(2 * R * Math.asin(Math.sqrt(a)));
            const min = Math.max(1, Math.round(km / 50 * 60));
            const laukas = el.querySelector('.zb-atstumas');
            if (laukas) laukas.textContent = km + ' km · ~' + min + ' min · ';
        },

        /** Kuriuos jau žiūrėjom — tas pats šaltinis kaip „Peržiūrėti skelbimai". */
        matytiId() {
            const o = {};
            try {
                (JSON.parse(localStorage.getItem('perziureti') || '[]') || [])
                    .forEach(x => { o[parseInt(x.id, 10)] = true; });
            } catch (e) {}
            (this._matytiServeryje || []).forEach(x => { o[x] = true; });
            return o;
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
