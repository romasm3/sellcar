"""Pokalbiai Django administravime — TIK METADUOMENYS, tik skaitymas.

Žinučių turinys čia NErodomas, neieškomas ir neredaguojamas: jį
atidaryti galima tik per /administracija/pokalbiai/<id>/, nurodžius
priežastį, ir kiekviena peržiūra įrašoma į PokalbioPerziura. Anksčiau
čia buvo redaguojamas žinučių sąrašas ir paieška pagal turinį — tai
leido skaityti (ir keisti) susirašinėjimą be jokio pėdsako.
"""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (Conversation, ConversationTranslation, Message,
                     MessageTranslation, PokalbioPerziura)


class TikSkaitymas:
    """Nei pridėti, nei keisti, nei trinti — tik sąrašas ir peržiūra."""

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MessageInline(TikSkaitymas, admin.TabularInline):
    model = Message
    extra = 0
    fields = ('sender', 'ar_tekstas', 'ar_foto', 'is_read', 'created_at')
    readonly_fields = fields
    can_delete = False

    @admin.display(description='Tekstas', boolean=True)
    def ar_tekstas(self, obj):
        return bool(obj.content)

    @admin.display(description='Foto', boolean=True)
    def ar_foto(self, obj):
        return bool(obj.image)


@admin.register(Conversation)
class ConversationAdmin(TikSkaitymas, admin.ModelAdmin):
    list_display = ('id', 'skelbimas', 'dalyviai', 'zinuciu', 'updated_at', 'perziura')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('participants__email', 'participants__username',
                     'listing__title')
    date_hierarchy = 'updated_at'
    inlines = [MessageInline]

    @admin.display(description='Skelbimas')
    def skelbimas(self, obj):
        return obj.listing or '— pagalba —'

    @admin.display(description='Dalyviai')
    def dalyviai(self, obj):
        return ', '.join(u.email or u.username for u in obj.participants.all())

    @admin.display(description='Žinučių')
    def zinuciu(self, obj):
        return obj.messages.count()

    @admin.display(description='Turinys')
    def perziura(self, obj):
        return format_html('<a href="{}">{}</a>',
                           reverse('pokalbiu_perziura:gija', args=[obj.pk]),
                           'Peržiūra su priežastimi →')


@admin.register(Message)
class MessageAdmin(TikSkaitymas, admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'ar_tekstas', 'ar_foto',
                    'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__email', 'sender__username')
    date_hierarchy = 'created_at'
    fields = ('conversation', 'sender', 'is_read', 'created_at')
    readonly_fields = fields

    @admin.display(description='Tekstas', boolean=True)
    def ar_tekstas(self, obj):
        return bool(obj.content)

    @admin.display(description='Foto', boolean=True)
    def ar_foto(self, obj):
        return bool(obj.image)


@admin.register(MessageTranslation)
class MessageTranslationAdmin(TikSkaitymas, admin.ModelAdmin):
    list_display = ('message', 'target_lang', 'detected_source_lang', 'created_at')
    list_filter = ('target_lang', 'detected_source_lang')
    fields = ('message', 'target_lang', 'detected_source_lang', 'created_at')
    readonly_fields = fields


@admin.register(ConversationTranslation)
class ConversationTranslationAdmin(admin.ModelAdmin):
    list_display = ('user', 'conversation', 'enabled', 'updated_at')
    list_filter = ('enabled',)
    raw_id_fields = ('user', 'conversation')


@admin.register(PokalbioPerziura)
class PokalbioPerziuraAdmin(TikSkaitymas, admin.ModelAdmin):
    """Žurnalas — tik skaitomas, net superadministratoriui."""
    list_display = ('kada', 'perziurejo_el_pastas', 'pokalbio_nr', 'priezastis')
    list_filter = ('priezastis', 'kada')
    search_fields = ('perziurejo_el_pastas', 'pokalbio_nr', 'paaiskinimas')
    readonly_fields = ('kada', 'perziurejo', 'perziurejo_el_pastas', 'pokalbis',
                       'pokalbio_nr', 'dalyviai', 'priezastis', 'paaiskinimas', 'ip')
    fields = readonly_fields

    def get_actions(self, request):
        return {}                                   # be „ištrinti pažymėtus"
