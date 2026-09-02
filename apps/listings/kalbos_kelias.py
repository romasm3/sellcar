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
