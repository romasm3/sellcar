# -*- coding: utf-8 -*-
"""
KELIAS BE KALBOS PRIEŠDĖLIO + AKTYVI NE LIETUVIŲ KALBA → 302 Į /<kalba>/…

Kodėl reikia
------------
`config/urls.py` naudoja `i18n_patterns(..., prefix_default_language=False)`:
lietuviški adresai be priešdėlio (`/`), kiti — su (`/ru/`).

Django `LocaleMiddleware` tokį derinį apsaugo pats: kai kelyje priešdėlio
nėra, jis PRIVERSTINAI grąžina `settings.LANGUAGE_CODE`
(django/middleware/locale.py — `if not language_from_path and
i18n_patterns_used and not prefixed_default_language`). Todėl anoniminiam
lankytojui su `django_language=ru` slapuku „/" atsidaro puikiai.

Bet `apps.accounts.middleware.UserLanguageMiddleware` veikia PO jo ir
prisijungusiam žmogui vėl įjungia profilio kalbą. Tada URL sprendimo
metu `LocalePrefixPattern.language_prefix` grąžina „ru/", o „/" nebeatitinka
NĖ VIENO maršruto — 404. Praktiškai: kas kartą pasirinko rusų kalbą ir
liko prisijungęs, į svetainę nebepateko visai.

Ką darom
--------
Jei aktyvi kalba ne numatytoji, o kelyje priešdėlio nėra — 302 į tą patį
kelią su priešdėliu ir tais pačiais GET parametrais.

Trys sargai, kad nukreipimas pats netaptų gedimu:

* nukreipiam TIK jei `/<kalba><kelias>` tikrai išsisprendžia — kitaip
  tikras 404 liktų 404, o ne suktųsi ratu;
* tik GET ir HEAD — 302 nuneštų POST kūną;
* nė vienas kelias už `i18n_patterns` ribų (/admin/, /static/, /media/,
  /i18n/, /rosetta/, robots.txt, sitemap) neliečiamas: jiems priešdėlio
  nėra ir nebus.

Atsakymo pusėje liko tas pats patikrinimas 404 atveju — kaip tinklas po
akrobatu, jei kalbą įjungtų kas nors kitas.
"""
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import Resolver404, resolve
from django.utils import translation
from django.utils.translation import get_language_from_path

# Keliai, gyvenantys UŽ i18n_patterns ribų (config/urls.py)
BE_PRIESDELIO = ('/admin/', '/static/', '/media/', '/i18n/', '/rosetta/',
                 '/robots.txt', '/sitemap')


def _uz_i18n(kelias):
    return kelias.startswith(BE_PRIESDELIO)


def _su_priesdeliu(kelias, kalba):
    return '/%s%s' % (kalba, kelias)


def _issisprendzia(kelias):
    try:
        resolve(kelias)
        return True
    except Resolver404:
        return False


def be_priesdelio(kelias):
    """„/ru/imones/" → „/imones/". Priešdėlio nesant — kelias nekeičiamas."""
    kalba = get_language_from_path(kelias)
    if not kalba:
        return kelias
    likutis = kelias[len(kalba) + 1:]        # nuimam „/ru"
    return likutis if likutis.startswith('/') else '/' + likutis


def su_kalba(adresas, kalba, gylis=2):
    """Adresą perrašo į `kalba` — kartu ir jo `next` parametrą.

    Kalbos perjungiklis siunčia `next = request.get_full_path()`, o
    prisijungimo ir registracijos puslapiuose tas adresas savo viduje
    nešasi DAR VIENĄ adresą: `/ru/accounts/login/?next=/ru/?category=cars`.
    Perrašius tik išorinį kelią, po prisijungimo žmogus vis tiek
    nukristų į `/ru/…` ir kalba grįžtų atgal — todėl lendam ir į vidų.

    Absoliučių ir svetimų adresų neliečiam: perjungiklis dirba tik su
    savo svetainės keliais.
    """
    if not adresas or not adresas.startswith('/') or adresas.startswith('//'):
        return adresas
    dalys = urlsplit(adresas)
    kelias = be_priesdelio(dalys.path)

    if _uz_i18n(kelias):
        naujas = dalys.path                   # /admin/, /static/… — nekeičiam
    elif kalba == settings.LANGUAGE_CODE:
        naujas = kelias                       # numatytoji kalba be priešdėlio
    else:
        su = _su_priesdeliu(kelias, kalba)
        # Priešdėlį dedam tik jei toks maršrutas tikrai yra — kitaip
        # perjungiklis pats pagamintų 404. Sprendžiam PO `override`:
        # `LocalePrefixPattern` atpažįsta tik aktyvios kalbos priešdėlį,
        # ir būtent dėl to Django `translate_url` čia nieko nekeisdavo.
        with translation.override(kalba):
            tinka = _issisprendzia(su)
        naujas = su if tinka else kelias

    uzklausa = dalys.query
    if gylis > 0 and uzklausa:
        poros = parse_qsl(uzklausa, keep_blank_values=True)
        if any(r == 'next' for r, _v in poros):
            poros = [(r, su_kalba(v, kalba, gylis - 1) if r == 'next' else v)
                     for r, v in poros]
            uzklausa = urlencode(poros)

    return urlunsplit(('', '', naujas, uzklausa, dalys.fragment))


class KalbosKelioMiddleware:
    """302 į kalbos priešdėlį, kai be jo maršruto nebūtų."""

    def __init__(self, get_response):
        self.get_response = get_response

    def _nukreipimas(self, request):
        if request.method not in ('GET', 'HEAD'):
            return None
        kelias = request.path_info
        if _uz_i18n(kelias) or get_language_from_path(kelias):
            return None
        kalba = translation.get_language() or settings.LANGUAGE_CODE
        if kalba == settings.LANGUAGE_CODE:
            return None
        naujas = _su_priesdeliu(kelias, kalba)
        if not _issisprendzia(naujas):
            return None
        uzklausa = request.META.get('QUERY_STRING', '')
        return HttpResponseRedirect(naujas + ('?' + uzklausa if uzklausa else ''))

    def __call__(self, request):
        nukreipimas = self._nukreipimas(request)
        if nukreipimas is not None:
            return nukreipimas

        response = self.get_response(request)

        # Tinklas: jei kalbą įjungė kas nors po mūsų, 404 vis tiek
        # virsta nukreipimu, o ne tuščiu puslapiu.
        if response.status_code == 404:
            nukreipimas = self._nukreipimas(request)
            if nukreipimas is not None:
                return nukreipimas
        return response


# ═══════════════════════════════════════════════════════════════════
# KALBOS PERJUNGIMAS
#
# Django `set_language` adreso priešdėlį persuka per `translate_url`, o
# tas pirma bando `resolve(kelias)`. `LocalePrefixPattern` atpažįsta TIK
# aktyvios kalbos priešdėlį, o perjungimo POST'as ateina į /i18n/setlang/
# — be priešdėlio, tad aktyvi kalba dažniausiai numatytoji. Tada
# `resolve("/ru/accounts/login/")` meta Resolver404, `translate_url`
# tyliai grąžina tą patį adresą, ir žmogus nukreipiamas atgal į /ru/…
# Slapukas jau naujas, bet kelio priešdėlis viršesnis — kalba grįžta.
#
# Todėl `next` persukam patys (`su_kalba`) ir tik tada atiduodam Django.
# ═══════════════════════════════════════════════════════════════════
def perjungti_kalba(request):
    """`set_language` su teisingai persuktu `next` (ir jo viduje esančiu)."""
    from django.views.i18n import set_language

    if request.method == 'POST':
        kalba = request.POST.get('language')
        adresas = request.POST.get('next') or request.META.get('HTTP_REFERER', '')
        if kalba and adresas:
            request.POST = request.POST.copy()
            request.POST['next'] = su_kalba(adresas, kalba)
        # Prisijungusio žmogaus profilio kalba — kitaip
        # UserLanguageMiddleware kitą užklausą vėl įjungtų senąją.
        if kalba and request.user.is_authenticated:
            try:
                profilis = request.user.profile
                profilis.language = kalba
                profilis.save(update_fields=['language'])
            except Exception:
                pass
    return set_language(request)
