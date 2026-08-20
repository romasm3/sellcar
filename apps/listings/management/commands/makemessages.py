"""`manage.py makemessages` su išjungtu msgmerge panašumo spėjimu.

KAM ŠITO REIKIA
───────────────
Django makemessages kviečia `msgmerge` be `--no-fuzzy-matching`. Kai
msgid pasikeičia arba atsiranda naujas, msgmerge suranda „panašiausią"
seną įrašą ir priskiria jo vertimą. Dažniausiai jis pažymimas `#, fuzzy`
(tada gettext jį ignoruoja ir rodo msgid — nekenksminga), bet dalis
priskyrimų lieka be žymos ir tampa gyvais, klaidingais vertimais.

Taip atsirado 57 klaidos, rastos 2026-08-20 audite:
    „Steel"             rodė „Vairavimas"
    „Fits car brands"   rodė „Diskiniai stabdžiai"
    „Polish"            rodė „English"
    „Bolt count"        rodė „Visos šalys"
    „Subscription active until" rodė „Techninė apžiūra galioja iki"

Su `--no-fuzzy-matching` msgmerge naujo msgid vertimo nespėlioja — jis
lieka tuščias, o tai matoma iš karto (`msgstr ""`) ir nepadaro žalos.

Komanda tik prideda vėliavą prie standartinės Django komandos; visa kita
elgsena nepakitusi.
"""
from django.core.management.commands import makemessages as base


class Command(base.Command):
    help = (base.Command.help or '') + \
        '  [AutoLeft: msgmerge visada leidžiamas su --no-fuzzy-matching]'

    msgmerge_options = base.Command.msgmerge_options + ['--no-fuzzy-matching']

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            'msgmerge --no-fuzzy-matching įjungtas: nauji msgid lieka be '
            'vertimo, o ne gauna spėtą svetimą.'
        ))
        return super().handle(*args, **options)
