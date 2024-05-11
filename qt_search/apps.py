from django.apps import AppConfig


class SpSearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qt_search'

    def ready(self):
        from . import signals
