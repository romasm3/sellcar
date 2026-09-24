# -*- coding: utf-8 -*-
"""
Ar kategorijų meniu skaičiai sutampa su tuo, kas iš tikrųjų yra DB.

Meniu skaičius ima iš `apps/listings/meniu_kiekiai.py` (viena vieta
visiems sąrašams). Ši komanda tą patį perskaičiuoja ATSKIRAI — po vieną
paprastą .count() užklausą kiekvienam punktui, be jokių agregacijų — ir
palygina. Sutampa visur → 0; bent vienas skirtumas → 1 ir eilutė su
abiem skaičiais.

    python manage.py tikrinti_meniu
    python manage.py tikrinti_meniu --tik-skirtumus
"""
from django.core.management.base import BaseCommand

from apps.listings.meniu_kiekiai import (RENTAL_SEKCIJOS, TRUCK_SEKCIJOS,
                                         kiekiai)


class Command(BaseCommand):
    help = 'Palygina kategorijų meniu skaičius su tikrais DB skaičiais.'

    def add_arguments(self, parser):
        parser.add_argument('--tik-skirtumus', action='store_true',
                            help='Rodyti tik nesutampančias eilutes.')

    # ── Nepriklausomas skaičiavimas ───────────────────────────────────
    def _tikri(self):
        """(raktas, pavadinimas, kiekis) — po vieną užklausą punktui."""
        from apps.listings import motogear_views
        from apps.listings.models import WheelListing
        from apps.listings.search_panel import PARTS_PANEL_SUBS
        from apps.listings.views import _public_listings_qs

        v = _public_listings_qs(None)
        ratai = WheelListing.objects.filter(status='active',
                                            is_shadow_banned=False)

        def pagal_tipa(slug):
            return v.filter(vehicle_type__slug=slug).count()

        def pagal_sub(slug):
            return v.filter(subcategory__slug=slug).count()

        apranga = motogear_views._moto_gear_public_qs(None).count()
        sunkusis = pagal_tipa('trucks')
        sekcijos = {s: pagal_sub(slug) for s, slug in TRUCK_SEKCIJOS.items()}

        eilutes = [
            ('cars',              'Automobiliai',                  pagal_tipa('cars')),
            ('motorcycles',       'Motociklai',                    max(0, pagal_tipa('motorcycles') - apranga)),
            ('motogear',          'Apranga, šalmai, aksesuarai',   apranga),
            ('moto-tyres',        'Padangos motociklams',          ratai.filter(product_type='tyre', purpose='moto').count()),
            # 'atv', ne 'quad' — taip vadinasi reikšmė WHEEL_PURPOSE_CHOICES
            ('quad-tyres',        'Padangos keturračiams',         ratai.filter(product_type='tyre', purpose='atv').count()),
            ('wheels:tyre',       'Padangos',                      ratai.filter(product_type='tyre').count()),
            ('wheels:rim',        'Ratlankiai',                    ratai.filter(product_type='rim').count()),
            ('trucks',            'Sunkvežimiai (visa kategorija)', sunkusis),
        ]
        for sekcija, kiek in sekcijos.items():
            eilutes.append(('trucks:' + sekcija, 'Sunkusis · ' + sekcija, kiek))
        eilutes.append(('trucks:main', 'Sunkusis · main (be sekcijų)',
                        max(0, sunkusis - sum(sekcijos.values()))))

        eilutes.append(('rental', 'Nuoma (visa kategorija)', pagal_tipa('rental')))
        for sekcija, slug in RENTAL_SEKCIJOS.items():
            eilutes.append(('rental:' + sekcija, 'Nuoma · ' + sekcija, pagal_sub(slug)))

        for slug, pav in (('trailers', 'Priekabos'),
                          ('agriculture', 'Žemės ūkio technika'),
                          ('construction', 'Statybinė technika'),
                          ('forestry', 'Miško ūkio technika'),
                          ('loading-equipment', 'Krovimo technika'),
                          ('camping-houses', 'Turistiniai nameliai'),
                          ('boats', 'Vandens transportas'),
                          ('bicycles', 'Dviračiai, paspirtukai'),
                          ('electronics', 'Video, audio, navigacijos'),
                          ('services', 'Paslaugos'),
                          ('parts', 'Dalys (visa kategorija)')):
            eilutes.append((slug, pav, pagal_tipa(slug)))

        eilutes.append(('construction:construction-attachments',
                        'Statybinės technikos priedai',
                        pagal_sub('construction-attachments')))
        eilutes.append(('services:car-buying', 'Automobilių supirkimas',
                        v.filter(vehicle_type__slug='services',
                                 service_type='car_buying').count()))
        for raktas, slug, etikete in PARTS_PANEL_SUBS:
            eilutes.append(('parts:' + raktas, 'Dalys · %s' % etikete,
                            pagal_sub(slug)))
        return eilutes

    # ── Paleidimas ────────────────────────────────────────────────────
    def handle(self, *args, **opt):
        meniu = kiekiai(None)
        eilutes = self._tikri()

        skirtumai = 0
        self.stdout.write('%-42s %10s %10s' % ('PUNKTAS', 'MENIU', 'DB'))
        self.stdout.write('-' * 64)
        for raktas, pavadinimas, tikras in eilutes:
            rodomas = meniu.get(raktas, 0)
            sutampa = (rodomas == tikras)
            if not sutampa:
                skirtumai += 1
            if opt['tik_skirtumus'] and sutampa:
                continue
            eil = '%-42s %10s %10s' % (pavadinimas[:42], rodomas, tikras)
            self.stdout.write(eil if sutampa
                              else self.style.ERROR(eil + '   ← SKIRIASI'))

        self.stdout.write('-' * 64)
        if skirtumai:
            self.stdout.write(self.style.ERROR(
                'Nesutampa %d punktas (-ai) iš %d.' % (skirtumai, len(eilutes))))
            raise SystemExit(1)
        self.stdout.write(self.style.SUCCESS(
            'Visi %d punktai sutampa.' % len(eilutes)))
