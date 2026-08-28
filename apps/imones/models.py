# -*- coding: utf-8 -*-
"""
ĮMONĖS — vienas objektas, du tipai.

Prekiautojas ir servisas skiriasi tik tuo, kas rodoma puslapio viduryje
(skelbimai ar paslaugos), todėl atskirų modelių nekuriame — vienas
`Imone` su `tipas`.

Vietos duomenys (adresas, lat/lng, miestas, šalis) — tokie patys laukai
kaip skelbime, todėl juos galima pildyti tuo pačiu Photon keliu
(apps/listings/geokodavimas.py), o žemėlapis moka rodyti ir vienus, ir
kitus.

Atsiliepimų ČIA NĖRA sąmoningai (3 etapas): jiems reikia atskirų
taisyklių, kas gali rašyti ir ką daryti su melagingais. Vietoj vertinimo
rodom „Nuo YYYY m." ir skelbimų skaičių.
"""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.listings import salys

# Savaitės dienos darbo laikui. Raktas — Python savaitės diena
# (0 = pirmadienis), kad `datetime.weekday()` tiktų tiesiogiai.
SAVAITE = [
    (0, _('Pirmadienis')), (1, _('Antradienis')), (2, _('Trečiadienis')),
    (3, _('Ketvirtadienis')), (4, _('Penktadienis')), (5, _('Šeštadienis')),
    (6, _('Sekmadienis')),
]


class VeiklosSritis(models.Model):
    """Žyma: prekyba, supirkimas, servisas, padangos, detailing…"""
    pavadinimas = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    tvarka = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tvarka', 'pavadinimas']
        verbose_name = _('Veiklos sritis')
        verbose_name_plural = _('Veiklos sritys')

    def __str__(self):
        return self.pavadinimas

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.pavadinimas)[:64]
        super().save(*args, **kwargs)


class Imone(models.Model):
    PREKIAUTOJAS = 'prekiautojas'
    SERVISAS = 'servisas'
    TIPAI = [(PREKIAUTOJAS, _('Prekiautojas')), (SERVISAS, _('Servisas'))]

    tipas = models.CharField(max_length=16, choices=TIPAI, default=PREKIAUTOJAS)
    pavadinimas = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    logotipas = models.ImageField(upload_to='imones/logo/', blank=True, null=True)
    aprasymas = models.TextField(blank=True)

    adresas = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    miestas = models.CharField(max_length=100, blank=True)
    salis = models.CharField(max_length=2, choices=salys.pasirinkimai(),
                             default=salys.NUMATYTA)

    telefonas = models.CharField(max_length=32, blank=True)
    el_pastas = models.EmailField(blank=True)
    svetaine = models.URLField(blank=True)

    # {"0": ["08:00", "18:00"], ..., "6": null}  — null reiškia „nedirba"
    darbo_laikas = models.JSONField(default=dict, blank=True)

    veiklos = models.ManyToManyField(VeiklosSritis, blank=True,
                                     related_name='imones')
    savininkas = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                   blank=True, on_delete=models.SET_NULL,
                                   related_name='imones')
    patvirtinta = models.BooleanField(default=False)
    # Bandomieji įrašai — kad juos būtų galima rasti ir pašalinti viena
    # komanda (manage.py imones_testines --pasalinti). Tikrų įmonių
    # niekada nežymim.
    testine = models.BooleanField(default=False, verbose_name='Testinė')

    sukurta = models.DateTimeField(auto_now_add=True)
    atnaujinta = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['pavadinimas']
        verbose_name = _('Įmonė')
        verbose_name_plural = _('Įmonės')
        indexes = [
            models.Index(fields=['patvirtinta', 'tipas']),
            models.Index(fields=['miestas']),
        ]

    def __str__(self):
        return self.pavadinimas

    def save(self, *args, **kwargs):
        if not self.slug:
            baze = slugify(self.pavadinimas)[:120] or 'imone'
            kandidatas, n = baze, 2
            while Imone.objects.filter(slug=kandidatas).exclude(pk=self.pk).exists():
                kandidatas = f'{baze}-{n}'
                n += 1
            self.slug = kandidatas
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('imones:imone', kwargs={'slug': self.slug})

    # ── Darbo laikas ────────────────────────────────────────────────
    def laikas(self, diena):
        """['08:00', '18:00'] arba None, jei tą dieną nedirba."""
        reiksme = (self.darbo_laikas or {}).get(str(diena))
        if isinstance(reiksme, (list, tuple)) and len(reiksme) == 2:
            return list(reiksme)
        return None

    def savaites_laikai(self):
        """[(vardas, ['08:00','18:00'] arba None, ar_siandien)] — puslapiui."""
        siandien = timezone.localtime().weekday()
        return [(vardas, self.laikas(d), d == siandien) for d, vardas in SAVAITE]

    def ar_atidaryta(self):
        laikai = self.laikas(timezone.localtime().weekday())
        if not laikai:
            return False
        dabar = timezone.localtime().strftime('%H:%M')
        return laikai[0] <= dabar < laikai[1]

    def uzsidaro(self):
        """„18:00" — kada šiandien užsidaro (arba None)."""
        laikai = self.laikas(timezone.localtime().weekday())
        return laikai[1] if laikai else None

    # ── Turinys ─────────────────────────────────────────────────────
    def skelbimai(self):
        """Prekiautojo skelbimai — per savininką, tas pats viešas srautas."""
        from apps.listings.views import _public_listings_qs
        if not self.savininkas_id:
            from apps.listings.models import Listing
            return Listing.objects.none()
        return _public_listings_qs(None).filter(seller_id=self.savininkas_id)

    def nuo_metu(self):
        """„Nuo 2019 m." — kol atsiliepimų nėra, tai rodom vietoj vertinimo."""
        return self.sukurta.year if self.sukurta else None


class ImonesNuotrauka(models.Model):
    imone = models.ForeignKey(Imone, on_delete=models.CASCADE,
                              related_name='nuotraukos')
    nuotrauka = models.ImageField(upload_to='imones/')
    tvarka = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tvarka', 'id']
        verbose_name = _('Įmonės nuotrauka')
        verbose_name_plural = _('Įmonės nuotraukos')

    def __str__(self):
        return f'{self.imone} #{self.pk}'


class ImonesPaslauga(models.Model):
    """Serviso paslauga su kaina ir trukme.

    Modelis paruoštas 1 etape, nes jis aprašytas kartu su įmone; sąrašo
    pildymo forma ir servisų registracija — 2 etapas.
    """
    imone = models.ForeignKey(Imone, on_delete=models.CASCADE,
                              related_name='paslaugos')
    pavadinimas = models.CharField(max_length=160)
    aprasymas = models.CharField(max_length=255, blank=True)
    trukme_min = models.PositiveIntegerField(null=True, blank=True,
                                             verbose_name=_('Trukmė (min.)'))
    kaina = models.DecimalField(max_digits=9, decimal_places=2,
                                null=True, blank=True)
    tvarka = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tvarka', 'id']
        verbose_name = _('Įmonės paslauga')
        verbose_name_plural = _('Įmonės paslaugos')

    def __str__(self):
        return self.pavadinimas
