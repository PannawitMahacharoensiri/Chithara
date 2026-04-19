from django.urls import path
from .views import generate_music

urlpatterns = [
    path("generate/", generate_music, name="generate_music"),
]