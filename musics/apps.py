from django.apps import AppConfig

class MusicsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'musics'

    def ready(self):
        import musics.utilities.create_default_music
