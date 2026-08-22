"""Paskutinės paieškos — sesijoje, kad veiktų ir neprisijungusiam.

Etalone „Mano paieškos" blokas turi du skirtukus: išsaugotos (reikia
paskyros) ir paskutinės. Antrosioms paskyros nereikia — jos gyvena
sesijoje ir dingsta kartu su ja.

Įrašom tik tada, kai paieška turi bent vieną prasmingą filtrą: kitaip
sąrašas prisipildytų tuščių „visi automobiliai" įrašų.
"""

RAKTAS = 'paskutines_paieskos'
KIEK = 6
NEREIKŠMINGI = {'sidebar', 'section', 'sekcija', 'vaizdas', 'sort', 'page', 'q'}


def _prasminga(params):
    return any(k not in NEREIKŠMINGI and v for k, v in params.items())


def irasyti(request, category, params, pavadinimas):
    """Įsimena paiešką sesijoje (naujausia — pirma, be dublikatų)."""
    if not _prasminga(params):
        return
    from urllib.parse import urlencode

    # doseq — kelios to paties lauko reikšmės (Benzinas IR Dyzelinas) turi
    # išlikti atskiromis poromis, kitaip adrese atsidurtų „['7', '8']"
    qs = urlencode({k: v for k, v in params.items() if v and k != 'sidebar'},
                   doseq=True)
    irasas = {'kategorija': category, 'params': qs, 'pavadinimas': pavadinimas}

    sarasas = [x for x in request.session.get(RAKTAS, []) if x.get('params') != qs]
    sarasas.insert(0, irasas)
    request.session[RAKTAS] = sarasas[:KIEK]
    request.session.modified = True


def sarasas(request):
    return request.session.get(RAKTAS, [])


def salinti(request, qs):
    """Išima vieną įrašą pagal jo parametrų eilutę."""
    request.session[RAKTAS] = [x for x in request.session.get(RAKTAS, [])
                               if x.get('params') != qs]
    request.session.modified = True


def isvalyti(request):
    request.session[RAKTAS] = []
    request.session.modified = True
