from django.db import models

class GenerateStrategy(models.TextChoices):
    SUNO = "suno", "Suno API"
    MOCK = "mock", "Mock Generator"
