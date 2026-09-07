# -*- coding: utf-8 -*-
"""
Management command: sunkiojo_subkategorijos

Sunkiojo transporto skelbimų subkategorijų peržiūra ir taisymas.

Kodėl reikia. `?subcategory=` būdavo įrašoma TIK kuriant juodraštį, tad
atėjus į formą su jau esamu juodraščiu ji dingdavo ir visi vilkikai
gulėdavo į „Sunkvežimius" (#749, #754, #762). Priežastis pataisyta
(apps/listings/trucks_views.py), o jau paskelbtus skelbimus sutvarko
ši komanda.

Naudojimas:

    # ką turim (skelbimų kiekiai pagal subkategorijas)
    python manage.py sunkiojo_subkategorijos

    # #749, #754, #762 → Vilkikai, „Tipas" išvalyti (pirma be --patvirtinu)
    python manage.py sunkiojo_subkategorijos --skelbimai 749 754 762 \
        --subkategorija semi-trucks-tractors --isvalyti-tipa
    python manage.py sunkiojo_subkategorijos --skelbimai 749 754 762 \
        --subkategorija semi-trucks-tractors --isvalyti-tipa --patvirtinu

Antraštės perrašomos ta pačia taisykle, kaip ir kuriant
(`sunkiojo_antraste`), tad po perkėlimo #749 tampa „MAN 18.510 4x2
2022 m Vilkikas".
"""
from django.core.management.base import BaseCommand, CommandError

from apps.listings import sunkusis
from apps.listings.models import Listing, SubCategory, VehicleType


class Command(BaseCommand):
    help = 'Sunkiojo transporto skelbimų subkategorijos: peržiūra ir taisymas'

    def add_arguments(self, parser):
        parser.add_argument('--skelbimai', type=int, nargs='+', default=None,
                            help='Skelbimų id, kuriuos perkelti')
        parser.add_argument('--subkategorija', default='',
                            help='Į kurią perkelti (slug, pvz. semi-trucks-tractors)')
        parser.add_argument('--isvalyti-tipa', action='store_true',
                            help='Kartu išvalyti „Tipas" (truck_type)')
        parser.add_argument('--patvirtinu', action='store_true',
                            help='Be jo tik parodo, ką darytų')

    # ── peržiūra ────────────────────────────────────────────────────
    def _apzvalga(self):
        vt = VehicleType.objects.filter(slug='trucks').first()
        if not vt:
            raise CommandError('Nėra „trucks" kategorijos')
        self.stdout.write('Sunkiojo transporto subkategorijos:')
        for sc in SubCategory.objects.filter(vehicle_type=vt).order_by('order', 'name'):
            kiek = Listing.objects.filter(subcategory=sc).count()
            zyme = '' if sc.slug in sunkusis.VISOS else '   (ne iš penkių)'
            self.stdout.write('  %-24s %-32s %4d%s'
                              % (sc.slug, sc.name, kiek, zyme))
        be_sub = Listing.objects.filter(vehicle_type=vt,
                                        subcategory__isnull=True).count()
        if be_sub:
            self.stdout.write(self.style.WARNING(
                '  %-24s %-32s %4d' % ('(nenurodyta)', '—', be_sub)))

    def handle(self, *args, **options):
        skelbimai = options['skelbimai']
        slug = (options['subkategorija'] or '').strip()
        isvalyti = options['isvalyti_tipa']
        patvirtinta = options['patvirtinu']

        if not skelbimai:
            self._apzvalga()
            return

        if not slug:
            raise CommandError('Nurodykite --subkategorija')
        if slug not in sunkusis.VISOS:
            raise CommandError('Nežinoma subkategorija „%s". Galimos: %s'
                               % (slug, ', '.join(sunkusis.VISOS)))

        vt = VehicleType.objects.filter(slug='trucks').first()
        sub = SubCategory.objects.filter(vehicle_type=vt, slug=slug).first()
        if sub is None:
            raise CommandError('Duomenų bazėje nėra subkategorijos „%s"' % slug)

        rasti = list(Listing.objects.filter(pk__in=skelbimai))
        trukstami = sorted(set(skelbimai) - {l.pk for l in rasti})
        if trukstami:
            raise CommandError('Nerasti skelbimai: %s'
                               % ', '.join(str(p) for p in trukstami))

        from apps.listings.trucks_views import sunkiojo_antraste

        for l in rasti:
            sena_sub = l.subcategory.name if l.subcategory_id else '—'
            sena_antraste = l.title
            l.subcategory = sub
            if isvalyti:
                l.truck_type = ''
            nauja_antraste = sunkiojo_antraste(l)
            self.stdout.write('  #%-5s %-28s → %s' % (l.pk, sena_sub, sub.name))
            self.stdout.write('         „%s"' % sena_antraste)
            self.stdout.write('      → „%s"' % nauja_antraste)
            if patvirtinta:
                l.title = nauja_antraste
                laukai = ['subcategory', 'title', 'country']
                if isvalyti:
                    laukai.append('truck_type')
                l.save(update_fields=laukai)

        self.stdout.write(self.style.SUCCESS(
            '%s %d skelbimų → %s%s'
            % ('Perkelta' if patvirtinta else 'Perkeltume',
               len(rasti), sub.name,
               '; „Tipas" išvalytas' if isvalyti else '')))
        if not patvirtinta:
            self.stdout.write(self.style.WARNING(
                'Tai buvo sausas bėgimas — pridėkite --patvirtinu'))
