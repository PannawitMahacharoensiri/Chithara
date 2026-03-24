from django.contrib import admin
from musics.models.GenreModel import Genre
from musics.models.MoodModel import Mood
from musics.models.MusicModel import Music

admin.site.register(Music)
admin.site.register(Mood)
admin.site.register(Genre)