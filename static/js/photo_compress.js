/* ═══════════════════════════════════════════════════════════
 * Bendras nuotraukų suspaudimas kliento pusėje.
 *
 * Telefono 10 MB kadras suspaudžiamas iki ~400 KB dar prieš siuntimą:
 * serveris priima iki 20 MB (image_validation.MAX_IMAGE_SIZE), todėl be
 * šito dalis vartotojų gaudavo „per didelis failas" ten, kur forma
 * suspaudimo neturėjo.
 *
 * Iki šiol ta pati funkcija buvo nukopijuota šešiuose šablonuose, o
 * kitose šešiose jos nebuvo visai.
 * ═══════════════════════════════════════════════════════════ */
(function (global) {
    'use strict';

    var MAX_DIM = 1920;
    var QUALITY = 0.85;
    var SKIP_BELOW = 600 * 1024;   // mažų failų neliečiam

    function compressImage(file) {
        return new Promise(function (resolve) {
            if (!file || file.type === 'image/gif' || file.size < SKIP_BELOW) {
                resolve(file);
                return;
            }
            var reader = new FileReader();
            reader.onload = function (e) {
                var img = new Image();
                img.onload = function () {
                    var w = img.width, h = img.height;
                    if (w > MAX_DIM || h > MAX_DIM) {
                        if (w > h) { h = Math.round(h * MAX_DIM / w); w = MAX_DIM; }
                        else { w = Math.round(w * MAX_DIM / h); h = MAX_DIM; }
                    }
                    var canvas = document.createElement('canvas');
                    canvas.width = w; canvas.height = h;
                    canvas.getContext('2d').drawImage(img, 0, 0, w, h);
                    canvas.toBlob(function (blob) {
                        // Jei suspaudimas nieko nelaimėjo — siunčiam originalą
                        if (!blob || blob.size >= file.size) { resolve(file); return; }
                        var name = file.name.replace(/\.[^.]+$/, '') + '.jpg';
                        resolve(new File([blob], name, { type: 'image/jpeg' }));
                    }, 'image/jpeg', QUALITY);
                };
                img.onerror = function () { resolve(file); };
                img.src = e.target.result;
            };
            reader.onerror = function () { resolve(file); };
            reader.readAsDataURL(file);
        });
    }

    function compressAll(files) {
        return Promise.all(Array.prototype.map.call(files, compressImage));
    }

    global.compressImage = compressImage;
    global.compressAll = compressAll;
})(window);
