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

// ═══════════════════════════════════════════════════════════════════
// Google objektai laikomi ČIA, ne Alpine būsenoje.
//
// Alpine (kaip ir Vue) kiekvieną komponento lauką apvynioja Proxy. Į
// proxy suvyniotam google.maps.Marker `setMap(null)` nebenuima žymeklio
// nuo žemėlapio — todėl kiekvienas filtras pridėdavo naujų žymeklių ant
// senų. Būsenoje lieka tik paprasti duomenys.
// ═══════════════════════════════════════════════════════════════════
// Didžiausias mastelis, iki kurio priartinam PATYS (sankaupa, vietos
// paieška). Ranka pelės ratuku žmogus gali priartinti ir toliau.
const MAKS_MASTELIS = 15;


// Markės parametras kiekvienoje šeimoje savas — sunkvežimiams
// `truck_brand`, žemės ūkiui `agri_brand_text` ir t. t. Vardus duoda
// /ajax/markes/ (`param` ir kiekvieno įrašo `p`); čia tik sąrašas, kurį
// reikia išvalyti keičiant pasirinkimą.
const MARKIU_PARAMAI = ['brand', 'truck_brand', 'motorcycle_brand',
    'agri_brand_text', 'trailer_brand_text', 'rent_brand_text',
    'elec_brand_text', 'load_brand_text', 'constr_brand_text',
    'forest_brand_text', 'camp_brand_text', 'bike_brand_text'];

const G = {
    zem: null, sankaupos: null, burbulas: null,
    imones: [],         // įmonių žymekliai (OverlayView)
    zymekliai: {},      // id -> žymeklis
    visi: [],           // visi šįkart sukurti žymekliai
    apskritimai: [],    // apytikslių vietų punktyrai
};

function zemelapioPaieska() {
    // Pradinė padėtis ateina per json_script — taip išvengiam HTML kabučių
    // vertimo (dėl jo anksčiau lūždavo visas skriptas).
    let pradine = { lat: 55.17, lng: 23.88, z: 7, is_url: false };
    try { pradine = JSON.parse(document.getElementById('zpPradine').textContent); } catch (e) {}

    return {
        // ── būsena ──
        kiek: 0,
        langoKiek: 0,
        kraunama: false,   // krovimo metu sąrašas pritemdomas
        _programinis: false,
        zemelapisMatomas: true,
        mobZemelapis: false,
        filtraiAtidaryti: false,
        vietosQ: '',
        vietos: [],
        markesQ: '',
        f: {},            // juostos filtrai (taikomi iškart)
        l: {},            // lango filtrai (taikomi paspaudus „Rodyti")
        kategorijos: [],   // [{slug, vardas, kiek}] — tik netuščios
        markes: [],        // [{v, n, c, k, p}] pagal pasirinktą kategoriją
        modeliai: [],      // [{v, n, c}] pagal pasirinktą markę
        markesKat: null,   // kuriai kategorijai jos užkrautos ('' = visos)
        markesParam: 'brand',
        markeRaktas: '',   // juostos pasirinkimas: 'parametras|reikšmė'
        lMarke: '',        // tas pats lange
        _pasirinktas: null,
        _atidarytas: null,
        _atidarytoUrl: '',
        naujameLange: !!pradine.naujame_lange,
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
                if (v && G.zem) setTimeout(() => google.maps.event.trigger(G.zem, 'resize'), 200);
            });
            // Markės — jei adrese jau yra kategorija ar markė, sąrašo
            // reikia iškart (kitaip laukas rodytų tuščią „Markė").
            if (this.f.brand || this.f.category) this.uzkraukMarkes();
            if (this.f.model) setTimeout(() => this.uzkraukModelius(), 400);
            this.laukZemelapio();
            // Atsarginis krovimas: telefone žemėlapis pagal nutylėjimą
            // paslėptas, todėl „idle" gali ir neįvykti — be šito sąrašas
            // liktų tuščias.
            setTimeout(() => { if (!this._pakrauta) this.uzkrauk(); }, 1500);
        },

        /** Filtrai iš adreso — tie patys raktai kaip visose paieškose. */
        isURL() {
            const p = new URLSearchParams(location.search), o = {};
            // Raktai — TIE PATYS, kuriuos skaito filter_listings. „make",
            // „vin", „tik_lietuvoje" iš čia dingo: tokių parametrų atrankos
            // variklis nemoka, todėl jie tik piešdavo žymes.
            ['model', 'category', 'price_min', 'price_max', 'year_min', 'year_max',
             'mileage_min', 'mileage_max', 'fuel_type', 'transmission', 'sort', 'q',
             'has_vin', 'feat_warranty', 'country_filter', 'su_nuotraukomis', 'city']
                .concat(MARKIU_PARAMAI).forEach(k => {
                const v = p.get(k); if (v) o[k] = v;
            });
            MARKIU_PARAMAI.forEach(k => { if (o[k]) this.markeRaktas = k + '|' + o[k]; });
            // Kategorija, markė ir modelis adrese guli kartu su lat/lng/z,
            // todėl nuoroda atkuria ir filtrus, ir žemėlapio padėtį.
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
            G.zem = new google.maps.Map(el, {
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

            // Google atitikmuo „moveend" yra `idle` — jis įvyksta pabaigus
            // tempti ar keisti mastelį, kai žemėlapis nurimsta.
            G.zem.addListener('idle', () => {
                this.irasykURL();
                if (!this._pakrauta) { this.uzkrauk(); return; }
                // Programinis postūmis (vietos paieška, „Atitolinti") pats
                // pasirūpina krovimu — kitaip gautume ciklą.
                if (this._programinis) { this._programinis = false; return; }
                if (!this.ribosPasikeite()) return;   // < 2 % — nejudinam
                clearTimeout(this._atidejimas);
                this._atidejimas = setTimeout(() => this.uzkrauk(), 400);
            });
            G.zem.addListener('click', () => this.uzdarykBurbula());
            document.addEventListener('keydown', e => { if (e.key === 'Escape') this.uzdarykBurbula(); });
            document.addEventListener('click', e => {
                if (e.target.closest('[data-uzdaryti]')) this.uzdarykBurbula();
                // Mygtukas ateina su AJAX HTML, todėl klausom deleguotai
                if (e.target.closest('[data-atitolinti]')) this.atitolink();
            });

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(p => {
                    this._musuVieta = { lat: p.coords.latitude, lng: p.coords.longitude };
                    if (!pradine.is_url) {
                        G.zem.setCenter(this._musuVieta);
                        G.zem.setZoom(10);   // „idle" perkraus sąrašą pats
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
        },

        /** Duomenys pagal matomą plotą. */
        /** Ar žemėlapis realiai matomas (telefone jis pagal nutylėjimą
         *  paslėptas — tada kraštinių nėra ir sąrašas rodo viską). */
        zemelapisRodomas() {
            const el = this.$refs.zemelapis;
            return !!(el && el.offsetWidth > 0 && el.offsetHeight > 0);
        },

        /** Ar plotas pasikeitė tiek, kad vertėtų perkrauti (>2 %).
         *  Pikselinis „drebėjimas" ir mikro postūmiai užklausų nekelia. */
        ribosPasikeite() {
            const b = this.zemelapisRodomas() && G.zem && G.zem.getBounds();
            if (!b) return false;
            const dabar = { s: b.getSouthWest().lat(), n: b.getNorthEast().lat(),
                            v: b.getSouthWest().lng(), r: b.getNorthEast().lng() };
            const sen = this._ribos;
            if (!sen) return true;
            const aukstis = Math.abs(sen.n - sen.s) || 1;
            const plotis = Math.abs(sen.r - sen.v) || 1;
            const santykis = Math.max(
                Math.abs(dabar.s - sen.s) / aukstis, Math.abs(dabar.n - sen.n) / aukstis,
                Math.abs(dabar.v - sen.v) / plotis, Math.abs(dabar.r - sen.r) / plotis);
            return santykis > 0.02;
        },

        /** Programinis žemėlapio postūmis — be automatinio perkrovimo. */
        pastumk(veiksmas) {
            this._programinis = true;
            veiksmas();
        },

        uzkrauk() {
            this._pakrauta = true;
            this.kraunama = true;
            // Sena užklausa nebeaktuali — nutraukiam, kad neperrašytų naujos
            if (this._ctrl) this._ctrl.abort();
            this._ctrl = ('AbortController' in window) ? new AbortController() : null;
            const p = new URLSearchParams(this.f);
            // „Arčiausiai" — atskaitos taškas: vartotojo vieta, o jei jos
            // nežinom, žemėlapio centras.
            if (this.f.sort === 'arciausiai' && G.zem) {
                const t = this._musuVieta || {
                    lat: G.zem.getCenter().lat(), lng: G.zem.getCenter().lng() };
                p.set('mlat', t.lat); p.set('mlng', t.lng);
            }
            const b = this.zemelapisRodomas() && G.zem && G.zem.getBounds();
            if (b) {
                p.set('s', b.getSouthWest().lat()); p.set('n', b.getNorthEast().lat());
                p.set('v', b.getSouthWest().lng()); p.set('r', b.getNorthEast().lng());
            }
            if (b) {
                this._ribos = { s: b.getSouthWest().lat(), n: b.getNorthEast().lat(),
                                v: b.getSouthWest().lng(), r: b.getNorthEast().lng() };
            }
            fetch('/map/duomenys/?' + p.toString(), {
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                signal: this._ctrl ? this._ctrl.signal : undefined,
            })
                .then(r => r.ok ? r.json() : null)
                .then(a => {
                    this.kraunama = false;
                    if (!a) return;
                    this.kiek = a.kiek;
                    if (a.kategorijos) this.kategorijos = a.kategorijos;
                    // Sąrašas keičiamas tik gavus atsakymą — krovimo metu jis
                    // tik pritemdomas, kad ekranas nemirksėtų tuštuma.
                    this.$refs.sarasas.innerHTML = a.html;
                    if (window.laikoZyma) window.laikoZyma.perpiesti(this.$refs.sarasas);
                    this.pieskZymeklius(a.zymekliai);
                    this.uzkraukImones();
                })
                .catch(e => {         // nutraukta arba tinklo klaida —
                    if (e && e.name === 'AbortError') return;   // lieka, kas matoma
                    this.kraunama = false;
                });
        },

        /** Tuščias plotas — atitolinam dviem lygiais ir kraunam iš naujo. */
        atitolink() {
            if (!G.zem) return;
            const naujas = Math.max(1, G.zem.getZoom() - 2);
            this.pastumk(() => G.zem.setZoom(naujas));
            setTimeout(() => this.uzkrauk(), 300);
        },

        /** Įmonių žymekliai: baltas burbulas su logotipu ir vardu.
         *  Google Marker ikona yra vienas paveikslėlis, todėl logotipo į
         *  ją neįdėsi — naudojam OverlayView su tikru HTML. */
        pieskImones(sarasas) {
            (G.imones || []).forEach(o => o.setMap(null));
            G.imones = [];
            if (!G.zem || !sarasas || !sarasas.length) return;
            if (!window.google || !google.maps.OverlayView) return;

            const Klase = this.imoniuKlase();
            sarasas.forEach(i => {
                const o = new Klase(i);
                o.setMap(G.zem);
                G.imones.push(o);
            });
        },

        /** OverlayView klasė kuriama vieną kartą — google.maps jau įkeltas. */
        imoniuKlase() {
            if (G._ImonesKlase) return G._ImonesKlase;
            class ImonesZymeklis extends google.maps.OverlayView {
                constructor(duom) { super(); this.d = duom; this.el = null; }
                onAdd() {
                    const e = document.createElement('a');
                    e.className = 'zp-imone';
                    e.href = this.d.url;
                    e.target = '_blank';
                    e.rel = 'noopener';
                    e.title = this.d.vardas;
                    const logo = this.d.logo
                        ? `<img src="${this.d.logo}" alt="">`
                        : `<span class="zp-imone-raide">${(this.d.vardas || '?')[0]}</span>`;
                    const kiek = this.d.kiek
                        ? `<em>${this.d.kiek}</em>` : '';
                    e.innerHTML = logo + `<span>${this.d.vardas}</span>` + kiek;
                    this.el = e;
                    this.getPanes().floatPane.appendChild(e);
                }
                draw() {
                    if (!this.el) return;
                    const t = this.getProjection().fromLatLngToDivPixel(
                        new google.maps.LatLng(this.d.lat, this.d.lng));
                    if (!t) return;
                    this.el.style.left = t.x + 'px';
                    this.el.style.top = t.y + 'px';
                }
                onRemove() {
                    if (this.el && this.el.parentNode) this.el.parentNode.removeChild(this.el);
                    this.el = null;
                }
            }
            G._ImonesKlase = ImonesZymeklis;
            return G._ImonesKlase;
        },

        uzkraukImones() {
            const p = new URLSearchParams();
            const b = this.zemelapisRodomas() && G.zem && G.zem.getBounds();
            if (b) {
                p.set('s', b.getSouthWest().lat()); p.set('n', b.getNorthEast().lat());
                p.set('v', b.getSouthWest().lng()); p.set('r', b.getNorthEast().lng());
            }
            fetch('/imones/duomenys/?' + p.toString(),
                  { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.ok ? r.json() : { imones: [] })
                .then(a => this.pieskImones(a.imones || []))
                .catch(() => {});   // be įmonių žemėlapis veikia toliau
        },

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
            if (!G.zem) return;
            // Senus žymeklius nuimam patys: vien `clearMarkers()` palieka
            // ankstesnę sankaupų grupę gyvą ir žymekliai kaupdavosi.
            if (G.sankaupos) {
                G.sankaupos.clearMarkers();
                G.sankaupos.setMap(null);
                G.sankaupos = null;
            }
            (G.visi || []).forEach(m => {
                google.maps.event.clearInstanceListeners(m);
                m.setMap(null);
            });
            G.visi = [];
            (G.apskritimai || []).forEach(a => a.setMap(null));
            G.apskritimai = [];
            G.zymekliai = {};
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
                m.addListener('click', () => this.zymeklioPaspaudimas(z.id, z.tipas));
                m.addListener('mouseover', () => this.zymeklioUzvedimas(z.id, true));
                m.addListener('mouseout', () => this.zymeklioUzvedimas(z.id, false));
                G.zymekliai[z.id] = m;
                zym.push(m);

                // Apytikslė vieta — punktyrinis ~500 m apskritimas
                if (z.apytiksliai) {
                    G.apskritimai.push(new google.maps.Circle({
                        map: G.zem, center: { lat: z.lat, lng: z.lng }, radius: 500,
                        strokeColor: '#111827', strokeOpacity: .55, strokeWeight: 1.5,
                        fillColor: '#111827', fillOpacity: .07, clickable: false,
                    }));
                }
            });

            G.visi = zym;
            if (window.markerClusterer && window.markerClusterer.MarkerClusterer) {
                G.sankaupos = new markerClusterer.MarkerClusterer({
                    map: G.zem, markers: zym,
                    renderer: { render: ({ count, position }) => new google.maps.Marker({
                        position, zIndex: 50,
                        icon: this.ikona(String(count), 'įprastas'),
                    }) },
                    onClusterClick: (e, sankaupa, zem) => this.sankaupaPaspausta(sankaupa, zem),
                });
            } else {
                zym.forEach(m => m.setMap(G.zem));
            }
        },

        /** Sankaupa: priartinam tiek, kad ji išsiskirtų — apie du lygius,
         *  ne iki galo. Ties MAKS_MASTELIS rodom skelbimų sąrašą.
         *
         *  fitBounds prie tankios sankaupos nulekia iki z=20, o tada
         *  matosi atskiri namai ir dingsta kontekstas — todėl po jo
         *  mastelį prispaudžiam. */
        sankaupaPaspausta(sankaupa, zem) {
            const dabar = zem.getZoom();
            if (dabar >= MAKS_MASTELIS) {
                this.rodykSarasa((sankaupa.markers || []).map(m => m.__id).filter(Boolean));
                return;
            }
            const tikslas = Math.min(dabar + 2, MAKS_MASTELIS);
            zem.fitBounds(sankaupa.bounds, 80);
            google.maps.event.addListenerOnce(zem, 'idle', () => {
                if (zem.getZoom() > tikslas) zem.setZoom(tikslas);
            });
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
            if (G.burbulas) G.burbulas.close();
            this.lapasAtidarytas = false;
            if (this._atidarytas !== null) { this._atidarytas = null; this.perpieskBusena(); }
        },

        rodykAikstele(pardavejas) {
            fetch('/map/pardavejas/' + pardavejas + '/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.ok ? r.json() : null)
                .then(a => { if (a) this.rodykTurini(a.html, null); })
                .catch(() => {});
        },

        /** Pirmas paspaudimas — kortelė, antras — atidaro skelbimą.
         *  Darbalaukyje naujame skirtuke (paieška lieka nepaliesta),
         *  telefone — tame pačiame lange; adrese guli žemėlapio padėtis
         *  ir filtrai, todėl „atgal" grąžina tiksliai ten, kur buvai. */
        zymeklioPaspaudimas(id, tipas) {
            if (this._atidarytas === id) { this.atidarykSkelbima(); return; }
            this._atidarytas = id;
            this._atidarytoUrl = '';
            this.perpieskBusena();
            const adr = '/map/kortele/' + id + '/' + (tipas ? '?tipas=' + tipas : '');
            fetch(adr, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.ok ? r.json() : null)
                .then(a => {
                    if (!a) return;
                    this._atidarytoUrl = a.url || '';
                    this.rodykTurini(a.html, G.zymekliai[id], a);
                })
                .catch(() => {});
        },

        atidarykSkelbima() {
            const url = this._atidarytoUrl;
            if (!url) return;
            // Sprendžia serveris (device_kind) — kad juostoje, burbule ir
            // žymeklyje elgesys būtų vienodas.
            if (this.naujameLange) window.open(url, '_blank', 'noopener');
            else window.location = url;
        },

        /** Užvedus — paryškinam kortelę sąraše (paspaudimas daro kita). */
        zymeklioUzvedimas(id, ijungta) {
            const kort = this.$refs.sarasas.querySelector('[data-kort="' + id + '"]');
            if (kort) kort.classList.toggle('is-pazymeta', ijungta);
            const m = G.zymekliai[id];
            if (!m) return;
            m.setIcon(this.ikona(m.__kaina, this._atidarytas === id ? 'pasirinktas' : m.__busena,
                                 ijungta));
            m.setZIndex(ijungta ? 60 : (m.__busena === 'ziuretas' ? 5 : 10));
        },

        perpieskBusena() {
            Object.keys(G.zymekliai).forEach(id => {
                const m = G.zymekliai[id];
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
            if (!G.burbulas) {
                G.burbulas = new google.maps.InfoWindow({ maxWidth: 268 });
                G.burbulas.addListener('closeclick', () => { this._atidarytas = null; this.perpieskBusena(); });
            }
            G.burbulas.setContent(html);
            // Sankaupoje esantis žymeklis nėra žemėlapyje — tada rišam prie taško
            if (zymeklis && zymeklis.getMap()) {
                G.burbulas.open({ map: G.zem, anchor: zymeklis });
            } else if (duom && duom.lat != null) {
                G.burbulas.setPosition({ lat: duom.lat, lng: duom.lng });
                G.burbulas.open({ map: G.zem });
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
            const m = G.zymekliai[kort.dataset.kort];
            if (m) m.setAnimation(google.maps.Animation.BOUNCE);
        },
        nupazymek() {
            Object.values(G.zymekliai).forEach(m => m.setAnimation(null));
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
            if (!G.zem || !v.lat) return;
            // Šalis — mažesnis mastelis, adresas — didesnis
            const salis = !v.miestas || v.tekstas.split(',').length <= 1;
            this.pastumk(() => {
                G.zem.setCenter({ lat: v.lat, lng: v.lon });
                G.zem.setZoom(Math.min(salis ? 6 : 12, MAKS_MASTELIS));
            });
            setTimeout(() => this.uzkrauk(), 300);
        },

        // ── Markės ──
        kategorijosVardas(slug) {
            const k = this.kategorijos.find(x => x.slug === slug);
            if (k) return k.vardas + ' (' + k.kiek + ')';
            return ((window.ZP_VARDAI || {}).kategorijos || {})[slug] || slug;
        },

        kategorijosIkona(slug) { return (window.ZP_IKONOS || {})[slug] || ''; },

        /** Markės iš /ajax/markes/ — to paties šaltinio kaip panelėse.
         *  Su kategorija — tos šeimos markės, be jos — visos šeimos. */
        uzkraukMarkes(kat) {
            kat = (kat === undefined ? (this.f.category || '') : (kat || ''));
            if (this.markesKat === kat) return;
            this.markesKat = kat;
            const adr = kat ? '/ajax/markes/?kategorija=' + encodeURIComponent(kat)
                            : '/ajax/markes/?visos=1';
            fetch(adr)
                .then(r => r.ok ? r.json() : { markes: [] })
                .then(a => {
                    this.markesParam = a.param || 'brand';
                    this.markes = (a.markes || []).slice()
                        .sort((x, y) => x.n.localeCompare(y.n, 'lt'));
                })
                .catch(() => { this.markes = []; });
        },

        /** Modeliai — tas pats /ajax/modeliai/, kurį naudoja panelės.
         *  Kaskada: be markės sąrašo nėra, todėl laukas neaktyvus.
         *  Modelių duomenų yra tik ten, kur jų yra DB (automobiliai,
         *  motociklai) — kitose kategorijose laukas lieka neaktyvus. */
        uzkraukModelius() {
            const m = this.pagalRakta(this.markeRaktas);
            const kat = this.f.category || '';
            if (!m || !kat) { this.modeliai = []; return; }
            fetch('/ajax/modeliai/?kategorija=' + encodeURIComponent(kat) +
                  '&marke=' + encodeURIComponent(m.v))
                .then(r => r.ok ? r.json() : { modeliai: [] })
                .then(a => {
                    this.modeliai = (a.modeliai || []).slice()
                        .sort((x, y) => x.n.localeCompare(y.n, 'lt'));
                })
                .catch(() => { this.modeliai = []; });
        },

        /** Lange rodom ne visas 2 300 — tik tas, kurias randa paieška. */
        markesRodomos() {
            const q = (this.markesQ || '').trim().toLowerCase();
            const sar = q ? this.markes.filter(m => m.n.toLowerCase().includes(q))
                          : this.markes;
            return sar.slice(0, 200);
        },

        /** Markę taikom TUO parametru, kurio prašo jos šeima. */
        taikykMarke() {
            MARKIU_PARAMAI.forEach(k => { delete this.f[k]; });
            // Modelis gyvena markės viduje — pakeitus markę jis nebegalioja
            delete this.f.model;
            this.modeliai = [];
            const m = this.pagalRakta(this.markeRaktas);
            if (m) {
                this.f[m.p || this.markesParam] = String(m.v);
                // Tekstiniai markės laukai veikia tik savo kategorijoje,
                // todėl kartu pažymim ir ją.
                if (m.k && !this.f.category) {
                    this.f.category = m.k;
                    this.markesKat = null;
                    this.uzkraukMarkes(m.k);
                }
            }
            this.uzkraukModelius();
            this.taikyk();
        },

        pagalRakta(raktas) {
            if (!raktas) return null;
            const i = raktas.indexOf('|');
            const par = raktas.slice(0, i), v = raktas.slice(i + 1);
            return this.markes.find(x => (x.p || this.markesParam) === par
                                         && String(x.v) === v) || null;
        },

        raktas(m) { return (m.p || this.markesParam) + '|' + m.v; },

        /** Kategorija: filtruoja sąrašą ir persirenka markes. */
        keiskKategorija() {
            // Markė gyvena kategorijos viduje (ir kitu parametru), todėl
            // pakeitus kategoriją senoji nebegalioja.
            MARKIU_PARAMAI.forEach(k => { delete this.f[k]; });
            delete this.f.model;
            this.markeRaktas = '';
            this.modeliai = [];
            this.markesKat = null;
            this.uzkraukMarkes();
            this.taikyk();
        },

        // ── Filtrai ──
        atidarykFiltrus() {
            this.l = Object.assign({}, this.f);
            this.lMarke = this.markeRaktas;
            this.filtraiAtidaryti = true;
            this.uzkraukMarkes(this.l.category || '');
            this.perskaiciuok();
        },
        uzdarykFiltrus() { this.filtraiAtidaryti = false; },
        pritaikykFiltrus() {
            this.f = Object.assign({}, this.valyk(this.l));
            this.filtraiAtidaryti = false;
            this.markeRaktas = this.lMarke;
            this.uzkraukMarkes(this.f.category || '');
            this.taikykMarke();
        },
        valyk(o) { const r = {}; Object.keys(o).forEach(k => { if (o[k]) r[k] = o[k]; }); return r; },

        perskaiciuok() {
            const l = Object.assign({}, this.l);
            MARKIU_PARAMAI.forEach(k => { delete l[k]; });
            const m = this.pagalRakta(this.lMarke);
            if (m) l[m.p || this.markesParam] = String(m.v);
            const p = new URLSearchParams(this.valyk(l));
            const b = this.zemelapisRodomas() && G.zem && G.zem.getBounds();
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
            this.lMarke = '';
            if (irJuosta) { this.f = {}; this.markeRaktas = ''; this.taikyk(); }
            this.perskaiciuok();
        },
        nuimk(raktas) {
            delete this.f[raktas]; delete this.l[raktas];
            if (MARKIU_PARAMAI.indexOf(raktas) !== -1) {
                this.markeRaktas = ''; this.lMarke = '';
                delete this.f.model; this.modeliai = [];
            }
            if (raktas === 'category') {
                // Be kategorijos senoji markė nebegalioja: kitoje šeimoje
                // tas pats id reiškia kitą markę.
                MARKIU_PARAMAI.forEach(k => { delete this.f[k]; delete this.l[k]; });
                this.markeRaktas = ''; this.lMarke = '';
                delete this.f.model; delete this.l.model; this.modeliai = [];
                this.markesKat = null; this.uzkraukMarkes('');
            }
            this.taikyk();
        },

        aktyvuKiek() { return Object.keys(this.valyk(this.f)).length; },
        /** Filtro reikšmė žmogui: kategorijos ir kuro vardai, ne raktai. */
        vardas(raktas, reiksme) {
            const V = window.ZP_VARDAI || {};
            if (raktas === 'category') return (V.kategorijos || {})[reiksme] || reiksme;
            if (raktas === 'model') {
                const m = this.modeliai.find(x => String(x.v) === String(reiksme));
                return m ? m.n : reiksme;
            }
            if (MARKIU_PARAMAI.indexOf(raktas) !== -1) {
                const m = this.markes.find(x => String(x.v) === String(reiksme));
                return m ? m.n : reiksme;   // tekstiniuose laukuose reikšmė ir yra vardas
            }
            if (raktas === 'fuel_type') return (V.kuras || {})[reiksme] || reiksme;
            if (raktas === 'sort') return (V.rusiavimas || {})[reiksme] || reiksme;
            return reiksme;
        },

        aktyvuSarasas() {
            const T = window.ZP_TEKSTAI || {};
            const vardai = { q: T.tekstas, category: T.kategorija, model: T.modelis,
                             city: T.vieta, price_min: T.kaina + ' ' + T.nuo, price_max: T.kaina + ' ' + T.iki,
                             year_min: T.metai + ' ' + T.nuo, year_max: T.metai + ' ' + T.iki,
                             mileage_min: T.rida + ' ' + T.nuo, mileage_max: T.rida + ' ' + T.iki,
                             fuel_type: T.kuras };
            // „Kita" žymos (has_vin, country_filter…) — vien pavadinimas,
            // reikšmė („1", „LT") žmogui nieko nesako.
            const papildomi = (window.ZP_VARDAI || {}).papildomi || {};
            return Object.keys(this.valyk(this.f)).map(k => {
                const et = MARKIU_PARAMAI.indexOf(k) !== -1 ? T.marke : vardai[k];
                return {
                    raktas: k,
                    tekstas: papildomi[k] ? papildomi[k]
                             : (et ? et + ': ' : '') + this.vardas(k, this.f[k]),
                };
            });
        },

        /** Padėtis ir filtrai adrese — nuorodą galima dalintis. */
        irasykURL() {
            if (!G.zem) return;
            const c = G.zem.getCenter(); if (!c) return;
            const p = new URLSearchParams(this.valyk(this.f));
            p.set('lat', c.lat().toFixed(5)); p.set('lng', c.lng().toFixed(5));
            p.set('z', G.zem.getZoom());
            history.replaceState(null, '', location.pathname + '?' + p.toString());
        },
    };
}
