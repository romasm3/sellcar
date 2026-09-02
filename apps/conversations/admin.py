from django.contrib import admin

from .models import (Conversation, ConversationTranslation, Message,
                     MessageTranslation)


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ('sender', 'content', 'image', 'is_read', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'skelbimas', 'dalyviai', 'zinuciu', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('participants__email', 'participants__username',
                     'listing__title')
    filter_horizontal = ('participants',)
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


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'trumpai', 'ar_foto',
                    'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('content', 'sender__email', 'sender__username')
    date_hierarchy = 'created_at'
    raw_id_fields = ('conversation', 'sender')

    @admin.display(description='Tekstas')
    def trumpai(self, obj):
        return (obj.content or '')[:60]

    @admin.display(description='Foto', boolean=True)
    def ar_foto(self, obj):
        return bool(obj.image)


@admin.register(MessageTranslation)
class MessageTranslationAdmin(admin.ModelAdmin):
    list_display = ('message', 'target_lang', 'detected_source_lang', 'created_at')
    list_filter = ('target_lang', 'detected_source_lang')
    raw_id_fields = ('message',)


@admin.register(ConversationTranslation)
class ConversationTranslationAdmin(admin.ModelAdmin):
    list_display = ('user', 'conversation', 'enabled', 'updated_at')
    list_filter = ('enabled',)
    raw_id_fields = ('user', 'conversation')
