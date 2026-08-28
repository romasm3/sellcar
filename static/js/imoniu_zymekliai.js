/**
 * ĮMONIŲ ŽYMEKLIAI — bendri žemėlapio paieškai ir įmonių puslapiui.
 *
 * Google Marker ikona yra vienas paveikslėlis, todėl logotipo į ją
 * neįdėsi — naudojam OverlayView su tikru HTML (baltas burbulas su
 * logotipu, vardu ir skelbimų skaičiumi).
 *
 * Naudojimas:
 *     const nauji = imoniuZymekliai(zemelapis, sarasas, seni);
 * `seni` — ankstesnis masyvas, jis nuimamas nuo žemėlapio.
 */
(function () {
    'use strict';

    let Klase = null;

    function klase() {
        if (Klase) return Klase;
        Klase = class ImonesZymeklis extends google.maps.OverlayView {
            constructor(duom) { super(); this.d = duom; this.el = null; }
            onAdd() {
                const e = document.createElement('a');
                e.className = 'zp-imone';
                e.href = this.d.url;
                e.target = '_blank';
                e.rel = 'noopener';
                e.title = this.d.vardas;
                const logo = this.d.logo
                    ? '<img src="' + this.d.logo + '" alt="">'
                    : '<span class="zp-imone-raide">' + (this.d.vardas || '?')[0] + '</span>';
                const kiek = this.d.kiek ? '<em>' + this.d.kiek + '</em>' : '';
                e.innerHTML = logo + '<span>' + this.d.vardas + '</span>' + kiek;
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
        };
        return Klase;
    }

    window.imoniuZymekliai = function (zemelapis, sarasas, seni) {
        (seni || []).forEach(o => o.setMap(null));
        if (!zemelapis || !sarasas || !sarasas.length) return [];
        if (!window.google || !google.maps.OverlayView) return [];
        const K = klase();
        return sarasas.map(i => {
            const o = new K(i);
            o.setMap(zemelapis);
            return o;
        });
    };
})();
