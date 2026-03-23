from django.db import models
from .utilities.validators import validate_audio_file, validate_file_size

# Enumerations
class Genre(models.TextChoices):
    POP = "POP", "Pop"
    ROCK = "ROCK", "Rock"
    JAZZ = "JAZZ", "Jazz"
    CLASSICAL = "CLASSICAL", "Classical"
    METAL = "METAL", "Metal"
    COUNTRY = "COUNTRY", "Country"

class Mood(models.TextChoices):
    AMBITIOUS = "AMBITIOUS", "Ambitious"
    ANXIOUS = "ANXIOUS", "Anxious"
    CALM = "CALM", "Calm"
    CHEERFUL = "CHEERFUL", "Cheerful"
    EXCITED = "EXCITED", "Excited"
    HEARTBROKEN = "HEARTBROKEN", "Heartbroken"

class GenerateState(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"
    CANCELED = "CANCELED", "Canceled"

# Main music model
class Music(models.Model):
    display_name = models.CharField(max_length=100)
    audio_file = models.FileField(
        upload_to="music/",
        validators=[validate_audio_file, validate_file_size]
    )
    genre = models.CharField(max_length=20, choices=Genre.choices)
    mood = models.CharField(max_length=20, choices=Mood.choices)
    usage_occupation = models.CharField(max_length=100, blank=True)
    vocal_preference = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    generate_state = models.CharField(max_length=20, choices=GenerateState.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("accounts.User",on_delete=models.CASCADE,related_name="musics")

    def __str__(self):
        return self.display_name