from django.db import models
from musics.enums.generate_state_enum import GenerateState
from musics.enums.generate_strategy_enum import GenerateStrategy



class Music(models.Model):
    display_name = models.CharField(max_length=100)
    task_id = models.CharField(max_length=100, null=True, blank=True)
    audio_url = models.URLField(max_length=500, null=True, blank=True)
    genre = models.ForeignKey("Genre", on_delete=models.SET_NULL, null=True)
    mood = models.ForeignKey("Mood", on_delete=models.SET_NULL, null=True)
    usage_occupation = models.CharField(max_length=100, blank=True)
    vocal_preference = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    generate_state = models.CharField(max_length=20, choices=GenerateState.choices)
    generator_strategy = models.CharField(max_length=20, choices=GenerateStrategy.choices, default="suno")
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey("accounts.User",on_delete=models.CASCADE,related_name="musics")

    def __str__(self):
        return self.display_name