
from django.db import models

from django.conf import settings





class PageView(models.Model):

    """Site-wide visitor tracking - loguoja kiekviena apsilankyma."""

    ip_address = models.GenericIPAddressField(db_index=True)

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

            models.Index(fields=['ip_address', 'created_at']),

            models.Index(fields=['is_bot', 'created_at']),

        ]



    def __str__(self):

        tag = '🤖' if self.is_bot else '👤'

        return f"{tag} {self.ip_address} -> {self.path}"

