from django.contrib import admin
from musics.models.genre_model import Genre
from musics.models.mood_model import Mood
from musics.models.music_model import Music

admin.site.register(Music)
admin.site.register(Mood)
admin.site.register(Genre)