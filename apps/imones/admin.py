# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Imone, ImonesNuotrauka, ImonesPaslauga, VeiklosSritis


class NuotraukuInline(admin.TabularInline):
    model = ImonesNuotrauka
    extra = 1


class PaslauguInline(admin.TabularInline):
    model = ImonesPaslauga
    extra = 0


@admin.register(Imone)
class ImoneAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'tipas', 'miestas', 'patvirtinta',
                    'testine', 'sukurta')
    list_filter = ('tipas', 'patvirtinta', 'testine', 'miestas', 'veiklos')
    search_fields = ('pavadinimas', 'adresas', 'miestas', 'telefonas', 'el_pastas')
    list_editable = ('patvirtinta',)
    prepopulated_fields = {'slug': ('pavadinimas',)}
    filter_horizontal = ('veiklos',)
    inlines = [NuotraukuInline, PaslauguInline]
    fieldsets = (
        (None, {'fields': ('tipas', 'pavadinimas', 'slug', 'savininkas',
                           'patvirtinta', 'testine')}),
        ('Turinys', {'fields': ('logotipas', 'aprasymas', 'veiklos', 'veikia_nuo',
                                'reitingas', 'atsiliepimu_kiekis')}),
        ('Vieta', {'fields': ('adresas', 'rajonas', 'miestas', 'salis',
                              'latitude', 'longitude')}),
        ('Kontaktai', {'fields': ('telefonas', 'el_pastas', 'svetaine')}),
        ('Darbo laikas', {'fields': ('darbo_laikas',),
                          'description': 'Pvz. {"0": ["08:00", "18:00"], '
                                         '"6": null} — 0 pirmadienis, 6 sekmadienis.'}),
    )


@admin.register(VeiklosSritis)
class VeiklosSritisAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'slug', 'ikona', 'grupe', 'tvarka')
    prepopulated_fields = {'slug': ('pavadinimas',)}
