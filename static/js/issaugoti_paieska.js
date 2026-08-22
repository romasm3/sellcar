/* „Išsaugoti paiešką" jungiklis + trumpas pranešimas (toast).
 *
 * Mygtukas: [data-issaugoti]. Filtrus imam iš adreso (location.search) —
 * tai tiksliai ta paieška, kurią žmogus mato ekrane, nesvarbu, ar ji atėjo
 * iš panelės, iš šoninės juostos, ar iš nuorodos.
 *
 * Serveris grąžina naują būseną ir skaitiklius, todėl antraštės žymė
 * atsinaujina be perkrovimo ([data-nauju-skaitiklis]).
 */
(function () {
    'use strict';

    var T = {
        issaugota: 'Paieška išsaugota. Pranešime, kai atsiras naujų skelbimų.',
        pasalinta: 'Paieška pašalinta.',
        nuoroda: 'Mano paieškos →',
        klaida: 'Nepavyko išsaugoti paieškos. Bandykite dar kartą.'
    };

    function csrf() {
        var m = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
        return m ? decodeURIComponent(m[1]) : '';
    }

    function pranesimas(tekstas, rusis) {
        var senas = document.getElementById('ip-toast');
        if (senas) { senas.remove(); }

        var t = document.createElement('div');
        t.id = 'ip-toast';
        t.className = 'ip-toast' + (rusis === 'klaida' ? ' is-klaida' : '');
        t.setAttribute('role', 'status');

        var sp = document.createElement('span');
        sp.textContent = tekstas;
        t.appendChild(sp);

        if (rusis !== 'klaida') {
            var a = document.createElement('a');
            a.href = '/searches/';
            a.textContent = T.nuoroda;
            t.appendChild(a);
        }

        document.body.appendChild(t);
        requestAnimationFrame(function () { t.classList.add('is-matomas'); });
        setTimeout(function () {
            t.classList.remove('is-matomas');
            setTimeout(function () { t.remove(); }, 250);
        }, 3000);
    }

    function atnaujintiSkaitiklius(nauju) {
        document.querySelectorAll('[data-nauju-skaitiklis]').forEach(function (el) {
            el.textContent = nauju;
            el.style.display = nauju > 0 ? '' : 'none';
        });
    }

    function perpiesti(btn, issaugota) {
        btn.classList.toggle('is-on', issaugota);
        btn.setAttribute('aria-pressed', issaugota ? 'true' : 'false');
        var tekstas = btn.querySelector('.ip-tekstas');
        if (tekstas) {
            tekstas.textContent = issaugota
                ? (btn.dataset.tekstasIssaugota || 'Paieška išsaugota')
                : (btn.dataset.tekstasIssaugoti || 'Išsaugoti paiešką');
        }
    }

    document.addEventListener('click', function (e) {
        var btn = e.target.closest('[data-issaugoti]');
        if (!btn) { return; }
        e.preventDefault();
        if (btn.disabled) { return; }
        btn.disabled = true;

        var kunas = new URLSearchParams(location.search);
        kunas.set('grizti', location.pathname + location.search);

        fetch('/search/toggle-save/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf(),
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: kunas.toString()
        }).then(function (r) {
            return r.json().then(function (d) { return { statusas: r.status, d: d }; });
        }).then(function (res) {
            btn.disabled = false;
            // Neprisijungęs — į prisijungimą, po jo paieška išsaugoma pati
            if (res.statusas === 401 && res.d.login_url) {
                window.location = res.d.login_url;
                return;
            }
            if (!res.d.ok) {
                pranesimas(res.d.klaida || T.klaida, 'klaida');
                return;
            }
            perpiesti(btn, res.d.issaugota);
            atnaujintiSkaitiklius(res.d.nauju);
            pranesimas(res.d.issaugota ? T.issaugota : T.pasalinta);
        }).catch(function () {
            btn.disabled = false;
            pranesimas(T.klaida, 'klaida');
        });
    });
})();
