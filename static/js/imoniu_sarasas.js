/**
 * ĮMONIŲ SĄRAŠO puslapis: filtrų langas ir savas žemėlapis.
 *
 * Žemėlapis rodo TIK įmones (/imones/duomenys/) — skelbimų čia nėra.
 * Žymekliai piešiami bendru imoniuZymekliai(), tuo pačiu, kurį naudoja
 * žemėlapio paieška.
 */
function imoniuSarasas() {
    return {
        filtraiAtidaryti: false,
        zemelapis: false,
        _zem: null,
        _zymekliai: [],

        init() {
            this.$watch('zemelapis', v => { if (v) this.paruoskZemelapi(); });
        },

        paruoskZemelapi() {
            if (!window.google || !google.maps) {   // dar neįkelta — palaukiam
                setTimeout(() => this.paruoskZemelapi(), 300);
                return;
            }
            if (!this._zem) {
                this._zem = new google.maps.Map(this.$refs.zemelapis, {
                    center: { lat: 55.17, lng: 23.88 },
                    zoom: 7,
                    gestureHandling: 'greedy',
                    mapTypeControl: false,
                    streetViewControl: false,
                    fullscreenControl: false,
                });
                this._zem.addListener('idle', () => this.uzkrauk());
            }
            setTimeout(() => {
                google.maps.event.trigger(this._zem, 'resize');
                this.uzkrauk();
            }, 200);
        },

        uzkrauk() {
            const p = new URLSearchParams(location.search);
            const b = this._zem && this._zem.getBounds();
            if (b) {
                p.set('s', b.getSouthWest().lat()); p.set('n', b.getNorthEast().lat());
                p.set('v', b.getSouthWest().lng()); p.set('r', b.getNorthEast().lng());
            }
            fetch('/imones/duomenys/?' + p.toString(),
                  { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.ok ? r.json() : { imones: [] })
                .then(a => {
                    this._zymekliai = window.imoniuZymekliai(
                        this._zem, a.imones || [], this._zymekliai);
                })
                .catch(() => {});   // be žemėlapio sąrašas veikia toliau
        },
    };
}
