# -*- coding: utf-8 -*-
"""
LANKYTOJŲ ĮRAŠAI — BE ŽALIO IP.

Buvo `PageView` su `ip_address = GenericIPAddressField`, t. y. žalias
lankytojo IP gulėdavo DB neribotam laikui. Adresas mums reikalingas tik
tam, kad atskirtume, ar tai tas pats žmogus, — o tam užtenka maišos.
Todėl vietoj adreso saugom `ip_hash` = sha256(IP + SECRET_KEY druska).
Maiša vienakryptė: suskaičiuoti ją iš IP galima, atsekti IP iš jos — ne.

Modelis pervadintas į `VisitorHit`; lentelė ta pati, seni įrašai
nedingo — tik `ip_address` stulpelis pakeistas į `ip_hash`
(migracija 0004).

Senesni nei `SAUGOM_DIENAS` įrašai valomi — žr.
apps/analytics/management/commands/valyti_lankytojus.py.
"""
import hashlib

from django.conf import settings
from django.db import models

# Kiek laiko laikom įrašus. Statistikai užtenka 90 d., o DB neauga be galo.
SAUGOM_DIENAS = 90


def ip_maisa(ip):
    """sha256(IP + druska) — 64 šešioliktainiai simboliai.

    Druska yra SECRET_KEY: be jos maišos iš viso pasaulio IPv4 sąrašo
    neperrinksi, nors adresų erdvė ir maža.
    """
    if not ip:
        return ''
    druska = getattr(settings, 'SECRET_KEY', '') or ''
    return hashlib.sha256(('%s%s' % (ip, druska)).encode('utf-8')).hexdigest()


class VisitorHit(models.Model):
    """Vienas apsilankymas. Kuria apps/analytics/middleware.py."""

    # sha256 heksais — 64 simboliai. Žalio IP NESAUGOM (privatumas).
    ip_hash = models.CharField(max_length=64, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='page_views',
    )
    path = models.CharField(max_length=500)
    country = models.CharField(max_length=2, blank=True, db_index=True)
    country_name = models.CharField(max_length=100, blank=True)
    user_agent = models.CharField(max_length=500, blank=True, default='')
    is_bot = models.BooleanField(default=False, db_index=True)
    bot_reason = models.CharField(
        max_length=20,
        blank=True,
        default='',
        help_text='empty_ua | ua_pattern | path_scan | behavior',
    )
    referrer = models.CharField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ip_hash', 'created_at']),
            models.Index(fields=['is_bot', 'created_at']),
            models.Index(fields=['country', 'created_at']),
        ]

    def __str__(self):
        zyme = '🤖' if self.is_bot else '👤'
        return '%s %s -> %s' % (zyme, self.ip_hash[:12], self.path)
