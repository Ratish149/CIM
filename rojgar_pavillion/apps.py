from django.apps import AppConfig


class RojgarPavillionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rojgar_pavillion'

    def ready(self):
        import rojgar_pavillion.signals
