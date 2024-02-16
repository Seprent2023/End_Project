from django.apps import AppConfig


class PostboardMainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PostBoard_main'

    def ready(self):
        from . import signals

