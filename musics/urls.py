from django.urls import path
from .views import generate_music, list_music, music_detail

urlpatterns = [
    path("generate/", generate_music, name="generate_music"),
    path("", list_music, name="music_list"),
    path("<int:id>/", music_detail, name="music_detail"),
]