/* Multiselect lauko antraštė — „Visi" arba pasirinktų reikšmių sąrašas.
 *
 * Naudoja templates/listings/partials/field_multiselect.html. Laikoma
 * atskirai, kad tas pats elgesys galiotų ir greitosiose panelėse, ir
 * detalioje paieškoje (kaip etalone).
 */
window.msTitle = function (root, allLabel) {
    if (!root) { return allLabel; }
    var checked = root.querySelectorAll('input[type="checkbox"]:checked');
    if (!checked.length) { return allLabel; }
    var labels = Array.prototype.map.call(checked, function (i) {
        return i.dataset.label || i.value;
    });
    return labels.join(', ');
};
