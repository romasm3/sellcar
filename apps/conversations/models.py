from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    """Pokalbis tarp dviejų vartotojų dėl skelbimo"""
    participants = models.ManyToManyField(
        User,
        related_name='conversations'
    )
    listing = models.ForeignKey(
        'listings.Listing',
        on_delete=models.CASCADE,
        related_name='conversations',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation #{self.id} about {self.listing}"

    def get_other_participant(self, user):
        return self.participants.exclude(id=user.id).first()

    def get_last_message(self):
        return self.messages.order_by('-created_at').first()

    def unread_count(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()

    class Meta:
        ordering = ['-updated_at']


class Message(models.Model):
    """Žinutė pokalbyje"""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='conversation_images/%Y/%m/',
        null=True,
        blank=True
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.created_at}"

    class Meta:
        ordering = ['created_at']


# ═══════════════════════════════════════════════════════════════════════════
# TRANSLATION CACHE — kad to paties teksto neperverstų kelis kartus
# ═══════════════════════════════════════════════════════════════════════════

class MessageTranslation(models.Model):
    """Cache: žinutės vertimas į konkrečią kalbą.
    Vienas Message + viena target_lang = unique.
    Kai pirmą kartą kviečiamas Google API, rezultatas saugomas čia.
    Kitą kartą — iš DB, ne iš API (taupom kvotą)."""

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='translations',
    )
    target_lang = models.CharField(
        max_length=10,
        help_text="ISO kalbos kodas: 'en', 'de', 'es', 'lt', etc.",
    )
    translated_text = models.TextField()
    detected_source_lang = models.CharField(
        max_length=10, blank=True,
        help_text="Google'o auto-detected šaltinio kalba",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['message', 'target_lang']
        indexes = [
            models.Index(fields=['message', 'target_lang']),
        ]
        verbose_name = "Message Translation"
        verbose_name_plural = "Message Translations"

    def __str__(self):
        return f"Msg #{self.message_id} → {self.target_lang}"