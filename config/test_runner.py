"""Testų paleidiklis BE testinės duomenų bazės.

Šis serveris yra produkcija: DB vartotojas neturi (ir neturi turėti) teisės
kurti naujų duomenų bazių, todėl įprastas `manage.py test` net nepasileidžia.

Čia esantys testai yra TIK SKAITANTYS — jie atidaro puslapius per test client'ą
ir tikrina HTML. Todėl duomenų bazės kurti nereikia: dirbam su ta pačia, kurią
mato svetainė, ir nieko į ją nerašom (išskyrus sesiją prisijungimui).

Naudojimas:
    venv/bin/python manage.py test apps.listings --testrunner=config.test_runner.BeDuombazes
"""
from django.conf import settings
from django.test.runner import DiscoverRunner
from django.test.utils import override_settings
from django.utils.functional import empty

# Paprasta statinių saugykla — be turinio maišų ir be staticfiles.json.
#
# KODĖL. Produkcijoje statinius atiduoda ManifestStaticFilesStorage, o ji
# reikalauja, kad KIEKVIENAS {% static %} kelias jau būtų staticfiles.json.
# Manifestą pagamina `collectstatic`, kuris deploy'e paleidžiamas PO šitų
# testų (deploy-from-git.sh: pirma scripts/patikra.sh, tik paskui
# deploy-agent.sh) — tyčia, kad krintanti patikra nė nepaliestų produkcijos.
#
# Todėl naujas statinis failas užrakindavo diegimą: šablonas jį jau mini,
# manifestas dar apie jį nežino, testai krinta su
#
#     ValueError: Missing staticfiles manifest entry for 'js/valiuta.js'
#
# ir kodas atsukamas atgal — o kartu su juo ir collectstatic, kuris tą
# manifestą būtų sutvarkęs. Užburtas ratas: 2026-09 taip užstrigo 19
# commit'ų. Rankomis nepataisysi ir commit'u nepataisysi — staticfiles/
# yra .gitignore'e.
#
# Šitie testai tikrina ŠABLONUS ir PUSLAPIUS, o ne surinkimo rezultatą, tad
# manifesto jiems nereikia. Ar maišai tikrai veikia, tikrina
# docs/statiniu_kesas_test.py, o deploy-agent.sh po collectstatic atskirai
# žiūri, kad staticfiles.json būtų šviežias.
STATINIU_SAUGYKLA = 'django.contrib.staticfiles.storage.StaticFilesStorage'


class BeDuombazes(DiscoverRunner):
    def setup_databases(self, **kwargs):
        return []

    def teardown_databases(self, old_config, **kwargs):
        return None

    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        self._statiniai = override_settings(STORAGES={
            **settings.STORAGES,
            'staticfiles': {'BACKEND': STATINIU_SAUGYKLA},
        })
        self._statiniai.enable()
        _pamirsk_saugykla()

    def teardown_test_environment(self, **kwargs):
        statiniai = getattr(self, '_statiniai', None)
        if statiniai is not None:
            statiniai.disable()
            _pamirsk_saugykla()
        super().teardown_test_environment(**kwargs)


def _pamirsk_saugykla():
    """Priverstinai perkrauna `staticfiles_storage`.

    `override_settings` pasikliauja Django signalu, kuris pamiršta seną
    saugyklą pasikeitus STORAGES. Nesiremiam juo: signalo gaudytojas
    skirtingose Django versijose stebi skirtingus raktus, o klaidos kaina
    čia — sustojęs diegimas. Objektas yra `SimpleLazyObject`, tad
    užtenka nuvalyti tai, ką jis jau buvo įsiminęs.
    """
    from django.contrib.staticfiles.storage import staticfiles_storage
    staticfiles_storage._wrapped = empty
