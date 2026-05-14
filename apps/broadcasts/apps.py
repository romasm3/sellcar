from django.apps import AppConfig


class BroadcastsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.broadcasts'
    verbose_name = 'Pranešimai (Broadcasts)'

    def ready(self):
        from config import admin as _admin  # noqa: F401