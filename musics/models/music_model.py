from django.db import models
from .genre_model import Genre
from .mood_model import Mood
from musics.enums.generate_state_enum import GenerateState
from musics.utilities.validators import validate_audio_file, validate_file_size


class Music(models.Model):
    display_name = models.CharField(max_length=100)
    task_id = models.CharField(max_length=100, null=True, blank=True)
    audio_file = models.FileField(
        upload_to="music/",
        validators=[validate_audio_file, validate_file_size],
        null=True,
        blank=True,
    )
    genre = models.ForeignKey("Genre", on_delete=models.SET_NULL, null=True)
    mood = models.ForeignKey("Mood", on_delete=models.SET_NULL, null=True)
    usage_occupation = models.CharField(max_length=100, blank=True)
    vocal_preference = models.CharField(max_length=100, blank=True)
    generate_description = models.TextField(blank=True)
    generate_state = models.CharField(max_length=20, choices=GenerateState.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("accounts.User",on_delete=models.CASCADE,related_name="musics")

    def __str__(self):
        return self.display_name