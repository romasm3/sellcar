/* ═══════════════════════════════════════════════════════════════════
   SKELBIMO NUOTRAUKŲ VALDYMAS — VIENA VIETA VISOMS KATEGORIJOMS

   Iki šiol kiekviena įkėlimo forma (28 šablonai) turėjo savo nusirašytą
   nuotraukų kodą. Todėl pataisa vienoje kategorijoje kitų nepasiekdavo:
   ◀ ▶ mygtukai atsirado tik automobiliuose, o pusėje formų iš viso
   nebuvo kaip pakeisti pagrindinės nuotraukos.

   Nuo šiol viskas čia. Forma prisijungia VIENA eilute:

       {% include 'listings/partials/_nuotrauku_valdymas.html' with
           tinklelis='#existing-photos' pk=listing.pk %}

   Ką duoda:
     • ◀ ▶ perstūmimas (telefone HTML5 tempimas nekyla visai);
     • pirmoji nuotrauka = pagrindinė, žalias ženklas ir numeracija;
     • trynimas su patvirtinimu;
     • nuoseklus įkėlimas po vieną su bendra eiga;
     • išėjimo sargas, kol siuntimas dar nebaigtas;
     • formos laukų išsaugojimas keičiant kalbą.

   Nieko nepiešia iš naujo: randa jau esamas miniatiūras ir papildo jas.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var T = (window.AL_NUOTRAUKU_TEKSTAI || {});
  function t(raktas, atsarginis) { return T[raktas] || atsarginis; }

  function csrf() {
    if (window.CSRF_TOKEN) return window.CSRF_TOKEN;
    var el = document.querySelector('input[name=csrfmiddlewaretoken]');
    return el ? el.value : '';
  }

  // ─────────────────────────────────────────────────────────────────
  // Konfigūracija iš šablono
  // ─────────────────────────────────────────────────────────────────
  function nustatymai() {
    var el = document.querySelector('[data-al-nuotraukos]');
    if (!el) return null;
    var d = el.dataset;
    return {
      tinklelis: d.tinklelis || '#existing-photos',
      pk: d.pk || '',
      ikelti: d.ikelti || '',
      pertvarkyti: d.pertvarkyti || '',
      trinti: d.trinti || '',
      pagrindine: d.pagrindine || '',
      perimtiIkelima: d.perimtiIkelima === '1',
      maks: parseInt(d.maks || '40', 10)
    };
  }

  var N = null;

  function kortos() {
    var t = document.querySelector(N.tinklelis);
    if (!t) return [];
    return Array.prototype.filter.call(
      t.children,
      function (el) { return el.nodeType === 1 && idIs(el); });
  }

  function idIs(el) {
    return el.dataset.imgId || el.dataset.existingImgId || el.dataset.id || '';
  }

  // ─────────────────────────────────────────────────────────────────
  // ◀ ▶ ir „PAGRINDINĖ"
  // ─────────────────────────────────────────────────────────────────
  function pridekMygtukus(el) {
    // Be pertvarkymo adreso mygtukų nededam: tvarka neišsisaugotų, o
    // mygtukas, kuris „veikia" tik iki perkrovimo, yra blogiau nei jo
    // nebuvimas.
    if (!N.pertvarkyti) return;
    if (el.querySelector('.foto-perstumti')) return;
    [['kaire', '◀', -1, t('kairen', 'Perkelti kairėn')],
     ['desine', '▶', 1, t('desinen', 'Perkelti dešinėn')]].forEach(function (m) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'foto-perstumti foto-perstumti-' + m[0];
      b.innerHTML = m[1];
      b.title = m[3];
      b.setAttribute('aria-label', m[3]);
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        e.preventDefault();
        perstumk(el, m[2]);
      });
      el.appendChild(b);
    });
  }

  function pridekTrynima(el) {
    if (!N.trinti || el.querySelector('.foto-trinti')) return;
    // Jei forma jau turi savo „×" — antro nededam.
    var savas = Array.prototype.some.call(
      el.querySelectorAll('button'),
      function (b) { return b.textContent.trim() === '×'; });
    if (savas) return;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'foto-trinti absolute top-1 right-1 w-6 h-6 bg-red-500 '
                + 'hover:bg-red-600 text-white rounded-full text-xs flex '
                + 'items-center justify-center z-10';
    b.textContent = '×';
    b.title = t('trinti', 'Ištrinti');
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      e.preventDefault();
      trink(el);
    });
    el.appendChild(b);
  }

  function perstumk(el, kryptis) {
    var tevas = el.parentNode;
    if (!tevas) return;
    var kaimynas = kryptis < 0 ? el.previousElementSibling : el.nextElementSibling;
    if (!kaimynas || !idIs(kaimynas)) return;
    if (kryptis < 0) tevas.insertBefore(el, kaimynas);
    else tevas.insertBefore(kaimynas, el);
    atnaujink();
    issaugokTvarka();
  }

  function atnaujink() {
    var sarasas = kortos();
    sarasas.forEach(function (el, idx) {
      pridekMygtukus(el);
      pridekTrynima(el);
      var k = el.querySelector('.foto-perstumti-kaire');
      var d = el.querySelector('.foto-perstumti-desine');
      if (k) k.disabled = (idx === 0);
      if (d) d.disabled = (idx === sarasas.length - 1);

      // Ženklas: pirmoji — pagrindinė, kitos — eilės numeris
      var senas = el.querySelector('.foto-zyme');
      if (senas) senas.remove();
      Array.prototype.forEach.call(
        el.querySelectorAll('.absolute.top-1.left-1'),
        function (b) { b.remove(); });
      var z = document.createElement('span');
      z.className = 'foto-zyme absolute top-1 left-1 text-white text-[10px] '
                  + 'rounded font-semibold pointer-events-none '
                  + (idx === 0 ? 'bg-green-600 px-2 py-0.5 shadow'
                               : 'bg-black/60 px-1.5 py-0.5');
      z.textContent = idx === 0 ? t('pagrindine', 'PAGRINDINĖ') : String(idx + 1);
      el.appendChild(z);

      el.classList.remove('border-green-500', 'border-gray-200');
      el.classList.add(idx === 0 ? 'border-green-500' : 'border-gray-200');
    });
    atnaujinkSkaitikli(sarasas.length);
  }

  function atnaujinkSkaitikli(kiek) {
    ['draft-photos-count', 'photos-count', 'existing-photos-count']
      .forEach(function (id) {
        var el = document.getElementById(id);
        if (el) el.textContent = '(' + kiek + ' / ' + N.maks + ')';
      });
  }

  function issaugokTvarka() {
    if (!N.pertvarkyti) return;
    var ids = kortos().map(function (el) { return parseInt(idIs(el), 10); });
    fetch(N.pertvarkyti, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ image_ids: ids })
    }).catch(function () {});
  }

  function trink(el) {
    if (!window.confirm(t('trintiKlausimas', 'Ištrinti šią nuotrauką?'))) return;
    var id = idIs(el);
    fetch(N.trinti.replace('0', id), {
      method: 'POST',
      headers: { 'X-CSRFToken': csrf() }
    }).then(function () {
      el.remove();
      atnaujink();
    }).catch(function () {});
  }

  // ─────────────────────────────────────────────────────────────────
  // Nuoseklus įkėlimas
  // ─────────────────────────────────────────────────────────────────
  var vyksta = 0;
  var sargasIdetas = false;

  function prasidejo() {
    vyksta++;
    if (sargasIdetas) return;
    sargasIdetas = true;
    try { history.pushState({ alIkelimas: true }, ''); } catch (e) {}
  }
  function baigesi() { vyksta = Math.max(0, vyksta - 1); }
  window.alIkelimuVyksta = function () { return vyksta; };

  window.addEventListener('beforeunload', function (e) {
    if (!vyksta) return;
    e.preventDefault();
    e.returnValue = '';
    return '';
  });

  window.addEventListener('popstate', function () {
    if (!vyksta) return;
    var likti = !window.confirm(
      t('iseiti', 'Turite dar nebaigtų keltis nuotraukų. Tikrai išeiti?'));
    if (likti) { try { history.pushState({ alIkelimas: true }, ''); } catch (e) {} }
  });

  function eiga(proc, uzrasas) {
    var d = document.getElementById('uploadProgress');
    if (d) d.classList.toggle('hidden', proc === null);
    var b = document.getElementById('uploadProgressBar');
    var p = document.getElementById('uploadProgressPercent');
    var l = document.getElementById('uploadProgressLabel');
    if (proc === null) return;
    if (b) b.style.width = proc + '%';
    if (p) p.textContent = proc + '%';
    if (l && uzrasas) l.textContent = uzrasas;
  }

  function siuskPoViena(failai) {
    var sarasas = Array.prototype.slice.call(failai).filter(function (f) {
      return f.type && f.type.indexOf('image/') === 0;
    });
    if (!sarasas.length || !N.ikelti) return;
    var viso = sarasas.length;
    var nepavyko = [];
    eiga(0, t('ruosiama', 'Ruošiamos nuotraukos...'));

    function viena(f, nr) {
      return new Promise(function (baigta) {
        prasidejo();
        var uzbaik = function () { baigesi(); baigta(); };
        var fd = new FormData();
        fd.append('images', f);
        fd.append('csrfmiddlewaretoken', csrf());
        var xhr = new XMLHttpRequest();
        xhr.open('POST', N.ikelti);
        xhr.setRequestHeader('X-CSRFToken', csrf());
        xhr.upload.onprogress = function (e) {
          if (!e.lengthComputable) return;
          var dalis = (nr + e.loaded / e.total) / viso;
          eiga(Math.round(dalis * 100),
               t('keliama', 'Keliamos nuotraukos...') + ' ' + (nr + 1) + ' / ' + viso);
        };
        xhr.onload = function () {
          var ok = false, duom = null;
          if (xhr.status >= 200 && xhr.status < 300) {
            try { duom = JSON.parse(xhr.responseText); ok = !!(duom && duom.success); }
            catch (err) { ok = false; }
          }
          if (ok && duom && duom.uploaded) pridekMiniatiuras(duom.uploaded);
          if (!ok) nepavyko.push(f.name || ('#' + (nr + 1)));
          uzbaik();
        };
        xhr.onerror = function () {
          nepavyko.push(f.name || ('#' + (nr + 1)));
          uzbaik();
        };
        xhr.send(fd);
      });
    }

    var eile = Promise.resolve();
    sarasas.forEach(function (f, nr) {
      eile = eile.then(function () { return viena(f, nr); });
    });
    eile.then(function () {
      eiga(null);
      if (nepavyko.length) {
        window.alert(t('nepavyko', 'Nepavyko įkelti') + ': ' + nepavyko.join(', '));
      }
    });
  }

  function pridekMiniatiuras(sarasas) {
    var tinkl = document.querySelector(N.tinklelis);
    if (!tinkl) return;
    var wrap = document.getElementById('draft-photos-wrapper')
            || document.getElementById('existing-photos-wrapper');
    if (wrap) wrap.style.display = '';
    sarasas.forEach(function (img) {
      var d = document.createElement('div');
      d.className = 'relative group aspect-square overflow-hidden rounded-lg '
                  + 'border-2 border-gray-200 bg-gray-100';
      d.dataset.imgId = img.id;
      var i = document.createElement('img');
      i.src = img.url;
      i.className = 'w-full h-full object-cover pointer-events-none';
      d.appendChild(i);
      tinkl.appendChild(d);
    });
    atnaujink();
  }

  // ─────────────────────────────────────────────────────────────────
  // Formos laukai išlieka perjungus kalbą
  //
  // Kalbos perjungimas yra POST į /i18n/setlang/ ir puslapio
  // perkrovimas nauju adresu — visa, kas įvesta ir dar neišsaugota,
  // dingdavo. Prieš perjungiant nusifotografuojam laukus, po
  // perkrovimo grąžinam TIK į tuščius (kad neperrašytume to, ką
  // serveris jau atstatė iš juodraščio).
  //
  // Įvestas turinys neverčiamas — persijungia tik sąsaja.
  // ─────────────────────────────────────────────────────────────────
  var RAKTAS = 'al_formos_bukle';

  function formosLaukai() {
    var f = document.querySelector('form[method="POST"], form[method="post"]');
    if (!f) return null;
    return f;
  }

  function nufotografuok() {
    var f = formosLaukai();
    if (!f) return;
    var b = {};
    Array.prototype.forEach.call(f.elements, function (el) {
      if (!el.name || el.name === 'csrfmiddlewaretoken') return;
      if (el.type === 'file' || el.type === 'password') return;
      if (el.type === 'checkbox' || el.type === 'radio') {
        if (el.checked) (b[el.name] = b[el.name] || []).push(el.value);
      } else if (el.value) {
        b[el.name] = el.value;
      }
    });
    try {
      sessionStorage.setItem(RAKTAS, JSON.stringify({
        kelias: location.pathname.replace(/^\/[a-z]{2}(-[a-z]+)?\//, '/'),
        laikas: Date.now(),
        laukai: b
      }));
    } catch (e) {}
  }

  function atstatyk() {
    var f = formosLaukai();
    if (!f) return;
    var g;
    try { g = JSON.parse(sessionStorage.getItem(RAKTAS) || 'null'); } catch (e) { return; }
    if (!g || !g.laukai) return;
    sessionStorage.removeItem(RAKTAS);
    // Tik tas pats puslapis (be kalbos priešdėlio) ir šviežia būklė
    var dabar = location.pathname.replace(/^\/[a-z]{2}(-[a-z]+)?\//, '/');
    if (g.kelias !== dabar) return;
    if (Date.now() - (g.laikas || 0) > 30 * 60 * 1000) return;

    Array.prototype.forEach.call(f.elements, function (el) {
      if (!el.name || !(el.name in g.laukai)) return;
      var v = g.laukai[el.name];
      if (el.type === 'checkbox' || el.type === 'radio') {
        if (Array.isArray(v) && v.indexOf(el.value) !== -1 && !el.checked) {
          el.checked = true;
          el.dispatchEvent(new Event('change', { bubbles: true }));
        }
      } else if (!el.value && typeof v === 'string') {
        el.value = v;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });
  }

  function sekLaKalbosPerjungima() {
    document.addEventListener('submit', function (e) {
      var f = e.target;
      if (f && f.action && f.action.indexOf('setlang') !== -1) nufotografuok();
    }, true);
    // Perjungiklis siunčia per mygtuko paspaudimą — pagaunam ir jį
    document.addEventListener('click', function (e) {
      var b = e.target.closest && e.target.closest('button[name=language]');
      if (b) nufotografuok();
    }, true);
  }

  // ─────────────────────────────────────────────────────────────────
  function paleisk() {
    sekLaKalbosPerjungima();
    atstatyk();

    N = nustatymai();
    if (!N) return;
    atnaujink();

    if (N.perimtiIkelima && N.ikelti) {
      var laukas = document.getElementById('imageInput');
      if (laukas) {
        // Formos savas tvarkytojas lieka, bet mūsų eina pirmas ir
        // sustabdo tolesnius — kitaip nuotraukos keliautų dukart.
        laukas.addEventListener('change', function (e) {
          e.stopImmediatePropagation();
          siuskPoViena(laukas.files);
          laukas.value = '';
        }, true);
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', paleisk);
  } else {
    paleisk();
  }
})();
