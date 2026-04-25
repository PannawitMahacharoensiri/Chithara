from django.contrib import admin
from musics.models.genre_model import Genre
from musics.models.mood_model import Mood
from musics.models.music_model import Music

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ("display_name", "owner", "generate_state", "created_at")
    readonly_fields = ("created_at",)
    list_filter = ("generate_state", "generator_strategy", "created_at")

admin.site.register(Mood)
admin.site.register(Genre)