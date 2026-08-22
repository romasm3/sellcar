"""Testų paleidiklis BE testinės duomenų bazės.

Šis serveris yra produkcija: DB vartotojas neturi (ir neturi turėti) teisės
kurti naujų duomenų bazių, todėl įprastas `manage.py test` net nepasileidžia.

Čia esantys testai yra TIK SKAITANTYS — jie atidaro puslapius per test client'ą
ir tikrina HTML. Todėl duomenų bazės kurti nereikia: dirbam su ta pačia, kurią
mato svetainė, ir nieko į ją nerašom (išskyrus sesiją prisijungimui).

Naudojimas:
    venv/bin/python manage.py test apps.listings --testrunner=config.test_runner.BeDuombazes
"""
from django.test.runner import DiscoverRunner


class BeDuombazes(DiscoverRunner):
    def setup_databases(self, **kwargs):
        return []

    def teardown_databases(self, old_config, **kwargs):
        return None
