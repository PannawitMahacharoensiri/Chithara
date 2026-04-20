from django.urls import path
from .views import generate_music, library_music, music_detail, check_music_status, overview_music, cancel_music

urlpatterns = [
    path("generate/", generate_music, name="generate_music"),
    path("", library_music, name="music_list"),
    path("<int:id>/", music_detail, name="music_detail"),
    path("<int:id>/check/", check_music_status, name="check_music_status"),
    path("<int:id>/overview/", overview_music, name="overview_music"),
    path("<int:id>/cancel/", cancel_music, name="cancel_music"),
]