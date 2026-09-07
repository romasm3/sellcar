/* ═══════════════════════════════════════════════════════════════════
   SKELBIMO NUOTRAUKŲ VALDYMAS — VIENA VIETA VISOMS KATEGORIJOMS

   Iki šiol kiekviena įkėlimo forma (28 šablonai) turėjo savo nusirašytą
   nuotraukų kodą. Todėl pataisa vienoje kategorijoje kitų nepasiekdavo:
   ◀ ▶ mygtukai atsirado tik automobiliuose, o pusėje formų iš viso
   nebuvo kaip pakeisti pagrindinės nuotraukos.

   Nuo šiol VISA elgsena čia. Forma prisijungia viena eilute:

       {% include 'listings/partials/_nuotrauku_valdymas.html' with
           tinklelis='#draft-photos' pertvarkyti='/ajax/...' %}

   Ką duoda:
     • ◀ ▶ perstūmimas (telefone HTML5 tempimas nekyla visai);
     • pirmoji nuotrauka = pagrindinė, žalias ženklas ir numeracija;
     • trynimas su patvirtinimu (jei forma savo „×" neturi);
     • nuoseklus įkėlimas po vieną su bendra eiga;
     • išėjimo sargas, kol siuntimas dar nebaigtas;
     • formos laukų išsaugojimas keičiant kalbą.

   DVI PRIJUNGIMO PAKOPOS. Kategorijos skiriasi ne elgsena, o tuo, KUR
   nuotraukos gyvena (juodraštis serveryje ar naršyklėje) ir ko reikia
   jų adresams (draft_id, listing_id, išankstinis juodraščio įrašymas).
   Todėl:

     1. Paprastoms formoms užtenka adresų — `data-pertvarkyti`,
        `data-trinti`, `data-ikelti`.
     2. Toms, kurios turi savo išsaugojimo tvarką, paduodam KABLĮ —
        `data-tvarkos-kablys="saveOrder"`. Perstūmimą piešiam mes,
        įrašo forma savo funkcija. Taip nedubliuojam nei mygtukų, nei
        adresų logikos.

   Nuoseklų siuntimą formos gali pasiimti ir tiesiogiai:

       ALNuotraukos.siuskPoViena(failai, {url: ..., laukai: {...},
                                          ikelta: fn, baigta: fn});

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

  function kablys(vardas) {
    return (vardas && typeof window[vardas] === 'function') ? window[vardas] : null;
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
      kortele: d.kortele || '',
      pk: d.pk || '',
      ikelti: d.ikelti || '',
      laukai: d.laukai || '',
      pertvarkyti: d.pertvarkyti || '',
      tvarkosLaukai: d.tvarkosLaukai || '',
      tvarkosKablys: d.tvarkosKablys || '',
      trinti: d.trinti || '',
      ivestis: d.ivestis || '#imageInput',
      perimtiIkelima: d.perimtiIkelima === '1',
      vietinis: d.vietinis === '1',
      maks: parseInt(d.maks || '40', 10)
    };
  }

  var N = null;

  function tinklas() { return document.querySelector(N.tinklelis); }

  function kortos() {
    var t = tinklas();
    if (!t) return [];
    if (N.kortele) {
      return Array.prototype.slice.call(t.querySelectorAll(N.kortele));
    }
    return Array.prototype.filter.call(
      t.children,
      function (el) { return el.nodeType === 1 && (N.vietinis || idIs(el)); });
  }

  function idIs(el) {
    var d = el.dataset || {};
    return d.imgId || d.existingImgId || d.imageId || d.id || '';
  }

  // ─────────────────────────────────────────────────────────────────
  // ◀ ▶ ir „PAGRINDINĖ"
  // ─────────────────────────────────────────────────────────────────
  function galimaPertvarkyti() {
    return !!(N.pertvarkyti || N.tvarkosKablys || N.vietinis);
  }

  function pridekMygtukus(el) {
    // Be išsaugojimo būdo mygtukų nededam: tvarka neišliktų, o mygtukas,
    // kuris „veikia" tik iki perkrovimo, yra blogiau nei jo nebuvimas.
    if (!galimaPertvarkyti()) return;
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
      // Tempiamose kortelėse (trucks) mygtukas be to pradėtų vilkimą.
      b.draggable = false;
      b.addEventListener('dragstart', function (e) { e.preventDefault(); });
      el.appendChild(b);
    });
  }

  var SAVO_TRYNIMAS = '.foto-trinti, .photo-action-btn.delete, .photo-delete, '
                    + '.delete-photo, [data-trinti], [data-delete]';

  function turiSavaTrynima(el) {
    if (el.querySelector(SAVO_TRYNIMAS)) return true;
    return Array.prototype.some.call(
      el.querySelectorAll('button, a'),
      function (b) {
        var v = (b.textContent || '').trim();
        return v === '×' || v === '✕' || v === '✖'
            || /delete|remove|trin/i.test(b.getAttribute('onclick') || '');
      });
  }

  function pridekTrynima(el) {
    if (!N.trinti || turiSavaTrynima(el)) return;
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
    var sarasas = kortos();
    var vieta = sarasas.indexOf(el);
    var nauja = vieta + kryptis;
    if (vieta < 0 || nauja < 0 || nauja >= sarasas.length) return;

    // Vietinis režimas (ratlankiai, padangos, ratai): nuotraukos dar
    // naršyklėje, tad tvarką keičia pati forma — mes tik pasakom, ką.
    if (N.vietinis) {
      var f = kablys(N.tvarkosKablys);
      if (f) f(vieta, nauja);
      setTimeout(atnaujink, 0);
      return;
    }

    var kaimynas = sarasas[nauja];
    var tevas = el.parentNode;
    if (!tevas || !kaimynas) return;
    if (kryptis < 0) tevas.insertBefore(el, kaimynas);
    else tevas.insertBefore(kaimynas, el);
    atnaujink();
    issaugokTvarka();
  }

  function pozicija(el) {
    // Ženklas dedamas absoliučiai — kortelė privalo būti atskaitos taškas.
    var s = window.getComputedStyle(el);
    if (s && s.position === 'static') el.style.position = 'relative';
  }

  function atnaujink() {
    if (!N) return;
    var sarasas = kortos();
    sarasas.forEach(function (el, idx) {
      pozicija(el);
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
      z.className = 'foto-zyme' + (idx === 0 ? ' foto-zyme-pagrindine' : '');
      z.textContent = idx === 0 ? t('pagrindine', 'PAGRINDINĖ') : String(idx + 1);
      el.appendChild(z);

      // Formos su savo „MAIN" ženklu (sunkvežimiai) — nuosekliai
      if (el.classList.contains('photo-item')) {
        el.classList.toggle('is-main', idx === 0);
      }
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

  function poros(tekstas) {
    // „a=1;b=@#laukas" → {a: '1', b: <lauko reikšmė siuntimo metu>}
    var out = {};
    (tekstas || '').split(';').forEach(function (d) {
      if (!d) return;
      var i = d.indexOf('=');
      if (i < 1) return;
      var raktas = d.slice(0, i).trim();
      var v = d.slice(i + 1).trim();
      if (v.charAt(0) === '@') {
        var el = document.querySelector(v.slice(1));
        v = el ? (el.value || '') : '';
      }
      out[raktas] = v;
    });
    return out;
  }

  function issaugokTvarka() {
    var f = kablys(N.tvarkosKablys);
    if (f) { f(); return; }
    if (!N.pertvarkyti) return;
    var kunas = { image_ids: kortos().map(function (el) {
      return parseInt(idIs(el), 10);
    }) };
    var papildomi = poros(N.tvarkosLaukai);
    Object.keys(papildomi).forEach(function (r) { kunas[r] = papildomi[r]; });
    fetch(N.pertvarkyti, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify(kunas)
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

  /* Siunčia PO VIENĄ. Kodėl ne visas iš karto: telefono ryšiu vienas
     didelis siuntinys arba pavyksta, arba krenta visas — o žmogus mato
     tik „Upload failed". Po vieną matosi eiga, o nepavykusią galima
     įvardyti. Formos šitą kviečia ir tiesiogiai — savo adresu ir savo
     laukais. */
  function siuskPoViena(failai, p) {
    p = p || {};
    var sarasas = Array.prototype.slice.call(failai).filter(function (f) {
      return f.type && f.type.indexOf('image/') === 0;
    });
    var url = p.url || (N && N.ikelti) || '';
    if (!sarasas.length || !url) return Promise.resolve([]);
    var viso = sarasas.length;
    var nepavyko = [];
    var rodyk = p.eiga || eiga;
    rodyk(0, t('ruosiama', 'Ruošiamos nuotraukos...'));

    function viena(f, nr) {
      return new Promise(function (baigta) {
        prasidejo();
        var uzbaik = function () { baigesi(); baigta(); };
        var fd = new FormData();
        fd.append('images', f);
        fd.append('csrfmiddlewaretoken', csrf());
        // Laukai gali priklausyti nuo ankstesnio atsakymo (juodraščio id
        // gimsta prie pirmos nuotraukos), tad leidžiam ir funkciją.
        var papildomi = (typeof p.laukai === 'function') ? p.laukai()
                      : (p.laukai || poros(N ? N.laukai : ''));
        Object.keys(papildomi).forEach(function (r) {
          if (papildomi[r] !== '' && papildomi[r] != null) fd.append(r, papildomi[r]);
        });
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url);
        xhr.setRequestHeader('X-CSRFToken', csrf());
        xhr.upload.onprogress = function (e) {
          if (!e.lengthComputable) return;
          var dalis = (nr + e.loaded / e.total) / viso;
          rodyk(Math.round(dalis * 100),
                t('keliama', 'Keliamos nuotraukos...') + ' ' + (nr + 1) + ' / ' + viso);
        };
        xhr.onload = function () {
          var ok = false, duom = null;
          if (xhr.status >= 200 && xhr.status < 300) {
            try { duom = JSON.parse(xhr.responseText); ok = !!(duom && duom.success); }
            catch (err) { ok = false; }
          }
          if (ok && duom) {
            if (p.ikelta) p.ikelta(duom);
            else if (duom.uploaded) pridekMiniatiuras(duom.uploaded);
          }
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
    return eile.then(function () {
      rodyk(null);
      if (nepavyko.length) {
        window.alert(t('nepavyko', 'Nepavyko įkelti') + ': ' + nepavyko.join(', '));
      }
      if (p.baigta) p.baigta(nepavyko);
      return nepavyko;
    });
  }

  function pridekMiniatiuras(sarasas) {
    var tinkl = tinklas();
    if (!tinkl) return;
    var wrap = document.getElementById('draft-photos-wrapper')
            || document.getElementById('existing-photos-wrapper')
            || document.getElementById('photo-preview-wrapper');
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
  function perimkIkelima() {
    if (!N.perimtiIkelima || !N.ikelti) return;
    var laukas = document.querySelector(N.ivestis);
    if (!laukas) return;
    // Klausom PRIE DOKUMENTO, gaudymo fazėje: taip mūsų tvarkytojas
    // suveikia anksčiau už bet kurį formos savą, nesvarbu, kada tas
    // buvo prikabintas. Su registracijos eile lenktyniauti negalima —
    // nuotraukos keliautų dukart.
    document.addEventListener('change', function (e) {
      if (e.target !== laukas) return;
      e.stopImmediatePropagation();
      siuskPoViena(laukas.files);
      laukas.value = '';
    }, true);
  }

  function paleisk() {
    sekLaKalbosPerjungima();
    atstatyk();

    N = nustatymai();
    if (!N) return;
    atnaujink();
    perimkIkelima();

    // Formos, kurios miniatiūras piešia pačios, po perpiešimo kviečia
    // ALNuotraukos.atnaujink() — kad ženklai ir ◀ ▶ grįžtų.
    var tinkl = tinklas();
    if (tinkl && window.MutationObserver) {
      var laukia = false;
      new MutationObserver(function () {
        if (laukia) return;
        laukia = true;
        setTimeout(function () { laukia = false; atnaujink(); }, 60);
      }).observe(tinkl, { childList: true });
    }
  }

  window.ALNuotraukos = {
    atnaujink: function () { if (N) atnaujink(); },
    siuskPoViena: siuskPoViena,
    eiga: eiga,
    vyksta: function () { return vyksta; }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', paleisk);
  } else {
    paleisk();
  }
})();
