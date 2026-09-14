/* KAINOS VALIUTA — VISADA EURAI.
 *
 * Anksčiau šis failas sufiksą ir paslėptą <input name="currency"> sekė
 * pagal pasirinktą šalį: Lenkija → „zł", Švedija → „kr", Šveicarija →
 * „CHF". Skaičius NEBUVO konvertuojamas, tad įvesti 43 000 € virsdavo
 * „43 000 zł" (≈10 000 €). Taip nukentėjo #789, #791, #792, #798, #799.
 *
 * Kursų svetainė neturi, tad vienintelis teisingas elgesys — nieko
 * nekeisti. Daugiavaliutės (GBP/USD) bus atskiras darbas kartu su kursais.
 *
 * Ką daro dabar:
 *   • kiekvienam [data-valiutos-sufiksas] įrašo „€";
 *   • paslėptam <input name="currency"> — „EUR";
 *   • šalies lauko nebeklauso.
 *
 * Išvaizdos nekeičia: tas pats elementas, tik ženklas jame nebekinta.
 */
(function () {
  'use strict';

  var Z = window.AL_VALIUTOS || {};
  var NUMATYTA = Z.numatyta || 'EUR';
  var ZENKLAS = (Z.simboliai || {})[NUMATYTA] || '€';

  function paleisk() {
    var i;
    var sufiksai = document.querySelectorAll('[data-valiutos-sufiksas]');
    for (i = 0; i < sufiksai.length; i++) sufiksai[i].textContent = ZENKLAS;

    var laukai = document.querySelectorAll('input[name="currency"]');
    for (i = 0; i < laukai.length; i++) laukai[i].value = NUMATYTA;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', paleisk);
  } else {
    paleisk();
  }
})();
