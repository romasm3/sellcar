/**
 * ĮMONIŲ PUSLAPIS — maketas ir elgsena iš docs/demo/imones-fresha-1v1.html.
 *
 * Rodom TIK apps.imones objektus: /imones/duomenys/ grąžina ir korteles,
 * ir žymeklius, ir burbulus iš vieno įrašo. Skelbimų (Listing) čia nėra.
 *
 * Žemėlapis — Google Maps su AdvancedMarkerElement: žymeklis lieka toks
 * pat HTML kaip etalone (juoda piliulė su ★, trikampis smaigalys).
 * /map/ (skelbimai) turi savo atskirą instanciją ir savo konteinerį —
 * nieko nebendrinam.
 *
 * Koordinatės į DB rašomos tik iš Photon/Nominatim (kūrimo forma) —
 * Google geokoderio čia nenaudojam.
 */
const FR = { zem: null, zymekliai: {}, sankaupos: null, burbulas: null,
             duomenys: [], musuVieta: null };

/** Tekstai iš šablono (json_script) — JS'e eilučių nelaikom.
 *  Skaitom tinginiu būdu: juosta pasileidžia anksčiau už puslapį. */
function frTekstai() {
    if (!FR.tekstai) {
        const e = document.getElementById('fr-tekstai');
        FR.tekstai = e ? JSON.parse(e.textContent) : {};
    }
    return FR.tekstai;
}

/* ── Paieškos baras antraštėje ───────────────────────────────────
 * Trys atskiri langai, kiekvienas savo segmente (maketas —
 * docs/paieskos-dropdown-demo_3.html). Atidarytas langas uždeda
 * body.fr-atverta: tamsėja fonas, baras platėja, apvalus mygtukas
 * virsta „Ieškoti".                                              */
const FR_ATMINTIS = { paieskos: 'fr-paskutines-paieskos', vietos: 'fr-paskutines-vietos' };

/** localStorage gali būti uždarytas (privatus langas) — tada tyliai be istorijos. */
function frAtmintis(raktas) {
    try { return JSON.parse(localStorage.getItem(raktas)) || []; } catch (e) { return []; }
}
function frIrasyk(raktas, sarasas) {
    try { localStorage.setItem(raktas, JSON.stringify(sarasas.slice(0, 5))); } catch (e) { /* pilna arba uždaryta */ }
}
function frKalba() { return document.documentElement.lang || 'lt'; }

function freshaJuosta() {
    return {
        atidarytas: '', ko: '', koVeikla: '', cipsas: 'visi',
        vieta: '', vietosQ: '', vietosKlaida: '', vlat: '', vlng: '',
        kada: '', data: '', paros: '',
        vietos: [], vietosPask: [], paskutines: [], grupes: [], cipsai: [],
        menuoData: null, skrisk: false,

        /** Pradinė būsena iš adreso — kad po perkrovimo baras rodytų tą patį. */
        paruoskJuosta() {
            const p = new URLSearchParams(location.search);
            this.ko = p.get('q') || '';
            this.koVeikla = p.get('veikla') || '';
            this.vieta = p.get('city') || '';
            this.vlat = p.get('vlat') || ''; this.vlng = p.get('vlng') || '';
            this.data = p.get('data') || ''; this.paros = p.get('paros') || '';
            this.paskutines = frAtmintis(FR_ATMINTIS.paieskos);
            this.vietosPask = frAtmintis(FR_ATMINTIS.vietos);
            this.menuoData = this.data ? new Date(this.data + 'T00:00:00') : new Date();
            this.menuoData.setDate(1);
        },

        /** Adresas iš juostos data- atributo (jame yra kalbos priešdėlis). */
        adresas(kuris, atsarginis) {
            const f = document.querySelector('.fr-sb');
            return (f && f.dataset[kuris]) || atsarginis;
        },

        atidaryk(kuris) {
            if (this.atidarytas === kuris) return;      // paspaudimas lange nieko nekeičia
            this.atidarytas = kuris;
            document.body.classList.add('fr-atverta');
            if (kuris === 'ko') { this.ieskok(); this.$nextTick(() => this.$refs.koLaukas.focus()); }
            if (kuris === 'vieta') { this.vietosKlaida = ''; this.$nextTick(() => this.$refs.vietosLaukas.focus()); }
        },

        uzdaryk() {
            this.atidarytas = '';
            document.body.classList.remove('fr-atverta');
        },

        /* ---- 1. Paslauga ---- */
        ieskok() {
            fetch(this.adresas('siulymai', '/ajax/paieska/') + '?sritis=imoniu_puslapis' +
                  '&tipas=' + encodeURIComponent(this.cipsas) +
                  '&q=' + encodeURIComponent(this.ko))
                .then(r => r.ok ? r.json() : { grupes: [] })
                .then(a => { this.grupes = a.grupes || []; this.cipsai = a.cipsai || this.cipsai; })
                .catch(() => { this.grupes = []; });
        },

        pasirink(e) {
            this.ko = e.vardas;
            // Paslauga filtruoja pagal veiklos sritį, įmonė ir meistras — pagal vardą
            this.koVeikla = (e.url || '').includes('veikla=') ? e.url.split('veikla=')[1] : '';
            this.idekPaskutine({ vardas: e.vardas, apie: e.vieta || e.apie || '',
                                 veikla: this.koVeikla });
            this.uzdaryk();
        },

        pasirinkPaskutine(pa) {
            this.ko = pa.vardas; this.koVeikla = pa.veikla || '';
            this.uzdaryk();
        },

        idekPaskutine(irasas) {
            const be = this.paskutines.filter(x => x.vardas !== irasas.vardas);
            this.paskutines = [irasas].concat(be).slice(0, 5);
            frIrasyk(FR_ATMINTIS.paieskos, this.paskutines);
        },

        valykPaskutines() { this.paskutines = []; frIrasyk(FR_ATMINTIS.paieskos, []); },

        /* ---- 2. Vieta ---- */
        ieskokVietos() {
            const q = this.vietosQ.trim();
            this.vietosKlaida = '';
            if (q.length < 3) { this.vietos = []; return; }
            if (this._vCtrl) this._vCtrl.abort();
            this._vCtrl = new AbortController();
            fetch(this.adresas('adresai', '/ajax/adresai/') + '?salis=LT&kiek=6&q=' +
                  encodeURIComponent(q), { signal: this._vCtrl.signal })
                .then(r => r.ok ? r.json() : { siulymai: [] })
                .then(a => { this.vietos = (a.siulymai || []).slice(0, 6); })
                .catch(e => { if (e.name !== 'AbortError') this.vietos = []; });
        },

        pasirinkVieta(v) {
            const vietove = ['city', 'town', 'village', 'district', 'locality', 'hamlet']
                .indexOf(v.tipas) !== -1;
            this.vieta = v.miestas || (vietove ? v.vardas : '') || v.vardas || v.tekstas || '';
            this.vlat = v.lat || ''; this.vlng = v.lng || v.lon || '';
            this.vietosQ = ''; this.vietos = [];
            if (this.vieta || this.vlat) {
                const be = this.vietosPask.filter(x => x.vardas !== (v.vardas || this.vieta));
                this.vietosPask = [{ vardas: v.vardas || this.vieta,
                                     apie: v.apie || v.tekstas || '', miestas: this.vieta,
                                     lat: this.vlat, lng: this.vlng }].concat(be).slice(0, 5);
                frIrasyk(FR_ATMINTIS.vietos, this.vietosPask);
            }
            this.uzdaryk();
            this.siusk();
        },

        valykVietas() { this.vietosPask = []; frIrasyk(FR_ATMINTIS.vietos, []); },

        dabartineVieta() {
            const T = frTekstai();
            if (!navigator.geolocation) { this.vietosKlaida = T.vietosKlaida; return; }
            this.vietosKlaida = T.vietosIeskom;
            navigator.geolocation.getCurrentPosition(p => {
                fetch(this.adresas('vieta', '/ajax/vieta/') +
                      '?lat=' + p.coords.latitude + '&lon=' + p.coords.longitude)
                    .then(r => r.ok ? r.json() : { vieta: {} })
                    .then(a => {
                        this.vietosKlaida = '';
                        this.pasirinkVieta({ vardas: (a.vieta || {}).miestas || T.vietaCia,
                                             miestas: (a.vieta || {}).miestas || '',
                                             apie: (a.vieta || {}).salis || '',
                                             lat: p.coords.latitude, lng: p.coords.longitude });
                    })
                    .catch(() => { this.vietosKlaida = T.vietosKlaida; });
            }, () => { this.vietosKlaida = T.vietosNeleido; }, { timeout: 8000 });
        },

        /* ---- 3. Kada ---- */
        get savaitesRaides() {
            const d = frTekstai().dienos || [];
            return [d[1], d[2], d[3], d[4], d[5], d[6], d[0]];   // nuo pirmadienio
        },

        get menuoVardas() {
            const d = this.menuoData || new Date();
            const m = d.toLocaleDateString(frKalba(), { month: 'long' });
            return m.charAt(0).toUpperCase() + m.slice(1) + ' ' + d.getFullYear();
        },

        /** Mėnesio tinklelis: tušti langeliai iki pirmadienio, tada dienos. */
        get dienos() {
            const d = this.menuoData || new Date();
            const metai = d.getFullYear(), men = d.getMonth();
            const pirma = new Date(metai, men, 1);
            const poslinkis = (pirma.getDay() + 6) % 7;
            const kiek = new Date(metai, men + 1, 0).getDate();
            const siandien = new Date(); siandien.setHours(0, 0, 0, 0);
            const eil = [];
            for (let i = 0; i < poslinkis; i++) eil.push({ diena: 0 });
            for (let n = 1; n <= kiek; n++) {
                const data = new Date(metai, men, n);
                eil.push({
                    diena: n,
                    praeitis: data < siandien,
                    iso: metai + '-' + String(men + 1).padStart(2, '0') + '-' + String(n).padStart(2, '0'),
                });
            }
            return eil;
        },

        menuo(zingsnis) {
            const d = new Date(this.menuoData || new Date());
            d.setDate(1); d.setMonth(d.getMonth() + zingsnis);
            this.menuoData = d;
        },

        valykKada() { this.data = ''; this.paros = ''; },

        get kadosVardas() {
            const T = frTekstai();
            const dalys = [];
            if (this.data) {
                dalys.push(new Date(this.data + 'T00:00:00')
                    .toLocaleDateString(frKalba(), { month: 'long', day: 'numeric' }));
            }
            if (this.paros) dalys.push((T.paros || {})[this.paros] || '');
            return { tikra: dalys.length > 0, tekstas: dalys.join(' · ') || T.betKada };
        },

        /* ---- Bendra ---- */
        paruosk() {
            const dek = (n, v) => { const e = this.$refs[n]; if (!e) return;
                e.value = v || ''; e.disabled = !v; };
            dek('pQ', this.koVeikla ? '' : this.ko.trim());
            dek('pVeikla', this.koVeikla);
            dek('pCity', this.vieta.trim());
            dek('pLaikas', this.kada);
            dek('pData', this.data);
            dek('pParos', this.paros);
            dek('pLat', this.vlat);
            dek('pLng', this.vlng);
        },

        /** Pasirinkus vietą ieškom iškart — žemėlapis nuskrenda pats. */
        siusk() {
            this.skrisk = true;
            this.paruosk();
            // $root — forma (x-data šaknis). $el čia būtų paspaustas mygtukas.
            this.$root.submit();
        },
    };
}

/* ── Puslapis: sąrašas, datų juosta ir žemėlapis ─────────────────── */
function freshaPuslapis() {
    const T = frTekstai;
    const ZVAIGZDE = '<svg viewBox="0 0 24 24"><path d="M12 2l3 6.6 7 .9-5.1 4.8 1.3 7-6.2-3.4L5.8 21l1.3-7L2 9.5l7-.9z"/></svg>';

    return {
        kiek: 0,
        zemelapis: true,
        pajudinta: false,
        filtraiAtidaryti: false,
        _pakrauta: false,
        _ctrl: null,

        paruosk() {
            this.datuJuosta();
            this.zemelapioParuosimas();
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(p => {
                    FR.musuVieta = { lat: p.coords.latitude, lng: p.coords.longitude };
                    this.piesk(FR.duomenys);      // atstumai atsiranda, kai žinom vietą
                }, () => {}, { timeout: 4000 });
            }
        },

        /* ---- datų juosta: Bet kada · Šiandien · Rytoj · Pr 31 … ---- */
        datuJuosta() {
            const t = T(), sh = t.dienos;
            let html = `<button class="on">${t.betKada}</button>` +
                       `<button>${t.siandien}</button>` +
                       `<button>${t.rytoj}</button>`;
            const dabar = new Date();
            for (let i = 2; i < 16; i++) {
                const d = new Date(dabar.getTime() + i * 864e5);
                html += `<button>${sh[d.getDay()]} ${d.getDate()}</button>`;
            }
            this.$refs.datos.innerHTML = html;
            this.$refs.datos.addEventListener('click', e => {
                if (e.target.tagName !== 'BUTTON') return;
                this.$refs.datos.querySelectorAll('button').forEach(b => b.classList.remove('on'));
                e.target.classList.add('on');
                this.uzkrauk();
            });
        },

        /* ---- žemėlapis (Google) ---- */
        zemelapioParuosimas() {
            if (!window.google || !google.maps || !google.maps.marker) {
                setTimeout(() => this.zemelapioParuosimas(), 200);
                return;
            }
            let pradine = { lat: 54.6872, lng: 25.2797, z: 12 };
            try { pradine = JSON.parse(document.getElementById('frPradine').textContent); }
            catch (e) {}
            const el = document.getElementById('frMap');
            FR.zem = new google.maps.Map(el, {
                center: { lat: pradine.lat, lng: pradine.lng },
                zoom: pradine.z,
                mapId: el.dataset.mapId || 'DEMO_MAP_ID',
                gestureHandling: 'greedy',   // ratukas zoomina iškart, be ctrl
                zoomControl: false,          // savi mygtukai apačioj dešinėj
                mapTypeControl: false,
                streetViewControl: false,
                fullscreenControl: false,
            });
            FR.burbulas = new google.maps.InfoWindow({ maxWidth: 268 });
            FR.zem.addListener('idle', () => {
                if (this._pakrauta) this.pajudinta = true;
                this.irasykURL();
            });
            FR.zem.addListener('click', () => FR.burbulas && FR.burbulas.close());
            this.uzkrauk();
        },

        priartink(k) { if (FR.zem) FR.zem.setZoom(FR.zem.getZoom() + k); },

        visasEkranas() {
            const el = document.getElementById('frMap');
            if (!document.fullscreenElement) el.requestFullscreen && el.requestFullscreen();
            else document.exitFullscreen();
            setTimeout(() => FR.zem && google.maps.event.trigger(FR.zem, 'resize'), 300);
        },

        perjunkZemelapi() {
            this.zemelapis = !this.zemelapis;
            if (this.zemelapis) setTimeout(() => {
                if (FR.zem) google.maps.event.trigger(FR.zem, 'resize');
            }, 60);
        },

        /* ---- duomenys ---- */
        uzkrauk() {
            this._pakrauta = true;
            if (this._ctrl) this._ctrl.abort();
            this._ctrl = ('AbortController' in window) ? new AbortController() : null;
            const p = new URLSearchParams(location.search);
            ['lat', 'lng', 'z', 'skrendam'].forEach(k => p.delete(k));
            // Paspaudus „Ieškoti" pirmas krovimas be kraštinių: nuskrendam
            // prie VISŲ rezultatų, ne prie to, kas atsitiktinai matoma.
            const skrendam = new URLSearchParams(location.search).get('skrendam');
            const b = !skrendam && FR.zem && this.zemelapis && FR.zem.getBounds();
            if (b) {
                p.set('s', b.getSouthWest().lat()); p.set('n', b.getNorthEast().lat());
                p.set('v', b.getSouthWest().lng()); p.set('r', b.getNorthEast().lng());
            }
            const adresas = (document.getElementById('frMap') || {}).dataset;
            fetch((adresas && adresas.duomenys || '/imones/duomenys/') + '?' + p.toString(),
                  { headers: { 'X-Requested-With': 'XMLHttpRequest' },
                    signal: this._ctrl ? this._ctrl.signal : undefined })
                .then(r => r.ok ? r.json() : null)
                .then(a => {
                    if (!a) return;
                    this.kiek = a.kiek;
                    FR.duomenys = a.imones || [];
                    this.piesk(FR.duomenys);
                    this.pajudinta = false;
                    if (skrendam) this.skriskPrieVisu();
                })
                .catch(e => { if (!e || e.name !== 'AbortError') { /* lieka, kas matoma */ } });
        },

        /** Paspaudus „Ieškoti" — nuskrendam prie visų rezultatų ribų. */
        skriskPrieVisu() {
            const su = FR.duomenys.filter(c => c.lat && c.lng);
            if (!FR.zem || !su.length) return;
            const ribos = new google.maps.LatLngBounds();
            su.forEach(c => ribos.extend({ lat: c.lat, lng: c.lng }));
            // Paraštės — kad piliulė neliktų nukirsta prie krašto
            FR.zem.fitBounds(ribos, { top: 60, right: 40, bottom: 40, left: 40 });
            this.pajudinta = false;
            window.scrollTo({ top: 0, behavior: 'smooth' });
            // Vėliavėlę nuimam, kad kiti krovimai vėl eitų pagal plotą
            const p = new URLSearchParams(location.search);
            p.delete('skrendam');
            history.replaceState(null, '', location.pathname +
                (p.toString() ? '?' + p.toString() : ''));
        },

        /* ---- kortelės ir žymekliai ---- */
        piesk(sarasas) {
            this.$refs.tinklas.innerHTML = sarasas.map(c => this.kortele(c)).join('');
            this.rikKorteles();
            (FR.sankaupos ? [FR.sankaupos] : []).forEach(s => s.clearMarkers());
            Object.values(FR.zymekliai).forEach(m => { m.map = null; });
            FR.zymekliai = {};
            const zym = [];
            sarasas.forEach(c => {
                if (!c.lat || !c.lng) return;
                const el = document.createElement('div');
                el.className = 'fr-pin';
                el.id = 'frPin' + c.id;
                el.innerHTML = ZVAIGZDE + (c.reitingas || 0).toFixed(1);
                const m = new google.maps.marker.AdvancedMarkerElement({
                    map: FR.zem, position: { lat: c.lat, lng: c.lng },
                    content: el, title: c.vardas,
                });
                m.addListener('click', () => this.rodykBurbula(c, m));
                FR.zymekliai[c.id] = m;
                zym.push(m);
            });
            // Persidengiančius suklijuojam į sankaupas
            if (window.markerClusterer && window.markerClusterer.MarkerClusterer) {
                if (FR.sankaupos) FR.sankaupos.setMap(null);
                FR.sankaupos = new markerClusterer.MarkerClusterer({
                    map: FR.zem, markers: zym,
                    // Sankaupa atrodo kaip ta pati piliulė, tik su skaičiumi
                    renderer: { render: ({ count, position }) => {
                        const el = document.createElement('div');
                        el.className = 'fr-pin';
                        el.textContent = String(count);
                        return new google.maps.marker.AdvancedMarkerElement({
                            position, content: el, zIndex: 10 });
                    } },
                });
            }
        },

        /** Burbulas — ta pati 268 px kortelė kaip anksčiau. */
        rodykBurbula(c, zymeklis) {
            if (!FR.burbulas) return;
            FR.burbulas.setContent(this.burbulas(c));
            FR.burbulas.open({ map: FR.zem, anchor: zymeklis });
        },

        atstumas(c) {
            if (!FR.musuVieta || !c.lat || !c.lng) return '';
            const R = 6371, dLat = (c.lat - FR.musuVieta.lat) * Math.PI / 180,
                  dLng = (c.lng - FR.musuVieta.lng) * Math.PI / 180;
            const a = Math.sin(dLat / 2) ** 2 + Math.cos(FR.musuVieta.lat * Math.PI / 180) *
                      Math.cos(c.lat * Math.PI / 180) * Math.sin(dLng / 2) ** 2;
            const km = 2 * R * Math.asin(Math.sqrt(a));
            return km.toFixed(1).replace('.', ',') + ' km · ';
        },

        kortele(c) {
            const t = T();
            const foto = c.img ? `<img src="${c.img}" alt="" loading="lazy">` : '';
            const meistras = c.meistras ? ' yra-meistras' : '';
            // Čipsai — mygtukai, ne nuorodos: kortelė jau yra <a>, o <a>
            // viduje <a> naršyklė išskaido (kortelė lūžo į dvi dalis).
            const cipsai = (c.cipsai || []).map(s =>
                `<button type="button" class="fr-cipsas${s.ghost ? ' ghost' : ''}"
                         data-url="${s.url}">${s.tekstas}</button>`).join('');
            return `
<a class="fr-kort${meistras}" data-id="${c.id}" href="${c.url}" target="_blank" rel="noopener">
  <div class="fr-foto">${foto}
    <button type="button" class="fr-sirdis" data-sirdis="${c.id}">
      <svg viewBox="0 0 24 24"><path d="M12 20s-7-4.5-7-9.2A4 4 0 0 1 12 8a4 4 0 0 1 7 2.8C19 15.5 12 20 12 20z"/></svg>
    </button>
  </div>
  <div class="fr-virsus">
    <div class="fr-vardas">${c.vardas}</div>
    ${c.reitingas ? `<div class="fr-reit">${ZVAIGZDE}${c.reitingas.toFixed(1)}</div>` : ''}
  </div>
  <div class="fr-meta">${this.atstumas(c)}${c.vietove}</div>
  <div class="fr-tipas">${c.tipas}${c.atsiliepimai ? ' · ' + c.atsiliepimai + ' ' + t.atsiliepimai : ''}</div>
  <div class="fr-pasl">
    <div class="fr-pasl-eil"><div class="fr-pasl-vardas">${c.paslauga}</div>
      <div class="fr-pasl-kaina">${c.kaina}</div></div>
    <div class="fr-pasl-trukme">${c.trukme}</div>
    <div class="fr-cipsai">${cipsai}</div>
  </div>
</a>`;
        },

        burbulas(c) {
            const t = T();
            return `<div class="fr-pop">${c.img ? `<a href="${c.url}" target="_blank" rel="noopener"><img src="${c.img}" alt=""></a>` : ''}
  <div class="b"><a class="n" href="${c.url}" target="_blank" rel="noopener">${c.vardas}</a>
  <div class="m">${ZVAIGZDE.replace('<svg', '<svg style="width:12px;height:12px;fill:#F5B301;vertical-align:-1px"')} ${(c.reitingas || 0).toFixed(1)} · ${c.atsiliepimai} ${t.atsiliepimai}</div>
  <div class="m">${c.tipas} · ${c.vietove}</div>
  <div class="p">${c.paslauga} — ${c.kaina}</div>
  <a class="fr-pop-btn" href="${c.url}" target="_blank" rel="noopener">${T().ziureti}</a>
  </div></div>`;
        },

        rikKorteles() {
            const t = this.$refs.tinklas;
            if (t.dataset.pariszta) return;
            t.dataset.pariszta = '1';
            t.addEventListener('click', e => {
                const s = e.target.closest('[data-sirdis]');
                if (s) {                       // širdutė puslapio neatidaro
                    e.preventDefault(); e.stopPropagation();
                    s.classList.toggle('on');
                    return;
                }
                const c = e.target.closest('.fr-cipsas');
                if (c) {                       // čipsas atidaro savo adresą
                    e.preventDefault(); e.stopPropagation();
                    window.open(c.dataset.url, '_blank', 'noopener');
                    return;
                }
            });
            t.addEventListener('mouseover', e => {
                const k = e.target.closest('.fr-kort');
                if (k) this.ryskus(+k.dataset.id, true);
            });
            t.addEventListener('mouseout', e => {
                const k = e.target.closest('.fr-kort');
                if (k) this.ryskus(+k.dataset.id, false);
            });
        },

        ryskus(id, on) {
            const p = document.getElementById('frPin' + id);
            if (p) p.classList.toggle('act', on);
        },

        /** Kortelė pati yra nuoroda į /imone/<slug>/; čia liko tik žymeklio
         *  paryškinimas užvedus. */

        irasykURL() {
            if (!FR.zem) return;
            const c = FR.zem.getCenter();
            if (!c) return;
            const p = new URLSearchParams(location.search);
            p.delete('skrendam');
            // Google LatLng — lat()/lng() yra metodai, ne laukai
            p.set('lat', c.lat().toFixed(5)); p.set('lng', c.lng().toFixed(5));
            p.set('z', FR.zem.getZoom());
            history.replaceState(null, '', location.pathname + '?' + p.toString());
        },

        zenklas(kiek) {
            const f = T().imoniu;
            const d = kiek % 10, dd = kiek % 100;
            return (d === 0 || (dd >= 11 && dd <= 19)) ? f[2] : (d === 1 ? f[0] : f[1]);
        },
    };
}
