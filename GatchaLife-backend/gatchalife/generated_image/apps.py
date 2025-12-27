from django.apps import AppConfig


class GeneratedImageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gatchalife.generated_image'

    def ready(self):
        import gatchalife.generated_image.handlers
