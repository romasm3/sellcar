# -*- coding: utf-8 -*-
"""
Išvalo skelbimus, kuriuose guli PASKYROS numeris, o ne įvestas kontaktas.

Kol kūrimo forma paskyros numerį įrašydavo į lauką `value`, žmogui nieko
nepakeitus jis nugulėdavo skelbime kaip to skelbimo kontaktas. Taip
paskyros savininko asmeninis numeris atsidūrė svetimų pardavėjų
skelbimuose (#827). Forma nuo šiol jo neįrašo (jis tik siūlomas
placeholder'iu), bet jau įrašytas reikšmes reikia pašalinti.

Numatytai NIEKO NEKEIČIA — tik parodo, ką keistų:

    python manage.py isvalyk_svetima_telefona
    python manage.py isvalyk_svetima_telefona --id 827 833 841 844 847
    python manage.py isvalyk_svetima_telefona --id 827 --daryk

Išvalytas laukas lieka TUŠČIAS: skelbimo puslapis tada nerodo jokio
numerio (Listing.kontaktinis_telefonas paskyros nebesiekia), o savininkas
teisingą numerį įrašo redaguodamas.

PRIEŠ `--daryk` pasidaryk DB kopiją — reikšmės neatkuriamos.
"""
from django.core.management.base import BaseCommand

from apps.listings.models import Listing


class Command(BaseCommand):
    help = 'Išvalo skelbimus, kurių contact_phone = savininko paskyros numeris.'

    def add_arguments(self, parser):
        parser.add_argument('--id', nargs='+', type=int, default=None,
                            help='Tik šie skelbimai. Be jo — visi tinkantys.')
        parser.add_argument('--daryk', action='store_true',
                            help='Tikrai išvalyti. Be jo — tik parodo.')

    def handle(self, *args, **opt):
        qs = Listing.objects.exclude(contact_phone='').select_related('seller')
        if opt['id']:
            qs = qs.filter(pk__in=opt['id'])

        radiniai = []
        for l in qs.iterator():
            profilis = getattr(l.seller, 'profile', None)
            paskyros = (getattr(profilis, 'phone_number', '') or '').strip()
            if paskyros and (l.contact_phone or '').strip() == paskyros:
                radiniai.append((l, paskyros))

        if not radiniai:
            self.stdout.write(self.style.SUCCESS(
                'Nerasta nė vieno skelbimo su paskyros numeriu.'))
            return

        self.stdout.write('%-8s %-22s %s' % ('ID', 'NUMERIS', 'SAVININKAS'))
        self.stdout.write('-' * 60)
        for l, paskyros in radiniai:
            self.stdout.write('%-8s %-22s %s' % (
                l.pk, paskyros, getattr(l.seller, 'email', '—')))
        self.stdout.write('-' * 60)

        if not opt['daryk']:
            self.stdout.write(self.style.WARNING(
                'Rasta %d. NIEKO NEPAKEISTA — pridėk --daryk (prieš tai DB kopija).'
                % len(radiniai)))
            return

        for l, _ in radiniai:
            l.contact_phone = ''
            l.save(update_fields=['contact_phone'])
        self.stdout.write(self.style.SUCCESS('Išvalyta: %d' % len(radiniai)))
