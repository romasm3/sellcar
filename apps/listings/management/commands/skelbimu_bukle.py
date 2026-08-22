# -*- coding: utf-8 -*-
"""
Management command: skelbimu_bukle

Diagnostika: kodėl skelbimo nesimato viešame sąraše.

Viešas sąrašas (_public_listings_qs) rodo TIK status='active' arba
neseniai parduotus, ir nerodo shadow-ban'intų. Ši komanda parodo, kokioje
būsenoje realiai guli skelbimai ir kiek jų dėl to nematomi.

TIK SKAITO — nieko nekeičia.

Naudojimas:
    python manage.py skelbimu_bukle
    python manage.py skelbimu_bukle --user romasm3@gmail.com
    python manage.py skelbimu_bukle --user romasm3@gmail.com --rodyti
"""
from collections import Counter
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.listings.models import Listing, Truck, WheelListing

MODELS = (Listing, Truck, WheelListing)


class Command(BaseCommand):
    help = 'Parodo skelbimų būsenas ir kiek jų nematomi viešame sąraše'

    def add_arguments(self, parser):
        parser.add_argument('--user', help='Pardavėjo el. paštas (be jo — visi)')
        parser.add_argument('--rodyti', action='store_true',
                            help='Išvardyti nematomus skelbimus po vieną')

    def handle(self, *args, **opts):
        now = timezone.now()
        seller = None
        if opts['user']:
            User = get_user_model()
            seller = User.objects.filter(email=opts['user']).first()
            if not seller:
                self.stderr.write(self.style.ERROR(
                    'Nerastas vartotojas: %s' % opts['user']))
                return
            self.stdout.write('Pardavėjas: %s (#%s)\n' % (seller.email, seller.pk))

        for model in MODELS:
            label = model.__name__
            qs = model.objects.all()
            if seller:
                if not any(f.name == 'seller' for f in model._meta.get_fields()):
                    continue
                qs = qs.filter(seller=seller)

            total = qs.count()
            if total == 0:
                self.stdout.write('%s: skelbimų nėra.\n' % label)
                continue

            counts = Counter(qs.values_list('status', flat=True))
            self.stdout.write(self.style.MIGRATE_HEADING('\n%s — iš viso %d' % (label, total)))
            for status, n in sorted(counts.items(), key=lambda x: -x[1]):
                matomas = 'MATOMAS' if status == 'active' else 'nematomas'
                self.stdout.write('  %-10s %5d   %s' % (status, n, matomas))

            # kodėl nematomi
            hidden = qs.exclude(status='active')
            shadow = qs.filter(status='active', is_shadow_banned=True).count() \
                if any(f.name == 'is_shadow_banned' for f in model._meta.get_fields()) else 0
            overdue = qs.filter(status='expired', expires_at__lt=now).count() \
                if any(f.name == 'expires_at' for f in model._meta.get_fields()) else 0

            self.stdout.write('  ─' * 20)
            self.stdout.write('  nematomi dėl būsenos:      %d' % hidden.count())
            if overdue:
                self.stdout.write('  iš jų pasibaigę (expires_at praeityje): %d' % overdue)
            if shadow:
                self.stdout.write(self.style.WARNING(
                    '  aktyvūs, bet shadow-ban:   %d' % shadow))

            # kada baigiasi dar aktyvūs
            if any(f.name == 'expires_at' for f in model._meta.get_fields()):
                soon = qs.filter(status='active', expires_at__lt=now + timedelta(days=7),
                                 expires_at__gte=now).count()
                never = qs.filter(status='active', expires_at__isnull=True).count()
                if soon:
                    self.stdout.write('  aktyvūs, baigsis per 7 d.: %d' % soon)
                if never:
                    self.stdout.write('  aktyvūs be pabaigos datos: %d '
                                      '(pvz. testiniai)' % never)

            if opts['rodyti'] and hidden.exists():
                self.stdout.write('\n  Nematomi skelbimai:')
                for l in hidden.order_by('-created_at')[:60]:
                    exp = getattr(l, 'expires_at', None)
                    exp_s = exp.strftime('%Y-%m-%d') if exp else '—'
                    self.stdout.write('    #%-6s %-10s baigėsi:%-12s %s'
                                      % (l.pk, l.status, exp_s, str(l.title)[:45]))

        self.stdout.write(self.style.SUCCESS(
            '\nViešame sąraše matomi tik status="active" (+ neseniai parduoti).\n'
            'Jei tavo seni skelbimai yra "expired" — juos reikia aktyvuoti iš naujo,\n'
            'o ne taisyti kode.'))
