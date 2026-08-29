/**
 * ĮMONIŲ PUSLAPIS — maketas ir elgsena iš docs/demo/imones-fresha-1v1.html.
 *
 * Rodom TIK apps.imones objektus: /imones/duomenys/ grąžina ir korteles,
 * ir žymeklius, ir burbulus iš vieno įrašo. Skelbimų (Listing) čia nėra.
 *
 * Žemėlapis — Leaflet su CARTO voyager plytelėmis, kaip etalone.
 */
const FR = { zem: null, zymekliai: {}, duomenys: [], musuVieta: null };

/* ── Paieškos baras antraštėje ───────────────────────────────────── */
function freshaJuosta() {
    return {
        atidarytas: '', ko: '', koVeikla: '', vieta: '', vietosQ: '', kada: '',
        vietos: [], grupes: [],

        atidaryk(kuris) {
            this.atidarytas = (this.atidarytas === kuris) ? '' : kuris;
            if (this.atidarytas === 'ko') this.ieskok();
        },

        ieskok() {
            fetch('/ajax/paieska/?sritis=imoniu_puslapis&q=' + encodeURIComponent(this.ko))
                .then(r => r.ok ? r.json() : { grupes: [] })
                .then(a => { this.grupes = a.grupes || []; })
                .catch(() => { this.grupes = []; });
        },

        pasirink(e) {
            this.ko = e.vardas;
            // Paslauga filtruoja pagal veiklos sritį, įmonė — pagal vardą
            this.koVeikla = (e.url || '').includes('veikla=')
                ? e.url.split('veikla=')[1] : '';
            this.atidarytas = '';
        },

        ieskokVietos() {
            const q = this.vietosQ.trim();
            if (q.length < 3) { this.vietos = []; return; }
            fetch('/ajax/adresai/?q=' + encodeURIComponent(q))
                .then(r => r.ok ? r.json() : { siulymai: [] })
                .then(a => { this.vietos = a.siulymai || []; })
                .catch(() => { this.vietos = []; });
        },

        pasirinkVieta(v) {
            const vietove = ['city', 'town', 'village', 'district', 'locality', 'hamlet']
                .indexOf(v.tipas) !== -1;
            this.vieta = (vietove ? v.vardas : v.miestas) || v.vardas || v.tekstas;
            this.atidarytas = '';
        },

        dabartineVieta() {
            if (!navigator.geolocation) return;
            navigator.geolocation.getCurrentPosition(p => {
                fetch('/ajax/vieta/?lat=' + p.coords.latitude + '&lon=' + p.coords.longitude)
                    .then(r => r.ok ? r.json() : { vieta: {} })
                    .then(a => { this.vieta = (a.vieta || {}).miestas || ''; this.atidarytas = ''; })
                    .catch(() => { this.atidarytas = ''; });
            }, () => { this.atidarytas = ''; }, { timeout: 5000 });
        },

        kadosVardas() {
            const T = window.FR_TEKSTAI || {};
            if (!this.kada) return (T.siandien || 'Šiandien') + ' · ' + (T.betKada || 'Bet kada');
            const el = [...document.querySelectorAll('.fr-lst-eil.is-on span')][0];
            return el ? el.textContent.trim() : '';
        },

        paruosk() {
            const dek = (n, v) => { const e = this.$refs[n]; if (!e) return;
                e.value = v || ''; e.disabled = !v; };
            dek('pQ', this.koVeikla ? '' : this.ko.trim());
            dek('pVeikla', this.koVeikla);
            dek('pCity', this.vieta.trim());
            dek('pLaikas', this.kada);
        },
    };
}

/* ── Puslapis: sąrašas, datų juosta ir žemėlapis ─────────────────── */
function freshaPuslapis() {
    const T = () => window.FR_TEKSTAI || {};
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
            const t = T(), sh = t.dienos || ['Sk','Pr','An','Tr','Kt','Pn','Št'];
            let html = `<button class="on">${t.betKada || 'Bet kada'}</button>` +
                       `<button>${t.siandien || 'Šiandien'}</button>` +
                       `<button>${t.rytoj || 'Rytoj'}</button>`;
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

        /* ---- žemėlapis ---- */
        zemelapioParuosimas() {
            if (!window.L) { setTimeout(() => this.zemelapioParuosimas(), 200); return; }
            let pradine = { lat: 54.6872, lng: 25.2797, z: 12 };
            try { pradine = JSON.parse(document.getElementById('frPradine').textContent); }
            catch (e) {}
            FR.zem = L.map('frMap', { zoomControl: false, scrollWheelZoom: true,
                                      attributionControl: true })
                      .setView([pradine.lat, pradine.lng], pradine.z);
            // Etalone CARTO voyager, bet jis dabar reikalauja API rakto
            // („API KEY REQUIRED" ant plytelių), todėl imam tas pačias OSM
            // plyteles, kurias jau naudoja kūrimo formos žemėlapis.
            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                { maxZoom: 19, attribution: '&copy; OpenStreetMap' }).addTo(FR.zem);
            FR.zem.on('moveend', () => {
                if (this._pakrauta) this.pajudinta = true;
                this.irasykURL();
            });
            this.uzkrauk();
        },

        priartink(k) { if (FR.zem) FR.zem.setZoom(FR.zem.getZoom() + k); },

        visasEkranas() {
            const el = document.getElementById('frMap');
            if (!document.fullscreenElement) el.requestFullscreen && el.requestFullscreen();
            else document.exitFullscreen();
            setTimeout(() => FR.zem && FR.zem.invalidateSize(), 300);
        },

        perjunkZemelapi() {
            this.zemelapis = !this.zemelapis;
            if (this.zemelapis) setTimeout(() => FR.zem && FR.zem.invalidateSize(), 60);
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
                p.set('s', b.getSouth()); p.set('n', b.getNorth());
                p.set('v', b.getWest()); p.set('r', b.getEast());
            }
            fetch('/imones/duomenys/?' + p.toString(),
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
            FR.zem.flyToBounds(L.latLngBounds(su.map(c => [c.lat, c.lng])),
                               { padding: [60, 60], duration: .7 });
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
            Object.values(FR.zymekliai).forEach(m => FR.zem.removeLayer(m));
            FR.zymekliai = {};
            sarasas.forEach(c => {
                if (!c.lat || !c.lng) return;
                const ikona = L.divIcon({ className: '', iconSize: [0, 0],
                    html: `<div class="fr-pin" id="frPin${c.id}">${ZVAIGZDE}${(c.reitingas || 0).toFixed(1)}</div>` });
                const m = L.marker([c.lat, c.lng], { icon: ikona }).addTo(FR.zem);
                m.bindPopup(this.burbulas(c), { closeButton: true, offset: [0, -14] });
                m.on('click', () => this.pazymek(c.id, false));
                FR.zymekliai[c.id] = m;
            });
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
            const cipsai = (c.cipsai || []).map(s =>
                `<a class="fr-cipsas${s.ghost ? ' ghost' : ''}" href="${s.url}">${s.tekstas}</a>`).join('');
            return `
<article class="fr-kort" data-id="${c.id}">
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
  <div class="fr-tipas">${c.tipas}${c.atsiliepimai ? ' · ' + c.atsiliepimai + ' ' + (t.atsiliepimai || 'atsiliepimai') : ''}</div>
  <div class="fr-pasl">
    <div class="fr-pasl-eil"><div class="fr-pasl-vardas">${c.paslauga}</div>
      <div class="fr-pasl-kaina">${c.kaina}</div></div>
    <div class="fr-pasl-trukme">${c.trukme}</div>
    <div class="fr-cipsai">${cipsai}</div>
  </div>
</article>`;
        },

        burbulas(c) {
            const t = T();
            return `<div class="fr-pop">${c.img ? `<img src="${c.img}" alt="">` : ''}
  <div class="b"><div class="n">${c.vardas}</div>
  <div class="m">${ZVAIGZDE.replace('<svg', '<svg style="width:12px;height:12px;fill:#F5B301;vertical-align:-1px"')} ${(c.reitingas || 0).toFixed(1)} · ${c.atsiliepimai} ${t.atsiliepimai || 'atsiliepimai'}</div>
  <div class="m">${c.tipas} · ${c.vietove}</div>
  <div class="p">${c.paslauga} — ${c.kaina}</div></div></div>`;
        },

        rikKorteles() {
            const t = this.$refs.tinklas;
            if (t.dataset.pariszta) return;
            t.dataset.pariszta = '1';
            t.addEventListener('click', e => {
                const s = e.target.closest('[data-sirdis]');
                if (s) { e.stopPropagation(); s.classList.toggle('on'); return; }
                if (e.target.closest('.fr-cipsas')) return;      // čipsas — nuoroda
                const k = e.target.closest('.fr-kort');
                if (k) this.pazymek(+k.dataset.id, true);
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

        /** Paspaudus kortelę — nuskrendam (zoom 15) ir atidarom burbulą. */
        pazymek(id, atidaryti) {
            FR.duomenys.forEach(c => this.ryskus(c.id, false));
            this.ryskus(id, true);
            const c = FR.duomenys.find(x => x.id === id);
            if (!c || !FR.zem) return;
            FR.zem.flyTo([c.lat, c.lng], 15, { duration: .6 });
            if (atidaryti) setTimeout(() => FR.zymekliai[id] && FR.zymekliai[id].openPopup(), 320);
        },

        irasykURL() {
            if (!FR.zem) return;
            const c = FR.zem.getCenter();
            const p = new URLSearchParams(location.search);
            p.delete('skrendam');
            p.set('lat', c.lat.toFixed(5)); p.set('lng', c.lng.toFixed(5));
            p.set('z', FR.zem.getZoom());
            history.replaceState(null, '', location.pathname + '?' + p.toString());
        },

        zenklas(kiek) {
            const f = (T().imoniu) || ['įmonė', 'įmonės', 'įmonių'];
            const d = kiek % 10, dd = kiek % 100;
            return (d === 0 || (dd >= 11 && dd <= 19)) ? f[2] : (d === 1 ? f[0] : f[1]);
        },
    };
}
