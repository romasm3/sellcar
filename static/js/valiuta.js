/* KAINOS VALIUTA SEKA ŠALĮ.
 *
 * Žemėlapis vienas visai svetainei — apps/listings/valiutos.py; į
 * naršyklę jis ateina per `{% valiutu_zemelapis_json %}` (base.html).
 * Iki šiol formos rodydavo „€", o siųsdavo paslėptą „USD", todėl
 * vokiškas ar kroatiškas skelbimas paskui rodydavo „$".
 *
 * Ką daro:
 *   • kiekvienam [data-valiutos-sufiksas] įrašo tos šalies simbolį;
 *   • paslėptam <input name="currency"> — valiutos kodą;
 *   • persijungia iškart, kai pasikeičia šalies laukas.
 *
 * Išvaizdos nekeičia: tas pats elementas, tik kitas ženklas jame.
 */
(function () {
  'use strict';

  var Z = window.AL_VALIUTOS || {};
  var SALYS = Z.salys || {};
  var SIMBOLIAI = Z.simboliai || { EUR: '€' };
  var NUMATYTA = Z.numatyta || 'EUR';

  function kodas(salis) {
    return SALYS[(salis || '').toUpperCase()] || NUMATYTA;
  }
  function simbolis(salis) {
    return SIMBOLIAI[kodas(salis)] || SIMBOLIAI[NUMATYTA] || '€';
  }

  function salies_laukas() {
    return document.getElementById('id_country')
        || document.querySelector('[name="country"]');
  }

  function atnaujink() {
    var laukas = salies_laukas();
    var salis = laukas ? laukas.value : '';
    var zenklas = simbolis(salis);
    var i;

    var sufiksai = document.querySelectorAll('[data-valiutos-sufiksas]');
    for (i = 0; i < sufiksai.length; i++) sufiksai[i].textContent = zenklas;

    var laukai = document.querySelectorAll('input[name="currency"]');
    for (i = 0; i < laukai.length; i++) laukai[i].value = kodas(salis);
  }

  function paleisk() {
    if (!document.querySelector('[data-valiutos-sufiksas], input[name="currency"]')) {
      return;                       // puslapyje kainos formos nėra
    }
    atnaujink();
    var laukas = salies_laukas();
    if (laukas) laukas.addEventListener('change', atnaujink);
    // Kontaktų blokas šalį keičia ir programiškai (contact_block.js)
    document.addEventListener('al:salis-pakeista', atnaujink);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', paleisk);
  } else {
    paleisk();
  }
})();
