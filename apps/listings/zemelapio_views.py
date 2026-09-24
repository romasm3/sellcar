# -*- coding: utf-8 -*-
"""
ŽEMĖLAPIO PAIEŠKA — /map/ ir jos duomenų galas.

Maketas kaip Fresha: kairėje rezultatai dviem stulpeliais, dešinėje
prilipęs žemėlapis. Sąrašas persirenka pagal MATOMĄ žemėlapio plotą,
todėl duomenys imami per atskirą galą (/map/duomenys/): jam paduodam
kraštines (šiaurė/pietūs/rytai/vakarai), o jis grąžina korteles ir jų
skaičių.

Kortelė ta pati kaip rezultatų puslapyje (partials/_skelbimo_kortele.html
per korteles.py) — atskiros kopijos nėra.
"""

import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from . import formatai
from .korteles import kortele
from .models import Listing, SavedListing

SIMBOLIAI = {'EUR': '€', 'USD': '$', 'GBP': '£'}

MAKS_KORTELIU = 60          # kiek kortelių rodom sąraše vienu metu
MAKS_ZYMEKLIU = 2000        # kiek taškų siunčiam žemėlapiui


def _filtruoti(request, qs=None):
    """Filtrai — TAS PATS kelias kaip rezultatų puslapyje ir detalioje
    paieškoje: search_params.sanitize + views.filter_listings. Ketvirtos
    kopijos nėra, todėl „Benzinas" čia ir ten reiškia tą patį."""
    from .views import filter_listings
    from .search_params import sanitize as sanitize_search_params
    parametrai = sanitize_search_params(request.GET)
    return filter_listings(parametrai, user=request.user,
                           category=parametrai.get('category') or None,
                           base_qs=qs if qs is not None else _su_koordinatemis(request.user))


def _su_koordinatemis(user):
    from .views import _public_listings_qs
    return _public_listings_qs(user).exclude(latitude=None).exclude(longitude=None)


# ═══════════════════════════════════════════════════════════════════
# KATEGORIJOS
#
# Sąrašas NERAŠOMAS ranka — jis išvedamas iš tos pačios struktūros,
# kuri piešia ikonų juostą ir pikerį (panels.ADVANCED_RAIL +
# ADVANCED_RAIL_CHILDREN + ADVANCED_RAIL_MORE). Atsiradus naujai
# kategorijai juostoje, ji pati atsiras ir čia.
#
# Dvi kategorijų šeimos gyvena ne `Listing` lentelėje:
#   • ratlankiai ir padangos — WheelListing (turi latitude/longitude);
#   • motoapranga — Listing su motociklų VT ir aprangos subkategorija.
# Abi filtruojamos kartu su visomis kitomis.
#
# Dalys lieka VIENAS punktas („Dalys"), nors juostoje jos skyla į auto/
# moto/sunkiojo. Skaidymas eina ne per filter_listings, o per atskirą
# parts_count_qs kelią; kartoti jį čia reikštų dar vieną filtrų kopiją.
# ═══════════════════════════════════════════════════════════════════

RATU_KATEGORIJOS = {
    'rims':       {'product_type': 'rim'},
    'tyres':      {'product_type': 'tyre'},
    'moto-tyres': {'product_type': 'tyre', 'purpose': 'moto'},
    'quad-tyres': {'product_type': 'tyre', 'purpose': 'quad'},
}

# Juostoje „Padangos" (po „Ratai") ir „Padangos motociklams" (po
# „Motociklai") yra atskiri punktai ir tas pats skelbimas skaičiuojamas
# abiejuose. Filtrų sąraše punktai turi nepersidengti — kitaip suma
# nesutampa su „N skelbimų šioje srityje", todėl bendros padangos
# rodomos be motociklų ir keturračių.
RATU_ISSKYRUS = {'tyres': {'purpose__in': ('moto', 'quad')}}

# Filtrai, kurių ratlankiai ir padangos neturi (metai, rida, kuras...).
# Jei toks filtras įjungtas, ratų šeima į rezultatus nepatenka — padanga
# neturi nei pagaminimo metų, nei ridos.
RATAMS_NETINKA = ('brand', 'truck_brand', 'motorcycle_brand', 'model',
                  'year_min', 'year_max', 'mileage_min', 'mileage_max',
                  'fuel_type', 'transmission', 'has_vin', 'feat_warranty',
                  'country_filter')


def kategoriju_medis():
    """[(slug, vardas)] — juostos lapai ta pačia tvarka.

    Vardas — pilnas („Automobiliai"), iš panelių konfigūracijos; juostos
    etiketės sutrumpintos ikonoms („Auto"), sąrašui jos netinka.
    """
    from .search_config import panels as P
    from .views import _kategorijos_vardas

    def _vardas(slug, atsarginis):
        return (_kategorijos_vardas(slug) if slug in P.PANELS
                else str(atsarginis))

    eiles = []
    for slug, label, _key in P.ADVANCED_RAIL:
        vaikai = P.ADVANCED_RAIL_CHILDREN.get(slug)
        if not vaikai:
            eiles.append((slug, _vardas(slug, label)))
            continue
        for vslug, vlabel in vaikai:
            # Dalių skaidymo nekartojam (žr. komentarą viršuje)
            if vslug in ('moto-parts', 'truck-parts'):
                continue
            eiles.append((vslug, _vardas(vslug, vlabel)))
    for slug in P.ADVANCED_RAIL_MORE:
        cfg = P.build_advanced(slug, None)
        eiles.append((slug, _vardas(slug, cfg['label'] if cfg else slug)))
    return eiles


def _motoaprangos_qs(user):
    from . import motogear_views
    return (motogear_views._moto_gear_public_qs(user)
            .exclude(latitude=None).exclude(longitude=None))


def _ratu_qs(request, kat=None):
    """WheelListing su koordinatėmis; None — kai filtrai ratams netinka."""
    from .models import WheelListing

    for raktas in RATAMS_NETINKA:
        if request.GET.get(raktas):
            return None

    qs = (WheelListing.objects.filter(status='active', is_shadow_banned=False)
          .exclude(latitude=None).exclude(longitude=None)
          .prefetch_related('images'))
    if kat:
        qs = qs.filter(**RATU_KATEGORIJOS[kat])
        if kat in RATU_ISSKYRUS:
            qs = qs.exclude(**RATU_ISSKYRUS[kat])

    # Bendri filtrai, kuriuos ratai turi. Vardai tie patys kaip visur.
    for raktas, laukas in (('price_min', 'price__gte'), ('price_max', 'price__lte')):
        reiksme = request.GET.get(raktas)
        if reiksme:
            try:
                qs = qs.filter(**{laukas: float(reiksme)})
            except ValueError:
                pass
    if request.GET.get('q'):
        qs = qs.filter(title__icontains=request.GET['q'].strip())
    if request.GET.get('city'):
        qs = qs.filter(city__icontains=request.GET['city'].strip())
    if request.GET.get('su_nuotraukomis'):
        qs = qs.filter(images__isnull=False).distinct()
    return qs


def _riba(reiksme):
    try:
        return float(reiksme)
    except (TypeError, ValueError):
        return None


def _naujame_lange(request):
    """Ar žemėlapio skelbimus atidaryti naujame skirtuke.

    Tik darbalaukyje: žmogus surenka filtrus, priartina žemėlapį ir
    randa kelis įdomius — kiekvieną nori pažiūrėti neprarasdamas to, ką
    surinko. Telefone naujas skirtukas naršyklėje nepatogus, todėl ten
    liekam tame pačiame lange: žemėlapio padėtis ir filtrai guli adrese
    (zemelapio_paieska.js irasykURL), tad „atgal" grąžina tiksliai ten,
    kur buvai. Įrenginį sprendžia tas pats device_kind kaip visur.
    """
    from .context_processors import device_kind
    return not device_kind(request)['is_phone']


def _plote(qs, request):
    """Apriboja iki matomo žemėlapio ploto (abiem modeliams vienodai)."""
    s, n = _riba(request.GET.get('s')), _riba(request.GET.get('n'))
    v, r = _riba(request.GET.get('v')), _riba(request.GET.get('r'))
    if None in (s, n, v, r):
        return qs
    qs = qs.filter(latitude__gte=s, latitude__lte=n)
    # Jei plotas kerta 180-ąjį dienovidinį, ilguma „apsisuka"
    return (qs.filter(longitude__gte=v, longitude__lte=r) if v <= r
            else qs.filter(Q(longitude__gte=v) | Q(longitude__lte=r)))


def _skelbimu_qs(request):
    """(listing_qs, ratu_qs) pagal pasirinktą kategoriją ir filtrus.

    Be kategorijos rodom abi šeimas; pasirinkus — tik tą, kuriai
    kategorija priklauso.
    """
    kat = (request.GET.get('category') or '').strip()

    if kat in RATU_KATEGORIJOS:
        return None, _plote_arba_none(_ratu_qs(request, kat), request)

    if kat == 'motogear':
        baze = _motoaprangos_qs(request.user)
    else:
        baze = _su_koordinatemis(request.user)
    baze = baze.select_related('brand', 'model', 'fuel_type', 'transmission',
                               'vehicle_type').prefetch_related('images')
    listing_qs = _plote(_filtruoti(request, baze), request)

    # Ratai — tik kai kategorija nepasirinkta arba ji pati yra ratų
    ratu_qs = None
    if not kat:
        ratu_qs = _plote_arba_none(_ratu_qs(request), request)
    return listing_qs, ratu_qs


def _plote_arba_none(qs, request):
    return None if qs is None else _plote(qs, request)


def _kategoriju_kiekiai(request):
    """[{slug, vardas, kiek}] — VISAS katalogas su skaičiais.

    Skaičiuojama be kategorijos ir be jos vidinių filtrų (markės,
    modelio) — kitaip pasirinkus vieną kategoriją visos kitos rodytų
    nulius ir nebeliktų kaip persijungti. Bendri filtrai (kaina, metai,
    tekstas...) ir matomas plotas įskaičiuojami, kaip ir markių atveju.
    """
    from django.db.models import Count

    get = request.GET.copy()
    get.pop('category', None)
    # Markė ir modelis galioja tik savo kategorijoje: palikti juos reikštų,
    # kad pasirinkus „BMW" visos kitos kategorijos nukristų į nulį ir
    # taptų nepaspaudžiamos — nebeliktų kaip persijungti.
    for raktas in ('model', 'brand', 'truck_brand', 'motorcycle_brand',
                   'agri_brand_text', 'trailer_brand_text', 'rent_brand_text',
                   'elec_brand_text', 'load_brand_text', 'constr_brand_text',
                   'forest_brand_text', 'camp_brand_text', 'bike_brand_text'):
        get.pop(raktas, None)
    # GET pakeičiam laikinai, kad filtravimo kelias liktų tas pats
    tikras = request.GET
    request.GET = get
    try:
        listing_qs = _plote(_filtruoti(
            request, _su_koordinatemis(request.user)), request)
        kiekiai = dict(listing_qs.values_list('vehicle_type__slug')
                       .annotate(n=Count('id')))

        # Motoapranga juostoje yra atskiras punktas, todėl ir čia
        aprangos = _plote(_filtruoti(
            request, _motoaprangos_qs(request.user)), request).count()
        if aprangos:
            kiekiai['motogear'] = aprangos
            kiekiai['motorcycles'] = max(0, kiekiai.get('motorcycles', 0) - aprangos)

        ratai = _plote_arba_none(_ratu_qs(request), request)
        if ratai is not None:
            for eil in ratai.values('product_type', 'purpose').annotate(n=Count('id')):
                for slug, salygos in RATU_KATEGORIJOS.items():
                    if not all(eil.get(k) == v for k, v in salygos.items()):
                        continue
                    isskyrus = RATU_ISSKYRUS.get(slug, {})
                    if any(eil.get(k.split('__')[0]) in v for k, v in isskyrus.items()):
                        continue
                    kiekiai[slug] = kiekiai.get(slug, 0) + eil['n']
    finally:
        request.GET = tikras

    # Sąrašas — VISAS kategorijų katalogas (kategoriju_medis), ne tik tai,
    # kas pateko į rezultatus: žmogus turi matyti, kas apskritai yra, o
    # tuščios rodomos pilkos ir nepaspaudžiamos.
    return [{'slug': slug, 'vardas': vardas, 'kiek': kiekiai.get(slug, 0)}
            for slug, vardas in kategoriju_medis()]


def zemelapio_rezultatai(request):
    """JSON: kortelės ir žymekliai matomame plote."""
    listing_qs, ratu_qs = _skelbimu_qs(request)

    kiek = (listing_qs.count() if listing_qs is not None else 0) + \
           (ratu_qs.count() if ratu_qs is not None else 0)

    # Filtrų langui užtenka skaičiaus — jis skaičiuojamas SU tomis pačiomis
    # kraštinėmis, todėl mygtuke matomas tas pats skaičius, kurį žmogus
    # pamatys sąraše pritaikęs filtrus.
    if request.GET.get('tik_skaicius'):
        return JsonResponse({'kiek': kiek})

    # Rikiavimas — ta pati funkcija kaip rezultatų puslapyje; be jos
    # filtrų lango „Rūšiuoti pagal" nieko nedarydavo. Dvi šeimos gyvena
    # skirtingose lentelėse, todėl po rikiavimo jas sulipdom čia: iš
    # kiekvienos imam iki MAKS_KORTELIU ir paliekam tiek pat iš viso.
    irasai = []
    if listing_qs is not None:
        irasai += list(_rikiuoti_zemelapiui(listing_qs, request)[:MAKS_KORTELIU])
    if ratu_qs is not None:
        irasai += list(_rikiuoti_ratus(ratu_qs, request)[:MAKS_KORTELIU])
    irasai = _sulipdyk(irasai, request)[:MAKS_KORTELIU]

    issaugoti = set()
    if request.user.is_authenticated:
        issaugoti = set(SavedListing.objects.filter(
            user=request.user,
            listing__in=[o for o in irasai if o.__class__.__name__ == 'Listing'],
        ).values_list('listing_id', flat=True))

    html = render_to_string('listings/partials/_zemelapio_sarasas.html', {
        'korteles': [kortele(o, issaugotas=o.pk in issaugoti) for o in irasai],
        'naujame_lange': _naujame_lange(request),
    }, request=request)

    zymekliai = _zymekliai(listing_qs, request) if listing_qs is not None else []
    if ratu_qs is not None:
        zymekliai += _ratu_zymekliai(ratu_qs)

    return JsonResponse({'kiek': kiek, 'html': html, 'zymekliai': zymekliai,
                         'rodoma': len(irasai),
                         'kategorijos': _kategoriju_kiekiai(request)})


def _rikiuoti_ratus(qs, request):
    """Ratams tinka tik kaina ir naujumas — metų ir ridos jie neturi."""
    sort = request.GET.get('sort') or 'newest'
    if sort == 'price_asc':
        return qs.order_by('price', '-created_at')
    if sort == 'price_desc':
        return qs.order_by('-price', '-created_at')
    return qs.order_by('-created_at')


def _sulipdyk(irasai, request):
    """Dviejų lentelių įrašai į vieną tvarką (rikiavimo raktas — tas pats)."""
    sort = request.GET.get('sort') or 'newest'
    if sort == 'price_asc':
        return sorted(irasai, key=lambda o: o.price or 0)
    if sort == 'price_desc':
        return sorted(irasai, key=lambda o: o.price or 0, reverse=True)
    if sort == 'arciausiai':
        return irasai      # tvarką jau nustatė duomenų bazė
    return sorted(irasai, key=lambda o: getattr(o, 'paskelbta', None)
                  or o.created_at, reverse=True)


def _ratu_zymekliai(qs):
    """Ratlankių ir padangų žymekliai — tos pačios formos kaip skelbimų."""
    laukai = ('id', 'latitude', 'longitude', 'price', 'city')
    return [{
        'id': e['id'],
        'tipas': 'ratai',
        'lat': float(e['latitude']),
        'lng': float(e['longitude']),
        'kaina': formatai.kaina(e['price'], '€'),
        'apytiksliai': False,
        'spetas': False,
    } for e in qs.values(*laukai)[:MAKS_ZYMEKLIU]]


def _rikiuoti_zemelapiui(qs, request):
    """Rikiavimas žemėlapyje: bendra views.rikiuoti + „Arčiausiai".

    „Arčiausiai" prasmę turi tik čia, todėl ir gyvena čia. Atskaitos
    taškas — vartotojo vieta (mlat/mlng), o jei jos nėra, žemėlapio
    centras. Atstumas skaičiuojamas apytiksliai (plokščias, ilgumos
    skirtumas pataisytas pagal platumą) — rikiavimui to užtenka ir
    nereikia PostGIS.
    """
    from .views import rikiuoti

    if (request.GET.get('sort') or '') != 'arciausiai':
        return rikiuoti(qs, request.GET.get('sort'))

    from django.db.models import F, FloatField, ExpressionWrapper, Value
    import math

    lat = _riba(request.GET.get('mlat')) or _riba(request.GET.get('lat'))
    lng = _riba(request.GET.get('mlng')) or _riba(request.GET.get('lng'))
    if lat is None or lng is None:
        return rikiuoti(qs, 'newest')

    k = math.cos(math.radians(lat)) ** 2
    atstumas = ExpressionWrapper(
        (F('latitude') - Value(lat)) * (F('latitude') - Value(lat))
        + (F('longitude') - Value(lng)) * (F('longitude') - Value(lng)) * Value(k),
        output_field=FloatField())
    return qs.annotate(_atstumas=atstumas).order_by('_atstumas')


def zemelapio_paieska(request):
    """Puslapis. Pradinis turinys — Lietuva; toliau viską tvarko žemėlapis."""
    from django.conf import settings
    from django.utils import timezone

    qs = _filtruoti(request)
    metai = timezone.now().year

    from .models import FuelType
    # vietinis „_" — kad msgid'us pagautų makemessages (jis ieško _(...))
    from django.utils.translation import gettext as _

    return render(request, 'listings/search_map.html', {
        'is_viso': qs.count(),
        # Filtrų lango turinys — tie patys raktai, kaip visose paieškose
        'rusiavimo_kortos': [
            ('newest', _('Naujausi'), 'fa-clock'),
            ('arciausiai', _('Arčiausiai'), 'fa-location-crosshairs'),
            ('price_asc', _('Pigiausi'), 'fa-arrow-down-short-wide'),
            ('price_desc', _('Brangiausi'), 'fa-arrow-up-wide-short'),
        ],
        # Kategorijos — TAS PATS šaltinis, kuris piešia ikonų juostą ir
        # pikerį (kategoriju_medis iš panels.ADVANCED_RAIL). Čia buvo
        # ranka surašytas aštuonių kategorijų sąrašas — ketvirta kopija.
        # Patys punktai su skaičiais ateina su duomenimis; šitas sąrašas
        # reikalingas tik vardams ir ikonoms naršyklėje.
        'kategoriju_vardai': kategoriju_medis(),
        'kuro_tipai': FuelType.objects.all().order_by('name'),
        # Raktai — TIKRI filter_listings parametrai, ne savi vardai.
        # „vin"/„tik_lietuvoje" niekur nebuvo skaitomi, todėl tos žymos
        # tik piešdavosi ir nieko nefiltruodavo.
        'papildomi_filtrai': [
            ('has_vin', '1', _('Su VIN')),
            ('feat_warranty', 'on', _('Su garantija')),
            ('country_filter', 'LT', _('Tik Lietuvoje')),
            ('su_nuotraukomis', '1', _('Su nuotraukomis')),
        ],
        # Markių sąrašo čia nebėra: jį paduoda /ajax/markes/ pagal
        # pasirinktą kategoriją — tas pats šaltinis (Brand + scopes),
        # kurį naudoja panelės, detali paieška ir antraštės paieška.
        'years': list(range(metai + 1, 1989, -1)),
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
        'pradine_busena': ({
            'lat': _riba(request.GET.get('lat')) or 55.17,
            'lng': _riba(request.GET.get('lng')) or 23.88,
            'z': int(request.GET.get('z') or 7),
            'is_url': bool(request.GET.get('lat')),
            # Skelbimai naujame skirtuke — tik darbalaukyje (žr. _naujame_lange)
            'naujame_lange': _naujame_lange(request),
        }),
    })


# ═══════════════════════════════════════════════════════════════════
# ŽYMEKLIAI
#
# Žemėlapyje rodoma KAINA, ne taškas. Prekiautojų skelbimai suklijuojami
# į vieną aikštelės žymeklį. Apytikslėms vietoms koordinatės apvalinamos
# ČIA — tikslios į naršyklę neiškeliauja.
# ═══════════════════════════════════════════════════════════════════

APVALINIMAS = 3          # 3 skaitmenys ≈ 110 m tikslumas


def _apytiksliai(reiksme):
    return round(float(reiksme), APVALINIMAS)


def _zymekliai(qs, request):
    laukai = ('id', 'latitude', 'longitude', 'koordinates_tikslios',
              'hide_exact_address', 'price', 'currency', 'city',
              'seller_id', 'seller__profile__dealer_subscription_active',
              'seller__profile__dealer_company_name', 'seller__username')
    eilutes = list(qs.values(*laukai)[:MAKS_ZYMEKLIU])

    # Prekiautojų skelbimai — vienas žymeklis aikštelei
    prekiautoju = {}
    for e in eilutes:
        if e['seller__profile__dealer_subscription_active']:
            prekiautoju.setdefault(e['seller_id'], []).append(e)

    zymekliai = []
    for e in eilutes:
        if e['seller_id'] in prekiautoju:
            continue
        neaisku = e['hide_exact_address'] or not e['koordinates_tikslios']
        zymekliai.append({
            'id': e['id'],
            'lat': _apytiksliai(e['latitude']) if neaisku else float(e['latitude']),
            'lng': _apytiksliai(e['longitude']) if neaisku else float(e['longitude']),
            'kaina': formatai.kaina(e['price'], SIMBOLIAI.get(e['currency'], '€')),
            'apytiksliai': bool(e['hide_exact_address']),
            'spetas': not e['koordinates_tikslios'],
        })

    for seller_id, jo in prekiautoju.items():
        pirmas = jo[0]
        zymekliai.append({
            'tipas': 'pardavejas',
            'pardavejas': seller_id,
            'lat': float(pirmas['latitude']),
            'lng': float(pirmas['longitude']),
            'vardas': (pirmas['seller__profile__dealer_company_name']
                       or pirmas['seller__username']),
            'kiek': len(jo),
        })
    return zymekliai


def zemelapio_kortele(request, pk):
    """Burbulo turinys paspaudus žymeklį.

    ?tipas=ratai — ratlankis arba padanga (WheelListing). Turinys
    renderinamas per bendrą korteles.kortele(), todėl šablonas abiem
    šeimoms tas pats.
    """
    from django.shortcuts import get_object_or_404

    if request.GET.get('tipas') == 'ratai':
        ratai = _ratu_qs(request)
        if ratai is None:
            from .models import WheelListing
            ratai = WheelListing.objects.filter(status='active',
                                                is_shadow_banned=False)
        o = get_object_or_404(ratai, pk=pk)
        neaisku = False
        valiuta = '€'
    else:
        o = get_object_or_404(_su_koordinatemis(request.user), pk=pk)
        neaisku = o.hide_exact_address or not o.koordinates_tikslios
        valiuta = o.currency_symbol

    # Navigacijai — apvalintos, jei vieta apytikslė
    lat = _apytiksliai(o.latitude) if neaisku else float(o.latitude)
    lng = _apytiksliai(o.longitude) if neaisku else float(o.longitude)
    return JsonResponse({
        'html': render_to_string(
            'listings/partials/_zemelapio_burbulas.html',
            {'k': kortele(o), 'neaisku': neaisku, 'valiuta': valiuta,
             'lat': lat, 'lng': lng,
             'naujame_lange': _naujame_lange(request)}, request=request),
        'lat': lat, 'lng': lng, 'url': kortele(o)['url'],
    })


def zemelapio_pardavejas(request, pk):
    """Prekiautojo aikštelė — visi jo skelbimai sąraše."""
    qs = _filtruoti(request).filter(seller_id=pk)
    irasai = list(qs.order_by('-id')[:50])
    return JsonResponse({
        'kiek': qs.count(),
        'html': render_to_string('listings/partials/_zemelapio_aikstele.html',
                                 {'korteles': [kortele(o) for o in irasai],
                                  'naujame_lange': _naujame_lange(request)},
                                 request=request),
    })
